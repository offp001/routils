import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class SubplaceMixin:
    def _build_subplace_joiner_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text=UI_TEXT['m5'])
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        ttk.Label(tab, text=UI_TEXT['m5'], font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w')
        row = ttk.Frame(tab)
        row.grid(row=1, column=0, sticky='ew', pady=8)
        row.columnconfigure(0, weight=1)
        self.subplace_id = tk.StringVar()
        ttk.Entry(row, textvariable=self.subplace_id).grid(row=0, column=0, sticky='ew')
        ttk.Button(row, text=UI_TEXT['w12'], command=self._subplace_search).grid(row=0, column=1, padx=6)
        self.subplace_tree = ttk.Treeview(tab, columns=('id', 'name'), show='headings')
        self.subplace_tree.heading('id', text=UI_TEXT['x12'])
        self.subplace_tree.heading('name', text=UI_TEXT['y12'])
        self.subplace_tree.column('id', width=160)
        self.subplace_tree.column('name', width=400)
        self.subplace_tree.grid(row=2, column=0, sticky='nsew')
        buttons = ttk.Frame(tab)
        buttons.grid(row=3, column=0, sticky='e', pady=8)
        ttk.Button(buttons, text=UI_TEXT['z12'], command=self._subplace_join).pack(side='left', padx=(0, 6))
        ttk.Button(buttons, text=UI_TEXT['g12'], command=self._subplace_copy_deeplink).pack(side='left')
    def _subplace_search(self):
        pid = self.subplace_id.get().strip()
        if not pid.isdigit():
            return
        try:
            with _routils_request(f'https://apis.roblox.com/universes/v1/places/{pid}/universe', timeout=10) as r:
                universe_id = json.load(r).get('universeId')
            if not universe_id:
                raise ValueError('Universe not found for this Place ID.')
            with _routils_request(f'https://develop.roblox.com/v1/universes/{universe_id}/places?limit=100&sortOrder=Asc', timeout=10) as r:
                data = json.load(r)
            self.subplace_tree.delete(*self.subplace_tree.get_children())
            for x in data.get('data', []):
                self.subplace_tree.insert('', 'end', values=(x.get('id', ''), x.get('name', x.get('id', ''))))
        except Exception as e:
            messagebox.showerror(UI_TEXT['m5'], UI_TEXT['a13'].format(p0=e), parent=self)
    def _subplace_copy_deeplink(self):
        place_id = None
        game_instance_id = None
        logs_dir = sober_logs_dir() if os.name != 'nt' else os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox', 'logs')
        uuid_re = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        try:
            log_files = sorted([os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.lower().endswith('.log')], key=lambda x: os.path.getmtime(x), reverse=True)[:30]
            join_re = re.compile(f"""!\\s*Joining\\s+game\\s+[\\"']?({uuid_re})[\\"']?\\s+place\\s+(\\d+)""", re.IGNORECASE)
            for log_path in log_files:
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                except Exception:
                    continue
                matches = list(join_re.finditer(text))
                if matches:
                    m = matches[-1]
                    game_instance_id, place_id = (m.group(1), m.group(2))
                    break
            if not place_id or not game_instance_id:
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
                    if not game_instance_id:
                        m = re.findall(f"""\\bjobId\\s*[:=]\\s*[\\"']?({uuid_re})""", text, re.IGNORECASE)
                        if m:
                            game_instance_id = m[-1]
                    if place_id and game_instance_id:
                        break
        except Exception as e:
            messagebox.showerror(UI_TEXT['m5'], UI_TEXT['b13'].format(p0=e), parent=self)
            return
        if not place_id or not game_instance_id:
            messagebox.showwarning(UI_TEXT['m5'], UI_TEXT['c13'], parent=self)
            return
        link = f'roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}'
        self._history_add(place_id, game_instance_id)
        try:
            self.clipboard_clear()
            self.clipboard_append(link)
            self.update_idletasks()
            messagebox.showinfo(UI_TEXT['m5'], UI_TEXT['d13'], parent=self)
        except Exception as e:
            messagebox.showerror(UI_TEXT['m5'], UI_TEXT['e13'].format(p0=e), parent=self)
    def _subplace_join(self):
        sel = self.subplace_tree.selection()
        if not sel:
            return
        pid = self.subplace_tree.item(sel[0], 'values')[0]
        try:
            os.startfile(f'roblox://placeId={pid}')
            self._console_log(UI_TEXT['f13'].format(p0=pid))
        except Exception as e:
            messagebox.showerror(UI_TEXT['m5'], UI_TEXT['g13'].format(p0=e), parent=self)
