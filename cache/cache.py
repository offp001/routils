import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class CacheMixin:
    def _wrap_rbxm_as_blob(self, data: bytes, content_type: str='application/octet-stream') -> bytes:
        if data[:4] == RBXH_MAGIC:
            return _wrap_rbxm_bytes(_extract_rbxh_document(data), content_type)
        return _wrap_rbxm_bytes(data, content_type)
    def _utils_r6_to_r15(self):
        src = filedialog.askopenfilename(parent=self, title=UI_TEXT['x7'], filetypes=[(UI_TEXT['y7'], '*.rbxm *.rbxmx'), (UI_TEXT['z7'], '*.*')])
        if not src:
            return
        try:
            with open(src, 'rb') as f:
                data = f.read()
            out = convert_r6_animation_to_r15(data)
            base = os.path.splitext(os.path.basename(src))[0] + '_R15.rbxmx'
            dest = filedialog.asksaveasfilename(parent=self, title=UI_TEXT['a8'], initialfile=base, defaultextension='.rbxmx', filetypes=[(UI_TEXT['b8'], '*.rbxmx'), (UI_TEXT['z7'], '*.*')])
            if not dest:
                return
            with open(dest, 'wb') as f:
                f.write(out)
            messagebox.showinfo(UI_TEXT['c8'], UI_TEXT['d8'].format(p0=dest), parent=self)
            self._console_log(UI_TEXT['e8'].format(p0=dest))
        except Exception as e:
            messagebox.showerror(UI_TEXT['c8'], UI_TEXT['f8'].format(p0=e), parent=self)
    def _cc_state_path(self):
        return os.path.join(DATA_DIR, 'routils_cconfigs_state.json')
    def _cc_load_applied_state(self):
        try:
            with open(self._cc_state_path(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.cc_applied_caches = data if isinstance(data, list) else []
        except Exception:
            self.cc_applied_caches = []
    def _cc_save_applied_state(self):
        try:
            with open(self._cc_state_path(), 'w', encoding='utf-8') as f:
                json.dump(self.cc_applied_caches, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    def _cc_record_applied_caches(self, caches):
        if not caches:
            return
        now = datetime.now().isoformat(timespec='seconds')
        by_hash = {}
        for item in self.cc_applied_caches:
            if isinstance(item, dict):
                h = str(item.get('hash', '')).lower()
                if h:
                    by_hash[h] = item
        for item in caches:
            if not isinstance(item, dict):
                continue
            h = re.sub('[^0-9A-Fa-f]', '', str(item.get('hash', ''))).lower()
            if not h:
                continue
            by_hash[h] = {'hash': h, 'name': str(item.get('name', '')), 'applied_at': str(item.get('applied_at') or now)}
        self.cc_applied_caches = list(by_hash.values())
        self._cc_save_applied_state()
        if hasattr(self, 'cc_cache_count_label'):
            self.cc_cache_count_label.config(text=UI_TEXT['g8'].format(p0=len(self.cc_applied_caches)))
    def _cc_safe_name(self, name):
        name = re.sub('[<>:"/\\\\\\\\|?*]', '_', str(name)).strip().rstrip('.')
        return name or 'Config'
    def _cc_unique_path(self, directory, filename):
        base, ext = os.path.splitext(filename)
        path = os.path.join(directory, filename)
        i = 1
        while os.path.exists(path):
            path = os.path.join(directory, f'{base} ({i}){ext}')
            i += 1
        return path
    def _cc_snapshot_database(self, src_db, dst_db):
        if not os.path.isfile(src_db):
            raise FileNotFoundError(f'Database not found:\n{src_db}')
        os.makedirs(os.path.dirname(dst_db), exist_ok=True)
        try:
            src_conn = sqlite3.connect(src_db, timeout=3)
            dst_conn = sqlite3.connect(dst_db)
            with dst_conn:
                src_conn.backup(dst_conn)
            dst_conn.close()
            src_conn.close()
        except Exception:
            try:
                if os.path.exists(dst_db):
                    os.remove(dst_db)
            except Exception:
                pass
            shutil.copy2(src_db, dst_db)
    def _cc_make_package(self, destination, name):
        src_db = getattr(self, 'db_path', None)
        if not src_db or not os.path.isfile(src_db):
            raise FileNotFoundError(UI_TEXT['t29'])
        with tempfile.TemporaryDirectory(prefix='routils_cc_') as td:
            snap = os.path.join(td, 'rbx-storage.db')
            self._cc_snapshot_database(src_db, snap)
            metadata = {'format': 'RoUtils CConfigs', 'version': 1, 'name': name, 'created_at': datetime.now().isoformat(timespec='seconds'), 'source_db': os.path.abspath(src_db), 'applied_caches': list(self.cc_applied_caches)}
            with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.write(snap, 'rbx-storage.db')
                z.writestr('config.json', json.dumps(metadata, ensure_ascii=False, indent=2))
    def _cc_read_package_info(self, path):
        if path.lower().endswith('.db'):
            conn = sqlite3.connect(path, timeout=3)
            try:
                conn.execute('PRAGMA schema_version').fetchone()
            finally:
                conn.close()
            return {'name': os.path.splitext(os.path.basename(path))[0], 'created_at': '', 'applied_caches': [], 'raw_db': True}
        with zipfile.ZipFile(path, 'r') as z:
            if 'config.json' not in z.namelist():
                raise ValueError('This is not a valid CConfigs package.')
            info = json.loads(z.read('config.json').decode('utf-8'))
            if 'rbx-storage.db' not in z.namelist():
                raise ValueError('CConfigs package is missing rbx-storage.db.')
            info['raw_db'] = False
            return info
    def _cc_scan_packages(self):
        out = []
        try:
            names = os.listdir(self.cconfigs_dir)
        except Exception:
            names = []
        for fname in names:
            if not fname.lower().endswith(('.ccdb', '.db')):
                continue
            path = os.path.join(self.cconfigs_dir, fname)
            try:
                info = self._cc_read_package_info(path)
            except Exception:
                info = {'name': os.path.splitext(fname)[0], 'created_at': '', 'applied_caches': []}
            info['_path'] = path
            info['_file'] = fname
            out.append(info)
        out.sort(key=lambda x: str(x.get('name', '')).lower())
        return out
    def _cc_refresh_list(self, select_path=None):
        if not hasattr(self, 'cc_tree'):
            return
        self.cc_tree.delete(*self.cc_tree.get_children())
        packages = self._cc_scan_packages()
        wanted = os.path.abspath(select_path) if select_path else None
        selected_iid = None
        for i, info in enumerate(packages):
            iid = str(i)
            caches = info.get('applied_caches') or []
            self.cc_tree.insert('', 'end', iid=iid, values=(info.get('name', os.path.splitext(info.get('_file', ''))[0]), info.get('created_at', ''), len(caches), info.get('_file', '')))
            if wanted and os.path.abspath(info.get('_path', '')) == wanted:
                selected_iid = iid
        if selected_iid is not None:
            self.cc_tree.selection_set(selected_iid)
            self.cc_tree.focus(selected_iid)
        self._cc_show_selected()
    def _cc_selected_info(self):
        sel = self.cc_tree.selection() if hasattr(self, 'cc_tree') else ()
        if not sel:
            return None
        try:
            idx = int(sel[0])
        except Exception:
            return None
        packages = self._cc_scan_packages()
        return packages[idx] if 0 <= idx < len(packages) else None
    def _cc_show_selected(self, _event=None):
        if not hasattr(self, 'cc_details'):
            return
        info = self._cc_selected_info()
        self.cc_details.configure(state='normal')
        self.cc_details.delete('1.0', tk.END)
        if not info:
            self.cc_details.insert(tk.END, UI_TEXT['s27'])
        else:
            caches = info.get('applied_caches') or []
            lines = [f"Config: {info.get('name', '')}", f"Created: {info.get('created_at', '')}", f"File: {info.get('_file', '')}", '', f'Applied caches: {len(caches)}', '']
            if caches:
                for i, cache in enumerate(caches, 1):
                    name = cache.get('name', '(unnamed)')
                    h = cache.get('hash', '')
                    at = cache.get('applied_at', '')
                    lines.append(f'{i}. {name}')
                    lines.append(f'   Hash: {h}')
                    if at:
                        lines.append(f'   Applied: {at}')
            else:
                lines.append('No cache applications were recorded for this config.')
            self.cc_details.insert(tk.END, '\n'.join(lines))
        self.cc_details.configure(state='disabled')
    def _cc_save_db(self):
        name = simpledialog.askstring(UI_TEXT['h8'], UI_TEXT['i8'], parent=self)
        if not name:
            return
        self._cc_save_named_config(name)
    def _cc_save_named_config(self, name):
        name = self._cc_safe_name(name)
        if not name:
            raise ValueError(UI_TEXT['v29'])
        path = self._cc_unique_path(self.cconfigs_dir, name + '.ccdb')
        try:
            self._cc_make_package(path, name)
        except Exception as e:
            messagebox.showerror(UI_TEXT['j8'], UI_TEXT['k8'].format(p0=e), parent=self)
            return
        self._cc_refresh_list(select_path=path)
        messagebox.showinfo(UI_TEXT['j8'], UI_TEXT['l8'].format(p0=os.path.basename(path), p1=len(self.cc_applied_caches)), parent=self)
    def _cc_upload_db(self):
        path = filedialog.askopenfilename(parent=self, title=UI_TEXT['m8'], filetypes=[(UI_TEXT['n8'], '*.db *.ccdb'), (UI_TEXT['o8'], '*.db'), (UI_TEXT['p8'], '*.ccdb'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        try:
            info = self._cc_read_package_info(path)
            if path.lower().endswith('.db'):
                name = self._cc_safe_name(os.path.splitext(os.path.basename(path))[0] or 'rbx-storage')
                dest = self._cc_unique_path(self.cconfigs_dir, name + '.db')
            else:
                name = self._cc_safe_name(info.get('name') or os.path.splitext(os.path.basename(path))[0])
                dest = self._cc_unique_path(self.cconfigs_dir, name + '.ccdb')
            shutil.copy2(path, dest)
        except Exception as e:
            messagebox.showerror(UI_TEXT['j8'], UI_TEXT['q8'].format(p0=e), parent=self)
            return
        self._cc_refresh_list(select_path=dest)
        messagebox.showinfo(UI_TEXT['j8'], UI_TEXT['r8'].format(p0=os.path.basename(dest)), parent=self)
    def _cc_apply_db(self):
        info = self._cc_selected_info()
        if not info:
            messagebox.showinfo(UI_TEXT['j8'], UI_TEXT['s8'], parent=self)
            return
        if not messagebox.askyesno(UI_TEXT['t8'], UI_TEXT['u8'].format(p0=info.get('name', '')), parent=self):
            return
        was_watching = self.watching
        if was_watching:
            self._stop_watching()
        temp_source = None
        try:
            with tempfile.NamedTemporaryFile(prefix='routils_cc_apply_', suffix='.db', delete=False) as tf:
                temp_source = tf.name
            if info.get('raw_db') or info.get('_file', '').lower().endswith('.db'):
                shutil.copy2(info['_path'], temp_source)
            else:
                with tempfile.TemporaryDirectory(prefix='routils_apply_cc_') as td:
                    with zipfile.ZipFile(info['_path'], 'r') as z:
                        z.extract('rbx-storage.db', td)
                    shutil.copy2(os.path.join(td, 'rbx-storage.db'), temp_source)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute('PRAGMA schema_version').fetchone()
            conn.close()
            self._install_selected_db(temp_source)
            self.cc_applied_caches = list(info.get('applied_caches') or [])
            self._cc_save_applied_state()
            self._update_status()
            if was_watching:
                self._start_watching()
        except Exception as e:
            messagebox.showerror(UI_TEXT['j8'], UI_TEXT['v8'].format(p0=e), parent=self)
            if was_watching:
                self._start_watching()
            return
        finally:
            if temp_source:
                try:
                    os.remove(temp_source)
                except Exception:
                    pass
        if hasattr(self, 'cc_cache_count_label'):
            self.cc_cache_count_label.config(text=UI_TEXT['g8'].format(p0=len(self.cc_applied_caches)))
        messagebox.showinfo(UI_TEXT['j8'], UI_TEXT['w8'].format(p0=info.get('name', ''), p1=len(self.cc_applied_caches)), parent=self)
    def _cc_export_db(self):
        info = self._cc_selected_info()
        if not info:
            messagebox.showinfo(UI_TEXT['j8'], UI_TEXT['s8'], parent=self)
            return
        base = self._cc_safe_name(info.get('name') or 'config') + '.db'
        path = filedialog.asksaveasfilename(parent=self, title=UI_TEXT['x8'], initialfile=base, defaultextension='.db', filetypes=[(UI_TEXT['o8'], '*.db'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        temp_source = None
        try:
            with tempfile.NamedTemporaryFile(prefix='routils_cc_export_', suffix='.db', delete=False) as tf:
                temp_source = tf.name
            if info.get('raw_db') or info.get('_file', '').lower().endswith('.db'):
                shutil.copy2(info['_path'], temp_source)
            else:
                with zipfile.ZipFile(info['_path'], 'r') as z:
                    with z.open('rbx-storage.db') as src, open(temp_source, 'wb') as dst:
                        shutil.copyfileobj(src, dst)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute('PRAGMA schema_version').fetchone()
            conn.close()
            shutil.copy2(temp_source, path)
        except Exception as e:
            messagebox.showerror(UI_TEXT['j8'], UI_TEXT['y8'].format(p0=e), parent=self)
            return
        finally:
            if temp_source:
                try:
                    os.remove(temp_source)
                except Exception:
                    pass
        messagebox.showinfo(UI_TEXT['j8'], UI_TEXT['z8'].format(p0=path), parent=self)
    def _cc_delete_db(self):
        info = self._cc_selected_info()
        if not info:
            return
        if not messagebox.askyesno(UI_TEXT['a9'], UI_TEXT['b9'].format(p0=info.get('name', '')), parent=self):
            return
        try:
            os.remove(info['_path'])
        except Exception as e:
            messagebox.showerror(UI_TEXT['j8'], UI_TEXT['c9'].format(p0=e), parent=self)
            return
        self._cc_refresh_list()
    def _build_cconfigs_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text=UI_TEXT['l5'])
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text=UI_TEXT['l5'], font=('Segoe UI Semibold', 15)).pack(side='left')
        self.cc_cache_count_label = ttk.Label(head, text=UI_TEXT['g8'].format(p0=len(self.cc_applied_caches)), foreground='#9aa0a6')
        self.cc_cache_count_label.pack(side='right')
        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        for label, command in ((UI_TEXT['w29'], self._cc_save_db), (UI_TEXT['m8'], self._cc_upload_db), (UI_TEXT['t8'], self._cc_apply_db), (UI_TEXT['x29'], self._cc_export_db), ('Delete DB', self._cc_delete_db), ('Refresh', lambda: self._cc_refresh_list())):
            ttk.Button(bar, text=label, command=command).pack(side='left', padx=(0, 6))
        paned = ttk.PanedWindow(tab, orient='vertical')
        paned.grid(row=2, column=0, sticky='nsew')
        top = ttk.Frame(paned)
        bottom = ttk.Frame(paned)
        paned.add(top, weight=3)
        paned.add(bottom, weight=2)
        columns = ('name', 'created', 'caches', 'file')
        self.cc_tree = ttk.Treeview(top, columns=columns, show='headings', selectmode='browse')
        self.cc_tree.heading('name', text=UI_TEXT['d9'])
        self.cc_tree.heading('created', text=UI_TEXT['e9'])
        self.cc_tree.heading('caches', text=UI_TEXT['f9'])
        self.cc_tree.heading('file', text=UI_TEXT['g9'])
        self.cc_tree.column('name', width=240, anchor='w')
        self.cc_tree.column('created', width=160, anchor='w')
        self.cc_tree.column('caches', width=80, anchor='center')
        self.cc_tree.column('file', width=280, anchor='w')
        self.cc_tree.pack(side='left', fill='both', expand=True)
        cc_scroll = ttk.Scrollbar(top, orient='vertical', command=self.cc_tree.yview)
        cc_scroll.pack(side='right', fill='y')
        self.cc_tree.configure(yscrollcommand=cc_scroll.set)
        self.cc_tree.bind('<<TreeviewSelect>>', self._cc_show_selected)
        self.cc_tree.bind('<Double-1>', lambda _e: self._cc_apply_db())
        ttk.Label(bottom, text=UI_TEXT['h9'], font=('Segoe UI Semibold', 10)).pack(anchor='w', pady=(4, 4))
        self.cc_details = tk.Text(bottom, wrap='word', height=8, font=('Consolas', 9), bg='#252526', fg='#d4d4d4', insertbackground='#ffffff', selectbackground='#007acc', selectforeground='#ffffff', relief='flat', bd=0)
        self.cc_details.pack(fill='both', expand=True)
        self.cc_details.configure(state='disabled')
        self._cc_refresh_list()
    def _build_utils_tab(self):
        tab_outer = _ScrollableTab(self.nb, padding=0)
        tab = tab_outer.inner
        self.nb.insert(2, tab_outer, text=UI_TEXT['k5'])
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text=UI_TEXT['k5'], font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w')
        ttk.Label(tab, text=UI_TEXT['l9'], foreground='#9aa0a6').grid(row=1, column=0, sticky='w', pady=(0, 14))
        converters = ttk.LabelFrame(tab, text=UI_TEXT['m9'], padding=14)
        converters.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        ttk.Button(converters, text=UI_TEXT['x7'], command=self._utils_r6_to_r15).pack(anchor='w', pady=(0, 6))
        ttk.Button(converters, text=UI_TEXT['n9'], command=self._utils_roblox_file_convert).pack(anchor='w', pady=(0, 6))
        ttk.Button(converters, text=UI_TEXT['o9'], command=self._utils_mesh_to_obj).pack(anchor='w')
        mesh = ttk.LabelFrame(tab, text=UI_TEXT['p9'], padding=14)
        mesh.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(mesh, text=UI_TEXT['q9']).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        pathrow = ttk.Frame(mesh)
        pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        pathrow.columnconfigure(0, weight=1)
        self.roblox_path_var = tk.StringVar(value=self.settings.get('roblox_path', ''))
        ttk.Entry(pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(pathrow, text=UI_TEXT['r9'], command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(pathrow, text=UI_TEXT['s9'], command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        self.mesh_rows = {}
        for i, name in enumerate(('Head.mesh', 'leftarm.mesh', 'leftleg.mesh', 'rightarm.mesh', 'rightleg.mesh', 'torso.mesh'), start=2):
            ttk.Label(mesh, text=name).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Button(mesh, text=UI_TEXT['b2'], command=lambda n=name: self._delete_default_mesh(n)).grid(row=i, column=1, padx=5)
            ttk.Button(mesh, text=UI_TEXT['r9'], command=lambda n=name: self._choose_default_mesh(n)).grid(row=i, column=2)
        mesh.columnconfigure(0, weight=1)
        sky = ttk.LabelFrame(tab, text=UI_TEXT['t9'], padding=14)
        sky.grid(row=4, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(sky, text=UI_TEXT['u9']).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        sky_pathrow = ttk.Frame(sky)
        sky_pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        sky_pathrow.columnconfigure(0, weight=1)
        ttk.Entry(sky_pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(sky_pathrow, text=UI_TEXT['r9'], command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(sky_pathrow, text=UI_TEXT['s9'], command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        for i, name in enumerate(SKYBOX_TEXTURES, start=2):
            ttk.Label(sky, text=name).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Button(sky, text=UI_TEXT['b2'], command=lambda n=name: self._delete_skybox_texture(n)).grid(row=i, column=1, padx=5)
            ttk.Button(sky, text=UI_TEXT['r9'], command=lambda n=name: self._choose_skybox_texture(n)).grid(row=i, column=2)
        sky.columnconfigure(0, weight=1)
        sounds = ttk.LabelFrame(tab, text=UI_TEXT['v9'], padding=14)
        sounds.grid(row=5, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(sounds, text=UI_TEXT['w9']).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        sound_pathrow = ttk.Frame(sounds)
        sound_pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        sound_pathrow.columnconfigure(0, weight=1)
        ttk.Entry(sound_pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(sound_pathrow, text=UI_TEXT['r9'], command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(sound_pathrow, text=UI_TEXT['s9'], command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        for i, name in enumerate(SOUND_FILES, start=2):
            ttk.Label(sounds, text=name).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Button(sounds, text=UI_TEXT['b2'], command=lambda n=name: self._delete_roblox_sound(n)).grid(row=i, column=1, padx=5)
            ttk.Button(sounds, text=UI_TEXT['r9'], command=lambda n=name: self._choose_roblox_sound(n)).grid(row=i, column=2)
        sounds.columnconfigure(0, weight=1)
        others = ttk.LabelFrame(tab, text=UI_TEXT['x9'], padding=14)
        others.grid(row=6, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(others, text=UI_TEXT['y9']).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        other_pathrow = ttk.Frame(others)
        other_pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        other_pathrow.columnconfigure(0, weight=1)
        ttk.Entry(other_pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(other_pathrow, text=UI_TEXT['r9'], command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(other_pathrow, text=UI_TEXT['s9'], command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        ttk.Label(others, text=UI_TEXT['z9']).grid(row=2, column=0, sticky='w', pady=3)
        ttk.Button(others, text=UI_TEXT['b2'], command=lambda: self._delete_other_file('studs')).grid(row=2, column=1, padx=5)
        ttk.Button(others, text=UI_TEXT['r9'], command=lambda: self._choose_other_file('studs')).grid(row=2, column=2)
        ttk.Label(others, text=UI_TEXT['a10']).grid(row=3, column=0, sticky='w', pady=3)
        ttk.Button(others, text=UI_TEXT['b2'], command=lambda: self._delete_other_file('diffuse')).grid(row=3, column=1, padx=5)
        ttk.Button(others, text=UI_TEXT['r9'], command=lambda: self._choose_other_file('diffuse')).grid(row=3, column=2)
        ttk.Label(others, text=UI_TEXT['b10']).grid(row=4, column=0, sticky='w', pady=3)
        ttk.Button(others, text=UI_TEXT['b2'], command=lambda: self._delete_other_file('font')).grid(row=4, column=1, padx=5)
        ttk.Button(others, text=UI_TEXT['r9'], command=lambda: self._choose_other_file('font')).grid(row=4, column=2)
        others.columnconfigure(0, weight=1)
    def _default_mesh_path(self, name):
        root = self.roblox_path_var.get().strip()
        if not root or os.path.basename(root).lower() != 'robloxplayerbeta.exe':
            return None
        root = os.path.dirname(root)
        folder = 'heads' if name.lower() == 'head.mesh' else 'meshes'
        return os.path.join(root, 'content', 'avatar', folder, name)
    def _choose_default_mesh(self, name):
        target = self._default_mesh_path(name)
        if not target:
            messagebox.showwarning(UI_TEXT['p9'], UI_TEXT['a11'], parent=self)
            return
        src = filedialog.askopenfilename(parent=self, title=UI_TEXT['b11'].format(p0=name), filetypes=[(UI_TEXT['c11'], '*.mesh'), (UI_TEXT['z7'], '*.*')])
        if not src:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(src).lower() == os.path.abspath(target).lower():
                return
            if os.path.exists(target):
                os.remove(target)
            shutil.copy2(src, target)
        except Exception as e:
            messagebox.showerror(UI_TEXT['p9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _delete_default_mesh(self, name):
        target = self._default_mesh_path(name)
        if not target:
            return
        try:
            if os.path.exists(target):
                os.remove(target)
        except Exception as e:
            messagebox.showerror(UI_TEXT['p9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _skybox_path(self, name):
        root = self.roblox_path_var.get().strip()
        if not root or os.path.basename(root).lower() != 'robloxplayerbeta.exe':
            return None
        return os.path.join(os.path.dirname(root), 'PlatformContent', 'pc', 'textures', 'sky', name)
    def _choose_skybox_texture(self, name):
        target = self._skybox_path(name)
        if not target:
            messagebox.showwarning(UI_TEXT['t9'], UI_TEXT['a11'], parent=self)
            return
        source = filedialog.askopenfilename(parent=self, title=UI_TEXT['b11'].format(p0=name), filetypes=[(UI_TEXT['e11'], '*.tex'), (UI_TEXT['z7'], '*.*')])
        if not source:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(source).lower() != os.path.abspath(target).lower():
                if os.path.exists(target):
                    os.remove(target)
                shutil.copy2(source, target)
            self._console_log(UI_TEXT['f11'].format(p0=name))
        except Exception as e:
            messagebox.showerror(UI_TEXT['t9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _delete_skybox_texture(self, name):
        target = self._skybox_path(name)
        if not target:
            return
        try:
            if os.path.exists(target):
                os.remove(target)
                self._console_log(UI_TEXT['g11'].format(p0=name))
        except Exception as e:
            messagebox.showerror(UI_TEXT['t9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _roblox_content_path(self, *parts):
        root = self.roblox_path_var.get().strip()
        if not root or os.path.basename(root).lower() != 'robloxplayerbeta.exe':
            return None
        return os.path.join(os.path.dirname(root), *parts)
    def _sound_path(self, name):
        return self._roblox_content_path('content', 'sounds', name)
    def _choose_roblox_sound(self, name):
        target = self._sound_path(name)
        if not target:
            messagebox.showwarning(UI_TEXT['v9'], UI_TEXT['a11'], parent=self)
            return
        source = filedialog.askopenfilename(parent=self, title=UI_TEXT['b11'].format(p0=name), filetypes=[(UI_TEXT['h11'], '*.ogg *.mp3 *.wav'), (UI_TEXT['z7'], '*.*')])
        if not source:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(source).lower() != os.path.abspath(target).lower():
                if os.path.exists(target):
                    os.remove(target)
                shutil.copy2(source, target)
            self._console_log(UI_TEXT['i11'].format(p0=name))
        except Exception as e:
            messagebox.showerror(UI_TEXT['v9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _delete_roblox_sound(self, name):
        target = self._sound_path(name)
        if not target:
            messagebox.showwarning(UI_TEXT['v9'], UI_TEXT['a11'], parent=self)
            return
        try:
            if os.path.exists(target):
                os.remove(target)
                self._console_log(UI_TEXT['j11'].format(p0=name))
        except Exception as e:
            messagebox.showerror(UI_TEXT['v9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _other_path(self, kind):
        if kind == 'studs':
            return self._roblox_content_path('PlatformContent', 'pc', 'textures', 'plastic', 'normal.dds')
        if kind == 'diffuse':
            return self._roblox_content_path('PlatformContent', 'pc', 'textures', 'plastic', 'diffuse.dds')
        if kind == 'font':
            return self._roblox_content_path('content', 'fonts', 'CustomFont.ttf')
        return None
    def _choose_other_file(self, kind):
        target = self._other_path(kind)
        if not target:
            messagebox.showwarning(UI_TEXT['x9'], UI_TEXT['a11'], parent=self)
            return
        if kind == 'studs':
            title = UI_TEXT['k28']
            filetypes = [('DDS texture', '*.dds'), ('All files', '*.*')]
        elif kind == 'diffuse':
            title = UI_TEXT['l28']
            filetypes = [('DDS texture', '*.dds'), ('All files', '*.*')]
        else:
            title = UI_TEXT['m28']
            filetypes = [('TrueType Font', '*.ttf'), ('All files', '*.*')]
        source = filedialog.askopenfilename(parent=self, title=title, filetypes=filetypes)
        if not source:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(source).lower() != os.path.abspath(target).lower():
                if os.path.exists(target):
                    os.remove(target)
                shutil.copy2(source, target)
            self._console_log(UI_TEXT['k11'].format(p0=os.path.basename(target)))
        except Exception as e:
            messagebox.showerror(UI_TEXT['x9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _delete_other_file(self, kind):
        target = self._other_path(kind)
        if not target:
            messagebox.showwarning(UI_TEXT['x9'], UI_TEXT['a11'], parent=self)
            return
        try:
            if os.path.exists(target):
                os.remove(target)
                self._console_log(UI_TEXT['l11'].format(p0=os.path.basename(target)))
        except Exception as e:
            messagebox.showerror(UI_TEXT['x9'], UI_TEXT['d11'].format(p0=e), parent=self)
    def _utils_mesh_to_obj(self):
        src = filedialog.askopenfilename(parent=self, title=UI_TEXT['m11'], filetypes=[(UI_TEXT['n11'], '*.mesh'), (UI_TEXT['z7'], '*.*')])
        if not src:
            return
        out = os.path.splitext(src)[0] + '.obj'
        try:
            with open(src, 'rb') as f:
                data = f.read()
            ver = _mesh_header(data).replace('version ', '') or 'unknown'
            print(UI_TEXT['o11'].format(p0=ver))
            print(UI_TEXT['p11'])
            convert(data, out)
            print(UI_TEXT['q11'].format(p0=out))
        except Exception as e:
            messagebox.showerror(UI_TEXT['o9'], UI_TEXT['r11'].format(p0=e), parent=self)
    def _utils_roblox_file_convert(self):
        src = filedialog.askopenfilename(parent=self, title=UI_TEXT['s11'], filetypes=[(UI_TEXT['t11'], '*.rbxm *.rbxh *.rbxmx'), (UI_TEXT['u11'], '*.rbxm'), (UI_TEXT['v11'], '*.rbxh'), (UI_TEXT['w11'], '*.rbxmx'), (UI_TEXT['z7'], '*.*')])
        if not src:
            return
        try:
            with open(src, 'rb') as f:
                content = f.read()
            filename, ext = os.path.splitext(os.path.basename(src))
            ext = ext.lower()
            if ext not in ('.rbxm', '.rbxh', '.rbxmx'):
                messagebox.showwarning(UI_TEXT['x11'], UI_TEXT['y11'], parent=self)
                return
            if ext in ('.rbxm', '.rbxmx'):
                new_ext = '.rbxh'
            else:
                new_ext = '.rbxm'
            template = b''
            if new_ext == '.rbxh':
                sibling = os.path.join(os.path.dirname(src), filename + '.rbxh')
                if os.path.isfile(sibling) and os.path.abspath(sibling) != os.path.abspath(src):
                    with open(sibling, 'rb') as f:
                        template = f.read()
            output_data = convert_roblox_file(content, ext, new_ext, template)
            output_path = os.path.join(os.path.dirname(src), f'{filename}_converted{new_ext}')
            with open(output_path, 'wb') as f:
                f.write(output_data)
            messagebox.showinfo(UI_TEXT['x11'], UI_TEXT['z11'].format(p0=os.path.basename(output_path), p1=human_size(len(output_data))), parent=self)
            self._console_log(UI_TEXT['a12'].format(p0=output_path))
        except Exception as e:
            messagebox.showerror(UI_TEXT['x11'], UI_TEXT['r11'].format(p0=e), parent=self)
    def _cache_type_matches(self, it, selected):
        cat = str(it.kind or '').split(' ', 1)[0].strip().lower()
        selected = str(selected).strip().lower()
        if selected == 'mesh':
            return cat == 'mesh'
        if selected == 'model/rbxm':
            return cat in {'model', 'rbxm', 'rbxl', 'rbxl (place)'}
        if selected == 'unsupported_animation':
            return cat == 'unsupported_animation'
        if selected == 'image':
            return cat in {'image', 'decal', 'texture'}
        if selected == 'audio':
            return cat in {'sound', 'audio'}
        if selected == 'video':
            return cat == 'video'
        if selected == 'font':
            return cat == 'font'
        if selected == 'text':
            return cat in {'text', 'translations', 'translation'}
        if selected == 'unknown':
            return cat == 'unknown'
        return False
    def _open_delete_cache_type(self):
        dlg = tk.Toplevel(self)
        dlg.title('Delete Cache Type')
        dlg.resizable(False, False)
        dlg.transient(self)
        theme_toplevel(dlg)
        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text=UI_TEXT['u23']).pack(anchor='w', pady=(0, 7))
        type_var = tk.StringVar(value='Mesh')
        combo = ttk.Combobox(outer, textvariable=type_var, values=('Mesh', 'Model/RBXM', 'Animation', 'Image', 'Audio', 'Video', 'Font', 'Text', 'Unknown'), state='readonly', width=18)
        combo.pack(fill='x')
        def do_delete():
            selected = type_var.get()
            dlg.destroy()
            self._delete_cache_type(selected)
        btns = ttk.Frame(outer)
        btns.pack(fill='x', pady=(10, 0))
        ttk.Button(btns, text=UI_TEXT['b2'], command=do_delete).pack(side='left')
        ttk.Button(btns, text=UI_TEXT['b3'], command=dlg.destroy).pack(side='right')
        combo.focus_set()
    def _delete_cache_type(self, selected):
        if getattr(self, '_cache_type_busy', False):
            return
        self._cache_type_busy = True
        try:
            self.btn_delete_type.config(state='disabled')
        except Exception:
            pass
        was_running = bool(self.watching)
        if was_running:
            self._stop_watching()
        def scan_worker():
            try:
                if not os.path.isfile(self.db_path):
                    result = ('error', 'rbx-storage.db was not found.')
                else:
                    items = scan_db_once(self.db_path, self.shard_root, set(), None)
                    targets = [it for it in items if self._cache_type_matches(it, selected)]
                    result = ('found', targets)
            except Exception as e:
                result = ('error', str(e))
            self.after(0, lambda r=result: self._delete_cache_type_scan_done(selected, r, was_running))
        threading.Thread(target=scan_worker, daemon=True, name='RoUtils-DeleteTypeScan').start()
    def _delete_cache_type_scan_done(self, selected, result, was_running):
        if result[0] == 'error':
            self._finish_delete_cache_type(('error', result[1]), was_running)
            return
        targets = result[1]
        if not targets:
            self._finish_delete_cache_type(('none', None), was_running)
            return
        try:
            ok = messagebox.askyesno(UI_TEXT['c23'], UI_TEXT['v23'].format(p0=len(targets), p1=selected), parent=self)
        except Exception as e:
            self._finish_delete_cache_type(('error', str(e)), was_running)
            return
        if not ok:
            self._finish_delete_cache_type(('cancel', None), was_running)
            return
        def delete_worker():
            deleted_ids = []
            failed = 0
            try:
                conn = connect_rw(self.db_path)
                try:
                    cur = conn.cursor()
                    cur.execute('BEGIN IMMEDIATE')
                    for it in targets:
                        try:
                            cur.execute('DELETE FROM files WHERE id=?', (it.id_bytes,))
                            if cur.rowcount:
                                deleted_ids.append(it)
                        except Exception:
                            failed += 1
                    conn.commit()
                finally:
                    conn.close()
                for it in deleted_ids:
                    try:
                        spath = shard_path(self.shard_root, it.hash)
                        if os.path.isfile(spath):
                            os.remove(spath)
                    except Exception:
                        failed += 1
                self.after(0, lambda: self._finish_delete_cache_type(('ok', len(deleted_ids), failed, deleted_ids, selected), was_running))
            except Exception as e:
                self.after(0, lambda e=e: self._finish_delete_cache_type(('error', str(e)), was_running))
        threading.Thread(target=delete_worker, daemon=True, name='RoUtils-DeleteTypeDelete').start()
    def _finish_delete_cache_type(self, result, was_running):
        try:
            kind = result[0]
            if kind == 'none':
                messagebox.showinfo(UI_TEXT['c23'], UI_TEXT['w23'], parent=self)
            elif kind == 'cancel':
                pass
            elif kind == 'ok':
                _, deleted, failed, targets, selected = result
                for it in targets:
                    self.seen_hashes.discard(it.hash)
                    self.items_by_iid.pop(it.hash, None)
                    self.items_by_hash.pop(it.hash, None)
                    for iid in self.tree.get_children(''):
                        try:
                            vals = self.tree.item(iid, 'values')
                            if len(vals) > 2 and str(vals[2]) == str(it.hash):
                                self.tree.delete(iid)
                                break
                        except Exception:
                            pass
                self._update_status()
                msg = f'Deleted {deleted} {selected} cache(s).'
                if failed:
                    msg += f'\nFailed: {failed}'
                messagebox.showinfo(UI_TEXT['c23'], msg, parent=self)
            else:
                messagebox.showerror(UI_TEXT['c23'], str(result[1]), parent=self)
        except Exception as e:
            try:
                messagebox.showerror(UI_TEXT['c23'], str(e), parent=self)
            except Exception:
                pass
        finally:
            self._cache_type_busy = False
            try:
                self.btn_delete_type.config(state='normal')
            except Exception:
                pass
            if was_running and (not self.watching):
                self._start_watching()
    def _cache_type_label(self, result):
        return 'selected type'
    def _dump_blob_body(self, blob):
        meta = parse_rbxh(blob)
        body = meta.get('body') or b''
        if not body:
            return (b'', meta)
        try:
            body = _maybe_gunzip(body, meta.get('headers') or {})
        except Exception:
            pass
        try:
            body = decompress_if_needed(body)
        except Exception:
            pass
        return (body, meta)
    def _dump_image_payload(self, body):
        try:
            label, off = find_embedded_image(body)
            if off > 0:
                body = body[off:]
            img = Image.open(io.BytesIO(body))
            out = io.BytesIO()
            fmt = (img.format or 'PNG').upper()
            if fmt == 'JPEG':
                ext = '.jpg'
                img.save(out, format='JPEG')
            elif fmt == 'WEBP':
                ext = '.webp'
                img.save(out, format='WEBP')
            elif fmt == 'GIF':
                ext = '.gif'
                img.save(out, format='GIF')
            else:
                ext = '.png'
                if img.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P'):
                    img = img.convert('RGBA')
                img.save(out, format='PNG')
            return (out.getvalue(), ext)
        except Exception:
            return (None, None)
    def _video_payload_from_body(self, it, body, meta):
        if not body:
            return (None, None)
        headers = meta.get('headers') or {}
        content_type = next((str(value or '').lower() for key, value in headers.items() if str(key).lower() == 'content-type'), '')
        kind = str(getattr(it, 'kind', '') or '').lower()
        if body[:4] == b'\x1aE\xdf\xa3':
            return (body, '.webm')
        if len(body) >= 12 and body[4:8] == b'ftyp':
            return (body, '.mp4')
        is_hls = body[:256].lstrip().lower().startswith(b'#extm3u') or 'm3u' in kind or 'mpegurl' in content_type
        if is_hls:
            try:
                resolved = self._download_hls_video(body, getattr(it, 'url', ''), it)
                if resolved:
                    if len(resolved) >= 12 and resolved[4:8] == b'ftyp':
                        return (resolved, '.mp4')
                    if resolved[:4] == b'\x1aE\xdf\xa3':
                        return (resolved, '.webm')
                    return (resolved, '.ts')
            except Exception:
                return (body, '.m3u8')
        if 'webm' in kind or 'video/webm' in content_type:
            return (body, '.webm')
        if 'mp4' in kind or 'video/mp4' in content_type:
            return (body, '.mp4')
        if 'mkv' in kind or 'matroska' in content_type:
            return (body, '.mkv')
        if 'm4v' in kind or 'x-m4v' in content_type:
            return (body, '.m4v')
        if 'mov' in kind or 'quicktime' in content_type:
            return (body, '.mov')
        return (None, None)
    def _dump_one_cache(self, it, dump_root, include_video=False):
        blob = self._fetch_full_blob(it)
        if not blob:
            return False
        body, meta = self._dump_blob_body(blob)
        if not body:
            return False
        cat = str(it.kind or 'Unknown').split(' ', 1)[0].strip()
        cat_low = cat.lower()
        folder = 'Unknown'
        payload = body
        ext = '.bin'
        if cat_low == 'mesh':
            folder, ext = ('Meshes', '.obj')
            try:
                obj = convert(body)
            except Exception:
                obj = None
            if not obj:
                return False
            payload = obj.encode('utf-8')
        elif cat_low in {'model', 'rbxm', 'rbxl', 'rbxl (place)'}:
            folder = 'Model-RBXM'
            out = self._rbxm_body(it)
            if out:
                payload, is_binary = out
                ext = '.rbxm' if is_binary else '.rbxmx'
            else:
                ext = '.rbxh'
                payload = blob
        elif cat_low == 'unsupported_animation':
            folder = 'Animations'
            out = self._rbxm_body(it)
            if out:
                payload, is_binary = out
                ext = '.rbxm' if is_binary else '.rbxmx'
            else:
                ext = '.bin'
        elif cat_low in {'image', 'decal', 'texture'}:
            folder = 'Images'
            img_payload, img_ext = self._dump_image_payload(body)
            if img_payload:
                payload, ext = (img_payload, img_ext)
            else:
                ext = '.ktx2' if b'KTX 20' in body[:64] else '.ktx' if b'KTX 11' in body[:64] else '.bin'
        elif cat_low in {'sound', 'audio'}:
            folder = 'Audios'
            lbl = str(it.kind).lower()
            if 'ogg' in lbl or body.startswith(b'OggS'):
                ext = '.ogg'
            elif 'wav' in lbl or (len(body) >= 12 and body[:4] == b'RIFF' and (body[8:12] == b'WAVE')):
                ext = '.wav'
            elif body.startswith(b'ID3'):
                ext = '.mp3'
            else:
                ext = '.bin'
        elif cat_low == 'font':
            folder, ext = ('Fonts', '.ttf')
            if b'OTTO' in body[:4]:
                ext = '.otf'
        elif cat_low in {'translations', 'translation'}:
            folder, ext = ('Translations', '.json')
        elif cat_low == 'text':
            folder, ext = ('Text', '.txt')
        elif cat_low == 'video':
            if not include_video:
                return False
            folder = 'Videos'
            payload, ext = self._video_payload_from_body(it, body, meta)
            if not payload or not ext:
                return False
        elif cat_low == 'compressed':
            folder, ext = ('Compressed', '.bin')
        out_dir = os.path.join(dump_root, folder)
        os.makedirs(out_dir, exist_ok=True)
        name = _sanitize_filename_for_windows(it.name or it.hash) or it.hash
        path = os.path.join(out_dir, f'{name}_{it.hash}{ext}')
        with open(path, 'wb') as f:
            f.write(payload)
        return True
    def _dump_all_caches(self):
        dump_root = os.path.abspath(os.path.join(DATA_DIR, 'Dump'))
        self._last_dump_folder = dump_root
        self._console_select_tab(UI_TEXT['u5'])
        if getattr(self, '_dump_caches_running', False):
            self._console_log(UI_TEXT['x23'])
            return
        os.makedirs(dump_root, exist_ok=True)
        self._console_log(UI_TEXT['m1'])
        self._console_log(UI_TEXT['y23'])
        self._console_log(UI_TEXT['z23'].format(p0=self.db_path))
        self._console_log(UI_TEXT['a24'].format(p0=dump_root))
        self._dump_caches_running = True
        self._dump_caches_prompt_pending = True
        self._console_log(UI_TEXT['q19'])
        try:
            self.after(120, lambda: self.console_entry.focus_set() if hasattr(self, 'console_entry') and self.console_entry.winfo_exists() else None)
        except Exception:
            pass
    def _clear_storage_now(self):
        was = self.watching
        if was:
            self._stop_watching()
        deleted_db = False
        try:
            if os.path.isfile(self.db_path):
                os.remove(self.db_path)
                deleted_db = True
        except Exception:
            pass
        deleted_shards = 0
        try:
            if os.path.isdir(self.shard_root):
                for a in os.listdir(self.shard_root):
                    ap = os.path.join(self.shard_root, a)
                    if os.path.isdir(ap) and len(a) == 2:
                        for f in os.listdir(ap):
                            fp = os.path.join(ap, f)
                            try:
                                if os.path.isfile(fp):
                                    os.remove(fp)
                                    deleted_shards += 1
                            except Exception:
                                pass
        except Exception:
            pass
        self.seen_hashes.clear()
        self.items_by_iid.clear()
        self.items_by_hash.clear()
        self.tree.delete(*self.tree.get_children())
        self._update_status()
        self._console_log(UI_TEXT['n24'].format(p0=deleted_shards, p1='yes' if deleted_db else 'no'))
        messagebox.showinfo(UI_TEXT['b23'], UI_TEXT['o24'].format(p0=deleted_shards, p1='yes' if deleted_db else 'no'))
        if was:
            self._start_watching()
    def _install_selected_db(self, source_db):
        local = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
        roblox_dir = os.path.join(local, 'Roblox')
        target = os.path.join(roblox_dir, 'rbx-storage.db')
        sidecars = [target, target + '-shm', target + '-wal', os.path.join(roblox_dir, 'rbx-storage.id')]
        os.makedirs(roblox_dir, exist_ok=True)
        source_db = os.path.abspath(source_db)
        if not os.path.isfile(source_db):
            raise FileNotFoundError(f'DB file not found: {source_db}')
        with tempfile.NamedTemporaryFile(prefix='routils_db_install_', suffix='.db', delete=False) as tf:
            temp_source = tf.name
        try:
            shutil.copy2(source_db, temp_source)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute('PRAGMA schema_version').fetchone()
            conn.close()
            backup_dir = tempfile.mkdtemp(prefix='routils_db_backup_')
            backups = {}
            try:
                for idx, path in enumerate(sidecars):
                    if os.path.isfile(path):
                        bp = os.path.join(backup_dir, f'{idx}.bak')
                        shutil.copy2(path, bp)
                        backups[path] = bp
                deleted = []
                try:
                    for path in sidecars:
                        if os.path.exists(path):
                            try:
                                os.remove(path)
                            except PermissionError as e:
                                raise PermissionError(f"Cannot delete '{os.path.basename(path)}'. Roblox or another program may be using it.") from e
                            except OSError as e:
                                raise OSError(f"Cannot delete '{os.path.basename(path)}': {e}") from e
                            deleted.append(path)
                    shutil.copy2(temp_source, target)
                except Exception:
                    try:
                        if os.path.isfile(target) and target not in backups:
                            os.remove(target)
                    except Exception:
                        pass
                    for path, bp in backups.items():
                        try:
                            if os.path.exists(path):
                                os.remove(path)
                            shutil.copy2(bp, path)
                        except Exception:
                            pass
                    raise
            finally:
                shutil.rmtree(backup_dir, ignore_errors=True)
        finally:
            try:
                os.remove(temp_source)
            except Exception:
                pass
        self.db_path = target
        self.shard_root = os.path.join(roblox_dir, 'rbx-storage')
        if getattr(self, 'db_label', None) is not None:
            self.db_label.config(text=self.db_path)
        self._reset_seen(clear_list=True)
        return target
    def _choose_db(self):
        path = filedialog.askopenfilename(title=UI_TEXT['p24'], filetypes=[(UI_TEXT['o8'], '*.db'), (UI_TEXT['q24'], '*.*')])
        if not path:
            return
        was_watching = self.watching
        if was_watching:
            self._stop_watching()
        try:
            self._install_selected_db(path)
        except Exception as e:
            messagebox.showerror(UI_TEXT['r24'], UI_TEXT['s24'].format(p0=e))
            if was_watching:
                self._start_watching()
            return
        if was_watching:
            self._start_watching()
        messagebox.showinfo(UI_TEXT['r24'], UI_TEXT['t24'])
    def _choose_shard_root(self):
        d = filedialog.askdirectory(title=UI_TEXT['u24'])
        if not d:
            return
        self.shard_root = d
        self._reset_seen(clear_list=False)
    def _toggle_watch(self):
        if self.watching:
            self._stop_watching()
            self._watch_loading_active = False
            self._watch_initial_scan_done.clear()
            if hasattr(self, '_watch_loading_label'):
                self._watch_loading_label.config(text=UI_TEXT['m1'])
            self._console_log(UI_TEXT['e20'])
            return
        self._watch_loading_active = True
        self._watch_initial_scan_done.clear()
        self.toggle_btn.config(state='disabled', text=UI_TEXT['v5'])
        if hasattr(self, '_watch_loading_label'):
            self._watch_loading_label.config(text=UI_TEXT['v5'])
        def begin():
            started = False
            try:
                started = self._start_watching()
                if started:
                    self._console_log(UI_TEXT['c20'])
                else:
                    self._console_log(UI_TEXT['d20'])
            except Exception as e:
                self._console_log(UI_TEXT['v24'].format(p0=e))
            if not started:
                self._watch_loading_active = False
                try:
                    self.toggle_btn.config(state='normal', text=UI_TEXT['d23'])
                    if hasattr(self, '_watch_loading_label'):
                        self._watch_loading_label.config(text=UI_TEXT['m1'])
                except Exception:
                    pass
        self.after(40, begin)
    def _start_watching(self):
        if not os.path.isfile(self.db_path):
            self._update_status()
            return False
        self.stop_event.clear()
        self.watching = True
        if hasattr(self, 'toggle_btn') and (not getattr(self, '_watch_loading_active', False)):
            self.toggle_btn.config(state='normal', text=UI_TEXT['w24'])
        self._update_status()
        self._launch_scan_loop()
        return True
    def _stop_watching(self):
        self.stop_event.set()
        self.watching = False
        if hasattr(self, 'toggle_btn'):
            self.toggle_btn.config(text=UI_TEXT['d23'])
        self._update_status()
    def _launch_scan_loop(self):
        if self.scan_thread and self.scan_thread.is_alive():
            return
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()
    def _update_scan_max_rows_value(self, *_):
        try:
            self._scan_max_rows_value = max(0, int(self.max_rows.get()))
        except Exception:
            self._scan_max_rows_value = 0
    def _scan_loop(self):
        first_scan = True
        while not self.stop_event.is_set():
            if getattr(self, '_resize_active', False):
                self.stop_event.wait(0.12)
                continue
            try:
                max_rows = self._scan_max_rows_value
                items = scan_db_once(self.db_path, self.shard_root, self.seen_hashes, None if max_rows <= 0 else max_rows, on_batch=self.new_items_q.put, batch_size=800)
                if items:
                    self.new_items_q.put(items)
            except Exception as e:
                self._console_log(UI_TEXT['x24'].format(p0=e))
            finally:
                if first_scan:
                    first_scan = False
                    self._watch_initial_scan_done.set()
            self.stop_event.wait(WATCH_INTERVAL_SEC)
    def _drain_queue(self):
        if getattr(self, '_resize_active', False):
            self.after(max(120, UI_QUEUE_INTERVAL_MS), self._drain_queue)
            return
        processed = 0
        try:
            while processed < 16:
                items = self.new_items_q.get_nowait()
                self._insert_items(items)
                processed += 1
        except queue.Empty:
            pass
        if getattr(self, '_watch_loading_active', False) and self._watch_initial_scan_done.is_set() and self.new_items_q.empty() and (not self._tree_insert_pending) and (self._tree_insert_pending_job is None) and (self._filter_render_phase is None):
            self._watch_loading_active = False
            try:
                self.toggle_btn.config(state='normal', text=UI_TEXT['w24'] if self.watching else UI_TEXT['d23'])
                if hasattr(self, '_watch_loading_label'):
                    self._watch_loading_label.config(text=UI_TEXT['m1'])
            except Exception:
                pass
        self.after(UI_QUEUE_INTERVAL_MS, self._drain_queue)
    def _should_display(self, it: ScanItem, filt: str, hide_tickets=None, type_filter=None) -> bool:
        if hide_tickets is None:
            hide_tickets = self.hide_tickets.get()
        if hide_tickets and it.is_ticket:
            return False
        if type_filter is None:
            type_filter = self.type_filter.get()
        if type_filter != 'All':
            cat = it.kind.split(' ', 1)[0]
            matcher = TYPE_FILTER_MATCHERS.get(type_filter)
            if matcher is not None and (not matcher(cat)):
                return False
        if filt:
            row_join = getattr(it, 'search_text', '')
            if not row_join:
                size_text = getattr(it, 'size_text', '') or human_size(it.size)
                row_join = ' '.join((it.time, it.name, it.hash, size_text, it.kind, it.src)).lower()
            if filt not in row_join:
                return False
        return True
    def _tree_insert_many(self, rows):
        if not rows or not hasattr(self, 'tree'):
            return
        rows_var = f'::routils_cache_rows_{id(self)}'
        tree_var = f'::routils_cache_widget_{id(self)}'
        try:
            self.tree.tk.call('set', rows_var, tuple(rows))
            self.tree.tk.call('set', tree_var, str(self.tree))
            script = f'set __routils_tree ${tree_var}\nforeach __routils_row ${rows_var} {{\n    set __routils_id [lindex $__routils_row 0]\n    set __routils_values [lindex $__routils_row 1]\n    if {{[catch {{$__routils_tree insert {{}} end -id $__routils_id -values $__routils_values}}]}} {{\n        if {{[$__routils_tree exists $__routils_id]}} {{$__routils_tree item $__routils_id -values $__routils_values}}\n    }}\n}}\nunset {rows_var}\nunset -nocomplain {tree_var}\n'
            self.tree.tk.eval(script)
        except Exception:
            try:
                self.tree.tk.call('unset', rows_var)
            except Exception:
                pass
            for iid, values in rows:
                try:
                    self.tree.insert('', 'end', iid=iid, values=values)
                except tk.TclError:
                    try:
                        if self.tree.exists(iid):
                            self.tree.item(iid, values=values)
                    except Exception:
                        pass
                except Exception:
                    pass
        finally:
            try:
                self.tree.tk.call('unset', rows_var)
            except Exception:
                pass
    def _insert_items(self, items: List[ScanItem]):
        if not items or getattr(self, '_ui_dispatch_closed', False):
            return
        try:
            self._tree_insert_pending.extend(items)
        except Exception:
            return
        if self._filter_render_phase is None and self._tree_insert_pending_job is None:
            try:
                self._tree_insert_pending_job = self.after(0, self._insert_items_batch)
            except Exception:
                self._tree_insert_pending_job = None
    def _insert_items_batch(self):
        self._tree_insert_pending_job = None
        if getattr(self, '_ui_dispatch_closed', False) or not self._tree_insert_pending:
            self._tree_insert_pending = []
            self._tree_insert_pending_index = 0
            return
        if self._filter_render_phase is not None:
            return
        if getattr(self, '_resize_active', False):
            try:
                self._tree_insert_pending_job = self.after(100, self._insert_items_batch)
            except Exception:
                self._tree_insert_pending_job = None
            return
        if not hasattr(self, 'tree'):
            self._tree_insert_pending = []
            self._tree_insert_pending_index = 0
            return
        pending = self._tree_insert_pending
        index = self._tree_insert_pending_index
        filt = self.filter_text.get().lower().strip()
        hide_tickets = self.hide_tickets.get()
        type_filter = self.type_filter.get()
        batch_rows = []
        batch_items = []
        last_iid = None
        started = time.perf_counter()
        while index < len(pending) and len(batch_rows) < 1200 and (time.perf_counter() - started < 0.025):
            item = pending[index]
            index += 1
            self.items_by_hash[item.hash] = item
            if not self._should_display(item, filt, hide_tickets, type_filter):
                continue
            size_text = getattr(item, 'size_text', '') or human_size(item.size)
            values = (item.time, item.name, item.hash, size_text, item.kind, item.src)
            batch_rows.append((item.hash, values))
            batch_items.append(item)
            last_iid = item.hash
        if batch_rows:
            self._tree_insert_many(batch_rows)
            for item in batch_items:
                self.items_by_iid[item.hash] = item
            self._tree_last_inserted_iid = last_iid
            self._update_status()
        self._tree_insert_pending_index = index
        if index < len(pending):
            try:
                self._tree_insert_pending_job = self.after(1, self._insert_items_batch)
            except Exception:
                self._tree_insert_pending_job = None
        else:
            self._tree_insert_pending = []
            self._tree_insert_pending_index = 0
            if self.autoscroll.get() and last_iid and (not getattr(self, '_watch_loading_active', False)) and self.new_items_q.empty():
                try:
                    self.tree.see(last_iid)
                except Exception:
                    pass
    def _safe_apply_filter(self):
        try:
            self._apply_filter()
        except tk.TclError:
            try:
                self.after(30, self._safe_apply_filter)
            except Exception:
                pass
        except Exception as exc:
            try:
                self._console_log(UI_TEXT['y24'].format(p0=exc))
            except Exception:
                pass
    def _apply_filter(self):
        if not hasattr(self, 'tree'):
            return
        self._filter_render_generation += 1
        generation = self._filter_render_generation
        if self._filter_render_job is not None:
            try:
                self.after_cancel(self._filter_render_job)
            except Exception:
                pass
            self._filter_render_job = None
        if self._tree_insert_pending_job is not None:
            try:
                self.after_cancel(self._tree_insert_pending_job)
            except Exception:
                pass
            self._tree_insert_pending_job = None
        self._filter_render_text = self.filter_text.get().lower().strip()
        self._filter_render_snapshot = list(self.items_by_hash.values())
        self._filter_render_index = 0
        try:
            self._filter_clear_iids = list(self.tree.get_children(''))
        except Exception:
            self._filter_clear_iids = []
        self._filter_clear_index = 0
        self._filter_render_phase = 'clear'
        self._filter_render_last_iid = None
        try:
            self.tree.selection_remove(self.tree.selection())
        except Exception:
            pass
        self.items_by_iid.clear()
        try:
            self._filter_render_job = self.after(0, lambda g=generation: self._apply_filter_batch(g))
        except Exception:
            self._filter_render_job = None
    def _apply_filter_batch(self, generation=None):
        self._filter_render_job = None
        if generation is None:
            generation = self._filter_render_generation
        if generation != self._filter_render_generation or getattr(self, '_ui_dispatch_closed', False):
            return
        if not hasattr(self, 'tree'):
            self._filter_render_phase = None
            return
        if getattr(self, '_resize_active', False):
            try:
                self._filter_render_job = self.after(100, lambda g=generation: self._apply_filter_batch(g))
            except Exception:
                self._filter_render_job = None
            return
        if self._filter_render_phase == 'clear':
            stop = min(self._filter_clear_index + 600, len(self._filter_clear_iids))
            chunk = self._filter_clear_iids[self._filter_clear_index:stop]
            if chunk:
                try:
                    self.tree.delete(*chunk)
                except Exception:
                    pass
                self._filter_clear_index = stop
                try:
                    self._filter_render_job = self.after(1, lambda g=generation: self._apply_filter_batch(g))
                except Exception:
                    self._filter_render_job = None
                return
            self._filter_render_phase = 'insert'
            try:
                self._filter_render_job = self.after(1, lambda g=generation: self._apply_filter_batch(g))
            except Exception:
                self._filter_render_job = None
            return
        if self._filter_render_phase != 'insert':
            return
        snapshot = self._filter_render_snapshot
        index = self._filter_render_index
        processed = 0
        started = time.perf_counter()
        hide_tickets = self.hide_tickets.get()
        type_filter = self.type_filter.get()
        batch_rows = []
        batch_items = []
        while index < len(snapshot) and processed < 2200 and (time.perf_counter() - started < 0.022):
            item = snapshot[index]
            index += 1
            processed += 1
            if not self._should_display(item, self._filter_render_text, hide_tickets, type_filter):
                continue
            size_text = getattr(item, 'size_text', '') or human_size(item.size)
            values = (item.time, item.name, item.hash, size_text, item.kind, item.src)
            batch_rows.append((item.hash, values))
            batch_items.append(item)
            self._filter_render_last_iid = item.hash
        if batch_rows:
            self._tree_insert_many(batch_rows)
            for item in batch_items:
                self.items_by_iid[item.hash] = item
        self._filter_render_index = index
        if index < len(snapshot):
            try:
                self._filter_render_job = self.after(1, lambda g=generation: self._apply_filter_batch(g))
            except Exception:
                self._filter_render_job = None
            return
        self._filter_render_phase = None
        self._filter_render_snapshot = []
        self._filter_clear_iids = []
        try:
            if self.autoscroll.get() and self._filter_render_last_iid:
                self.tree.see(self._filter_render_last_iid)
        except Exception:
            pass
        self._update_status()
        if self._tree_insert_pending and self._tree_insert_pending_job is None:
            try:
                self._tree_insert_pending_job = self.after(1, self._insert_items_batch)
            except Exception:
                self._tree_insert_pending_job = None
    def _apply_stay_on_top(self):
        self._app_focus_changed()
    def _apply_show_lines(self):
        self.viewport_3d.show_wireframe.set(self.show_lines.get())
        if hasattr(self, '_titlebar'):
            try:
                self._titlebar.configure(bg=_CURRENT_PALETTE['bg_dark'])
                self._titlebar_canvas.configure(bg=_CURRENT_PALETTE['bg_dark'])
                for child in self._titlebar.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=_CURRENT_PALETTE['bg_dark'], fg=_CURRENT_PALETTE['fg'])
            except Exception:
                pass
        if self.viewport_3d.winfo_ismapped():
            self.viewport_3d.draw_frame()
    def _show_details(self):
        try:
            self._cancel_image_preview()
            sel = self.tree.selection()
            if not sel:
                return
            iid = sel[0]
            if not self.tree.exists(iid):
                return
            it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
            if not it:
                return
            self.details_text.configure(state='normal')
            self.details_text.delete('1.0', 'end')
            lines = [f'Hash:    {it.hash}', f'Name:    {it.name}', f'Time:    {it.time}', f'Source:  {it.src}', f'Wrapped: {it.wrapped}', f'Size:    {human_size(it.size)}', f'Type:    {it.kind}']
            if len(sel) > 1:
                lines.append(f'Selection: {len(sel)} rows (actions apply to all selected)')
            if it.content_type:
                lines.append(f'Content-Type: {it.content_type}')
            lines.extend((f'URL:     {it.url}', ''))
            if it.header_text:
                lines.extend(('RBXH headers (best-effort):', it.header_text.strip(), ''))
            if it.is_ticket:
                lines.append('Note: This is a signed-URL ticket cached by the client before fetching the real asset.')
            self.details_text.insert('1.0', '\n'.join(lines))
            self.details_text.configure(state='disabled')
        except tk.TclError:
            return
    def _update_preview(self):
        try:
            sel = self.tree.selection()
            if not sel:
                self.viewport_3d.hide()
                return
            iid = sel[0]
            if not self.tree.exists(iid):
                self.viewport_3d.hide()
                return
            it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
            if not it:
                self.viewport_3d.hide()
                return
            blob = self._fetch_full_blob(it)
            if not blob:
                self.viewport_3d.hide()
                return
            meta = parse_rbxh(blob)
            body = meta.get('body') or b''
            cat = it.kind.split(' ', 1)[0]
            is_mesh = cat == 'Mesh'
            scan_end = min(len(body), 262144)
            is_anim = cat == 'Animation' or (cat in ('RBXM', 'Model') and any((body.find(marker, 0, scan_end) != -1 for marker in (b'Keyframe', b'CurveAnimation', b'KeyframeSequence', b'AnimationClip'))))
            is_audio = cat == 'Sound'
            is_model = cat in ('Model', 'RBXM', 'rbxl (place)')
            if not (is_mesh or is_anim or is_audio or is_model) or is_anim:
                self.viewport_3d.hide()
                return
            self._close_animation_preview()
            temp_pkg_path = os.path.join(TEMP_EMU_DIR, f'preview_{it.hash}.bin')
            try:
                with open(temp_pkg_path, 'wb') as f:
                    f.write(body)
            except OSError:
                self.viewport_3d.hide()
                return
            self.viewport_3d.set_asset_data_from_temp(temp_pkg_path, is_anim=is_anim, is_mesh=is_mesh, is_model=is_model, is_audio=is_audio)
            if is_mesh:
                self.viewport_3d.show(is_anim=False, mode_label='Mesh View')
            elif is_model:
                self.viewport_3d.show(is_anim=False, mode_label='Model View')
            elif is_audio:
                self.viewport_3d.show(is_anim=False, mode_label='Audio View')
        except (tk.TclError, FileNotFoundError, OSError):
            try:
                self.viewport_3d.hide()
            except Exception:
                pass
    def _close_animation_preview(self):
        win = getattr(self, '_animation_preview_win', None)
        if win is not None:
            try:
                if win.winfo_exists():
                    win.withdraw()
            except Exception:
                pass
    def _update_displaycolumns(self, save: bool=True):
        cols = [c for c in self.columns if self._col_vars[c].get()]
        if not cols:
            first = self.columns[0]
            self._col_vars[first].set(True)
            cols = [first]
        self.tree.config(displaycolumns=cols)
        for c in cols:
            w = self.tree.column(c, width=None)
            self.tree.column(c, width=w)
        if save:
            self._save_settings()
    def _on_tree_select(self, event):
        self._clear_tree_hover()
        self._schedule_ui('tree_select', 20, self._update_selected_view)
    def _update_selected_view(self):
        self._show_details()
        self._update_preview()
    def _clear_tree_hover(self):
        iid = self._tree_hover_iid
        self._tree_hover_iid = None
        if not iid:
            return
        try:
            if not self.tree.exists(iid):
                return
            tags = list(self.tree.item(iid, 'tags'))
            if 'hover' in tags:
                tags.remove('hover')
                self.tree.item(iid, tags=tags)
        except tk.TclError:
            pass
    def _on_tree_leave(self, event):
        self._cancel_image_preview()
        self._clear_tree_hover()
    def _on_tree_right_click(self, event):
        self._cancel_image_preview()
        region = self.tree.identify_region(event.x, event.y)
        if region == 'heading':
            try:
                self._colmenu.tk_popup(event.x_root, event.y_root)
            finally:
                self._colmenu.grab_release()
            return
        row = self.tree.identify_row(event.y)
        if row and (not self.tree.exists(row)):
            row = ''
        if row:
            sel = self.tree.selection()
            if not self.tree.exists(row):
                return
            if row not in sel:
                self.tree.selection_set(row)
            items = self._get_selected_items()
            if not items:
                return
            any_model = any((i.kind.split(' ', 1)[0] in ('RBXM', 'Model') for i in items))
            any_mesh = any((i.kind.split(' ', 1)[0] == 'Mesh' for i in items))
            any_img = any((i.kind.split(' ', 1)[0] in ('Image', 'Decal', 'Texture') for i in items))
            any_video = any((i.kind.split(' ', 1)[0] == 'Video' for i in items))
            self._ctx.entryconfigure(self._ctx_rbxm_index, state=tk.NORMAL if any_model else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_obj_index, state=tk.NORMAL if any_mesh else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_img_index, state=tk.NORMAL if any_img else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_video_index, state=tk.NORMAL if any_video else tk.DISABLED)
            try:
                self._ctx.tk_popup(event.x_root, event.y_root)
            finally:
                self._ctx.grab_release()
    def _copy_selected_hash(self):
        items = self._get_selected_items()
        if not items:
            return
        joined = '\n'.join((it.hash for it in items))
        self.clipboard_clear()
        self.clipboard_append(joined)
        messagebox.showinfo(UI_TEXT['z24'], UI_TEXT['a25'].format(p0=len(items)))
    def _on_tree_motion(self, event):
        try:
            row = self.tree.identify_row(event.y)
            if row and (not self.tree.exists(row)):
                row = ''
            self._hover_preview_xy = (event.x_root, event.y_root)
            if row != self._tree_hover_iid:
                self._clear_tree_hover()
                if row and self.tree.exists(row):
                    tags = list(self.tree.item(row, 'tags'))
                    if 'hover' not in tags:
                        tags.append('hover')
                        self.tree.item(row, tags=tags)
                    self._tree_hover_iid = row
            if row == self._hover_preview_iid:
                return
            self._cancel_image_preview()
            if not row or not self.tree.exists(row):
                return
            it = self.items_by_iid.get(row) or self.items_by_hash.get(row)
            if not it:
                return
            cat = it.kind.split(' ', 1)[0]
            if cat in ('Image', 'Decal', 'Texture'):
                self._hover_preview_iid = row
                self._hover_preview_job = self.after(1200, self._show_image_preview)
        except tk.TclError:
            self._tree_hover_iid = None
            self._hover_preview_iid = None
    def _cancel_image_preview(self):
        if self._hover_preview_job:
            try:
                self.after_cancel(self._hover_preview_job)
            except Exception:
                pass
            self._hover_preview_job = None
        self._hover_preview_iid = None
        if self._img_preview_fade_job:
            try:
                self.after_cancel(self._img_preview_fade_job)
            except Exception:
                pass
            self._img_preview_fade_job = None
        if self._img_preview_win and self._img_preview_win.winfo_exists():
            self._fade_preview(0.0)
    def _show_image_preview(self):
        self._hover_preview_job = None
        iid = self._hover_preview_iid
        if not iid:
            return
        try:
            if not self.tree.exists(iid):
                self._hover_preview_iid = None
                return
        except tk.TclError:
            self._hover_preview_iid = None
            return
        it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
        if not it:
            return
        blob = self._fetch_full_blob(it)
        if not blob:
            return
        meta = parse_rbxh(blob)
        body = meta.get('body') or b''
        _, off = find_embedded_image(body)
        if off > 0:
            body = body[off:]
        try:
            img = Image.open(io.BytesIO(body))
            img.thumbnail((256, 256))
            photo = ImageTk.PhotoImage(img)
        except Exception:
            return
        if not self._img_preview_win or not self._img_preview_win.winfo_exists():
            self._img_preview_win = tk.Toplevel(self)
            self._img_preview_win._skip_custom_chrome = True
            self._img_preview_win._skip_popup_centering = True
            theme_toplevel(self._img_preview_win)
            self._img_preview_label = ttk.Label(self._img_preview_win)
            self._img_preview_label.pack()
        if self._img_preview_fade_job:
            try:
                self.after_cancel(self._img_preview_fade_job)
            except Exception:
                pass
            self._img_preview_fade_job = None
        self._img_preview_photo = photo
        self._img_preview_label.configure(image=photo)
        x, y = self._hover_preview_xy
        self._img_preview_win.geometry(f'+{x + 16}+{y + 16}')
        try:
            self._img_preview_win.attributes('-alpha', 0.0)
        except Exception:
            pass
        self._img_preview_win.deiconify()
        self._img_preview_win.lift()
        self._fade_preview(1.0)
    def _fade_preview(self, target: float, step: float=0.12):
        if not self._img_preview_win or not self._img_preview_win.winfo_exists():
            return
        try:
            cur = float(self._img_preview_win.attributes('-alpha'))
        except Exception:
            self._img_preview_win.attributes('-alpha', target)
            if target == 0.0:
                self._img_preview_win.withdraw()
            return
        if target > cur and cur >= target - step or (target < cur and cur <= target + step):
            self._img_preview_win.attributes('-alpha', target)
            if target == 0.0:
                self._img_preview_win.withdraw()
            self._img_preview_fade_job = None
            return
        cur += step if target > cur else -step
        self._img_preview_win.attributes('-alpha', cur)
        self._img_preview_fade_job = self.after(25, self._fade_preview, target, step)
    def _fetch_full_blob(self, it: ScanItem) -> Optional[bytes]:
        if it is None or not getattr(it, 'hash', None):
            return None
        conn = None
        row = None
        try:
            if not os.path.isfile(self.db_path):
                return read_shard_bytes(self.shard_root, it.hash)
            conn = connect_ro(self.db_path)
            cur = conn.cursor()
            cur.execute('SELECT content FROM files WHERE id=?', (it.id_bytes,))
            row = cur.fetchone()
        except (FileNotFoundError, sqlite3.Error, OSError):
            row = None
        except Exception:
            row = None
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
        if row is not None and row[0] is not None:
            return row[0]
        return read_shard_bytes(self.shard_root, it.hash)
    def _export_selected_full(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['b25'], UI_TEXT['c25'])
            return
        if len(items) == 1:
            self._export_one_full(items[0])
            return
        directory = filedialog.askdirectory(title=UI_TEXT['d25'])
        if not directory:
            return
        saved = 0
        for it in items:
            blob = self._fetch_full_blob(it)
            if not blob:
                continue
            ext = '.rbxh' if blob[:4] == RBXH_MAGIC else '.bin'
            path = os.path.join(directory, f'{it.hash}{ext}')
            try:
                with open(path, 'wb') as f:
                    f.write(blob)
                saved += 1
            except Exception:
                pass
        messagebox.showinfo(UI_TEXT['b25'], UI_TEXT['e25'].format(p0=saved, p1=len(items), p2=directory))
    def _export_one_full(self, it):
        blob = self._fetch_full_blob(it)
        if not blob:
            messagebox.showerror(UI_TEXT['b25'], UI_TEXT['f25'])
            return
        ext = '.rbxh' if blob[:4] == RBXH_MAGIC else '.bin'
        default_name = f'{it.hash}{ext}'
        path = filedialog.asksaveasfilename(title=UI_TEXT['g25'], defaultextension=ext, initialfile=default_name, filetypes=[(UI_TEXT['h25'], '*.rbxh'), (UI_TEXT['i25'], '*.bin'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        try:
            with open(path, 'wb') as f:
                f.write(blob)
            messagebox.showinfo(UI_TEXT['b25'], UI_TEXT['j25'].format(p0=path))
        except Exception as e:
            messagebox.showerror(UI_TEXT['b25'], UI_TEXT['k25'].format(p0=e))
    def _export_selected_rbxm(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['l25'], UI_TEXT['c25'])
            return
        if len(items) > 1:
            directory = filedialog.askdirectory(title=UI_TEXT['m25'])
            if not directory:
                return
            saved = 0
            for it in items:
                out = self._rbxm_body(it)
                if not out:
                    continue
                ext = '.rbxm' if out[1] else '.rbxmx'
                path = os.path.join(directory, f'{it.hash}{ext}')
                try:
                    with open(path, 'wb') as f:
                        f.write(out[0])
                    saved += 1
                except Exception:
                    pass
            messagebox.showinfo(UI_TEXT['l25'], UI_TEXT['n25'].format(p0=saved, p1=len(items), p2=directory))
            return
        it = items[0]
        out = self._rbxm_body(it)
        if not out:
            return
        body, is_binary = out
        ext = '.rbxm' if is_binary else '.rbxmx'
        default_name = f'{it.hash}{ext}'
        path = filedialog.asksaveasfilename(title=UI_TEXT['l25'], defaultextension=ext, initialfile=default_name, filetypes=[(UI_TEXT['o25'], f'*{ext}'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        try:
            with open(path, 'wb') as f:
                f.write(body)
            messagebox.showinfo(UI_TEXT['l25'], UI_TEXT['p25'].format(p0=path))
        except Exception as e:
            messagebox.showerror(UI_TEXT['l25'], UI_TEXT['k25'].format(p0=e))
    def _export_selected_mesh_obj(self):
        items = [it for it in self._get_selected_items() if (it.kind or '').split(' ', 1)[0] == 'Mesh']
        if not items:
            messagebox.showinfo(UI_TEXT['m23'], UI_TEXT['q25'], parent=self)
            return
        directory = None
        if len(items) > 1:
            directory = filedialog.askdirectory(title=UI_TEXT['r25'], parent=self)
            if not directory:
                return
        saved = 0
        errors = []
        for it in items:
            try:
                blob = self._fetch_full_blob(it)
                if not blob:
                    raise ValueError('cache blob could not be read')
                if blob[:4] == RBXH_MAGIC:
                    meta = parse_rbxh(blob)
                    data = _maybe_gunzip(meta.get('body') or b'', meta.get('headers') or {})
                else:
                    data = blob
                data = decompress_if_needed(data)
                base = _sanitize_filename_for_windows(os.path.splitext(it.name or it.hash)[0]) or it.hash
                if directory:
                    path = os.path.join(directory, base + '.obj')
                else:
                    path = filedialog.asksaveasfilename(title=UI_TEXT['s25'], parent=self, defaultextension='.obj', initialfile=base + '.obj', filetypes=[(UI_TEXT['t25'], '*.obj'), (UI_TEXT['z7'], '*.*')])
                    if not path:
                        return
                convert(data, path)
                saved += 1
                self._console_log(UI_TEXT['u25'].format(p0=path))
            except Exception as exc:
                errors.append(f'{it.name or it.hash}: {exc}')
        if errors:
            messagebox.showerror(UI_TEXT['m23'], UI_TEXT['v25'] + '\n'.join(errors), parent=self)
        elif saved:
            messagebox.showinfo(UI_TEXT['m23'], UI_TEXT['w25'].format(p0=saved), parent=self)
    def _video_signed_query_values(self, source_url: str) -> Dict[str, str]:
        values = {}
        try:
            raw_query = urlparse(source_url or '').query
            for key, vals in parse_qs(raw_query, keep_blank_values=True).items():
                if vals:
                    values[key.lower()] = vals[0]
        except Exception:
            pass
        return values
    @staticmethod
    def _video_has_placeholders(text: str) -> bool:
        low = str(text or '').lower()
        return any((x in low for x in ('{$__token_}', '{$__token__}', '{$expires}', '{$policy}', '{$signature}', '{$key-pair-id}', '${__token_}', '${expires}', '${policy}', '${signature}', '${key-pair-id}')))
    def _find_video_ticket_urls(self, video_it: ScanItem, manifest: bytes) -> List[str]:
        candidates = []
        manifest_text = manifest.decode('utf-8', 'ignore')
        path_tokens = set()
        for line in manifest_text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                for part in urlparse(line).path.lower().split('/'):
                    if len(part) >= 5:
                        path_tokens.add(part)
            except Exception:
                pass
        ticket_entries = getattr(self, '_video_ticket_entries', None)
        if ticket_entries is None:
            ticket_entries = []
            seen_urls = set()
            conn = None
            try:
                conn = connect_ro(self.db_path)
                cur = conn.cursor()
                cur.execute('SELECT id, content FROM files')
                for id_b, content in cur:
                    h = id_bytes_to_hex(id_b)
                    blob = content if content is not None else read_shard_bytes(self.shard_root, h)
                    if not blob:
                        continue
                    try:
                        meta = parse_rbxh(blob)
                        url = str(meta.get('url') or '')
                        body = meta.get('body') or b''
                        full = meta.get('full_payload') or body
                        is_ticket, _ = detect_ticket(full, url)
                        if not is_ticket:
                            continue
                        found = [url] if url else []
                        found.extend(self._extract_signed_urls_from_bytes(body))
                        found.extend(self._extract_signed_urls_from_bytes(full))
                        for candidate_url in found:
                            if candidate_url.startswith(('http://', 'https://')) and candidate_url not in seen_urls:
                                seen_urls.add(candidate_url)
                                ticket_entries.append(candidate_url)
                    except Exception:
                        continue
            except Exception:
                pass
            finally:
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass
            self._video_ticket_entries = ticket_entries
        for candidate_url in ticket_entries:
            low = candidate_url.lower()
            score = 10 if 'rbxcdn.com' in low else 0
            if any((token in low for token in ('__token_', 'signature', 'key-pair-id', 'policy', 'expires'))):
                score += 20
            try:
                candidate_path = urlparse(candidate_url).path.lower()
                if path_tokens:
                    score += 25 * sum((1 for token in path_tokens if token in candidate_path))
            except Exception:
                pass
            if any((token in low for token in ('.m3u8', 'playlist', 'video'))):
                score += 15
            candidates.append((score, candidate_url))
        candidates.sort(key=lambda item: item[0], reverse=True)
        return list(dict.fromkeys((url for _score, url in candidates[:80])))
    def _resolve_hls_uri(self, uri: str, base_url: str, token_values: Dict[str, str]) -> str:
        uri = str(uri or '').strip().strip('"\'')
        if not uri:
            return ''
        def repl(match):
            key = match.group(1).strip().lower()
            return token_values.get(key, match.group(0))
        uri = re.sub('\\{\\$([^}]+)\\}', repl, uri)
        uri = re.sub('\\$\\{([^}]+)\\}', repl, uri)
        uri = re.sub('\\$([A-Za-z0-9_-]+)', repl, uri)
        return urljoin(base_url, uri)
    def _download_hls_video(self, manifest: bytes, source_url: str, video_it: Optional[ScanItem]=None, timeout: int=20):
        headers = {'User-Agent': f'RoUtils/{APP_VERSION}', 'Accept': '*/*', 'Accept-Encoding': 'identity'}
        def fetch(url):
            with _routils_request(url, timeout=timeout, headers=headers) as r:
                return (r.read(), r.geturl(), dict(r.headers.items()))
        ticket_urls = []
        if video_it is not None and self._video_has_placeholders(manifest.decode('utf-8', 'ignore')):
            ticket_urls = self._find_video_ticket_urls(video_it, manifest)
        initial_urls = []
        if source_url and (not self._video_has_placeholders(source_url)) and (source_url != '-'):
            initial_urls.append(source_url)
        initial_urls.extend(ticket_urls)
        def parse_manifest(data, base_url, token_values=None, depth=0):
            if depth > 5:
                raise RuntimeError('HLS playlist nesting is too deep.')
            token_values = dict(token_values or {})
            token_values.update(self._video_signed_query_values(base_url))
            text = data.decode('utf-8-sig', 'replace')
            lines = [x.strip() for x in text.splitlines() if x.strip()]
            if not any((x.upper().startswith('#EXTM3U') for x in lines)):
                raise RuntimeError('The cached video is not a valid HLS manifest.')
            variants = []
            pending_inf = None
            for line in lines:
                if line.upper().startswith('#EXT-X-STREAM-INF:'):
                    pending_inf = line.split(':', 1)[1]
                    continue
                if pending_inf is not None and (not line.startswith('#')):
                    bw = 0
                    res_area = 0
                    m = re.search('(?:^|,)BANDWIDTH=(\\d+)', pending_inf, re.I)
                    if m:
                        bw = int(m.group(1))
                    m = re.search('(?:^|,)RESOLUTION=(\\d+)x(\\d+)', pending_inf, re.I)
                    if m:
                        res_area = int(m.group(1)) * int(m.group(2))
                    variants.append((bw, res_area, line))
                    pending_inf = None
            if variants:
                variants.sort(key=lambda x: (x[0], x[1]), reverse=True)
                errors = []
                for _bw, _area, variant in variants:
                    uri = self._resolve_hls_uri(variant, base_url, token_values)
                    try:
                        child, child_url, child_headers = fetch(uri)
                        child_values = dict(token_values)
                        child_values.update(self._video_signed_query_values(child_url))
                        return parse_manifest(child, child_url, child_values, depth + 1)
                    except Exception as e:
                        errors.append(str(e))
                raise RuntimeError('Unable to open any HLS quality playlist: ' + (errors[-1] if errors else 'unknown error'))
            parts = []
            init_uri = None
            for line in lines:
                upper = line.upper()
                if upper.startswith('#EXT-X-KEY:'):
                    method = re.search('METHOD=([^,]+)', line, re.I)
                    if method and method.group(1).upper() != 'NONE':
                        raise RuntimeError('This HLS video is encrypted and the required key is not present in the cache.')
                    continue
                if upper.startswith('#EXT-X-MAP:'):
                    m = re.search('URI="([^"]+)"', line, re.I)
                    if m:
                        init_uri = self._resolve_hls_uri(m.group(1), base_url, token_values)
                    continue
                if not line.startswith('#'):
                    parts.append(self._resolve_hls_uri(line, base_url, token_values))
            if not parts:
                raise RuntimeError('The HLS playlist contains no media segments.')
            output = bytearray()
            if init_uri:
                init_data, _, _ = fetch(init_uri)
                output.extend(init_data)
            for n, part_url in enumerate(parts, 1):
                segment, _, _ = fetch(part_url)
                if not segment:
                    raise RuntimeError(f'HLS segment {n} was empty.')
                output.extend(segment)
            return bytes(output)
        errors = []
        for candidate in initial_urls:
            try:
                candidate_values = self._video_signed_query_values(candidate)
                resolved_candidate = self._resolve_hls_uri(candidate, candidate, candidate_values)
                data, final_url, _headers = fetch(resolved_candidate)
                if data.lstrip().startswith(b'#EXTM3U'):
                    values = dict(candidate_values)
                    values.update(self._video_signed_query_values(final_url))
                    return parse_manifest(data, final_url, values)
                cached_text = manifest.decode('utf-8', 'ignore')
                master_path = next((x.strip() for x in cached_text.splitlines() if x.strip() and (not x.lstrip().startswith('#')) and ('playlist.m3u8' in x.lower())), None)
                if master_path:
                    base = final_url if final_url.endswith('/') else final_url.rsplit('/', 1)[0] + '/'
                    playlist_url = self._resolve_hls_uri(master_path, base, values)
                    pdata, pfinal, _ = fetch(playlist_url)
                    if pdata.lstrip().startswith(b'#EXTM3U'):
                        values.update(self._video_signed_query_values(pfinal))
                        return parse_manifest(pdata, pfinal, values)
                errors.append('Ticket URL did not return an HLS playlist')
            except Exception as e:
                errors.append(str(e))
        if source_url and (not self._video_has_placeholders(manifest.decode('utf-8', 'ignore'))):
            return parse_manifest(manifest, source_url, self._video_signed_query_values(source_url))
        detail = errors[0] if errors else UI_TEXT['n29']
        raise RuntimeError('Could not recover the Roblox video ticket from cache. ' + detail)
    def _export_selected_video(self):
        if getattr(self, '_video_export_running', False):
            self._console_log(UI_TEXT['x25'])
            return
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['y25'], UI_TEXT['c25'], parent=self)
            return
        video_items = [it for it in items if str(it.kind).split(' ', 1)[0].lower() == 'video']
        if not video_items:
            messagebox.showerror(UI_TEXT['y25'], UI_TEXT['z25'], parent=self)
            return
        self._video_ticket_entries = None
        directory = None
        selected_path = None
        if len(video_items) > 1:
            directory = filedialog.askdirectory(parent=self, title=UI_TEXT['a26'])
            if not directory:
                return
        else:
            item = video_items[0]
            base_name = _sanitize_filename_for_windows(item.name or item.hash) or item.hash
            selected_path = filedialog.asksaveasfilename(parent=self, title=UI_TEXT['y25'], defaultextension='.mp4', initialfile=f'{base_name}.mp4', filetypes=[(UI_TEXT['b26'], '*.mp4 *.webm *.ts *.mkv *.m4v *.mov *.m3u8'), (UI_TEXT['z7'], '*.*')])
            if not selected_path:
                return
        self._video_export_running = True
        self._console_select_tab(UI_TEXT['u5'])
        self._console_log(UI_TEXT['c26'].format(p0=len(video_items)))
        def worker():
            saved = 0
            failed = 0
            paths = []
            errors = []
            for index, it in enumerate(video_items, 1):
                try:
                    blob = self._fetch_full_blob(it)
                    if not blob:
                        raise ValueError('cache data was not found')
                    body, meta = self._dump_blob_body(blob)
                    payload, ext = self._video_payload_from_body(it, body, meta)
                    if not payload or not ext:
                        raise ValueError('could not recover the video data')
                    if directory:
                        name = _sanitize_filename_for_windows(it.name or it.hash) or it.hash
                        path = os.path.join(directory, f'{name}_{it.hash}{ext}')
                    else:
                        base = os.path.splitext(selected_path)[0]
                        path = base + ext
                    with open(path, 'wb') as stream:
                        stream.write(payload)
                    saved += 1
                    paths.append(path)
                    if index == 1 or index % 5 == 0 or index == len(video_items):
                        self.after(0, lambda i=index, total=len(video_items), name=os.path.basename(path): self._console_log(UI_TEXT['d26'].format(p0=i, p1=total, p2=name)))
                except Exception as exc:
                    failed += 1
                    if len(errors) < 5:
                        errors.append(f"{getattr(it, 'name', None) or getattr(it, 'hash', 'video')}: {exc}")
                    if index == 1 or index % 5 == 0 or index == len(video_items):
                        self.after(0, lambda i=index, total=len(video_items): self._console_log(UI_TEXT['e26'].format(p0=i, p1=total)))
            try:
                self.after(0, lambda: self._finish_video_export(saved, failed, len(video_items), paths, directory, selected_path, errors))
            except Exception:
                self._video_export_running = False
        threading.Thread(target=worker, daemon=True, name='RoUtils-VideoExport').start()
    def _finish_video_export(self, saved, failed, total, paths, directory, selected_path, errors):
        self._video_export_running = False
        self._console_log(UI_TEXT['f26'].format(p0=saved, p1=total, p2=failed))
        if saved:
            if directory:
                message = UI_TEXT['g26'].format(p0=saved, p1=total, p2=directory)
            else:
                message = UI_TEXT['h26'].format(p0=paths[0], p1=human_size(os.path.getsize(paths[0])))
            if failed:
                message += f'\n\nFailed: {failed}'
                if errors:
                    message += '\n' + '\n'.join(errors)
            messagebox.showinfo(UI_TEXT['y25'], message, parent=self)
        else:
            message = UI_TEXT['i26']
            if errors:
                message += '\n\n' + '\n'.join(errors)
            messagebox.showerror(UI_TEXT['y25'], message, parent=self)
    def _rbxm_body(self, it):
        try:
            blob = self._fetch_full_blob(it)
            if not blob:
                return None
            meta = parse_rbxh(blob)
            body = meta.get('body') or b''
            if not body:
                return None
            body = _maybe_gunzip(body, meta.get('headers') or {})
            body = decompress_if_needed(body)
            magic = body.find(b'<roblox!')
            if magic == -1:
                magic = body.find(b'<roblox')
            if magic > 0:
                body = body[magic:]
            stripped = body.lstrip()
            if stripped.startswith(b'\xef\xbb\xbf'):
                stripped = stripped[3:].lstrip()
            if stripped.startswith(b'<roblox!'):
                return (body, True)
            if body.find(b'<roblox', 0, min(len(body), 4096)) != -1:
                if _write_rbxm is not None:
                    try:
                        return (write_rbxm(_xml_to_document(body)), True)
                    except Exception:
                        return (body, False)
                return (body, False)
        except Exception:
            return None
        return None
    def _export_selected_image(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['j26'], UI_TEXT['c25'])
            return
        if len(items) > 1:
            directory = filedialog.askdirectory(title=UI_TEXT['k26'])
            if not directory:
                return
            saved = 0
            for it in items:
                img = self._image_from_item(it)
                if not img:
                    continue
                fmt = (img.format or 'PNG').upper()
                ext = f'.{fmt.lower()}'
                path = os.path.join(directory, f'{it.hash}{ext}')
                try:
                    img.save(path)
                    saved += 1
                except Exception:
                    pass
            messagebox.showinfo(UI_TEXT['j26'], UI_TEXT['l26'].format(p0=saved, p1=len(items), p2=directory))
            return
        it = items[0]
        img = self._image_from_item(it)
        if not img:
            messagebox.showerror(UI_TEXT['j26'], UI_TEXT['m26'])
            return
        fmt = (img.format or 'PNG').upper()
        ext = f'.{fmt.lower()}'
        default_name = f'{it.hash}{ext}'
        path = filedialog.asksaveasfilename(title=UI_TEXT['j26'], defaultextension=ext, initialfile=default_name, filetypes=[(UI_TEXT['n26'].format(p0=fmt), f'*{ext}'), (UI_TEXT['z7'], '*.*')])
        if not path:
            return
        try:
            img.save(path)
            messagebox.showinfo(UI_TEXT['j26'], UI_TEXT['o26'].format(p0=path))
        except Exception as e:
            messagebox.showerror(UI_TEXT['j26'], UI_TEXT['k25'].format(p0=e))
    def _image_from_item(self, it) -> Optional[Image.Image]:
        blob = self._fetch_full_blob(it)
        if not blob:
            return None
        meta = parse_rbxh(blob)
        body = meta.get('body') or b''
        _, off = find_embedded_image(body)
        if off > 0:
            body = body[off:]
        try:
            return Image.open(io.BytesIO(body))
        except Exception:
            return None
    def _get_selected_item(self) -> Optional[ScanItem]:
        try:
            sel = self.tree.selection()
            if not sel:
                return None
            iid = sel[0]
            if not self.tree.exists(iid):
                return None
            return self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
        except tk.TclError:
            return None
    def _get_selected_items(self) -> List[ScanItem]:
        out: List[ScanItem] = []
        try:
            for iid in self.tree.selection():
                if not self.tree.exists(iid):
                    continue
                it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
                if it:
                    out.append(it)
        except tk.TclError:
            return []
        return out
    def _pause_scanner(self):
        was = self.watching
        if was:
            self._stop_watching()
        return was
    def _resume_scanner(self, was_running: bool):
        if was_running:
            self._start_watching()
    def _parse_new_hash(self, s: str, expected_nibbles: int) -> bytes:
        if not s:
            raise ValueError('Empty input.')
        s = s.strip()
        if s.lower().startswith('0x'):
            s = s[2:]
        s = re.sub('[^0-9A-Fa-f]', '', s)
        if len(s) != expected_nibbles:
            raise ValueError(f'Hash must be {expected_nibbles} hex characters (got {len(s)}).')
        try:
            return bytes.fromhex(s)
        except Exception:
            raise ValueError('Invalid hex characters.')
    def _action_change_hash(self):
        it = self._get_selected_item()
        if not it:
            return
        expected_nibbles = len(it.id_bytes) * 2
        new_hash = simpledialog.askstring(UI_TEXT['p26'], UI_TEXT['q26'].format(p0=expected_nibbles), initialvalue=it.hash)
        if not new_hash:
            return
        try:
            new_id_b = self._parse_new_hash(new_hash, expected_nibbles)
            new_hash_hex = new_id_b.hex()
        except Exception as e:
            messagebox.showerror(UI_TEXT['r26'], str(e))
            return
        if not messagebox.askyesno(UI_TEXT['s26'], UI_TEXT['t26'].format(p0=it.hash, p1=new_hash_hex)):
            return
        was_running = self._pause_scanner()
        try:
            conn = connect_rw(self.db_path)
            try:
                cur = conn.cursor()
                cur.execute('BEGIN IMMEDIATE')
                cur.execute('UPDATE files SET id=? WHERE id=?', (new_id_b, it.id_bytes))
                conn.commit()
            finally:
                conn.close()
            old_path = shard_path(self.shard_root, it.hash)
            if os.path.isfile(old_path):
                new_dir = os.path.join(self.shard_root, new_hash_hex[:2])
                os.makedirs(new_dir, exist_ok=True)
                new_path = os.path.join(new_dir, new_hash_hex)
                try:
                    if os.path.isfile(new_path):
                        os.remove(new_path)
                    os.replace(old_path, new_path)
                except Exception as e:
                    messagebox.showwarning(UI_TEXT['u26'], UI_TEXT['v26'].format(p0=e))
            old_hash = it.hash
            self.seen_hashes.discard(old_hash)
            self.items_by_iid.pop(old_hash, None)
            self.items_by_hash.pop(old_hash, None)
            try:
                self.tree.delete(old_hash)
            except Exception:
                pass
            it.hash, it.id_bytes = (new_hash_hex, new_id_b)
            self.seen_hashes.add(new_hash_hex)
            self.items_by_hash[new_hash_hex] = it
            self.tree.insert('', 'end', iid=new_hash_hex, values=(it.time, it.name, it.hash, human_size(it.size), it.kind, it.src))
            self.tree.selection_set(new_hash_hex)
            self._update_status()
            messagebox.showinfo(UI_TEXT['p26'], UI_TEXT['w26'])
        except Exception as e:
            messagebox.showerror(UI_TEXT['p26'], UI_TEXT['x26'].format(p0=e))
        finally:
            self._resume_scanner(was_running)
    def _action_delete_blob(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['y26'], UI_TEXT['c25'])
            return
        names = ', '.join((it.hash for it in items[:12])) + ('…' if len(items) > 12 else '')
        if not messagebox.askyesno(UI_TEXT['z26'], UI_TEXT['a27'].format(p0=len(items), p1=names)):
            return
        was_running = self._pause_scanner()
        deleted = 0
        try:
            for it in items:
                try:
                    conn = connect_rw(self.db_path)
                    cur = conn.cursor()
                    cur.execute('BEGIN IMMEDIATE')
                    cur.execute('DELETE FROM files WHERE id=?', (it.id_bytes,))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass
                spath = shard_path(self.shard_root, it.hash)
                if os.path.isfile(spath):
                    try:
                        os.remove(spath)
                    except Exception:
                        pass
                self.seen_hashes.discard(it.hash)
                self.items_by_iid.pop(it.hash, None)
                self.items_by_hash.pop(it.hash, None)
                try:
                    self.tree.delete(it.hash)
                except Exception:
                    pass
                deleted += 1
            self._update_status()
            messagebox.showinfo(UI_TEXT['y26'], UI_TEXT['b27'].format(p0=deleted))
        except Exception as e:
            messagebox.showerror(UI_TEXT['y26'], UI_TEXT['c27'].format(p0=e))
        finally:
            self._resume_scanner(was_running)
    def _action_save_hash_to_saves(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['z1'], UI_TEXT['c25'])
            return
        name = simpledialog.askstring(UI_TEXT['z1'], UI_TEXT['d27'])
        if not name:
            return
        safe_name = _sanitize_filename_for_windows(name.strip())
        if not safe_name:
            messagebox.showerror(UI_TEXT['z1'], UI_TEXT['e27'])
            return
        base_dir = getattr(self.replacer, 'hash_saves_dir', None)
        if not base_dir:
            messagebox.showerror(UI_TEXT['z1'], UI_TEXT['f27'])
            return
        os.makedirs(base_dir, exist_ok=True)
        saved = 0
        for idx, it in enumerate(items):
            label = safe_name if len(items) == 1 else f'{safe_name}_{idx + 1}'
            filename = f'{it.hash} - {label}'
            dest = os.path.join(base_dir, filename)
            if os.path.exists(dest):
                base = filename
                i = 1
                while True:
                    cand = f'{base} ({i})'
                    cand_path = os.path.join(base_dir, cand)
                    if not os.path.exists(cand_path):
                        dest = cand_path
                        break
                    i += 1
            try:
                with open(dest, 'x'):
                    pass
            except FileExistsError:
                with open(dest, 'wb'):
                    pass
            except Exception as e:
                messagebox.showerror(UI_TEXT['z1'], UI_TEXT['k3'].format(p0=e))
                return
            saved += 1
        try:
            if self.replacer.source_var.get() == 'HashSaves':
                self.replacer.refresh_view()
        except Exception:
            pass
        messagebox.showinfo(UI_TEXT['z1'], UI_TEXT['g27'].format(p0=saved))
    def _action_save_blob_to_saves(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo(UI_TEXT['h27'], UI_TEXT['c25'])
            return
        name = simpledialog.askstring(UI_TEXT['h27'], UI_TEXT['i27'])
        if not name:
            return
        safe_name = _sanitize_filename_for_windows(name.strip())
        if not safe_name:
            messagebox.showerror(UI_TEXT['h27'], UI_TEXT['e27'])
            return
        base_dir = getattr(self.replacer, 'file_saves_dir', None)
        if not base_dir:
            messagebox.showerror(UI_TEXT['h27'], UI_TEXT['j27'])
            return
        os.makedirs(base_dir, exist_ok=True)
        saved = 0
        for idx, it in enumerate(items):
            blob = self._fetch_full_blob(it)
            if not blob:
                continue
            fname = safe_name if len(items) == 1 else f'{safe_name}_{idx + 1}'
            dest = os.path.join(base_dir, fname)
            if os.path.exists(dest):
                b = fname
                i = 1
                while True:
                    cand = f'{b} ({i})'
                    cand_path = os.path.join(base_dir, cand)
                    if not os.path.exists(cand_path):
                        dest = cand_path
                        break
                    i += 1
            try:
                with open(dest, 'wb') as f:
                    f.write(blob)
            except Exception as e:
                messagebox.showerror(UI_TEXT['h27'], UI_TEXT['k27'].format(p0=e))
                return
            saved += 1
        try:
            if self.replacer.source_var.get() == 'FileSaves':
                self.replacer.refresh_view()
        except Exception:
            pass
        messagebox.showinfo(UI_TEXT['h27'], UI_TEXT['l27'].format(p0=saved))
    def _reset_seen(self, clear_list: bool):
        self.seen_hashes.clear()
        if clear_list:
            self._filter_render_generation += 1
            for job_name in ('_tree_insert_pending_job', '_filter_render_job'):
                job = getattr(self, job_name, None)
                if job is not None:
                    try:
                        self.after_cancel(job)
                    except Exception:
                        pass
                    setattr(self, job_name, None)
            self._tree_insert_pending = []
            self._tree_insert_pending_index = 0
            self._filter_render_phase = None
            self._filter_render_snapshot = []
            self._filter_render_index = 0
            self._filter_clear_iids = []
            self._filter_clear_index = 0
            self.items_by_iid.clear()
            self.items_by_hash.clear()
            try:
                self.tree.delete(*self.tree.get_children(''))
            except Exception:
                pass
        self._update_status()
    def _sort_by(self, col_key: str, numeric: bool=False):
        fields = {'time': 'time', 'name': 'name', 'hash': 'hash', 'size': 'size', 'kind': 'kind', 'src': 'src'}
        field_name = fields.get(col_key)
        try:
            iids = list(self.tree.get_children(''))
        except Exception:
            return
        if field_name:
            items = []
            for iid in iids:
                item = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
                if item is None:
                    try:
                        value = self.tree.set(iid, col_key)
                    except Exception:
                        value = ''
                else:
                    value = getattr(item, field_name, '')
                items.append((value, iid))
        else:
            items = [(self.tree.set(iid, col_key), iid) for iid in iids]
        def size_value(value):
            if isinstance(value, (int, float)):
                return float(value)
            text = str(value).strip().upper()
            for suffix, factor in (('TB', 1024 ** 4), ('GB', 1024 ** 3), ('MB', 1024 ** 2), ('KB', 1024), ('B', 1)):
                if text.endswith(suffix):
                    try:
                        return float(text[:-len(suffix)]) * factor
                    except Exception:
                        return 0.0
            try:
                return float(text)
            except Exception:
                return 0.0
        if col_key == 'size' or numeric:
            items.sort(key=lambda pair: size_value(pair[0]))
        else:
            items.sort(key=lambda pair: str(pair[0]).casefold())
        direction = 'asc'
        if getattr(self, '_last_sort', None) == (col_key, 'asc'):
            items.reverse()
            direction = 'desc'
        self._last_sort = (col_key, direction)
        ordered = [iid for _, iid in items]
        try:
            self.tree.set_children('', *ordered)
        except Exception:
            for idx, iid in enumerate(ordered):
                try:
                    self.tree.move(iid, '', idx)
                except Exception:
                    pass
    def _update_status(self):
        if not hasattr(self, 'status_label'):
            return
        total = len(self.items_by_hash)
        vis = len(self.items_by_iid)
        stat = 'Watching' if self.watching else 'Idle'
        self.status_label.config(text=UI_TEXT['m27'].format(p0=stat, p1=vis, p2=total, p3=WATCH_INTERVAL_SEC))
