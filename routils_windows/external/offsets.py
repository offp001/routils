import json
import ntpath
import os
import re
import sys
import threading
import time
import urllib.request
from fflag.processes import _windows_process_path
from external.properties import ExternalPropertiesMixin
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
_FFLAG_COLOR_MUTED = globals().get('_FFLAG_COLOR_MUTED', '#9aa0a6')
_FFLAG_COLOR_SUCCESS = globals().get('_FFLAG_COLOR_SUCCESS', '#65d98b')
_FFLAG_COLOR_ERROR = globals().get('_FFLAG_COLOR_ERROR', '#ff6b6b')
_FFLAG_COLOR_WARNING = globals().get('_FFLAG_COLOR_WARNING', '#f2c94c')

class ExternalOffsetsMixin(ExternalPropertiesMixin):
    _EXTERNAL_VERSION_API = 'https://www.rbxoffsets.com/api/v1/windows/version'
    _EXTERNAL_OFFSETS_URL = 'https://offsets.imtheo.lol/{version}/offsets.hpp'
    _EXTERNAL_MAX_HEADER_SIZE = 2 * 1024 * 1024
    _EXTERNAL_VERSION_PATTERN = re.compile('version-[A-Za-z0-9_-]+')

    @staticmethod
    def _external_parse_header(source):
        if not isinstance(source, str) or len(source) > ExternalOffsetsMixin._EXTERNAL_MAX_HEADER_SIZE:
            raise ValueError('Invalid offsets header size')
        if 'namespace Offsets' not in source or 'namespace World' not in source:
            raise ValueError('The downloaded file is not a supported offsets.hpp header')
        namespace_stack = []
        offsets = {}
        version_match = re.search('inline\\s+std::string\\s+ClientVersion\\s*=\\s*"([^"]+)"', source)
        for line in source.splitlines():
            namespace_match = re.match('^\\s*namespace\\s+([A-Za-z_]\\w*)\\s*\\{', line)
            if namespace_match:
                namespace_stack.append(namespace_match.group(1))
                continue
            value_match = re.match('^\\s*inline\\s+(?:(?:constexpr|const)\\s+)?([A-Za-z_]\\w*(?:::[A-Za-z_]\\w*)*)\\s+([A-Za-z_]\\w*)\\s*=\\s*(0x[0-9A-Fa-f]+|\\d+)\\s*;', line)
            if value_match:
                value_type, name, value = value_match.groups()
                path = namespace_stack[1:] if namespace_stack and namespace_stack[0] == 'Offsets' else namespace_stack
                qualified = '::'.join(path + [name])
                offsets[qualified] = {'name': qualified, 'value': value, 'type': value_type}
            if re.match('^\\s*}\\s*;?\\s*$', line) and namespace_stack:
                namespace_stack.pop()
        required = ('FakeDataModel::Pointer', 'FakeDataModel::RealDataModel', 'DataModel::Workspace', 'Workspace::World', 'World::Gravity')
        missing = [name for name in required if name not in offsets]
        if missing:
            raise ValueError('Required offsets are missing: ' + ', '.join(missing))
        return {'version': version_match.group(1) if version_match else '', 'offsets': offsets}

    def _external_offsets_cache_path(self):
        return os.path.join(DATA_DIR, 'external_offsets_latest.json')

    @staticmethod
    def _external_read_url(url, limit):
        request = urllib.request.Request(url, headers={'User-Agent': f'RoUtils/{APP_VERSION}', 'Accept': 'application/json, text/plain, */*'})
        with urllib.request.urlopen(request, timeout=15) as response:
            data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError('The offsets response is too large')
        return data

    def _external_fetch_latest_offsets(self):
        api_data = json.loads(self._external_read_url(self._EXTERNAL_VERSION_API, 128 * 1024).decode('utf-8-sig'))

        def find_value(node, names):
            if isinstance(node, dict):
                for key in names:
                    value = node.get(key)
                    if isinstance(value, str) and value.strip():
                        return value.strip()
                for value in node.values():
                    found = find_value(value, names)
                    if found:
                        return found
            elif isinstance(node, list):
                for value in node:
                    found = find_value(value, names)
                    if found:
                        return found
            return ''
        version = find_value(api_data, ('version', 'clientVersion', 'latestVersion'))
        if not re.fullmatch('version-[A-Za-z0-9_-]+', version):
            raise ValueError('The latest Windows build version could not be identified')
        display_version = find_value(api_data, ('displayVersion', 'robloxVersion', 'fileVersion')) or version
        url = self._EXTERNAL_OFFSETS_URL.format(version=version)
        header = self._external_read_url(url, self._EXTERNAL_MAX_HEADER_SIZE).decode('utf-8-sig', errors='strict')
        parsed = self._external_parse_header(header)
        if parsed['version'] and parsed['version'] != version:
            raise ValueError('The downloaded header version does not match the latest build')
        parsed.update({'version': version, 'display_version': display_version, 'url': url, 'loaded_at': time.time()})
        return parsed

    def _external_client_version(self, pid):
        client_path = _windows_process_path(pid)
        if not client_path:
            raise RuntimeError('Could not locate the selected Roblox client executable.')
        folder = ntpath.basename(ntpath.dirname(ntpath.normpath(client_path)))
        if not self._EXTERNAL_VERSION_PATTERN.fullmatch(folder):
            raise RuntimeError('Could not read the selected Roblox build version from its installation folder.')
        return folder

    def _external_version_cache_path(self, version):
        if not self._EXTERNAL_VERSION_PATTERN.fullmatch(str(version)):
            raise ValueError('Invalid Roblox build version.')
        return os.path.join(DATA_DIR, f'external_offsets_{version}.json')

    def _external_fetch_offsets_for_version(self, version):
        version = str(version).strip()
        if not self._EXTERNAL_VERSION_PATTERN.fullmatch(version):
            raise ValueError('Invalid Roblox build version.')
        url = self._EXTERNAL_OFFSETS_URL.format(version=version)
        header = self._external_read_url(url, self._EXTERNAL_MAX_HEADER_SIZE).decode('utf-8-sig', errors='strict')
        parsed = self._external_parse_header(header)
        if parsed.get('version') and parsed['version'] != version:
            raise ValueError('Theo returned offsets for a different Roblox build.')
        parsed.update({'version': version, 'display_version': version, 'url': url, 'loaded_at': time.time()})
        return parsed

    def _external_offsets_for_client(self, pid, force=False):
        version = self._external_client_version(pid)
        memory_cache = getattr(self, '_external_offsets_version_cache', None)
        if not isinstance(memory_cache, dict):
            memory_cache = {}
            self._external_offsets_version_cache = memory_cache
        if not force and version in memory_cache:
            return memory_cache[version]
        path = self._external_version_cache_path(version)
        if not force:
            try:
                with open(path, 'r', encoding='utf-8') as source:
                    cached = json.load(source)
                if isinstance(cached, dict) and cached.get('version') == version and isinstance(cached.get('offsets'), dict):
                    cached['cached'] = True
                    memory_cache[version] = cached
                    return cached
            except Exception:
                pass
        result = self._external_fetch_offsets_for_version(version)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        temporary = path + '.tmp'
        with open(temporary, 'w', encoding='utf-8') as output:
            json.dump(result, output, ensure_ascii=False, separators=(',', ':'))
        os.replace(temporary, path)
        result['cached'] = False
        memory_cache[version] = result
        return result

    def _external_load_latest_offsets(self, force=False):
        if getattr(self, '_external_offsets_loading', False):
            return
        self._external_offsets_loading = True
        if hasattr(self, 'external_property_status'):
            self.external_property_status.configure(text='loading latest property definitions…', foreground=_FFLAG_COLOR_MUTED)

        def worker():
            try:
                pid = int(getattr(self, 'fflag_pid', 0) or 0)
                engine = getattr(self, 'fflag_engine', None)
                result = self._external_offsets_for_client(pid, force=force) if pid and engine and engine.handle else self._external_fetch_latest_offsets()
                version = str(result.get('version', '')) if isinstance(result, dict) else ''
                path = self._external_version_cache_path(version) if self._EXTERNAL_VERSION_PATTERN.fullmatch(version) else self._external_offsets_cache_path()
                os.makedirs(os.path.dirname(path), exist_ok=True)
                temporary = path + '.tmp'
                with open(temporary, 'w', encoding='utf-8') as output:
                    json.dump(result, output, ensure_ascii=False, separators=(',', ':'))
                os.replace(temporary, path)
                result['cached'] = False
            except Exception as error:
                result = {'error': str(error)}
                try:
                    with open(self._external_offsets_cache_path(), 'r', encoding='utf-8') as source:
                        cached = json.load(source)
                    if isinstance(cached, dict) and isinstance(cached.get('offsets'), dict):
                        result = cached
                        result['cached'] = True
                        result['refresh_error'] = str(error)
                except Exception:
                    pass
            try:
                self.after(0, self._external_offsets_loaded, result)
            except Exception:
                self._external_offsets_loading = False
        threading.Thread(target=worker, name='RoUtilsExternalDefinitions', daemon=True).start()

    def _external_offsets_loaded(self, result):
        self._external_offsets_loading = False
        if not isinstance(result, dict) or not isinstance(result.get('offsets'), dict):
            error = str(result.get('error', 'Unknown error'))
            self.external_property_status.configure(text='property definitions unavailable', foreground=_FFLAG_COLOR_WARNING)
            if hasattr(self, 'external_property_status_detail'):
                self.external_property_status_detail.configure(text=error, foreground=_FFLAG_COLOR_WARNING)
            return
        self._external_offsets_data = result
        state = 'Cached' if result.get('cached') else 'Latest'
        if result.get('cached'):
            state += ' · offline cache'
        display_version = result.get('display_version') or result.get('version', 'unknown')
        if result.get('refresh_error'):
            state += ' · refresh failed'
        self.external_property_status.configure(text=f'{state} · {display_version}', foreground=_FFLAG_COLOR_SUCCESS if not result.get('refresh_error') else _FFLAG_COLOR_WARNING)
        self._external_properties_offsets_ready()

    def _build_external_tab(self):
        tab = ttk.Frame(self.nb, padding=10)
        self.nb.add(tab, text='external')
        self._external_build_offsets_panel(tab)

    def _external_build_offsets_panel(self, tab):
        self._external_offsets_data = None
        self._external_offsets_loading = False
        self._external_build_property_panel(tab)
        self._external_load_latest_offsets()
