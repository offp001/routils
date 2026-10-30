import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class ViewerMixin:
    def _build_viewer_widgets(self):
        top = ttk.Frame(self.viewer_root, padding=(8, 6))
        top.pack(fill='x')
        self._cache_top = top
        self._cache_toolbar_toggles = [ttk.Checkbutton(top, style='TCheckbutton', text=UI_TEXT['x22'], variable=self.autoscroll), ttk.Checkbutton(top, style='TCheckbutton', text=UI_TEXT['y22'], variable=self.hide_tickets, command=self._apply_filter), ttk.Checkbutton(top, style='TCheckbutton', text=UI_TEXT['z22'], variable=self.stay_on_top, command=self._apply_stay_on_top), ttk.Checkbutton(top, style='TCheckbutton', text=UI_TEXT['a23'], variable=self.show_lines, command=self._apply_show_lines)]
        for i, widget in enumerate(self._cache_toolbar_toggles):
            widget.grid(row=0, column=i, sticky='w', padx=(0 if i == 0 else 4, 0))
        self.btn_clear = ttk.Button(top, text=UI_TEXT['b23'], command=self._clear_storage_now)
        self.btn_clear.grid(row=0, column=5, sticky='e', padx=(0, 6))
        self.btn_delete_type = ttk.Button(top, text=UI_TEXT['c23'], command=self._open_delete_cache_type)
        self.btn_delete_type.grid(row=0, column=6, sticky='e', padx=(0, 6))
        self.toggle_btn = ttk.Button(top, text=UI_TEXT['d23'], command=self._toggle_watch)
        self.toggle_btn.grid(row=0, column=7, sticky='e', padx=(0, 6))
        self._watch_loading_label = ttk.Label(top, text=UI_TEXT['m1'], foreground='#f2c94c')
        self._watch_loading_label.grid(row=0, column=9, sticky='w', padx=(4, 0))
        self.btn_dump = ttk.Button(top, text=UI_TEXT['e23'], command=self._dump_all_caches)
        self.btn_dump.grid(row=0, column=8, sticky='e')
        self._cache_db_label = None
        self.db_label = None
        self._cache_type_label = ttk.Label(top, text=UI_TEXT['f23'])
        self._cache_type_label.grid(row=2, column=0, sticky='w', pady=(4, 0))
        type_combo = ttk.Combobox(top, textvariable=self.type_filter, values=[t[0] for t in TYPE_FILTERS], state='readonly', width=14)
        self._cache_type_combo = type_combo
        type_combo.grid(row=2, column=1, sticky='w', padx=(8, 0), pady=(4, 0))
        type_combo.bind('<<ComboboxSelected>>', lambda e: self.after_idle(self._safe_apply_filter))
        self._cache_filter_label = ttk.Label(top, text=UI_TEXT['w1'])
        self._cache_filter_label.grid(row=3, column=0, sticky='w', pady=(4, 0))
        f_entry = ttk.Entry(top, textvariable=self.filter_text)
        self._cache_filter_entry = f_entry
        f_entry.grid(row=3, column=1, columnspan=6, sticky='ew', pady=(4, 0))
        f_entry.bind('<KeyRelease>', lambda e: self._schedule_ui('cache_filter', 120, self._apply_filter))
        for c in (3, 4):
            top.columnconfigure(c, weight=1)
        for c in (5, 6, 7, 8):
            top.columnconfigure(c, weight=0)
        top.bind('<Configure>', lambda _e: self._schedule_ui('cache_toolbar', 80, self._responsive_cache_toolbar), add='+')
        self.after_idle(self._responsive_cache_toolbar)
        self.vpaned = ttk.PanedWindow(self.viewer_root, orient='vertical')
        self.vpaned.pack(fill='both', expand=True, padx=8, pady=(0, 6))
        self.table_frame = ttk.Frame(self.vpaned)
        self.vpaned.add(self.table_frame, weight=3)
        _set_pane_minsize(self.vpaned, self.table_frame, 200)
        columns = ('time', 'name', 'hash', 'size', 'kind', 'src')
        self.columns = columns
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', selectmode='extended')
        self.tree.heading('time', text=UI_TEXT['g23'], command=lambda: self._sort_by('time'))
        self.tree.heading('name', text=UI_TEXT['y12'], command=lambda: self._sort_by('name'))
        self.tree.heading('hash', text=UI_TEXT['h23'], command=lambda: self._sort_by('hash'))
        self.tree.heading('size', text=UI_TEXT['i23'], command=lambda: self._sort_by('size', numeric=True))
        self.tree.heading('kind', text=UI_TEXT['l14'], command=lambda: self._sort_by('kind'))
        self.tree.heading('src', text=UI_TEXT['j23'], command=lambda: self._sort_by('src'))
        self.tree.column('time', width=70, minwidth=60, anchor='w', stretch=True)
        self.tree.column('name', width=140, minwidth=80, anchor='w', stretch=True)
        self.tree.column('hash', width=200, minwidth=200, anchor='w', stretch=True)
        self.tree.column('size', width=70, minwidth=60, anchor='w', stretch=True)
        self.tree.column('kind', width=150, minwidth=120, anchor='w', stretch=True)
        self.tree.column('src', width=80, minwidth=60, anchor='w', stretch=True)
        vsb = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)
        self.tree.tag_configure('hover', background='#333333')
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        self.tree.bind('<Delete>', lambda e: self._action_delete_blob())
        self.tree.bind('<F2>', lambda e: self._action_change_hash())
        self._ctx = tk.Menu(self, tearoff=0)
        self._ctx.add_command(label=UI_TEXT['k23'], command=self._export_selected_full)
        self._ctx.add_command(label=UI_TEXT['l23'], command=self._export_selected_rbxm)
        self._ctx_rbxm_index = self._ctx.index('end')
        self._ctx.add_command(label=UI_TEXT['m23'], command=self._export_selected_mesh_obj)
        self._ctx_obj_index = self._ctx.index('end')
        self._ctx.add_command(label=UI_TEXT['n23'], command=self._export_selected_image)
        self._ctx_img_index = self._ctx.index('end')
        self._ctx.add_command(label=UI_TEXT['o23'], command=self._export_selected_video)
        self._ctx_video_index = self._ctx.index('end')
        self._ctx.add_separator()
        for lbl, cmd in [(UI_TEXT['w27'], self._action_change_hash), (UI_TEXT['x27'], self._action_delete_blob)]:
            self._ctx.add_command(label=lbl, command=cmd)
        self._ctx.add_separator()
        self._ctx.add_command(label=UI_TEXT['p23'], command=lambda: self._copy_selected_hash())
        self._ctx.add_separator()
        self._ctx.add_command(label=UI_TEXT['q23'], command=self._action_save_hash_to_saves)
        self._ctx.add_command(label=UI_TEXT['r23'], command=self._action_save_blob_to_saves)
        darken_menus((self._ctx,))
        self._col_vars = {}
        self._colmenu = tk.Menu(self, tearoff=0)
        col_defs = {'time': (UI_TEXT['y27'], True), 'name': (UI_TEXT['z27'], True), 'hash': (UI_TEXT['h23'], True), 'size': (UI_TEXT['i23'], True), 'kind': (UI_TEXT['a28'], True), 'src': (UI_TEXT['b28'], False)}
        for col in self.columns:
            label, default = col_defs[col]
            var = tk.BooleanVar(value=self.settings.get('columns', {}).get(col, default))
            self._col_vars[col] = var
            self._colmenu.add_checkbutton(label=label, variable=var, command=self._update_displaycolumns)
        self._update_displaycolumns(save=False)
        darken_menus((self._colmenu,))
        self.tree.bind('<Button-3>', self._on_tree_right_click)
        self.tree.bind('<Control-Button-1>', self._on_tree_right_click)
        self.tree.bind('<Motion>', self._on_tree_motion)
        self.tree.bind('<Leave>', self._on_tree_leave)
        self.details = ttk.Frame(self.vpaned)
        self.vpaned.add(self.details, weight=2)
        _set_pane_minsize(self.vpaned, self.details, 100)
        self.detail_pane = ttk.PanedWindow(self.details, orient='horizontal')
        self.detail_pane.pack(fill='both', expand=True)
        self.viewport_host = ttk.Frame(self.detail_pane)
        self.detail_pane.add(self.viewport_host, weight=2)
        self.viewport_3d = Viewport3DPanel(self.viewport_host)
        self.viewport_3d.is_own_host = True
        self.viewport_3d.reduce_polys.set(bool(self.settings.get('preview_optimize_vertices', True)))
        self.viewport_3d.reduce_polys.trace_add('write', lambda *_: self._save_settings())
        self.text_host = ttk.Frame(self.detail_pane)
        self.detail_pane.add(self.text_host, weight=1)
        description = ttk.LabelFrame(self.text_host, text=UI_TEXT['s23'], padding=(6, 4))
        description.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.details_text = tk.Text(description, wrap='word', height=6, font=('Consolas', 10), bg='#252526', fg='#d4d4d4', insertbackground='#ffffff', selectbackground='#007acc', selectforeground='#ffffff', relief='flat', bd=0)
        d_vsb = ttk.Scrollbar(description, orient='vertical', command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=d_vsb.set)
        self.details_text.grid(row=0, column=0, sticky='nsew')
        d_vsb.grid(row=0, column=1, sticky='ns')
        description.rowconfigure(0, weight=1)
        description.columnconfigure(0, weight=1)
        self.text_host.rowconfigure(0, weight=1)
        self.text_host.columnconfigure(0, weight=1)
        _set_pane_minsize(self.detail_pane, self.viewport_host, 260)
        _set_pane_minsize(self.detail_pane, self.text_host, 220)
        self.after(50, self._ensure_pane_order)
        status = ttk.Frame(self.viewer_root, padding=(8, 6, 8, 8))
        status.pack(fill='x')
        self.status_label = ttk.Label(status, text=UI_TEXT['m1'])
        self.status_label.pack(side='left')
    def _responsive_cache_toolbar(self, _event=None):
        top = getattr(self, '_cache_top', None)
        if top is None:
            return
        try:
            width = max(1, top.winfo_width())
            mode = 0 if width < 520 else 1 if width < 850 else 2
            if getattr(self, '_cache_toolbar_layout_applied', None) == mode:
                return
            self._cache_toolbar_layout_applied = mode
            toggles = list(getattr(self, '_cache_toolbar_toggles', ()))
            if mode == 0:
                for index, widget in enumerate(toggles):
                    widget.grid_configure(row=index // 2, column=index % 2, sticky='w', padx=(0, 8), pady=(0, 2))
                self.btn_clear.grid_configure(row=2, column=0, sticky='ew', padx=(0, 5), pady=(4, 0))
                self.btn_delete_type.grid_configure(row=2, column=1, sticky='ew', padx=(5, 0), pady=(4, 0))
                self.toggle_btn.grid_configure(row=3, column=0, sticky='ew', padx=(0, 5), pady=(4, 0))
                self.btn_dump.grid_configure(row=3, column=1, sticky='ew', padx=(5, 0), pady=(4, 0))
                self._cache_type_label.grid_configure(row=4, column=0, sticky='w', pady=(6, 0))
                self._cache_type_combo.grid_configure(row=4, column=1, sticky='ew', padx=(6, 0), pady=(6, 0))
                self._cache_filter_label.grid_configure(row=5, column=0, sticky='w', pady=(5, 0))
                self._cache_filter_entry.grid_configure(row=5, column=1, columnspan=3, sticky='ew', padx=(6, 0), pady=(5, 0))
                self._watch_loading_label.grid_configure(row=6, column=0, columnspan=2, sticky='w', pady=(3, 0))
                for col in range(4):
                    top.columnconfigure(col, weight=1 if col in (1, 2, 3) else 0, uniform='cachetoolbar')
            elif mode == 1:
                for index, widget in enumerate(toggles):
                    widget.grid_configure(row=0, column=index, sticky='w', padx=(0 if index == 0 else 8, 0), pady=0)
                self.btn_clear.grid_configure(row=1, column=0, sticky='ew', padx=(0, 5), pady=(5, 0))
                self.btn_delete_type.grid_configure(row=1, column=1, sticky='ew', padx=(5, 0), pady=(5, 0))
                self.toggle_btn.grid_configure(row=1, column=2, sticky='ew', padx=(5, 0), pady=(5, 0))
                self.btn_dump.grid_configure(row=1, column=3, sticky='ew', padx=(5, 0), pady=(5, 0))
                self._cache_type_label.grid_configure(row=2, column=0, sticky='w', pady=(6, 0))
                self._cache_type_combo.grid_configure(row=2, column=1, sticky='ew', padx=(6, 0), pady=(6, 0))
                self._cache_filter_label.grid_configure(row=3, column=0, sticky='w', pady=(5, 0))
                self._cache_filter_entry.grid_configure(row=3, column=1, columnspan=3, sticky='ew', padx=(6, 0), pady=(5, 0))
                self._watch_loading_label.grid_configure(row=2, column=2, columnspan=2, sticky='e', padx=(6, 0), pady=(6, 0))
                for col in range(4):
                    top.columnconfigure(col, weight=1, uniform='cachetoolbar')
            else:
                for index, widget in enumerate(toggles):
                    widget.grid_configure(row=0, column=index, sticky='w', padx=(0 if index == 0 else 8, 0), pady=0)
                self.btn_clear.grid_configure(row=0, column=5, sticky='e', padx=(0, 6), pady=0)
                self.btn_delete_type.grid_configure(row=0, column=6, sticky='e', padx=(0, 6), pady=0)
                self.toggle_btn.grid_configure(row=0, column=7, sticky='e', padx=(0, 6), pady=0)
                self.btn_dump.grid_configure(row=0, column=8, sticky='e', pady=0)
                self._cache_type_label.grid_configure(row=1, column=0, sticky='w', pady=(6, 0))
                self._cache_type_combo.grid_configure(row=1, column=1, sticky='w', padx=(6, 0), pady=(6, 0))
                self._cache_filter_label.grid_configure(row=2, column=0, sticky='w', pady=(5, 0))
                self._cache_filter_entry.grid_configure(row=2, column=1, columnspan=6, sticky='ew', padx=(6, 0), pady=(5, 0))
                self._watch_loading_label.grid_configure(row=0, column=9, sticky='w', padx=(4, 0), pady=0)
                for col in range(4):
                    top.columnconfigure(col, weight=0, uniform='')
                top.columnconfigure(3, weight=1)
                for col in (5, 6, 7, 8):
                    top.columnconfigure(col, weight=0, uniform='')
        except Exception:
            pass
    def _ensure_pane_order(self):
        try:
            panes = self.vpaned.panes()
            tf = str(self.table_frame)

            if not panes or panes[0] != tf:
                self.vpaned.forget(self.table_frame)
                self.vpaned.forget(self.details)
                self.vpaned.add(self.table_frame, weight=3)
                _set_pane_minsize(self.vpaned, self.table_frame, 200)
                self.vpaned.add(self.details, weight=2)
                _set_pane_minsize(self.vpaned, self.details, 100)
        except Exception:
            pass
    def _on_hsash_release(self, _event=None):
        self._clamp_hsash()
        self._save_settings()
    def _clamp_hsash(self):
        try:
            panes = self.hpaned.panes()
            if len(panes) < 2:
                return
            total = self.hpaned.winfo_width()
            pos = self.hpaned.sashpos(0)
            scale = max(0.62, min(1.0, float(getattr(self, '_responsive_last_scale', 1.0) or 1.0)))
            min_left = max(260, int(VIEWER_MIN_WIDTH * scale))
            min_right = max(190, int(REPLACER_MIN_WIDTH * scale))
            if total > min_left + min_right:
                clamped = max(min_left, min(pos, total - min_right))
                if clamped != pos:
                    self.hpaned.sashpos(0, clamped)
        except Exception:
            pass
    def _toggle_viewer_pane(self):
        if self.viewer_collapsed:
            try:
                if self._restore_geom:
                    w, h, _, _ = self._restore_geom
                    cur_w = self.winfo_width()
                    cur_x = self.winfo_x()
                    cur_y = self.winfo_y()
                    right = cur_x + cur_w
                    new_x = right - w
                    self.geometry(f'{w}x{h}+{new_x}+{cur_y}')
                self.hpaned.insert(0, self.viewer_root, weight=3)
                _set_pane_minsize(self.hpaned, self.viewer_root, max(260, int(VIEWER_MIN_WIDTH * max(0.62, getattr(self, '_responsive_last_scale', 1.0) or 1.0))))
                self.hpaned.paneconfigure(self.replacer, weight=2)
                _set_pane_minsize(self.hpaned, self.replacer, max(190, int(REPLACER_MIN_WIDTH * max(0.62, getattr(self, '_responsive_last_scale', 1.0) or 1.0))))
                self.update_idletasks()
                total = self.hpaned.winfo_width()
                if total > 0:
                    pos = self._saved_sash if self._saved_sash is not None else int(total * HPANED_LEFT_FRACTION)
                    self.hpaned.sashpos(0, pos)
                    self._clamp_hsash()
            except Exception:
                pass
            self.viewer_collapsed = False
            self.collapse_btn.config(text=UI_TEXT['g5'])
            self._save_settings()
        else:
            try:
                self.update_idletasks()
                self._restore_geom = (self.winfo_width(), self.winfo_height(), self.winfo_x(), self.winfo_y())
                self._saved_sash = None
                try:
                    self._saved_sash = self.hpaned.sashpos(0)
                except Exception:
                    pass
                viewer_w = self.viewer_root.winfo_width()
                self.hpaned.forget(self.viewer_root)
                min_w, _ = self.wm_minsize()
                orig_w, h, x, y = self._restore_geom
                new_w = max(orig_w - viewer_w, min_w)
                orig_right = x + orig_w
                new_x = orig_right - new_w
                self.geometry(f'{new_w}x{h}+{new_x}+{y}')
            except Exception:
                pass
            self.viewer_collapsed = True
            self.collapse_btn.config(text=UI_TEXT['t23'])
            self._save_settings()
    def _app_focus_changed(self, _event=None):
        try:
            focused = _routils_process_has_focus(self)
            self.wm_attributes('-topmost', bool(self.stay_on_top.get() and focused))
            _routils_sync_popup_topmost(self)
            for win, _height in list(getattr(_MacNotification, '_active', [])):
                try:
                    win.attributes('-topmost', focused)
                    if focused:
                        win.lift()
                except Exception:
                    pass
            try:
                self.after(50, lambda r=self: _routils_sync_popup_topmost(r))
                self.after(250, lambda r=self: _routils_sync_popup_topmost(r))
            except Exception:
                pass
        except Exception:
            pass
    def _finish_resize_activity(self):
        self._resize_idle_job = None
        self._resize_active = False
        if self._deferred_canvas_widths and self._resize_canvas_flush_job is None:
            self._resize_canvas_flush_job = self.after(15, self._flush_deferred_canvas_widths)
        deferred_jobs = list(getattr(self, '_resize_deferred_jobs', {}).items())
        self._resize_deferred_jobs.clear()
        if deferred_jobs:
            existing = {item[0] for item in self._resize_release_jobs}
            for item in deferred_jobs:
                if item[0] not in existing:
                    self._resize_release_jobs.append(item)
                    existing.add(item[0])
                else:
                    for index, old_item in enumerate(self._resize_release_jobs):
                        if old_item[0] == item[0]:
                            self._resize_release_jobs[index] = item
                            break
        if self._resize_release_jobs and self._resize_release_job is None:
            self._resize_release_job = self.after(20, self._run_resize_release_jobs)
        if getattr(self, '_settings_save_deferred', False):
            self._settings_save_deferred = False
            try:
                self.after(450, self._save_settings)
            except Exception:
                pass
        try:
            viewport = getattr(self, 'viewport_3d', None)
            if viewport is not None and getattr(viewport, '_controls_layout_pending', False):
                viewport._controls_layout_pending = False
                if viewport.winfo_exists():
                    viewport.after(60, viewport._layout_controls)
            if viewport is not None and getattr(viewport, '_resize_draw_pending', False):
                viewport._resize_draw_pending = False
                if viewport.winfo_exists() and viewport.winfo_ismapped():
                    viewport.after(500, viewport._redraw_after_resize)
        except Exception:
            pass
    def _run_resize_release_jobs(self):
        self._resize_release_job = None
        if getattr(self, '_resize_active', False):
            return
        if not self._resize_release_jobs:
            return
        key, job = self._resize_release_jobs.pop(0)
        delay_ms, callback = job
        def run_one():
            if getattr(self, '_resize_active', False):
                self._resize_release_jobs.insert(0, (key, job))
                return
            try:
                if not getattr(self, '_ui_dispatch_closed', False):
                    callback()
            except Exception as exc:
                try:
                    self.report_callback_exception(type(exc), exc, exc.__traceback__)
                except Exception:
                    pass
            if self._resize_release_jobs and (not getattr(self, '_ui_dispatch_closed', False)):
                try:
                    self._resize_release_job = self.after(35, self._run_resize_release_jobs)
                except Exception:
                    self._resize_release_job = None
        try:
            if delay_ms > 0:
                self.after(min(int(delay_ms), 250), run_one)
            else:
                self.after_idle(run_one)
        except Exception:
            self._resize_release_job = None
    def _schedule_resize_canvas_flush(self, delay_ms=None):
        if self._resize_canvas_flush_job is not None or not self._deferred_canvas_widths:
            return
        if delay_ms is None:
            delay_ms = 65 if getattr(self, '_resize_active', False) else 20
        try:
            self._resize_canvas_flush_job = self.after(max(0, int(delay_ms)), self._flush_deferred_canvas_widths)
        except Exception:
            self._resize_canvas_flush_job = None
    def _flush_deferred_canvas_widths(self):
        self._resize_canvas_flush_job = None
        if not self._deferred_canvas_widths:
            return
        if getattr(self, '_resize_active', False):
            return
        key = next(iter(self._deferred_canvas_widths))
        canvas, window_id, width, state_key = self._deferred_canvas_widths.pop(key)
        try:
            if canvas.winfo_exists() and width != getattr(self, state_key, -1):
                canvas.itemconfigure(window_id, width=width)
                setattr(self, state_key, width)
        except Exception:
            pass
        if self._deferred_canvas_widths:
            self._schedule_resize_canvas_flush(65 if getattr(self, '_resize_active', False) else 22)
    def _schedule_responsive_ui_scale(self, dimensions=None):
        try:
            if dimensions is None:
                width = int(self.winfo_width())
                height = int(self.winfo_height())
            else:
                width, height = (int(dimensions[0]), int(dimensions[1]))
            reference_width = max(1, int(getattr(self, '_responsive_reference_width', 1400)))
            reference_height = max(1, int(getattr(self, '_responsive_reference_height', 800)))
            ratio = max(0.35, min(1.0, width / reference_width, height / reference_height))
            if abs(ratio - float(getattr(self, '_responsive_applied_ratio', 1.0))) < 0.015:
                return
            job = getattr(self, '_responsive_scale_job', None)
            if job is not None:
                try:
                    self.after_cancel(job)
                except Exception:
                    pass
            self._responsive_scale_job = self.after(190, lambda value=ratio: self._apply_responsive_ui_scale(value))
        except Exception:
            pass
    def _apply_responsive_ui_scale(self, ratio):
        self._responsive_scale_job = None
        if getattr(self, '_resize_active', False):
            try:
                self._responsive_scale_job = self.after(260, lambda value=ratio: self._apply_responsive_ui_scale(value))
            except Exception:
                self._responsive_scale_job = None
            return
        try:
            if not self.winfo_exists():
                return
            ratio = max(0.35, min(1.0, float(ratio)))
            current_width = int(self.winfo_width())
            current_height = int(self.winfo_height())
            reference_width = max(1, int(getattr(self, '_responsive_reference_width', 1400)))
            reference_height = max(1, int(getattr(self, '_responsive_reference_height', 800)))
            ratio = max(0.35, min(1.0, current_width / reference_width, current_height / reference_height))
            if abs(ratio - float(getattr(self, '_responsive_applied_ratio', 1.0))) < 0.015:
                return
            self._responsive_applied_ratio = ratio
            self._responsive_last_scale = ratio
            if not hasattr(self, '_responsive_widget_fonts'):
                self._responsive_widget_fonts = {}
            if not hasattr(self, '_responsive_font_objects'):
                self._responsive_font_objects = {}
            if not hasattr(self, '_responsive_font_base_sizes'):
                self._responsive_font_base_sizes = {}
            def scale_widget(widget):
                try:
                    if not widget.winfo_exists():
                        return
                    try:
                        current_font = widget.cget('font')
                    except Exception:
                        current_font = None
                    if current_font:
                        key = str(widget)
                        saved = self._responsive_widget_fonts.get(key)
                        if saved is None:
                            saved = current_font
                            self._responsive_widget_fonts[key] = saved
                        font_key = (key, str(saved))
                        font_obj = self._responsive_font_objects.get(font_key)
                        if font_obj is None:
                            try:
                                font_obj = tkfont.Font(root=self, font=saved)
                                self._responsive_font_objects[font_key] = font_obj
                                self._responsive_font_base_sizes[font_key] = int(font_obj.cget('size'))
                            except Exception:
                                font_obj = None
                        if font_obj is not None:
                            try:
                                base_size = int(self._responsive_font_base_sizes.get(font_key, font_obj.cget('size')))
                                font_ratio = max(0.82, ratio)
                                if base_size < 0:
                                    scaled_size = -max(8, int(round(abs(base_size) * font_ratio)))
                                else:
                                    scaled_size = max(8, int(round(base_size * font_ratio)))
                                font_obj.configure(size=scaled_size)
                                if str(widget.cget('font')) != str(font_obj):
                                    widget.configure(font=font_obj)
                            except Exception:
                                pass
                    try:
                        children = widget.winfo_children()
                    except Exception:
                        children = ()
                    for child in children:
                        scale_widget(child)
                except Exception:
                    pass
            scale_widget(self)
            try:
                style = ttk.Style(self)
                style_fonts = {'TButton': ('Segoe UI', 9, 'bold'), 'Toolbutton': ('Segoe UI', 9, 'bold'), 'TCheckbutton': ('Segoe UI', 9), 'TRadiobutton': ('Segoe UI', 9), 'TMenubutton': ('Segoe UI', 9), 'TCombobox': ('Segoe UI', 9), 'TEntry': ('Segoe UI', 9), 'TLabel': ('Segoe UI', 10), 'TLabelframe.Label': ('Segoe UI', 9), 'Treeview': ('Consolas', 9), 'Treeview.Heading': ('Segoe UI Semibold', 10), 'RoUtils.Nav.TButton': ('Segoe UI Semibold', 9), 'RoUtils.ActiveNav.TButton': ('Segoe UI Semibold', 9)}
                font_ratio = max(0.82, ratio)
                for style_name, base_font in style_fonts.items():
                    size = max(8, int(round(base_font[1] * font_ratio)))
                    style.configure(style_name, font=(base_font[0], size, *base_font[2:]))
                scaled_padding = max(1, int(round(6 * ratio)))
                scaled_vertical = max(1, int(round(4 * ratio)))
                for style_name in ('TButton', 'Toolbutton', 'TCheckbutton', 'TRadiobutton', 'TMenubutton', 'TCombobox', 'TEntry'):
                    try:
                        style.configure(style_name, padding=(scaled_padding, scaled_vertical))
                    except Exception:
                        pass
                try:
                    style.configure('Treeview', rowheight=max(18, int(round(23 * ratio))))
                except Exception:
                    pass
            except Exception:
                pass
            try:
                self.update_idletasks()
            except Exception:
                pass
        except Exception:
            pass
    def _on_geometry_configure(self, event=None):
        if event is not None and event.widget is not self:
            return
        try:
            if event is not None:
                dimensions = (int(event.width), int(event.height))
            else:
                dimensions = (int(self.winfo_width()), int(self.winfo_height()))
            self._schedule_responsive_ui_scale(dimensions)
            previous = getattr(self, '_last_geometry_dimensions', None)
            self._last_geometry_dimensions = dimensions
            position = (int(getattr(event, 'x', 0) or 0), int(getattr(event, 'y', 0) or 0)) if event is not None else (int(self.winfo_x()), int(self.winfo_y()))
            geometry_key = (dimensions, position)
            if previous is not None and dimensions != previous:
                self._resize_active = True
                if self._resize_idle_job is not None:
                    try:
                        self.after_cancel(self._resize_idle_job)
                    except Exception:
                        pass
                self._resize_idle_job = self.after(420, self._finish_resize_activity)
            if geometry_key == getattr(self, '_last_geometry_seen', None):
                return
            self._last_geometry_seen = geometry_key
            self._geometry_pending_key = geometry_key
            if getattr(self, '_geometry_configure_idle_job', None) is None:
                self._geometry_configure_idle_job = self.after_idle(self._commit_geometry_configure)
        except Exception:
            return
    def _commit_geometry_configure(self):
        self._geometry_configure_idle_job = None
        if getattr(self, '_resize_active', False):
            self._settings_save_deferred = True
            return
        job = getattr(self, '_geometry_save_job', None)
        if job is not None:
            try:
                self.after_cancel(job)
            except Exception:
                pass
        try:
            self._geometry_save_job = self.after(1100, self._save_settings)
        except Exception:
            self._geometry_save_job = None
    def _apply_mesh_preview_vertices_setting(self):
        value = bool(self.mesh_preview_vertices.get())
        self.settings['preview_optimize_vertices'] = value
        try:
            if hasattr(self, 'viewport_3d'):
                self.viewport_3d.reduce_polys.set(value)
        except Exception:
            pass
        self._save_settings()
    def _autosize_columns_once(self, padding=24):
        cols = self.tree['columns']
        for c in cols:
            try:
                w = tkfont.Font().measure(self.tree.heading(c)['text'])
            except Exception:
                w = 80
            for i, iid in enumerate(self.tree.get_children('')):
                if i > 500:
                    break
                text = str(self.tree.set(iid, c))
                w = max(w, tkfont.Font().measure(text))
            measured = min(max(w + padding, 80), 520)
            current = int(self.tree.column(c, 'width'))
            self.tree.column(c, width=max(current, measured))
