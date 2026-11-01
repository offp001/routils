import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class ConsoleMixin:
    def _console_log(self, message):
        if threading.get_ident() != getattr(self, '_ui_thread_id', threading.get_ident()):
            try:
                self.after(0, self._console_log, str(message))
            except Exception:
                pass
            return
        lines = _routils_visible_text(str(message)).replace('\r', '').splitlines() or ['']
        history = getattr(self, '_console_history', [])
        history.extend(lines)
        self._console_history = history[-1000:]
        if self._console_save_job is None:
            try:
                self._console_save_job = self.after(350, self._save_console_history)
            except Exception:
                self._console_save_job = None
        if hasattr(self, 'console_text'):
            if getattr(self, '_console_render_pending', False):
                return
            self._console_render_pending = True
            def render():
                try:
                    self._console_render_pending = False
                    self.console_text.configure(state='normal')
                    self.console_text.delete('1.0', 'end')
                    self.console_text.insert('end', '\n'.join(self._console_history) + '\n')
                    self.console_text.see('end')
                    self.console_text.configure(state='disabled')
                except Exception:
                    self._console_render_pending = False
            try:
                self.after(0, render)
            except Exception:
                pass
    def _console_undo(self):
        if not self._console_undo_stack:
            self._console_log(UI_TEXT['g19'])
            return
        kind, payload = self._console_undo_stack.pop()
        if kind == 'fflags':
            self.fflag_flags = payload
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._console_log(UI_TEXT['h19'])
        elif kind == 'cache':
            clean, blob = payload
            conn = connect_rw(self.db_path)
            try:
                conn.execute('INSERT OR REPLACE INTO files(id, content) VALUES(?, ?)', (bytes.fromhex(clean), sqlite3.Binary(blob)))
                conn.commit()
            finally:
                conn.close()
            self._console_log(UI_TEXT['i19'].format(p0=clean))
        elif kind == 'config':
            path, data = payload
            with open(path, 'wb') as f:
                f.write(data)
            self._cc_refresh_list()
            self._console_log(UI_TEXT['j19'].format(p0=os.path.basename(path)))
    def _console_select_tab(self, name):
        for tab_id in self.nb.tabs():
            if self.nb.tab(tab_id, 'text') == name:
                self.nb.select(tab_id)
                return True
        return False
    def _console_cache_search(self, query=''):
        query = str(query or '').lower().strip()
        rows = []
        for it in self.items_by_hash.values():
            text = f'{it.name} {it.hash} {it.kind} {it.src}'.lower()
            if not query or query in text:
                rows.append(f'{it.name} | {it.hash} | {it.kind}')
        self._console_log(UI_TEXT['k19'] + ('\n'.join(rows) if rows else UI_TEXT['l19']))
    def _console_create_backup(self, name='backup'):
        safe = _sanitize_filename_for_windows(str(name).strip()) or 'backup'
        backup_dir = os.path.join(DATA_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        path = os.path.join(backup_dir, f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for filename in ('routils_settings.json', 'routils_fflags.json', 'console_history.json'):
                source = os.path.join(DATA_DIR, filename)
                if os.path.isfile(source):
                    archive.write(source, filename)
            for folder in ('filesaves', 'hashsaves'):
                root = os.path.join(DATA_DIR, folder)
                if os.path.isdir(root):
                    for current, _, files in os.walk(root):
                        for filename in files:
                            source = os.path.join(current, filename)
                            archive.write(source, os.path.relpath(source, DATA_DIR))
        self._console_log(UI_TEXT['m19'].format(p0=path))
    def _console_restore_backup(self, path):
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(str(path))))
        if not os.path.isfile(path) or not path.lower().endswith('.zip'):
            raise ValueError(UI_TEXT['d29'])
        root = os.path.abspath(DATA_DIR)
        with zipfile.ZipFile(path, 'r') as archive:
            for member in archive.infolist():
                target = os.path.abspath(os.path.join(root, member.filename))
                if os.path.commonpath((root, target)) != root:
                    raise ValueError('Unsafe backup path.')
            archive.extractall(root)
        if hasattr(self, 'replacer'):
            self.replacer.refresh_view(preserve_selection=True)
        self._console_log(UI_TEXT['n19'].format(p0=path))
    def _console_command(self, raw):
        raw = str(raw or '').strip()
        if not raw:
            return
        self._console_log(UI_TEXT['o19'] + raw)
        if getattr(self, '_dump_caches_prompt_pending', False):
            answer = raw.strip().lower()
            if answer in ('y', 'yes'):
                self._dump_caches_prompt_pending = False
                self._start_dump_all_caches(True)
            elif answer in ('n', 'no'):
                self._dump_caches_prompt_pending = False
                self._start_dump_all_caches(False)
            else:
                self._console_log(UI_TEXT['p19'])
                self._console_log(UI_TEXT['q19'])
            return
        try:
            args = shlex.split(raw, posix=False)
            args = [x[1:-1] if len(x) >= 2 and x[0] == x[-1] and (x[0] in '"\'') else x for x in args]
            command = args[0].lower()
            values = args[1:]
            if command == 'help':
                self._console_log(UI_TEXT['r19'])
            elif command == 'cache' and len(values) >= 2 and (values[0].lower() not in ('delete', 'list', 'clear', 'search')):
                self._console_apply_cache(values[0], values[1])
            elif command == 'cache' and values and (values[0].lower() == 'delete') and (len(values) >= 2):
                self._console_delete_cache(values[1])
            elif command == 'cache' and values and (values[0].lower() == 'list'):
                self._console_list_caches(values[1] if len(values) >= 2 else '')
            elif command == 'cache' and values and (values[0].lower() == 'search'):
                self._console_cache_search(' '.join(values[1:]))
            elif command == 'fflag' and len(values) >= 2 and (values[0].lower() not in ('delete', 'list', 'clear')):
                self._console_undo_stack.append(('fflags', json.loads(json.dumps(self.fflag_flags))))
                name, value = (fflag_strip_prefix(values[0]), values[1])
                self.fflag_flags = [x for x in self.fflag_flags if fflag_strip_prefix(x.get('name', '')).lower() != name.lower()]
                self.fflag_flags.append({'name': name, 'value': value, 'type': fflag_infer_type(value)})
                self._save_fflag_flags()
                self._refresh_fflag_list()
                self._fflag_apply(silent=True)
                self._console_log(UI_TEXT['s19'].format(p0=name, p1=value))
            elif command == 'fflag' and values and (values[0].lower() == 'delete') and (len(values) >= 2):
                self._console_undo_stack.append(('fflags', json.loads(json.dumps(self.fflag_flags))))
                self._console_delete_fflag(values[1])
            elif command == 'fflag' and values and (values[0].lower() == 'clear'):
                self._console_undo_stack.append(('fflags', json.loads(json.dumps(self.fflag_flags))))
                self.fflag_flags = []
                self._save_fflag_flags()
                self._refresh_fflag_list()
                self._fflag_apply(silent=True)
                self._console_log(UI_TEXT['t19'])
            elif command == 'fflag' and values and (values[0].lower() == 'list'):
                self._console_list_fflags()
            elif command == 'fflag' and values and (values[0].lower() == 'apply'):
                self._fflag_apply(silent=True)
                self._console_log(UI_TEXT['u19'])
            elif command == 'fflag' and values and (values[0].lower() == 'unapply'):
                self._fflag_unapply()
                self._console_log(UI_TEXT['v19'])
            elif command == 'fflag' and values and (values[0].lower() in ('defaults', 'default')):
                self._open_default_fflag_values()
                self._console_log(UI_TEXT['w19'])
            elif command == 'fflag' and values and (values[0].lower() in ('latest', 'latestlist')):
                self._open_latest_fflag_list()
                self._console_log(UI_TEXT['x19'])
            elif command == 'config' and values:
                if values[0].lower() == 'list':
                    self._console_list_configs()
                elif values[0].lower() == 'save' and len(values) >= 2:
                    self._cc_save_named_config(' '.join(values[1:]))
                    self._console_log(UI_TEXT['y19'].format(p0=' '.join(values[1:])))
                elif values[0].lower() == 'delete' and len(values) >= 2:
                    self._console_delete_config(values[1])
                else:
                    self._console_apply_config(values[0])
            elif command == 'modif' and values and (values[0].lower() == 'meshtoobj') and (len(values) >= 2):
                self._console_mesh_to_obj(values[1])
            elif command == 'modif' and len(values) >= 2:
                self._console_replace_mesh(values[0], values[1], values[2] if len(values) >= 3 else '')
            elif command == 'join' and values and str(values[0]).isdigit():
                os.startfile(f'roblox://placeId={values[0]}')
                self._console_log(UI_TEXT['z19'].format(p0=values[0]))
            elif command == 'viewserver' and values:
                self._console_select_tab(UI_TEXT['n5'])
                self.after(100, lambda link=' '.join(values): (self.server_viewer_link.set(link), self._server_viewer_load()))
            elif command == 'information':
                self._console_select_tab(UI_TEXT['p5'])
                self.after(150, self._client_refresh)
                self._console_log(UI_TEXT['a20'])
            elif command == 'theme' and values:
                if values[0].lower() == 'list':
                    self._console_log(UI_TEXT['b20'] + ', '.join(THEME_NAMES))
                else:
                    self._console_apply_theme(' '.join(values))
            elif command == 'watch' and values and (values[0].lower() in ('start', 'stop')):
                if values[0].lower() == 'start':
                    if self._start_watching():
                        self._console_log(UI_TEXT['c20'])
                    else:
                        self._console_log(UI_TEXT['d20'])
                else:
                    self._stop_watching()
                    self._console_log(UI_TEXT['e20'])
            elif command == 'fps' and values:
                fps = max(0, min(240, int(values[0])))
                self.fps_limit.set(fps)
                self._save_settings()
                self._sync_fps_flag_to_manager()
                self._apply_fps_flag(silent=True)
                self._console_log(UI_TEXT['f20'].format(p0=fps if fps else 'uncapped'))
            elif command == 'dump-folder':
                dump_root = getattr(self, '_last_dump_folder', os.path.join(DATA_DIR, 'Dump'))
                os.makedirs(dump_root, exist_ok=True)
                try:
                    if hasattr(os, 'startfile'):
                        os.startfile(dump_root)
                    else:
                        webbrowser.open('file://' + os.path.abspath(dump_root))
                    self._console_log(UI_TEXT['g20'].format(p0=os.path.abspath(dump_root)))
                except Exception as e:
                    raise RuntimeError(f'Could not open dump folder: {e}')
            elif command == 'export' and values and (values[0].lower() == 'all'):
                self._dump_all_caches()
                self._console_log(UI_TEXT['h20'])
            elif command == 'backup' and values and (values[0].lower() == 'create'):
                self._console_create_backup(' '.join(values[1:]) if len(values) > 1 else 'backup')
            elif command == 'backup' and values and (values[0].lower() == 'restore') and (len(values) >= 2):
                self._console_restore_backup(values[1])
            elif command == 'ai':
                self._open_ai_chat()
            elif command == 'open' and values:
                tab_name = ' '.join(values)
                if not self._console_select_tab(tab_name):
                    raise ValueError(f'Tab not found: {tab_name}')
                self._console_log(UI_TEXT['i20'].format(p0=tab_name))
            elif command == 'status':
                self._console_log(UI_TEXT['j20'].format(p0=self.fflag_pid or 'not attached', p1='running' if self.watching else 'stopped', p2=self.db_path))
            elif command == 'clear':
                self._console_history = []
                self._save_console_history()
                if hasattr(self, 'console_text'):
                    self.console_text.configure(state='normal')
                    self.console_text.delete('1.0', 'end')
                    self.console_text.configure(state='disabled')
            elif command == 'history':
                self._console_log(UI_TEXT['k20'] + ('\n'.join(self._console_history) if self._console_history else UI_TEXT['l20']))
            elif command == 'undo':
                self._console_undo()
            else:
                self._console_log(UI_TEXT['m20'])
        except Exception as e:
            self._console_log(UI_TEXT['n20'] + str(e))
    def _console_apply_cache(self, path, hash_value):
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        clean = re.sub('[^0-9A-Fa-f]', '', str(hash_value))
        if not os.path.isfile(path) or not clean or len(clean) % 2:
            raise ValueError(UI_TEXT['e29'])
        with open(path, 'rb') as f:
            blob = f.read()
        id_b = bytes.fromhex(clean)
        conn = connect_rw(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute('BEGIN IMMEDIATE')
            cur.execute('DELETE FROM files WHERE id=?', (id_b,))
            cur.execute('INSERT INTO files(id, content) VALUES(?, ?)', (id_b, sqlite3.Binary(blob)))
            conn.commit()
        finally:
            conn.close()
        self._console_log(UI_TEXT['o20'].format(p0=clean, p1=path))
    def _console_delete_cache(self, hash_value):
        clean = re.sub('[^0-9A-Fa-f]', '', str(hash_value)).lower()
        if not clean or len(clean) % 2:
            raise ValueError(UI_TEXT['f29'])
        id_b = bytes.fromhex(clean)
        old_blob = None
        conn = connect_rw(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute('BEGIN IMMEDIATE')
            row = cur.execute('SELECT content FROM files WHERE id=?', (id_b,)).fetchone()
            if row and row[0] is not None:
                old_blob = bytes(row[0])
            cur.execute('DELETE FROM files WHERE id=?', (id_b,))
            deleted = cur.rowcount
            conn.commit()
        finally:
            conn.close()
        try:
            sp = shard_path(self.shard_root, clean)
            if os.path.isfile(sp):
                os.remove(sp)
        except Exception:
            pass
        self.seen_hashes.discard(clean)
        self.items_by_hash.pop(clean, None)
        self.items_by_iid.pop(clean, None)
        if hasattr(self, 'tree'):
            try:
                self.tree.delete(clean)
            except Exception:
                pass
        if hasattr(self, 'status_label'):
            self._update_status()
        if deleted and old_blob is not None:
            self._console_undo_stack.append(('cache', (clean, old_blob)))
        self._console_log(UI_TEXT['p20'].format(p0=clean) if deleted else UI_TEXT['q20'].format(p0=clean))
    def _console_list_caches(self, query=''):
        query = str(query or '').lower()
        rows = []
        for item in self.items_by_hash.values():
            text = f'{item.hash} {item.name} {item.kind}'.lower()
            if not query or query in text:
                rows.append(f"{item.hash} | {item.name or '(unnamed)'} | {item.kind}")
        self._console_log(UI_TEXT['r20'] + ('\n'.join(rows) if rows else UI_TEXT['s20']))
    def _console_delete_fflag(self, query):
        query = fflag_strip_prefix(str(query)).lower()
        matches = [x for x in self.fflag_flags if fflag_strip_prefix(x.get('name', '')).lower() == query]
        if len(matches) != 1:
            raise ValueError(UI_TEXT['g29'])
        self.fflag_flags = [x for x in self.fflag_flags if fflag_strip_prefix(x.get('name', '')).lower() != query]
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._fflag_apply(silent=True)
        self._console_log(UI_TEXT['t20'].format(p0=query))
    def _console_list_fflags(self):
        rows = [f"{x.get('name', '')} = {x.get('value', '')}" for x in self.fflag_flags]
        self._console_log(UI_TEXT['u20'] + ('\n'.join(rows) if rows else UI_TEXT['v20']))
    def _console_list_configs(self):
        configs = self._cc_scan_packages()
        rows = [f"{x.get('name', '')} | {x.get('_file', '')}" for x in configs]
        self._console_log(UI_TEXT['w20'] + ('\n'.join(rows) if rows else UI_TEXT['v20']))
    def _console_delete_config(self, query):
        q = str(query).lower()
        matches = [x for x in self._cc_scan_packages() if str(x.get('name', '')).lower().startswith(q)]
        if len(matches) != 1:
            raise ValueError(UI_TEXT['h29'])
        path = matches[0]['_path']
        with open(path, 'rb') as f:
            self._console_undo_stack.append(('config', (path, f.read())))
        os.remove(path)
        self._cc_refresh_list()
        self._console_log(UI_TEXT['x20'].format(p0=matches[0].get('name', '')))
    def _console_apply_config(self, query):
        self._console_select_tab(UI_TEXT['l5'])
        def apply():
            candidates = self._cc_scan_packages()
            q = str(query).lower()
            matches = [x for x in candidates if str(x.get('name', '')).lower().startswith(q)]
            if len(q) < 4 and len(matches) != 1:
                raise ValueError('Use at least the first 4 unique config characters.')
            if len(matches) != 1:
                raise ValueError('Config prefix is missing or ambiguous.')
            wanted = os.path.abspath(matches[0]['_path'])
            self._cc_refresh_list(select_path=wanted)
            self._cc_apply_db()
            self._console_log(UI_TEXT['y20'].format(p0=matches[0].get('name', '')))
        self.after(150, lambda: self._console_safe_call(apply))
    def _console_safe_call(self, fn):
        try:
            fn()
        except Exception as e:
            self._console_log(UI_TEXT['n20'] + str(e))
    def _console_mesh_to_obj(self, path):
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        out = os.path.splitext(path)[0] + '.obj'
        with open(path, 'rb') as f:
            data = f.read()
        convert(data, out)
        self._console_log(UI_TEXT['z20'].format(p0=out))
    def _console_replace_mesh(self, mesh_name, replacement, roblox_path=''):
        mesh_aliases = {'head': 'Head.mesh', 'torso': 'Torso.mesh', 'left arm': 'Left Arm.mesh', 'right arm': 'Right Arm.mesh', 'left leg': 'Left Leg.mesh', 'right leg': 'Right Leg.mesh'}
        mesh_name = mesh_aliases.get(str(mesh_name).strip().lower(), str(mesh_name).strip())
        if not mesh_name.lower().endswith('.mesh'):
            mesh_name += '.mesh'
        source = os.path.abspath(os.path.expandvars(os.path.expanduser(replacement)))
        if not os.path.isfile(source):
            raise FileNotFoundError(source)
        if roblox_path:
            self.roblox_path_var.set(os.path.abspath(os.path.expandvars(os.path.expanduser(roblox_path))))
        target = self._default_mesh_path(mesh_name)
        if not target:
            raise ValueError(UI_TEXT['i29'])
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(source, target)
        self._console_log(UI_TEXT['a21'].format(p0=mesh_name))
    def _console_apply_theme(self, query):
        names = [x for x in THEME_NAMES if x.lower() == str(query).lower() or x.lower().startswith(str(query).lower())]
        if len(names) != 1:
            raise ValueError(UI_TEXT['j29'])
        self._console_select_tab(UI_TEXT['q5'])
        def apply():
            self.theme_var.set(names[0])
            self._apply_theme()
            self._console_log(UI_TEXT['b21'].format(p0=names[0]))
        self.after(150, lambda: self._console_safe_call(apply))
    def _build_console_tab(self):
        tab = ttk.Frame(self.nb, padding=10)
        self.nb.add(tab, text=UI_TEXT['u5'])
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text=UI_TEXT['u5'], font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w', pady=(0, 8))
        self.console_text = tk.Text(tab, wrap='word', state='disabled', font=('Consolas', 9), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground='#ffffff', relief='flat', bd=0)
        self.console_text.grid(row=1, column=0, sticky='nsew')
        row = ttk.Frame(tab)
        row.grid(row=2, column=0, sticky='ew', pady=(8, 0))
        row.columnconfigure(1, weight=1)
        ttk.Label(row, text=UI_TEXT['v21'], font=('Consolas', 10, 'bold')).grid(row=0, column=0, padx=(0, 6))
        self.console_entry = ttk.Entry(row)
        self.console_entry.grid(row=0, column=1, sticky='ew')
        self.console_entry.bind('<Return>', lambda _e: (self._console_command(self.console_entry.get()), self.console_entry.delete(0, 'end'), 'break')[2])
        self._console_log(UI_TEXT['w21'])
