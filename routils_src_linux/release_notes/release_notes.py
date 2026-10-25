import sys
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
class ReleaseNotesMixin:
    def _build_release_notes_tab(self, tab=None):
        if tab is None:
            tab = ttk.Frame(self.nb, padding=0)
            self.nb.add(tab, text=UI_TEXT['t5'])
        else:
            for child in tab.winfo_children():
                child.destroy()
            tab.configure(padding=0)
            self.nb.tab(tab, text=UI_TEXT['t5'])
        self.release_notes_tab = tab
        self._release_notes_loading = False
        self._release_notes_image_refs = []
        palette = _CURRENT_PALETTE
        bg = palette.get('bg_dark', '#111318')
        card_bg = palette.get('bg_medium', '#1a1d24')
        fg = palette.get('fg', '#e6e9ef')
        accent = palette.get('accent', '#8ab4f8')
        border = palette.get('border', '#3b4351')
        hero = tk.Frame(tab, bg=card_bg, highlightthickness=1, highlightbackground=border, bd=0)
        hero.pack(fill='x', padx=12, pady=(12, 8))
        accent_bar = tk.Frame(hero, bg=accent, width=5)
        accent_bar.pack(side='left', fill='y')
        hero_content = tk.Frame(hero, bg=card_bg)
        hero_content.pack(side='left', fill='both', expand=True, padx=18, pady=15)
        top_line = tk.Frame(hero_content, bg=card_bg)
        top_line.pack(fill='x')
        title_block = tk.Frame(top_line, bg=card_bg)
        title_block.pack(side='left', fill='x', expand=True)
        tk.Label(title_block, text=UI_TEXT['c21'], bg=card_bg, fg=accent, font=('Segoe UI Semibold', 9), anchor='w').pack(anchor='w')
        tk.Label(title_block, text=UI_TEXT['d21'], bg=card_bg, fg=fg, font=('Segoe UI Semibold', 21), anchor='w').pack(anchor='w', pady=(2, 0))
        button_box = tk.Frame(top_line, bg=card_bg)
        button_box.pack(side='right', anchor='n', padx=(12, 0))
        self.release_notes_refresh_button = ttk.Button(button_box, text=UI_TEXT['c12'], command=lambda: self._refresh_release_notes(force=True))
        self.release_notes_refresh_button.pack(side='left', padx=(0, 6))
        ttk.Button(button_box, text=UI_TEXT['e21'], command=lambda: webbrowser.open(RELEASES_URL)).pack(side='left')
        status_row = tk.Frame(tab, bg=bg)
        status_row.pack(fill='x', padx=17, pady=(0, 5))
        self.release_notes_status = tk.Label(status_row, text=UI_TEXT['f21'], bg=bg, fg='#9aa8bd', font=('Segoe UI', 9), anchor='w')
        self.release_notes_status.pack(side='left', fill='x', expand=True)
        self.release_notes_scroll = _ScrollableTab(tab, padding=12)
        self.release_notes_scroll.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        self.release_notes_content = self.release_notes_scroll.inner
        self.release_notes_content.columnconfigure(0, weight=1)
        cached_releases = None
        cache_is_fresh = False
        try:
            cached_payload = _routils_load_http_cache(RELEASES_API_URL, 600, allow_stale=True)
            cache_is_fresh = _routils_load_http_cache(RELEASES_API_URL, 600) is not None
            if cached_payload is not None:
                parsed = json.loads(cached_payload[0].decode('utf-8', 'replace'))
                if isinstance(parsed, list):
                    cached_releases = parsed
        except Exception:
            cached_releases = None
            cache_is_fresh = False
        if cached_releases is not None:
            self.after_idle(lambda data=cached_releases: self._render_release_notes(data))
            self.after_idle(lambda fresh=cache_is_fresh: self._refresh_release_notes(force=not fresh))
        else:
            self.after_idle(lambda: self._refresh_release_notes(force=True))
    def _refresh_release_notes(self, force=False):
        if not hasattr(self, 'release_notes_tab') or not self.release_notes_tab.winfo_exists():
            return
        if getattr(self, '_release_notes_loading', False):
            return
        if not force:
            try:
                if _routils_load_http_cache(RELEASES_API_URL, 600) is not None:
                    return
            except Exception:
                pass
        self._release_notes_loading = True
        self.release_notes_status.configure(text=UI_TEXT['g21'], fg='#f2c94c')
        self.release_notes_refresh_button.configure(state='disabled')
        def worker():
            try:
                with _routils_request(RELEASES_API_URL, timeout=10, headers={'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}, cache_bypass=force) as response:
                    payload = response.read(5 * 1024 * 1024 + 1)
                if len(payload) > 5 * 1024 * 1024:
                    raise ValueError('GitHub release response exceeded the size limit.')
                releases = json.loads(payload.decode('utf-8', 'replace'))
                if not isinstance(releases, list):
                    raise ValueError('GitHub returned an unexpected release response.')
                self.after(0, lambda data=releases: self._render_release_notes(data))
            except Exception as exc:
                message = str(exc)
                self.after(0, lambda error=message: self._release_notes_failed(error))
        threading.Thread(target=worker, daemon=True, name='RoUtils-ReleaseNotes').start()
    def _release_notes_failed(self, error):
        self._release_notes_loading = False
        try:
            self.release_notes_refresh_button.configure(state='normal')
            self.release_notes_status.configure(text=UI_TEXT['h21'], fg='#ff8a80')
            if not self.release_notes_content.winfo_children():
                panel = tk.Frame(self.release_notes_content, bg=_CURRENT_PALETTE.get('bg_medium', '#1a1d24'), highlightthickness=1, highlightbackground=_CURRENT_PALETTE.get('border', '#3b4351'))
                panel.grid(row=0, column=0, sticky='ew', pady=5)
                tk.Label(panel, text=UI_TEXT['i21'], bg=_CURRENT_PALETTE.get('bg_medium', '#1a1d24'), fg=_CURRENT_PALETTE.get('fg', '#e6e9ef'), font=('Segoe UI Semibold', 12)).pack(anchor='w', padx=16, pady=(14, 4))
                tk.Label(panel, text=error, bg=_CURRENT_PALETTE.get('bg_medium', '#1a1d24'), fg='#ff8a80', justify='left', wraplength=900).pack(anchor='w', padx=16, pady=(0, 12))
                ttk.Button(panel, text=UI_TEXT['j21'], command=lambda: webbrowser.open(RELEASES_URL)).pack(anchor='w', padx=16, pady=(0, 14))
        except Exception:
            pass
    def _release_notes_extract_images(self, body):
        image_urls = []
        markdown_image = re.compile('!\\[([^\\]]*)\\]\\((https?://[^\\s)]+)(?:\\s+[^)]*)?\\)', re.IGNORECASE)
        html_image = re.compile('<img\\b[^>]*?\\bsrc\\s*=\\s*["\\\']([^"\\\']+)["\\\'][^>]*>', re.IGNORECASE)
        def keep_markdown(match):
            image_urls.append((html.unescape(match.group(2)), match.group(1).strip()))
            return ''
        body = markdown_image.sub(keep_markdown, body or '')
        def keep_html(match):
            image_urls.append((html.unescape(match.group(1).strip()), UI_TEXT['f32']))
            return ''
        body = html_image.sub(keep_html, body)
        unique = []
        seen = set()
        for url, alt in image_urls:
            if url.startswith(('https://', 'http://')) and url not in seen:
                seen.add(url)
                unique.append((url, alt or UI_TEXT['f32']))
        body = re.sub('<br\\s*/?>', '\n', body, flags=re.IGNORECASE)
        body = re.sub('</(?:p|div|li|h[1-6]|summary|details)\\s*>', '\n', body, flags=re.IGNORECASE)
        body = re.sub('<(?:p|div|li|h[1-6]|summary|details)\\b[^>]*>', '', body, flags=re.IGNORECASE)
        body = re.sub('<[^>]+>', '', body)
        body = html.unescape(body).replace('\r\n', '\n').replace('\r', '\n')
        body = re.sub('\\n{3,}', '\n\n', body).strip()
        body = re.sub('(?<!\\!)\\[([^\\]]+)\\]\\((https?://[^)]+)\\)', '\\1 (\\2)', body)
        return (body, unique)
    def _release_notes_insert_inline(self, widget, text, accent, fg, code_bg, link_index):
        pattern = re.compile('(\\*\\*.+?\\*\\*|`[^`]+`|\\*[^*]+\\*|\\[[^\\]]+\\]\\(https?://[^)]+\\)|https?://[^\\s<>]+)')
        cursor = 0
        for match in pattern.finditer(text):
            if match.start() > cursor:
                widget.insert('end', text[cursor:match.start()])
            token = match.group(0)
            if token.startswith('**') and token.endswith('**'):
                widget.insert('end', token[2:-2], 'bold')
            elif token.startswith('`') and token.endswith('`'):
                widget.insert('end', token[1:-1], 'code')
            elif token.startswith('*') and token.endswith('*'):
                widget.insert('end', token[1:-1], 'italic')
            elif token.startswith('[') and '](' in token:
                label, url = re.match('\\[([^\\]]+)\\]\\((https?://[^)]+)\\)', token).groups()
                tag = f'release_link_{link_index[0]}'
                link_index[0] += 1
                widget.insert('end', label, (tag, 'link'))
                widget.tag_bind(tag, '<Button-1>', lambda _event, target=url: webbrowser.open(target))
                widget.tag_bind(tag, '<Enter>', lambda _event: widget.configure(cursor='hand2'))
                widget.tag_bind(tag, '<Leave>', lambda _event: widget.configure(cursor=''))
            else:
                url = token.rstrip('.,;:)')
                suffix = token[len(url):]
                tag = f'release_link_{link_index[0]}'
                link_index[0] += 1
                widget.insert('end', url, (tag, 'link'))
                widget.insert('end', suffix)
                widget.tag_bind(tag, '<Button-1>', lambda _event, target=url: webbrowser.open(target))
                widget.tag_bind(tag, '<Enter>', lambda _event: widget.configure(cursor='hand2'))
                widget.tag_bind(tag, '<Leave>', lambda _event: widget.configure(cursor=''))
            cursor = match.end()
        if cursor < len(text):
            widget.insert('end', text[cursor:])
    def _release_notes_render_markdown(self, parent, body):
        palette = _CURRENT_PALETTE
        card_bg = palette.get('bg_medium', '#1a1d24')
        fg = palette.get('fg', '#e6e9ef')
        accent = palette.get('accent', '#8ab4f8')
        if not body:
            body = UI_TEXT['m29']
        lines = body.splitlines()
        estimated_lines = sum((max(1, math.ceil(len(line) / 100)) for line in lines)) + len(lines) // 2 + 1
        widget = tk.Text(parent, wrap='word', height=max(4, min(34, estimated_lines)), bg=card_bg, fg=fg, insertbackground=fg, relief='flat', bd=0, padx=0, pady=5, font=('Segoe UI', 10), spacing1=2, spacing3=3, selectbackground=accent)
        widget.tag_configure('h1', font=('Segoe UI Semibold', 15), foreground=accent, spacing1=8, spacing3=6)
        widget.tag_configure('h2', font=('Segoe UI Semibold', 13), foreground=accent, spacing1=7, spacing3=4)
        widget.tag_configure('h3', font=('Segoe UI Semibold', 11), foreground=accent, spacing1=6, spacing3=3)
        widget.tag_configure('bold', font=('Segoe UI Semibold', 10), foreground=fg)
        widget.tag_configure('italic', font=('Segoe UI', 10, 'italic'), foreground=fg)
        widget.tag_configure('code', font=('Cascadia Code', 9), foreground='#a6e3a1', background=palette.get('bg_dark', '#111318'))
        widget.tag_configure('link', foreground=accent, underline=True)
        link_index = [0]
        for line in lines:
            stripped = line.strip()
            if not stripped:
                widget.insert('end', '\n')
                continue
            heading = re.match('^(#{1,3})\\s+(.*)$', stripped)
            if heading:
                level = len(heading.group(1))
                self._release_notes_insert_inline(widget, heading.group(2), accent, fg, card_bg, link_index)
                widget.insert('end', '\n', f'h{level}')
                continue
            bullet = re.match('^\\s*[-*+]\\s+(.*)$', line)
            ordered = re.match('^\\s*\\d+[.)]\\s+(.*)$', line)
            if bullet:
                widget.insert('end', '  •  ')
                self._release_notes_insert_inline(widget, bullet.group(1), accent, fg, card_bg, link_index)
            elif ordered:
                widget.insert('end', '  ')
                self._release_notes_insert_inline(widget, ordered.group(1), accent, fg, card_bg, link_index)
            else:
                self._release_notes_insert_inline(widget, line, accent, fg, card_bg, link_index)
            widget.insert('end', '\n')
        widget.configure(state='disabled')
        widget.pack(fill='x', expand=True, pady=(4, 0))
        return widget
    def _release_notes_load_image(self, url, label, alt):
        def worker():
            try:
                with _routils_request(url, timeout=12, headers={'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8'}) as response:
                    content = response.read(8 * 1024 * 1024 + 1)
                if not content or len(content) > 8 * 1024 * 1024:
                    raise ValueError('Image exceeded the allowed size.')
                with Image.open(io.BytesIO(content)) as opened:
                    image_data = opened.convert('RGBA')
                resampling = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
                image_data.thumbnail((720, 320), resampling)
                self.after(0, lambda img=image_data: self._release_notes_apply_image(label, img, alt))
            except Exception:
                self.after(0, lambda: self._release_notes_image_failed(label, alt))
        threading.Thread(target=worker, daemon=True, name='RoUtils-ReleaseImage').start()
    def _release_notes_apply_image(self, label, image_data, alt):
        try:
            if not label.winfo_exists():
                return
            photo = ImageTk.PhotoImage(image_data, master=self)
            label.configure(image=photo, text=UI_TEXT['m1'], compound='top', width=0, height=0, padx=4, pady=4)
            label.image = photo
            self._release_notes_image_refs.append(photo)
        except Exception:
            self._release_notes_image_failed(label, alt)
    def _release_notes_image_failed(self, label, alt):
        try:
            if label.winfo_exists():
                label.configure(text=UI_TEXT['k21'].format(p0=alt), fg='#9aa8bd', padx=10, pady=8)
        except Exception:
            pass
    def _render_release_notes(self, releases):
        self._release_notes_loading = False
        self.release_notes_refresh_button.configure(state='normal')
        for child in self.release_notes_content.winfo_children():
            child.destroy()
        self._release_notes_image_refs = []
        if not releases:
            self.release_notes_status.configure(text=UI_TEXT['l21'], fg='#9aa8bd')
            return
        visible_count = 0
        image_count = 0
        palette = _CURRENT_PALETTE
        bg = palette.get('bg_dark', '#111318')
        card_bg = palette.get('bg_medium', '#1a1d24')
        fg = palette.get('fg', '#e6e9ef')
        accent = palette.get('accent', '#8ab4f8')
        border = palette.get('border', '#3b4351')
        releases = [item for item in releases if isinstance(item, dict) and (not item.get('draft'))]
        if not releases:
            self.release_notes_status.configure(text=UI_TEXT['l21'], fg='#9aa8bd')
            return
        stable = next((item for item in releases if not item.get('prerelease')), releases[0])
        self.release_notes_status.configure(text=UI_TEXT['m21'].format(p0=len(releases)), fg='#65d98b')
        for index, release in enumerate(releases):
            visible_count += 1
            tag = str(release.get('tag_name') or '').strip()
            name = str(release.get('name') or tag or 'Untitled release').strip()
            published = str(release.get('published_at') or release.get('created_at') or '').strip()
            date_text = published[:10] if len(published) >= 10 else UI_TEXT['k29']
            is_latest = release is stable
            is_prerelease = bool(release.get('prerelease'))
            raw_body = str(release.get('body') or '')
            body, images = self._release_notes_extract_images(raw_body)
            card = tk.Frame(self.release_notes_content, bg=card_bg, highlightthickness=1, highlightbackground=border, bd=0)
            card.grid(row=visible_count - 1, column=0, sticky='ew', pady=(0, 12))
            card.columnconfigure(1, weight=1)
            strip = tk.Frame(card, bg=accent if is_latest else border, width=4)
            strip.grid(row=0, column=0, rowspan=6, sticky='ns')
            content = tk.Frame(card, bg=card_bg)
            content.grid(row=0, column=1, sticky='ew', padx=16, pady=13)
            content.columnconfigure(0, weight=1)
            title_row = tk.Frame(content, bg=card_bg)
            title_row.grid(row=0, column=0, sticky='ew')
            title_label = tk.Label(title_row, text=name, bg=card_bg, fg=fg, font=('Segoe UI Semibold', 14), anchor='w', justify='left', wraplength=890)
            title_label.pack(side='left', fill='x', expand=True)
            if tag:
                tk.Label(title_row, text=UI_TEXT['n21'].format(p0=tag), bg=palette.get('bg_dark', '#111318'), fg=accent, font=('Cascadia Code', 9), padx=5, pady=3).pack(side='right', padx=(8, 0))
            meta = tk.Frame(content, bg=card_bg)
            meta.grid(row=1, column=0, sticky='ew', pady=(5, 1))
            tk.Label(meta, text=date_text, bg=card_bg, fg='#9aa8bd', font=('Segoe UI', 9)).pack(side='left')
            badge_text = UI_TEXT['l29'] if is_latest else 'PRE-RELEASE' if is_prerelease else 'RELEASE'
            badge_bg = '#214d3b' if is_latest else palette.get('bg_dark', '#111318')
            badge_fg = '#8de0ad' if is_latest else '#ffcf86' if is_prerelease else '#9aa8bd'
            tk.Label(meta, text=UI_TEXT['n21'].format(p0=badge_text), bg=badge_bg, fg=badge_fg, font=('Segoe UI Semibold', 8), padx=5, pady=2).pack(side='left', padx=(9, 0))
            body_wrap = tk.Frame(content, bg=card_bg)
            body_wrap.grid(row=2, column=0, sticky='ew', pady=(4, 0))
            self._release_notes_render_markdown(body_wrap, body)
            if images:
                gallery = tk.Frame(content, bg=card_bg)
                gallery.grid(row=3, column=0, sticky='ew', pady=(8, 2))
                for image_url, image_alt in images[:4]:
                    if image_count >= 8:
                        break
                    image_count += 1
                    holder = tk.Frame(gallery, bg=bg, highlightthickness=1, highlightbackground=border)
                    holder.pack(side='left', anchor='nw', padx=(0, 8), pady=3)
                    preview = tk.Label(holder, text=UI_TEXT['o21'].format(p0=image_alt), bg=bg, fg='#9aa8bd', font=('Segoe UI', 8), width=28, height=5, wraplength=190, justify='center')
                    preview.pack(padx=2, pady=2)
                    ttk.Button(holder, text=UI_TEXT['p21'], command=lambda url=image_url: webbrowser.open(url)).pack(fill='x', padx=4, pady=(0, 4))
                    self._release_notes_load_image(image_url, preview, image_alt)
            footer = tk.Frame(content, bg=card_bg)
            footer.grid(row=4, column=0, sticky='ew', pady=(8, 0))
            ttk.Button(footer, text=UI_TEXT['q21'], command=lambda url=release.get('html_url') or RELEASES_URL: webbrowser.open(url)).pack(side='left')
            assets = release.get('assets') if isinstance(release.get('assets'), list) else []
            tk.Label(footer, text=UI_TEXT['r21'].format(p0=len(assets)) + (UI_TEXT['m1'] if len(assets) == 1 else UI_TEXT['s21']), bg=card_bg, fg='#9aa8bd', font=('Segoe UI', 9)).pack(side='left', padx=(10, 0))
            if assets:
                asset_row = tk.Frame(content, bg=card_bg)
                asset_row.grid(row=5, column=0, sticky='ew', pady=(6, 0))
                for asset in assets[:5]:
                    if not isinstance(asset, dict):
                        continue
                    asset_name = str(asset.get('name') or 'Download')
                    if len(asset_name) > 30:
                        asset_name = asset_name[:27] + '…'
                    url = str(asset.get('browser_download_url') or '')
                    if url.startswith('https://'):
                        ttk.Button(asset_row, text=asset_name, command=lambda target=url: webbrowser.open(target)).pack(side='left', padx=(0, 5), pady=2)
                if len(assets) > 5:
                    tk.Label(asset_row, text=UI_TEXT['t21'].format(p0=len(assets) - 5), bg=card_bg, fg='#9aa8bd', font=('Segoe UI', 9)).pack(side='left', padx=3)
        if visible_count == 0:
            tk.Label(self.release_notes_content, text=UI_TEXT['u21'], bg=bg, fg=fg, font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=20)
