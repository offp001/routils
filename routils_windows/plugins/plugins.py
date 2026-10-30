import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class PluginsMixin:
    def _plugin_files(self):
        try:
            return sorted((os.path.join(self.plugins_dir, name) for name in os.listdir(self.plugins_dir) if name.lower().endswith('.py')))
        except Exception:
            return []
    def _plugin_load_python(self, path):
        module_name = 'routils_plugin_' + re.sub('[^a-zA-Z0-9_]', '_', os.path.splitext(os.path.basename(path))[0]) + '_' + uuid.uuid4().hex[:8]
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ValueError(UI_TEXT['b29'])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not callable(getattr(module, 'register', None)):
            raise ValueError(UI_TEXT['c29'])
        return module
    def _plugin_forget_tabs(self, name):
        tabs = list(self._plugin_tabs.pop(name, []) or [])
        module = self._plugin_modules.get(name)
        if module is not None:
            tabs.extend(list(getattr(module, 'ROUTILS_PLUGIN_TABS', []) or []))
        seen = set()
        for tab in tabs:
            key = str(tab)
            if key in seen:
                continue
            seen.add(key)
            try:
                if tab in self.nb.tabs():
                    self.nb.forget(tab)
            except Exception:
                try:
                    self.nb.forget(tab)
                except Exception:
                    pass
    def _plugin_enable(self, path, enabled=True):
        name = os.path.basename(path)
        enabled = bool(enabled)
        if not enabled:
            cleanup = self._plugin_cleanup.pop(name, None)
            if callable(cleanup):
                try:
                    cleanup()
                except Exception:
                    pass
            self._plugin_forget_tabs(name)
            self._plugin_modules.pop(name, None)
            self._plugin_enabled[name] = False
            self._save_settings()
            self._reorder_tabs()
            return
        if self._plugin_enabled.get(name, False) and name in self._plugin_modules:
            return
        try:
            self._plugin_forget_tabs(name)
            old_module = self._plugin_modules.pop(name, None)
            self._plugin_cleanup.pop(name, None)
            before_tabs = set(self.nb.tabs())
            module = self._plugin_load_python(path)
            result = module.register(self)
            plugin_tabs = []
            if isinstance(result, dict) and isinstance(result.get('tabs'), (list, tuple)):
                plugin_tabs.extend(result['tabs'])
            plugin_tabs.extend((tab for tab in self.nb.tabs() if tab not in before_tabs))
            unique_tabs = []
            seen = set()
            for tab in plugin_tabs:
                key = str(tab)
                if key not in seen:
                    seen.add(key)
                    unique_tabs.append(tab)
            module.ROUTILS_PLUGIN_TABS = unique_tabs
            self._plugin_tabs[name] = unique_tabs
            self._plugin_modules[name] = module
            cleanup = result.get('cleanup') if isinstance(result, dict) else None
            if callable(cleanup):
                self._plugin_cleanup[name] = cleanup
            self._plugin_enabled[name] = True
            self._save_settings()
            self._reorder_tabs()
        except Exception as exc:
            self._plugin_forget_tabs(name)
            self._plugin_modules.pop(name, None)
            self._plugin_cleanup.pop(name, None)
            self._plugin_enabled[name] = False
            self._save_settings()
            messagebox.showerror(UI_TEXT['y16'], UI_TEXT['z16'].format(p0=name, p1=exc), parent=self)
    def _restore_enabled_plugins(self):
        if getattr(self, '_restoring_enabled_plugins', False):
            return
        self._restoring_enabled_plugins = True
        try:
            enabled_names = {name for name, enabled in self._plugin_enabled.items() if enabled}
            if not enabled_names:
                return
            for path in self._plugin_files():
                name = os.path.basename(path)
                if name in enabled_names and name not in self._plugin_modules:
                    self._plugin_enable(path, True)
        finally:
            self._restoring_enabled_plugins = False
    def _plugin_open_guide(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            win = tk.Toplevel(self)
            win.title(os.path.basename(path))
            win.geometry('850x650')
            win.transient(self)
            txt = tk.Text(win, wrap='word', font=('Consolas', 10), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground=_CURRENT_PALETTE['fg'], bd=0, padx=14, pady=14)
            txt.pack(fill='both', expand=True)
            txt.insert('1.0', text)
            txt.configure(state='disabled')
        except Exception as exc:
            messagebox.showerror(UI_TEXT['y16'], UI_TEXT['a17'].format(p0=exc), parent=self)
    def _build_plugins_tab(self, tab=None):
        if tab is None:
            tab = ttk.Frame(self.nb, padding=14)
            self.nb.add(tab, text=UI_TEXT['s5'])
        else:
            for child in tab.winfo_children():
                child.destroy()
            tab.configure(padding=14)
            self.nb.tab(tab, text=UI_TEXT['s5'])
        header = ttk.Frame(tab)
        header.pack(fill='x', pady=(0, 10))
        ttk.Label(header, text=UI_TEXT['s5'], font=('Segoe UI Semibold', 16)).pack(side='left')
        ttk.Button(header, text=UI_TEXT['b17'], command=self._import_plugin_file).pack(side='right')
        ttk.Label(tab, text=UI_TEXT['c17'], foreground='#9aa0a6', wraplength=950).pack(anchor='w', pady=(0, 10))
        body = ttk.Frame(tab)
        body.pack(fill='both', expand=True)
        files = self._plugin_files()
        if not files:
            ttk.Label(body, text=UI_TEXT['d17'], foreground='#9aa0a6', justify='center').pack(expand=True)
            return
        for path in files:
            name = os.path.basename(path)
            card = ttk.LabelFrame(body, text=os.path.splitext(name)[0])
            card.pack(fill='x', pady=5)
            if path.lower().endswith('.txt'):
                ttk.Label(card, text=UI_TEXT['e17'], foreground='#9aa0a6').pack(anchor='w', padx=10, pady=7)
                ttk.Button(card, text=UI_TEXT['f17'], command=lambda p=path: self._plugin_open_guide(p)).pack(anchor='w', padx=8, pady=(0, 8))
            else:
                module = self._plugin_modules.get(name)
                desc = str(getattr(module, 'PLUGIN_DESCRIPTION', UI_TEXT['i17']) if module else UI_TEXT['i17'])
                ttk.Label(card, text=desc, foreground='#9aa0a6', wraplength=950).pack(anchor='w', padx=10, pady=7)
                row = ttk.Frame(card)
                row.pack(fill='x', padx=8, pady=(0, 8))
                enabled = tk.BooleanVar(value=bool(self._plugin_enabled.get(name, False)))
                ttk.Checkbutton(row, text=UI_TEXT['g17'], variable=enabled, command=lambda p=path, v=enabled: self._plugin_enable(p, v.get())).pack(side='left')
                if self._plugin_enabled.get(name, False) and name not in self._plugin_modules:
                    self._plugin_enable(path, True)
    def _import_plugin_file(self):
        path = filedialog.askopenfilename(parent=self, title=UI_TEXT['h17'], filetypes=[(UI_TEXT['i17'], '*.py')])
        if not path:
            return
        try:
            if path.lower().endswith('.py'):
                with open(path, 'r', encoding='utf-8') as f:
                    compile(f.read(), path, 'exec')
            target = os.path.join(self.plugins_dir, os.path.basename(path))
            shutil.copy2(path, target)
            self._reload_lazy_tab(UI_TEXT['s5'])
            messagebox.showinfo(UI_TEXT['y16'], UI_TEXT['j17'].format(p0=os.path.basename(path)), parent=self)
        except Exception as exc:
            messagebox.showerror(UI_TEXT['y16'], UI_TEXT['k17'].format(p0=exc), parent=self)
    def _reload_lazy_tab(self, tab_name):
        for tab_id in list(self.nb.tabs()):
            if str(self.nb.tab(tab_id, 'text')) == tab_name:
                try:
                    self.nb.forget(tab_id)
                except Exception:
                    pass
                break
        self._lazy_tabs = {k: v for k, v in self._lazy_tabs.items() if v[0] != tab_name}
        self._lazy_tab_ids.pop(tab_name, None)
        self._recreate_special_tab(tab_name)
    def _recreate_special_tab(self, tab_name):
        builder = {UI_TEXT['s5']: self._build_plugins_tab, UI_TEXT['t5']: self._build_release_notes_tab}.get(tab_name)
        if builder:
            builder()
            self._reorder_tabs()
            self._refresh_tab_nav()
