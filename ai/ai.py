import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class AIMixin:
    def _save_gemini_api_key(self):
        key = self.gemini_api_key.get().strip()
        if not key:
            messagebox.showwarning(UI_TEXT['i18'], UI_TEXT['x21'], parent=self)
            return
        self.settings['gemini_api_key'] = key
        self._save_settings()
        messagebox.showinfo(UI_TEXT['i18'], UI_TEXT['y21'], parent=self)
    def _ai_canvas_resize(self, canvas, window_id, event):
        width = int(getattr(event, 'width', 0) or 0)
        key = f'_ai_canvas_width_{id(canvas)}'
        self._apply_or_defer_canvas_window_width(canvas, window_id, width, key)
    def _build_ai_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text=UI_TEXT['j5'])
        self.ai_tab = tab
        self._construct_ai_chat(tab)
    def _open_ai_chat(self, prompt=None):
        ai_id = next((tid for tid in self.nb.tabs() if self.nb.tab(tid, 'text') == UI_TEXT['j5']), None)
        if ai_id is not None:
            self.nb.select(ai_id)
            self._lazy_tab_changed()
        if prompt and str(prompt).strip():
            def submit_when_ready(attempt=0):
                callback = getattr(self, '_ai_send_callback', None)
                input_box = getattr(self, '_ai_input_box', None)
                if callback is not None and input_box is not None and input_box.winfo_exists():
                    input_box.delete('1.0', 'end')
                    input_box.insert('1.0', str(prompt).strip())
                    callback()
                elif attempt < 20:
                    self.after(100, lambda: submit_when_ready(attempt + 1))
            self.after(150, submit_when_ready)
        self._console_log(UI_TEXT['z21'])
    def _construct_ai_chat(self, win):
        palette = _CURRENT_PALETTE
        win.columnconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)
        header = tk.Frame(win, bg=palette.get('bg_medium', '#252526'), padx=16, pady=12)
        header.grid(row=0, column=0, sticky='ew')
        header.columnconfigure(1, weight=1)
        tk.Label(header, text=UI_TEXT['a22'], bg=palette.get('bg_medium', '#252526'), fg=palette.get('fg', '#e6e6e6'), font=('Segoe UI Semibold', 16)).grid(row=0, column=0, sticky='w')
        tk.Label(header, text=UI_TEXT['b22'], bg=palette.get('bg_medium', '#252526'), fg='#a6abb4', font=('Segoe UI', 9)).grid(row=1, column=0, sticky='w', pady=(3, 0))
        model_names = {UI_TEXT['g30']: 'gemini-3.8-flash', UI_TEXT['h30']: 'gemini-3.7-flash', UI_TEXT['i30']: 'gemini-3.6-flash', UI_TEXT['j30']: 'gemini-3.5-flash', UI_TEXT['k30']: 'gemini-3.5-flash-lite', UI_TEXT['l30']: 'gemini-3.1-flash-lite', UI_TEXT['m30']: 'gemini-3.1-pro-preview', UI_TEXT['n30']: 'gemini-3-flash-preview', UI_TEXT['o30']: 'gemini-2.5-flash', UI_TEXT['p30']: 'gemini-2.5-pro', UI_TEXT['q30']: 'gemini-2.5-flash-lite'}
        saved_model = self.settings.get('ai_model', UI_TEXT['g30'])
        if saved_model not in model_names:
            saved_model = UI_TEXT['g30']
        model_var = tk.StringVar(value=saved_model)
        model_box = ttk.Combobox(header, textvariable=model_var, values=list(model_names.keys()), state='readonly', width=24)
        model_box.grid(row=0, column=2, sticky='e')
        model_box.bind('<<ComboboxSelected>>', lambda _e: (self.settings.__setitem__('ai_model', model_var.get()), self._save_settings()))
        tk.Label(header, text=UI_TEXT['c22'], bg=palette.get('bg_medium', '#252526'), fg='#a6abb4', font=('Segoe UI Semibold', 8)).grid(row=1, column=2, sticky='e', pady=(3, 0))
        body = tk.Frame(win, bg=palette.get('bg_dark', '#1b1b1c'), padx=10, pady=10)
        body.grid(row=1, column=0, sticky='nsew')
        body.rowconfigure(0, weight=1)
        body.columnconfigure(0, weight=1)
        canvas = tk.Canvas(body, bg=palette.get('bg_dark', '#1b1b1c'), highlightthickness=0, bd=0)
        scroll = ttk.Scrollbar(body, orient='vertical', command=canvas.yview)
        messages = tk.Frame(canvas, bg=palette.get('bg_dark', '#1b1b1c'))
        canvas.configure(yscrollcommand=scroll.set)
        canvas.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')
        window_id = canvas.create_window((0, 0), window=messages, anchor='nw')
        messages.bind('<Configure>', lambda _e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(window_id, width=max(1, e.width)))
        history = []
        busy = {'value': False}
        attachment = {'path': None}
        thinking = {'row': None, 'bubble': None, 'started': 0.0}
        bubble_bg = '#ded8cd'
        bubble_fg = '#242424'
        def scroll_bottom():
            try:
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'))
                canvas.yview_moveto(1.0)
            except Exception:
                pass
        def copy_code(code):
            try:
                win.clipboard_clear()
                win.clipboard_append(code)
            except Exception:
                pass
        def save_generated_file(content, language=''):
            extensions = {'python': '.py', 'py': '.py', 'json': '.json', 'javascript': '.js', 'js': '.js', 'html': '.html', 'css': '.css', 'xml': '.xml', 'yaml': '.yaml', 'yml': '.yml', 'csv': '.csv', 'markdown': '.md', 'md': '.md', 'text': '.txt', 'txt': '.txt', 'powershell': '.ps1', 'ps1': '.ps1', 'lua': '.lua', 'sql': '.sql', 'bat': '.bat', 'bash': '.sh', 'sh': '.sh'}
            ext = extensions.get((language or '').strip().lower(), '.txt')
            path = filedialog.asksaveasfilename(parent=self, title=UI_TEXT['d22'], defaultextension=ext, initialfile='routils_ai_output' + ext, filetypes=[(UI_TEXT['e22'], '*' + ext), (UI_TEXT['z7'], '*.*')])
            if not path:
                return
            try:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                messagebox.showinfo(UI_TEXT['f22'], UI_TEXT['g22'], parent=self)
            except Exception as exc:
                messagebox.showerror(UI_TEXT['f22'], UI_TEXT['h22'].format(p0=exc), parent=self)
        def add_code_block(parent, code, language=''):
            box = tk.Frame(parent, bg='#cfc8bc', highlightthickness=1, highlightbackground='#b6ad9f')
            box.pack(fill='x', pady=(6, 5))
            top = tk.Frame(box, bg='#c4bcae', height=29)
            top.pack(fill='x')
            top.pack_propagate(False)
            tk.Label(top, text=language or 'code', bg='#c4bcae', fg='#38342f', font=('Segoe UI', 8)).pack(side='left', padx=8)
            tk.Button(top, text=UI_TEXT['i22'], command=lambda c=code, lang=language: save_generated_file(c, lang), bg='#b7ad9d', fg='#292622', activebackground='#a79c8b', relief='flat', bd=0, padx=8, font=('Segoe UI Semibold', 8), cursor='hand2').pack(side='right', padx=5, pady=3)
            tk.Button(top, text=UI_TEXT['j22'], command=lambda c=code: copy_code(c), bg='#b7ad9d', fg='#292622', activebackground='#a79c8b', relief='flat', bd=0, padx=8, font=('Segoe UI Semibold', 8), cursor='hand2').pack(side='right', padx=2, pady=3)
            txt = tk.Text(box, width=1, height=max(2, min(14, code.count('\n') + 2)), wrap='word', bg='#d9d2c6', fg='#242424', insertbackground='#242424', relief='flat', bd=0, padx=9, pady=7, font=('Consolas', 9))
            txt.insert('1.0', code)
            txt.configure(state='disabled')
            txt.pack(fill='x')
        def add_rich_line(parent, text, pady=2):
            visible_text = re.sub('\\*\\*|__|`', '', str(text))
            line_font = tkfont.Font(family='Segoe UI', size=10)
            max_content_width = max(90, bubble_max_width() - 42)
            char_unit = max(1, line_font.measure('0'))
            natural_width = line_font.measure(visible_text)
            text_units = max(1, min(len(visible_text) or 1, int((max_content_width + char_unit - 1) / char_unit), int((natural_width + char_unit - 1) / char_unit) + 1))
            line = tk.Text(parent, width=text_units, height=1, wrap='word', bg=bubble_bg, fg=bubble_fg, relief='flat', bd=0, highlightthickness=0, padx=0, pady=0, font=('Segoe UI', 10), cursor='arrow')
            line.pack(fill='x', pady=pady)
            line.tag_configure('bold', font=('Segoe UI Semibold', 10), foreground='#171717')
            line.tag_configure('inline', font=('Consolas', 9), foreground='#303030', background='#d0c8bb')
            tokens = re.split('(\\*\\*.*?\\*\\*|__.*?__|`[^`]+`)', str(text))
            for token in tokens:
                if not token:
                    continue
                bold = token.startswith('**') and token.endswith('**') or (token.startswith('__') and token.endswith('__'))
                inline = token.startswith('`') and token.endswith('`') and (len(token) >= 2)
                value = token[2:-2] if bold else token[1:-1] if inline else token
                line.insert('end', value, 'bold' if bold else 'inline' if inline else '')
            line.configure(state='disabled')
            def sync_display_height(widget=line):
                try:
                    if not widget.winfo_exists() or widget.winfo_width() < 8:
                        return
                    count = widget.count('1.0', 'end', 'displaylines')
                    desired = max(1, int(count[0]) if count else 1)
                    if int(widget.cget('height')) != desired:
                        widget.configure(height=desired)
                except Exception:
                    pass
            line.bind('<Configure>', lambda _e, w=line: w.after_idle(lambda: sync_display_height(w)), add='+')
            line.after_idle(lambda w=line: sync_display_height(w))
            line.bind('<Button-1>', lambda _e, w=line: (w.configure(state='normal'), w.focus_set()), add='+')
            return line
        def add_markdown_message(parent, text):
            lines = str(text).replace('\r\n', '\n').replace('\r', '\n').split('\n')
            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if stripped.startswith('```'):
                    language = stripped[3:].strip()
                    i += 1
                    code = []
                    while i < len(lines) and (not lines[i].strip().startswith('```')):
                        code.append(lines[i])
                        i += 1
                    if i < len(lines):
                        i += 1
                    add_code_block(parent, '\n'.join(code), language)
                    continue
                heading = re.match('^#{1,6}\\s+(.+)$', stripped)
                if heading:
                    w = add_rich_line(parent, heading.group(1), pady=(5, 4))
                    w.configure(state='normal')
                    w.tag_configure('heading', font=('Segoe UI Semibold', 12 if stripped.startswith('# ') else 11), foreground='#171717')
                    w.tag_add('heading', '1.0', 'end')
                    w.configure(state='disabled')
                    i += 1
                    continue
                if i + 1 < len(lines) and '|' in line and re.match('^\\s*\\|?\\s*:?-+:?\\s*(\\|\\s*:?-+:?\\s*)+\\|?\\s*$', lines[i + 1].strip()):
                    rows = [[x.strip() for x in line.strip().strip('|').split('|')]]
                    i += 2
                    while i < len(lines) and '|' in lines[i] and lines[i].strip():
                        rows.append([x.strip() for x in lines[i].strip().strip('|').split('|')])
                        i += 1
                    table = tk.Frame(parent, bg='#bdb4a6')
                    table.pack(fill='x', pady=6)
                    cols = max((len(r) for r in rows))
                    for r, row_data in enumerate(rows):
                        for c in range(cols):
                            value = row_data[c] if c < len(row_data) else ''
                            tk.Label(table, text=value, bg='#c8c0b3' if r == 0 else bubble_bg, fg=bubble_fg, justify='left', anchor='w', padx=7, pady=5, wraplength=420, font=('Segoe UI Semibold' if r == 0 else 'Segoe UI', 9)).grid(row=r, column=c, sticky='nsew', padx=1, pady=1)
                    for c in range(cols):
                        table.grid_columnconfigure(c, weight=1)
                    continue
                if stripped:
                    bullet = re.match('^[-*]\\s+(.+)$', stripped)
                    if bullet:
                        stripped = '• ' + bullet.group(1)
                    add_rich_line(parent, stripped)
                else:
                    tk.Frame(parent, bg=bubble_bg, height=4).pack(fill='x')
                i += 1
        def bubble_max_width():
            canvas_width = canvas.winfo_width()
            if canvas_width <= 1:
                canvas_width = 760
            return max(180, int((canvas_width - 42) * 0.72))
        def measured_bubble_width(text, font, include_markdown=False):
            available = bubble_max_width()
            lines = str(text).replace('\r\n', '\n').replace('\r', '\n').split('\n')
            widths = []
            for line in lines:
                candidate = line.strip()
                if not candidate or candidate.startswith('```'):
                    continue
                if include_markdown:
                    candidate = re.sub('[`*_#>|]', '', candidate)
                widths.append(font.measure(candidate))
            natural = max(widths, default=font.measure('Thinking...'))
            return max(72, min(available, natural + 34))
        def make_rounded_bubble(parent, color, border, width, side, padx=10, pady=7):
            max_width = bubble_max_width()
            size_state = {'width': max(72, min(max_width, int(width)))}
            outer = tk.Canvas(parent, width=size_state['width'], height=42, bg=palette.get('bg_dark', '#1b1b1c'), highlightthickness=0, bd=0)
            outer.pack(side=side, anchor='e' if side == 'right' else 'w', padx=(35, 0) if side == 'right' else (0, 35))
            inner = tk.Frame(outer, bg=color, bd=0, padx=padx, pady=pady)
            window_id = outer.create_window(7, 7, window=inner, anchor='nw', width=max(58, size_state['width'] - 14))
            def redraw(_event=None):
                try:
                    max_width_now = bubble_max_width()
                    requested = inner.winfo_reqwidth() + 14
                    actual_w = max(72, min(max_width_now, max(size_state['width'], requested)))
                    actual_h = max(34, inner.winfo_reqheight() + 14)
                    current_width = int(float(outer.cget('width')))
                    current_height = int(float(outer.cget('height')))
                    if current_width != actual_w or current_height != actual_h:
                        outer.configure(width=actual_w, height=actual_h)
                    outer.coords(window_id, 7, 7)
                    outer.itemconfigure(window_id, width=max(58, actual_w - 14))
                    outer.delete('bubble-shape')
                    r = min(12, max(7, actual_h // 4))
                    points = [r, 0, actual_w - r, 0, actual_w, r, actual_w, actual_h - r, actual_w - r, actual_h, r, actual_h, 0, actual_h - r, 0, r]
                    outer.create_polygon(points, smooth=True, splinesteps=18, fill=color, outline=border, width=1.5, tags='bubble-shape')
                    outer.tag_lower('bubble-shape', window_id)
                except Exception:
                    pass
            def set_bubble_width(new_width):
                try:
                    size_state['width'] = max(72, min(bubble_max_width(), int(new_width)))
                    outer.after_idle(redraw)
                except Exception:
                    pass
            inner._routils_set_bubble_width = set_bubble_width
            inner._routils_resize_bubble = redraw
            inner.bind('<Configure>', redraw, add='+')
            outer.bind('<Configure>', redraw, add='+')
            outer.after_idle(redraw)
            return (inner, outer)
        def make_row(role, text, meta=''):
            row = tk.Frame(messages, bg=palette.get('bg_dark', '#1b1b1c'))
            row.pack(fill='x', padx=7, pady=6)
            if role == 'user':
                bubble_color = palette.get('accent', '#7f8cff')
                user_font = tkfont.Font(family='Segoe UI', size=10)
                estimated_width = measured_bubble_width(text, user_font)
                bubble, outer = make_rounded_bubble(row, bubble_color, _routils_darken_color(bubble_color, 0.18), estimated_width, 'right', padx=10, pady=7)
                tk.Label(bubble, text=str(text), bg=bubble_color, fg='#ffffff', justify='left', anchor='w', wraplength=max(45, estimated_width - 28), font=('Segoe UI', 10)).pack(anchor='w', fill='x')
                if meta:
                    tk.Label(bubble, text=meta, bg=bubble_color, fg='#f0f0f0', font=('Segoe UI', 8)).pack(anchor='e', pady=(4, 0))
                return (row, bubble)
            header_row = tk.Frame(row, bg=palette.get('bg_dark', '#1b1b1c'))
            header_row.pack(fill='x', padx=(0, 60), pady=(0, 3))
            title_label = tk.Label(header_row, text=UI_TEXT['f22'] + (UI_TEXT['k22'].format(p0=meta) if meta else UI_TEXT['m1']), bg=palette.get('bg_dark', '#1b1b1c'), fg='#aeb4be', font=('Segoe UI Semibold', 8))
            title_label.pack(side='left')
            ai_font = tkfont.Font(family='Segoe UI', size=10)
            estimated_width = measured_bubble_width(text, ai_font, include_markdown=True)
            bubble, outer = make_rounded_bubble(row, bubble_bg, '#c5bdaf', estimated_width, 'left', padx=10, pady=7)
            if text == 'Thinking...':
                tk.Label(bubble, text=UI_TEXT['l22'], bg=bubble_bg, fg='#4a463f', font=('Segoe UI', 10, 'italic')).pack(anchor='w')
            else:
                add_markdown_message(bubble, text)
            return (row, bubble, title_label)
        def update_thinking(elapsed):
            row = thinking.get('row')
            if row is None:
                return
            try:
                if not row.winfo_exists() or not busy['value']:
                    return
                title = thinking.get('title')
                if title is not None and title.winfo_exists():
                    title.configure(text=UI_TEXT['m22'].format(p0=int(elapsed)))
                win.after(1000, lambda: update_thinking(time.monotonic() - thinking['started']))
            except Exception:
                pass
        def choose_file():
            path = filedialog.askopenfilename(parent=self, title=UI_TEXT['n22'], filetypes=[(UI_TEXT['o22'], '*.txt *.md *.py *.json *.csv *.log *.yaml *.yml *.xml *.html *.css *.js *.png *.jpg *.jpeg *.webp *.gif *.bmp *.pdf'), (UI_TEXT['z7'], '*.*')])
            if not path:
                return
            attachment['path'] = path
            filename = os.path.basename(path)
            ext = os.path.splitext(filename)[1] or 'file'
            attach_label.configure(text=UI_TEXT['p22'].format(p0=filename, p1=ext), state='normal')
            for child in attach_preview.winfo_children():
                child.destroy()
            attachment.pop('preview_photo', None)
            if ext.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}:
                try:
                    with Image.open(path) as source_image:
                        preview_image = source_image.copy()
                    preview_image.thumbnail((210, 125), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
                    photo = ImageTk.PhotoImage(preview_image, master=self)
                    attachment['preview_photo'] = photo
                    tk.Label(attach_preview, image=photo, bg=palette.get('bg_medium', '#252526'), bd=0).pack(anchor='w', pady=(4, 2))
                    tk.Label(attach_preview, text=UI_TEXT['q22'].format(p0=preview_image.width, p1=preview_image.height), bg=palette.get('bg_medium', '#252526'), fg=palette.get('fg', '#e6e6e6'), font=('Segoe UI', 8)).pack(anchor='w')
                except Exception as exc:
                    tk.Label(attach_preview, text=UI_TEXT['r22'].format(p0=exc), bg=palette.get('bg_medium', '#252526'), fg=palette.get('fg', '#e6e6e6'), font=('Segoe UI', 8)).pack(anchor='w')
            elif ext.lower() == '.pdf':
                tk.Label(attach_preview, text=UI_TEXT['s22'], bg=palette.get('bg_medium', '#252526'), fg=palette.get('fg', '#e6e6e6'), font=('Segoe UI', 8)).pack(anchor='w', pady=(4, 2))
            attach_row.grid()
            input_box.configure(height=5)
            scroll_bottom()
        def clear_file():
            attachment['path'] = None
            attachment.pop('preview_photo', None)
            for child in attach_preview.winfo_children():
                child.destroy()
            attach_row.grid_remove()
            input_box.configure(height=3)
        def send():
            if busy['value']:
                return
            text = input_box.get('1.0', 'end-1c').strip()
            path = attachment.get('path')
            if not text and (not path):
                return
            normalized_greeting = re.sub('[^\\w]+', ' ', text.casefold(), flags=re.UNICODE).strip()
            simple_greetings = {'hello', 'hi', 'hey', 'hello there', 'hi there', 'hey there', 'merhaba', 'selam', 'selamlar', 'sa', 'günaydın', 'iyi günler', 'good morning', 'good afternoon', 'good evening'}
            if not path and normalized_greeting in simple_greetings:
                input_box.delete('1.0', 'end')
                make_row('user', text)
                history.append({'role': 'user', 'parts': [{'text': text}]})
                greeting_answer = 'Hey! Need a hand with RoUtils?'
                history.append({'role': 'model', 'parts': [{'text': greeting_answer}]})
                make_row('model', greeting_answer)
                scroll_bottom()
                input_box.focus_set()
                return
            settings_queries = {'settings', 'setting', 'settings help', 'help with settings', 'settings tab', 'how to use settings', 'ayarlar', 'ayarlar yardımı', 'ayarlar sekmesi'}
            if not path and normalized_greeting in settings_queries:
                input_box.delete('1.0', 'end')
                make_row('user', text)
                history.append({'role': 'user', 'parts': [{'text': text}]})
                settings_answer = 'You can find app options in Settings. To set up Gemini, open Settings > Gemini AI and add your API key. You can change the app theme in Customize. Tell me the name of a setting and I’ll point you to it.'
                history.append({'role': 'model', 'parts': [{'text': settings_answer}]})
                make_row('model', settings_answer)
                scroll_bottom()
                input_box.focus_set()
                return
            key = self.gemini_api_key.get().strip()
            if not key:
                messagebox.showwarning(UI_TEXT['i18'], UI_TEXT['t22'], parent=self)
                return
            input_box.delete('1.0', 'end')
            filename = os.path.basename(path) if path else ''
            user_display = text if text else UI_TEXT['f28']
            if filename:
                user_display += f'\n\n📎 {filename}'
            make_row('user', user_display)
            user_parts = [{'text': user_display}]
            history.append({'role': 'user', 'parts': user_parts})
            busy['value'] = True
            send_btn.configure(state='disabled')
            input_box.configure(state='disabled')
            attach_btn.configure(state='disabled')
            clear_btn.configure(state='disabled')
            row, bubble, title_label = make_row('model', 'Thinking...')
            thinking.update({'row': row, 'bubble': bubble, 'title': title_label, 'started': time.monotonic()})
            update_thinking(0)
            selected_model = model_names.get(model_var.get(), 'gemini-3.8-flash')
            history_snapshot = [dict(item) for item in history]
            for item in history_snapshot:
                item['parts'] = list(item.get('parts', []))
            def worker():
                try:
                    parts = [{'text': user_display}]
                    if path:
                        size = os.path.getsize(path)
                        if size > 12 * 1024 * 1024:
                            parts.append({'text': 'The selected file is larger than 12 MB; only its filename was attached.'})
                        else:
                            mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
                            ext_lower = os.path.splitext(path)[1].lower()
                            if ext_lower in {'.txt', '.md', '.py', '.json', '.csv', '.log', '.yaml', '.yml', '.xml', '.html', '.css', '.js'}:
                                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                                    content = f.read(1000000)
                                parts.append({'text': f'\n\nAttached file content ({filename}):\n```\n{content}\n```'})
                            elif mime.startswith('image/') or mime == 'application/pdf':
                                with open(path, 'rb') as f:
                                    encoded = base64.b64encode(f.read()).decode('ascii')
                                parts.append({'inline_data': {'mime_type': mime, 'data': encoded}})
                            else:
                                parts.append({'text': f'Attached file: {filename} ({mime}). This file type is not embedded; ask the user to paste relevant content if needed.'})
                    history_snapshot[-1]['parts'] = parts
                    prompt_rules = UI_TEXT['u22']
                    payload = {'systemInstruction': {'parts': [{'text': prompt_rules}]}, 'contents': history_snapshot}
                    with _routils_request('https://generativelanguage.googleapis.com/v1beta/models/' + selected_model + ':generateContent', timeout=45, headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, data=json.dumps(payload).encode('utf-8'), method='POST') as response:
                        result = json.loads(response.read().decode('utf-8'))
                    parts_out = result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                    answer = ''.join((str(part.get('text', '')) for part in parts_out)).strip()
                    if not answer:
                        raise RuntimeError('Gemini returned an empty response.')
                    history.append({'role': 'model', 'parts': [{'text': answer}]})
                    win.after(0, lambda a=answer: finish(a))
                except Exception as exc:
                    error_text = str(exc)
                    try:
                        win.after(0, lambda e=error_text: finish(f'**Request failed**\n\n{e}'))
                    except Exception:
                        pass
            threading.Thread(target=worker, daemon=True, name='RoUtilsGeminiRequest').start()
        def finish(answer):
            try:
                elapsed = max(0, int(time.monotonic() - thinking['started']))
                bubble = thinking.get('bubble')
                title_label = thinking.get('title')
                if bubble is not None and bubble.winfo_exists():
                    for child in bubble.winfo_children():
                        child.destroy()
                    bubble_font = tkfont.Font(family='Segoe UI', size=10)
                    bubble._routils_set_bubble_width(measured_bubble_width(answer, bubble_font, include_markdown=True))
                    add_markdown_message(bubble, answer)
                    bubble.after_idle(bubble._routils_resize_bubble)
                if title_label is not None and title_label.winfo_exists():
                    title_label.configure(text=UI_TEXT['v22'].format(p0=elapsed))
            except Exception:
                row, bubble, title_label = make_row('model', answer, f"{int(time.monotonic() - thinking['started'])}s")
            busy['value'] = False
            thinking.update({'row': None, 'bubble': None, 'title': None})
            send_btn.configure(state='normal')
            input_box.configure(state='normal')
            attach_btn.configure(state='normal')
            clear_btn.configure(state='normal')
            clear_file()
            input_box.focus_set()
            scroll_bottom()
        composer_outer = tk.Frame(win, bg=palette.get('bg_dark', '#1b1b1c'), padx=12, pady=10)
        composer_outer.grid(row=2, column=0, sticky='ew')
        composer_outer.columnconfigure(0, weight=1)
        composer_card = tk.Frame(composer_outer, bg=palette.get('bg_medium', '#252526'), highlightthickness=1, highlightbackground=palette.get('border', '#444446'), padx=8, pady=7)
        composer_card.grid(row=0, column=0, sticky='ew')
        composer_card.columnconfigure(1, weight=1)
        attach_btn = tk.Button(composer_card, text=UI_TEXT['m6'], command=choose_file, bg=palette.get('bg_light', '#3a3a3c'), fg=palette.get('fg', '#e6e6e6'), activebackground=palette.get('accent', '#7f8cff'), relief='flat', bd=0, width=3, font=('Segoe UI Semibold', 15), cursor='hand2')
        attach_btn.grid(row=0, column=0, rowspan=2, sticky='ns', padx=(0, 8))
        input_box = tk.Text(composer_card, height=3, wrap='word', font=('Segoe UI', 10), bg=palette.get('bg_medium', '#252526'), fg=palette.get('fg', '#e6e6e6'), insertbackground=palette.get('fg', '#ffffff'), relief='flat', bd=0, padx=8, pady=7)
        input_box.grid(row=0, column=1, sticky='ew')
        send_btn = tk.Button(composer_card, text=UI_TEXT['w22'], command=send, bg=palette.get('accent', '#7f8cff'), fg='#ffffff', activebackground=_routils_darken_color(palette.get('accent', '#7f8cff'), 0.15), relief='flat', bd=0, padx=14, pady=8, font=('Segoe UI Semibold', 9), cursor='hand2')
        send_btn.grid(row=0, column=2, rowspan=2, sticky='ns', padx=(8, 0))
        attach_row = tk.Frame(composer_card, bg=palette.get('bg_medium', '#252526'))
        attach_row.grid(row=1, column=1, sticky='ew', pady=(5, 0))
        attach_label = tk.Label(attach_row, text=UI_TEXT['m1'], bg=palette.get('bg_medium', '#252526'), fg=palette.get('fg', '#e6e6e6'), font=('Segoe UI', 8), anchor='w')
        attach_label.pack(side='left', fill='x', expand=True)
        clear_btn = tk.Button(attach_row, text=UI_TEXT['e5'], command=clear_file, bg=palette.get('bg_light', '#3a3a3c'), fg=palette.get('fg', '#e6e6e6'), relief='flat', bd=0, padx=8)
        clear_btn.pack(side='right')
        attach_preview = tk.Frame(composer_card, bg=palette.get('bg_medium', '#252526'))
        attach_preview.grid(row=2, column=1, sticky='ew')
        attach_preview.grid_remove()
        original_choose_file = choose_file
        def choose_file_with_preview_layout():
            original_choose_file()
            if attachment.get('path'):
                attach_preview.grid()
        choose_file = choose_file_with_preview_layout
        original_clear_file = clear_file
        def clear_file_with_preview_layout():
            original_clear_file()
            attach_preview.grid_remove()
        clear_file = clear_file_with_preview_layout
        attach_row.grid_remove()
        input_box.bind('<Return>', lambda e: None if e.state & 1 else (send(), 'break')[1])
        input_box.bind('<Shift-Return>', lambda _e: None)
        self._ai_input_box = input_box
        self._ai_send_callback = send
        self._ai_model_var = model_var
        make_row('model', UI_TEXT['e28'])
        input_box.focus_set()
