"""Build a local preparation ZIP; never upload or release it."""
import hashlib
import zipfile
from pathlib import PurePosixPath
from validate import ROOT, package_files, validate

manifest = validate()
files = package_files()
output = ROOT / 'dist' / f'{manifest["name"]}-{manifest["version"]}-preparation.zip'
output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        assert not path.is_symlink()
        archive.write(path, PurePosixPath(manifest['name']) / path.relative_to(ROOT))
with zipfile.ZipFile(output) as archive:
    expected = {str(PurePosixPath(manifest['name']) / p.relative_to(ROOT)): p for p in files}
    assert set(archive.namelist()) == set(expected)
    assert len(archive.namelist()) == len(expected)
    assert archive.testzip() is None
    for name, path in expected.items():
        assert not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
        assert archive.read(name) == path.read_bytes()
print(f'PASS: {output.relative_to(ROOT)} ({len(files)} files) sha256={hashlib.sha256(output.read_bytes()).hexdigest()}')
