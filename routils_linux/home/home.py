import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class HomeMixin:
    def _open_selected_roblox(self):
        if sys.platform.startswith('linux'):
            try:
                subprocess.Popen(['flatpak', 'run', 'org.vinegarhq.Sober'], close_fds=True, start_new_session=True)
                self._console_log('Started Sober with Flatpak.')
            except Exception as error:
                messagebox.showerror(UI_TEXT['x5'], f'Could not launch Sober. Verify that Flatpak and org.vinegarhq.Sober are installed.\n\n{error}', parent=self)
            return
        path = self.settings.get('roblox_path', '') if hasattr(self, 'settings') else ''
        if not path:
            try:
                path = self.roblox_path_var.get()
            except Exception:
                path = ''
        if os.path.isdir(path):
            candidate = os.path.join(path, 'RobloxPlayerBeta.exe')
            if os.path.isfile(candidate):
                path = candidate
        if not path or os.path.basename(path).lower() != 'robloxplayerbeta.exe' or not os.path.isfile(path):
            try:
                messagebox.showwarning(UI_TEXT['x5'], UI_TEXT['i9'])
            except Exception:
                pass
            return
        self._launch_roblox_executable(path)
    def _launch_roblox_executable(self, path):
        try:
            subprocess.Popen([path], shell=False)
            self._console_log(UI_TEXT['j9'].format(p0=path))
        except Exception as e:
            try:
                messagebox.showerror(UI_TEXT['x5'], UI_TEXT['k9'].format(p0=e))
            except Exception:
                pass
    def _version_path(self):
        return os.path.join(DATA_DIR, 'version.txt')
    def _reset_version_file(self):
        try:
            vp = self._version_path()
            if os.path.exists(vp):
                try:
                    os.remove(vp)
                except Exception:
                    pass
            with open(vp, 'w', encoding='utf-8') as f:
                f.write(APP_VERSION)
        except Exception:
            pass
    def _local_version(self):
        try:
            if not os.path.exists(self._version_path()):
                with open(self._version_path(), 'w', encoding='utf-8') as f:
                    f.write(APP_VERSION)
            with open(self._version_path(), encoding='utf-8') as f:
                return f.read().strip() or APP_VERSION
        except Exception:
            return APP_VERSION
    def _build_home_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.insert(0, tab, text=UI_TEXT['w5'])
        ttk.Label(tab, text=UI_TEXT['x5'], font=('Segoe UI Semibold', 20)).pack(anchor='w')
        ttk.Label(tab, text=UI_TEXT['c10'], font=('Segoe UI Semibold', 14)).pack(anchor='w', pady=(14, 14))
        links = ttk.Frame(tab)
        links.pack(anchor='w', fill='x')
        def add_link(text_value, url):
            label = tk.Label(links, text=text_value, fg='#4da6ff', bg=_CURRENT_PALETTE['bg_dark'], cursor='hand2', font=('Segoe UI Semibold', 12), anchor='w')
            label.pack(anchor='w', pady=3)
            label.bind('<Button-1>', lambda _e, u=url: webbrowser.open(u))
            label.bind('<Enter>', lambda _e, w=label: w.config(font=('Segoe UI Semibold', 12, 'underline')))
            label.bind('<Leave>', lambda _e, w=label: w.config(font=('Segoe UI Semibold', 12)))
            return label
        add_link(UI_TEXT['o29'], 'https://github.com/offp001/routils')
        add_link(UI_TEXT['p29'], 'https://discord.com/invite/849VtrYhm2')
        ttk.Label(links, text=UI_TEXT['d10'], foreground='#9aa0a6', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 8))
        _q = bytes.fromhex('446973636c616d65723a20546865206f6666696369616c20646f776e6c6f6164207265706f7369746f727920666f7220526f5574696c732069732068747470733a2f2f6769746875622e636f6d2f6f6666703030312f726f7574696c732053696e636520526f5574696c73206973206f70656e2d736f757263652c206974206973206561737920666f72206d616c6963696f757320636f646520746f20626520696e73657274656420696e746f2069743b20696620796f7520646f776e6c6f616465642069742066726f6d20616e20756e6b6e6f776e20736f75726365206f7220612066696c652073656e7420746f20796f7520627920736f6d656f6e6520656c73652c20706c656173652064656c65746520746861742066696c6520616e6420646f776e6c6f61642069742066726f6d20746865206f6666696369616c20736f757263653a2068747470733a2f2f6769746875622e636f6d2f6f6666703030312f726f7574696c730a0a596f752063616e20616c736f207368617265207468652066696c6520796f752070726576696f75736c7920646f776e6c6f616465642077697468206d6520286f66667030303129206279206a6f696e696e672074686520446973636f7264207365727665722061742068747470733a2f2f646973636f72642e636f6d2f696e766974652f38343956747259686d32').decode('utf-8')
        disclaimer_frame = tk.Frame(tab, bg=_CURRENT_PALETTE.get('bg_dark', '#1e1e1e'))
        disclaimer_frame.pack(fill='x', pady=(2, 8))
        disclaimer_text = tk.Text(disclaimer_frame, bg=_CURRENT_PALETTE.get('bg_dark', '#1e1e1e'), fg='#ff0000', font=('Segoe UI', -14, 'bold'), relief='flat', bd=0, highlightthickness=0, wrap='word', height=6, padx=0, pady=0, cursor='arrow')
        disclaimer_text.pack(fill='x', expand=True)
        disclaimer_text.tag_configure('plain', foreground='#ff0000', font=('Segoe UI', -14, 'bold'))
        disclaimer_text.tag_configure('link', foreground='#0080ff', font=('Segoe UI', -14, 'bold', 'underline'))
        urls = ('https://github.com/offp001/routils', 'https://discord.com/invite/849VtrYhm2')
        for part in re.split('(https://github\\.com/offp001/routils|https://discord\\.com/invite/849VtrYhm2)', _q):
            if not part:
                continue
            if part in urls:
                tag = 'url_' + str(abs(hash(part)))
                disclaimer_text.tag_configure(tag, foreground='#0080ff', font=('Segoe UI', -14, 'bold', 'underline'))
                disclaimer_text.insert('end', part, tag)
                disclaimer_text.tag_bind(tag, '<Button-1>', lambda event, url=part: webbrowser.open(url))
                disclaimer_text.tag_bind(tag, '<Enter>', lambda event: disclaimer_text.configure(cursor='hand2'))
                disclaimer_text.tag_bind(tag, '<Leave>', lambda event: disclaimer_text.configure(cursor='arrow'))
            else:
                disclaimer_text.insert('end', part, 'plain')
        disclaimer_text.configure(state='disabled')
        ttk.Separator(tab).pack(fill='x', pady=10)
        version_row = ttk.Frame(tab)
        version_row.pack(anchor='w')
        ttk.Label(version_row, text=UI_TEXT['e10'], font=('Segoe UI', 10, 'bold')).pack(side='left')
        self.home_version_value = ttk.Label(version_row, text=self._local_version(), font=('Segoe UI', 10, 'bold'))
        self.home_version_value.pack(side='left')
        self.home_version_state = ttk.Label(version_row, text=UI_TEXT['f10'], font=('Segoe UI', 10, 'bold'))
        self.home_version_state.pack(side='left', padx=(6, 0))
        self.home_version_var = tk.StringVar(value=f'Version: {self._local_version()} (Checking)')
        self.home_download_frame = ttk.Frame(tab)
        self.home_download_label = ttk.Label(self.home_download_frame, text=UI_TEXT['g10'])
        self.home_download_label.pack(anchor='w')
        self.home_download_progress = ttk.Progressbar(self.home_download_frame, orient='horizontal', mode='determinate', length=320)
        self.home_download_progress.pack(anchor='w', fill='x', pady=(3, 0))
    def _set_update_progress(self, downloaded=0, total=0, visible=True):
        try:
            if visible:
                self.home_download_frame.pack(side='bottom', anchor='w', fill='x', padx=10, pady=10)
                if total > 0:
                    self.home_download_progress.configure(mode='determinate', maximum=total, value=downloaded)
                    self.home_download_label.configure(text=UI_TEXT['h10'].format(p0=downloaded / total * 100))
                else:
                    self.home_download_progress.configure(mode='indeterminate')
                    self.home_download_progress.start(12)
                    self.home_download_label.configure(text=UI_TEXT['g10'])
            else:
                try:
                    self.home_download_progress.stop()
                except Exception:
                    pass
                self.home_download_frame.pack_forget()
        except Exception:
            pass
    def _extract_profile_from_cookies(self):
        path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox', 'LocalStorage', 'RobloxCookies.dat') if os.name == 'nt' else os.path.join(str(sober_appdata_root()), 'RobloxCookies.dat')
        if not os.path.isfile(path):
            return (None, None)
        try:
            raw = open(path, 'rb').read()
            text = raw.decode('utf-8', errors='ignore')
            uid = None
            username = None
            for pat in ('"userId"\\s*[:=]\\s*"?(\\d+)', '"UserId"\\s*[:=]\\s*"?(\\d+)', 'userid[^0-9]{0,30}(\\d+)'):
                m = re.search(pat, text, re.I)
                if m:
                    uid = m.group(1)
                    break
            for pat in ('"username"\\s*[:=]\\s*"([^"\\\\]+)', '"name"\\s*[:=]\\s*"([^"\\\\]+)'):
                m = re.search(pat, text, re.I)
                if m:
                    username = m.group(1)
                    break
            if not uid:
                for token in re.findall('[A-Za-z0-9+/=]{24,}', text):
                    try:
                        t = base64.b64decode(token).decode('utf-8', errors='ignore')
                        m = re.search('"(?:userId|UserId)"\\s*:\\s*"?(\\d+)', t)
                        if m:
                            uid = m.group(1)
                        m2 = re.search('"(?:username|name)"\\s*:\\s*"([^"\\\\]+)', t, re.I)
                        if m2:
                            username = m2.group(1)
                        if uid:
                            break
                    except Exception:
                        pass
            return (username, uid)
        except Exception:
            return (None, None)
    def _detect_roblox_profile(self):
        username, uid = self._extract_profile_from_cookies()
        if username:
            self.settings['roblox_username'] = username
        if uid:
            self.settings['roblox_user_id'] = uid
        save_settings(self.settings)
    def _start_profile_detection(self):
        def worker():
            self._detect_roblox_profile()
        threading.Thread(target=worker, daemon=True).start()
    @staticmethod
    def _version_tuple(version):
        parts = re.findall('\\d+', str(version or ''))
        if not parts:
            return (0,)
        return tuple((int(x) for x in parts[:4]))
    def _is_newer_version(self, latest, current):
        return self._version_tuple(latest) > self._version_tuple(current)
    def _show_outdated_dialog(self, latest):
        if self._outdated_dialog_shown or self._auto_update_in_progress:
            return
        self._outdated_dialog_shown = True
        try:
            dlg = tk.Toplevel(self)
            dlg.title('RoUtils is Outdated')
            dlg.resizable(False, False)
            dlg.transient(self)
            dlg.grab_set()
            theme_toplevel(dlg)
            width, height = (440, 230)
            self.update_idletasks()
            x = max(0, (self.winfo_screenwidth() - width) // 2)
            y = max(0, (self.winfo_screenheight() - height) // 2)
            dlg.geometry(f'{width}x{height}+{x}+{y}')
            outer = ttk.Frame(dlg, padding=24)
            outer.pack(fill='both', expand=True)
            ttk.Label(outer, text=UI_TEXT['i10'], font=('Segoe UI Semibold', 18)).pack(pady=(8, 8))
            ttk.Label(outer, text=UI_TEXT['j10'].format(p0=latest), font=('Segoe UI', 11)).pack(pady=(0, 20))
            buttons = ttk.Frame(outer)
            buttons.pack()
            def download():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                try:
                    dlg.destroy()
                except Exception:
                    pass
                webbrowser.open(f'https://github.com/offp001/routils/releases/download/{latest}/RoUtils.exe')
            def later():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                try:
                    dlg.destroy()
                except Exception:
                    pass
            ttk.Button(buttons, text=UI_TEXT['k10'], command=download).pack(side='left', padx=6)
            ttk.Button(buttons, text=UI_TEXT['l10'], command=later).pack(side='left', padx=6)
            dlg._routils_close_callback = later
            dlg.protocol('WM_DELETE_WINDOW', later)
            dlg.after(100, lambda d=dlg: (_routils_popup_chrome(d), d.lift(), d.focus_force()) if d.winfo_exists() else None)
            dlg.focus_force()
        except Exception:
            self._outdated_dialog_shown = False
    def _start_auto_update(self, latest):
        if self._auto_update_in_progress:
            return
        self._auto_update_in_progress = True
        def worker():
            try:
                current = self._local_version()
                if not self._is_newer_version(latest, current):
                    self._auto_update_in_progress = False
                    return
                download_url = f'https://github.com/offp001/routils/releases/download/{latest}/RoUtils.exe'
                target_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
                target_path = os.path.join(target_dir, f'RoUtils-{latest}.exe')
                temp_path = os.path.join(tempfile.gettempdir(), f'RoUtils-{latest}.download')
                self.after(0, lambda: self._set_update_progress(0, 0, True))
                self.after(0, lambda v=latest: self._console_log(UI_TEXT['m10'].format(p0=v)))
                with _routils_request(download_url, timeout=30, headers={'Accept': 'application/octet-stream, */*'}) as response:
                    total = int(response.headers.get('Content-Length', '0') or 0)
                    downloaded = 0
                    with open(temp_path, 'wb') as out:
                        while True:
                            chunk = response.read(1024 * 256)
                            if not chunk:
                                break
                            out.write(chunk)
                            downloaded += len(chunk)
                            self.after(0, lambda d=downloaded, t=total: self._set_update_progress(d, t, True))
                if not os.path.isfile(temp_path) or os.path.getsize(temp_path) < 1024:
                    raise RuntimeError('Downloaded update is invalid.')
                os.replace(temp_path, target_path)
                self.after(0, lambda p=target_path: self._console_log(UI_TEXT['n10'].format(p0=p)))
                subprocess.Popen([target_path], cwd=target_dir, close_fds=True, creationflags=getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0))
                self.after(0, lambda: (self._set_update_progress(0, 0, False), self._on_close(force=True)))
            except Exception as e:
                self._auto_update_in_progress = False
                try:
                    self.after(0, lambda err=str(e): self._console_log(UI_TEXT['o10'].format(p0=err)))
                except Exception:
                    pass
                try:
                    self.after(0, lambda: self._set_update_progress(0, 0, False))
                except Exception:
                    pass
                try:
                    temp_path = locals().get('temp_path')
                    if temp_path and os.path.isfile(temp_path):
                        os.remove(temp_path)
                except Exception:
                    pass
                try:
                    self.after(0, lambda err=str(e): self._show_update_error(err))
                except Exception:
                    pass
        threading.Thread(target=worker, daemon=True, name='RoUtils-AutoUpdate').start()
    def _show_update_error(self, error):
        self._auto_update_in_progress = False
        try:
            messagebox.showwarning(UI_TEXT['p10'], UI_TEXT['q10'].format(p0=error), parent=self)
        except Exception:
            pass
    def _start_version_check(self):
        if getattr(self, '_version_check_started', False):
            return
        self._version_check_started = True
        self._version_check_result_queue = queue.Queue()
        current = self._local_version()
        try:
            self.home_version_value.configure(text=current)
            self.home_version_state.configure(text='Checking...', foreground='#f2c94c')
            self.home_version_var.set(UI_TEXT['r10'].format(p0=current, p1='Checking...'))
        except Exception:
            pass
        def worker():
            current_version = current
            errors = []
            latest = ''
            endpoints = (
                ('https://api.github.com/repos/offp001/routils/releases/latest', 'single'),
                ('https://api.github.com/repos/offp001/routils/releases?per_page=1', 'list'),
            )
            for url, response_kind in endpoints:
                try:
                    with _routils_request(url, timeout=2.5, headers={'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}) as response:
                        payload = response.read(256 * 1024)
                    data = json.loads(payload.decode('utf-8', 'replace'))
                    if response_kind == 'list':
                        if not isinstance(data, list) or not data:
                            raise ValueError('No published releases were returned')
                        release = data[0]
                    else:
                        release = data
                    if not isinstance(release, dict):
                        raise ValueError('Invalid release response')
                    tag = str(release.get('tag_name', '')).strip()
                    if not tag:
                        raise ValueError('The release response did not contain tag_name')
                    latest = tag.lstrip('vV').strip()
                    if not latest:
                        raise ValueError('The release tag was empty')
                    break
                except Exception as error:
                    errors.append(f'{url}: {error}')
            if latest:
                try:
                    outdated = self._is_newer_version(latest, current_version)
                    state = 'Outdated' if outdated else 'Latest'
                    color = '#ff5f57' if outdated else '#65d98b'
                    result = {'current': current_version, 'latest': latest, 'state': state, 'color': color, 'outdated': outdated, 'error': ''}
                except Exception as error:
                    result = {'current': current_version, 'latest': '', 'retry': True, 'error': str(error)}
            else:
                result = {'current': current_version, 'latest': '', 'retry': True, 'error': ' | '.join(errors) or 'Version endpoint unavailable'}
            try:
                self._version_check_result_queue.put_nowait(result)
            except Exception:
                pass
        self._version_check_worker = threading.Thread(target=worker, daemon=True, name='RoUtils-VersionCheck')
        self._version_check_worker.start()
        try:
            self._version_check_poll_after = self.after(40, self._poll_version_check_result)
        except Exception:
            self._version_check_poll_after = None
    def _retry_version_check(self):
        self._version_check_retry_after = None
        self._version_check_started = False
        try:
            if self.winfo_exists():
                self._start_version_check()
        except Exception:
            pass
    def _poll_version_check_result(self):
        try:
            result_queue = getattr(self, '_version_check_result_queue', None)
            result = result_queue.get_nowait() if result_queue is not None else None
        except queue.Empty:
            result = None
        except Exception:
            result = None
        if result is None:
            try:
                if self.winfo_exists():
                    self._version_check_poll_after = self.after(60, self._poll_version_check_result)
            except Exception:
                self._version_check_poll_after = None
            return
        current = str(result.get('current') or self._local_version())
        if result.get('retry'):
            try:
                self.home_version_value.configure(text=current)
                self.home_version_state.configure(text='Checking...', foreground='#f2c94c')
                self.home_version_var.set(UI_TEXT['r10'].format(p0=current, p1='Checking...'))
            except Exception:
                pass
            try:
                logging.getLogger('RoUtils').debug('Version check will retry: %s', result.get('error', 'unavailable'))
            except Exception:
                pass
            try:
                if self.winfo_exists():
                    old_job = getattr(self, '_version_check_retry_after', None)
                    if old_job:
                        try:
                            self.after_cancel(old_job)
                        except Exception:
                            pass
                    self._version_check_retry_after = self.after(2500, self._retry_version_check)
            except Exception:
                self._version_check_retry_after = None
            return
        latest = str(result.get('latest') or current)
        state = str(result.get('state') or 'Latest')
        color = str(result.get('color') or '#65d98b')
        self._latest_version = latest
        try:
            self.home_version_value.configure(text=current)
            self.home_version_state.configure(text=state, foreground=color)
            self.home_version_var.set(UI_TEXT['r10'].format(p0=current, p1=state))
        except Exception:
            pass
        if result.get('outdated'):
            if self.auto_update.get():
                self._start_auto_update(latest)
            else:
                self._show_outdated_dialog(latest)
    def _initial_tab_order_post_map(self, attempts=0):
        try:
            if not self.winfo_exists():
                return
            splash = getattr(self, '_routils_splash', None)
            if splash is not None:
                try:
                    if splash.winfo_exists() and attempts < 60:
                        self.after(100, lambda a=attempts + 1: self._initial_tab_order_post_map(a))
                        return
                except Exception:
                    pass
            self._reorder_tabs()
            self._tab_nav_layout_signature = None
            self._refresh_tab_nav()
            self.after_idle(self._refresh_tab_nav)
        except Exception:
            if attempts < 60:
                try:
                    self.after(100, lambda a=attempts + 1: self._initial_tab_order_post_map(a))
                except Exception:
                    pass
    def _reorder_tabs(self):
        defaults = [UI_TEXT['w5'], UI_TEXT['f5'], UI_TEXT['h5'], UI_TEXT['i5'], UI_TEXT['j5'], UI_TEXT['l5'], UI_TEXT['k5'], UI_TEXT['m5'], UI_TEXT['n5'], UI_TEXT['o5'], UI_TEXT['p5'], UI_TEXT['q5'], UI_TEXT['s5'], UI_TEXT['t5'], UI_TEXT['u5'], UI_TEXT['r5']]
        current_tabs = list(self.nb.tabs())
        remaining = list(current_tabs)
        ordered_tabs = []
        for name in defaults:
            tab_id = next((candidate for candidate in remaining if str(self.nb.tab(candidate, 'text')) == name), None)
            if tab_id is not None:
                ordered_tabs.append(tab_id)
                remaining.remove(tab_id)
        ordered_tabs.extend(remaining)
        for index, tab_id in enumerate(ordered_tabs):
            self.nb.insert(index, tab_id)
        if hasattr(self, 'settings'):
            self.settings['tab_order'] = [str(self.nb.tab(tab_id, 'text')) for tab_id in self.nb.tabs()]
        self._tab_nav_layout_signature = None
        self._refresh_tab_nav()
