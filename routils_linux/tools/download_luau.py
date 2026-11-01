import argparse
import json
import os
import tempfile
import urllib.request
import zipfile
from pathlib import Path

API_URL = 'https://api.github.com/repos/luau-lang/luau/releases/latest'
USER_AGENT = 'RoUtils-Luau-Builder'
MAX_DOWNLOAD_SIZE = 134217728


def fetch(url, accept):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': accept})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(MAX_DOWNLOAD_SIZE + 1)
        if len(data) > MAX_DOWNLOAD_SIZE:
            raise RuntimeError('The Luau release archive is larger than the allowed download size.')
        return data


def find_asset(release):
    assets = release.get('assets', [])
    matches = [asset for asset in assets if str(asset.get('name', '')).lower().endswith('.zip') and 'luau' in str(asset.get('name', '')).lower() and 'ubuntu' in str(asset.get('name', '')).lower()]
    if not matches:
        matches = [asset for asset in assets if str(asset.get('name', '')).lower().endswith('.zip') and 'luau' in str(asset.get('name', '')).lower() and 'linux' in str(asset.get('name', '')).lower()]
    if not matches:
        names = ', '.join(str(asset.get('name', '')) for asset in assets)
        raise RuntimeError(f'No official Ubuntu/Linux Luau CLI archive was found. Available assets: {names}')
    matches.sort(key=lambda asset: ('x86_64' not in str(asset.get('name', '')).lower(), 'x64' not in str(asset.get('name', '')).lower(), str(asset.get('name', '')).lower()))
    return matches[0]


def install(output):
    release = json.loads(fetch(API_URL, 'application/vnd.github+json'))
    asset = find_asset(release)
    url = str(asset.get('browser_download_url', ''))
    if not url.startswith('https://github.com/luau-lang/luau/releases/download/'):
        raise RuntimeError('The release asset URL did not match the official Luau repository.')
    archive_data = fetch(url, 'application/octet-stream')
    output = Path(output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='routils-luau-') as temporary:
        archive_path = Path(temporary) / 'luau.zip'
        archive_path.write_bytes(archive_data)
        if not zipfile.is_zipfile(archive_path):
            raise RuntimeError('The downloaded Luau asset is not a valid ZIP archive.')
        with zipfile.ZipFile(archive_path) as archive:
            matches = [entry for entry in archive.infolist() if not entry.is_dir() and entry.filename.rstrip('/').split('/')[-1] == 'luau']
            if not matches:
                raise RuntimeError('The official Luau archive does not contain the luau CLI executable.')
            if len(matches) > 1:
                matches.sort(key=lambda entry: (entry.filename.count('/'), entry.filename))
            executable_data = archive.read(matches[0])
            if not executable_data.startswith(b'\x7fELF'):
                raise RuntimeError('The downloaded luau executable is not a Linux ELF binary.')
        temporary_output = output.with_name(output.name + '.tmp')
        temporary_output.write_bytes(executable_data)
        temporary_output.chmod(0o755)
        os.replace(temporary_output, output)
    return output, str(release.get('tag_name', 'latest'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(Path(__file__).resolve().parents[1] / 'bin' / 'luau'))
    args = parser.parse_args()
    output, version = install(args.output)
    print(f'Luau {version} installed at {output}')


if __name__ == '__main__':
    main()
