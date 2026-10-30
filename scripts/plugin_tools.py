"""Assemble independent host packages from one shared Matchall source tree."""
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from package_validation import (require_no_links, validate_package,
                                render_workbuddy_skill, split_shared_skill)

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = {"agent-plugins": "plugin.json", "cursor": ".cursor-plugin/plugin.json",
             "workbuddy": "connector-meta.json"}


def load_platforms(root=ROOT):
    platforms = json.loads((root / "platforms.json").read_text(encoding="utf-8"))
    assert isinstance(platforms, dict) and platforms, "Empty platform registry"
    names = set()
    for platform_id, config in platforms.items():
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", platform_id), "Invalid platform ID"
        assert platform_id != "all", "Platform ID 'all' is reserved for the CLI"
        assert set(config) == {"name", "format"}, "Unexpected platform settings"
        assert config["format"] in MANIFESTS, "Unsupported package format"
        name = config["name"]
        assert isinstance(name, str) and len(name) <= 64
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name), "Invalid package name"
        assert name not in names, "Duplicate package name would overwrite another platform"
        names.add(name)
    return platforms


def platform_config(platform_id, root=ROOT):
    platforms = load_platforms(root)
    if platform_id not in platforms:
        raise ValueError(f"Unknown platform: {platform_id}; choose {', '.join(platforms)}")
    return dict(platforms[platform_id], id=platform_id)


def package_files(platform_id, root=ROOT):
    """Explicit source-to-package map; never recurse over the repository root."""
    platform = platform_config(platform_id, root)
    source = root / "platforms" / platform_id
    for directory in (source, root / "shared", root / "schemas"):
        require_no_links(directory)
    files = {"LICENSE": root / "LICENSE"}
    for name in ("README.md", "mcp.json", MANIFESTS[platform["format"]]):
        files[name] = source / name
    if platform["format"] == "workbuddy":
        files["icon.png"] = root / "shared/assets/logo.png"
    for directory in ("assets", "skills"):
        if platform["format"] == "workbuddy" and directory == "assets":
            continue
        shared = root / "shared" / directory
        for path in shared.rglob("*"):
            if path.is_file():
                files[str(PurePosixPath(directory) / path.relative_to(shared).as_posix())] = path
    for directory, base in (("docs", source), ("schemas", root)):
        if directory == "schemas" and platform["format"] != "agent-plugins":
            continue
        for path in (base / directory).rglob("*"):
            if path.is_file():
                files[path.relative_to(base).as_posix()] = path
    for name, path in files.items():
        assert not path.is_symlink() and path.is_file(), f"Missing or linked source: {name}"
        assert path.resolve().is_relative_to(root.resolve()), f"Source outside repository: {name}"
    return dict(sorted(files.items()))


def stage_package(platform_id, destination, root=ROOT):
    """Materialize the runtime layout without symlinks or sibling platforms."""
    for name, source in package_files(platform_id, root).items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    if platform_config(platform_id, root)["format"] == "workbuddy":
        source = root / "platforms" / platform_id
        metadata = json.loads((source / "skill-metadata.json").read_text(encoding="utf-8"))
        connector = json.loads((destination / "connector-meta.json").read_text(encoding="utf-8"))
        skill = destination / "skills/match-service/SKILL.md"
        original = skill.read_bytes()
        shared_fields, body = split_shared_skill(original)
        skill.write_bytes(render_workbuddy_skill(original, metadata, connector["version"]))
        integrity = destination / "docs/skill-integrity.json"
        assert not integrity.exists(), "Skill integrity record must be generated, not supplied"
        integrity.write_text(json.dumps(dict(shared_fields,
                             body_sha256=hashlib.sha256(body).hexdigest()),
                             ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return validate_package(destination, platform_config(platform_id, root))


def validate_platform(platform_id, root=ROOT):
    with tempfile.TemporaryDirectory(prefix="matchall-validate-") as temporary:
        return stage_package(platform_id, Path(temporary), root)


def build_platform(platform_id, root=ROOT):
    platform = platform_config(platform_id, root)
    output = root / "dist"
    assert not output.is_symlink(), "Output directory must not be a symlink"
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="matchall-build-") as temporary:
        staged = Path(temporary) / platform["name"]
        staged.mkdir()
        manifest = stage_package(platform_id, staged, root)
        files = sorted(path for path in staged.rglob("*") if path.is_file())
        archive_name = f'{manifest["name"]}-{manifest["version"]}-preparation.zip'
        archive_path = Path(temporary) / archive_name
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                name = str(PurePosixPath(manifest["name"]) / path.relative_to(staged).as_posix())
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
        with zipfile.ZipFile(archive_path) as archive:
            expected = {f'{manifest["name"]}/{path.relative_to(staged).as_posix()}': path for path in files}
            assert len(archive.namelist()) == len(expected)
            assert set(archive.namelist()) == set(expected)
            assert archive.testzip() is None
            for name, source in expected.items():
                assert archive.read(name) == source.read_bytes()
        target = output / manifest["name"]
        archive_target = output / archive_name
        require_no_links(target)
        assert not archive_target.is_symlink(), "Archive must not be a symlink"
        # Preflight failures preserve old outputs; final copies are not transactional.
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(staged, target)
        shutil.copyfile(archive_path, archive_target)
        return {
            "platform": platform_id,
            "directory": str(target.relative_to(root)),
            "archive": str(archive_target.relative_to(root)),
            "files": len(files),
            "sha256": hashlib.sha256(archive_target.read_bytes()).hexdigest(),
        }
