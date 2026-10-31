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
    def _build_home_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.insert(0, tab, text=UI_TEXT['w5'])
        ttk.Label(tab, text=UI_TEXT['x5'], font=('Segoe UI Semibold', 20)).pack(anchor='w')
        self._build_home_profile_card(tab)
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
    def _home_device_name(self):
        name = os.environ.get('COMPUTERNAME') or os.environ.get('HOSTNAME')
        if not name and hasattr(os, 'uname'):
            try:
                name = os.uname().nodename
            except Exception:
                name = None
        return str(name or 'This device')
    def _build_home_profile_card(self, parent):
        palette = _CURRENT_PALETTE
        bg = palette.get('bg_medium', palette.get('bg_dark', '#1e1e1e'))
        border = palette.get('border', '#3a3a3a')
        muted = palette.get('fg', '#d7d7d7')
        accent = palette.get('accent', '#4da6ff')
        shell = tk.Frame(parent, bg=border, padx=1, pady=1)
        shell.pack(fill='x', pady=(12, 12))
        card = tk.Frame(shell, bg=bg, padx=18, pady=14)
        card.pack(fill='x')
        info = tk.Frame(card, bg=bg)
        info.pack(side='left', fill='both', expand=True)
        self.home_profile_kind = tk.Label(info, text='DEVICE', bg=bg, fg=accent, font=('Segoe UI', 9, 'bold'), anchor='w')
        self.home_profile_kind.pack(anchor='w', pady=(0, 5))
        self.home_profile_name = tk.Label(info, text=self._home_device_name(), bg=bg, fg=muted, font=('Segoe UI Semibold', 19), anchor='w', justify='left')
        self.home_profile_name.pack(anchor='w', fill='x')
        self.home_profile_handle = tk.Label(info, text='', bg=bg, fg='#9aa0a6', font=('Segoe UI', 10), anchor='w')
        self.home_profile_handle.pack(anchor='w', pady=(4, 0))
        self.home_profile_avatar_frame = tk.Frame(card, bg=border, padx=2, pady=2)
        self.home_profile_avatar = tk.Label(self.home_profile_avatar_frame, bg=bg, bd=0, width=92, height=92)
        self.home_profile_avatar.pack()
        self.home_profile_photo = None
    def _profile_cookie_paths(self):
        try:
            root = str(sober_appdata_root())
        except Exception:
            return []
        return [
            os.path.join(root, 'LocalStorage', 'RobloxCookies.dat'),
            os.path.join(root, 'Roblox', 'LocalStorage', 'RobloxCookies.dat'),
            os.path.join(root, 'RobloxCookies.dat'),
        ]
    def _extract_profile_from_cookies(self):
        for path in self._profile_cookie_paths():
            if not os.path.isfile(path):
                continue
            try:
                with open(path, 'rb') as source:
                    raw = source.read(2 * 1024 * 1024)
                text = raw.decode('utf-8', errors='ignore')
                uid = None
                username = None
                for pattern in (r'"userId"\s*[:=]\s*"?(\d+)', r'"UserId"\s*[:=]\s*"?(\d+)', r'"user_id"\s*[:=]\s*"?(\d+)', r'userid[^0-9]{0,16}(\d{3,})'):
                    match = re.search(pattern, text, re.I)
                    if match:
                        uid = match.group(1)
                        break
                for pattern in (r'"username"\s*[:=]\s*"([^"\\]+)', r'"userName"\s*[:=]\s*"([^"\\]+)'):
                    match = re.search(pattern, text, re.I)
                    if match:
                        username = match.group(1)
                        break
                if uid or username:
                    return username, uid
            except Exception:
                continue
        return None, None
    def _fetch_roblox_profile(self, username, uid):
        try:
            if uid:
                url = f'https://users.roblox.com/v1/users/{uid}'
                with _routils_request(url, timeout=12, headers={'Accept': 'application/json'}) as response:
                    profile = json.loads(response.read().decode('utf-8', errors='replace'))
            elif username:
                payload = json.dumps({'usernames': [username], 'excludeBannedUsers': False}).encode('utf-8')
                with _routils_request('https://users.roblox.com/v1/usernames/users', timeout=12, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, data=payload, method='POST') as response:
                    result = json.loads(response.read().decode('utf-8', errors='replace'))
                profile = (result.get('data') or [None])[0] or {}
            else:
                return None
            resolved_uid = str(profile.get('id') or uid or '')
            resolved_username = str(profile.get('name') or username or '')
            display_name = str(profile.get('displayName') or resolved_username or '')
            if not resolved_uid:
                return None
            return {'user_id': resolved_uid, 'username': resolved_username, 'display_name': display_name}
        except Exception:
            if uid:
                return {'user_id': str(uid), 'username': str(username or ''), 'display_name': str(username or '')}
            return None
    def _fetch_roblox_avatar(self, uid):
        try:
            url = f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={uid}&size=150x150&format=Png&isCircular=true&thumbnailType=HeadShot'
            with _routils_request(url, timeout=12, headers={'Accept': 'application/json'}) as response:
                result = json.loads(response.read().decode('utf-8', errors='replace'))
            items = result.get('data') or []
            image_url = items[0].get('imageUrl') if items else None
            if not image_url:
                return None
            with _routils_request(image_url, timeout=15, headers={'Accept': 'image/png,image/*,*/*'}) as response:
                return response.read()
        except Exception:
            return None
    def _detect_roblox_profile(self):
        username, uid = self._extract_profile_from_cookies()
        if not uid and not username:
            return None, None
        profile = self._fetch_roblox_profile(username, uid)
        if not profile:
            return None, None
        avatar = self._fetch_roblox_avatar(profile['user_id'])
        return profile, avatar
    def _apply_home_profile(self, profile, avatar_data):
        try:
            if not self.winfo_exists() or not hasattr(self, 'home_profile_name'):
                return
            if not profile:
                self.home_profile_kind.configure(text='DEVICE')
                self.home_profile_name.configure(text=self._home_device_name())
                self.home_profile_handle.configure(text='')
                self.home_profile_avatar_frame.pack_forget()
                return
            self.settings['roblox_username'] = profile.get('username', '')
            self.settings['roblox_user_id'] = profile.get('user_id', '')
            self.settings['roblox_display_name'] = profile.get('display_name', '')
            save_settings(self.settings)
            self.home_profile_kind.configure(text='ROBLOX ACCOUNT')
            self.home_profile_name.configure(text=profile.get('display_name') or profile.get('username') or 'Roblox User')
            self.home_profile_handle.configure(text=f"@{profile['username']}" if profile.get('username') else '')
            if avatar_data:
                try:
                    image = Image.open(io.BytesIO(avatar_data)).convert('RGBA')
                    image.thumbnail((92, 92), getattr(Image, 'Resampling', Image).LANCZOS)
                    self.home_profile_photo = ImageTk.PhotoImage(image)
                    self.home_profile_avatar.configure(image=self.home_profile_photo, text='')
                    self.home_profile_avatar_frame.pack(side='right', padx=(18, 0))
                except Exception:
                    self.home_profile_avatar_frame.pack_forget()
        except Exception:
            pass
    def _start_profile_detection(self):
        def worker():
            profile, avatar = self._detect_roblox_profile()
            try:
                self.after(0, lambda p=profile, a=avatar: self._apply_home_profile(p, a))
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True, name='RoUtilsRobloxProfile').start()
    @staticmethod
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
