"""Validate staged plugin packages offline, preserving platform review checks."""
import hashlib
import json
import re
import struct
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

import jsonschema

REPOSITORY = "https://github.com/AgentConnect/matchall-plugins"
IGNORED = {".git", ".venv", "__pycache__", "dist"}


def require_no_links(root):
    assert not root.is_symlink(), "Package root must not be a symlink"
    for path in root.rglob("*"):
        assert not path.is_symlink(), f"Symlink: {path.relative_to(root)}"


def validate_package(root, platform):
    root = Path(root)
    portable = platform['format'] == 'agent-plugins'
    require_no_links(root)
    manifest_path = root / ('plugin.json' if portable else '.cursor-plugin/plugin.json')
    manifest = json.loads(manifest_path.read_text())
    mcp = json.loads((root / 'mcp.json').read_text())
    expected_name = platform['name']
    assert manifest['name'] == expected_name
    assert re.fullmatch(r'\d+\.\d+\.\d+', manifest['version'])
    assert manifest['license'] == 'MIT'
    assert manifest['repository'] == REPOSITORY
    assert not any(k in manifest for k in ('apps', 'hooks'))
    assert (root / 'LICENSE').read_text().startswith('MIT License\n')
    expected_server = {'url': 'https://matchall.net/amatch/v2'}
    if portable:
        expected_server['type'] = 'streamable-http'
        for kind, value in (('plugin', manifest), ('mcp', mcp)):
            schema_root = root / 'schemas' / 'agent-plugins-1.0.0'
            provenance = json.loads((schema_root / 'provenance.json').read_text())
            record = next(s for s in provenance['sources']
                          if s['file'] == f'{kind}.schema.json')
            schema_bytes = (schema_root / record['file']).read_bytes()
            assert hashlib.sha256(schema_bytes).hexdigest() == record['sha256']
            schema = json.loads(schema_bytes)
            assert schema['$id'] == record['source']
            jsonschema.Draft202012Validator.check_schema(schema)
            jsonschema.Draft202012Validator(schema).validate(value)
    if platform['id'] == 'chatgpt':
        interface = manifest['extensions']['com.openai']['interface']
        assert len(interface['displayName']) <= 30
        assert len(interface['shortDescription']) <= 30
        assert len(interface['longDescription']) <= 4000
        assert interface['websiteURL'] == 'https://matchall.net'
        assert interface['developerName'] == 'Zhang Yifan'
        assert interface['supportURL'] == 'https://matchall.net/support'
        assert interface['privacyPolicyURL'] == 'https://matchall.net/privacy'
        assert interface['termsOfServiceURL'] == 'https://matchall.net/terms'
        prompts = interface['defaultPrompt']
        assert 0 < len(prompts) <= 3 and len(set(prompts)) == len(prompts)
        assert all(0 < len(s) <= 128 and '\n' not in s for s in prompts)
        assert 'apps' not in manifest['extensions']['com.openai']
        review = manifest['extensions']['com.openai']['review']
        assert set(review) == {'test_cases', 'demo_recording_url', 'commerce',
                               'commerce_description'}
        assert review['demo_recording_url'] == (
            'https://matchall.net/review/matchall-chatgpt-demo-20261023-narrated.mp4')
        assert review['commerce'] is True and review['commerce_description'].strip()
        assert manifest['extensions']['com.openai']['publication']['countries'] == []
        for value in (interface['websiteURL'], interface['supportURL'],
                      interface['privacyPolicyURL'], interface['termsOfServiceURL'],
                      review['demo_recording_url']):
            url = urlsplit(value)
            assert url.scheme == 'https' and url.hostname
            assert url.username is None and url.password is None
        assert not {'test_credentials', 'reviewer_instructions'} & set(review)
        icons = [(interface['logo'], 256), (interface['composerIcon'], 48)]
    elif platform['format'] == 'cursor':
        assert set(manifest) == {'name', 'version', 'description', 'repository',
                                'license', 'keywords', 'logo', 'skills', 'mcpServers', 'homepage'}
        assert manifest['homepage'] == 'https://matchall.net'
        assert manifest['skills'] == './skills/'
        assert manifest['mcpServers'] == './mcp.json'
        icons = [(manifest['logo'], 256)]
    else:
        icons = []
    assert mcp['mcpServers'] == {'matchall': expected_server}
    assert set(mcp) == ({'$schema', 'mcpServers'} if portable else {'mcpServers'})
    for name, minimum in icons:
        rel = PurePosixPath(name)
        assert not rel.is_absolute() and '..' not in rel.parts
        data = (root / name).read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) <= 5 * 1024 * 1024
        width, height = struct.unpack('>II', data[16:24])
        assert minimum <= width <= 4096 and width == height
    skill = (root / 'skills/match-service/SKILL.md').read_text()
    assert skill.startswith('---\nname: match-service\ndescription: ')
    assert all(s in skill for s in ('contact_details', 'email_bound',
                                   'expected_row_version', 'mutual approval'))
    assert all(s in skill for s in ('data.public_preview', 'intent_version',
                                   'expected_visibility_version'))
    cases = json.loads((root / 'docs/review-cases.json').read_text())
    assert cases['execution_status'] in {'NOT_RUN_IN_TARGET_HOST', 'PARTIAL_TARGET_HOST', 'PASSED_TARGET_HOST'}
    if cases['execution_status'] != 'NOT_RUN_IN_TARGET_HOST':
        report = PurePosixPath(cases['execution_report'])
        assert not report.is_absolute() and '..' not in report.parts
        assert (root / 'docs' / report).is_file()
    cases = cases['test_cases']
    assert len(cases['positive']) == 5 and len(cases['negative']) == 3
    for case in cases['positive']:
        assert all(case.get(k) for k in ('description', 'prompt', 'tools_triggered',
                                        'expected_behavior'))
    for case in cases['negative']:
        assert case['description'] and case['prompt']
    if platform['id'] == 'chatgpt':
        assert review['test_cases'] == cases
    status = json.loads((root / 'docs/readiness.json').read_text())
    assert status['submission_ready'] is False
    assert status['marketplace_submitted'] is False
    assert status['source_package_version'] == manifest['version']
    assert status['mcp_endpoint'] == expected_server['url']
    suspicious = re.compile(
        r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}'
        r'|sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
        r'|/Users/[A-Za-z0-9_-]+/|[A-Za-z0-9._%+-]+@(?:gmail|qq)\.com'
    )
    for path in root.rglob('*'):
        if any(part in IGNORED for part in path.relative_to(root).parts):
            continue
        assert not path.is_symlink(), f'Symlink: {path.relative_to(root)}'
        if not path.is_file():
            continue
        assert path.name != '.app.json'
        assert not path.name.startswith('.env')
        assert path.suffix not in ('.key', '.pem')
        if path.suffix != '.png':
            assert not suspicious.search(path.read_text()), f'Sensitive pattern: {path.relative_to(root)}'
    return manifest
