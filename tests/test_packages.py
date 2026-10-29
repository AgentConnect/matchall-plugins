"""Exercise real generated plugins, migration integrity and rejected inputs."""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from package_validation import validate_package
from plugin_tools import build_platform, load_platforms, platform_config, validate_platform


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="matchall-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "dist"))

    def test_each_archive_is_a_self_contained_platform_with_identical_shared_skill(self):
        for platform_id, manifest_path, absent_manifest, own_doc, other_doc in (
            ("chatgpt", "plugin.json", ".cursor-plugin/plugin.json", "docs/ADMIN-HANDOFF.md", "docs/GROK-SUBMISSION.md"),
            ("grok-bot", ".cursor-plugin/plugin.json", "plugin.json", "docs/GROK-SUBMISSION.md", "docs/ADMIN-HANDOFF.md"),
        ):
            with self.subTest(platform=platform_id):
                result = build_platform(platform_id, self.root)
                extracted = self.root / ("extracted-" + platform_id)
                with zipfile.ZipFile(self.root / result["archive"]) as archive:
                    names = archive.namelist()
                    self.assertEqual(len(names), len(set(names)))
                    self.assertTrue(all(name.startswith("matchall-" + platform_id + "/") for name in names))
                    self.assertFalse(any("/platforms/" in name or "/scripts/" in name for name in names))
                    archive.extractall(extracted)
                package = extracted / ("matchall-" + platform_id)
                self.assertTrue((package / manifest_path).is_file())
                self.assertFalse((package / absent_manifest).exists())
                self.assertTrue((package / own_doc).is_file())
                self.assertFalse((package / other_doc).exists())
                skill = "skills/match-service/SKILL.md"
                self.assertEqual((package / skill).read_bytes(), (self.root / "shared" / skill).read_bytes())
                self.assertEqual((package / "mcp.json").read_bytes(),
                                 (self.root / "platforms" / platform_id / "mcp.json").read_bytes())
                validate_package(package, platform_config(platform_id, self.root))

    def test_rebuild_removes_stale_files_and_is_reproducible(self):
        first = build_platform("grok-bot", self.root)
        package = self.root / first["directory"]
        (package / "stale.txt").write_text("must not survive")
        second = build_platform("grok-bot", self.root)
        self.assertFalse((package / "stale.txt").exists())
        self.assertEqual(first["sha256"], second["sha256"])

    def test_bad_config_does_not_replace_a_previous_good_package(self):
        result = build_platform("chatgpt", self.root)
        path = self.root / "platforms/chatgpt/mcp.json"
        config = json.loads(path.read_text())
        config["mcpServers"]["matchall"]["url"] = "https://example.com/wrong-service"
        write_json(path, config)
        with self.assertRaises(AssertionError):
            build_platform("chatgpt", self.root)
        self.assertEqual(hashlib.sha256((self.root / result["archive"]).read_bytes()).hexdigest(), result["sha256"])

    def test_rejects_a_shared_skill_symlink_before_reading_it(self):
        skill = self.root / "shared/skills/match-service/SKILL.md"
        skill.unlink()
        skill.symlink_to(ROOT / "shared/skills/match-service/SKILL.md")
        with self.assertRaisesRegex(AssertionError, "Symlink"):
            build_platform("grok-bot", self.root)

    def test_rejects_linked_output_without_writing_outside_repository(self):
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        (self.root / "dist").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(AssertionError, "symlink"):
            build_platform("chatgpt", self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_excludes_repository_secrets_but_rejects_secrets_in_packaged_docs(self):
        (self.root / ".env").write_text("local-only")
        result = build_platform("grok-bot", self.root)
        with zipfile.ZipFile(self.root / result["archive"]) as archive:
            self.assertFalse(any(name.endswith(".env") for name in archive.namelist()))
        (self.root / "platforms/grok-bot/docs/.env").write_text("do not package")
        with self.assertRaises(AssertionError):
            build_platform("grok-bot", self.root)

    def test_rejects_package_names_that_collide_or_escape_output(self):
        path = self.root / "platforms.json"
        registry = json.loads(path.read_text())
        registry["grok-bot"]["name"] = registry["chatgpt"]["name"]
        write_json(path, registry)
        with self.assertRaisesRegex(AssertionError, "Duplicate"):
            load_platforms(self.root)
        registry["grok-bot"]["name"] = "../outside"
        write_json(path, registry)
        with self.assertRaisesRegex(AssertionError, "Invalid"):
            load_platforms(self.root)

    def test_unknown_platform_fails_without_building_anything(self):
        with self.assertRaisesRegex(ValueError, "Unknown platform"):
            build_platform("unknown-host", self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_rejects_changed_schema_provenance(self):
        path = self.root / "schemas/agent-plugins-1.0.0/plugin.schema.json"
        path.write_text(path.read_text() + "\n")
        with self.assertRaises(AssertionError):
            validate_platform("chatgpt", self.root)

    def test_rejects_removed_public_visibility_consent_rules(self):
        skill = self.root / "shared/skills/match-service/SKILL.md"
        skill.write_text(skill.read_text().replace("data.public_preview", "preview"))
        for platform in load_platforms(self.root):
            with self.subTest(platform=platform), self.assertRaises(AssertionError):
                validate_platform(platform, self.root)

    def test_rejects_review_manifest_divergence(self):
        path = self.root / "platforms/chatgpt/docs/review-cases.json"
        cases = json.loads(path.read_text())
        cases["test_cases"]["positive"][0]["expected_behavior"] = "unexpected behavior"
        write_json(path, cases)
        with self.assertRaises(AssertionError):
            validate_platform("chatgpt", self.root)

    def test_new_portable_platform_uses_templates_without_inheriting_host_acceptance(self):
        path = self.root / "platforms.json"
        registry = json.loads(path.read_text())
        registry["example-host"] = {"name": "matchall-example-host", "format": "agent-plugins"}
        write_json(path, registry)
        source = self.root / "platforms/example-host"
        write_json(source / "plugin.json", {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "matchall-example-host", "version": "0.1.0",
            "description": "Match needs and offers with mutually consented introductions.",
            "repository": "https://github.com/AgentConnect/matchall-plugins", "license": "MIT",
        })
        (source / "README.md").write_text("# Example host\nHost integration has not been verified.\n")
        shutil.copyfile(self.root / "platforms/chatgpt/mcp.json", source / "mcp.json")
        (source / "docs").mkdir()
        for name in ("readiness.json", "review-cases.json"):
            shutil.copyfile(self.root / "templates" / name, source / "docs" / name)
        result = build_platform("example-host", self.root)
        package = self.root / result["directory"]
        readiness = json.loads((package / "docs/readiness.json").read_text())
        self.assertEqual(readiness["target_host_e2e"], "NOT_RUN_IN_TARGET_HOST")
        self.assertNotIn("extensions", json.loads((package / "plugin.json").read_text()))
        self.assertFalse((package / "docs/host-validation-2026-10-19.md").exists())


class MigrationTests(unittest.TestCase):
    def test_every_original_review_document_and_shared_asset_is_preserved(self):
        inventory = json.loads((ROOT / "docs/source-inventory.json").read_text())
        for platform, source in inventory["sources"].items():
            for name, digest in source["files"].items():
                if name.startswith(("assets/", "skills/")):
                    target = ROOT / "shared" / name
                elif name.startswith("docs/"):
                    target = ROOT / "platforms" / platform / name
                elif name.startswith("schemas/") or name in ("LICENSE", "requirements-dev.txt"):
                    target = ROOT / name
                elif name == "mcp.json":
                    target = ROOT / "platforms" / platform / name
                else:
                    continue
                with self.subTest(platform=platform, file=name):
                    self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest)

    def test_manifest_identity_version_prompts_and_review_metadata_are_preserved(self):
        inventory = json.loads((ROOT / "docs/source-inventory.json").read_text())
        for platform, path in (("chatgpt", "plugin.json"), ("grok-bot", ".cursor-plugin/plugin.json")):
            manifest = json.loads((ROOT / "platforms" / platform / path).read_text())
            self.assertEqual(manifest.pop("repository"), "https://github.com/AgentConnect/matchall-plugins")
            digest = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
            self.assertEqual(digest, inventory["sources"][platform]["manifest_semantic_sha256_excluding_repository"])


if __name__ == "__main__":
    unittest.main()
