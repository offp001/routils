import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class ThemesMixin:
    def _apply_titlebar_theme(self):
        try:
            _apply_native_titlebar_theme(self)
        except Exception:
            pass
        try:
            style = ttk.Style(self)
            style.configure('RoUtils.ActiveNav.TButton', foreground=_CURRENT_PALETTE.get('accent', '#7f8cff'))
        except Exception:
            pass
        try:
            self._refresh_tab_nav()
        except Exception:
            pass
    def _build_themes_tab(self):
        self.settings.pop('background_image', None)
        self.settings.pop('background_opacity', None)
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text=UI_TEXT['q5'])
        ttk.Label(tab, text=UI_TEXT['i7'], font=('Segoe UI Semibold', 16)).pack(anchor='w')
        ttk.Label(tab, text=UI_TEXT['j7'], foreground='#9aa0a6').pack(anchor='w', pady=(0, 10))
        outer = ttk.Frame(tab)
        outer.pack(fill='both', expand=True)
        left = ttk.Frame(outer)
        left.pack(side='left', fill='both', expand=True)
        right = ttk.LabelFrame(outer, text=UI_TEXT['k7'], padding=12)
        right.pack(side='right', fill='y', padx=(14, 0))
        self.theme_var = tk.StringVar(value=self.settings.get('theme', DEFAULT_THEME))
        lb = tk.Listbox(left, bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], selectbackground=_CURRENT_PALETTE['accent'], relief='flat', bd=0, font=('Segoe UI', 10), exportselection=False)
        lb.pack(fill='both', expand=True)
        self._theme_listbox = lb
        theme_names = THEME_NAMES + (['Custom'] if 'Custom' not in THEME_NAMES else [])
        for name in theme_names:
            lb.insert('end', name)
        try:
            lb.selection_set(theme_names.index(self.theme_var.get()))
            lb.see(theme_names.index(self.theme_var.get()))
        except Exception:
            pass
        lb.bind('<<ListboxSelect>>', lambda _e: self._theme_list_apply(lb))
        custom = self.settings.get('custom_theme', {})
        if not isinstance(custom, dict):
            custom = {}
        self.custom_theme_vars = {}
        self._custom_theme_swatches = {}
        ttk.Label(right, text=UI_TEXT['l7'], font=('Segoe UI Semibold', 10)).pack(anchor='w', pady=(0, 4))
        palette_defaults = THEMES[DEFAULT_THEME]
        palette_labels = (('bg_dark', 'Main background'), ('bg_medium', 'Surface'), ('bg_light', 'Panel'), ('bg_hover', 'Hover'), ('fg', 'Text'), ('accent', 'Accent'), ('border', 'Border'))
        for key, label_text in palette_labels:
            chosen = custom.get(key, palette_defaults[key])
            if not isinstance(chosen, str) or not re.fullmatch('#[0-9a-fA-F]{6}', chosen):
                chosen = palette_defaults[key]
            color_var = tk.StringVar(value=chosen)
            self.custom_theme_vars[key] = color_var
            row = ttk.Frame(right)
            row.pack(fill='x', pady=2)
            ttk.Label(row, text=label_text, width=15).pack(side='left')
            swatch = tk.Button(row, text=UI_TEXT['m7'], bg=chosen, activebackground=chosen, relief='flat', bd=0, cursor='hand2', command=lambda k=key: self._choose_custom_theme_color(k))
            swatch.pack(side='left', padx=(0, 6))
            self._custom_theme_swatches[key] = swatch
            ttk.Button(row, text=UI_TEXT['n7'], command=lambda k=key: self._choose_custom_theme_color(k)).pack(side='left', fill='x', expand=True)
            ttk.Button(row, text=UI_TEXT['o7'], command=lambda k=key: self._reset_custom_theme_color(k)).pack(side='left', padx=(4, 0))
        ttk.Button(right, text=UI_TEXT['p7'], command=self._apply_custom_theme).pack(fill='x', pady=(7, 3))
        ttk.Button(right, text=UI_TEXT['q7'], command=self._save_custom_theme).pack(fill='x', pady=(0, 7))
        ttk.Separator(right).pack(fill='x', pady=6)
        ttk.Label(right, text=UI_TEXT['r7'], font=('Segoe UI Semibold', 10)).pack(anchor='w', pady=(0, 4))
        saved_button_colors = self.settings.get('topbar_button_colors', {})
        if not isinstance(saved_button_colors, dict):
            saved_button_colors = {}
        legacy_button_color = self.settings.get('topbar_button_color')
        defaults = {'close': '#ff5f57', 'max': '#28c840', 'min': '#febc2e'}
        self._topbar_button_color_vars = {}
        self._topbar_button_color_swatches = {}
        self._topbar_button_default_colors = defaults.copy()
        for button_name, label_text in (('close', 'Close'), ('max', 'Maximize'), ('min', 'Minimize')):
            chosen = saved_button_colors.get(button_name, legacy_button_color or defaults[button_name])
            if not isinstance(chosen, str) or not re.fullmatch('#[0-9a-fA-F]{6}', chosen):
                chosen = defaults[button_name]
            color_var = tk.StringVar(value=chosen)
            self._topbar_button_color_vars[button_name] = color_var
            color_row = ttk.Frame(right)
            color_row.pack(fill='x', pady=2)
            ttk.Label(color_row, text=label_text, width=15).pack(side='left')
            swatch = tk.Button(color_row, text=UI_TEXT['m7'], bg=chosen, activebackground=chosen, relief='flat', bd=0, cursor='hand2', command=lambda n=button_name: self._choose_topbar_button_color(n))
            swatch.pack(side='left', padx=(0, 5))
            self._topbar_button_color_swatches[button_name] = swatch
            ttk.Button(color_row, text=UI_TEXT['n7'], command=lambda n=button_name: self._choose_topbar_button_color(n)).pack(side='left', fill='x', expand=True)
            ttk.Button(color_row, text=UI_TEXT['o7'], command=lambda n=button_name: self._reset_topbar_button_color(n)).pack(side='left', padx=(4, 0))
        self.settings.pop('background_image', None)
        self.settings.pop('background_opacity', None)
    def _choose_custom_theme_color(self, key):
        variables = getattr(self, 'custom_theme_vars', {})
        variable = variables.get(key)
        if variable is None:
            return
        current = variable.get().strip()
        if not re.fullmatch('#[0-9a-fA-F]{6}', current):
            current = THEMES[DEFAULT_THEME].get(key, '#7f8cff')
        selected = colorchooser.askcolor(color=current, title=UI_TEXT['s7'].format(p0=key.replace('_', ' ')), parent=self)
        color = selected[1] if selected and selected[1] else None
        if not color or not re.fullmatch('#[0-9a-fA-F]{6}', color):
            return
        variable.set(color)
        swatch = getattr(self, '_custom_theme_swatches', {}).get(key)
        if swatch is not None:
            try:
                swatch.configure(bg=color, activebackground=color)
            except tk.TclError:
                pass
    def _reset_custom_theme_color(self, key):
        if key not in THEMES[DEFAULT_THEME]:
            return
        color = THEMES[DEFAULT_THEME][key]
        variable = getattr(self, 'custom_theme_vars', {}).get(key)
        if variable is not None:
            variable.set(color)
        swatch = getattr(self, '_custom_theme_swatches', {}).get(key)
        if swatch is not None:
            try:
                swatch.configure(bg=color, activebackground=color)
            except tk.TclError:
                pass
    def _apply_custom_theme(self):
        palette_defaults = THEMES[DEFAULT_THEME]
        palette = {}
        for key, default in palette_defaults.items():
            variable = getattr(self, 'custom_theme_vars', {}).get(key)
            value = variable.get().strip() if variable is not None else default
            palette[key] = value if isinstance(value, str) and re.fullmatch('#[0-9a-fA-F]{6}', value) else default
        self.settings['theme'] = 'Custom'
        self.settings['custom_theme'] = palette
        if hasattr(self, 'theme_var'):
            self.theme_var.set('Custom')
        try:
            if hasattr(self, '_theme_listbox') and self._theme_listbox.winfo_exists():
                names = self._theme_listbox.get(0, 'end')
                if 'Custom' in names:
                    index = names.index('Custom')
                    self._theme_listbox.selection_clear(0, 'end')
                    self._theme_listbox.selection_set(index)
                    self._theme_listbox.see(index)
        except (tk.TclError, ValueError):
            pass
        self._apply_theme()
    def _save_custom_theme(self):
        self._apply_custom_theme()
        messagebox.showinfo(UI_TEXT['i7'], UI_TEXT['t7'], parent=self)
    def _choose_topbar_button_color(self, button_name):
        if button_name not in {'close', 'max', 'min'}:
            return
        variables = getattr(self, '_topbar_button_color_vars', {})
        current = variables.get(button_name)
        saved_colors = self.settings.get('topbar_button_colors', {})
        if not isinstance(saved_colors, dict):
            saved_colors = {}
        current_color = current.get() if current is not None else saved_colors.get(button_name, '#7f8cff')
        selected = colorchooser.askcolor(color=current_color, title=UI_TEXT['u7'].format(p0=button_name.title()), parent=self)
        color = selected[1] if selected and selected[1] else None
        if not color or not re.fullmatch('#[0-9a-fA-F]{6}', color):
            return
        if current is not None:
            current.set(color)
        swatch = getattr(self, '_topbar_button_color_swatches', {}).get(button_name)
        if swatch is not None:
            try:
                swatch.configure(bg=color, activebackground=color)
            except tk.TclError:
                pass
        saved_colors[button_name] = color
        self.settings['topbar_button_colors'] = saved_colors
        try:
            item, command, _old_color = self._titlebar_buttons[button_name]
            self._titlebar_buttons[button_name] = (item, command, color)
            self._titlebar_canvas.itemconfigure(item, fill=color)
        except (AttributeError, KeyError, tk.TclError):
            pass
        self._save_settings()
    def _reset_topbar_button_color(self, button_name):
        defaults = getattr(self, '_topbar_button_default_colors', {'close': '#ff5f57', 'max': '#28c840', 'min': '#febc2e'})
        if button_name not in defaults:
            return
        color = defaults[button_name]
        variable = getattr(self, '_topbar_button_color_vars', {}).get(button_name)
        if variable is not None:
            variable.set(color)
        swatch = getattr(self, '_topbar_button_color_swatches', {}).get(button_name)
        if swatch is not None:
            try:
                swatch.configure(bg=color, activebackground=color)
            except tk.TclError:
                pass
        saved = self.settings.get('topbar_button_colors', {})
        if not isinstance(saved, dict):
            saved = {}
        saved[button_name] = color
        self.settings['topbar_button_colors'] = saved
        try:
            item, command, _old_color = self._titlebar_buttons[button_name]
            self._titlebar_buttons[button_name] = (item, command, color)
            self._titlebar_canvas.itemconfigure(item, fill=color)
        except (AttributeError, KeyError, tk.TclError):
            pass
        self._save_settings()
    def _apply_topbar_button_color(self):
        variables = getattr(self, '_topbar_button_color_vars', {})
        saved = self.settings.get('topbar_button_colors', {})
        if not isinstance(saved, dict):
            saved = {}
        for name, variable in variables.items():
            color = variable.get().strip()
            if re.fullmatch('#[0-9a-fA-F]{6}', color):
                saved[name] = color
        self.settings['topbar_button_colors'] = saved
        for name, color in saved.items():
            try:
                item, command, _old_color = self._titlebar_buttons[name]
                self._titlebar_buttons[name] = (item, command, color)
                self._titlebar_canvas.itemconfigure(item, fill=color)
            except (AttributeError, KeyError, tk.TclError):
                pass
        self._save_settings()
    def _theme_list_apply(self, lb):
        try:
            sel = lb.curselection()
            if not sel:
                return
            self.theme_var.set(lb.get(sel[0]))
            self._apply_theme()
        except (tk.TclError, AttributeError, IndexError):
            return
    def _apply_theme(self):
        theme_variable = getattr(self, 'theme_var', None)
        name = str((theme_variable.get() if theme_variable is not None else self.settings.get('theme', DEFAULT_THEME)) or DEFAULT_THEME)
        if name not in THEMES and name != 'Custom':
            name = DEFAULT_THEME
        self.settings['theme'] = name
        defaults = THEMES[DEFAULT_THEME]
        custom_palette = self.settings.get('custom_theme', {})
        if not isinstance(custom_palette, dict):
            custom_palette = {}
        palette = dict(defaults if name == 'Custom' else THEMES.get(name, defaults))
        if name == 'Custom':
            for key, fallback in defaults.items():
                value = custom_palette.get(key, fallback)
                palette[key] = value if isinstance(value, str) and re.fullmatch('#[0-9a-fA-F]{6}', value) else fallback
            self.settings['custom_theme'] = palette.copy()
        try:
            apply_visual_polish(self, theme=UI_THEME, palette=palette)
        except Exception as exc:
            try:
                self._console_log(UI_TEXT['v7'].format(p0=exc))
            except Exception:
                pass
        self._apply_titlebar_theme()
        try:
            darken_menus(self._collect_menus())
        except Exception:
            pass
        try:
            theme_listbox = getattr(self, '_theme_listbox', None)
            if theme_listbox is not None and theme_listbox.winfo_exists():
                theme_listbox.configure(bg=palette['bg_medium'], fg=palette['fg'], selectbackground=palette['accent'], selectforeground='#ffffff')
        except (tk.TclError, AttributeError):
            pass
        menu_widgets = (getattr(self, '_ctx', None), getattr(self, '_colmenu', None), getattr(getattr(self, 'replacer', None), 'ctx_menu', None))
        for menu in menu_widgets:
            if menu is not None:
                try:
                    menu.configure(bg=palette['bg_dark'], fg=palette['fg'], activebackground=palette['accent'], activeforeground='#ffffff')
                except (tk.TclError, AttributeError):
                    pass
        try:
            titlebar = getattr(self, '_titlebar', None)
            canvas = getattr(self, '_titlebar_canvas', None)
            if titlebar is not None and titlebar.winfo_exists():
                titlebar.configure(bg=palette['bg_dark'])
            if canvas is not None and canvas.winfo_exists():
                canvas.configure(bg=palette['bg_dark'])
                canvas.itemconfigure('title', fill=palette['fg'])
                canvas.itemconfigure('spotlight', fill=palette['accent'])
                canvas.itemconfigure('notification_button', fill=palette['fg'])
                for name, (item, command, color) in getattr(self, '_titlebar_buttons', {}).items():
                    canvas.itemconfigure(item, fill=color)
            for child in titlebar.winfo_children() if titlebar is not None else ():
                if isinstance(child, tk.Label):
                    child.configure(bg=palette['bg_dark'], fg=palette['fg'])
        except (tk.TclError, AttributeError):
            pass
        try:
            self._refresh_tab_nav()
        except (tk.TclError, AttributeError):
            pass
        try:
            for popup in list(self.winfo_children()):
                if isinstance(popup, tk.Toplevel):
                    _routils_refresh_popup_chrome(popup)
        except tk.TclError:
            pass
        try:
            if getattr(self, 'viewport_3d', None) is not None and self.viewport_3d.winfo_ismapped():
                self.viewport_3d.draw_frame()
        except (tk.TclError, AttributeError):
            pass
        self._save_settings()
    def _collect_menus(self):
        out = []
        try:
            m = self.nametowidget(self.cget('menu'))
            if m:
                out.append(m)
                for i in range(m.index('end') + 1 if m.index('end') is not None else 0):
                    try:
                        sub = m.entrycget(i, 'menu')
                        if sub:
                            out.append(sub)
                    except Exception:
                        pass
        except Exception:
            pass
        return out
