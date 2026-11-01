import json
import os
import shutil
import subprocess
import tempfile
import threading
import tkinter as tk
import sys
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
        tab.rowconfigure(4, weight=0)
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
        console_frame = ttk.LabelFrame(tab, text='Console', padding=7)
        console_frame.grid(row=3, column=0, sticky='nsew')
        console_frame.rowconfigure(0, weight=1)
        console_frame.columnconfigure(0, weight=1)
        self.luau_console = tk.Text(console_frame, wrap='word', state='disabled', bg=palette.get('bg_dark', '#17191f'), fg=palette.get('fg', '#e6e9ef'), insertbackground=palette.get('fg', '#e6e9ef'), relief='flat', borderwidth=0, padx=10, pady=8, font=('Consolas', 9))
        console_scroll = ttk.Scrollbar(console_frame, orient='vertical', command=self.luau_console.yview)
        self.luau_console.configure(yscrollcommand=console_scroll.set)
        self.luau_console.grid(row=0, column=0, sticky='nsew')
        console_scroll.grid(row=0, column=1, sticky='ns')
        input_bar = ttk.Frame(tab)
        input_bar.grid(row=4, column=0, sticky='ew', pady=(7, 0))
        input_bar.columnconfigure(1, weight=1)
        ttk.Label(input_bar, text='$', font=('Consolas', 10, 'bold')).grid(row=0, column=0, padx=(2, 8))
        self.luau_input_var = tk.StringVar(value='')
        self.luau_input_entry = ttk.Entry(input_bar, textvariable=self.luau_input_var)
        self.luau_input_entry.grid(row=0, column=1, sticky='ew')
        self.luau_input_entry.bind('<Return>', self._luau_queue_input)
        self.luau_input_queue_status = tk.StringVar(value='0 input lines queued')
        ttk.Label(input_bar, textvariable=self.luau_input_queue_status, foreground='#9aa0a6').grid(row=0, column=2, padx=(8, 8))
        ttk.Button(input_bar, text='Queue', command=self._luau_queue_input).grid(row=0, column=3)
        self._luau_input_queue = []
        self._luau_running = False
        self._luau_run_token = 0
        self._luau_console_write('Luau runs locally in a separate process. It does not attach to or inject into Roblox.\n')
        self._luau_console_write('Type input below before Run; io.read() consumes queued lines and io.write() prints to this console.\n')

    def _luau_queue_input(self, _event=None):
        value = self.luau_input_var.get()
        if len(value.encode('utf-8')) > 8192:
            self._luau_console_write('Input line limit exceeded: 8 KiB maximum.\n')
            return 'break'
        if len(self._luau_input_queue) >= 256:
            self._luau_console_write('Input queue limit reached: 256 lines maximum.\n')
            return 'break'
        self._luau_input_queue.append(value)
        self._luau_console_write(f'$ {value}\n')
        self.luau_input_var.set('')
        self.luau_input_queue_status.set(f'{len(self._luau_input_queue)} input lines queued')
        self.luau_input_entry.focus_set()
        return 'break'

    @staticmethod
    def _luau_io_compatibility_source(input_lines):
        encoded_lines = '{' + ','.join(json.dumps(str(line), ensure_ascii=False) for line in input_lines) + '}'
        return '''local __routils_input_values = INPUT_LINES
local __routils_input_index = 0
local function __routils_read(format)
    format = format or "*l"
    if format == "*a" then
        local remaining = {}
        while __routils_input_index < #__routils_input_values do
            __routils_input_index += 1
            remaining[#remaining + 1] = __routils_input_values[__routils_input_index]
        end
        return table.concat(remaining, "\n")
    end
    if __routils_input_index >= #__routils_input_values then
        print("[RoUtils] No queued input remains. Type a line below the console before Run.")
        return nil
    end
    __routils_input_index += 1
    local value = __routils_input_values[__routils_input_index]
    if format == "*n" then
        return tonumber(value)
    elseif format == "*L" then
        return value .. "\n"
    end
    return value
end
local function __routils_write(...)
    local values = {...}
    local output = {}
    for index, value in ipairs(values) do
        output[index] = tostring(value)
    end
    print(table.concat(output, ""))
    return true
end
local function __routils_lines()
    return function()
        return __routils_read("*l")
    end
end
local __routils_io = {}
__routils_io.read = __routils_read
__routils_io.write = __routils_write
__routils_io.lines = __routils_lines
__routils_io.flush = function() return true end
__routils_io.stdin = {
    read = function(first, second)
        if first == __routils_io.stdin then
            return __routils_read(second)
        end
        return __routils_read(first)
    end
}
__routils_io.stdout = {
    write = function(first, ...)
        if first == __routils_io.stdout then
            return __routils_write(...)
        end
        return __routils_write(first, ...)
    end,
    flush = function() return true end
}
io = __routils_io
'''.replace('INPUT_LINES', encoded_lines)

    def _luau_find_runtime(self):
        bundle_root = getattr(sys, '_MEIPASS', '')
        source_root = os.path.dirname(os.path.abspath(__file__))
        app_root = os.path.dirname(source_root)
        executable = 'luau.exe' if os.name == 'nt' else 'luau'
        candidates = []
        if bundle_root:
            candidates.append(os.path.join(bundle_root, 'bin', executable))
        candidates.extend((
            os.path.join(app_root, 'bin', executable),
            os.path.join(source_root, 'bin', executable),
            shutil.which(executable) or '',
            shutil.which('luau') or '',
        ))
        if os.name != 'nt':
            candidates.extend((
                os.path.expanduser('~/.local/bin/luau'),
                '/usr/local/bin/luau',
                '/usr/bin/luau',
            ))
        seen = set()
        for candidate in candidates:
            if not candidate:
                continue
            candidate = os.path.abspath(candidate)
            if candidate in seen:
                continue
            seen.add(candidate)
            if os.path.isfile(candidate) and (os.name == 'nt' or os.access(candidate, os.X_OK)):
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
        queued_inputs = list(self._luau_input_queue)
        if not source.strip():
            self._luau_console_write('No code to run.\n')
            return
        if len(source.encode('utf-8')) > 262144:
            self._luau_console_write('Code limit exceeded: 256 KiB maximum.\n')
            return
        source = self._luau_io_compatibility_source(queued_inputs) + '\n' + source
        runtime = self._luau_find_runtime()
        if not runtime:
            self.luau_status_var.set('Luau CLI not found')
            self._luau_console_write('The Luau CLI is missing. Rebuild RoUtils with the platform compile script or GitHub Actions workflow.\n')
            return
        del self._luau_input_queue[:len(queued_inputs)]
        self.luau_input_queue_status.set(f'{len(self._luau_input_queue)} input lines queued')
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
                    result = subprocess.run([runtime, script_path], cwd=workdir, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=8, check=False, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
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
