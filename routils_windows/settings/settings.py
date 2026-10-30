import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class SettingsMixin:
    def _settings_canvas_resize(self, canvas, window_id, event):
        width = int(getattr(event, 'width', 0) or 0)
        key = f'_canvas_width_{id(canvas)}'
        self._apply_or_defer_canvas_window_width(canvas, window_id, width, key)
    def _build_settings_tab(self):
        try:
            st = ttk.Style(self)
            st.configure('RoUtils.Settings.TFrame', background=_CURRENT_PALETTE['bg_dark'])
            st.configure('RoUtils.Settings.TLabel', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'])
            st.configure('RoUtils.Settings.TLabelframe', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'], bordercolor=_CURRENT_PALETTE['border'])
            st.configure('RoUtils.Settings.TLabelframe.Label', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'])
            st.configure('RoUtils.Settings.TCheckbutton', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'])
            st.map('RoUtils.Settings.TCheckbutton', background=[('active', _CURRENT_PALETTE['bg_dark'])])
        except Exception:
            pass
        tab_root = ttk.Frame(self.nb, padding=0, style='RoUtils.Settings.TFrame')
        self.nb.add(tab_root, text=UI_TEXT['r5'])
        shell = ttk.Frame(tab_root, style='RoUtils.Settings.TFrame')
        shell.pack(fill='both', expand=True)
        canvas = tk.Canvas(shell, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(shell, orient='vertical', command=canvas.yview)
        inner = ttk.Frame(canvas, style='RoUtils.Settings.TFrame')
        window_id = canvas.create_window((0, 0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        inner.bind('<Configure>', lambda _e: self._schedule_ui('settings_region', 30, lambda: canvas.configure(scrollregion=canvas.bbox('all'))))
        canvas.bind('<Configure>', lambda e: self._settings_canvas_resize(canvas, window_id, e))
        def update_scrollbar(_e=None):
            key = f'settings_scrollbar_{id(canvas)}'
            def apply_scrollbar_state():
                if not canvas.winfo_exists() or not inner.winfo_exists():
                    return
                bbox = canvas.bbox('all')
                needed = bool(bbox and bbox[3] > canvas.winfo_height() + 2)
                visible = bool(getattr(canvas, '_scrollbar_visible', False))
                if needed == visible:
                    return
                canvas._scrollbar_visible = needed
                if needed:
                    scrollbar.pack(side='right', fill='y')
                else:
                    scrollbar.pack_forget()
                    canvas.yview_moveto(0)
            self._schedule_ui(key, 90, apply_scrollbar_state)
        inner.bind('<Configure>', update_scrollbar, add='+')
        canvas.bind('<Configure>', update_scrollbar, add='+')
        middle = {'y': None}
        def middle_press(event):
            middle['y'] = event.y
            return 'break'
        def middle_drag(event):
            if middle['y'] is not None:
                canvas.yview_scroll(int((middle['y'] - event.y) / 2), 'units')
                middle['y'] = event.y
            return 'break'
        def middle_release(_event):
            middle['y'] = None
            return 'break'
        middle_tag = f'RoUtilsSettingsMiddle_{id(canvas)}'
        canvas.bind_class(middle_tag, '<Button-2>', middle_press)
        canvas.bind_class(middle_tag, '<B2-Motion>', middle_drag)
        canvas.bind_class(middle_tag, '<ButtonRelease-2>', middle_release)
        def attach_middle_scroll(parent):
            for child in parent.winfo_children():
                try:
                    tags = list(child.bindtags())
                    if middle_tag not in tags:
                        child.bindtags((middle_tag, *tags))
                except Exception:
                    pass
                attach_middle_scroll(child)
        attach_middle_scroll(inner)
        for widget in (canvas, inner):
            widget.bind('<Button-2>', middle_press, add='+')
            widget.bind('<B2-Motion>', middle_drag, add='+')
            widget.bind('<ButtonRelease-2>', middle_release, add='+')
        tab = inner
        ttk.Label(tab, style='RoUtils.Settings.TLabel', text=UI_TEXT['l17'], font=('Segoe UI Semibold', 12)).pack(anchor='w')
        ttk.Label(tab, style='RoUtils.Settings.TLabel', text=UI_TEXT['m17'], foreground='#9aa0a6').pack(anchor='w', pady=(0, 10))
        dpi_box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['n17'])
        dpi_box.pack(fill='x', pady=6)
        try:
            _saved_dpi = int(self.settings.get('dpi_percent', 100) or 100)
        except Exception:
            _saved_dpi = 100
        _saved_dpi = max(50, min(200, _saved_dpi))
        self.dpi_percent = tk.IntVar(value=_saved_dpi)
        dpi_row = ttk.Frame(dpi_box)
        dpi_row.pack(fill='x', padx=8, pady=8)
        ttk.Label(dpi_row, style='RoUtils.Settings.TLabel', text=UI_TEXT['o17']).pack(side='left')
        dpi_combo = ttk.Combobox(dpi_row, textvariable=self.dpi_percent, state='readonly', width=8, values=(50, 60, 70, 75, 80, 90, 100, 110, 125, 150, 175, 200))
        dpi_combo.pack(side='left', padx=(12, 8))
        ttk.Label(dpi_row, style='RoUtils.Settings.TLabel', text=UI_TEXT['p17'], foreground='#9aa0a6').pack(side='left')
        ttk.Label(dpi_box, style='RoUtils.Settings.TLabel', text=UI_TEXT['q17'], foreground='#ffb84d').pack(anchor='w', padx=8, pady=(0, 8))
        dpi_combo.bind('<<ComboboxSelected>>', lambda _e: self._save_dpi_setting_only())
        box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['r17'])
        box.pack(fill='x', pady=6)
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['s17'], variable=self.autostart_watch, command=self._save_settings).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['t17'], variable=self.autoscroll, command=self._save_settings).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['u17'], variable=self.hide_tickets, command=self._apply_filter).pack(anchor='w', padx=8, pady=2)
        ttk.Label(box, text=UI_TEXT['v17'], foreground='#c8c8c8').pack(anchor='w', padx=8, pady=(6, 0))
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['w17'], variable=self.show_lines, command=self._apply_show_lines).pack(anchor='w', padx=8, pady=2)
        self.mesh_preview_vertices = tk.BooleanVar(value=bool(self.settings.get('preview_optimize_vertices', True)))
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['x17'], variable=self.mesh_preview_vertices, command=self._apply_mesh_preview_vertices_setting).pack(anchor='w', padx=8, pady=2)
        startup = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['y17'])
        startup.pack(fill='x', pady=6)
        ttk.Checkbutton(startup, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['z17'], variable=self.launch_on_tray, command=self._startup_setting_changed).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(startup, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['a18'], variable=self.launch_on_startup, command=self._startup_setting_changed).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(startup, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['b18'], variable=self.hide_to_tray_on_close, command=self._startup_setting_changed).pack(anchor='w', padx=8, pady=2)
        discord_box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Discord Rich Presence')
        discord_box.pack(fill='x', pady=6)
        ttk.Checkbutton(discord_box, style='RoUtils.Settings.TCheckbutton', text='Enable Discord Rich Presence', variable=self.discord_rpc_enabled, command=self._toggle_discord_rpc).pack(anchor='w', padx=8, pady=(7, 3))
        application_id_row = ttk.Frame(discord_box, style='RoUtils.Settings.TFrame')
        application_id_row.pack(fill='x', padx=8, pady=(4, 7))
        ttk.Label(application_id_row, style='RoUtils.Settings.TLabel', text='Application ID').pack(side='left')
        application_id_entry = ttk.Entry(application_id_row, textvariable=self.discord_application_id_var, width=26, state='readonly')
        application_id_entry.pack(side='left', fill='x', expand=True, padx=(8, 6))
        application_id_entry.bind('<Button-1>', lambda _event: (self._prompt_change_discord_application_id(), 'break')[1])
        ttk.Button(application_id_row, text='Change ID', command=self._prompt_change_discord_application_id).pack(side='left')
        ttk.Label(discord_box, style='RoUtils.Settings.TLabel', textvariable=self.discord_rpc_status_var, foreground='#9aa0a6').pack(anchor='w', padx=8, pady=(0, 7))
        streamer = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['c18'])
        streamer.pack(fill='x', pady=6)
        ttk.Checkbutton(streamer, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['d18'], variable=self.streamer_mode, command=self._apply_streamer_mode).pack(anchor='w', padx=8, pady=4)
        ttk.Label(streamer, text=UI_TEXT['e18'], foreground='#9aa0a6').pack(anchor='w', padx=8, pady=(0, 6))
        updates = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['f18'])
        updates.pack(fill='x', pady=6)
        ttk.Checkbutton(updates, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['g18'], variable=self.auto_update, command=self._save_settings).pack(anchor='w', padx=8, pady=(6, 1))
        ttk.Label(updates, text=UI_TEXT['h18'], foreground='#9aa0a6').pack(anchor='w', padx=8, pady=(0, 7))
        gemini = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['i18'])
        gemini.pack(fill='x', pady=6)
        ttk.Label(gemini, text=UI_TEXT['j18']).grid(row=0, column=0, sticky='w', padx=8, pady=(8, 4))
        key_entry = ttk.Entry(gemini, textvariable=self.gemini_api_key, show='•')
        key_entry.grid(row=1, column=0, columnspan=2, sticky='ew', padx=8, pady=(0, 8))
        gemini.columnconfigure(0, weight=1)
        ttk.Button(gemini, text=UI_TEXT['k18'], command=lambda: _open_webview2_process('https://raw.githubusercontent.com/offp001/routils/refs/heads/main/src/help/API%20Key%20Tutorial.txt', 'Gemini API Key Tutorial')).grid(row=2, column=0, sticky='w', padx=8, pady=(0, 8))
        ttk.Button(gemini, text=UI_TEXT['l18'], command=self._save_gemini_api_key).grid(row=2, column=1, sticky='e', padx=8, pady=(0, 8))
        db = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['m18'])
        db.pack(fill='x', pady=6)
        ttk.Button(db, text=UI_TEXT['n18'], command=self._choose_db).pack(anchor='w', padx=8, pady=4)
        ttk.Button(db, text=UI_TEXT['o18'], command=self._choose_shard_root).pack(anchor='w', padx=8, pady=4)
        settings_box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text=UI_TEXT['p18'])
        settings_box.pack(fill='x', pady=6)
        self.include_cconfigs = tk.BooleanVar(value=bool(self.settings.get('include_cconfigs', False)))
        self.include_cache_dumps = tk.BooleanVar(value=bool(self.settings.get('include_cache_dumps', False)))
        self.include_cconfigs.trace_add('write', lambda *_: self._save_settings())
        self.include_cache_dumps.trace_add('write', lambda *_: self._save_settings())
        ttk.Checkbutton(settings_box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['q18'], variable=self.include_cconfigs).pack(anchor='w', padx=8, pady=(7, 2))
        ttk.Checkbutton(settings_box, style='RoUtils.Settings.TCheckbutton', text=UI_TEXT['r18'], variable=self.include_cache_dumps).pack(anchor='w', padx=8, pady=2)
        backup_buttons = ttk.Frame(settings_box)
        backup_buttons.pack(fill='x', padx=8, pady=8)
        ttk.Button(backup_buttons, text=UI_TEXT['s18'], command=self._export_settings).pack(side='left')
        ttk.Button(backup_buttons, text=UI_TEXT['t18'], command=self._import_settings).pack(side='left', padx=(7, 0))
    def _save_dpi_setting_only(self):
        try:
            percent = max(50, min(200, int(self.dpi_percent.get())))
            self.settings['dpi_percent'] = percent
            self._save_settings()
        except Exception as exc:
            self._console_log(UI_TEXT['u18'].format(p0=exc))
    def _export_settings(self):
        self._save_settings()
        path = filedialog.asksaveasfilename(parent=self, title=UI_TEXT['v18'], defaultextension='.rconfig', filetypes=[(UI_TEXT['w18'], '*.rconfig'), (UI_TEXT['x18'], '*.zip'), (UI_TEXT['y18'], '*.json')])
        if not path:
            return
        try:
            if path.lower().endswith('.json'):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, ensure_ascii=False, indent=2)
            else:
                with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
                    archive.writestr('settings.json', json.dumps(self.settings, ensure_ascii=False, indent=2))
                    include_cconfigs = bool(self.include_cconfigs.get())
                    include_dumps = bool(self.include_cache_dumps.get())
                    for root, dirs, files in os.walk(DATA_DIR):
                        dirs[:] = [name for name in dirs if name != 'errors' and (name != 'cconfigs' or include_cconfigs) and (name != 'Dump' or include_dumps)]
                        for filename in files:
                            full = os.path.join(root, filename)
                            relative = os.path.relpath(full, DATA_DIR).replace('\\', '/')
                            if relative == 'routils_settings.json' or relative.startswith('errors/'):
                                continue
                            if relative.startswith('cconfigs/') and (not include_cconfigs):
                                continue
                            if (relative == 'Dump' or relative.startswith('Dump/')) and (not include_dumps):
                                continue
                            archive.write(full, relative)
            self._console_log(UI_TEXT['z18'].format(p0=path))
            messagebox.showinfo(UI_TEXT['p18'], UI_TEXT['a19'], parent=self)
        except Exception as exc:
            messagebox.showerror(UI_TEXT['p18'], UI_TEXT['b19'].format(p0=exc), parent=self)
    def _import_settings(self):
        path = filedialog.askopenfilename(parent=self, title=UI_TEXT['c19'], filetypes=[(UI_TEXT['w18'], '*.rconfig *.zip'), (UI_TEXT['x18'], '*.zip'), (UI_TEXT['y18'], '*.json'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        try:
            if path.lower().endswith(('.rconfig', '.zip')):
                with zipfile.ZipFile(path, 'r') as archive:
                    names = set(archive.namelist())
                    settings_name = 'settings.json' if 'settings.json' in names else 'config.json' if 'config.json' in names else None
                    if not settings_name:
                        raise ValueError('This archive does not contain RoUtils settings.')
                    data = json.loads(archive.read(settings_name).decode('utf-8'))
                    if not isinstance(data, dict):
                        raise ValueError(UI_TEXT['h32'])
                    self.settings.update(data)
                    for name in ('fflags.json', 'cconfigs/routils_fflags.json'):
                        if name in names:
                            target = self._fflag_path()
                            with open(target, 'wb') as f:
                                f.write(archive.read(name))
                            break
                    for name in names:
                        normalized = name.replace('\\', '/').lstrip('/')
                        if normalized.startswith('../') or '/..' in normalized or ':' in normalized:
                            continue
                        if normalized.startswith(('cconfigs/', 'Dump/', 'jsons/', 'plugins/')) or normalized in {'history.json', 'console_history.json', 'routils_cconfigs_state.json', 'routils_fflags.json'}:
                            target = os.path.abspath(os.path.join(DATA_DIR, normalized))
                            if os.path.commonpath((os.path.abspath(DATA_DIR), target)) != os.path.abspath(DATA_DIR):
                                continue
                            os.makedirs(os.path.dirname(target), exist_ok=True)
                            with open(target, 'wb') as f:
                                f.write(archive.read(name))
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError(UI_TEXT['h32'])
                self.settings.update(data)
            self.settings.pop('multi_instance_enabled', None)
            if hasattr(self, 'discord_application_id_var'):
                imported_id = str(self.settings.get('discord_application_id') or DISCORD_APPLICATION_ID).strip()
                if imported_id.isdigit():
                    self.discord_application_id_var.set(imported_id)
                    if hasattr(self, '_discord_rpc'):
                        self._discord_rpc.set_client_id(imported_id)
            for name in ('autoscroll', 'hide_tickets', 'stay_on_top', 'show_lines', 'streamer_mode', 'autostart_watch', 'auto_update', 'launch_on_tray', 'launch_on_startup', 'hide_to_tray_on_close', 'discord_rpc_enabled'):
                var = getattr(self, name, None)
                if var is not None and name in self.settings:
                    var.set(bool(self.settings[name]))
            if hasattr(self, 'include_cconfigs'):
                self.include_cconfigs.set(bool(self.settings.get('include_cconfigs', False)))
                self.include_cache_dumps.set(bool(self.settings.get('include_cache_dumps', False)))
            if 'fps_limit' in self.settings:
                self.fps_limit.set(max(0, min(240, int(self.settings['fps_limit']))))
            if 'theme' in self.settings and hasattr(self, 'theme_var'):
                self.theme_var.set(str(self.settings['theme']))
                self._apply_theme()
            if hasattr(self, '_discord_rpc'):
                self._discord_rpc.set_enabled(bool(self.discord_rpc_enabled.get()))
                self._refresh_discord_rpc_activity()
            self._load_fflag_flags()
            if hasattr(self, 'fflag_tree'):
                self._refresh_fflag_list()
            self._save_settings()
            self._console_log(UI_TEXT['d19'].format(p0=path))
            messagebox.showinfo(UI_TEXT['p18'], UI_TEXT['e19'], parent=self)
        except Exception as exc:
            messagebox.showerror(UI_TEXT['p18'], UI_TEXT['f19'].format(p0=exc), parent=self)
    def _startup_setting_changed(self):
        self._save_settings()
        self._install_startup_shortcut()
        self._update_kill_routils_visibility()
    def _install_startup_shortcut(self):
        if os.name != 'nt':
            return
        run_path = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        value_name = 'RoUtils'
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_path, 0, winreg.KEY_SET_VALUE) as key:
                if not self.launch_on_startup.get():
                    try:
                        winreg.DeleteValue(key, value_name)
                    except FileNotFoundError:
                        pass
                    return
                target = sys.executable
                if not getattr(sys, 'frozen', False):
                    base = os.path.basename(target).lower()
                    if base == 'python.exe':
                        candidate = os.path.join(os.path.dirname(target), 'pythonw.exe')
                        if os.path.isfile(candidate):
                            target = candidate
                    command = f'"{target}" "{os.path.abspath(__file__)}"'
                else:
                    command = f'"{target}"'
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, command)
        except Exception as exc:
            try:
                self._console_log(UI_TEXT['n27'].format(p0=exc))
                messagebox.showerror(UI_TEXT['y17'], UI_TEXT['o27'].format(p0=exc), parent=self)
            except Exception:
                pass
