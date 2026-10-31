import ctypes
import json
import math
import os
import re
import struct
import sys
import threading
import time
import urllib.request
from fflag.processes import _windows_process_path
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
_FFLAG_COLOR_MUTED = globals().get('_FFLAG_COLOR_MUTED', '#9aa0a6')
_FFLAG_COLOR_SUCCESS = globals().get('_FFLAG_COLOR_SUCCESS', '#65d98b')
_FFLAG_COLOR_ERROR = globals().get('_FFLAG_COLOR_ERROR', '#ff6b6b')
_FFLAG_COLOR_WARNING = globals().get('_FFLAG_COLOR_WARNING', '#f2c94c')

class ExternalOffsetsMixin:
    _EXTERNAL_VERSION_API = 'https://www.rbxoffsets.com/api/v1/windows/version'
    _EXTERNAL_OFFSETS_URL = 'https://offsets.imtheo.lol/{version}/offsets.hpp'
    _EXTERNAL_MAX_HEADER_SIZE = 2 * 1024 * 1024

    @staticmethod
    def _external_parse_header(source):
        if not isinstance(source, str) or len(source) > ExternalOffsetsMixin._EXTERNAL_MAX_HEADER_SIZE:
            raise ValueError('Invalid offsets header size')
        if 'namespace Offsets' not in source or 'namespace World' not in source:
            raise ValueError('The downloaded file is not a supported offsets.hpp header')
        namespace_stack = []
        offsets = {}
        version_match = re.search(r'inline\s+std::string\s+ClientVersion\s*=\s*"([^"]+)"', source)
        for line in source.splitlines():
            namespace_match = re.match(r'^\s*namespace\s+([A-Za-z_]\w*)\s*\{', line)
            if namespace_match:
                namespace_stack.append(namespace_match.group(1))
                continue
            value_match = re.match(r'^\s*inline\s+(?:(?:constexpr|const)\s+)?([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)\s+([A-Za-z_]\w*)\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*;', line)
            if value_match:
                value_type, name, value = value_match.groups()
                path = namespace_stack[1:] if namespace_stack and namespace_stack[0] == 'Offsets' else namespace_stack
                qualified = '::'.join(path + [name])
                offsets[qualified] = {'name': qualified, 'value': value, 'type': value_type}
            if re.match(r'^\s*}\s*;?\s*$', line) and namespace_stack:
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
        if not re.fullmatch(r'version-[A-Za-z0-9_-]+', version):
            raise ValueError('The latest Windows build version could not be identified')
        display_version = find_value(api_data, ('displayVersion', 'robloxVersion', 'fileVersion')) or version
        url = self._EXTERNAL_OFFSETS_URL.format(version=version)
        raw = self._external_read_url(url, self._EXTERNAL_MAX_HEADER_SIZE)
        header = raw.decode('utf-8-sig', errors='strict')
        parsed = self._external_parse_header(header)
        if parsed['version'] and parsed['version'] != version:
            raise ValueError('The downloaded header version does not match the latest build')
        parsed.update({'version': version, 'display_version': display_version, 'url': url, 'loaded_at': time.time()})
        return parsed

    def _external_load_latest_offsets(self, force=False):
        if getattr(self, '_external_offsets_loading', False):
            return
        self._external_offsets_loading = True
        if hasattr(self, 'external_offsets_status'):
            self.external_offsets_status.configure(text='Checking latest Windows offsets…', foreground=_FFLAG_COLOR_MUTED)
        def worker():
            try:
                result = self._external_fetch_latest_offsets()
                path = self._external_offsets_cache_path()
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
        threading.Thread(target=worker, name='RoUtilsExternalOffsets', daemon=True).start()

    def _external_offsets_loaded(self, result):
        self._external_offsets_loading = False
        if not isinstance(result, dict) or not isinstance(result.get('offsets'), dict):
            self.external_offsets_status.configure(text='Could not load latest offsets', foreground=_FFLAG_COLOR_ERROR)
            messagebox.showerror('External Offsets', str(result.get('error', 'Unknown error')), parent=self)
            return
        self._external_offsets_data = result
        rows = sorted(result['offsets'].values(), key=lambda item: (item.get('name', '').casefold()))
        self._external_offsets_rows = rows
        self._external_render_offsets_rows()
        gravity = result['offsets'].get('World::Gravity', {})
        self.external_gravity_offset_var.set(str(gravity.get('value', '')))
        self.external_gravity_offset_type.configure(text=str(gravity.get('type', 'unknown')))
        state = 'Cached' if result.get('cached') else 'Latest'
        if result.get('cached'):
            state += ' · offline cache'
        display_version = result.get('display_version') or result.get('version', 'unknown')
        if result.get('refresh_error'):
            state += ' · refresh failed'
        self.external_offsets_status.configure(text=f'{state} · {display_version}', foreground=_FFLAG_COLOR_SUCCESS if not result.get('refresh_error') else _FFLAG_COLOR_WARNING)

    def _external_render_offsets_rows(self):
        tree = getattr(self, 'external_offsets_tree', None)
        if tree is None:
            return
        query = self.external_offsets_search_var.get().strip().casefold()
        tree.delete(*tree.get_children())
        for item in getattr(self, '_external_offsets_rows', []):
            name = str(item.get('name', ''))
            value = str(item.get('value', ''))
            value_type = str(item.get('type', ''))
            if query and query not in name.casefold() and query not in value.casefold() and query not in value_type.casefold():
                continue
            tags = ('gravity',) if name == 'World::Gravity' else ()
            tree.insert('', 'end', values=(name, value, value_type), tags=tags)

    def _external_select_offset(self, _event=None):
        selection = self.external_offsets_tree.selection()
        if not selection:
            return
        values = self.external_offsets_tree.item(selection[0], 'values')
        if len(values) < 3:
            return
        name, offset, value_type = values[:3]
        self.external_selected_name.configure(text=name)
        self.external_selected_offset.configure(text=offset)
        self.external_selected_type.configure(text=value_type)
        self.external_selected_value_type.configure(text='float' if name == 'World::Gravity' else '—')
        self.external_apply_button.configure(state='normal' if name == 'World::Gravity' else 'disabled')

    @staticmethod
    def _external_file_version(path):
        if not path or not os.path.isfile(path):
            return ''
        version_api = ctypes.WinDLL('version', use_last_error=True)
        version_api.GetFileVersionInfoSizeW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint)]
        version_api.GetFileVersionInfoSizeW.restype = ctypes.c_uint
        version_api.GetFileVersionInfoW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]
        version_api.GetFileVersionInfoW.restype = ctypes.c_int
        version_api.VerQueryValueW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_uint)]
        version_api.VerQueryValueW.restype = ctypes.c_int
        size = ctypes.c_uint(version_api.GetFileVersionInfoSizeW(path, None))
        if not size.value:
            return ''
        buffer = ctypes.create_string_buffer(size.value)
        if not version_api.GetFileVersionInfoW(path, 0, size.value, buffer):
            return ''
        pointer = ctypes.c_void_p()
        length = ctypes.c_uint()
        if not version_api.VerQueryValueW(buffer, '\\', ctypes.byref(pointer), ctypes.byref(length)) or not pointer.value:
            return ''
        class FixedFileInfo(ctypes.Structure):
            _fields_ = [('dwSignature', ctypes.c_uint32), ('dwStrucVersion', ctypes.c_uint32), ('dwFileVersionMS', ctypes.c_uint32), ('dwFileVersionLS', ctypes.c_uint32), ('dwProductVersionMS', ctypes.c_uint32), ('dwProductVersionLS', ctypes.c_uint32), ('dwFileFlagsMask', ctypes.c_uint32), ('dwFileFlags', ctypes.c_uint32), ('dwFileOS', ctypes.c_uint32), ('dwFileType', ctypes.c_uint32), ('dwFileSubtype', ctypes.c_uint32), ('dwFileDateMS', ctypes.c_uint32), ('dwFileDateLS', ctypes.c_uint32)]
        info = ctypes.cast(pointer, ctypes.POINTER(FixedFileInfo)).contents
        major = info.dwFileVersionMS >> 16
        minor = info.dwFileVersionMS & 0xFFFF
        build = info.dwFileVersionLS >> 16
        revision = info.dwFileVersionLS & 0xFFFF
        return f'{major}.{minor}.{build}.{revision}'

    def _external_resolve_gravity_address(self, offsets):
        engine = getattr(self, 'fflag_engine', None)
        if engine is None or not engine.handle or not engine.module_base:
            raise RuntimeError('No Roblox client is attached. Open Clients and select a running client first.')
        def number(key):
            value = offsets.get(key, {}).get('value')
            if value is None:
                raise ValueError(f'Missing offset: {key}')
            return int(str(value), 0)
        fake_model_slot = engine.module_base + number('FakeDataModel::Pointer')
        fake_model = engine._read_u64(fake_model_slot)
        if not fake_model:
            raise RuntimeError('The Roblox data model pointer is not ready yet.')
        real_model = engine._read_u64(fake_model + number('FakeDataModel::RealDataModel'))
        if not real_model:
            raise RuntimeError('The Roblox data model could not be resolved.')
        workspace = engine._read_u64(real_model + number('DataModel::Workspace'))
        if not workspace:
            raise RuntimeError('The Roblox Workspace pointer could not be resolved.')
        world = engine._read_u64(workspace + number('Workspace::World'))
        if not world:
            raise RuntimeError('The Roblox World pointer could not be resolved.')
        return world + number('World::Gravity')

    def _external_gravity_apply(self, silent=False):
        data = getattr(self, '_external_offsets_data', None)
        if not isinstance(data, dict) or not isinstance(data.get('offsets'), dict):
            if not silent:
                messagebox.showwarning('External Offsets', 'Load the latest offsets first.', parent=self)
            return
        try:
            gravity = float(self.external_gravity_value_var.get().strip())
            offset = int(self.external_gravity_offset_var.get().strip(), 0)
            if not math.isfinite(gravity) or not -10000.0 <= gravity <= 10000.0:
                raise ValueError('Gravity must be a finite number between -10000 and 10000.')
            if not 0 <= offset <= 0x100000:
                raise ValueError('The Gravity offset is outside the accepted range.')
            if not silent:
                self.settings['external_gravity_value'] = str(gravity)
                self.settings['external_gravity_offset'] = hex(offset)
                self._save_settings()
        except Exception as error:
            if not silent:
                messagebox.showerror('External Offsets', str(error), parent=self)
            return
        if getattr(self, '_external_gravity_worker_active', False):
            return
        self._external_gravity_worker_active = True
        offsets = dict(data['offsets'])
        offsets['World::Gravity'] = dict(offsets['World::Gravity'], value=hex(offset))
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        def worker():
            result = {'ok': False, 'message': 'Gravity could not be applied.'}
            try:
                engine = self.fflag_engine
                if not pid or engine.pid != pid or not engine.handle:
                    raise RuntimeError('No attached Roblox client. Open Clients and select a running client first.')
                client_path = _windows_process_path(pid)
                running_version = self._external_file_version(client_path)
                expected_version = str(data.get('display_version') or '').strip()
                if not running_version or not expected_version:
                    raise RuntimeError('Could not verify that the latest offsets match the selected Roblox client.')
                if running_version != expected_version:
                    raise RuntimeError(f'Roblox version mismatch. Running client: {running_version} · offsets: {expected_version}. Update or restart Roblox before applying.')
                address = self._external_resolve_gravity_address(offsets)
                original = engine._read(address, 4)
                if original is None:
                    raise RuntimeError('Could not read the current Gravity value from the Roblox client.')
                key = (pid, address)
                if key not in self._external_gravity_originals:
                    self._external_gravity_originals[key] = original
                payload = struct.pack('<f', gravity)
                written = ctypes.c_size_t()
                ok = ctypes.windll.kernel32.WriteProcessMemory(engine.handle, ctypes.c_void_p(address), payload, len(payload), ctypes.byref(written))
                if not ok or written.value != len(payload):
                    raise RuntimeError('Windows could not write the Gravity value.')
                result = {'ok': True, 'message': f'Gravity {gravity:g} applied to PID {pid}.', 'pid': pid, 'address': address}
            except Exception as error:
                result = {'ok': False, 'message': str(error)}
            self.after(0, self._external_gravity_apply_finished, result, bool(silent))
        threading.Thread(target=worker, name='RoUtilsGravityApply', daemon=True).start()

    def _external_gravity_apply_finished(self, result, silent=False):
        self._external_gravity_worker_active = False
        color = _FFLAG_COLOR_SUCCESS if result.get('ok') else _FFLAG_COLOR_ERROR
        self.external_gravity_status.configure(text=str(result.get('message', '')), foreground=color)
        if not silent:
            self._console_log(str(result.get('message', 'Gravity apply finished')))
        if not result.get('ok') and not silent:
            messagebox.showerror('External Offsets', str(result.get('message', 'Gravity could not be applied.')), parent=self)

    def _external_gravity_toggle_auto_apply(self):
        enabled = bool(self.external_gravity_auto_var.get())
        if enabled and not getattr(self, '_external_gravity_auto_confirmed', False):
            approved = messagebox.askyesno('External Gravity Auto Apply', 'Auto Apply will repeatedly write the selected Gravity value to the attached Roblox client. The offsets must match the running client build. Continue?', parent=self)
            if not approved:
                self.external_gravity_auto_var.set(False)
                return
            self._external_gravity_auto_confirmed = True
        self.settings['external_gravity_auto_apply'] = enabled
        self._save_settings()
        self.external_gravity_status.configure(text='Auto Apply enabled' if enabled else 'Auto Apply disabled', foreground=_FFLAG_COLOR_SUCCESS if enabled else _FFLAG_COLOR_MUTED)
        if enabled:
            self._external_gravity_apply(silent=True)

    def _external_gravity_auto_tick(self):
        try:
            if self.external_gravity_auto_var.get() and self.fflag_pid and self.fflag_engine.handle:
                self._external_gravity_apply(silent=True)
        except Exception:
            pass
        try:
            self.after(3000, self._external_gravity_auto_tick)
        except Exception:
            pass

    def _external_build_offsets_panel(self, tab):
        self._external_offsets_data = None
        self._external_offsets_rows = []
        self._external_offsets_loading = False
        self._external_gravity_worker_active = False
        self._external_gravity_auto_confirmed = False
        self._external_gravity_originals = {}
        self.external_gravity_auto_var = tk.BooleanVar(value=bool(self.settings.get('external_gravity_auto_apply', False)))
        self.external_gravity_offset_var = tk.StringVar(value='')
        self.external_gravity_value_var = tk.StringVar(value=str(self.settings.get('external_gravity_value', '196.2')))
        self.external_offsets_search_var = tk.StringVar(value='')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        header = ttk.Frame(tab)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(header, text='Latest Windows offsets', font=('Segoe UI Semibold', 10)).pack(side='left')
        self.external_offsets_status = ttk.Label(header, text='Not loaded', foreground=_FFLAG_COLOR_MUTED)
        self.external_offsets_status.pack(side='right')
        controls = ttk.Frame(tab)
        controls.grid(row=1, column=0, sticky='nsew')
        controls.columnconfigure(0, weight=1)
        controls.rowconfigure(1, weight=1)
        search_row = ttk.Frame(controls)
        search_row.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        search = ttk.Entry(search_row, textvariable=self.external_offsets_search_var)
        search.pack(side='left', fill='x', expand=True)
        ttk.Button(search_row, text='Load Latest', command=lambda: self._external_load_latest_offsets(force=True)).pack(side='right', padx=(6, 0))
        self.external_offsets_tree = ttk.Treeview(controls, columns=('name', 'offset', 'type'), show='headings', selectmode='browse')
        for key, label, width in (('name', 'Name', 220), ('offset', 'Offset', 90), ('type', 'Type', 90)):
            self.external_offsets_tree.heading(key, text=label)
            self.external_offsets_tree.column(key, width=width, anchor='w', stretch=key == 'name')
        self.external_offsets_tree.tag_configure('gravity', foreground='#e0a34d')
        ybar = ttk.Scrollbar(controls, orient='vertical', command=self.external_offsets_tree.yview)
        self.external_offsets_tree.configure(yscrollcommand=ybar.set)
        self.external_offsets_tree.grid(row=1, column=0, sticky='nsew')
        ybar.grid(row=1, column=1, sticky='ns')
        self.external_offsets_tree.bind('<<TreeviewSelect>>', self._external_select_offset, add='+')
        self.external_offsets_search_var.trace_add('write', lambda *_: self._external_render_offsets_rows())
        details = ttk.LabelFrame(tab, text='Gravity', padding=8)
        details.grid(row=2, column=0, sticky='ew', pady=(8, 0))
        for column in range(4):
            details.columnconfigure(column, weight=1 if column in (1, 3) else 0)
        ttk.Label(details, text='Offset name').grid(row=0, column=0, sticky='w', padx=(0, 5), pady=3)
        self.external_selected_name = ttk.Label(details, text='World::Gravity')
        self.external_selected_name.grid(row=0, column=1, sticky='w', pady=3)
        ttk.Label(details, text='Offset type').grid(row=0, column=2, sticky='w', padx=(12, 5), pady=3)
        self.external_selected_type = ttk.Label(details, text='uintptr_t')
        self.external_selected_type.grid(row=0, column=3, sticky='w', pady=3)
        ttk.Label(details, text='Offset').grid(row=1, column=0, sticky='w', padx=(0, 5), pady=3)
        ttk.Entry(details, textvariable=self.external_gravity_offset_var, width=14).grid(row=1, column=1, sticky='w', pady=3)
        ttk.Label(details, text='Value type').grid(row=1, column=2, sticky='w', padx=(12, 5), pady=3)
        self.external_selected_value_type = ttk.Label(details, text='float')
        self.external_selected_value_type.grid(row=1, column=3, sticky='w', pady=3)
        ttk.Label(details, text='Gravity value').grid(row=2, column=0, sticky='w', padx=(0, 5), pady=3)
        ttk.Entry(details, textvariable=self.external_gravity_value_var, width=14).grid(row=2, column=1, sticky='w', pady=3)
        self.external_gravity_status = ttk.Label(details, text='Select a Roblox client from Clients before applying.', foreground=_FFLAG_COLOR_MUTED)
        self.external_gravity_status.grid(row=2, column=2, columnspan=2, sticky='w', padx=(12, 0), pady=3)
        footer = ttk.Frame(tab)
        footer.grid(row=3, column=0, sticky='ew', pady=(8, 0))
        ttk.Checkbutton(footer, text='Auto Apply', variable=self.external_gravity_auto_var, command=self._external_gravity_toggle_auto_apply).pack(side='left')
        self.external_apply_button = ttk.Button(footer, text='Apply', command=lambda: self._external_gravity_apply(silent=False))
        self.external_apply_button.pack(side='right')
        self.external_apply_button.configure(state='normal')
        self.external_selected_offset = ttk.Label(details, text='')
        self.external_selected_offset.grid_remove()
        self._external_load_latest_offsets()
        self.after(3000, self._external_gravity_auto_tick)
