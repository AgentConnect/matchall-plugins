"""Validate staged plugin packages offline, preserving platform review checks."""
import hashlib
import json
import re
import struct
import zlib
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

import jsonschema

REPOSITORY = "https://github.com/AgentConnect/matchall-plugins"
IGNORED = {".git", ".venv", "__pycache__", "dist"}
WORKBUDDY_SKILL_TEXT = ('name', 'description', 'display_name', 'display_name_en',
                       'description_zh', 'description_en', 'version', 'author')
WORKBUDDY_SKILL_LISTS = ('examples_zh', 'examples_en')


def workbuddy_literal(value):
    """JSON quoting plus escapes for YAML's additional control/line characters."""
    text = json.dumps(value, ensure_ascii=False)
    return ''.join(f'\\u{ord(c):04x}' if 0x7f <= ord(c) <= 0x9f or c in '\u2028\u2029'
                   else c for c in text)


def validate_workbuddy_skill_fields(fields):
    assert set(fields) == set(WORKBUDDY_SKILL_TEXT + WORKBUDDY_SKILL_LISTS), 'Invalid Skill fields'
    for key in WORKBUDDY_SKILL_TEXT:
        assert isinstance(fields[key], str) and fields[key].strip(), f'Invalid Skill {key}'
        fields[key].encode('utf-8')
    assert fields['name'] == 'match-service'
    assert re.fullmatch(r'\d+\.\d+\.\d+', fields['version'])
    for key in WORKBUDDY_SKILL_LISTS:
        assert isinstance(fields[key], list) and 2 <= len(fields[key]) <= 5, f'Invalid Skill {key}'
        assert all(isinstance(s, str) and s.strip() for s in fields[key]), f'Invalid Skill {key}'
        for value in fields[key]:
            value.encode('utf-8')


def split_skill(data):
    lines = data.splitlines(keepends=True)
    assert lines and lines[0].rstrip(b'\r\n') == b'---', 'Missing Skill frontmatter'
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip(b'\r\n') == b'---'), None)
    assert end is not None, 'Unclosed Skill frontmatter'
    return b''.join(lines[1:end]).decode('utf-8'), b''.join(lines[end + 1:])


def split_shared_skill(data):
    """Read the repository's fixed two-field header, not arbitrary YAML."""
    header, body = split_skill(data)
    fields = {}
    for line in header.splitlines():
        key, separator, value = line.partition(': ')
        assert separator and key not in fields, 'Unsupported shared Skill header'
        fields[key] = value
    assert set(fields) == {'name', 'description'}, 'Unsupported shared Skill fields'
    assert fields['name'] == 'match-service' and fields['description'].strip()
    return fields, body


def render_workbuddy_skill(shared, metadata, version):
    fields, body = split_shared_skill(shared)
    expected = set(WORKBUDDY_SKILL_TEXT + WORKBUDDY_SKILL_LISTS) - {'name', 'description', 'version'}
    assert set(metadata) == expected, 'Invalid WorkBuddy Skill metadata'
    fields.update(metadata, version=version)
    validate_workbuddy_skill_fields(fields)
    header = '\n'.join(f'{key}: {workbuddy_literal(fields[key])}'
                       for key in WORKBUDDY_SKILL_TEXT + WORKBUDDY_SKILL_LISTS)
    return ('---\n' + header + '\n---\n').encode('utf-8') + body


def parse_workbuddy_skill(data):
    """Accept only our fixed JSON-literal YAML subset, rejecting duplicate fields."""
    header, body = split_skill(data)
    fields = {}
    for line in header.splitlines():
        key, separator, literal = line.partition(': ')
        assert separator and key not in fields, 'Invalid or duplicate Skill field'
        try:
            value = json.loads(literal)
        except (ValueError, TypeError) as error:
            raise AssertionError('Invalid Skill literal') from error
        assert literal == workbuddy_literal(value), 'Noncanonical Skill literal'
        fields[key] = value
    validate_workbuddy_skill_fields(fields)
    return fields, body


def validate_workbuddy_connector(connector, platform):
    text = ('name', 'name_zh', 'name_en', 'description', 'description_zh', 'description_en',
            'source', 'type', 'version', 'minWorkbuddyVersion')
    lists = ('examples_zh', 'examples_en')
    assert set(connector) == set(text + lists), 'Unexpected WorkBuddy connector fields'
    for key in text:
        assert isinstance(connector[key], str) and connector[key].strip(), f'Invalid connector {key}'
    for key in lists:
        assert isinstance(connector[key], list) and 2 <= len(connector[key]) <= 5
        assert all(isinstance(s, str) and s.strip() for s in connector[key])
    assert connector['source'] == platform['name']
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', connector['source'])
    assert re.fullmatch(r'\d+\.\d+\.\d+', connector['version'])
    assert connector['type'] == 'mcp'
    assert connector['minWorkbuddyVersion'] == '4.24.0'


