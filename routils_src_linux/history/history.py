import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class HistoryMixin:
    def _history_load(self):
        try:
            if not os.path.exists(HISTORY_PATH):
                return []
            with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []
    def _history_save(self, data):
        try:
            tmp = HISTORY_PATH + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, HISTORY_PATH)
        except Exception:
            pass
    def _history_add(self, place_id, job_id):
        place_id = str(place_id or '').strip()
        job_id = str(job_id or '').strip()
        if not place_id or not job_id:
            return
        key = (place_id, job_id.lower())
        if self._history_last_game == key:
            return
        self._history_last_game = key
        def worker():
            name = self._resolve_history_game_name(place_id) or place_id
            now = datetime.now()
            entry = {'game_name': name, 'place_id': place_id, 'job_id': job_id, 'deeplink': f'roblox://experiences/start?placeId={place_id}&gameInstanceId={job_id}', 'date': now.strftime('%d.%m.%Y'), 'time': now.strftime('%H:%M:%S'), 'timestamp': now.isoformat(timespec='seconds')}
            history = self._history_load()
            history = [x for x in history if not (str(x.get('place_id')) == place_id and str(x.get('job_id', '')).lower() == job_id.lower())]
            history.insert(0, entry)
            history = history[:20]
            self._history_save(history)
            try:
                self.after(0, self._history_refresh)
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()
    def _detect_current_game(self, silent=True):
        logs_dir = sober_logs_dir() if os.name != 'nt' else os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox', 'logs')
        uuid_re = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        join_re = re.compile(f"""!\\s*Joining\\s+game\\s+[\\"']?({uuid_re})[\\"']?\\s+place\\s+(\\d+)""", re.IGNORECASE)
        try:
            log_files = sorted([os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.lower().endswith('.log')], key=lambda x: os.path.getmtime(x), reverse=True)[:30]
        except Exception:
            return (None, None)
        for log_path in log_files:
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except Exception:
                continue
            matches = list(join_re.finditer(text))
            if matches:
                m = matches[-1]
                return (m.group(2), m.group(1))
        place_id = job_id = None
        for log_path in log_files:
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except Exception:
                continue
            if not place_id:
                m = re.findall('\\bplaceid\\s*[:=]\\s*(\\d+)', text, re.IGNORECASE)
                if m:
                    place_id = m[-1]
            if not job_id:
                m = re.findall(f"""\\bjobId\\s*[:=]\\s*[\\"']?({uuid_re})""", text, re.IGNORECASE)
                if m:
                    job_id = m[-1]
            if place_id and job_id:
                return (place_id, job_id)
        return (None, None)
    def _start_history_watcher(self):
        def worker():
            while True:
                try:
                    place_id, job_id = self._detect_current_game()
                    if place_id and job_id:
                        self.after(0, lambda p=place_id, j=job_id: self._history_add(p, j))
                except Exception:
                    pass
                time.sleep(2.5)
        threading.Thread(target=worker, daemon=True).start()
    def _build_history_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text=UI_TEXT['o5'])
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text=UI_TEXT['b12'], font=('Segoe UI Semibold', 15)).pack(side='left')
        ttk.Button(head, text=UI_TEXT['c12'], command=self._history_refresh).pack(side='right', padx=(6, 0))
        ttk.Button(head, text=UI_TEXT['d12'], command=self._history_clear).pack(side='right')
        ttk.Label(tab, text=UI_TEXT['e12'], foreground='#9aa0a6').grid(row=1, column=0, sticky='w', pady=(0, 8))
        outer = ttk.Frame(tab)
        outer.grid(row=2, column=0, sticky='nsew')
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        self.history_canvas = tk.Canvas(outer, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, borderwidth=0)
        scroll = ttk.Scrollbar(outer, orient='vertical', command=self.history_canvas.yview)
        self.history_canvas.configure(yscrollcommand=scroll.set)
        self.history_canvas.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')
        self.history_inner = ttk.Frame(self.history_canvas)
        self.history_window = self.history_canvas.create_window((0, 0), window=self.history_inner, anchor='nw')
        self.history_inner.bind('<Configure>', lambda _e: self._schedule_ui('history_region', 30, lambda: self.history_canvas.configure(scrollregion=self.history_canvas.bbox('all'))))
        self.history_canvas.bind('<Configure>', lambda e: self._history_resize_canvas(e))
        self._history_refresh()
    def _history_resize_canvas(self, event):
        width = int(getattr(event, 'width', 0) or 0)
        self._apply_or_defer_canvas_window_width(self.history_canvas, self.history_window, width, '_history_canvas_width')
    def _history_refresh(self):
        if not hasattr(self, 'history_inner'):
            return
        history = self._history_load()
        signature = tuple(((str(x.get('timestamp', '')), str(x.get('place_id', '')), str(x.get('job_id', '')), str(x.get('game_name', '')), str(x.get('deeplink', ''))) for x in history)) if history else ()
        if signature == getattr(self, '_history_render_signature', None):
            return
        self._history_render_signature = signature
        for child in self.history_inner.winfo_children():
            child.destroy()
        if not history:
            ttk.Label(self.history_inner, text=UI_TEXT['f12'], foreground='#9aa0a6').pack(anchor='w', padx=12, pady=18)
            return
        header = ttk.Frame(self.history_inner)
        header.pack(fill='x', padx=6, pady=(0, 4))
        for col, weight in enumerate((3, 2, 3, 2, 0, 0)):
            header.columnconfigure(col, weight=weight)
        for col, label in enumerate((UI_TEXT['w20'], 'ID', UI_TEXT['j31'], UI_TEXT['k31'], '', '')):
            ttk.Label(header, text=label, foreground='#9aa0a6').grid(row=0, column=col, sticky='w', padx=6)
        for entry in history:
            row = ttk.Frame(self.history_inner)
            row.pack(fill='x', padx=6, pady=2)
            for col, weight in enumerate((3, 2, 3, 2, 0, 0)):
                row.columnconfigure(col, weight=weight)
            game = str(entry.get('game_name') or entry.get('place_id') or 'Unknown Game')
            pid = str(entry.get('place_id') or '')
            jid = str(entry.get('job_id') or '')
            dt = f"{entry.get('date', '')} {entry.get('time', '')}".strip()
            link = str(entry.get('deeplink') or f'roblox://experiences/start?placeId={pid}&gameInstanceId={jid}')
            ttk.Label(row, text=game, font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=6, pady=5)
            ttk.Label(row, text=pid).grid(row=0, column=1, sticky='w', padx=6)
            ttk.Label(row, text=jid).grid(row=0, column=2, sticky='w', padx=6)
            ttk.Label(row, text=dt).grid(row=0, column=3, sticky='w', padx=6)
            ttk.Button(row, text=UI_TEXT['g12'], command=lambda l=link: self._history_copy(l)).grid(row=0, column=4, padx=4)
            ttk.Button(row, text=UI_TEXT['h12'], command=lambda l=link: self._history_join(l)).grid(row=0, column=5, padx=(2, 6))
    def _history_copy(self, link):
        try:
            self.clipboard_clear()
            self.clipboard_append(link)
        except Exception as e:
            messagebox.showerror(UI_TEXT['o5'], UI_TEXT['i12'].format(p0=e), parent=self)
    def _history_join(self, link):
        try:
            os.startfile(link)
            self._console_log(UI_TEXT['j12'].format(p0=link))
        except Exception as e:
            messagebox.showerror(UI_TEXT['o5'], UI_TEXT['k12'].format(p0=e), parent=self)
    def _history_clear(self):
        if not messagebox.askyesno(UI_TEXT['o5'], UI_TEXT['l12'], parent=self):
            return
        self._history_save([])
        self._history_last_game = None
        self._history_refresh()
