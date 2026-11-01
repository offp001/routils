import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class EmoteManagerMixin:
    def _emote_refresh_list(self):
        if not hasattr(self, 'emote_tree') or not self.emote_tree.winfo_exists():
            return
        selected = self.emote_tree.selection()
        selected_dance = self.emote_tree.item(selected[0], 'values')[1] if selected else None
        self.emote_tree.delete(*self.emote_tree.get_children())
        for dance in self.emote_names:
            key = self.emote_binds.get(dance, '') or '***'
            self.emote_tree.insert('', 'end', iid=dance, values=(key, dance))
        if selected_dance and selected_dance in self.emote_names:
            self.emote_tree.selection_set(selected_dance)
    def _emote_selected_dance(self):
        if not hasattr(self, 'emote_tree'):
            return None
        selected = self.emote_tree.selection()
        if not selected:
            messagebox.showinfo(UI_TEXT['i5'], UI_TEXT['y13'], parent=self)
            return None
        return self.emote_tree.item(selected[0], 'values')[1]
    def _emote_add_bind(self):
        dance = self._emote_selected_dance()
        if not dance:
            return
        if getattr(self, '_emote_capture_dialog', None):
            try:
                if self._emote_capture_dialog.winfo_exists():
                    self._emote_capture_dialog.destroy()
            except Exception:
                pass
        dlg = tk.Toplevel(self)
        self._emote_capture_dialog = dlg
        dlg.title('Add Bind')
        dlg.transient(self)
        dlg.resizable(False, False)
        theme_toplevel(dlg)
        ttk.Label(dlg, text=UI_TEXT['z13'].format(p0=dance), font=('Segoe UI Semibold', 11)).pack(padx=20, pady=(18, 8))
        key_var = tk.StringVar(value=UI_TEXT['w28'])
        ttk.Label(dlg, textvariable=key_var).pack(padx=20, pady=(0, 18))
        captured = {'key': ''}
        def capture(event):
            if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Win_L', 'Win_R'):
                return 'break'
            key = event.keysym.upper()
            if key == 'ESCAPE':
                key = 'ESC'
            if not fflag_key_to_vk(key):
                return 'break'
            captured['key'] = key
            key_var.set(key)
            self.emote_binds[dance] = key
            self._emote_refresh_list()
            dlg.after(120, dlg.destroy)
            return 'break'
        dlg.bind('<KeyPress>', capture)
        dlg.bind('<Button-1>', lambda _e: dlg.focus_force())
        dlg.after(100, dlg.focus_force)
    def _emote_remove_bind(self):
        dance = self._emote_selected_dance()
        if not dance:
            return
        self.emote_binds[dance] = ''
        self._emote_refresh_list()
    def _emote_save_binds(self):
        used = {}
        all_bindings = [(dance, key) for dance, key in self.emote_binds.items()]
        all_bindings.extend((({'previous': UI_TEXT['r30'], 'next': UI_TEXT['s30'], 'play': UI_TEXT['t30']}.get(action, action), key) for action, key in self._emote_nav_binds.items()))
        all_bindings.append(('Hotkeys Toggle', getattr(self, '_emote_hotkeys_toggle_key', '')))
        for label, key in all_bindings:
            key = str(key or '').upper()
            if key and key in used:
                messagebox.showerror(UI_TEXT['i5'], UI_TEXT['a14'].format(p0=key, p1=used[key]), parent=self)
                return
            if key:
                used[key] = label
        self.settings['emote_binds'] = dict(self.emote_binds)
        self.settings['emote_nav_binds'] = dict(self._emote_nav_binds)
        self._save_settings()
        if hasattr(self, 'emote_status'):
            self.emote_status.config(text=UI_TEXT['b14'], foreground='#65d98b')
        self._emote_refresh_list()
    def _emote_update_control_button_states(self):
        try:
            enabled = bool(getattr(self, '_emote_hotkeys_enabled', True))
            if hasattr(self, '_emote_hotkeys_button') and self._emote_hotkeys_button.winfo_exists():
                self._emote_hotkeys_button.configure(text=UI_TEXT['c14'].format(p0='ON' if enabled else 'OFF'))
            if hasattr(self, '_emote_toggle_hotkey_button') and self._emote_toggle_hotkey_button.winfo_exists():
                self._emote_toggle_hotkey_button.configure(text=self._emote_toggle_hotkey_button_text())
            panel = getattr(self, '_emote_controls_window', None)
            if hasattr(self, '_emote_controls_button') and self._emote_controls_button.winfo_exists():
                self._emote_controls_button.configure(text=UI_TEXT['d14'] if panel is not None and panel.winfo_exists() else UI_TEXT['x13'])
        except Exception:
            pass
    def _emote_toggle_hotkey_button_text(self):
        key = str(getattr(self, '_emote_hotkeys_toggle_key', '') or '').upper()
        return f'Toggle Key: {key}' if key else 'Set Toggle Key'
    def _emote_assign_toggle_hotkey(self):
        existing_dialog = getattr(self, '_emote_toggle_capture_dialog', None)
        if existing_dialog is not None:
            try:
                if existing_dialog.winfo_exists():
                    existing_dialog.lift()
                    existing_dialog.focus_force()
                    return
            except Exception:
                pass
        dlg = tk.Toplevel(self)
        self._emote_toggle_capture_dialog = dlg
        dlg.title('Set Hotkeys Toggle Key')
        dlg.geometry('390x154')
        dlg.resizable(False, False)
        dlg.transient(self)
        theme_toplevel(dlg)
        ttk.Label(dlg, text='Press a key to toggle Emote Manager Hotkeys ON/OFF.', wraplength=350, justify='center').pack(fill='x', padx=16, pady=(20, 7))
        ttk.Label(dlg, text='Escape cancels. Backspace or Delete clears the assigned key.', wraplength=350, justify='center').pack(fill='x', padx=16, pady=(0, 14))
        state = {'closed': False}
        self._emote_toggle_hotkey_capture_active = True
        def close_dialog(clear_capture=True):
            if state['closed']:
                return
            state['closed'] = True
            if clear_capture:
                self._emote_toggle_hotkey_capture_active = False
            try:
                if dlg.winfo_exists():
                    dlg.destroy()
            except Exception:
                pass
            self._emote_toggle_capture_dialog = None
        def capture(event):
            keysym = str(getattr(event, 'keysym', '') or '')
            upper = keysym.upper()
            if upper in ('SHIFT_L', 'SHIFT_R', 'CONTROL_L', 'CONTROL_R', 'ALT_L', 'ALT_R', 'WIN_L', 'WIN_R'):
                return 'break'
            if upper == 'ESCAPE':
                close_dialog()
                return 'break'
            if upper in ('BACKSPACE', 'DELETE'):
                key = ''
            else:
                key = upper
                if key == 'KP_ENTER':
                    key = 'ENTER'
                elif key == 'RETURN':
                    key = 'ENTER'
                elif key == 'SPACE':
                    key = 'SPACE'
            if key and (not fflag_key_to_vk(key)):
                return 'break'
            conflicts = set((str(value or '').upper() for value in getattr(self, 'emote_binds', {}).values() if str(value or '').strip()))
            conflicts.update((str(value or '').upper() for action, value in getattr(self, '_emote_nav_binds', {}).items() if str(value or '').strip()))
            conflicts.update((str(item.get('key', '') or '').upper() for item in getattr(self, 'fflag_hotkeys', []) if isinstance(item, dict) and str(item.get('key', '') or '').strip()))
            conflicts.update((str(value or '').upper() for value in getattr(self, 'fps_hotkeys', {}).values() if str(value or '').strip()))
            conflicts.update(('F7', 'F3'))
            if key and key in conflicts:
                self._emote_set_action_status(f'{key} is already assigned. Choose another key.', '#ff6b6b')
                return 'break'
            self._emote_hotkeys_toggle_key = key
            self.settings['emote_hotkeys_toggle_key'] = key
            vk = fflag_key_to_vk(key) if key else 0
            if vk:
                self._hotkey_prev[vk] = True
            self._save_settings()
            self._emote_update_control_button_states()
            close_dialog()
            self._emote_set_action_status(f'Hotkeys toggle key: {key}' if key else 'Hotkeys toggle key cleared.', '#65d98b')
            return 'break'
        dlg.bind('<KeyPress>', capture)
        dlg.bind('<Escape>', lambda _event: close_dialog())
        dlg.protocol('WM_DELETE_WINDOW', close_dialog)
        dlg.after(100, dlg.focus_force)
    def _set_emote_hotkeys_enabled(self, enabled, persist=True):
        self._emote_hotkeys_enabled = bool(enabled)
        self.settings['emote_hotkeys_enabled'] = self._emote_hotkeys_enabled
        self._emote_update_control_button_states()
        if persist:
            self._save_settings()
    def _toggle_emote_hotkeys(self):
        self._set_emote_hotkeys_enabled(not bool(getattr(self, '_emote_hotkeys_enabled', True)))
        enabled = bool(getattr(self, '_emote_hotkeys_enabled', True))
        self._emote_set_action_status(UI_TEXT['x28'] if enabled else UI_TEXT['y28'], '#65d98b' if enabled else '#f2c94c')
    def _emote_current_dance(self):
        names = list(getattr(self, 'emote_names', ['/e dance1']))
        if not names:
            return '/e dance1'
        self._emote_current_index = max(0, min(int(getattr(self, '_emote_current_index', 0)), len(names) - 1))
        return names[self._emote_current_index]
    def _emote_key_label(self, action):
        key = str(getattr(self, '_emote_nav_binds', {}).get(action, '') or '').upper()
        return key if key else '—'
    def _emote_refresh_controls(self, capture_action=None):
        labels = getattr(self, '_emote_controls_labels', {})
        dance = self._emote_current_dance()
        for action, label in list(labels.items()):
            try:
                if not label.winfo_exists():
                    continue
                if capture_action == action:
                    label.configure(text=UI_TEXT['e14'], fg='#88c7ff')
                elif action == 'previous':
                    label.configure(text=UI_TEXT['f14'].format(p0=self._emote_key_label(action)), fg='#ffffff')
                elif action == 'next':
                    label.configure(text=UI_TEXT['g14'].format(p0=self._emote_key_label(action)), fg='#ffffff')
                elif action == 'play':
                    label.configure(text=UI_TEXT['h14'].format(p0=dance, p1=self._emote_key_label(action)), fg='#ffffff')
            except Exception:
                pass
        self._emote_update_control_button_states()
    def _emote_controls_remove_duplicate_windows(self):
        if os.name != 'nt':
            return
        try:
            user32 = ctypes.windll.user32
            panel = getattr(self, '_emote_controls_window', None)
            keep_hwnd = _win32_root_hwnd(panel) if panel is not None and panel.winfo_exists() else 0
            enum_proc_type = getattr(ctypes, 'WINFUNCTYPE', ctypes.CFUNCTYPE)
            callback_type = enum_proc_type(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            def visit(hwnd, _lparam):
                try:
                    hwnd_value = int(hwnd)
                    if keep_hwnd and hwnd_value == int(keep_hwnd):
                        return True
                    length = int(user32.GetWindowTextLengthW(hwnd))
                    buffer = ctypes.create_unicode_buffer(max(2, length + 2))
                    user32.GetWindowTextW(hwnd, buffer, len(buffer))
                    window_title = buffer.value.strip().casefold()
                    rect = ctypes.wintypes.RECT()
                    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                        return True
                    width = int(rect.right - rect.left)
                    height = int(rect.bottom - rect.top)
                    small_window = 140 <= width <= 360 and 55 <= height <= 190
                    is_emote_window = 'emote manager - hide: ctrl + f3' in window_title or (window_title == 'routils' and small_window)
                    if is_emote_window and small_window:
                        user32.ShowWindow(hwnd, 0)
                        user32.PostMessageW(hwnd, 16, 0, 0)
                except Exception:
                    pass
                return True
            callback = callback_type(visit)
            user32.EnumWindows.argtypes = [callback_type, ctypes.wintypes.LPARAM]
            user32.EnumWindows.restype = ctypes.wintypes.BOOL
            user32.EnumWindows(callback, 0)
        except Exception:
            pass
    def _toggle_emote_controls(self):
        panel = getattr(self, '_emote_controls_window', None)
        if panel is not None:
            try:
                if panel.winfo_exists():
                    panel.destroy()
            except Exception:
                pass
            self._emote_controls_window = None
            self._emote_controls_labels = {}
            self._emote_control_capture_action = None
            job = getattr(self, '_emote_controls_position_job', None)
            if job is not None:
                try:
                    self.after_cancel(job)
                except Exception:
                    pass
            self._emote_controls_position_job = None
            self._emote_update_control_button_states()
            return
        self._set_emote_hotkeys_enabled(True, persist=True)
        self._emote_controls_remove_duplicate_windows()
        tk._routils_skip_next_popup_chrome = True
        try:
            panel = tk.Toplevel(self)
        finally:
            tk._routils_skip_next_popup_chrome = False
        panel.title('Emote Manager - Hide: Ctrl + F3')
        panel._skip_custom_chrome = True
        panel._skip_popup_centering = True
        panel.withdraw()
        self._emote_controls_window = panel
        panel.overrideredirect(True)
        panel.resizable(False, False)
        try:
            panel.attributes('-topmost', True)
        except Exception:
            pass
        palette = _CURRENT_PALETTE if isinstance(_CURRENT_PALETTE, dict) else THEMES[DEFAULT_THEME]
        surface = palette.get('bg_medium', '#252526')
        topbar_bg = _routils_darken_color(palette.get('bg_dark', '#1b1b1c'), 0.16)
        fg = palette.get('fg', '#eeeeee')
        accent = palette.get('accent', '#7f8cff')
        border = palette.get('border', '#444446')
        hover_bg = palette.get('bg_hover', '#464648')
        panel.configure(bg=surface, bd=0, highlightthickness=0, relief='flat')
        try:
            panel.minsize(180, 80)
            panel.maxsize(180, 80)
        except Exception:
            pass
        panel.geometry('180x80+0+0')
        shell = tk.Frame(panel, bg=surface, bd=0, highlightthickness=0, relief='flat')
        shell.pack(fill='both', expand=True, padx=0, pady=0)
        topbar = tk.Frame(shell, bg=topbar_bg, height=17, bd=0, highlightthickness=0, relief='flat')
        topbar.pack(fill='x', side='top')
        topbar.pack_propagate(False)
        title = tk.Label(topbar, text=UI_TEXT['i14'], bg=topbar_bg, fg=fg, font=('Segoe UI Semibold', 8), anchor='w', bd=0, highlightthickness=0)
        title.pack(side='left', fill='both', expand=True, padx=(7, 2))
        close = tk.Label(topbar, text=UI_TEXT['e5'], bg=topbar_bg, fg='#ff7a82', font=('Segoe UI', 10), width=2, cursor='hand2', bd=0, highlightthickness=0)
        close.pack(side='right', fill='y')
        close.bind('<Button-1>', lambda _e: self._toggle_emote_controls())
        close.bind('<Enter>', lambda _e: close.configure(bg='#542a31'))
        close.bind('<Leave>', lambda _e: close.configure(bg=topbar_bg))
        row = tk.Frame(shell, bg=surface, bd=0, highlightthickness=0, relief='flat')
        row.pack(fill='both', expand=True, padx=2, pady=(2, 1))
        previous = tk.Label(row, text=UI_TEXT['m1'], bg=surface, fg=fg, font=('Segoe UI Semibold', 8), cursor='hand2', relief='flat', bd=0, highlightthickness=1, highlightbackground=border, highlightcolor=border, justify='center', wraplength=36, anchor='center')
        current = tk.Label(row, text=UI_TEXT['m1'], bg=surface, fg=fg, font=('Segoe UI Semibold', 8), cursor='hand2', relief='flat', bd=0, highlightthickness=1, highlightbackground=border, highlightcolor=border, justify='center', wraplength=78, anchor='center')
        next_label = tk.Label(row, text=UI_TEXT['m1'], bg=surface, fg=fg, font=('Segoe UI Semibold', 8), cursor='hand2', relief='flat', bd=0, highlightthickness=1, highlightbackground=border, highlightcolor=border, justify='center', wraplength=36, anchor='center')
        previous.place(x=1, y=1, width=40, height=57)
        current.place(x=45, y=1, width=84, height=57)
        next_label.place(x=133, y=1, width=40, height=57)
        self._emote_controls_labels = {'previous': previous, 'play': current, 'next': next_label}
        previous.bind('<Button-1>', lambda _e: self._emote_begin_key_capture('previous'))
        next_label.bind('<Button-1>', lambda _e: self._emote_begin_key_capture('next'))
        current.bind('<Button-1>', lambda _e: self._emote_begin_key_capture('play'))
        def set_button_hover(widget, hovering):
            try:
                if not widget.winfo_exists():
                    return
                if hovering:
                    widget.configure(bg=hover_bg, highlightbackground=accent, highlightcolor=accent)
                else:
                    widget.configure(bg=surface, highlightbackground=border, highlightcolor=border)
            except Exception:
                pass
        for label in (previous, current, next_label):
            label.bind('<Enter>', lambda _e, w=label: set_button_hover(w, True))
            def leave_button(event, widget=label):
                def clear_if_outside():
                    try:
                        if not widget.winfo_exists():
                            return
                        px, py = (widget.winfo_pointerx(), widget.winfo_pointery())
                        target = widget.winfo_containing(px, py)
                        if target is not widget:
                            set_button_hover(widget, False)
                    except Exception:
                        set_button_hover(widget, False)
                try:
                    widget.after_idle(clear_if_outside)
                except Exception:
                    set_button_hover(widget, False)
            label.bind('<Leave>', leave_button)
        panel.bind('<KeyPress>', self._emote_controls_keypress, add='+')
        panel.bind('<Escape>', lambda _e: self._toggle_emote_controls(), add='+')
        panel.bind('<Destroy>', self._emote_controls_destroyed, add='+')
        self._emote_refresh_controls()
        self._emote_update_control_button_states()
        self._emote_controls_position_tick()
        try:
            panel.deiconify()
            panel.lift()
            panel.focus_force()
            panel.update_idletasks()
            self._emote_controls_detach_from_main()
        except Exception:
            pass
    def _emote_controls_detach_from_main(self, no_activate=False):
        panel = getattr(self, '_emote_controls_window', None)
        if panel is None or os.name != 'nt':
            return
        try:
            if not panel.winfo_exists():
                return
            native_hwnd = _win32_root_hwnd(panel)
            if not native_hwnd:
                native_hwnd = int(panel.winfo_id())
            hwnd = ctypes.wintypes.HWND(native_hwnd)
            user32 = ctypes.windll.user32
            get_long = getattr(user32, 'GetWindowLongPtrW', None)
            set_long = getattr(user32, 'SetWindowLongPtrW', None)
            if get_long is None:
                get_long = user32.GetWindowLongW
            if set_long is None:
                set_long = user32.SetWindowLongW
            get_long.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
            get_long.restype = ctypes.c_ssize_t
            set_long.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
            set_long.restype = ctypes.c_ssize_t
            owner = get_long(hwnd, -8)
            if owner:
                set_long(hwnd, -8, 0)
            ex_style = get_long(hwnd, -20)
            ex_style |= 128
            ex_style &= ~262144
            if no_activate:
                ex_style |= 134217728
            else:
                ex_style &= ~134217728
            set_long(hwnd, -20, ex_style)
            user32.SetWindowPos.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.wintypes.UINT]
            user32.SetWindowPos.restype = ctypes.wintypes.BOOL
            flags = 1 | 2 | 16 | 64
            user32.SetWindowPos(hwnd, ctypes.wintypes.HWND(-1), 0, 0, 0, 0, flags)
            if no_activate:
                user32.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
                user32.ShowWindow.restype = ctypes.wintypes.BOOL
                user32.ShowWindow(hwnd, 8)
            try:
                panel.attributes('-topmost', True)
            except Exception:
                pass
            self._emote_controls_noactivate = bool(no_activate)
        except Exception:
            try:
                panel.attributes('-topmost', True)
                if not no_activate:
                    panel.lift()
            except Exception:
                pass
    def _emote_controls_ensure_visible_after_hide(self):
        panel = getattr(self, '_emote_controls_window', None)
        if panel is None:
            return
        try:
            if not panel.winfo_exists():
                return
            if panel.state() in ('withdrawn', 'iconic'):
                panel.deiconify()
            panel.update_idletasks()
            self._emote_controls_position_tick()
            self._emote_controls_detach_from_main(no_activate=True)
            if os.name == 'nt':
                native_hwnd = _win32_root_hwnd(panel)
                if not native_hwnd:
                    native_hwnd = int(panel.winfo_id())
                hwnd = ctypes.wintypes.HWND(native_hwnd)
                user32 = ctypes.windll.user32
                user32.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
                user32.ShowWindow.restype = ctypes.wintypes.BOOL
                user32.ShowWindow(hwnd, 8)
                user32.SetWindowPos(hwnd, ctypes.wintypes.HWND(-1), 0, 0, 0, 0, 1 | 2 | 16 | 64)
        except Exception:
            pass
    def _emote_controls_restore_activation(self):
        panel = getattr(self, '_emote_controls_window', None)
        if panel is None:
            return
        try:
            if not panel.winfo_exists():
                return
            if panel.state() in ('withdrawn', 'iconic'):
                panel.deiconify()
            self._emote_controls_detach_from_main(no_activate=False)
            panel.attributes('-topmost', True)
        except Exception:
            pass
    def _emote_controls_position_tick(self):
        panel = getattr(self, '_emote_controls_window', None)
        if panel is None:
            self._emote_controls_position_job = None
            return
        try:
            if not panel.winfo_exists():
                self._emote_controls_position_job = None
                return
            width, height = (180, 80)
            left, top = (0, 0)
            right = int(panel.winfo_screenwidth())
            bottom = int(panel.winfo_screenheight())
            try:
                if sys.platform == 'win32':
                    class RECT(ctypes.Structure):
                        _fields_ = [('left', ctypes.wintypes.LONG), ('top', ctypes.wintypes.LONG), ('right', ctypes.wintypes.LONG), ('bottom', ctypes.wintypes.LONG)]
                    rect = RECT()
                    if ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(rect), 0):
                        left, top, right, bottom = (rect.left, rect.top, rect.right, rect.bottom)
            except Exception:
                pass
            x = max(left + 2, right - width - 12)
            y = max(top + 2, bottom - height - 12)
            expected = f'{width}x{height}{x:+d}{y:+d}'
            if panel.geometry() != expected:
                panel.geometry(expected)
            try:
                scan_at = float(getattr(self, '_emote_duplicate_scan_at', 0.0))
                if time.monotonic() >= scan_at:
                    self._emote_duplicate_scan_at = time.monotonic() + 1.0
                    self._emote_controls_remove_duplicate_windows()
                main_state = self.state()
                main_hidden = bool(getattr(self, '_tray_hidden', False)) or main_state in ('iconic', 'withdrawn')
                if main_hidden:
                    if panel.state() in ('withdrawn', 'iconic'):
                        panel.deiconify()
                    self._emote_controls_detach_from_main(no_activate=True)
                    if os.name == 'nt':
                        native_hwnd = _win32_root_hwnd(panel)
                        if not native_hwnd:
                            native_hwnd = int(panel.winfo_id())
                        hwnd = ctypes.wintypes.HWND(native_hwnd)
                        ctypes.windll.user32.ShowWindow(hwnd, 8)
                else:
                    if getattr(self, '_emote_controls_noactivate', False):
                        self._emote_controls_detach_from_main(no_activate=False)
                    panel.attributes('-topmost', True)
                    panel.lift()
            except Exception:
                pass
            self._emote_controls_position_job = self.after(250, self._emote_controls_position_tick)
        except Exception:
            self._emote_controls_position_job = None
    def _emote_controls_destroyed(self, event=None):
        try:
            if event is not None and getattr(event, 'widget', None) is self._emote_controls_window:
                self._emote_controls_window = None
                self._emote_controls_labels = {}
                self._emote_control_capture_action = None
                job = getattr(self, '_emote_controls_position_job', None)
                if job is not None:
                    try:
                        self.after_cancel(job)
                    except Exception:
                        pass
                self._emote_controls_position_job = None
                self._emote_update_control_button_states()
        except Exception:
            pass
    def _emote_begin_key_capture(self, action):
        if action not in ('previous', 'next', 'play'):
            return
        panel = getattr(self, '_emote_controls_window', None)
        if panel is None or not panel.winfo_exists():
            return
        self._emote_control_capture_action = action
        self._emote_refresh_controls(capture_action=action)
        try:
            self._emote_controls_detach_from_main(no_activate=False)
            panel.lift()
            panel.focus_force()
        except Exception:
            pass
    def _emote_controls_keypress(self, event):
        action = getattr(self, '_emote_control_capture_action', None)
        if not action:
            return None
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Win_L', 'Win_R'):
            return 'break'
        key = str(event.keysym or '').upper()
        if key == 'ESCAPE':
            self._emote_control_capture_action = None
            self._emote_refresh_controls()
            try:
                main_hidden = bool(getattr(self, '_tray_hidden', False)) or self.state() in ('iconic', 'withdrawn')
                if main_hidden:
                    self._emote_controls_detach_from_main(no_activate=True)
            except Exception:
                pass
            return 'break'
        if key in ('SPACE', 'RETURN', 'KP_ENTER'):
            key = {'SPACE': 'SPACE', 'RETURN': 'ENTER', 'KP_ENTER': 'ENTER'}[key]
        if not key or not fflag_key_to_vk(key):
            return 'break'
        all_existing = {str(v or '').upper() for v in self.emote_binds.values() if str(v or '').strip()}
        all_existing.update((str(v or '').upper() for k, v in self._emote_nav_binds.items() if k != action and str(v or '').strip()))
        all_existing.update((str(item.get('key', '') or '').upper() for item in getattr(self, 'fflag_hotkeys', []) if isinstance(item, dict)))
        all_existing.update((str(v or '').upper() for v in getattr(self, 'fps_hotkeys', {}).values() if str(v or '').strip()))
        all_existing.add('F7')
        all_existing.add(str(getattr(self, '_emote_hotkeys_toggle_key', '') or '').upper())
        if key in all_existing:
            self._emote_control_capture_action = None
            self._emote_refresh_controls()
            self._emote_set_action_status(f'{key} is already assigned. Choose another key.', '#ff6b6b')
            try:
                main_hidden = bool(getattr(self, '_tray_hidden', False)) or self.state() in ('iconic', 'withdrawn')
                if main_hidden:
                    self._emote_controls_detach_from_main(no_activate=True)
            except Exception:
                pass
            return 'break'
        self._emote_nav_binds[action] = key
        try:
            main_hidden = bool(getattr(self, '_tray_hidden', False)) or self.state() in ('iconic', 'withdrawn')
            if main_hidden:
                self._emote_controls_detach_from_main(no_activate=True)
        except Exception:
            pass
        vk = fflag_key_to_vk(key)
        if vk:
            self._hotkey_prev[vk] = True
        self._emote_control_capture_action = None
        self.settings['emote_nav_binds'] = dict(self._emote_nav_binds)
        self._save_settings()
        self._emote_refresh_controls()
        action_text = {'previous': UI_TEXT['r30'], 'next': UI_TEXT['s30'], 'play': UI_TEXT['t30']}.get(action, action)
        self._emote_set_action_status(f"{action_text}{UI_TEXT['c33']}{key}.", '#65d98b')
        return 'break'
    def _handle_emote_nav_hotkey(self, binding):
        action = str(binding.get('action', '')).lower()
        key = str(binding.get('key', '')).upper()
        if action == 'previous':
            self._emote_current_index = (self._emote_current_index - 1) % len(self.emote_names)
            self._emote_refresh_controls()
            self._emote_set_action_status(f"{UI_TEXT['u30']}{self._emote_current_dance()}", '#65d98b')
        elif action == 'next':
            self._emote_current_index = (self._emote_current_index + 1) % len(self.emote_names)
            self._emote_refresh_controls()
            self._emote_set_action_status(f"{UI_TEXT['u30']}{self._emote_current_dance()}", '#65d98b')
        elif action == 'play':
            self._handle_emote_hotkey({'key': key, 'dance': self._emote_current_dance()})
    def _emote_status_tick(self):
        if not getattr(self, 'winfo_exists', lambda: False)():
            return
        if hasattr(self, 'emote_status') and self.emote_status.winfo_exists():
            pid = self.fflag_pid if getattr(self, 'fflag_pid', 0) else _fflag_find_pid()
            if pid:
                self.emote_status.config(text=UI_TEXT['j14'].format(p0=pid), foreground='#65d98b')
            else:
                self.emote_status.config(text=UI_TEXT['q13'], foreground='#9aa0a6')
        self.after(1000, self._emote_status_tick)
    def _emote_set_action_status(self, message, color='#9aa0a6'):
        try:
            if hasattr(self, 'emote_action_status') and self.emote_action_status.winfo_exists():
                self.emote_action_status.config(text=message, foreground=color)
        except Exception:
            pass
    def _handle_emote_hotkey(self, binding):
        dance = str(binding.get('dance', '')).strip()
        key = str(binding.get('key', '')).upper()
        if dance not in self.emote_names:
            return
        with self._emote_typing_lock:
            if self._emote_typing_active:
                return
            self._emote_typing_active = True
        self._emote_set_action_status(f"{UI_TEXT['a33']}{key} → {dance}{UI_TEXT['b33']}", '#f2c94c')
        worker = threading.Thread(target=self._emote_type_command, args=(dance, key), daemon=True, name='RoUtilsEmote')
        try:
            worker.start()
        except Exception as e:
            with self._emote_typing_lock:
                self._emote_typing_active = False
            self._emote_set_action_status(f"{UI_TEXT['v30']}{e}", '#ff6b6b')
    def _emote_type_command(self, dance, key=''):
        user32 = None
        foreground = None
        thread_id = 0
        old_layout = None
        english_layout = None
        pressed_keys = set()
        def status(message, color='#9aa0a6'):
            try:
                self.after(0, lambda message=message, color=color: self._emote_set_action_status(message, color))
            except Exception:
                pass
        try:
            if sys.platform.startswith('linux'):
                roblox_pid = self.fflag_pid or _fflag_find_pid()
                if not roblox_pid:
                    status(f'{key} → {dance}: Sober not detected.', '#ff6b6b')
                    return
                success, detail = type_sober_emote(dance, roblox_pid)
                status(f'{key} → {dance}: {detail}', '#65d98b' if success else '#ff6b6b')
                return
            if sys.platform != 'win32':
                status(UI_TEXT['v27'], '#ff6b6b')
                return
            roblox_pid = self.fflag_pid or _fflag_find_pid()
            if not roblox_pid:
                status(f'{key} → {dance}: Roblox not detected.', '#ff6b6b')
                return
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            user32.GetForegroundWindow.restype = ctypes.wintypes.HWND
            user32.GetWindowThreadProcessId.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.DWORD)]
            user32.GetWindowThreadProcessId.restype = ctypes.wintypes.DWORD
            user32.GetKeyboardLayout.argtypes = [ctypes.wintypes.DWORD]
            user32.GetKeyboardLayout.restype = ctypes.c_void_p
            user32.LoadKeyboardLayoutW.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.UINT]
            user32.LoadKeyboardLayoutW.restype = ctypes.c_void_p
            user32.SendMessageTimeoutW.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.c_size_t, ctypes.c_ssize_t, ctypes.wintypes.UINT, ctypes.wintypes.UINT, ctypes.POINTER(ctypes.c_size_t)]
            user32.SendMessageTimeoutW.restype = ctypes.c_ssize_t
            user32.VkKeyScanExW.argtypes = [ctypes.wintypes.WCHAR, ctypes.c_void_p]
            user32.VkKeyScanExW.restype = ctypes.c_short
            user32.MapVirtualKeyExW.argtypes = [ctypes.wintypes.UINT, ctypes.wintypes.UINT, ctypes.c_void_p]
            user32.MapVirtualKeyExW.restype = ctypes.wintypes.UINT
            ULONG_PTR = ctypes.wintypes.WPARAM
            class MOUSEINPUT(ctypes.Structure):
                _fields_ = [('dx', ctypes.wintypes.LONG), ('dy', ctypes.wintypes.LONG), ('mouseData', ctypes.wintypes.DWORD), ('dwFlags', ctypes.wintypes.DWORD), ('time', ctypes.wintypes.DWORD), ('dwExtraInfo', ULONG_PTR)]
            class KEYBDINPUT(ctypes.Structure):
                _fields_ = [('wVk', ctypes.wintypes.WORD), ('wScan', ctypes.wintypes.WORD), ('dwFlags', ctypes.wintypes.DWORD), ('time', ctypes.wintypes.DWORD), ('dwExtraInfo', ULONG_PTR)]
            class HARDWAREINPUT(ctypes.Structure):
                _fields_ = [('uMsg', ctypes.wintypes.DWORD), ('wParamL', ctypes.wintypes.WORD), ('wParamH', ctypes.wintypes.WORD)]
            class INPUTUNION(ctypes.Union):
                _fields_ = [('mi', MOUSEINPUT), ('ki', KEYBDINPUT), ('hi', HARDWAREINPUT)]
            class INPUT(ctypes.Structure):
                _fields_ = [('type', ctypes.wintypes.DWORD), ('u', INPUTUNION)]
            user32.SendInput.argtypes = [ctypes.wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
            user32.SendInput.restype = ctypes.wintypes.UINT
            WM_INPUTLANGCHANGEREQUEST = 80
            KLF_ACTIVATE = 1
            KLF_SUBSTITUTE_OK = 2
            SMTO_ABORTIFHUNG = 2
            KEYEVENTF_KEYUP = 2
            KEYEVENTF_SCANCODE = 8
            KEYEVENTF_EXTENDEDKEY = 1
            MAPVK_VK_TO_VSC_EX = 4
            VK_SHIFT = 16
            VK_RETURN = 13
            foreground = user32.GetForegroundWindow()
            foreground_pid = ctypes.wintypes.DWORD(0)
            if foreground:
                user32.GetWindowThreadProcessId(foreground, ctypes.byref(foreground_pid))
            if not foreground or int(foreground_pid.value) != int(roblox_pid):
                status(f'{key} → {dance}: Roblox is not focused.', '#ff6b6b')
                return
            thread_id = user32.GetWindowThreadProcessId(foreground, None)
            old_layout = user32.GetKeyboardLayout(thread_id)
            if not old_layout:
                raise OSError('Could not read the current keyboard layout')
            english_layout = user32.LoadKeyboardLayoutW('00000409', KLF_ACTIVATE | KLF_SUBSTITUTE_OK)
            if not english_layout:
                raise OSError('Could not load English (US) keyboard layout')
            def switch_layout(layout, timeout=1.5):
                if not layout:
                    raise OSError('Keyboard layout handle is invalid')
                result = ctypes.c_size_t(0)
                sent = user32.SendMessageTimeoutW(foreground, WM_INPUTLANGCHANGEREQUEST, 0, ctypes.c_ssize_t(int(layout)).value, SMTO_ABORTIFHUNG, int(timeout * 1000), ctypes.byref(result))
                if not sent:
                    raise OSError('Windows did not accept the keyboard layout change')
                deadline = time.monotonic() + timeout
                while time.monotonic() < deadline:
                    current = user32.GetKeyboardLayout(thread_id)
                    if current and int(current) == int(layout):
                        return True
                    time.sleep(0.025)
                current = user32.GetKeyboardLayout(thread_id)
                if not current or int(current) != int(layout):
                    raise OSError('Keyboard layout did not change in Roblox')
                return True
            scan_code_cache = {}
            def send_key_event(vk, key_up=False):
                vk = int(vk) & 255
                scan_info = scan_code_cache.get(vk)
                if scan_info is None:
                    mapped = int(user32.MapVirtualKeyExW(vk, MAPVK_VK_TO_VSC_EX, english_layout))
                    if not mapped:
                        raise OSError(f'Could not map virtual key {vk} to an English keyboard scan code')
                    scan = mapped & 255
                    extended = mapped & 65280 in (57344, 57600)
                    scan_info = (scan, extended)
                    scan_code_cache[vk] = scan_info
                scan, extended = scan_info
                flags = KEYEVENTF_SCANCODE
                if key_up:
                    flags |= KEYEVENTF_KEYUP
                if extended:
                    flags |= KEYEVENTF_EXTENDEDKEY
                item = INPUT()
                item.type = 1
                item.u.ki.wVk = 0
                item.u.ki.wScan = scan
                item.u.ki.dwFlags = flags
                item.u.ki.time = 0
                item.u.ki.dwExtraInfo = 0
                sent = user32.SendInput(1, ctypes.byref(item), ctypes.sizeof(INPUT))
                if sent != 1:
                    error = ctypes.get_last_error()
                    raise OSError(error, f'SendInput failed for English scan code {scan:#x}')
            def key_down(vk):
                vk = int(vk) & 255
                send_key_event(vk, False)
                pressed_keys.add(vk)
            def key_up(vk):
                vk = int(vk) & 255
                send_key_event(vk, True)
                pressed_keys.discard(vk)
            def tap_vk(vk, shift=False):
                if shift:
                    key_down(VK_SHIFT)
                    time.sleep(0.00115)
                try:
                    key_down(vk)
                    time.sleep(0.0019)
                finally:
                    if int(vk) & 255 in pressed_keys:
                        key_up(vk)
                time.sleep(0.0019)
                if shift and VK_SHIFT in pressed_keys:
                    key_up(VK_SHIFT)
                    time.sleep(0.00115)
            def tap_character(character):
                mapping = user32.VkKeyScanExW(character, english_layout)
                if mapping == -1:
                    raise OSError(f'Character cannot be mapped on English (US): {character!r}')
                vk = mapping & 255
                modifiers = mapping >> 8 & 255
                if modifiers & 6:
                    raise OSError(f'Unsupported keyboard modifier for character: {character!r}')
                tap_vk(vk, bool(modifiers & 1))
            status(f'{key} → {dance}: switching to English keyboard...', '#f2c94c')
            switch_layout(english_layout)
            command_name = str(dance).strip()
            if command_name.lower().startswith('/e '):
                command_name = command_name[3:].strip()
            command_name = command_name.strip(' \'"')
            if not command_name:
                raise ValueError('Emote command is empty')
            if not re.fullmatch('[A-Za-z0-9_-]+', command_name):
                raise ValueError('Emote name contains unsupported characters')
            status(f'{key} → {dance}: opening chat and typing command...', '#f2c94c')
            text_to_type = f'//e {command_name}'
            for index, character in enumerate(text_to_type):
                tap_character(character)
                if index == 0:
                    time.sleep(0.08)
                else:
                    time.sleep(0.0015)
            time.sleep(0.013)
            tap_vk(VK_RETURN)
            time.sleep(0.3)
            status(f'{key} → {dance}: command sent; restoring keyboard...', '#65d98b')
        except Exception as e:
            status(f"{UI_TEXT['v30']}{e}", '#ff6b6b')
        finally:
            if user32 is not None:
                for vk in tuple(pressed_keys):
                    try:
                        send_key_event(vk, True)
                    except Exception:
                        pass
                pressed_keys.clear()
                if foreground and old_layout:
                    try:
                        result = ctypes.c_size_t(0)
                        user32.SendMessageTimeoutW(foreground, 80, 0, ctypes.c_ssize_t(int(old_layout)).value, 2, 1500, ctypes.byref(result))
                        deadline = time.monotonic() + 1.0
                        while time.monotonic() < deadline:
                            current = user32.GetKeyboardLayout(thread_id)
                            if current and int(current) == int(old_layout):
                                break
                            time.sleep(0.025)
                    except Exception:
                        pass
            time.sleep(0.15)
            try:
                with self._emote_typing_lock:
                    self._emote_typing_active = False
            except Exception:
                self._emote_typing_active = False