def validate_workbuddy_files(root, manifest):
    assert {p.name for p in root.iterdir()} == {
        'LICENSE', 'README.md', 'connector-meta.json', 'mcp.json', 'icon.png', 'skills', 'docs'}
    assert {p.relative_to(root / 'skills').as_posix() for p in (root / 'skills').rglob('*')
            if p.is_file()} == {'match-service/SKILL.md'}
    fields, body = parse_workbuddy_skill((root / 'skills/match-service/SKILL.md').read_bytes())
    integrity = json.loads((root / 'docs/skill-integrity.json').read_text(encoding='utf-8'))
    assert set(integrity) == {'name', 'description', 'body_sha256'}
    assert fields['name'] == integrity['name'] and fields['description'] == integrity['description']
    assert fields['version'] == manifest['version']
    assert hashlib.sha256(body).hexdigest() == integrity['body_sha256'], 'Changed Skill body'
    status = json.loads((root / 'docs/readiness.json').read_text(encoding='utf-8'))
    cases = json.loads((root / 'docs/review-cases.json').read_text(encoding='utf-8'))
    host = json.loads((root / 'docs/host-cases.json').read_text(encoding='utf-8'))
    assert status['marketplace_approved'] is False
    assert status['target_host_e2e'] == cases['execution_status'] == host['execution_status']
    assert host['connector_source'] == manifest['name']
    if status['target_host_e2e'] != 'NOT_RUN_IN_TARGET_HOST':
        assert status['execution_report'] == cases['execution_report'] == host['execution_report'], 'Inconsistent acceptance reports'
        results = cases['execution_results']
        assert set(results) == {'P1', 'P2', 'P3', 'P4', 'P5', 'N1', 'N2', 'N3'}, 'Missing business results'
        host_ids = [case['id'] for case in host['cases']]
        assert len(host_ids) == 6 and set(host_ids) == {'WB1', 'WB2', 'WB3', 'WB4', 'WB5', 'WB6'}, 'Invalid host results'
        allowed = {'NOT_RUN', 'PARTIAL', 'PASSED', 'FAILED', 'BLOCKED', 'PASSED_CONVERSATIONAL_ONLY'}
        for result in results.values():
            assert result['result'] in allowed and result['reason'].strip(), 'Invalid business result'
        for case in host['cases']:
            assert case['result'] in allowed and case['observation'].strip(), 'Invalid host result'
        if status['target_host_e2e'] == 'PASSED_TARGET_HOST':
            assert all(r['result'] == 'PASSED' for r in results.values()), 'Incomplete business acceptance'
            assert all(c['result'] == 'PASSED' for c in host['cases']), 'Incomplete host acceptance'
            assert not status['pending'], 'Unresolved acceptance items'
    data = (root / 'icon.png').read_bytes()
    assert data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) <= 5 * 1024 * 1024
    offset, chunks = 8, []
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset:offset + 4], 'big')
        end = offset + 12 + length
        assert end <= len(data), 'Truncated PNG chunk'
        chunk = data[offset + 4:offset + 8]
        assert zlib.crc32(data[offset + 4:end - 4]) == int.from_bytes(data[end - 4:end], 'big'), 'Invalid PNG CRC'
        chunks.append(chunk)
        if len(chunks) == 1:
            assert chunk == b'IHDR' and length == 13
        if chunk == b'IEND':
            assert length == 0 and end == len(data)
        offset = end
    assert offset == len(data) and chunks[-1:] == [b'IEND'] and b'IDAT' in chunks


def require_no_links(root):
    assert not root.is_symlink(), "Package root must not be a symlink"
    for path in root.rglob("*"):
        assert not path.is_symlink(), f"Symlink: {path.relative_to(root)}"


def validate_package(root, platform):
    root = Path(root)
    portable = platform['format'] == 'agent-plugins'
    workbuddy = platform['format'] == 'workbuddy'
    assert platform['format'] in {'agent-plugins', 'cursor', 'workbuddy'}, 'Unsupported package format'
    require_no_links(root)
    manifest_path = root / ('connector-meta.json' if workbuddy else
                            'plugin.json' if portable else '.cursor-plugin/plugin.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if workbuddy:
        validate_workbuddy_connector(manifest, platform)
        manifest = {'name': manifest['source'], 'version': manifest['version']}
        validate_workbuddy_files(root, manifest)
    mcp = json.loads((root / 'mcp.json').read_text(encoding='utf-8'))
    expected_name = platform['name']
    assert manifest['name'] == expected_name
    assert re.fullmatch(r'\d+\.\d+\.\d+', manifest['version'])
    if not workbuddy:
        assert manifest['license'] == 'MIT'
        assert manifest['repository'] == REPOSITORY
    assert not any(k in manifest for k in ('apps', 'hooks'))
    assert (root / 'LICENSE').read_text(encoding='utf-8').startswith('MIT License\n')
    expected_server = {'url': 'https://matchall.net/amatch/v2'}
    if portable:
        expected_server['type'] = 'streamable-http'
        for kind, value in (('plugin', manifest), ('mcp', mcp)):
            schema_root = root / 'schemas' / 'agent-plugins-1.0.0'
            provenance = json.loads((schema_root / 'provenance.json').read_text(encoding='utf-8'))
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
        icons = [('icon.png', 64)] if workbuddy else []
    if workbuddy:
        expected_server['type'] = 'streamableHttp'
    assert mcp['mcpServers'] == {'matchall': expected_server}
    assert set(mcp) == ({'$schema', 'mcpServers'} if portable else {'mcpServers'})
    for name, minimum in icons:
        rel = PurePosixPath(name)
        assert not rel.is_absolute() and '..' not in rel.parts
        data = (root / name).read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n') and 24 <= len(data) <= 5 * 1024 * 1024
        width, height = struct.unpack('>II', data[16:24])
        assert minimum <= width <= 4096 and width == height
    skill = (root / 'skills/match-service/SKILL.md').read_text(encoding='utf-8')
    if not workbuddy:
        assert skill.startswith('---\nname: match-service\ndescription: ')
    assert all(s in skill for s in ('contact_details', 'email_bound',
                                   'expected_row_version', 'mutual approval'))
    assert all(s in skill for s in ('data.public_preview', 'intent_version',
                                   'expected_visibility_version'))
    cases = json.loads((root / 'docs/review-cases.json').read_text(encoding='utf-8'))
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
    status = json.loads((root / 'docs/readiness.json').read_text(encoding='utf-8'))
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
            assert not suspicious.search(path.read_text(encoding='utf-8')), f'Sensitive pattern: {path.relative_to(root)}'
    return manifest
