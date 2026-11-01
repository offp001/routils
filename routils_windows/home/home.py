import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})

class HomeMixin:

    def _open_selected_roblox(self):
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
        if not path or os.path.basename(path).lower() != 'robloxplayerbeta.exe' or (not os.path.isfile(path)):
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
        tab = ttk.Frame(self.nb, padding=22)
        self.nb.insert(0, tab, text=UI_TEXT['w5'])
        content = ttk.Frame(tab)
        content.pack(fill='both', expand=True)
        hero = ttk.Frame(content, style='RoUtils.Card.TFrame', padding=(28, 25, 28, 23))
        hero.pack(fill='x', pady=(0, 16))
        ttk.Label(hero, text='your roblox workspace', style='RoUtils.Eyebrow.TLabel').pack(anchor='w', pady=(0, 8))
        ttk.Label(hero, text='routils', style='RoUtils.HeroTitle.TLabel').pack(anchor='w')
        ttk.Label(hero, text='one place for the tools you use with roblox.', style='RoUtils.HeroBody.TLabel').pack(anchor='w', pady=(5, 16))
        actions = ttk.Frame(hero, style='RoUtils.Card.TFrame')
        actions.pack(anchor='w')
        ttk.Button(actions, text='open github', style='RoUtils.Primary.TButton', command=lambda: webbrowser.open('https://github.com/offp001/routils')).pack(side='left', padx=(0, 8))
        ttk.Button(actions, text='join discord', style='RoUtils.Secondary.TButton', command=lambda: webbrowser.open('https://discord.com/invite/849VtrYhm2')).pack(side='left')
        ttk.Label(content, text='quick access', style='RoUtils.Eyebrow.TLabel').pack(anchor='w', pady=(1, 8))
        quick = ttk.Frame(content)
        quick.pack(fill='x', pady=(0, 15))
        quick.columnconfigure((0, 1, 2), weight=1, uniform='quick')
        quick_items = (('cache', 'preview and manage local files', UI_TEXT['f5']), ('fflag manager', 'edit flags and organize presets', UI_TEXT['h5']), ('server viewer', 'browse public game servers', UI_TEXT['n5']))

        def open_section(name):
            target = next((tab_id for tab_id in self.nb.tabs() if str(self.nb.tab(tab_id, 'text')).lower() == name.lower()), None)
            if target:
                self.nb.select(target)
                self._lazy_tab_changed()
        for index, (title, description, target_name) in enumerate(quick_items):
            card = ttk.Frame(quick, style='RoUtils.Card.TFrame', padding=(15, 14, 15, 13))
            card.grid(row=0, column=index, sticky='nsew', padx=(0 if index == 0 else 6, 0 if index == 2 else 6))
            ttk.Label(card, text=title, style='RoUtils.CardTitle.TLabel').pack(anchor='w')
            ttk.Label(card, text=description, style='RoUtils.CardBody.TLabel', wraplength=205, justify='left').pack(anchor='w', pady=(5, 10))
            ttk.Button(card, text='open section', style='RoUtils.Secondary.TButton', command=lambda n=target_name: open_section(n)).pack(anchor='w')
        info_row = ttk.Frame(content)
        info_row.pack(fill='x', pady=(0, 13))
        info_row.columnconfigure((0, 1), weight=1, uniform='info')
        version_card = ttk.Frame(info_row, style='RoUtils.Card.TFrame', padding=(16, 14))
        version_card.grid(row=0, column=0, sticky='nsew', padx=(0, 6))
        ttk.Label(version_card, text='installed version', style='RoUtils.CardBody.TLabel').pack(anchor='w')
        version_line = ttk.Frame(version_card, style='RoUtils.Card.TFrame')
        version_line.pack(anchor='w', pady=(5, 0))
        ttk.Label(version_line, text='v', style='RoUtils.CardTitle.TLabel').pack(side='left')
        self.home_version_value = ttk.Label(version_line, text=self._local_version(), style='RoUtils.CardTitle.TLabel')
        self.home_version_value.pack(side='left')
        self.home_version_state = ttk.Label(version_line, text=UI_TEXT['f10'], style='RoUtils.CardBody.TLabel')
        self.home_version_state.pack(side='left', padx=(9, 0))
        self.home_version_var = tk.StringVar(value=f'version: {self._local_version()} (checking)')
        update_card = ttk.Frame(info_row, style='RoUtils.Card.TFrame', padding=(16, 14))
        update_card.grid(row=0, column=1, sticky='nsew', padx=(6, 0))
        ttk.Label(update_card, text='updates', style='RoUtils.CardBody.TLabel').pack(anchor='w')
        self.home_download_frame = ttk.Frame(update_card, style='RoUtils.Card.TFrame')
        self.home_download_label = ttk.Label(self.home_download_frame, text=UI_TEXT['g10'], style='RoUtils.CardTitle.TLabel')
        self.home_download_label.pack(anchor='w')
        self.home_download_progress = ttk.Progressbar(self.home_download_frame, orient='horizontal', mode='determinate', length=320)
        self.home_download_progress.pack(anchor='w', fill='x', pady=(8, 0))
        self.home_download_frame.pack(fill='x', pady=(5, 0))
        disclaimer = ttk.Frame(content, style='RoUtils.Card.TFrame', padding=(16, 13))
        disclaimer.pack(fill='x', pady=(0, 3))
        ttk.Label(disclaimer, text='download safely', style='RoUtils.CardTitle.TLabel').pack(anchor='w')
        disclaimer_text = bytes.fromhex('446973636c61696d65723a20546865206f6666696369616c20646f776e6c6f6164207265706f7369746f727920666f7220526f5574696c732069732068747470733a2f2f6769746875622e636f6d2f6f6666703030312f726f7574696c732053696e636520526f5574696c73206973206f70656e2d736f757263652c206974206973206561737920666f72206d616c6963696f757320636f646520746f20626520696e73657274656420696e746f2069743b20696620796f7520646f776e6c6f616465642069742066726f6d20616e20756e6b6e6f776e20736f75726365206f7220612066696c652073656e7420746f20796f7520627920736f6d656f6e6520656c73652c20706c656173652064656c65746520746861742066696c6520616e6420646f776e6c6f61642069742066726f6d20746865206f6666696369616c20736f757263653a2068747470733a2f2f6769746875622e636f6d2f6f6666703030312f726f7574696c730a0a596f752063616e20616c736f207368617265207468652066696c6520796f752070726576696f75736c7920646f776e6c6f616465642077697468206d6520286f66667030303129206279206a6f696e696e672074686520446973636f7264207365727665722061742068747470733a2f2f646973636f72642e636f6d2f696e766974652f38343956747259686d32').decode('utf-8').lower()
        ttk.Label(disclaimer, text=disclaimer_text, style='RoUtils.CardBody.TLabel', wraplength=940, justify='left').pack(fill='x', anchor='w', pady=(7, 0))

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
        defaults = [UI_TEXT['w5'], UI_TEXT['f5'], UI_TEXT['h5'], 'External', UI_TEXT['i5'], UI_TEXT['j5'], UI_TEXT['l5'], UI_TEXT['k5'], UI_TEXT['m5'], UI_TEXT['n5'], UI_TEXT['o5'], UI_TEXT['p5'], UI_TEXT['q5'], UI_TEXT['s5'], UI_TEXT['t5'], UI_TEXT['u5'], UI_TEXT['r5']]
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
