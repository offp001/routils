import sys
from fflag.processes import list_roblox_clients
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
_FFLAG_COLOR_MUTED = globals().get('_FFLAG_COLOR_MUTED', '#9aa0a6')
_FFLAG_COLOR_SUCCESS = globals().get('_FFLAG_COLOR_SUCCESS', '#65d98b')
_FFLAG_COLOR_ERROR = globals().get('_FFLAG_COLOR_ERROR', '#ff6b6b')
_FFLAG_COLOR_WARNING = globals().get('_FFLAG_COLOR_WARNING', '#f2c94c')
_FFLAG_COLOR_WHITE = globals().get('_FFLAG_COLOR_WHITE', '#ffffff')
_FFLAG_DEFAULT_MODE = globals().get('_FFLAG_DEFAULT_MODE', 'Toggle')
_FFLAG_DEFAULT_TRUE = globals().get('_FFLAG_DEFAULT_TRUE', 'true')
_FFLAG_DEFAULT_FALSE = globals().get('_FFLAG_DEFAULT_FALSE', 'false')
_FFLAG_MAX_VALUE_BYTES = 4096

class FFlagMixin:
    def _sober_confirm_close_port_owner(self, program_name, pid=None, port=58443):
        dialog = tk.Toplevel(self)
        dialog.title('Port In Use')
        dialog.geometry('420x170')
        dialog.resizable(False, False)
        dialog.transient(self)
        theme_toplevel(dialog)
        outer = ttk.Frame(dialog, padding=18)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text=f'Do you want to close "{program_name}"?', font=('Segoe UI Semibold', 10), wraplength=370).pack(anchor='w', pady=(2, 8))
        detail = f'127.0.0.1:{int(port)}'
        if pid:
            detail += f' · PID {int(pid)}'
        ttk.Label(outer, text=detail).pack(anchor='w')
        result = {'confirmed': False}
        buttons = ttk.Frame(outer)
        buttons.pack(side='bottom', anchor='e', pady=(14, 0))
        def choose(value):
            result['confirmed'] = bool(value)
            dialog.destroy()
        ttk.Button(buttons, text='Yes', command=lambda: choose(True), width=10).pack(side='left', padx=(0, 8))
        ttk.Button(buttons, text='No', command=lambda: choose(False), width=10).pack(side='left')
        dialog.protocol('WM_DELETE_WINDOW', lambda: choose(False))
        dialog.bind('<Escape>', lambda _event: choose(False))
        dialog.bind('<Return>', lambda _event: choose(True))
        dialog.grab_set()
        dialog.focus_set()
        self.wait_window(dialog)
        return result['confirmed']

    def _sober_proxy_start_and_launch(self):
        if not sys.platform.startswith('linux'):
            return
        try:
            if sober_flatpak_running():
                messagebox.showwarning('FFlag', 'Sober is already running. Close Sober completely, then use Start Proxy + Launch Sober.', parent=self)
                return
            from sober_proxy.service import ProxyPortInUseError, SoberProxyService
            self._fflag_apply(silent=True)
            service = SoberProxyService(DATA_DIR)
            try:
                result = service.start_and_launch()
            except ProxyPortInUseError as error:
                if not error.pid:
                    raise
                if not self._sober_confirm_close_port_owner(error.process_name, error.pid, error.port):
                    self._fflag_status_text('Proxy start cancelled', _FFLAG_COLOR_MUTED)
                    return
                self._console_log(f'Closing {error.process_name} (PID {error.pid}) after confirmation because it owns 127.0.0.1:{error.port}.')
                service.terminate_port_owner(error.pid, error.port)
                result = service.start_and_launch()
            self._sober_proxy_service = service
            self._fflag_status_text('Proxy Running', _FFLAG_COLOR_SUCCESS)
            if hasattr(self, 'sober_proxy_status_label'):
                self.sober_proxy_status_label.configure(text=f"Running · PID {result['proxy_pid']}", foreground=_FFLAG_COLOR_SUCCESS)
            self._console_log(f"FFlag proxy started on 127.0.0.1:{result['port']}; CA bundle: {result['overlay_path']}")
            self._console_log(f"Proxy log: {result['log_path']}")
        except Exception as error:
            self._fflag_status_text('Proxy start failed', _FFLAG_COLOR_ERROR)
            self._console_log(f'FFlag proxy start failed: {error}')
            messagebox.showerror('FFlag', str(error), parent=self)

    def _sober_proxy_stop(self):
        if not sys.platform.startswith('linux'):
            return
        try:
            from sober_proxy.service import SoberProxyService
            service = SoberProxyService(DATA_DIR)
            service.stop()
            if hasattr(self, 'sober_proxy_status_label'):
                self.sober_proxy_status_label.configure(text='Proxy: stopped', foreground=_FFLAG_COLOR_MUTED)
            self._fflag_status_text('Proxy stopped', _FFLAG_COLOR_MUTED)
            self._console_log('FFlag proxy stopped and the previous CA bundle was restored.')
        except Exception as error:
            self._console_log(f'Sober proxy stop failed: {error}')
            messagebox.showerror('FFlag', str(error), parent=self)

    def _load_sober_fflag_catalog(self, force=False):
        if getattr(self, '_sober_fflag_catalog_loading', False) and not force:
            return
        try:
            from sober_proxy.fflag_catalog import fetch_fflag_catalog
        except Exception as error:
            self.fflag_reference_status.configure(text=f'Unable to load FFlag module: {error}')
            return
        self._sober_fflag_catalog_loading = True
        self._sober_fflag_catalog_generation = getattr(self, '_sober_fflag_catalog_generation', 0) + 1
        generation = self._sober_fflag_catalog_generation
        if hasattr(self, 'fflag_reference_status'):
            self.fflag_reference_status.configure(text='Loading FFlags…', foreground=_FFLAG_COLOR_MUTED)
        def worker():
            try:
                result = fetch_fflag_catalog(DATA_DIR, force=force)
            except Exception as error:
                result = {'entries': [], 'status': str(error), 'error': str(error), 'cached': False}
            try:
                self.after(0, lambda g=generation, r=result: self._sober_fflag_catalog_loaded(g, r))
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True, name='RoUtils-SoberFFlagCatalog').start()

    def _sober_fflag_catalog_loaded(self, generation, result):
        if generation != getattr(self, '_sober_fflag_catalog_generation', generation):
            return
        self._sober_fflag_catalog_loading = False
        self._sober_fflag_catalog_rows = list(result.get('entries') or [])
        self._sober_fflag_catalog_status = str(result.get('status') or result.get('error') or '')
        self._sober_fflag_catalog_error = bool(result.get('error'))
        color = _FFLAG_COLOR_SUCCESS if self._sober_fflag_catalog_rows and not self._sober_fflag_catalog_error else _FFLAG_COLOR_MUTED if self._sober_fflag_catalog_rows else _FFLAG_COLOR_ERROR
        self.fflag_reference_status.configure(text=self._sober_fflag_catalog_status, foreground=color)
        self._refresh_sober_fflag_catalog()
        self._refresh_fflag_list()
        self._fflag_check_source_flags()

    def _refresh_sober_fflag_catalog(self):
        tree = getattr(self, 'fflag_reference_tree', None)
        if tree is None:
            return
        try:
            if not tree.winfo_exists():
                return
        except Exception:
            return
        self._fflag_reference_render_token = getattr(self, '_fflag_reference_render_token', 0) + 1
        token = self._fflag_reference_render_token
        old_job = getattr(self, '_fflag_reference_render_job', None)
        if old_job:
            try:
                tree.after_cancel(old_job)
            except Exception:
                pass
        try:
            tree.delete(*tree.get_children())
        except Exception:
            pass
        needle = self.fflag_reference_search.get().strip().casefold()
        rows = [row for row in getattr(self, '_sober_fflag_catalog_rows', []) if not needle or needle in str(row[0]).casefold() or needle in str(row[1]).casefold()]
        status = getattr(self, '_sober_fflag_catalog_status', '')
        color = _FFLAG_COLOR_ERROR if not getattr(self, '_sober_fflag_catalog_rows', []) else _FFLAG_COLOR_MUTED if getattr(self, '_sober_fflag_catalog_error', False) else _FFLAG_COLOR_SUCCESS
        self.fflag_reference_status.configure(text=f'{len(rows):,} / {len(getattr(self, "_sober_fflag_catalog_rows", [])):,} · {status}', foreground=color)
        def insert_batch(start=0):
            if token != getattr(self, '_fflag_reference_render_token', None):
                return
            try:
                if not tree.winfo_exists():
                    return
            except Exception:
                return
            end = min(len(rows), start + 300)
            for pos in range(start, end):
                try:
                    tree.insert('', 'end', iid=f'sober_catalog_{token}_{pos}', text='+', values=rows[pos])
                except Exception:
                    pass
            if end < len(rows):
                self._fflag_reference_render_job = tree.after(1, insert_batch, end)
            else:
                self._fflag_reference_render_job = None
        insert_batch(0)


    def _fflag_favorites_path(self):
        return os.path.join(DATA_DIR, 'routils_fflag_favorites.json')

    def _fflag_load_favorites(self):
        try:
            with open(self._fflag_favorites_path(), 'r', encoding='utf-8') as source:
                data = json.load(source)
            if not isinstance(data, list):
                return []
            cleaned = []
            seen = set()
            for item in data:
                if not isinstance(item, dict) or not item.get('name'):
                    continue
                name = fflag_strip_prefix(str(item.get('name', '')).strip())
                key = name.casefold()
                if not key or key in seen:
                    continue
                value = str(item.get('value', ''))
                cleaned.append({'name': name, 'value': value, 'type': item.get('type') or fflag_infer_type(value)})
                seen.add(key)
            return cleaned
        except Exception:
            return []

    def _fflag_save_favorites(self):
        try:
            path = self._fflag_favorites_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            temporary = path + '.tmp'
            with open(temporary, 'w', encoding='utf-8') as output:
                json.dump(self.fflag_favorites, output, ensure_ascii=False, indent=2)
            os.replace(temporary, path)
        except Exception as error:
            self._console_log(f'Could not save FFlag favorites: {error}')

    def _build_fflag_side_panels(self, favorite_tab, presets_tab, hotkeys_tab):
        self.fflag_favorites = self._fflag_load_favorites()
        favorite_tab.rowconfigure(1, weight=1)
        favorite_tab.columnconfigure(0, weight=1)
        favorite_head = ttk.Frame(favorite_tab)
        favorite_head.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        ttk.Label(favorite_head, text='Favorited FFlags', font=('Segoe UI Semibold', 10)).pack(side='left')
        ttk.Button(favorite_head, text='Refresh', command=self._fflag_refresh_favorites_panel).pack(side='right')
        self.fflag_favorites_tree = ttk.Treeview(favorite_tab, columns=('name', 'type', 'value'), show='tree headings', selectmode='browse')
        self.fflag_favorites_tree.heading('#0', text='+')
        self.fflag_favorites_tree.column('#0', width=30, minwidth=30, stretch=False, anchor='center')
        for column, label, width, anchor in (('name', 'Name', 235, 'w'), ('type', 'Type', 65, 'center'), ('value', 'Value', 125, 'w')):
            self.fflag_favorites_tree.heading(column, text=label)
            self.fflag_favorites_tree.column(column, width=width, anchor=anchor, stretch=column != 'type')
        favorite_scroll = ttk.Scrollbar(favorite_tab, orient='vertical', command=self.fflag_favorites_tree.yview)
        self.fflag_favorites_tree.configure(yscrollcommand=favorite_scroll.set)
        self.fflag_favorites_tree.grid(row=1, column=0, sticky='nsew')
        favorite_scroll.grid(row=1, column=1, sticky='ns')
        self.fflag_favorites_tree.bind('<Button-1>', self._fflag_favorite_plus_click, add='+')
        self.fflag_favorites_tree.bind('<Double-1>', self._fflag_favorite_double_click)
        favorite_buttons = ttk.Frame(favorite_tab)
        favorite_buttons.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(7, 0))
        ttk.Button(favorite_buttons, text='Add to FFlags', command=self._fflag_add_selected_favorite).pack(side='left')
        ttk.Button(favorite_buttons, text='Remove Favorite', command=self._fflag_remove_favorite).pack(side='left', padx=(6, 0))
        self._fflag_refresh_favorites_panel()

        presets_tab.rowconfigure(1, weight=1)
        presets_tab.columnconfigure(0, weight=1)
        presets_head = ttk.Frame(presets_tab)
        presets_head.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        ttk.Label(presets_head, text='Presets', font=('Segoe UI Semibold', 10)).pack(side='left')
        ttk.Button(presets_head, text='Browse Online', command=self._fflag_presets_dialog).pack(side='right', padx=(5, 0))
        ttk.Button(presets_head, text='Refresh', command=self._fflag_refresh_local_presets).pack(side='right')
        self.fflag_presets_tree = ttk.Treeview(presets_tab, columns=('name', 'count'), show='tree headings', selectmode='browse')
        self.fflag_presets_tree.heading('#0', text='+')
        self.fflag_presets_tree.column('#0', width=30, minwidth=30, stretch=False, anchor='center')
        self.fflag_presets_tree.heading('name', text='Preset')
        self.fflag_presets_tree.heading('count', text='FFlags')
        self.fflag_presets_tree.column('name', width=270, anchor='w', stretch=True)
        self.fflag_presets_tree.column('count', width=75, anchor='center', stretch=False)
        preset_scroll = ttk.Scrollbar(presets_tab, orient='vertical', command=self.fflag_presets_tree.yview)
        self.fflag_presets_tree.configure(yscrollcommand=preset_scroll.set)
        self.fflag_presets_tree.grid(row=1, column=0, sticky='nsew')
        preset_scroll.grid(row=1, column=1, sticky='ns')
        self.fflag_presets_tree.bind('<Button-1>', self._fflag_add_preset_plus_click, add='+')
        self.fflag_presets_tree.bind('<Double-1>', lambda _event: self._fflag_add_selected_preset())
        preset_buttons = ttk.Frame(presets_tab)
        preset_buttons.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(7, 0))
        ttk.Button(preset_buttons, text='Add to FFlags', command=self._fflag_add_selected_preset).pack(side='left')
        ttk.Button(preset_buttons, text='Replace FFlags', command=lambda: self._fflag_add_selected_preset(replace=True)).pack(side='left', padx=(6, 0))
        self._fflag_refresh_local_presets()

        hotkeys_tab.rowconfigure(1, weight=1)
        hotkeys_tab.columnconfigure(0, weight=1)
        ttk.Label(hotkeys_tab, text='FFlag Hotkeys', font=('Segoe UI Semibold', 10)).grid(row=0, column=0, sticky='w', pady=(0, 6))
        columns = ('key', 'flag', 'mode', 'value1', 'value2')
        self.fflag_hotkeys_tree = ttk.Treeview(hotkeys_tab, columns=columns, show='headings', selectmode='browse')
        headers = {'key': 'KEY', 'flag': 'FFLAG', 'mode': 'MODE', 'value1': 'VALUE 1', 'value2': 'VALUE 2'}
        widths = {'key': 60, 'flag': 180, 'mode': 72, 'value1': 82, 'value2': 82}
        for column in columns:
            self.fflag_hotkeys_tree.heading(column, text=headers[column])
            self.fflag_hotkeys_tree.column(column, width=widths[column], minwidth=50, anchor='w', stretch=column == 'flag')
        hotkey_scroll = ttk.Scrollbar(hotkeys_tab, orient='vertical', command=self.fflag_hotkeys_tree.yview)
        self.fflag_hotkeys_tree.configure(yscrollcommand=hotkey_scroll.set)
        self.fflag_hotkeys_tree.grid(row=1, column=0, sticky='nsew')
        hotkey_scroll.grid(row=1, column=1, sticky='ns')
        self.fflag_hotkeys_tree.bind('<Double-1>', lambda _event: self._fflag_edit_selected_hotkey())
        hotkey_buttons = ttk.Frame(hotkeys_tab)
        hotkey_buttons.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(7, 0))
        ttk.Button(hotkey_buttons, text='Add', command=lambda: self._fflag_hotkey_editor(None, hotkeys_tab, self._fflag_refresh_hotkeys_panel)).pack(side='left')
        ttk.Button(hotkey_buttons, text='Edit', command=self._fflag_edit_selected_hotkey).pack(side='left', padx=(6, 0))
        ttk.Button(hotkey_buttons, text='Remove', command=self._fflag_remove_selected_hotkey).pack(side='left', padx=(6, 0))
        ttk.Button(hotkey_buttons, text='Refresh', command=self._fflag_refresh_hotkeys_panel).pack(side='right')
        self._fflag_refresh_hotkeys_panel()

    def _fflag_refresh_favorites_panel(self):
        tree = getattr(self, 'fflag_favorites_tree', None)
        if tree is None:
            return
        try:
            tree.delete(*tree.get_children())
            favorites = getattr(self, 'fflag_favorites', None)
            if not isinstance(favorites, list):
                self.fflag_favorites = self._fflag_load_favorites()
                favorites = self.fflag_favorites
            for index, item in enumerate(favorites):
                tree.insert('', 'end', iid=str(index), text='+', values=(item.get('name', ''), item.get('type', ''), item.get('value', '')))
        except Exception:
            pass

    def _fflag_toggle_favorite(self):
        selection = self.fflag_tree.selection() if hasattr(self, 'fflag_tree') else ()
        if not selection:
            return
        try:
            index = int(selection[0])
            source = self.fflag_flags[index]
            name = fflag_strip_prefix(str(source.get('name', '')).strip())
            key = name.casefold()
            favorites = self.fflag_load_favorites() if not hasattr(self, 'fflag_favorites') else self.fflag_favorites
            existing = next((i for i, item in enumerate(favorites) if fflag_strip_prefix(str(item.get('name', ''))).casefold() == key), None)
            if existing is None:
                value = str(source.get('value', ''))
                favorites.append({'name': name, 'value': value, 'type': source.get('type') or fflag_infer_type(value)})
                message = f'Added {name} to Favorited FFlags.'
            else:
                favorites.pop(existing)
                message = f'Removed {name} from Favorited FFlags.'
            self.fflag_favorites = favorites
            self._fflag_save_favorites()
            self._fflag_refresh_favorites_panel()
            self._console_log(message)
        except Exception as error:
            self._console_log(f'Could not update FFlag favorites: {error}')

    def _fflag_remove_favorite(self):
        tree = getattr(self, 'fflag_favorites_tree', None)
        selection = tree.selection() if tree is not None else ()
        if not selection:
            return
        try:
            index = int(selection[0])
            removed = self.fflag_favorites.pop(index)
            self._fflag_save_favorites()
            self._fflag_refresh_favorites_panel()
            self._console_log(f'Removed {removed.get("name", "FFlag")} from Favorited FFlags.')
        except Exception as error:
            self._console_log(f'Could not remove favorite: {error}')

    def _fflag_favorite_plus_click(self, event):
        tree = getattr(self, 'fflag_favorites_tree', None)
        if tree is None or tree.identify_column(event.x) != '#0':
            return None
        row = tree.identify_row(event.y)
        if row:
            try:
                item = self.fflag_favorites[int(row)]
                self._fflag_add_flag_to_current(item.get('name', ''), item.get('value', ''))
                return 'break'
            except Exception:
                return 'break'
        return None

    def _fflag_favorite_double_click(self, event):
        tree = getattr(self, 'fflag_favorites_tree', None)
        if tree is None:
            return
        row = tree.identify_row(event.y)
        if row:
            try:
                item = self.fflag_favorites[int(row)]
                self.clipboard_clear()
                self.clipboard_append(str(item.get('name', '')))
                self.update_idletasks()
            except Exception:
                pass

    def _fflag_add_selected_favorite(self):
        tree = getattr(self, 'fflag_favorites_tree', None)
        selection = tree.selection() if tree is not None else ()
        if not selection:
            return
        item = self.fflag_favorites[int(selection[0])]
        self._fflag_add_flag_to_current(item.get('name', ''), item.get('value', ''))

    def _fflag_refresh_local_presets(self):
        tree = getattr(self, 'fflag_presets_tree', None)
        if tree is None:
            return
        candidates = []
        roots = [os.path.join(DATA_DIR, 'presets')]
        bundle = getattr(sys, '_MEIPASS', BASE_DIR)
        for base in (os.path.join(bundle, 'src', 'presets'), os.path.join(BASE_DIR, 'src', 'presets'), os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'presets')):
            resolved = os.path.realpath(base)
            if resolved not in roots:
                roots.append(resolved)
        seen = set()
        seen_names = set()
        for directory in roots:
            if not os.path.isdir(directory):
                continue
            for filename in sorted(os.listdir(directory), key=str.casefold):
                if not filename.lower().endswith('.json'):
                    continue
                path = os.path.join(directory, filename)
                name_key = filename.casefold()
                if path in seen or name_key in seen_names:
                    continue
                seen.add(path)
                seen_names.add(name_key)
                try:
                    with open(path, 'r', encoding='utf-8') as source:
                        flags = _normalize_fflag_json(json.load(source))
                    if flags:
                        candidates.append({'name': os.path.splitext(filename)[0], 'path': path, 'flags': flags})
                except Exception:
                    continue
        self._fflag_local_presets = candidates
        try:
            tree.delete(*tree.get_children())
            for index, item in enumerate(candidates):
                tree.insert('', 'end', iid=str(index), text='+', values=(item['name'], len(item['flags'])))
        except Exception:
            pass

    def _fflag_add_preset_plus_click(self, event):
        tree = getattr(self, 'fflag_presets_tree', None)
        if tree is None or tree.identify_column(event.x) != '#0':
            return None
        row = tree.identify_row(event.y)
        if row:
            self._fflag_add_local_preset(int(row), replace=False)
            return 'break'
        return None

    def _fflag_add_selected_preset(self, replace=False):
        tree = getattr(self, 'fflag_presets_tree', None)
        selection = tree.selection() if tree is not None else ()
        if not selection:
            return
        self._fflag_add_local_preset(int(selection[0]), replace=replace)

    def _fflag_add_local_preset(self, index, replace=False):
        presets = getattr(self, '_fflag_local_presets', [])
        if not 0 <= index < len(presets):
            return
        preset = presets[index]
        incoming = [dict(item) for item in preset.get('flags', [])]
        if replace:
            candidate = incoming
        else:
            candidate = [dict(item) for item in self.fflag_flags if isinstance(item, dict)]
            locations = {fflag_strip_prefix(str(item.get('name', ''))).casefold(): pos for pos, item in enumerate(candidate)}
            for item in incoming:
                key = fflag_strip_prefix(str(item.get('name', ''))).casefold()
                if not key:
                    continue
                if key in locations:
                    candidate[locations[key]] = item
                else:
                    locations[key] = len(candidate)
                    candidate.append(item)
        if not self._fflag_confirm_large_values(candidate, self):
            return
        self.fflag_flags = candidate
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._fflag_check_source_flags()
        if self.fflag_pid and self.fflag_auto_apply.get():
            self._fflag_apply(silent=True)
        self._console_log(f'Loaded preset {preset["name"]}: {len(incoming)} FFlags.')

    def _fflag_refresh_hotkeys_panel(self):
        tree = getattr(self, 'fflag_hotkeys_tree', None)
        if tree is None:
            return
        try:
            tree.delete(*tree.get_children())
            for index, item in enumerate(self.fflag_hotkeys):
                tree.insert('', 'end', iid=str(index), values=(item.get('key', ''), item.get('flag', ''), item.get('mode', _FFLAG_DEFAULT_MODE), item.get('value1', _FFLAG_DEFAULT_TRUE), item.get('value2', _FFLAG_DEFAULT_FALSE)))
        except Exception:
            pass

    def _fflag_edit_selected_hotkey(self):
        tree = getattr(self, 'fflag_hotkeys_tree', None)
        selection = tree.selection() if tree is not None else ()
        if not selection:
            return
        self._fflag_hotkey_editor(int(selection[0]), getattr(self, 'fflag_hotkeys_tab', self), self._fflag_refresh_hotkeys_panel)

    def _fflag_remove_selected_hotkey(self):
        tree = getattr(self, 'fflag_hotkeys_tree', None)
        if tree is not None:
            self._remove_fflag_hotkey(tree, self._fflag_refresh_hotkeys_panel)

    def _fflag_add_flag_to_current(self, name, value, parent=None):
        clean_name = fflag_strip_prefix(str(name or '').strip())
        clean_value = str(value if value is not None else '').strip()
        if not clean_name:
            return
        candidate = [dict(item) for item in self.fflag_flags if isinstance(item, dict)]
        existing_index = next((index for index, item in enumerate(candidate) if fflag_strip_prefix(str(item.get('name', ''))).casefold() == clean_name.casefold()), None)
        if not clean_value or clean_value == '*':
            self._fflag_add_dialog(initial_name=clean_name, initial_value='')
            return
        new_item = {'name': clean_name, 'value': clean_value, 'type': fflag_infer_type(clean_value)}
        if existing_index is not None:
            if not messagebox.askyesno('FFlag Already Exists', f'{clean_name} is already in your FFlags list. Update its value?', parent=parent or self):
                return
            if existing_index >= len(candidate):
                return
            candidate[existing_index] = new_item
        else:
            candidate.append(new_item)
        if not self._fflag_confirm_large_values(candidate, parent or self):
            return
        self.fflag_flags = candidate
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._fflag_check_source_flags()
        if self.fflag_pid and (self.fflag_engine.handle or sys.platform.startswith('linux')):
            self._fflag_apply(silent=True)
        self._console_log(f'Added {clean_name} to FFlags.' if existing_index is None else f'Updated {clean_name}.')

    def _fflag_reference_plus_click(self, event):
        tree = getattr(self, 'fflag_reference_tree', None)
        if tree is None or tree.identify_column(event.x) != '#0':
            return None
        row = tree.identify_row(event.y)
        if not row:
            return None
        values = tree.item(row, 'values')
        if not values:
            return 'break'
        if len(values) >= 3:
            name, value = values[0], values[2]
        else:
            name, value = values[0], values[1] if len(values) > 1 else ''
        self._fflag_add_flag_to_current(name, value)
        return 'break'

    def _fflag_list_clients(self):
        return list_roblox_clients()

    def _fflag_client_account(self, pid, clients):
        username = str(self.settings.get('roblox_username', '') or '').strip() if hasattr(self, 'settings') else ''
        display_name = str(self.settings.get('roblox_display_name', '') or '').strip() if hasattr(self, 'settings') else ''
        if username and (len(clients) == 1 or int(pid) == int(getattr(self, 'fflag_pid', 0) or 0)):
            return f'{display_name} (@{username})' if display_name and display_name.casefold() != username.casefold() else f'@{username}'
        return '****'

    def _refresh_fflag_clients_panel(self):
        tree = getattr(self, '_fflag_clients_tree', None)
        if tree is None:
            return
        try:
            tree.delete(*tree.get_children())
            clients = self._fflag_list_clients()
            for item in clients:
                account = self._fflag_client_account(item['pid'], clients)
                tree.insert('', 'end', values=(item['pid'], account, item['process']))
            count = len(clients)
            label = getattr(self, '_fflag_clients_count_label', None)
            if label is not None:
                label.configure(text=f'{count} client' if count == 1 else f'{count} clients')
            if not clients:
                tree.insert('', 'end', values=('', '****', 'No Roblox clients detected'))
        except Exception:
            pass

    def _open_fflag_clients_panel(self):
        panel = getattr(self, '_fflag_clients_panel', None)
        if panel is not None:
            try:
                if panel.winfo_exists():
                    if panel.winfo_ismapped():
                        panel.place_forget()
                    else:
                        self._refresh_fflag_clients_panel()
                        panel.place(relx=1.0, x=-12, y=42, anchor='ne', width=440, height=340)
                        panel.lift()
                    return
            except Exception:
                pass
        bg = _CURRENT_PALETTE.get('bg_dark', '#111318')
        surface = _CURRENT_PALETTE.get('bg_medium', '#1a1d24')
        fg = _CURRENT_PALETTE.get('fg', '#e6e9ef')
        accent = _CURRENT_PALETTE.get('accent', '#8ab4f8')
        panel = tk.Frame(self, bg=bg, bd=0, highlightthickness=1, highlightbackground=accent)
        self._fflag_clients_panel = panel
        panel.place(relx=1.0, x=-12, y=42, anchor='ne', width=440, height=340)
        header = tk.Frame(panel, bg=bg)
        header.pack(fill='x', padx=10, pady=(8, 6))
        tk.Label(header, text='Roblox Clients', bg=bg, fg=fg, font=('Segoe UI Semibold', 11)).pack(side='left')
        self._fflag_clients_count_label = tk.Label(header, text='0 clients', bg=bg, fg='#9aa0a6', font=('Segoe UI', 8))
        self._fflag_clients_count_label.pack(side='left', padx=(8, 0))
        ttk.Button(header, text='Refresh', command=self._refresh_fflag_clients_panel).pack(side='right', padx=(4, 0))
        close = tk.Label(header, text='×', bg=bg, fg=fg, font=('Segoe UI', 16), cursor='hand2')
        close.pack(side='right', padx=(6, 4))
        close.bind('<Button-1>', lambda _event: panel.place_forget())
        listing = tk.Frame(panel, bg=surface)
        listing.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        listing.rowconfigure(0, weight=1)
        listing.columnconfigure(0, weight=1)
        self._fflag_clients_tree = ttk.Treeview(listing, columns=('pid', 'account', 'process'), show='headings', selectmode='browse')
        for column, title, width, anchor in (('pid', 'PID', 70, 'center'), ('account', 'Account', 180, 'w'), ('process', 'Process', 145, 'w')):
            self._fflag_clients_tree.heading(column, text=title)
            self._fflag_clients_tree.column(column, width=width, minwidth=55, anchor=anchor, stretch=column != 'pid')
        scroll = ttk.Scrollbar(listing, orient='vertical', command=self._fflag_clients_tree.yview)
        self._fflag_clients_tree.configure(yscrollcommand=scroll.set)
        self._fflag_clients_tree.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')
        self._refresh_fflag_clients_panel()
        panel.lift()
        return panel

    def _fflag_path(self):
        return os.path.join(DATA_DIR, 'routils_fflags.json')

    def _load_fflag_flags(self):
        try:
            with open(self._fflag_path(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.fflag_flags = data if isinstance(data, list) else []
        except Exception:
            self.fflag_flags = []

    def _fflag_source_names(self):
        if sys.platform.startswith('linux'):
            rows = getattr(self, '_sober_fflag_catalog_rows', None)
            if not rows or getattr(self, '_sober_fflag_catalog_error', False):
                return None
        else:
            rows = getattr(self, '_fflag_reference_rows', None)
            cache = getattr(self, '_fflag_reference_cache', None)
            if not rows or not isinstance(cache, dict) or not isinstance(cache.get('offsets'), dict) or not cache.get('offsets'):
                return None
        cached = getattr(self, '_fflag_source_names_cache', None)
        if isinstance(cached, tuple) and len(cached) == 2 and cached[0] == id(rows):
            return cached[1] or None
        names = set()
        for row in rows:
            try:
                raw_name = row.get('name', '') if isinstance(row, dict) else row[0]
                name = fflag_strip_prefix(str(raw_name or '').strip()).casefold()
                if name:
                    names.add(name)
            except Exception:
                continue
        self._fflag_source_names_cache = (id(rows), names)
        return names or None

    def _fflag_missing_source_names(self):
        source_names = self._fflag_source_names()
        if source_names is None:
            return None
        flag_names = tuple(
            fflag_strip_prefix(str(flag.get('name', '') or '').strip()).casefold()
            for flag in self.fflag_flags if isinstance(flag, dict)
        )
        cache_key = (id(source_names), flag_names)
        cached = getattr(self, '_fflag_missing_source_cache', None)
        if isinstance(cached, tuple) and len(cached) == 2 and cached[0] == cache_key:
            return set(cached[1])
        missing = {name for name in flag_names if name and name not in source_names}
        self._fflag_missing_source_cache = (cache_key, set(missing))
        return missing

    def _fflag_check_source_flags(self):
        missing = self._fflag_missing_source_names()
        if missing is None:
            return
        self._fflag_missing_source_names_cache = set(missing)
        if not missing:
            self._fflag_source_prompt_signature = None
            return
        signature = tuple(sorted(missing))
        if signature == getattr(self, '_fflag_source_prompt_signature', None):
            return
        self._fflag_source_prompt_signature = signature
        names = []
        for flag in self.fflag_flags:
            if not isinstance(flag, dict):
                continue
            name = fflag_strip_prefix(str(flag.get('name', '') or '').strip())
            if name.casefold() in missing and name not in names:
                names.append(name)
        shown = names[:8]
        details = '\n'.join(f'• {name}' for name in shown)
        if len(names) > len(shown):
            details += f'\n• and {len(names) - len(shown):,} more'
        prompt = (
            'Some FFlags in your list are not present in the current source:'
            f'\n\n{details}\n\nWould you like to remove these FFlags?'
        )
        if messagebox.askyesno('FFlag Source Check', prompt, parent=self):
            self.fflag_flags = [
                flag for flag in self.fflag_flags
                if not isinstance(flag, dict) or fflag_strip_prefix(str(flag.get('name', '') or '').strip()).casefold() not in missing
            ]
            self._fflag_source_prompt_signature = None
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._console_log(f'Removed {len(names)} FFlags that were not present in the current source.')

    def _fflag_confirm_large_values(self, flags=None, parent=None):
        current = self.fflag_flags if flags is None else flags
        large = []
        for flag in current:
            if not isinstance(flag, dict):
                continue
            value = str(flag.get('value', '') or '')
            size = len(value.encode('utf-8', 'replace'))
            if size > _FFLAG_MAX_VALUE_BYTES:
                name = fflag_strip_prefix(str(flag.get('name', '') or '').strip()) or 'Unnamed FFlag'
                large.append((name, size, value))
        if not large:
            self._fflag_large_value_approved = None
            return True
        signature = tuple(sorted((name.casefold(), size, value) for name, size, value in large))
        if signature == getattr(self, '_fflag_large_value_approved', None):
            return True
        details = '\n'.join(f'• {name}: {size:,} bytes' for name, size, _ in large[:6])
        if len(large) > 6:
            details += f'\n• and {len(large) - 6:,} more'
        prompt = (
            f'{len(large)} FFlag value(s) exceed {_FFLAG_MAX_VALUE_BYTES:,} bytes. '
            'Very large values may cause Roblox or Sober to fail while loading the configuration.'
            f'\n\n{details}\n\nContinue anyway?'
        )
        approved = messagebox.askyesno('Large FFlag Value', prompt, parent=parent or self)
        if approved:
            self._fflag_large_value_approved = signature
        return approved

    def _save_fflag_flags(self):
        try:
            path = self._fflag_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            temporary = path + '.tmp'
            with open(temporary, 'w', encoding='utf-8') as stream:
                json.dump(self.fflag_flags, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
            return True
        except Exception as error:
            self._console_log(f'FFlag save failed: {error}')
            self._fflag_status_text('FFlag save failed', _FFLAG_COLOR_ERROR)
            return False

    def _build_fflag_tab(self, tab=None):
        if tab is None:
            tab = ttk.Frame(self.nb, padding=12)
            self.nb.insert(1, tab, text='FFlag')
        else:
            for child in tab.winfo_children():
                child.destroy()
            tab.configure(padding=12)
            self.nb.tab(tab, text='FFlag')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=0 if sys.platform.startswith('linux') else 1)
        if sys.platform.startswith('linux'):
            tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        header_text = 'FFlag'
        ttk.Label(head, text=header_text, font=('Segoe UI Semibold', 15)).pack(side='left')
        self.fflag_status = ttk.Label(head, text=UI_TEXT['q13'], foreground=_FFLAG_COLOR_MUTED)
        self.fflag_status.pack(side='right', padx=(12, 0))
        ttk.Button(head, text='Clients', command=self._open_fflag_clients_panel).pack(side='right', padx=(8, 0))
        if sys.platform.startswith('linux'):
            proxy_controls = ttk.Frame(head)
            proxy_controls.pack(side='right', padx=(8, 0))
            self.sober_proxy_status_label = ttk.Label(proxy_controls, text='Proxy stopped', foreground=_FFLAG_COLOR_MUTED)
            self.sober_proxy_status_label.pack(side='left', padx=(0, 12))
            ttk.Button(proxy_controls, text='Start Proxy + Launch Sober', command=self._sober_proxy_start_and_launch).pack(side='left', padx=(0, 6), ipady=4, ipadx=3)
            ttk.Button(proxy_controls, text='Stop Proxy', command=self._sober_proxy_stop).pack(side='left', padx=(0, 6), ipady=4, ipadx=3)
            ttk.Button(proxy_controls, text='Open Sober Config', command=lambda: open_path(str(sober_config_path().parent))).pack(side='left', ipady=4, ipadx=3)
        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        toolbar = ttk.Frame(bar)
        toolbar.pack(side='left', fill='x', expand=True)
        toggles = ttk.Frame(bar)
        toggles.pack(side='right', padx=(8, 0))
        ttk.Checkbutton(toggles, text='Anti-AFK', variable=self.anti_afk_enabled, command=self._toggle_anti_afk).pack(side='left', padx=(0, 8))
        buttons = [(UI_TEXT['q32'], self._fflag_add_dialog), (UI_TEXT['q6'], self._fflag_remove), (UI_TEXT['r32'], self._fflag_remove_all), ('Favorite', self._fflag_toggle_favorite), ('Import', self._fflag_import), ('Export', self._fflag_export), ('JSON Editor', self._fflag_json_editor)]
        try:
            ttk.Style(self).configure('RoUtils.FFlag.Small.TButton', font=('Segoe UI', 8), padding=(4, 1))
        except Exception:
            pass
        self._fflag_toolbar = []
        self._fflag_toolbar_frame = toolbar
        for index, (text, cmd) in enumerate(buttons):
            button = ttk.Button(toolbar, text=text, command=cmd, style='RoUtils.FFlag.Small.TButton')
            button.grid(row=index // 8, column=index % 8, sticky='w', padx=(0, 4), pady=(0, 2))
            self._fflag_toolbar.append(button)
        for col in range(8):
            toolbar.columnconfigure(col, weight=0)
        toolbar.bind('<Configure>', self._responsive_fflag_toolbar, add='+')
        frame = ttk.PanedWindow(tab, orient='horizontal')
        frame.grid(row=2, column=0, sticky='nsew')
        left = ttk.Frame(frame)
        right = ttk.Frame(frame)
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)
        frame.add(left, weight=1)
        frame.add(right, weight=1)
        search_row = ttk.Frame(left)
        search_row.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        ttk.Label(search_row, text=UI_TEXT['k14']).pack(side='left')
        self.fflag_search = tk.StringVar()
        ent = ttk.Entry(search_row, textvariable=self.fflag_search)
        ent.pack(side='left', fill='x', expand=True, padx=6)
        self.fflag_search.trace_add('write', lambda *_: self._refresh_fflag_list())
        cols = ('name', 'type', 'value', 'remove')
        self.fflag_tree = ttk.Treeview(left, columns=cols, show='headings', selectmode='browse')
        self.fflag_tree.heading('name', text=UI_TEXT['y12'])
        self.fflag_tree.heading('type', text=UI_TEXT['l14'])
        self.fflag_tree.heading('value', text=UI_TEXT['m14'])
        self.fflag_tree.heading('remove', text=UI_TEXT['m1'])
        self.fflag_tree.column('name', width=280, anchor='w', stretch=True)
        self.fflag_tree.column('type', width=65, anchor='center', stretch=False)
        self.fflag_tree.column('value', width=130, anchor='w', stretch=True)
        self.fflag_tree.column('remove', width=28, minwidth=28, stretch=False, anchor='center')
        fflag_ybar = ttk.Scrollbar(left, orient='vertical', command=self.fflag_tree.yview)
        self.fflag_tree.configure(yscrollcommand=fflag_ybar.set)
        self.fflag_tree.grid(row=1, column=0, sticky='nsew')
        fflag_ybar.grid(row=1, column=1, sticky='ns')
        self.fflag_tree.bind('<Double-1>', self._fflag_inline_edit)
        self.fflag_tree.bind('<Button-1>', self._fflag_tree_click_remove, add='+')
        self.fflag_side_notebook = ttk.Notebook(right)
        self.fflag_side_notebook.grid(row=0, column=0, sticky='nsew')
        reference_tab = ttk.Frame(self.fflag_side_notebook, padding=8)
        favorite_tab = ttk.Frame(self.fflag_side_notebook, padding=8)
        presets_tab = ttk.Frame(self.fflag_side_notebook, padding=8)
        hotkeys_tab = ttk.Frame(self.fflag_side_notebook, padding=8)
        saved_tab = ttk.Frame(self.fflag_side_notebook, padding=8)
        history_tab = ttk.Frame(self.fflag_side_notebook, padding=8)
        self.fflag_history_tab = history_tab
        self.fflag_reference_tab = reference_tab
        self.fflag_saved_tab = saved_tab
        self.fflag_favorites_tab = favorite_tab
        self.fflag_presets_tab = presets_tab
        self.fflag_hotkeys_tab = hotkeys_tab
        if sys.platform.startswith('linux'):
            self.fflag_side_notebook.add(reference_tab, text='FFlags')
            self.fflag_side_notebook.add(favorite_tab, text='Favorited FFlags')
            self.fflag_side_notebook.add(presets_tab, text='Presets')
            self.fflag_side_notebook.add(hotkeys_tab, text='Hotkeys')
            self.fflag_side_notebook.add(saved_tab, text='Saved JSONs')
            self.fflag_side_notebook.add(history_tab, text='History')
            reference_tab.rowconfigure(1, weight=1)
            reference_tab.columnconfigure(0, weight=1)
            reference_head = ttk.Frame(reference_tab)
            reference_head.grid(row=0, column=0, sticky='ew', pady=(0, 6))
            self.fflag_reference_status = ttk.Label(reference_head, text='Loading FFlags…', foreground=_FFLAG_COLOR_MUTED)
            self.fflag_reference_status.pack(side='right')
            self.fflag_reference_search = tk.StringVar()
            reference_search = ttk.Entry(reference_head, textvariable=self.fflag_reference_search)
            reference_search.pack(side='left', fill='x', expand=True, padx=(0, 8))
            ttk.Button(reference_head, text='Refresh', command=lambda: self._load_sober_fflag_catalog(force=True)).pack(side='right', padx=(0, 8))
            self.fflag_reference_tree = ttk.Treeview(reference_tab, columns=('name', 'value'), show='tree headings', selectmode='browse')
            self.fflag_reference_tree.heading('#0', text='+')
            self.fflag_reference_tree.column('#0', width=30, minwidth=30, stretch=False, anchor='center')
            self.fflag_reference_tree.heading('name', text='Name')
            self.fflag_reference_tree.heading('value', text='Value')
            self.fflag_reference_tree.column('name', width=330, minwidth=180, anchor='w', stretch=True)
            self.fflag_reference_tree.column('value', width=180, minwidth=100, anchor='w', stretch=True)
            ref_ybar = ttk.Scrollbar(reference_tab, orient='vertical', command=self.fflag_reference_tree.yview)
            ref_xbar = ttk.Scrollbar(reference_tab, orient='horizontal', command=self.fflag_reference_tree.xview)
            self.fflag_reference_tree.configure(yscrollcommand=ref_ybar.set, xscrollcommand=ref_xbar.set)
            self.fflag_reference_tree.grid(row=1, column=0, sticky='nsew')
            ref_ybar.grid(row=1, column=1, sticky='ns')
            ref_xbar.grid(row=2, column=0, sticky='ew')
            self.fflag_reference_tree.bind('<Double-1>', lambda event: self._copy_fflag_reference_row(self.fflag_reference_tree, event))
            self.fflag_reference_tree.bind('<Button-1>', self._fflag_reference_plus_click, add='+')
            self.fflag_reference_search.trace_add('write', lambda *_: self._schedule_ui('sober_fflag_catalog_filter', 70, self._refresh_sober_fflag_catalog))
            self._sober_fflag_catalog_rows = []
            self._sober_fflag_catalog_status = ''
            self._sober_fflag_catalog_generation = 0
            self._sober_fflag_catalog_loading = False
            self._fflag_reference_render_job = None
            self._fflag_reference_render_token = 0
            self._fflag_reference_load_started = True
            self._load_sober_fflag_catalog(force=False)
        else:
            self.fflag_side_notebook.add(reference_tab, text=UI_TEXT['n14'])
            self.fflag_side_notebook.add(favorite_tab, text='Favorited FFlags')
            self.fflag_side_notebook.add(presets_tab, text='Presets')
            self.fflag_side_notebook.add(hotkeys_tab, text='Hotkeys')
            self.fflag_side_notebook.add(saved_tab, text='Saved JSONs')
            self.fflag_side_notebook.add(history_tab, text='History')
            reference_tab.rowconfigure(1, weight=1)
            reference_tab.columnconfigure(0, weight=1)
            reference_head = ttk.Frame(reference_tab)
            reference_head.grid(row=0, column=0, sticky='ew', pady=(0, 6))
            self.fflag_reference_status = ttk.Label(reference_head, text=UI_TEXT['p14'], foreground=_FFLAG_COLOR_MUTED)
            self.fflag_reference_status.pack(side='right')
            self.fflag_reference_search = tk.StringVar()
            reference_search = ttk.Entry(reference_head, textvariable=self.fflag_reference_search)
            reference_search.pack(side='left', fill='x', expand=True, padx=(0, 8))
            self.fflag_reference_tree = ttk.Treeview(reference_tab, columns=('name', 'offset', 'value'), show='tree headings', selectmode='browse')
            self.fflag_reference_tree.heading('#0', text='+')
            self.fflag_reference_tree.column('#0', width=30, minwidth=30, stretch=False, anchor='center')
            self.fflag_reference_tree.heading('name', text=UI_TEXT['q14'])
            self.fflag_reference_tree.heading('offset', text=UI_TEXT['r14'])
            self.fflag_reference_tree.heading('value', text=UI_TEXT['s14'])
            self.fflag_reference_tree.column('name', width=260, anchor='w', stretch=True)
            self.fflag_reference_tree.column('offset', width=105, anchor='w', stretch=False)
            self.fflag_reference_tree.column('value', width=100, anchor='w', stretch=True)
            ref_ybar = ttk.Scrollbar(reference_tab, orient='vertical', command=self.fflag_reference_tree.yview)
            ref_xbar = ttk.Scrollbar(reference_tab, orient='horizontal', command=self.fflag_reference_tree.xview)
            self.fflag_reference_tree.configure(yscrollcommand=ref_ybar.set, xscrollcommand=ref_xbar.set)
            self.fflag_reference_tree.grid(row=1, column=0, sticky='nsew')
            ref_ybar.grid(row=1, column=1, sticky='ns')
            ref_xbar.grid(row=2, column=0, sticky='ew')
            self.fflag_reference_tree.bind('<Double-1>', lambda event: self._copy_fflag_reference_row(self.fflag_reference_tree, event))
            self.fflag_reference_search.trace_add('write', lambda *_: self._schedule_ui('fflag_reference_filter', 70, self._refresh_fflag_reference_panel))
            self._fflag_reference_rows = []
            self._fflag_reference_render_job = None
            self._fflag_reference_render_token = 0
            self._fflag_reference_load_started = False
        self._build_fflag_side_panels(favorite_tab, presets_tab, hotkeys_tab)
        saved_tab.rowconfigure(1, weight=1)
        saved_tab.columnconfigure(0, weight=1)
        ttk.Label(saved_tab, text=UI_TEXT['o14'], font=('Segoe UI Semibold', 10)).grid(row=0, column=0, sticky='w', pady=(0, 6))
        self.json_tree = tk.Listbox(saved_tab, bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], relief='flat', bd=0, highlightthickness=0, selectbackground=_CURRENT_PALETTE['accent'], selectforeground=_FFLAG_COLOR_WHITE)
        json_ybar = ttk.Scrollbar(saved_tab, orient='vertical', command=self.json_tree.yview)
        self.json_tree.configure(yscrollcommand=json_ybar.set)
        self.json_tree.grid(row=1, column=0, sticky='nsew')
        json_ybar.grid(row=1, column=1, sticky='ns')
        self.json_tree.bind('<Double-1>', lambda _e: self._apply_selected_json())
        json_buttons = ttk.Frame(saved_tab)
        json_buttons.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(8, 0))
        ttk.Button(json_buttons, text=UI_TEXT['t14'], command=self._apply_selected_json).pack(side='left', fill='x', expand=True, padx=(0, 4))
        ttk.Button(json_buttons, text=UI_TEXT['c12'], command=self._refresh_json_list).pack(side='right')
        self._refresh_json_list()
        history_tab.rowconfigure(1, weight=1)
        history_tab.columnconfigure(0, weight=1)
        history_head = ttk.Frame(history_tab)
        history_head.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        self.fflag_history_search = tk.StringVar()
        history_search = ttk.Entry(history_head, textvariable=self.fflag_history_search)
        history_search.pack(side='left', fill='x', expand=True, padx=(0, 6))
        ttk.Button(history_head, text='Refresh', command=self._fflag_history_refresh).pack(side='left', padx=(0, 4))
        ttk.Button(history_head, text='Clear', command=self._fflag_history_clear).pack(side='left')
        history_body = ttk.Frame(history_tab)
        history_body.grid(row=1, column=0, sticky='nsew')
        history_body.rowconfigure(0, weight=1)
        history_body.columnconfigure(0, weight=1)
        self.fflag_history_text = tk.Text(history_body, wrap='none', height=10, undo=False, relief='flat', bd=0, highlightthickness=1, highlightbackground=_CURRENT_PALETTE.get('border', '#444446'), bg=_CURRENT_PALETTE.get('bg_medium', '#252526'), fg=_CURRENT_PALETTE.get('fg', '#dcdcdc'), insertbackground=_FFLAG_COLOR_WHITE, selectbackground=_CURRENT_PALETTE.get('accent', '#7f8cff'), font=('Consolas', 9), padx=9, pady=8, state='disabled')
        history_ybar = ttk.Scrollbar(history_body, orient='vertical', command=self.fflag_history_text.yview)
        history_xbar = ttk.Scrollbar(history_body, orient='horizontal', command=self.fflag_history_text.xview)
        self.fflag_history_text.configure(yscrollcommand=history_ybar.set, xscrollcommand=history_xbar.set)
        self.fflag_history_text.grid(row=0, column=0, sticky='nsew')
        history_ybar.grid(row=0, column=1, sticky='ns')
        history_xbar.grid(row=1, column=0, sticky='ew')
        self.fflag_history_text.tag_configure('history_add', foreground=_FFLAG_COLOR_SUCCESS)
        self.fflag_history_text.tag_configure('history_old', foreground=_FFLAG_COLOR_ERROR)
        self.fflag_history_text.tag_configure('history_new', foreground=_FFLAG_COLOR_SUCCESS)
        self.fflag_history_text.tag_configure('history_meta', foreground=_FFLAG_COLOR_MUTED)
        self.fflag_history_text.tag_configure('history_title', foreground='#8ab4f8', font=('Segoe UI Semibold', 9))
        self.fflag_history_text.tag_configure('history_removed', foreground=_FFLAG_COLOR_ERROR)
        self.fflag_history_text.tag_configure('history_separator', foreground='#565b66')
        self.fflag_history_search.trace_add('write', lambda *_: self._schedule_ui('fflag_history_filter', 90, self._fflag_history_refresh))
        self._fflag_history_refresh()
        bottom = ttk.Frame(tab)
        bottom.grid(row=4 if sys.platform.startswith('linux') else 3, column=0, sticky='ew', pady=(8, 0))
        self.fflag_auto_apply_button = ttk.Button(bottom, text=UI_TEXT['u14'] if self.fflag_auto_apply.get() else UI_TEXT['v14'], command=self._toggle_fflag_auto_apply)
        self.fflag_auto_apply_button.pack(side='right', padx=(5, 0))
        ttk.Button(bottom, text=UI_TEXT['w14'], command=lambda: self._fflag_apply(silent=True)).pack(side='right', padx=(5, 0))
        ttk.Button(bottom, text=UI_TEXT['x14'], command=self._save_fflag_flags).pack(side='right')
        ttk.Button(bottom, text=UI_TEXT['c12'], command=self._fflag_refresh_process).pack(side='left')
        self._refresh_fflag_list()
        self.after(350, self._fflag_refresh_process)
        if not sys.platform.startswith('linux'):
            self._load_fflag_reference_panel()

    def _responsive_fflag_toolbar(self, _event=None):
        bar = getattr(self, '_fflag_toolbar_frame', None)
        buttons = getattr(self, '_fflag_toolbar', [])
        if bar is None or not buttons:
            return
        if getattr(self, '_resize_active', False):
            self._resize_deferred_jobs['fflag_toolbar'] = (0, self._responsive_fflag_toolbar)
            return
        try:
            width = max(1, bar.winfo_width())
            columns = 8 if width >= 900 else 6 if width >= 680 else 4 if width >= 430 else 2
            if columns == getattr(self, '_fflag_toolbar_columns', None):
                return
            self._fflag_toolbar_columns = columns
            for index, button in enumerate(buttons):
                button.grid_configure(row=index // columns, column=index % columns, sticky='w')
            for col in range(8):
                bar.columnconfigure(col, weight=0)
        except Exception:
            pass

    def _refresh_fflag_list(self):
        if not hasattr(self, 'fflag_tree'):
            return
        self._fflag_history_track_changes()
        self.fflag_tree.delete(*self.fflag_tree.get_children())
        filt = self.fflag_search.get().strip().lower() if hasattr(self, 'fflag_search') else ''
        conflicts = self._fflag_conflicts()
        missing = self._fflag_missing_source_names()
        self._fflag_missing_source_names_cache = set(missing or ())
        try:
            self.fflag_tree.tag_configure('conflict', background='#8b1e1e', foreground=_FFLAG_COLOR_WHITE)
            self.fflag_tree.tag_configure('source_missing', background='#493318', foreground='#ffb454')
        except Exception:
            pass
        for i, flag in enumerate(self.fflag_flags):
            if not isinstance(flag, dict):
                continue
            name = fflag_strip_prefix(str(flag.get('name', '')))
            folded = name.casefold()
            if filt and filt not in name.lower():
                continue
            if folded in conflicts:
                tags = ('conflict',)
            elif missing is not None and folded in missing:
                tags = ('source_missing',)
            else:
                tags = ()
            self.fflag_tree.insert('', 'end', iid=str(i), values=(name, flag.get('type', ''), flag.get('value', ''), '×'), tags=tags)

    def _fflag_conflicts(self):
        counts = {}
        for flag in self.fflag_flags:
            name = fflag_strip_prefix(str(flag.get('name', '')).strip())
            if name:
                key = name.lower()
                counts[key] = counts.get(key, 0) + 1
        return {name for name, count in counts.items() if count > 1}

    def _fflag_tree_click_remove(self, event):
        try:
            row = self.fflag_tree.identify_row(event.y)
            col = self.fflag_tree.identify_column(event.x)
            if row and col == '#4':
                idx = int(row)
                if 0 <= idx < len(self.fflag_flags):
                    self.fflag_flags.pop(idx)
                    self._save_fflag_flags()
                    self._refresh_fflag_list()
                    self._console_log(UI_TEXT['b15'])
                return 'break'
        except Exception:
            pass
        return None

    def _fflag_add_dialog(self, initial_name="", initial_value=""):
        dlg = tk.Toplevel(self)
        dlg.title(UI_TEXT['y31'])
        dlg.transient(self)
        dlg.grab_set()
        theme_toplevel(dlg)
        ttk.Label(dlg, text=UI_TEXT['c15']).grid(row=0, column=0, padx=10, pady=(10, 4), sticky='w')
        name = ttk.Entry(dlg, width=48)
        name.grid(row=1, column=0, padx=10, sticky='ew')
        if initial_name:
            name.insert(0, str(initial_name))
        ttk.Label(dlg, text=UI_TEXT['d15']).grid(row=2, column=0, padx=10, pady=(8, 4), sticky='w')
        value = ttk.Entry(dlg, width=48)
        value.grid(row=3, column=0, padx=10, sticky='ew')
        if initial_value:
            value.insert(0, str(initial_value))
        def add():
            n, v = (name.get().strip(), value.get().strip())
            if not n or not v:
                return
            bare = fflag_strip_prefix(n)
            item = {'name': bare, 'value': v, 'type': fflag_infer_type(v)}
            prefix = _prefix_from_name(n)
            if prefix:
                item['prefix'] = prefix
            candidate = [dict(flag) for flag in self.fflag_flags if isinstance(flag, dict)] + [item]
            if not self._fflag_confirm_large_values(candidate, dlg):
                return
            self.fflag_flags.append(item)
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._fflag_check_source_flags()
            self._fflag_apply(silent=True)
            dlg.destroy()
            self._console_log(UI_TEXT['e15'].format(p0=bare, p1=v))
        btns = ttk.Frame(dlg)
        btns.grid(row=4, column=0, pady=10)
        ttk.Button(btns, text=UI_TEXT['f15'], command=add).pack(side='left', padx=4)
        ttk.Button(btns, text=UI_TEXT['b3'], command=dlg.destroy).pack(side='left', padx=4)
        dlg.columnconfigure(0, weight=1)
        name.focus_set()

    def _fflag_inline_edit(self, event):
        tree = self.fflag_tree
        row = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if not row or col not in ('#1', '#3'):
            return
        idx = int(row)
        column = 'name' if col == '#1' else 'value'
        bbox = tree.bbox(row, col)
        if not bbox:
            return
        x, y, w, h = bbox
        entry = ttk.Entry(tree)
        entry.place(x=x, y=y, width=w, height=h)
        entry.insert(0, str(self.fflag_flags[idx].get(column, '')))
        entry.focus_set()
        entry.selection_range(0, 'end')
        def save(_=None):
            if not entry.winfo_exists():
                return
            value = entry.get().strip()
            if value:
                candidate = [dict(flag) for flag in self.fflag_flags if isinstance(flag, dict)]
                if idx >= len(candidate):
                    entry.destroy()
                    return
                if column == 'name':
                    candidate[idx]['name'] = fflag_strip_prefix(value)
                    prefix = _prefix_from_name(value)
                    if prefix:
                        candidate[idx]['prefix'] = prefix
                    else:
                        candidate[idx].pop('prefix', None)
                else:
                    candidate[idx][column] = value
                    if not self._fflag_confirm_large_values(candidate, self):
                        entry.focus_set()
                        return 'break'
                candidate[idx]['type'] = fflag_infer_type(candidate[idx].get('value', ''))
                self.fflag_flags = candidate
                self._save_fflag_flags()
                self._refresh_fflag_list()
                self._fflag_check_source_flags()
                self._fflag_apply(silent=True)
            entry.destroy()
        entry.bind('<Return>', save)
        entry.bind('<FocusOut>', save)
        entry.bind('<Escape>', lambda _e: entry.destroy())

    def _fflag_remove(self):
        sel = self.fflag_tree.selection()
        if not sel:
            return
        removed = self.fflag_flags[int(sel[0])].get('name', '')
        del self.fflag_flags[int(sel[0])]
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._console_log(UI_TEXT['g15'].format(p0=removed))

    def _fflag_remove_all(self):
        if not self.fflag_flags or not messagebox.askyesno(UI_TEXT['h5'], UI_TEXT['h15'], parent=self):
            return
        self.fflag_flags.clear()
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._console_log(UI_TEXT['i15'])

    def _fflag_json_editor(self):
        dlg = tk.Toplevel(self)
        dlg.title('JSON Editor')
        dlg.geometry('620x460')
        theme_toplevel(dlg)
        txt = tk.Text(dlg, wrap='none', font=('Consolas', 10), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground='#fff')
        txt.pack(fill='both', expand=True, padx=10, pady=10)
        ttk.Button(dlg, text=UI_TEXT['s10'], command=lambda: self._add_json_editor_value(txt, dlg)).pack(pady=(0, 10))

    def _fflag_presets_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title('FFlag Presets')
        dlg.geometry('620x520')
        dlg.transient(self)
        theme_toplevel(dlg)
        ttk.Label(dlg, text=UI_TEXT['j15'], font=('Segoe UI Semibold', 12)).pack(anchor='w', padx=12, pady=(10, 6))
        ttk.Label(dlg, text=UI_TEXT['k15'], foreground=_FFLAG_COLOR_MUTED).pack(anchor='w', padx=12, pady=(0, 8))
        search = tk.StringVar()
        ttk.Entry(dlg, textvariable=search).pack(fill='x', padx=12, pady=(0, 8))
        body = ttk.Frame(dlg)
        body.pack(fill='both', expand=True, padx=12, pady=4)
        canvas = tk.Canvas(body, bg=_CURRENT_PALETTE['bg_medium'], highlightthickness=0, bd=0)
        scroll = ttk.Scrollbar(body, orient='vertical', command=canvas.yview)
        inner = ttk.Frame(canvas, style='RoUtils.Settings.TFrame')
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        window = canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind('<Configure>', lambda _e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(window, width=e.width))
        state = {'files': []}
        status = ttk.Label(dlg, text=UI_TEXT['u15'], foreground=_FFLAG_COLOR_MUTED)
        status.pack(anchor='w', padx=12, pady=(0, 6))
        def load_preset(url, filename, add_to_current=False, local_path=None):
            try:
                if local_path and os.path.isfile(local_path):
                    with open(local_path, 'r', encoding='utf-8') as source:
                        data = json.load(source)
                else:
                    with _routils_request(url, timeout=18, headers={'Accept': 'application/json'}, cache_bypass=True) as response:
                        body = response.read(2 * 1024 * 1024 + 1)
                    if len(body) > 2 * 1024 * 1024:
                        raise ValueError('Preset JSON is larger than the allowed size.')
                    data = json.loads(body.decode('utf-8-sig'))
                flags = _normalize_fflag_json(data)
                if not flags:
                    raise ValueError('Preset JSON did not contain any FFlags.')
                if add_to_current:
                    candidate = [dict(item) for item in self.fflag_flags if isinstance(item, dict)]
                    existing = {str(item.get('name', '')).casefold(): i for i, item in enumerate(candidate)}
                    added = 0
                    updated = 0
                    for flag in flags:
                        name = str(flag.get('name', ''))
                        key = name.casefold()
                        if key in existing:
                            candidate[existing[key]] = flag
                            updated += 1
                        else:
                            candidate.append(flag)
                            existing[key] = len(candidate) - 1
                            added += 1
                    if not self._fflag_confirm_large_values(candidate, dlg):
                        return
                    self.fflag_flags = candidate
                    self._save_fflag_flags()
                    self._refresh_fflag_list()
                    self._fflag_check_source_flags()
                    if self.fflag_pid and getattr(self.fflag_engine, 'handle', None) and self.fflag_auto_apply.get():
                        self._fflag_apply(silent=True)
                    messagebox.showinfo(UI_TEXT['l15'], UI_TEXT['m15'].format(p0=added, p1=updated, p2=filename), parent=dlg)
                    self._console_log(UI_TEXT['n15'].format(p0=filename, p1=added, p2=updated))
                else:
                    if not self._fflag_confirm_large_values(flags, dlg):
                        return
                    self.fflag_flags = flags
                    self._save_fflag_flags()
                    self._refresh_fflag_list()
                    self._fflag_check_source_flags()
                    if self.fflag_pid and getattr(self.fflag_engine, 'handle', None) and self.fflag_auto_apply.get():
                        self._fflag_apply(silent=True)
                    messagebox.showinfo(UI_TEXT['l15'], UI_TEXT['o15'].format(p0=len(flags), p1=filename), parent=dlg)
                    self._console_log(UI_TEXT['p15'].format(p0=filename, p1=len(flags)))
                dlg.destroy()
            except Exception as error:
                messagebox.showerror(UI_TEXT['l15'], UI_TEXT['q15'].format(p0=filename, p1=error), parent=dlg)
        def render(*_):
            for widget in inner.winfo_children():
                widget.destroy()
            needle = search.get().strip().casefold()
            for item in state['files']:
                name = item.get('name', '')
                if needle and needle not in name.casefold():
                    continue
                label = os.path.splitext(name)[0]
                row = ttk.Frame(inner)
                row.pack(fill='x', pady=3)
                local_path = item.get('_local_path')
                ttk.Button(row, text=label, command=lambda u=item['download_url'], n=label, p=local_path: load_preset(u, n, False, p)).pack(side='left', fill='x', expand=True, padx=(0, 4))
                ttk.Button(row, text=UI_TEXT['r15'], command=lambda u=item['download_url'], n=label, p=local_path: load_preset(u, n, True, p)).pack(side='right')
        def cache_remote_preset(item):
            filename = os.path.basename(str(item.get('name') or '')).strip()
            url = str(item.get('download_url') or '').strip()
            parsed = urlparse(url)
            if not filename.lower().endswith('.json') or parsed.scheme != 'https' or parsed.hostname != 'raw.githubusercontent.com':
                return False
            try:
                with _routils_request(url, timeout=20, headers={'Accept': 'application/json'}, cache_bypass=True) as response:
                    body = response.read(2 * 1024 * 1024 + 1)
                if not body or len(body) > 2 * 1024 * 1024:
                    return False
                payload = json.loads(body.decode('utf-8-sig'))
                if not _normalize_fflag_json(payload):
                    return False
                safe_name = re.sub(r'[^A-Za-z0-9._ -]', '_', filename)
                if safe_name in {'', '.', '..'}:
                    return False
                directory = os.path.join(DATA_DIR, 'presets')
                os.makedirs(directory, exist_ok=True)
                destination = os.path.join(directory, safe_name)
                temporary = destination + '.download'
                with open(temporary, 'wb') as output:
                    output.write(body)
                os.replace(temporary, destination)
                item['_local_path'] = destination
                return True
            except Exception:
                return False
        def worker():
            try:
                with _routils_request(GITHUB_PRESETS_API, timeout=20, headers={'Accept': 'application/vnd.github+json'}, cache_bypass=True) as response:
                    items = json.loads(response.read().decode('utf-8-sig'))
                if not isinstance(items, list):
                    raise ValueError('GitHub returned an unexpected preset listing.')
                files = [item for item in items if isinstance(item, dict) and item.get('type') == 'file' and str(item.get('name', '')).lower().endswith('.json') and item.get('download_url')]
                files.sort(key=lambda item: str(item.get('name', '')).casefold())
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=5, thread_name_prefix='RoUtilsPreset') as executor:
                    cached_count = sum(executor.map(cache_remote_preset, files))
                def done():
                    if not dlg.winfo_exists():
                        return
                    state['files'] = files
                    render()
                    self._fflag_refresh_local_presets()
                    if files:
                        status.configure(text=f'Saved {cached_count} of {len(files)} online presets to the local Presets list.')
                    else:
                        status.configure(text=UI_TEXT['s15'])
                self.after(0, done)
            except Exception as error:
                message = str(error)
                self.after(0, lambda detail=message: status.configure(text=UI_TEXT['t15'].format(p0=detail)))
        search.trace_add('write', render)
        ttk.Label(inner, text=UI_TEXT['u15'], foreground=_FFLAG_COLOR_MUTED).pack(pady=20)
        threading.Thread(target=worker, daemon=True, name='RoUtilsOnlinePresets').start()

    def _fflag_import(self):
        path = filedialog.askopenfilename(parent=self, title=UI_TEXT['x15'], filetypes=[(UI_TEXT['y15'], '*.json'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            candidate = [dict(flag) for flag in self.fflag_flags if isinstance(flag, dict)]
            count = 0
            if isinstance(data, dict):
                for n, v in data.items():
                    bare = fflag_strip_prefix(n)
                    found = next((x for x in candidate if x.get('name') == bare), None)
                    item = {'name': bare, 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)}
                    if found:
                        found.update(item)
                    else:
                        candidate.append(item)
                    count += 1
            elif isinstance(data, list):
                for x in data:
                    if isinstance(x, dict) and x.get('name') is not None:
                        item = {'name': fflag_strip_prefix(x['name']), 'value': str(x.get('value', '')), 'type': x.get('type') or fflag_infer_type(x.get('value', ''))}
                        candidate.append(item)
                        count += 1
            else:
                raise ValueError('JSON must be an object or an array.')
            if not self._fflag_confirm_large_values(candidate, self):
                return
            self.fflag_flags = candidate
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._fflag_check_source_flags()
            messagebox.showinfo(UI_TEXT['h5'], UI_TEXT['z15'].format(p0=count), parent=self)
            self._console_log(UI_TEXT['a16'].format(p0=count, p1=os.path.basename(path)))
        except Exception as e:
            messagebox.showerror(UI_TEXT['h5'], UI_TEXT['b16'].format(p0=e), parent=self)

    def _fflag_export(self):
        if not self.fflag_flags:
            return
        data = {x['name']: x['value'] for x in self.fflag_flags}
        dialog = tk.Toplevel(self)
        dialog.title(UI_TEXT['z31'])
        dialog.geometry('470x170')
        dialog.minsize(430, 150)
        dialog.transient(self)
        dialog.grab_set()
        theme_toplevel(dialog)
        ttk.Label(dialog, text=UI_TEXT['c16'], font=('Segoe UI Semibold', 10)).pack(anchor='w', padx=14, pady=(14, 4))
        name_var = tk.StringVar(value=f"fflags_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        ttk.Entry(dialog, textvariable=name_var).pack(fill='x', padx=14, pady=(0, 12))
        buttons = ttk.Frame(dialog)
        buttons.pack(fill='x', padx=14)
        def save_json(path, target_label):
            try:
                base = _sanitize_filename_for_windows(name_var.get().strip()) or 'fflags'
                if not base.lower().endswith('.json'):
                    base += '.json'
                if path is None:
                    path = os.path.join(DATA_DIR, 'jsons', base)
                elif os.path.isdir(path):
                    path = os.path.join(path, base)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                try:
                    in_file_saves = hasattr(self.replacer, 'file_saves_dir') and os.path.commonpath((os.path.abspath(path), os.path.abspath(self.replacer.file_saves_dir))) == os.path.abspath(self.replacer.file_saves_dir)
                except ValueError:
                    in_file_saves = False
                if in_file_saves:
                    self.replacer.source_var.set('FileSaves')
                    self.replacer.refresh_view(preserve_selection=True)
                self._console_log(UI_TEXT['d16'].format(p0=len(data), p1=target_label, p2=path))
                dialog.destroy()
            except Exception as e:
                messagebox.showerror(UI_TEXT['h5'], UI_TEXT['e16'].format(p0=e), parent=dialog)
        ttk.Button(buttons, text=UI_TEXT['f16'], command=lambda: save_json(None, 'JSONs')).pack(side='left', expand=True, fill='x', padx=(0, 6))
        def choose_path():
            path = filedialog.asksaveasfilename(parent=dialog, title=UI_TEXT['g16'], initialfile=name_var.get().strip() + '.json', defaultextension='.json', filetypes=[(UI_TEXT['y15'], '*.json'), (UI_TEXT['z7'], '*.*')])
            if path:
                save_json(path, 'chosen location')
        ttk.Button(buttons, text=UI_TEXT['h16'], command=choose_path).pack(side='left', expand=True, fill='x')

    def _load_fflag_reference_panel(self, force=False):
        if getattr(self, '_fflag_reference_load_started', False) and (not force):
            return
        self._fflag_reference_load_started = True
        if force:
            self._fflag_reference_cache = None
        elif not getattr(self, '_fflag_reference_cache', None):
            try:
                with open(FFLAG_REFERENCE_CACHE_PATH, 'r', encoding='utf-8') as source:
                    saved = json.load(source)
                age = time.time() - float(saved.get('time', 0))
                if age <= 21600 and len(saved.get('offsets', {})) >= 500 and isinstance(saved.get('rows'), list):
                    self._fflag_reference_cache = saved
                    self._fflag_reference_rows = list(saved['rows'])
                    self._fflag_reference_loaded(saved)
                    if age <= 900:
                        return
            except Exception:
                pass
        if hasattr(self, 'fflag_reference_status'):
            try:
                self.fflag_reference_status.configure(text=UI_TEXT['p14'])
            except Exception:
                pass
        def worker():
            try:
                result = self._fetch_fflag_reference_data(force=force)
            except Exception as exc:
                result = {'rows': [], 'offsets_error': str(exc), 'defaults_error': ''}
            try:
                self.after(0, lambda r=result: self._fflag_reference_loaded(r))
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True, name='RoUtils-FFlagReference').start()

    def _fflag_reference_loaded(self, result):
        if isinstance(result, dict) and result.get('offsets'):
            self._fflag_reference_cache = result
        if not hasattr(self, 'fflag_reference_tree'):
            return
        rows = result.get('rows', [])
        self._fflag_reference_rows = list(rows)
        if rows:
            status = f'{len(rows):,} flags'
            if result.get('defaults_error'):
                status += ' · defaults unavailable (* = missing)'
            if result.get('offsets_error'):
                status += ' · fallback offsets'
            self.fflag_reference_status.configure(text=status)
            self._refresh_fflag_reference_panel()
        else:
            errors = '; '.join((value for value in (result.get('offsets_error'), result.get('defaults_error')) if value))
            self.fflag_reference_status.configure(text=UI_TEXT['y14'])
            if errors:
                self._console_log(UI_TEXT['z14'].format(p0=errors))

    def _refresh_fflag_reference_panel(self):
        tree = getattr(self, 'fflag_reference_tree', None)
        if tree is None:
            return
        try:
            if not tree.winfo_exists():
                return
        except Exception:
            return
        self._fflag_reference_render_token = getattr(self, '_fflag_reference_render_token', 0) + 1
        token = self._fflag_reference_render_token
        old_job = getattr(self, '_fflag_reference_render_job', None)
        if old_job:
            try:
                tree.after_cancel(old_job)
            except Exception:
                pass
        try:
            tree.delete(*tree.get_children())
        except Exception:
            pass
        needle = self.fflag_reference_search.get().strip().casefold()
        rows = [row for row in getattr(self, '_fflag_reference_rows', []) if not needle or any((needle in str(value).casefold() for value in row))]
        self.fflag_reference_status.configure(text=UI_TEXT['a15'].format(p0=len(rows)))
        def insert_batch(start=0):
            if token != getattr(self, '_fflag_reference_render_token', None):
                return
            if getattr(self, '_resize_active', False):
                try:
                    self._fflag_reference_render_job = tree.after(80, insert_batch, start)
                except Exception:
                    self._fflag_reference_render_job = None
                return
            try:
                if not tree.winfo_exists():
                    return
            except Exception:
                return
            processed = 0
            started = time.perf_counter()
            pos = start
            while pos < len(rows) and processed < 240 and (time.perf_counter() - started < 0.007):
                try:
                    tree.insert('', 'end', iid=f'ref_{token}_{pos}', text='+', values=rows[pos])
                except Exception:
                    pass
                pos += 1
                processed += 1
            if pos < len(rows):
                self._fflag_reference_render_job = tree.after(1, insert_batch, pos)
            else:
                self._fflag_reference_render_job = None
        insert_batch(0)

    def _show_fflag_reference_panel(self):
        if not hasattr(self, 'nb'):
            return
        for tab_id in self.nb.tabs():
            try:
                if self.nb.tab(tab_id, 'text') == UI_TEXT['h5']:
                    self.nb.select(tab_id)
                    self._lazy_tab_changed()
                    def select_reference():
                        try:
                            fflag_tab = next((item for item in self.nb.tabs() if self.nb.tab(item, 'text') == UI_TEXT['h5']), None)
                            if fflag_tab is not None:
                                self.nb.select(fflag_tab)
                            if hasattr(self, 'fflag_side_notebook') and self.fflag_side_notebook.winfo_exists():
                                self.fflag_side_notebook.select(self.fflag_reference_tab)
                        except Exception:
                            pass
                    self.after_idle(select_reference)
                    return
            except Exception:
                continue

    def _fetch_fflag_reference_data(self, force=False):
        cached = getattr(self, '_fflag_reference_cache', None)
        if not force and cached and (time.time() - cached.get('time', 0) < 900) and (len(cached.get('offsets', {})) >= 500):
            return cached
        if not force:
            try:
                with open(FFLAG_REFERENCE_CACHE_PATH, 'r', encoding='utf-8') as source:
                    disk_cache = json.load(source)
                age = time.time() - float(disk_cache.get('time', 0))
                if age <= 900 and len(disk_cache.get('offsets', {})) >= 500 and isinstance(disk_cache.get('rows'), list):
                    disk_cache['time'] = time.time()
                    self._fflag_reference_cache = disk_cache
                    return disk_cache
            except Exception:
                pass
        def fetch(url):
            with _routils_request(url, timeout=10, headers={'Accept': 'application/json,text/plain,*/*'}, cache_bypass=force) as response:
                return response.read().decode('utf-8', 'replace')
        def extract_block(text, namespace_name):
            match = re.search('\\bnamespace\\s+' + re.escape(namespace_name) + '\\s*\\{', text)
            if not match:
                return None
            open_brace = text.find('{', match.start())
            depth = 0
            for index in range(open_brace, len(text)):
                char = text[index]
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        return text[open_brace + 1:index]
            return text[open_brace + 1:]
        def parse_offsets(text):
            text = html.unescape(str(text or ''))
            text = re.sub('/\\*.*?\\*/', '', text, flags=re.S)
            text = re.sub('//[^\\n]*', '', text)
            block = extract_block(text, UI_TEXT['h5'])
            if block is None:
                block = extract_block(text, 'FFlagOffsets')
                if block is not None:
                    block = re.sub('namespace\\s+FFlagList\\s*\\{.*?\\}', '', block, flags=re.S)
            if block is None:
                block = text
            offsets = {}
            declaration = re.compile('\\b(?:inline\\s+)?(?:static\\s+)?(?:constexpr\\s+)?(?:const\\s+)?(?:std::)?uintptr_t\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*=\\s*(0x[0-9a-fA-F]+|\\d+)\\s*;')
            for match in declaration.finditer(block):
                name, value = match.groups()
                if name in {'Pointer', 'ToFlag', 'ToValue'}:
                    continue
                offsets[name] = value.lower() if value.lower().startswith('0x') else f'0x{int(value):x}'
            if len(offsets) < 500:
                alternate_patterns = (re.compile('\\b([A-Za-z_][A-Za-z0-9_]*)\\s*(?:=|:)\\s*(0x[0-9a-fA-F]{4,})\\b'), re.compile('(0x[0-9a-fA-F]{4,})\\s+(?:(?:offset|Offset)\\s+)?\\b([A-Za-z_][A-Za-z0-9_]*)\\b'))
                for pattern_index, pattern in enumerate(alternate_patterns):
                    for match in pattern.finditer(block):
                        if pattern_index == 0:
                            name, value = (match.group(1), match.group(2))
                        else:
                            value, name = (match.group(1), match.group(2))
                        if name not in {'Pointer', 'ToFlag', 'ToValue', 'FFlagList'}:
                            offsets.setdefault(name, value.lower())
            return offsets
        defaults = {}
        defaults_error = ''
        default_names = {}
        offsets = {}
        offsets_error = ''
        source_errors = []
        primary_url = _get_latest_offsets_webview_url()
        mirror_url = 'https://raw.githubusercontent.com/4anti/Roblox-Fastflag-Manager/main/data/FFlags.hpp'
        pool = ThreadPoolExecutor(max_workers=3, thread_name_prefix='RoUtils-FFlagFetch')
        future_roles = {pool.submit(fetch, WEBVIEW2_URL_DEFAULTS): ('defaults', WEBVIEW2_URL_DEFAULTS), pool.submit(fetch, primary_url): ('primary', primary_url), pool.submit(fetch, mirror_url): ('mirror', mirror_url)}
        pending = set(future_roles)
        candidates = {}
        defaults_done = False
        deadline = time.monotonic() + 11.0
        def process_future(future):
            nonlocal defaults, default_names, defaults_error, defaults_done
            role, url = future_roles[future]
            try:
                content = future.result()
            except Exception as exc:
                if role == 'defaults':
                    defaults_error = str(exc)
                    defaults_done = True
                else:
                    source_errors.append(f'{url}: {exc}')
                return
            if role == 'defaults':
                try:
                    raw_defaults = json.loads(content)
                    if isinstance(raw_defaults, dict):
                        default_items = raw_defaults.items()
                    elif isinstance(raw_defaults, list):
                        default_items = ((item.get('name'), item.get('value', '*')) for item in raw_defaults if isinstance(item, dict) and item.get('name') is not None)
                    else:
                        default_items = ()
                    for name, value in default_items:
                        full_name = str(name or '').strip()
                        if not full_name:
                            continue
                        bare_name = fflag_strip_prefix(full_name).strip()
                        key = bare_name.casefold()
                        normalized_value = str(value).lower() if isinstance(value, bool) else '*' if value is None else str(value)
                        if key and key not in defaults:
                            defaults[key] = normalized_value
                            default_names[key] = full_name
                except Exception as exc:
                    defaults_error = str(exc)
                defaults_done = True
                return
            try:
                candidate_offsets = parse_offsets(content)
            except Exception as exc:
                source_errors.append(f'{url}: {exc}')
                return
            if len(candidate_offsets) >= 500:
                candidates[role] = candidate_offsets
            else:
                source_errors.append(f'{url}: parsed only {len(candidate_offsets)} offsets')
        try:
            while pending and time.monotonic() < deadline:
                finished, pending = wait(pending, timeout=min(0.2, max(0.0, deadline - time.monotonic())), return_when=FIRST_COMPLETED)
                if not finished:
                    continue
                for future in finished:
                    process_future(future)
                if 'primary' in candidates:
                    offsets = candidates['primary']
                    break
                if 'mirror' in candidates:
                    if any((role == 'primary' and future in pending for future, (role, _) in future_roles.items())):
                        ready, _ = wait([future for future, (role, _) in future_roles.items() if role == 'primary' and future in pending], timeout=0.25)
                        for future in ready:
                            pending.discard(future)
                            process_future(future)
                    if 'primary' in candidates:
                        offsets = candidates['primary']
                    else:
                        offsets = candidates['mirror']
                        offsets_error = 'Theo source did not contain a full offset list; loaded the mirror instead.'
                    break
            if not defaults_done:
                default_future = next((future for future, (role, _) in future_roles.items() if role == 'defaults'), None)
                if default_future is not None and default_future in pending:
                    ready, _ = wait([default_future], timeout=0.35)
                    if ready:
                        pending.discard(default_future)
                        process_future(default_future)
                if not defaults_done and (not defaults_error):
                    defaults_error = 'FFlag defaults request timed out.'
            if not offsets:
                offsets_error = '; '.join(source_errors) or UI_TEXT['c30']
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
        rows = []
        for bare_name, offset in offsets.items():
            key = str(bare_name).casefold()
            if key in defaults:
                display_name = default_names.get(key, bare_name)
                value = defaults[key]
            else:
                display_name = bare_name
                value = '*'
            rows.append((display_name, offset, value))
        rows.sort(key=lambda row: row[0].casefold())
        result = {'time': time.time(), 'defaults': defaults, 'default_names': default_names, 'offsets': offsets, 'rows': rows, 'defaults_error': defaults_error, 'offsets_error': offsets_error}
        if len(offsets) >= 500:
            self._fflag_reference_cache = result
            try:
                temporary = FFLAG_REFERENCE_CACHE_PATH + '.tmp'
                with open(temporary, 'w', encoding='utf-8') as output:
                    json.dump(result, output, ensure_ascii=False, separators=(',', ':'))
                os.replace(temporary, FFLAG_REFERENCE_CACHE_PATH)
            except Exception:
                pass
        return result

    def _copy_fflag_reference_row(self, tree, event=None):
        try:
            row = tree.identify_row(event.y) if event is not None else None
            column = tree.identify_column(event.x) if event is not None else None
            if event is not None and not row:
                return
            selection = [row] if row else tree.selection()
            if not selection:
                return
            values = tree.item(selection[0], 'values')
            value_column = '#2' if len(values) == 2 else '#3'
            if column == value_column:
                text = str(values[int(column[1:]) - 1])
            elif column and column.startswith('#') and int(column[1:]) <= len(values):
                text = ' - '.join(map(str, values))
            elif len(values) >= 3:
                text = f'{values[0]} - {values[1]} - {values[2]}'
            else:
                text = ' - '.join(map(str, values))
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update_idletasks()
            messagebox.showinfo(UI_TEXT['h5'], UI_TEXT['v15'], parent=self)
        except Exception as exc:
            self._console_log(UI_TEXT['w15'].format(p0=exc))

    def _fflag_history_load(self):
        try:
            with open(FFLAG_HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                return [x for x in data if isinstance(x, dict)][-500:]
        except Exception:
            pass
        return []

    def _fflag_history_save(self):
        try:
            os.makedirs(os.path.dirname(FFLAG_HISTORY_PATH), exist_ok=True)
            temporary = FFLAG_HISTORY_PATH + '.tmp'
            with open(temporary, 'w', encoding='utf-8') as f:
                json.dump(self._fflag_history_items[-500:], f, ensure_ascii=False, indent=2)
            os.replace(temporary, FFLAG_HISTORY_PATH)
        except Exception as exc:
            try:
                self._console_log(f'FFlag history save failed: {exc}')
            except Exception:
                pass

    def _fflag_history_snapshot_from_flags(self, flags):
        snapshot = []
        for index, flag in enumerate(flags or []):
            if not isinstance(flag, dict):
                continue
            snapshot.append({'name': fflag_strip_prefix(str(flag.get('name', '') or '').strip()), 'value': str(flag.get('value', '') or ''), 'type': str(flag.get('type', '') or ''), 'index': index})
        return snapshot

    def _fflag_history_commit(self, entries):
        if not entries:
            return
        lock = getattr(self, '_fflag_history_lock', None)
        if lock is None:
            self._fflag_history_lock = threading.RLock()
            lock = self._fflag_history_lock
        with lock:
            items = getattr(self, '_fflag_history_items', None)
            if not isinstance(items, list):
                items = self._fflag_history_items = []
            items.extend(entries)
            del items[:-500]
            self._fflag_history_save()
        if hasattr(self, 'fflag_history_text'):
            self._schedule_ui('fflag_history_render', 45, self._fflag_history_refresh)

    def _fflag_history_record(self, event, old=None, new=None):
        self._fflag_history_commit([{'timestamp': time.time(), 'event': str(event), 'old': dict(old) if isinstance(old, dict) else None, 'new': dict(new) if isinstance(new, dict) else None}])

    def _fflag_history_track_changes(self):
        current = self._fflag_history_snapshot_from_flags(self.fflag_flags)
        previous = getattr(self, '_fflag_history_snapshot', None)
        if not getattr(self, '_fflag_history_snapshot_ready', False) or not isinstance(previous, list):
            self._fflag_history_snapshot = current
            self._fflag_history_snapshot_ready = True
            return
        changes = []
        def keyed(items):
            counts = {}
            result = {}
            for item in items:
                name_key = str(item.get('name', '')).casefold()
                occurrence = counts.get(name_key, 0)
                counts[name_key] = occurrence + 1
                result[name_key, occurrence] = item
            return result
        old_by_name = keyed(previous)
        new_by_name = keyed(current)
        old_only = [x for key, x in old_by_name.items() if key not in new_by_name]
        new_only = [x for key, x in new_by_name.items() if key not in old_by_name]
        paired_old = set()
        paired_new = set()
        if len(previous) == len(current) and len(old_only) == len(new_only):
            new_by_index = {x['index']: x for x in new_only}
            for old in old_only:
                candidate = new_by_index.get(old['index'])
                if candidate is not None:
                    changes.append({'timestamp': time.time(), 'event': 'changed', 'old': dict(old), 'new': dict(candidate)})
                    paired_old.add(id(old))
                    paired_new.add(id(candidate))
        for key in old_by_name.keys() & new_by_name.keys():
            old = old_by_name[key]
            new = new_by_name[key]
            if old.get('name') != new.get('name') or old.get('value') != new.get('value') or old.get('type') != new.get('type'):
                changes.append({'timestamp': time.time(), 'event': 'changed', 'old': dict(old), 'new': dict(new)})
        for item in new_only:
            if id(item) not in paired_new:
                changes.append({'timestamp': time.time(), 'event': 'added', 'old': None, 'new': dict(item)})
        for item in old_only:
            if id(item) not in paired_old:
                changes.append({'timestamp': time.time(), 'event': 'removed', 'old': dict(item), 'new': None})
        self._fflag_history_snapshot = current
        self._fflag_history_snapshot_ready = True
        self._fflag_history_commit(changes)

    def _fflag_history_refresh(self):
        text = getattr(self, 'fflag_history_text', None)
        if text is None:
            return
        try:
            if not text.winfo_exists():
                return
        except Exception:
            return
        query = str(self.fflag_history_search.get() if hasattr(self, 'fflag_history_search') else '').strip().casefold()
        with getattr(self, '_fflag_history_lock', threading.RLock()):
            entries = list(reversed(getattr(self, '_fflag_history_items', [])))
        if query:
            def matches(item):
                old = item.get('old') or {}
                new = item.get('new') or {}
                combined = ' '.join((str(value) for value in (item.get('event', ''), old.get('name', ''), old.get('value', ''), new.get('name', ''), new.get('value', ''), old.get('type', ''), new.get('type', '')))).casefold()
                return query in combined
            entries = [item for item in entries if matches(item)]
        text.configure(state='normal')
        text.delete('1.0', 'end')
        if not entries:
            text.insert('end', 'No FFlag changes recorded yet.\n' if not query else 'No history entries match this filter.\n', 'history_meta')
        for entry in entries[:300]:
            try:
                stamp = datetime.fromtimestamp(float(entry.get('timestamp', 0))).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                stamp = 'Unknown time'
            event = str(entry.get('event', 'changed')).lower()
            old = entry.get('old') or {}
            new = entry.get('new') or {}
            if event == 'added':
                title, tag = ('NEW FFLAG', 'history_add')
            elif event == 'removed':
                title, tag = ('FFLAG REMOVED', 'history_removed')
            else:
                title, tag = ('FFLAG CHANGED', 'history_title')
            text.insert('end', f'{stamp}  ', 'history_meta')
            text.insert('end', title + '\n', tag)
            if old.get('name') != new.get('name') and old.get('name') is not None and (new.get('name') is not None):
                text.insert('end', 'Name: ', 'history_meta')
                text.insert('end', str(old.get('name', '')), 'history_old')
                text.insert('end', '  →  ', 'history_meta')
                text.insert('end', str(new.get('name', '')), 'history_new')
                text.insert('end', '\n')
            elif new.get('name') is not None:
                text.insert('end', 'Name: ', 'history_meta')
                text.insert('end', str(new.get('name', '')), tag if event == 'added' else 'history_meta')
                text.insert('end', '\n')
            elif old.get('name') is not None:
                text.insert('end', 'Name: ', 'history_meta')
                text.insert('end', str(old.get('name', '')), 'history_old')
                text.insert('end', '\n')
            if old.get('value') != new.get('value') and old.get('value') is not None and (new.get('value') is not None):
                text.insert('end', 'Value: ', 'history_meta')
                text.insert('end', str(old.get('value', '')), 'history_old')
                text.insert('end', '  →  ', 'history_meta')
                text.insert('end', str(new.get('value', '')), 'history_new')
                text.insert('end', '\n')
            elif new.get('value') is not None:
                text.insert('end', 'Value: ', 'history_meta')
                text.insert('end', str(new.get('value', '')), tag if event == 'added' else 'history_meta')
                text.insert('end', '\n')
            elif old.get('value') is not None:
                text.insert('end', 'Value: ', 'history_meta')
                text.insert('end', str(old.get('value', '')), 'history_old')
                text.insert('end', '\n')
            if old.get('type') != new.get('type') and old.get('type') is not None and (new.get('type') is not None):
                text.insert('end', 'Type: ', 'history_meta')
                text.insert('end', str(old.get('type', '')), 'history_old')
                text.insert('end', '  →  ', 'history_meta')
                text.insert('end', str(new.get('type', '')), 'history_new')
                text.insert('end', '\n')
            text.insert('end', '────────────────────────────────────────────────────────\n', 'history_separator')
        text.configure(state='disabled')
        text.yview_moveto(0)

    def _fflag_history_clear(self):
        if not messagebox.askyesno('FFlag History', 'Clear all saved FFlag change history?', parent=self):
            return
        with getattr(self, '_fflag_history_lock', threading.RLock()):
            self._fflag_history_items = []
            self._fflag_history_save()
        self._fflag_history_refresh()

    def _open_fflag_history_panel(self):
        fflag_tab_id = next((tab_id for tab_id in self.nb.tabs() if self.nb.tab(tab_id, 'text') == UI_TEXT['h5']), None)
        if fflag_tab_id is not None:
            self.nb.select(fflag_tab_id)
            self._lazy_tab_changed()
        def select_history():
            try:
                if hasattr(self, 'fflag_side_notebook') and self.fflag_side_notebook.winfo_exists() and hasattr(self, 'fflag_history_tab'):
                    self.fflag_side_notebook.select(self.fflag_history_tab)
                    self._fflag_history_refresh()
            except Exception:
                pass
        self.after_idle(select_history)


    def _fflag_hotkey_editor(self, index, parent, refresh):
        dlg = tk.Toplevel(parent)
        dlg.title(UI_TEXT['q27'])
        dlg.transient(parent)
        dlg.grab_set()
        theme_toplevel(dlg)
        existing = self.fflag_hotkeys[index] if index is not None else {}
        key_var = tk.StringVar(value=str(existing.get('key', '')))
        flag_var = tk.StringVar(value=str(existing.get('flag', '')))
        mode_var = tk.StringVar(value=str(existing.get('mode', _FFLAG_DEFAULT_MODE)))
        v1_var = tk.StringVar(value=str(existing.get('value1', _FFLAG_DEFAULT_TRUE)))
        v2_var = tk.StringVar(value=str(existing.get('value2', _FFLAG_DEFAULT_FALSE)))
        ttk.Label(dlg, text=UI_TEXT['s6']).grid(row=0, column=0, padx=10, pady=(12, 4), sticky='w')
        key_entry = ttk.Entry(dlg, textvariable=key_var, width=20)
        key_entry.grid(row=1, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text=UI_TEXT['t6']).grid(row=2, column=0, padx=10, pady=(8, 4), sticky='w')
        flag_combo = ttk.Combobox(dlg, textvariable=flag_var, values=[x.get('name', '') for x in self.fflag_flags], width=48)
        flag_combo.grid(row=3, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text=UI_TEXT['u6']).grid(row=4, column=0, padx=10, pady=(8, 4), sticky='w')
        mode_combo = ttk.Combobox(dlg, textvariable=mode_var, values=[_FFLAG_DEFAULT_MODE], state='readonly', width=20)
        mode_combo.grid(row=5, column=0, padx=10, sticky='w')
        ttk.Label(dlg, text=UI_TEXT['v6']).grid(row=6, column=0, padx=10, pady=(8, 4), sticky='w')
        ttk.Entry(dlg, textvariable=v1_var, width=30).grid(row=7, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text=UI_TEXT['w6']).grid(row=8, column=0, padx=10, pady=(8, 4), sticky='w')
        ttk.Entry(dlg, textvariable=v2_var, width=30).grid(row=9, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text=UI_TEXT['x6'], foreground=_FFLAG_COLOR_MUTED).grid(row=10, column=0, padx=10, pady=(8, 4), sticky='w')
        def capture_key(event):
            if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
                return 'break'
            key = event.keysym.upper()
            if key == 'ESCAPE':
                key = 'ESC'
            key_var.set(key)
            return 'break'
        key_entry.bind('<KeyPress>', capture_key)
        def save():
            key = key_var.get().strip().upper()
            flag = fflag_strip_prefix(flag_var.get().strip())
            if not key or not fflag_key_to_vk(key):
                messagebox.showerror(UI_TEXT['y6'], UI_TEXT['z6'], parent=dlg)
                return
            if not flag:
                messagebox.showerror(UI_TEXT['y6'], UI_TEXT['a7'], parent=dlg)
                return
            item = {'key': key, 'flag': flag, 'mode': _FFLAG_DEFAULT_MODE, 'value1': v1_var.get(), 'value2': v2_var.get(), 'state': bool(existing.get('state', False))}
            if index is None:
                self.fflag_hotkeys.append(item)
            else:
                self.fflag_hotkeys[index] = item
            self._save_settings()
            refresh()
            dlg.destroy()
        btns = ttk.Frame(dlg)
        btns.grid(row=11, column=0, pady=12)
        ttk.Button(btns, text=UI_TEXT['i6'], command=save).pack(side='left', padx=4)
        ttk.Button(btns, text=UI_TEXT['b3'], command=dlg.destroy).pack(side='left', padx=4)
        dlg.columnconfigure(0, weight=1)
        for button_number in range(1, 6):
            key_entry.bind(f'<Button-{button_number}>', lambda event, n=button_number: (key_var.set(f'MOUSE{n}'), 'break')[1])
        key_entry.focus_set()

    def _fflag_refresh_process(self):
        pid = _fflag_find_pid()
        if sys.platform.startswith('linux'):
            if pid:
                if pid != self.fflag_pid:
                    self.fflag_original_values.clear()
                    self.fflag_pid = pid
                    try:
                        self.fflag_engine.close()
                    except Exception:
                        pass
                    self._console_log(f'Sober detected: PID {pid}; using Sober config mode.')
                    if self.fflag_auto_apply.get():
                        self.after(0, lambda: self._fflag_apply(silent=True))
                self.fflag_status.config(text=f'Sober detected (PID {pid}) · config mode', foreground=_FFLAG_COLOR_SUCCESS)
                if hasattr(self, 'fps_pid_label'):
                    self.fps_pid_label.config(text=f'Sober PID: {pid}', foreground=_FFLAG_COLOR_SUCCESS)
            else:
                had_pid = self.fflag_pid
                self.fflag_pid = 0
                self.fflag_original_values.clear()
                try:
                    self.fflag_engine.close()
                except Exception:
                    pass
                self.fflag_status.config(text='Sober not detected', foreground=_FFLAG_COLOR_MUTED)
                if had_pid:
                    self._console_log('Sober process closed; config-based FFlag mode remains available.')
                if hasattr(self, 'fps_pid_label'):
                    self.fps_pid_label.config(text='Sober not detected', foreground=_FFLAG_COLOR_MUTED)
            self.after(1000, self._fflag_refresh_process)
            return
        if pid and pid != self.fflag_pid:
            self.fflag_original_values.clear()
            self.fflag_pid = pid
            exe_path = _get_process_exe_path(pid)
            if exe_path and os.path.basename(exe_path).lower() == 'robloxplayerbeta.exe':
                self.settings['roblox_path'] = exe_path
                self._save_settings()
                if hasattr(self, 'roblox_path_var'):
                    self.roblox_path_var.set(exe_path)
            if self.fflag_engine.attach(pid):
                self.fflag_status.config(text=UI_TEXT['j14'].format(p0=pid), foreground=_FFLAG_COLOR_SUCCESS)
                self._console_log(UI_TEXT['i16'].format(p0=pid))
                if hasattr(self, 'fps_pid_label'):
                    self.fps_pid_label.config(text=UI_TEXT['j16'].format(p0=pid), foreground=_FFLAG_COLOR_SUCCESS)
                if self.fflag_auto_apply.get():
                    self.after(0, lambda: self._fflag_apply(silent=True))
            else:
                self.fflag_status.config(text=UI_TEXT['k16'], foreground=_FFLAG_COLOR_ERROR)
                self._console_log(UI_TEXT['l16'].format(p0=pid))
        elif not pid:
            had_pid = self.fflag_pid
            if had_pid:
                self.fflag_engine.close()
            self.fflag_original_values.clear()
            self.fflag_pid = 0
            self.fflag_status.config(text=UI_TEXT['q13'], foreground=_FFLAG_COLOR_MUTED)
            if had_pid:
                self._console_log(UI_TEXT['m16'])
            if hasattr(self, 'fps_pid_label'):
                self.fps_pid_label.config(text=UI_TEXT['r12'], foreground=_FFLAG_COLOR_MUTED)
        self.after(1000, self._fflag_refresh_process)

    def _fps_flag_value(self):
        fps = max(0, min(240, int(self.fps_limit.get())))
        return str(fps)

    def _sync_fps_flag_to_manager(self):
        full_name = 'TaskSchedulerTargetFps'
        normalized_name = fflag_strip_prefix(full_name)
        value = self._fps_flag_value()
        original_signature = [(str(flag.get('name', '')), str(flag.get('value', '')), str(flag.get('type', ''))) for flag in self.fflag_flags if isinstance(flag, dict)]
        fps_entry = None
        cleaned_flags = []
        for flag in self.fflag_flags:
            if not isinstance(flag, dict):
                continue
            flag_name = str(flag.get('name', '')).strip()
            if fflag_strip_prefix(flag_name) == normalized_name:
                if fps_entry is None:
                    flag['name'] = full_name
                    flag['value'] = value
                    flag['type'] = 'int'
                    fps_entry = flag
                    cleaned_flags.append(flag)
                continue
            cleaned_flags.append(flag)
        if fps_entry is None:
            fps_entry = {'name': full_name, 'value': value, 'type': 'int'}
            cleaned_flags.append(fps_entry)
        new_signature = [(str(flag.get('name', '')), str(flag.get('value', '')), str(flag.get('type', ''))) for flag in cleaned_flags]
        if original_signature != new_signature:
            self.fflag_flags = cleaned_flags
            self._save_fflag_flags()
            if hasattr(self, 'fflag_tree'):
                self._refresh_fflag_list()

    def _apply_fps_flag(self, silent=True):
        if sys.platform.startswith('linux'):
            try:
                path, value = set_sober_fps_cap(self.fps_limit.get())
                self._fflag_status_text(f'Sober FPS cap set to {value}', _FFLAG_COLOR_SUCCESS)
                self._console_log(f'Sober FPS cap set to {value} in {path}')
                if not silent:
                    messagebox.showinfo(UI_TEXT['h5'], f'Sober FPS cap set to {value}. Restart Sober to apply it.', parent=self)
                return True
            except Exception as error:
                self._console_log(f'Sober FPS cap update failed: {error}')
                if not silent:
                    messagebox.showwarning(UI_TEXT['h5'], str(error), parent=self)
                return False
        self._sync_fps_flag_to_manager()
        if not self.fflag_pid or not self.fflag_engine.handle:
            return False
        value = self._fps_flag_value()
        return bool(self._fflag_write_offset('DFIntTaskSchedulerTargetFps', value, 'int'))

    def _apply_fps_after_slider(self):
        self._fps_release_job = None
        try:
            if sys.platform.startswith('linux'):
                self._apply_fps_flag(silent=True)
            else:
                self._sync_fps_flag_to_manager()
                self._fflag_apply(silent=True)
            self._save_settings()
        except Exception:
            pass

    def _fflag_write_offset(self, name, value, value_type):
        cache = getattr(self, '_fflag_reference_cache', None)
        if not cache or not isinstance(cache.get('offsets'), dict):
            return False
        offsets = cache['offsets']
        candidates = [str(name).strip()]
        bare_name = fflag_strip_prefix(str(name).strip())
        if bare_name and bare_name not in candidates:
            candidates.append(bare_name)
        for prefix in FFLAG_PREFIXES:
            candidate = prefix + bare_name
            if candidate not in candidates:
                candidates.append(candidate)
        offset_value = None
        lookup_cache = getattr(self, '_fflag_offset_lookup_cache', None)
        if not isinstance(lookup_cache, tuple) or len(lookup_cache) != 2 or lookup_cache[0] is not offsets:
            folded_offsets = {str(key).casefold(): value for key, value in offsets.items()}
            self._fflag_offset_lookup_cache = (offsets, folded_offsets)
        else:
            folded_offsets = lookup_cache[1]
        for candidate in candidates:
            offset_value = offsets.get(candidate)
            if offset_value is None:
                offset_value = folded_offsets.get(candidate.casefold())
            if offset_value is not None:
                break
        if offset_value is None:
            return False
        try:
            address = int(str(offset_value), 16) + int(self.fflag_engine.module_base)
            value_text = str(value).strip()
            kind = str(value_type or fflag_infer_type(value_text)).lower()
            if kind == 'bool':
                data = bytes([1 if value_text.lower() in (_FFLAG_DEFAULT_TRUE, '1') else 0])
            elif kind == 'int':
                data = int(value_text, 10).to_bytes(4, 'little', signed=True)
            elif kind == 'float':
                data = __import__('struct').pack('<d', float(value_text))
            else:
                data = value_text.encode('utf-8') + b'\x00'
            original = self.fflag_engine._read(address, len(data))
            if original is None:
                return False
            if address not in self.fflag_original_values:
                self.fflag_original_values[address] = original
            written = ctypes.c_size_t()
            ok = ctypes.windll.kernel32.WriteProcessMemory(self.fflag_engine.handle, ctypes.c_void_p(address), data, len(data), ctypes.byref(written))
            return bool(ok and written.value == len(data))
        except Exception:
            return False

    def _fflag_apply(self, silent=False):
        conflicts = self._fflag_conflicts()
        if conflicts:
            names = [fflag_strip_prefix(str(f.get('name', ''))) for f in self.fflag_flags if fflag_strip_prefix(str(f.get('name', ''))).lower() in conflicts]
            unique_names = []
            seen = set()
            for name in names:
                key = name.lower()
                if key not in seen:
                    seen.add(key)
                    unique_names.append(name)
            self._console_log(UI_TEXT['n16'] + ', '.join(unique_names))
            if not silent:
                messagebox.showerror(UI_TEXT['h5'], UI_TEXT['o16'], parent=self)
            return
        if not self._fflag_confirm_large_values(self.fflag_flags):
            self._fflag_status_text('FFlag apply cancelled because a value is too large', _FFLAG_COLOR_WARNING)
            return
        if sys.platform.startswith('linux'):
            try:
                if not self._save_fflag_flags():
                    return
                result = apply_sober_fflags(self.fflag_flags, DATA_DIR)
                applied = int(result.get('applied', 0))
                total = int(result.get('total', 0))
                skipped = result.get('skipped', [])
                from sober_proxy.service import SoberProxyService
                live = SoberProxyService(DATA_DIR).is_running()
                status = 'Applied (Restart Needed)'
                ok = applied == total and not skipped
                self._fflag_status_text(status if ok else f'{status} · {len(skipped)} skipped', _FFLAG_COLOR_SUCCESS if ok else _FFLAG_COLOR_ERROR)
                self._console_log(f'Sober FFlags written to {result.get("path", sober_config_path())}: {applied}/{total}')
                if live:
                    self._console_log('Custom FFlags are available to the live proxy on the next ClientSettings refresh.')
                if skipped:
                    for detail in skipped[:10]:
                        self._console_log(f'Sober FFlag skipped: {detail}')
            except Exception as error:
                self._fflag_status_text('FFlag apply failed', _FFLAG_COLOR_ERROR)
                self._console_log(f'Sober FFlag apply failed: {error}')
            return
        if not self.fflag_pid or not self.fflag_engine.handle:
            self._console_log(UI_TEXT['p16'])
            if not silent:
                messagebox.showwarning(UI_TEXT['h5'], UI_TEXT['q16'], parent=self)
            return
        cache = getattr(self, '_fflag_reference_cache', None)
        if not cache or not isinstance(cache.get('offsets'), dict) or len(cache.get('offsets', {})) < 1:
            self._fflag_status_text('Loading offsets…', _FFLAG_COLOR_MUTED)
            self._load_fflag_reference_panel(force=True)
            self._console_log(UI_TEXT['r16'])
            return
        self._sync_fps_flag_to_manager()
        with self._fflag_apply_state_lock:
            if self._fflag_apply_in_progress:
                self._fflag_apply_pending = True
                self._fflag_apply_pending_silent = self._fflag_apply_pending_silent and bool(silent)
                return
            self._fflag_apply_in_progress = True
        flags = [dict(flag) for flag in self.fflag_flags if isinstance(flag, dict)]
        method = 'Offsets'
        pid = self.fflag_pid
        def worker():
            started = time.perf_counter()
            ok = 0
            failed = 0
            total = len(flags)
            try:
                for flag in flags:
                    name = fflag_strip_prefix(str(flag.get('name', '')))
                    if name:
                        value = str(flag.get('value', ''))
                        value_type = str(flag.get('type') or fflag_infer_type(value))
                        if self._fflag_write_offset(name, value, value_type):
                            ok += 1
                        else:
                            failed += 1
                elapsed = time.perf_counter() - started
                result = {'ok': ok, 'failed': failed, 'total': total, 'elapsed': elapsed, 'method': method, 'pid': pid, 'error': ''}
            except Exception as exc:
                elapsed = time.perf_counter() - started
                result = {'ok': ok, 'failed': failed + 1, 'total': total, 'elapsed': elapsed, 'method': method, 'pid': pid, 'error': str(exc)}
            self.after(0, self._fflag_apply_finished, result, bool(silent))
        threading.Thread(target=worker, daemon=True, name='RoUtils-FFlagApply').start()

    def _fflag_apply_finished(self, result, silent=True):
        elapsed_text = f"{float(result.get('elapsed', 0.0)):.9f}".replace('.', ',')
        ok = int(result.get('ok', 0))
        failed = int(result.get('failed', 0))
        total = int(result.get('total', 0))
        method = str(result.get('method', 'Offsets'))
        pid = result.get('pid', self.fflag_pid)
        if result.get('error'):
            self._console_log(f"FFlag apply worker error: {result['error']}")
        color = _FFLAG_COLOR_SUCCESS if ok and (not failed) else _FFLAG_COLOR_ERROR
        self._fflag_status_text(f'Applied ({elapsed_text} seconds)', color)
        self._console_log(UI_TEXT['t16'].format(p0=method, p1=ok, p2=total, p3=failed, p4=pid))
        if not silent and (not ok or failed):
            messagebox.showwarning(UI_TEXT['h5'], UI_TEXT['u16'].format(p0=method) + (f'\n\nSucceeded: {ok}\nFailed: {failed}' if failed else ''), parent=self)
        with self._fflag_apply_state_lock:
            self._fflag_apply_in_progress = False
            pending = self._fflag_apply_pending
            pending_silent = self._fflag_apply_pending_silent
            self._fflag_apply_pending = False
            self._fflag_apply_pending_silent = True
        if pending:
            self.after(60, lambda s=pending_silent: self._fflag_apply(silent=s))

    def _fflag_status_text(self, text, color=_FFLAG_COLOR_MUTED):
        try:
            self.fflag_status.config(text=text, foreground=color)
        except Exception:
            pass

    def _fflag_unapply(self):
        self.fflag_auto_apply.set(False)
        if sys.platform.startswith('linux'):
            try:
                path = restore_sober_fflags(DATA_DIR)
                self._fflag_status_text('Restored previous Sober FFlags', _FFLAG_COLOR_SUCCESS)
                self._console_log(f'Restored previous Sober FFlags in {path}')
                messagebox.showinfo(UI_TEXT['h5'], f'Previous Sober FFlags were restored in:\n{path}', parent=self)
            except Exception as error:
                self._fflag_status_text('No Sober FFlag backup', _FFLAG_COLOR_MUTED)
                messagebox.showwarning(UI_TEXT['h5'], str(error), parent=self)
            return
        if not self.fflag_pid or not self.fflag_engine.handle:
            self.fflag_original_values.clear()
            messagebox.showwarning(UI_TEXT['h5'], UI_TEXT['q16'], parent=self)
            return
        restored = 0
        failed = 0
        snapshots = list(self.fflag_original_values.items())
        for address, original in snapshots:
            try:
                written = ctypes.c_size_t()
                ok = ctypes.windll.kernel32.WriteProcessMemory(self.fflag_engine.handle, ctypes.c_void_p(address), original, len(original), ctypes.byref(written))
                if ok and written.value == len(original):
                    restored += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        self.fflag_original_values.clear()
        self.fflag_status.config(text=UI_TEXT['v16'].format(p0=restored) + (UI_TEXT['w16'].format(p0=failed) if failed else UI_TEXT['m1']), foreground=_FFLAG_COLOR_SUCCESS if not failed else _FFLAG_COLOR_ERROR)
        self._console_log(UI_TEXT['x16'].format(p0=restored, p1=failed))

    def _toggle_fflag_auto_apply(self):
        enabled = not bool(self.fflag_auto_apply.get())
        self.fflag_auto_apply.set(enabled)
        self.settings['fflag_auto_apply'] = enabled
        self._save_settings()
        if hasattr(self, 'fflag_auto_apply_button'):
            self.fflag_auto_apply_button.config(text=UI_TEXT['u14'] if enabled else UI_TEXT['v14'])
        self._fflag_status_text(UI_TEXT['z28'] if enabled else UI_TEXT['a29'], _FFLAG_COLOR_SUCCESS if enabled else _FFLAG_COLOR_MUTED)
        if enabled and (sys.platform.startswith('linux') or (self.fflag_pid and self.fflag_engine.handle)):
            threading.Thread(target=lambda: self.after(0, lambda: self._fflag_apply(silent=True)), name='RoUtilsFFlagAutoApply', daemon=True).start()

    def _fflag_auto_apply_tick(self):
        try:
            if self.fflag_auto_apply.get() and (sys.platform.startswith('linux') or (self.fflag_pid and self.fflag_engine.handle)):
                self._fflag_apply(silent=True)
        except Exception:
            pass
        try:
            self.after(15000, self._fflag_auto_apply_tick)
        except Exception:
            pass

    def _toggle_anti_afk(self):
        enabled = bool(self.anti_afk_enabled.get())
        self.settings['anti_afk_enabled'] = enabled
        if enabled:
            self._anti_afk_last_action = time.monotonic()
        self._save_settings()
        self._console_log('Anti-AFK enabled; activity signal scheduled every 15 minutes.' if enabled else 'Anti-AFK disabled.')

    def _anti_afk_tick(self):
        try:
            enabled = bool(self.anti_afk_enabled.get())
            now = time.monotonic()
            last_action = float(getattr(self, '_anti_afk_last_action', now))
            if enabled and now - last_action >= 900 and not getattr(self, '_anti_afk_in_progress', False):
                candidates = []
                pid = int(getattr(self, 'fflag_pid', 0) or _fflag_find_pid() or 0)
                if pid > 0:
                    candidates.append(pid)
                if hasattr(self, '_client_roblox_pids'):
                    try:
                        candidates.extend(int(value) for value in self._client_roblox_pids() if int(value) > 0)
                    except Exception:
                        pass
                candidates = tuple(dict.fromkeys(candidates))
                if candidates:
                    self._anti_afk_in_progress = True
                    self._anti_afk_last_action = now
                    threading.Thread(target=self._anti_afk_signal_worker, args=(candidates,), daemon=True, name='RoUtils-AntiAFK').start()
        except Exception:
            pass
        try:
            self.after(15000, self._anti_afk_tick)
        except Exception:
            pass

    def _anti_afk_signal_worker(self, pids):
        success = False
        error = ''
        candidates = pids if isinstance(pids, (tuple, list, set)) else (pids,)
        for pid in candidates:
            try:
                if self._anti_afk_send_virtual_signal(int(pid)):
                    success = True
                    break
            except Exception as exc:
                error = str(exc)
        if not success and not error:
            error = 'No usable Roblox window was found, or Windows did not allow focus switching.'
        try:
            self.after(0, self._anti_afk_signal_finished, success, error)
        except Exception:
            self._anti_afk_in_progress = False

    def _anti_afk_send_virtual_signal(self, pid):
        if os.name != 'nt':
            return False
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        HWND = ctypes.wintypes.HWND
        DWORD = ctypes.wintypes.DWORD
        BOOL = ctypes.wintypes.BOOL
        LPARAM = ctypes.wintypes.LPARAM
        UINT = ctypes.wintypes.UINT
        user32.IsWindowVisible.argtypes = [HWND]
        user32.IsWindowVisible.restype = BOOL
        user32.IsIconic.argtypes = [HWND]
        user32.IsIconic.restype = BOOL
        user32.IsWindow.argtypes = [HWND]
        user32.IsWindow.restype = BOOL
        user32.GetWindow.argtypes = [HWND, UINT]
        user32.GetWindow.restype = HWND
        user32.GetWindowThreadProcessId.argtypes = [HWND, ctypes.POINTER(DWORD)]
        user32.GetWindowThreadProcessId.restype = DWORD
        user32.GetForegroundWindow.argtypes = []
        user32.GetForegroundWindow.restype = HWND
        user32.SetForegroundWindow.argtypes = [HWND]
        user32.SetForegroundWindow.restype = BOOL
        user32.BringWindowToTop.argtypes = [HWND]
        user32.BringWindowToTop.restype = BOOL
        user32.SetActiveWindow.argtypes = [HWND]
        user32.SetActiveWindow.restype = HWND
        user32.AttachThreadInput.argtypes = [DWORD, DWORD, BOOL]
        user32.AttachThreadInput.restype = BOOL
        user32.keybd_event.argtypes = [ctypes.wintypes.BYTE, ctypes.wintypes.BYTE, DWORD, ctypes.c_size_t]
        user32.keybd_event.restype = None
        kernel32.GetCurrentThreadId.argtypes = []
        kernel32.GetCurrentThreadId.restype = DWORD
        callback_type = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
        windows = []
        def enum_window(hwnd, _lparam):
            try:
                if not user32.IsWindowVisible(hwnd) or user32.IsIconic(hwnd):
                    return True
                owner_pid = DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner_pid))
                if int(owner_pid.value) == int(pid) and not user32.GetWindow(hwnd, 4):
                    windows.append(hwnd)
            except Exception:
                pass
            return True
        user32.EnumWindows.argtypes = [callback_type, LPARAM]
        user32.EnumWindows.restype = BOOL
        callback = callback_type(enum_window)
        if not user32.EnumWindows(callback, 0) or not windows:
            return False
        target = windows[0]
        previous = user32.GetForegroundWindow()
        target_thread = user32.GetWindowThreadProcessId(target, None)
        current_thread = kernel32.GetCurrentThreadId()
        attached_pairs = []
        success = False
        try:
            msg = ctypes.wintypes.MSG()
            user32.PeekMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG), HWND, UINT, UINT, UINT]
            user32.PeekMessageW.restype = BOOL
            user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 0)
            if target_thread and target_thread != current_thread:
                if user32.AttachThreadInput(current_thread, target_thread, True):
                    attached_pairs.append((current_thread, target_thread))
            if previous:
                previous_thread = user32.GetWindowThreadProcessId(previous, None)
                if previous_thread and previous_thread not in (current_thread, target_thread):
                    if user32.AttachThreadInput(previous_thread, target_thread, True):
                        attached_pairs.append((previous_thread, target_thread))
            user32.BringWindowToTop(target)
            user32.SetActiveWindow(target)
            if not user32.SetForegroundWindow(target):
                return False
            for _ in range(30):
                if user32.GetForegroundWindow() == target:
                    break
                time.sleep(0.01)
            if user32.GetForegroundWindow() != target:
                return False
            user32.keybd_event(0xA0, 0x2A, 0, 0)
            try:
                time.sleep(0.04)
            finally:
                user32.keybd_event(0xA0, 0x2A, 0x0002, 0)
            time.sleep(0.02)
            success = True
        finally:
            if previous and previous != target and user32.IsWindow(previous):
                try:
                    user32.SetForegroundWindow(previous)
                except Exception:
                    pass
            for first_thread, second_thread in reversed(attached_pairs):
                try:
                    user32.AttachThreadInput(first_thread, second_thread, False)
                except Exception:
                    pass
        return success

    def _anti_afk_signal_finished(self, success, error=''):
        self._anti_afk_in_progress = False
        if success:
            self._console_log('Anti-AFK: sent a virtual activity signal to Roblox.')
        elif error:
            self._console_log('Anti-AFK: ' + str(error))
