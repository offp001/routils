import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
import urllib.request
import zipfile


def request(url, accept=None):
    headers = {'User-Agent': 'RoUtils-Luau-Builder'}
    if accept:
        headers['Accept'] = accept
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read()


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: download_cli.py <output-path>')
    output = pathlib.Path(sys.argv[1]).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = json.loads(request('https://api.github.com/repos/luau-lang/luau/releases/latest', 'application/vnd.github+json'))
    assets = metadata.get('assets') or []
    asset = next((item for item in assets if item.get('name', '').lower() == 'luau-ubuntu.zip'), None)
    if asset is None:
        available = ', '.join(item.get('name', '') for item in assets)
        raise RuntimeError('official Luau Linux release asset was not found: ' + available)
    archive_data = request(asset['browser_download_url'], 'application/octet-stream')
    expected = str(asset.get('digest') or '').lower().removeprefix('sha256:')
    if not expected and str(metadata.get('tag_name', '')).lstrip('v') == '0.745':
        expected = '186e5ddaa2b048ebc7390c11ed1b00c04e7d3beaffed429250329e3575d2ece2'
    if expected:
        actual = hashlib.sha256(archive_data).hexdigest()
        if actual != expected:
            raise RuntimeError('Luau release archive SHA-256 verification failed')
    with tempfile.TemporaryDirectory(prefix='routils_luau_download_') as temporary:
        archive_path = pathlib.Path(temporary) / 'luau.zip'
        archive_path.write_bytes(archive_data)
        with zipfile.ZipFile(archive_path) as archive:
            matches = [item for item in archive.infolist() if pathlib.PurePosixPath(item.filename).name == 'luau' and not item.is_dir()]
            if not matches:
                raise RuntimeError('Luau Linux archive did not contain the luau executable')
            with archive.open(matches[0]) as source, output.open('wb') as target:
                shutil.copyfileobj(source, target)
    output.chmod(0o755)
    import subprocess
    result = subprocess.run([str(output)], input='print("routils luau ready")\n', text=True, capture_output=True, timeout=10, check=False)
    if result.returncode != 0 or 'routils luau ready' not in result.stdout:
        raise RuntimeError('downloaded Luau CLI did not pass its execution check: ' + (result.stderr or result.stdout))
    print('Luau CLI ' + str(metadata.get('tag_name', 'latest')) + ' installed at ' + str(output))


if __name__ == '__main__':
    main()
