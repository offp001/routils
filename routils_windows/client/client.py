import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class ClientMixin:
    def _build_client_tab(self):
        self._client_tab_active = True
        tab_outer = _ScrollableTab(self.nb, padding=0)
        tab = tab_outer.inner
        self.nb.add(tab_outer, text=UI_TEXT['p5'])
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text=UI_TEXT['m12'], font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w')
        ttk.Label(tab, text=UI_TEXT['n12'], foreground='#9aa0a6').grid(row=1, column=0, sticky='w', pady=(0, 14))
        info = ttk.LabelFrame(tab, text=UI_TEXT['o12'], padding=14)
        info.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        info.columnconfigure(1, weight=1)
        self.client_status_var = tk.StringVar(value=UI_TEXT['d30'])
        self.client_pid_var = tk.StringVar(value='—')
        self.client_path_var = tk.StringVar(value='—')
        self.client_version_var = tk.StringVar(value='—')
        self.client_game_var = tk.StringVar(value=UI_TEXT['e30'])
        self.client_place_var = tk.StringVar(value='—')
        self.client_job_var = tk.StringVar(value='—')
        self.client_cpu_var = tk.StringVar(value='—')
        self.client_ram_var = tk.StringVar(value='—')
        rows = ((UI_TEXT['f31'], self.client_status_var), (UI_TEXT['g31'], self.client_pid_var), (UI_TEXT['h31'], self.client_path_var), (UI_TEXT['q28'], self.client_version_var), (UI_TEXT['i31'], self.client_game_var), (UI_TEXT['o28'], self.client_place_var), ('Job ID', self.client_job_var), (UI_TEXT['r28'], self.client_cpu_var), (UI_TEXT['s28'], self.client_ram_var))
        for i, (label, var) in enumerate(rows):
            ttk.Label(info, text=label).grid(row=i, column=0, sticky='w', padx=(0, 14), pady=5)
            ttk.Label(info, textvariable=var).grid(row=i, column=1, sticky='w', pady=5)
        actions = ttk.Frame(tab)
        actions.grid(row=3, column=0, sticky='w', pady=(4, 0))
        ttk.Button(actions, text=UI_TEXT['c12'], command=self._client_refresh).pack(side='left', padx=(0, 6))
        ttk.Button(actions, text=UI_TEXT['p12'], command=self._open_selected_roblox).pack(side='left')
        fps_box = ttk.LabelFrame(tab, text=UI_TEXT['q12'], padding=(10, 8))
        fps_box.grid(row=4, column=0, sticky='ew', pady=(12, 0))
        self.fps_value_label = ttk.Label(fps_box, font=('Segoe UI Semibold', 10))
        self.fps_value_label.pack(anchor='w')
        self.fps_pid_label = ttk.Label(fps_box, text=UI_TEXT['r12'], foreground='#9aa0a6')
        self.fps_pid_label.pack(anchor='w', pady=(0, 4))
        def _fps_ui(value=None):
            fps = int(round(float(self.fps_limit.get() if value is None else value)))
            fps = max(0, min(240, fps))
            if self.fps_limit.get() != fps:
                self.fps_limit.set(fps)
            self.fps_value_label.config(text=UI_TEXT['z5'] if fps == 0 else UI_TEXT['a6'].format(p0=fps))
            if hasattr(self, '_fps_text_var') and self._fps_text_var.get() != str(fps):
                self._fps_text_var.set(str(fps))
        def _fps_slider_released(_event=None):
            if getattr(self, '_fps_release_job', None):
                try:
                    self.after_cancel(self._fps_release_job)
                except Exception:
                    pass
            self._fps_release_job = self.after(80, self._apply_fps_after_slider)
        ttk.Scale(fps_box, from_=0, to=240, orient='horizontal', variable=self.fps_limit, command=_fps_ui).pack(fill='x')
        self._fps_scale_widget = fps_box.winfo_children()[-1]
        self._fps_scale_widget.bind('<ButtonRelease-1>', _fps_slider_released, add='+')
        self._fps_text_var = tk.StringVar(value=str(self.fps_limit.get()))
        self._fps_text_entry = ttk.Entry(fps_box, textvariable=self._fps_text_var, width=12)
        self._fps_text_entry.pack(anchor='w', pady=(6, 0))
        def _fps_text_apply(_event=None):
            try:
                fps = int(self._fps_text_var.get().strip())
            except Exception:
                self._fps_text_var.set(str(self.fps_limit.get()))
                return
            fps = max(0, min(240, fps))
            self.fps_limit.set(fps)
            _fps_ui(fps)
            self._apply_fps_after_slider()
        self._fps_text_entry.bind('<Return>', _fps_text_apply)
        self._fps_text_entry.bind('<FocusOut>', _fps_text_apply)
        fps_hotkey_frame = ttk.Frame(fps_box)
        fps_hotkey_frame.pack(fill='x', pady=(8, 0))
        self._fps_hotkey_frame = fps_hotkey_frame
        self._build_fps_hotkey_buttons()
        fps_hotkey_actions = ttk.Frame(fps_box)
        fps_hotkey_actions.pack(fill='x', pady=(6, 0))
        ttk.Button(fps_hotkey_actions, text=UI_TEXT['s12'], command=self._reset_fps_hotkeys).pack(side='left')
        ttk.Label(fps_box, text=UI_TEXT['t12'], font=('Segoe UI', 8), foreground='#9aa0a6').pack(anchor='w')
        self._refresh_fps_hotkey_buttons()
        _fps_ui()
        self._client_cpu_prev = None
        self._client_system_prev = None
        self._client_refresh()
        self.after(UI_CLIENT_INTERVAL_MS, self._client_live_update)
    def _client_roblox_pids(self):
        if os.name != 'nt':
            return []
        try:
            class PROCESSENTRY32W(ctypes.Structure):
                _fields_ = [('dwSize', ctypes.wintypes.DWORD), ('cntUsage', ctypes.wintypes.DWORD), ('th32ProcessID', ctypes.wintypes.DWORD), ('th32DefaultHeapID', ctypes.POINTER(ctypes.c_ulong)), ('th32ModuleID', ctypes.wintypes.DWORD), ('cntThreads', ctypes.wintypes.DWORD), ('th32ParentProcessID', ctypes.wintypes.DWORD), ('pcPriClassBase', ctypes.c_long), ('dwFlags', ctypes.wintypes.DWORD), ('szExeFile', ctypes.wintypes.WCHAR * 260)]
            snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(2, 0)
            if snap in (0, -1):
                return []
            procs = []
            pe = PROCESSENTRY32W()
            pe.dwSize = ctypes.sizeof(pe)
            try:
                ok = ctypes.windll.kernel32.Process32FirstW(snap, ctypes.byref(pe))
                while ok:
                    name = pe.szExeFile.lower()
                    if name in ('robloxplayerbeta.exe', 'roblox.exe'):
                        procs.append((int(pe.th32ProcessID), int(pe.th32ParentProcessID), name))
                    ok = ctypes.windll.kernel32.Process32NextW(snap, ctypes.byref(pe))
            finally:
                ctypes.windll.kernel32.CloseHandle(snap)
            if not procs:
                return []
            pids = {pid for pid, _, _ in procs}
            changed = True
            while changed:
                changed = False
                for pid, ppid, _ in procs:
                    if ppid in pids and pid not in pids:
                        pids.add(pid)
                        changed = True
            return list(pids)
        except Exception:
            return []
    def _client_process_stats(self, pids):
        if not pids:
            return (None, None)
        try:
            wt = ctypes.wintypes
            PROCESS_QUERY_LIMITED_INFORMATION = 4096
            PROCESS_VM_READ = 16
            class PMC(ctypes.Structure):
                _fields_ = [('cb', wt.DWORD), ('PageFaultCount', wt.DWORD), ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t), ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
            total_cpu = 0
            total_ram = 0
            any_cpu = False
            any_ram = False
            for pid in pids:
                h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ, False, int(pid))
                if not h:
                    h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
                if not h:
                    continue
                try:
                    pm = PMC()
                    pm.cb = ctypes.sizeof(pm)
                    if ctypes.windll.psapi.GetProcessMemoryInfo(h, ctypes.byref(pm), pm.cb):
                        total_ram += int(pm.WorkingSetSize)
                        any_ram = True
                    c = wt.FILETIME()
                    e = wt.FILETIME()
                    k = wt.FILETIME()
                    u = wt.FILETIME()
                    if ctypes.windll.kernel32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e), ctypes.byref(k), ctypes.byref(u)):
                        total_cpu += (k.dwHighDateTime << 32 | k.dwLowDateTime) + (u.dwHighDateTime << 32 | u.dwLowDateTime)
                        any_cpu = True
                finally:
                    ctypes.windll.kernel32.CloseHandle(h)
            if not any_cpu and (not any_ram):
                return (None, None)
            st = wt.FILETIME()
            kt = wt.FILETIME()
            ut = wt.FILETIME()
            if ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(st), ctypes.byref(kt), ctypes.byref(ut)):
                system_time = (kt.dwHighDateTime << 32 | kt.dwLowDateTime) + (ut.dwHighDateTime << 32 | ut.dwLowDateTime)
                idle_time = st.dwHighDateTime << 32 | st.dwLowDateTime
                cpu_data = (total_cpu, (system_time, idle_time))
            else:
                cpu_data = total_cpu
            return (cpu_data, total_ram if any_ram else None)
        except Exception:
            return (None, None)
    def _client_game_refresh(self, place_id, job_id):
        place_id = str(place_id or '').strip()
        self.client_place_var.set(place_id or '—')
        self.client_job_var.set(str(job_id or '—'))
        if not place_id:
            self.client_game_var.set(UI_TEXT['y29'])
            return
        self.client_game_var.set(UI_TEXT['n28'])
        def worker():
            name = None
            try:
                name = self._resolve_history_game_name(place_id)
            except Exception:
                pass
            if not name:
                name = f'Place {place_id}'
            try:
                def update():
                    self.client_game_var.set(name)
                    self.client_place_var.set(f'{place_id} — {name}')
                self.after(0, update)
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()
    def _client_live_update(self):
        if getattr(self, '_resize_active', False):
            try:
                self.after(180, self._client_live_update)
            except Exception:
                pass
            return
        try:
            active = False
            if hasattr(self, 'nb'):
                active = str(self.nb.tab(self.nb.select(), 'text')) == UI_TEXT['p5']
            if not active and (not getattr(self, '_client_tab_active', False)):
                self.after(UI_CLIENT_INTERVAL_MS, self._client_live_update)
                return
            pids = self._client_roblox_pids()
            if pids:
                stats, ram = self._client_process_stats(pids)
                if isinstance(stats, tuple) and len(stats) == 2 and isinstance(stats[1], tuple):
                    proc, system = stats
                    if self._client_cpu_prev and self._client_system_prev:
                        dp = proc - self._client_cpu_prev
                        ds_total = system[0] - self._client_system_prev[0]
                        if ds_total > 0:
                            cpu_pct = dp / ds_total * 100.0
                            self.client_cpu_var.set(f'{max(0.0, min(100.0, cpu_pct)):.1f}%')
                    self._client_cpu_prev = proc
                    self._client_system_prev = system
                elif isinstance(stats, (int, float)):
                    if self._client_cpu_prev is not None:
                        dp = stats - self._client_cpu_prev
                        if dp >= 0:
                            self.client_cpu_var.set(f'{dp / 10000000 * 100:.1f}%')
                    self._client_cpu_prev = stats
                if ram is not None:
                    self.client_ram_var.set(f'{ram / 1024 / 1024:.1f} MB')
            else:
                self._client_cpu_prev = None
                self._client_system_prev = None
                self.client_cpu_var.set('—')
                self.client_ram_var.set('—')
        except Exception:
            pass
        try:
            self.after(UI_CLIENT_INTERVAL_MS, self._client_live_update)
        except Exception:
            pass
    def _client_refresh(self):
        pids = self._client_roblox_pids()
        pid = pids[0] if pids else _fflag_find_pid()
        path = _get_process_exe_path(pid) if pid else ''
        if not path:
            saved = str(self.settings.get('roblox_path', '') or '')
            if saved and os.path.isfile(saved):
                path = saved
        self.client_pid_var.set(', '.join((str(x) for x in sorted(pids))) if pids else 'Not running' if not pid else str(pid))
        self.client_status_var.set(UI_TEXT['u12'] if pids or pid else UI_TEXT['v12'])
        self.client_path_var.set(path or UI_TEXT['t28'])
        version = '—'
        if path and os.path.isfile(path):
            try:
                import win32api
                info = win32api.GetFileVersionInfo(path, '\\')
                ms = info['FileVersionMS']
                ls = info['FileVersionLS']
                version = f'{ms >> 16}.{ms & 65535}.{ls >> 16}.{ls & 65535}'
            except Exception:
                pass
        self.client_version_var.set(version)
        place_id, job_id = self._detect_current_game(silent=True) if pids or pid else (None, None)
        self._client_game_refresh(place_id, job_id)
        self._client_cpu_prev = None
        self._client_system_prev = None
