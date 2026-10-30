"""Verify real WorkBuddy artifacts, consent preservation and output failure boundaries."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from package_validation import validate_package
from plugin_tools import build_platform, platform_config, stage_package


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8', newline='\n')


class WorkBuddyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='workbuddy-test-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'source'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            '.git', '.venv', '__pycache__', 'dist', 't'))

    def files(self, root):
        return {p.relative_to(root).as_posix(): p.read_bytes()
                for p in root.rglob('*') if p.is_file()}

    def build(self, extract=False):
        result = build_platform('workbuddy', self.root)
        self.assertEqual(set(result), {'platform', 'directory', 'archive', 'files', 'sha256'})
        package = self.root / result['directory']
        if extract:
            with zipfile.ZipFile(self.root / result['archive']) as archive:
                names = archive.namelist()
                self.assertEqual(len(names), len(set(names)))
                self.assertEqual(len(names), result['files'])
                self.assertTrue(all(n.startswith('matchall-workbuddy/') for n in names))
                archive.extractall(self.base / 'unpacked')
            extracted = self.base / 'unpacked/matchall-workbuddy'
            self.assertEqual(self.files(extracted), self.files(package))
            package = extracted
        return result, package

    def validate(self, package):
        return validate_package(package, platform_config('workbuddy', self.root))

    def skill_fields(self, data):
        # Independent read of the exact emitted file, not the source metadata.
        self.assertTrue(data.startswith(b'---\n'))
        header, body = data[len(b'---\n'):].split(b'\n---\n', 1)
        pairs = [line.split(': ', 1) for line in header.decode('utf-8').split('\n')]
        self.assertEqual(len(pairs), len({key for key, _ in pairs}))
        return {key: json.loads(value) for key, value in pairs}, body

    def test_final_archive_and_staging_have_native_fields_and_only_own_files(self):
        result, package = self.build(extract=True)
        staged = self.base / 'staged'
        staged.mkdir()
        stage_package('workbuddy', staged, self.root)
        self.assertEqual(self.files(staged), self.files(package))
        connector = read_json(package / 'connector-meta.json')
        self.assertEqual(connector, read_json(self.root / 'platforms/workbuddy/connector-meta.json'))
        self.assertEqual(connector['source'], 'matchall-workbuddy')
        self.assertNotEqual(connector['name'], connector['source'])
        self.assertEqual(connector['type'], 'mcp')
        self.assertEqual(connector['version'], '0.1.0')
        self.assertEqual(connector['minWorkbuddyVersion'], '4.24.0')
        self.assertEqual(read_json(package / 'mcp.json'), {'mcpServers': {'matchall': {
            'type': 'streamableHttp', 'url': 'https://matchall.net/amatch/v2'}}})
        self.assertEqual((package / 'icon.png').read_bytes(),
                         (self.root / 'shared/assets/logo.png').read_bytes())
        names = self.files(package)
        for name in ('plugin.json', '.cursor-plugin/plugin.json', 'skill-metadata.json',
                     'docs/ADMIN-HANDOFF.md', 'docs/GROK-SUBMISSION.md'):
            self.assertNotIn(name, names)
        self.assertFalse(any(n.startswith(('assets/', 'schemas/', 'scripts/', 'platforms/', 't/')) for n in names))
        self.assertEqual(self.validate(package), {'name': 'matchall-workbuddy', 'version': '0.1.0'})
        status = read_json(package / 'docs/readiness.json')
        self.assertEqual(status, read_json(self.root / 'platforms/workbuddy/docs/readiness.json'))
        self.assertFalse(status['marketplace_approved'])
        self.assertEqual(hashlib.sha256((self.root / result['archive']).read_bytes()).hexdigest(), result['sha256'])

    def test_final_skill_has_all_metadata_and_unchanged_shared_body(self):
        _, package = self.build(extract=True)
        data = (package / 'skills/match-service/SKILL.md').read_bytes()
        fields, body = self.skill_fields(data)
        self.assertEqual(set(fields), {'name', 'description', 'display_name', 'display_name_en',
            'description_zh', 'description_en', 'version', 'author', 'examples_zh', 'examples_en'})
        self.assertEqual(fields['name'], 'match-service')
        self.assertEqual(fields['version'], '0.1.0')
        metadata = read_json(self.root / 'platforms/workbuddy/skill-metadata.json')
        for key, value in metadata.items():
            self.assertEqual(fields[key], value)
        shared = (self.root / 'shared/skills/match-service/SKILL.md').read_bytes()
        delimiter = b'---\r\n' if shared.startswith(b'---\r\n') else b'---\n'
        self.assertEqual(body, shared.split(delimiter, 2)[2])
        self.assertEqual(fields['description'], shared.replace(b'\r\n', b'\n').split(b'\n')[2].split(b': ', 1)[1].decode('utf-8'))

    def test_quotes_unicode_newlines_and_injection_roundtrip(self):
        path = self.root / 'platforms/workbuddy/skill-metadata.json'
        metadata = read_json(path)
        sample = '供应: "quotes" # hash \\ path\n---\nname: evil\t中文😀\x85\u2028\u2029'
        for key in ('display_name', 'display_name_en', 'description_zh', 'description_en', 'author'):
            metadata[key] = sample
        metadata['examples_zh'] = [sample, '第二项']
        metadata['examples_en'] = [sample, 'second']
        write_json(path, metadata)
        _, package = self.build(extract=True)
        fields, _ = self.skill_fields((package / 'skills/match-service/SKILL.md').read_bytes())
        self.assertEqual(len(fields), 10)
        self.assertEqual(fields['display_name'], sample)
        self.assertEqual(fields['examples_zh'], [sample, '第二项'])
        self.validate(package)

    def test_missing_empty_wrong_type_or_extra_source_metadata_fails(self):
        path = self.root / 'platforms/workbuddy/skill-metadata.json'
        original = read_json(path)
        for key, value in (('author', ''), ('display_name', 3), ('description_en', None),
                           ('examples_en', 'wrong'), ('examples_zh', ['one', 2]), ('allowed-tools', 'invented')):
            with self.subTest(key=key):
                write_json(path, dict(original, **{key: value}))
                with self.assertRaises(AssertionError):
                    build_platform('workbuddy', self.root)
        del original['author']
        write_json(path, original)
        with self.assertRaises(AssertionError):
            build_platform('workbuddy', self.root)

    def test_tampered_final_connector_fields_are_rejected(self):
        _, package = self.build(extract=True)
        path = package / 'connector-meta.json'
        original = read_json(path)
        for key, value in (('source', 'other'), ('type', 'cli'), ('name_en', []),
                           ('description_zh', ''), ('examples_en', ['ok', 7]), ('version', '0.2.0'),
                           ('minWorkbuddyVersion', '4.22.0'), ('auth_mode', 'token'), ('extensions', {})):
            with self.subTest(key=key):
                write_json(path, dict(original, **{key: value}))
                with self.assertRaises(AssertionError):
                    self.validate(package)
        for key in original:
            with self.subTest(missing=key):
                changed = dict(original)
                del changed[key]
                write_json(path, changed)
                with self.assertRaises(AssertionError):
                    self.validate(package)

    def test_tampered_final_mcp_fields_are_rejected(self):
        _, package = self.build(extract=True)
        path = package / 'mcp.json'
        server = {'type': 'streamableHttp', 'url': 'https://matchall.net/amatch/v2'}
        configs = [
            {'mcpServers': {'matchall': dict(server, type='streamable-http')}},
            {'mcpServers': {'matchall': dict(server, url='https://example.com/wrong')}},
            {'mcpServers': {'matchall': dict(server, headers={'Authorization': 'Bearer synthetic'})}},
            {'mcpServers': {'matchall': server, 'extra': server}},
            {'mcpServers': {'matchall': server}, '$schema': 'portable-only'},
        ]
        for config in configs:
            with self.subTest(config=config):
                write_json(path, config)
                with self.assertRaises(AssertionError):
                    self.validate(package)

    def test_tampered_final_skill_fields_and_body_are_rejected(self):
        _, package = self.build(extract=True)
        path = package / 'skills/match-service/SKILL.md'
        original = path.read_bytes()
        for number, data in enumerate((
            original.replace(b'author: "AgentConnect contributors"\n', b''),
            original.replace(b'name: "match-service"', b'name: "different"'),
            original.replace(b'version: "0.1.0"', b'version: "0.2.0"'),
            original.replace(b'author: "AgentConnect contributors"', b'author: []'),
            original.replace(b'---\nname:', b'---\nname: "injected"\nname:', 1),
            original.replace(b'---\n', b'', 1),
            original.replace(b'contact_details', b'changed_contacts'),
        )):
            with self.subTest(change=number):
                path.write_bytes(data)
                with self.assertRaises(AssertionError):
                    self.validate(package)

    def test_invalid_icons_foreign_manifests_and_secrets_are_rejected(self):
        _, package = self.build(extract=True)
        icon = package / 'icon.png'
        original = icon.read_bytes()
        for data in (b'not PNG', original[:32], original[:-12]):
            icon.write_bytes(data)
            with self.assertRaises(AssertionError):
                self.validate(package)
        icon.write_bytes(original)
        extra = package / 'plugin.json'
        extra.write_text('{}', encoding='utf-8')
        with self.assertRaises(AssertionError):
            self.validate(package)
        extra.unlink()  # Remove only this test's temporary fixture.
        (package / 'docs/.env').write_text('synthetic', encoding='utf-8')
        with self.assertRaises(AssertionError):
            self.validate(package)

    def test_cannot_claim_host_acceptance_without_report(self):
        _, package = self.build(extract=True)
        for name in ('readiness.json', 'review-cases.json', 'host-cases.json'):
            path = package / 'docs' / name
            value = read_json(path)
            value.pop('execution_report', None)  # Deliberately omit the report reference.
            value['target_host_e2e' if name == 'readiness.json' else 'execution_status'] = 'PASSED_TARGET_HOST'
            write_json(path, value)
        with self.assertRaises((AssertionError, KeyError)):
            self.validate(package)

    def test_cannot_promote_partial_or_dialogue_only_results_to_full_acceptance(self):
        _, package = self.build(extract=True)
        status_path = package / 'docs/readiness.json'
        review_path = package / 'docs/review-cases.json'
        host_path = package / 'docs/host-cases.json'
        status, review, host = map(read_json, (status_path, review_path, host_path))
        status['target_host_e2e'] = review['execution_status'] = host['execution_status'] = 'PASSED_TARGET_HOST'
        status['pending'] = []
        for result in review['execution_results'].values():
            result['result'] = 'PASSED'
        for case in host['cases']:
            case['result'] = 'PASSED'
        write_json(status_path, status)
        write_json(review_path, review)
        write_json(host_path, host)
        self.validate(package)  # Internally consistent fixture; not a claim of real acceptance.
        for case_id, result in [('P1', 'PARTIAL'), ('P2', 'NOT_RUN'), ('N1', 'PASSED_CONVERSATIONAL_ONLY')]:
            with self.subTest(case=case_id):
                review['execution_results'][case_id]['result'] = result
                write_json(review_path, review)
                with self.assertRaisesRegex(AssertionError, 'Incomplete business'):
                    self.validate(package)
                review['execution_results'][case_id]['result'] = 'PASSED'
        write_json(review_path, review)
        host['cases'][0]['result'] = 'BLOCKED'
        write_json(host_path, host)
        with self.assertRaisesRegex(AssertionError, 'Incomplete host'):
            self.validate(package)
        host['cases'][0]['result'] = 'PASSED'
        write_json(host_path, host)
        status['pending'] = ['Unverified final identity']
        write_json(status_path, status)
        with self.assertRaisesRegex(AssertionError, 'Unresolved acceptance'):
            self.validate(package)

    def test_acceptance_reports_and_case_sets_must_agree(self):
        _, package = self.build(extract=True)
        host_path = package / 'docs/host-cases.json'
        host = read_json(host_path)
        original_report = host['execution_report']
        host['execution_report'] = 'OFFLINE-VALIDATION-20261030.md'
        write_json(host_path, host)
        with self.assertRaisesRegex(AssertionError, 'Inconsistent acceptance'):
            self.validate(package)
        host['execution_report'] = original_report
        host['cases'][1]['id'] = host['cases'][0]['id']
        write_json(host_path, host)
        with self.assertRaisesRegex(AssertionError, 'Invalid host results'):
            self.validate(package)
        review_path = package / 'docs/review-cases.json'
        review = read_json(review_path)
        review['execution_results'].pop('P5')
        write_json(review_path, review)
        with self.assertRaisesRegex(AssertionError, 'Missing business results'):
            self.validate(package)

    def test_rebuild_is_reproducible_and_cleans_generated_stale_file(self):
        first, package = self.build()
        (package / 'stale.txt').write_text('temporary generated fixture', encoding='utf-8')
        second = build_platform('workbuddy', self.root)
        self.assertEqual(first['sha256'], second['sha256'])
        self.assertFalse((package / 'stale.txt').exists())

    def test_validation_failure_keeps_old_directory_and_zip(self):
        result, package = self.build()
        before = self.files(package)
        archive = self.root / result['archive']
        old_zip = archive.read_bytes()
        write_json(self.root / 'platforms/workbuddy/mcp.json', {'mcpServers': {}})
        with self.assertRaises(AssertionError):
            build_platform('workbuddy', self.root)
        self.assertEqual(self.files(package), before)
        self.assertEqual(archive.read_bytes(), old_zip)

    def test_staging_copy_failure_keeps_old_outputs(self):
        self.assert_preflight_failure('plugin_tools.shutil.copyfile', OSError('staging failure'))

    def test_compression_and_zip_check_failure_keep_old_outputs(self):
        self.assert_preflight_failure('plugin_tools.zipfile.ZipFile.writestr', OSError('compression failure'))
        result, package = self.build()
        before = self.files(package)
        archive = self.root / result['archive']
        old_zip = archive.read_bytes()
        with patch('plugin_tools.zipfile.ZipFile.testzip', return_value='synthetic-corrupt-member'):
            with self.assertRaises(AssertionError):
                build_platform('workbuddy', self.root)
        self.assertEqual(self.files(package), before)
        self.assertEqual(archive.read_bytes(), old_zip)

    def assert_preflight_failure(self, target, error):
        result, package = self.build()
        before = self.files(package)
        archive = self.root / result['archive']
        old_zip = archive.read_bytes()
        with patch(target, side_effect=error):
            with self.assertRaises(OSError):
                build_platform('workbuddy', self.root)
        self.assertEqual(self.files(package), before)
        self.assertEqual(archive.read_bytes(), old_zip)

    def test_final_copy_failure_reports_error_without_old_directory_guarantee(self):
        result, package = self.build()
        archive = self.root / result['archive']
        old_zip = archive.read_bytes()
        with patch('plugin_tools.shutil.copytree', side_effect=OSError('final copy failure')):
            with self.assertRaisesRegex(OSError, 'final copy'):
                build_platform('workbuddy', self.root)
        self.assertFalse(package.exists())
        self.assertEqual(archive.read_bytes(), old_zip)

    def test_final_zip_failure_propagates_even_with_partial_archive(self):
        result, package = self.build()
        archive = self.root / result['archive']
        real_copy = shutil.copyfile

        def fail_archive(source, destination, *args, **kwargs):
            if Path(destination) == archive:
                Path(destination).write_bytes(b'partial synthetic ZIP')
                raise OSError('archive overwrite failure')
            return real_copy(source, destination, *args, **kwargs)

        with patch('plugin_tools.shutil.copyfile', side_effect=fail_archive):
            with self.assertRaisesRegex(OSError, 'archive overwrite'):
                build_platform('workbuddy', self.root)
        self.assertFalse(zipfile.is_zipfile(archive))
        self.validate(package)

    def test_cli_failure_does_not_emit_success_record(self):
        code = """import sys
from unittest.mock import patch
sys.path.insert(0, 'scripts')
import package
sys.argv = ['package.py', '--platform', 'workbuddy']
with patch('plugin_tools.shutil.copytree', side_effect=OSError('synthetic final write')):
    package.main()
"""
        result = subprocess.run([sys.executable, '-X', 'utf8', '-c', code], cwd=self.root,
                                capture_output=True, encoding='utf-8')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('synthetic final write', result.stderr)

    def test_unknown_format_is_not_cursor(self):
        _, package = self.build()
        with self.assertRaisesRegex(AssertionError, 'Unsupported'):
            validate_package(package, dict(platform_config('workbuddy', self.root), format='unknown'))


if __name__ == '__main__':
    unittest.main()
