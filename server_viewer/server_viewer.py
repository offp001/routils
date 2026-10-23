import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class ServerViewerMixin:
    def _build_server_viewer_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text=UI_TEXT['n5'])
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text=UI_TEXT['n5'], font=('Segoe UI Semibold', 15)).pack(side='left')
        self.server_viewer_status = ttk.Label(head, text=UI_TEXT['h13'], foreground='#9aa0a6')
        self.server_viewer_status.pack(side='right')
        row = ttk.Frame(tab)
        row.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        row.columnconfigure(0, weight=1)
        self.server_viewer_link = tk.StringVar()
        ttk.Entry(row, textvariable=self.server_viewer_link).grid(row=0, column=0, sticky='ew')
        ttk.Button(row, text=UI_TEXT['i13'], command=self._server_viewer_load).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(row, text=UI_TEXT['j6'], command=self._server_viewer_clear).grid(row=0, column=2, padx=(6, 0))
        body = ttk.PanedWindow(tab, orient='horizontal')
        body.grid(row=2, column=0, sticky='nsew')
        left = ttk.Frame(body)
        right = ttk.Frame(body)
        body.add(left, weight=1)
        body.add(right, weight=1)
        self.server_viewer_body = body
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        info = ttk.LabelFrame(left, text=UI_TEXT['j13'])
        info.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        for i in range(2):
            info.columnconfigure(i, weight=1)
        self.server_viewer_vars = {}
        fields = [(UI_TEXT['o28'], 'place_id'), (UI_TEXT['p28'], 'job_id'), (UI_TEXT['d31'], 'players'), (UI_TEXT['a30'], 'max_players'), (UI_TEXT['e31'], 'ping'), (UI_TEXT['b30'], 'fps'), ('Location', 'location')]
        for i, (label, key) in enumerate(fields):
            r, c = divmod(i, 2)
            ttk.Label(info, text=label, foreground='#9aa0a6').grid(row=r * 2, column=c, sticky='w', padx=8, pady=(6, 0))
            var = tk.StringVar(value='—')
            self.server_viewer_vars[key] = var
            ttk.Label(info, textvariable=var).grid(row=r * 2 + 1, column=c, sticky='w', padx=8, pady=(0, 6))
        note = ttk.Label(left, text=UI_TEXT['k13'], foreground='#9aa0a6', justify='left')
        note.grid(row=1, column=0, sticky='nw', pady=(4, 0))
        ttk.Label(right, text=UI_TEXT['m1'], font=('Segoe UI Semibold', 10)).grid(row=0, column=0, sticky='w', pady=(0, 6))
        self.server_viewer_players = tk.Listbox(right, bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], relief='flat', bd=0, highlightthickness=0, selectbackground=_CURRENT_PALETTE['bg_light'])
        self.server_viewer_players.grid(row=1, column=0, sticky='nsew')
        _set_pane_minsize(body, left, 280)
        _set_pane_minsize(body, right, 280)
        self.after_idle(lambda: self._center_server_viewer_pane(body))
    def _center_server_viewer_pane(body):
        try:
            width = body.winfo_width()
            if width > 0:
                body.sashpos(0, width // 2)
        except Exception:
            pass
    def _server_viewer_parse_deeplink(value):
        value = str(value or '').strip()
        if not value:
            raise ValueError(UI_TEXT['u28'])
        parsed = urlparse(value)
        query = parse_qs(parsed.query)
        place_id = None
        job_id = None
        for key in ('placeId', 'placeid', 'placeID'):
            if query.get(key):
                place_id = query[key][0]
                break
        for key in ('gameInstanceId', 'gameinstanceid', 'jobId', 'jobid'):
            if query.get(key):
                job_id = query[key][0]
                break
        if not place_id or not str(place_id).isdigit():
            m = re.search('(?:placeId|placeid)[=/](\\d+)', value, re.IGNORECASE)
            if m:
                place_id = m.group(1)
        if not job_id:
            m = re.search('(?:gameInstanceId|jobId|jobid)[=/]([0-9a-fA-F-]{32,36})', value, re.IGNORECASE)
            if m:
                job_id = m.group(1)
        if not place_id or not job_id:
            raise ValueError(UI_TEXT['v28'])
        return (str(place_id), str(job_id))
    def _server_viewer_clear(self):
        self.server_viewer_link.set('')
        for var in self.server_viewer_vars.values():
            var.set('—')
        self.server_viewer_players.delete(0, tk.END)
        self.server_viewer_status.config(text=UI_TEXT['h13'], foreground='#9aa0a6')
    def _server_viewer_load(self):
        try:
            place_id, job_id = self._server_viewer_parse_deeplink(self.server_viewer_link.get())
        except Exception as e:
            messagebox.showerror(UI_TEXT['n5'], str(e), parent=self)
            return
        self.server_viewer_status.config(text=UI_TEXT['l13'], foreground='#f2c94c')
        self._console_log(UI_TEXT['m13'].format(p0=self.server_viewer_link.get()))
        self.server_viewer_players.delete(0, tk.END)
        for var in self.server_viewer_vars.values():
            var.set('—')
        threading.Thread(target=self._server_viewer_worker, args=(place_id, job_id), daemon=True, name='RoUtils-ServerViewer').start()
    def _server_viewer_worker(self, place_id, job_id):
        try:
            cursor = None
            found = None
            pages = 0
            while pages < 50:
                pages += 1
                params = 'sortOrder=Asc&excludeFullGames=false&limit=100'
                if cursor:
                    params += '&cursor=' + quote(cursor, safe='')
                url = f'https://games.roblox.com/v1/games/{place_id}/servers/Public?{params}'
                with _routils_request(url, timeout=7) as r:
                    data = json.loads(r.read().decode('utf-8', 'replace'))
                for server in data.get('data', []):
                    if str(server.get('id', '')) == job_id:
                        found = server
                        break
                if found:
                    break
                cursor = data.get('nextPageCursor')
                if not cursor:
                    break
            if not found:
                raise ValueError('That server was not found in the public server list. It may have closed, be private, or no longer be listed.')
            players = found.get('playing', 0)
            max_players = found.get('maxPlayers', 0)
            ping = found.get('ping')
            fps = found.get('fps')
            tokens = found.get('playerTokens') or []
            public_players = found.get('players') or []
            result = {'place_id': place_id, 'job_id': job_id, 'players': f'{players}/{max_players}', 'max_players': str(max_players), 'ping': f'{round(float(ping))} ms' if ping is not None else '—', 'fps': f'{float(fps):.1f}' if fps is not None else '—', 'tokens': tokens, 'public_players': public_players}
            self.after(0, lambda result=result: self._server_viewer_show(result))
        except Exception as e:
            self.after(0, lambda msg=str(e): self._server_viewer_error(msg))
    def _server_viewer_show(self, result):
        for key in ('place_id', 'job_id', 'players', 'max_players', 'ping', 'fps'):
            self.server_viewer_vars[key].set(result[key])
        self.server_viewer_players.delete(0, tk.END)
        public_players = result.get('public_players') or []
        tokens = result.get('tokens') or []
        if public_players:
            for player in public_players:
                if isinstance(player, dict):
                    name = player.get('username') or player.get('name') or player.get('displayName') or str(player)
                else:
                    name = str(player)
                self.server_viewer_players.insert(tk.END, name)
        elif tokens:
            for i, token in enumerate(tokens, 1):
                self.server_viewer_players.insert(tk.END, f'Player {i}')
        else:
            self.server_viewer_players.insert(tk.END, '')
        self.server_viewer_status.config(text=UI_TEXT['n13'], foreground='#65d98b')
    def _server_viewer_error(self, message):
        self.server_viewer_status.config(text=UI_TEXT['o13'], foreground='#ff6b6b')
        messagebox.showerror(UI_TEXT['n5'], UI_TEXT['p13'].format(p0=message), parent=self)
