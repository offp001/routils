import os
import shutil
import subprocess
import tempfile
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk

_host = __import__('sys').modules.get('main') or __import__('sys').modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})


class LuauInterpreterMixin:
    def _build_luau_interpreter_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text='Luau Interpreter')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=3)
        tab.rowconfigure(3, weight=2)
        header = ttk.Frame(tab)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(header, text='Luau Interpreter', font=('Segoe UI Semibold', 15)).pack(side='left')
        self.luau_status_var = tk.StringVar(value='Ready')
        ttk.Label(header, textvariable=self.luau_status_var, foreground='#9aa0a6').pack(side='right')
        editor_frame = ttk.LabelFrame(tab, text='Code', padding=7)
        editor_frame.grid(row=1, column=0, sticky='nsew')
        editor_frame.rowconfigure(0, weight=1)
        editor_frame.columnconfigure(0, weight=1)
        palette = globals().get('_CURRENT_PALETTE', {})
        self.luau_editor = tk.Text(editor_frame, wrap='none', undo=True, bg=palette.get('bg_dark', '#17191f'), fg=palette.get('fg', '#e6e9ef'), insertbackground=palette.get('fg', '#e6e9ef'), selectbackground=palette.get('accent', '#5865f2'), relief='flat', borderwidth=0, padx=10, pady=9, font=('Consolas', 10))
        ybar = ttk.Scrollbar(editor_frame, orient='vertical', command=self.luau_editor.yview)
        xbar = ttk.Scrollbar(editor_frame, orient='horizontal', command=self.luau_editor.xview)
        self.luau_editor.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        self.luau_editor.grid(row=0, column=0, sticky='nsew')
        ybar.grid(row=0, column=1, sticky='ns')
        xbar.grid(row=1, column=0, sticky='ew')
        self.luau_editor.insert('1.0', 'print("hello")\n')
        controls = ttk.Frame(tab)
        controls.grid(row=2, column=0, sticky='ew', pady=8)
        self.luau_run_button = ttk.Button(controls, text='Run', command=self._luau_run_code)
        self.luau_run_button.pack(side='left')
        ttk.Button(controls, text='Clear Console', command=self._luau_clear_console).pack(side='left', padx=(6, 0))
        ttk.Button(controls, text='Example', command=self._luau_load_example).pack(side='left', padx=(6, 0))
        ttk.Button(controls, text='Install Guide', command=lambda: webbrowser.open('https://luau.org/getting-started/')).pack(side='right')
        console_frame = ttk.LabelFrame(tab, text='Console', padding=7)
        console_frame.grid(row=3, column=0, sticky='nsew')
        console_frame.rowconfigure(0, weight=1)
        console_frame.columnconfigure(0, weight=1)
        self.luau_console = tk.Text(console_frame, wrap='word', state='disabled', bg=palette.get('bg_dark', '#17191f'), fg=palette.get('fg', '#e6e9ef'), insertbackground=palette.get('fg', '#e6e9ef'), relief='flat', borderwidth=0, padx=10, pady=8, font=('Consolas', 9))
        console_scroll = ttk.Scrollbar(console_frame, orient='vertical', command=self.luau_console.yview)
        self.luau_console.configure(yscrollcommand=console_scroll.set)
        self.luau_console.grid(row=0, column=0, sticky='nsew')
        console_scroll.grid(row=0, column=1, sticky='ns')
        self._luau_running = False
        self._luau_run_token = 0
        self._luau_console_write('Luau runs locally in a separate process. It does not attach to or inject into Roblox.\n')

    def _luau_find_runtime(self):
        runtime = shutil.which('luau')
        if runtime:
            return runtime
        candidates = (
            os.path.join(os.path.dirname(__file__), 'bin', 'luau'),
            os.path.expanduser('~/.local/bin/luau'),
            '/usr/local/bin/luau',
            '/usr/bin/luau',
        )
        for candidate in candidates:
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
        return None

    def _luau_console_write(self, value):
        console = getattr(self, 'luau_console', None)
        if console is None or not console.winfo_exists():
            return
        console.configure(state='normal')
        console.insert('end', str(value))
        console.see('end')
        console.configure(state='disabled')

    def _luau_clear_console(self):
        self.luau_console.configure(state='normal')
        self.luau_console.delete('1.0', 'end')
        self.luau_console.configure(state='disabled')

    def _luau_load_example(self):
        self.luau_editor.delete('1.0', 'end')
        self.luau_editor.insert('1.0', 'local numbers = {1, 2, 3, 4, 5}\nlocal total = 0\n\nfor _, number in numbers do\n    total += number\nend\n\nprint("Total:", total)\n')

    def _luau_run_code(self):
        if getattr(self, '_luau_running', False):
            return
        source = self.luau_editor.get('1.0', 'end-1c')
        if not source.strip():
            self._luau_console_write('No code to run.\n')
            return
        if len(source.encode('utf-8')) > 262144:
            self._luau_console_write('Code limit exceeded: 256 KiB maximum.\n')
            return
        runtime = self._luau_find_runtime()
        if not runtime:
            self.luau_status_var.set('Luau CLI not found')
            self._luau_console_write('Luau CLI was not found. On Arch Linux install it with:\nsudo pacman -S --needed luau\n\nThen restart RoUtils.\n')
            return
        self._luau_running = True
        self._luau_run_token += 1
        token = self._luau_run_token
        self.luau_run_button.configure(state='disabled')
        self.luau_status_var.set('Running…')
        self._luau_console_write('> Running script\n')

        def worker():
            output = ''
            exit_code = None
            try:
                with tempfile.TemporaryDirectory(prefix='routils_luau_') as workdir:
                    script_path = os.path.join(workdir, 'main.luau')
                    with open(script_path, 'w', encoding='utf-8', newline='') as stream:
                        stream.write(source)
                    result = subprocess.run([runtime, script_path], cwd=workdir, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=8, check=False)
                    exit_code = int(result.returncode)
                    output = (result.stdout or '') + (result.stderr or '')
            except subprocess.TimeoutExpired as error:
                output = 'Execution timed out after 8 seconds.\n'
                if error.stdout:
                    output += error.stdout.decode('utf-8', 'replace') if isinstance(error.stdout, bytes) else str(error.stdout)
                if error.stderr:
                    output += error.stderr.decode('utf-8', 'replace') if isinstance(error.stderr, bytes) else str(error.stderr)
                exit_code = -1
            except Exception as error:
                output = f'{type(error).__name__}: {error}\n'
                exit_code = -1
            output = output[:200000]
            try:
                self.after(0, self._luau_run_finished, token, output, exit_code)
            except Exception:
                pass

        threading.Thread(target=worker, name='RoUtilsLuauInterpreter', daemon=True).start()

    def _luau_run_finished(self, token, output, exit_code):
        if token != getattr(self, '_luau_run_token', 0):
            return
        self._luau_running = False
        self.luau_run_button.configure(state='normal')
        if output:
            self._luau_console_write(output)
            if not output.endswith('\n'):
                self._luau_console_write('\n')
        if exit_code == 0:
            self.luau_status_var.set('Finished')
            self._luau_console_write('[Process exited with code 0]\n')
        else:
            self.luau_status_var.set(f'Exit code: {exit_code}')
            self._luau_console_write(f'[Process exited with code {exit_code}]\n')
