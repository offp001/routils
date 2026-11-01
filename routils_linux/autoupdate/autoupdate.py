import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import webbrowser
import zipfile
_host = sys.modules.get('main') or sys.modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})

class AutoUpdateMixin:
    def _version_path(self):
        return os.path.join(DATA_DIR, 'version.txt')

    def _reset_version_file(self):
        try:
            vp = self._version_path()
            if os.path.exists(vp):
                try:
                    os.remove(vp)
                except Exception:
                    pass
            with open(vp, 'w', encoding='utf-8') as f:
                f.write(APP_VERSION)
        except Exception:
            pass

    def _local_version(self):
        try:
            if not os.path.exists(self._version_path()):
                with open(self._version_path(), 'w', encoding='utf-8') as f:
                    f.write(APP_VERSION)
            with open(self._version_path(), encoding='utf-8') as f:
                return f.read().strip() or APP_VERSION
        except Exception:
            return APP_VERSION

    def _set_update_progress(self, downloaded=0, total=0, visible=True):
        try:
            if visible:
                self.home_download_frame.pack(side='bottom', anchor='w', fill='x', padx=10, pady=10)
                if total > 0:
                    self.home_download_progress.configure(mode='determinate', maximum=total, value=downloaded)
                    self.home_download_label.configure(text=UI_TEXT['h10'].format(p0=downloaded / total * 100))
                else:
                    self.home_download_progress.configure(mode='indeterminate')
                    self.home_download_progress.start(12)
                    self.home_download_label.configure(text=UI_TEXT['g10'])
            else:
                try:
                    self.home_download_progress.stop()
                except Exception:
                    pass
                self.home_download_frame.pack_forget()
        except Exception:
            pass

    @staticmethod
    def _version_tuple(version):
        parts = re.findall('\\d+', str(version or ''))
        if not parts:
            return (0,)
        return tuple((int(x) for x in parts[:4]))

    def _is_newer_version(self, latest, current):
        return self._version_tuple(latest) > self._version_tuple(current)

    def _show_outdated_dialog(self, latest):
        if self._outdated_dialog_shown or self._auto_update_in_progress:
            return
        self._outdated_dialog_shown = True
        try:
            dlg = tk.Toplevel(self)
            dlg.title('RoUtils is Outdated')
            dlg.resizable(False, False)
            dlg.transient(self)
            dlg.grab_set()
            theme_toplevel(dlg)
            width, height = (440, 230)
            self.update_idletasks()
            x = max(0, (self.winfo_screenwidth() - width) // 2)
            y = max(0, (self.winfo_screenheight() - height) // 2)
            dlg.geometry(f'{width}x{height}+{x}+{y}')
            outer = ttk.Frame(dlg, padding=24)
            outer.pack(fill='both', expand=True)
            ttk.Label(outer, text=UI_TEXT['i10'], font=('Segoe UI Semibold', 18)).pack(pady=(8, 8))
            ttk.Label(outer, text=UI_TEXT['j10'].format(p0=latest), font=('Segoe UI', 11)).pack(pady=(0, 20))
            buttons = ttk.Frame(outer)
            buttons.pack()
            def download():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                try:
                    dlg.destroy()
                except Exception:
                    pass
                webbrowser.open(f'https://github.com/offp001/routils/releases/tag/{latest}')
            def later():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                try:
                    dlg.destroy()
                except Exception:
                    pass
            ttk.Button(buttons, text=UI_TEXT['k10'], command=download).pack(side='left', padx=6)
            ttk.Button(buttons, text=UI_TEXT['l10'], command=later).pack(side='left', padx=6)
            dlg._routils_close_callback = later
            dlg.protocol('WM_DELETE_WINDOW', later)
            dlg.after(100, lambda d=dlg: (_routils_popup_chrome(d), d.lift(), d.focus_force()) if d.winfo_exists() else None)
            dlg.focus_force()
        except Exception:
            self._outdated_dialog_shown = False

    def _start_auto_update(self, latest):
        if self._auto_update_in_progress:
            return
        self._auto_update_in_progress = True
        def worker():
            temp_path = None
            target_dir = None
            try:
                current = self._local_version()
                if not self._is_newer_version(latest, current):
                    self._auto_update_in_progress = False
                    return
                is_windows = os.name == 'nt'
                archive_name = 'RoUtils-Windows.zip' if is_windows else 'RoUtils-Linux.zip'
                executable_name = 'RoUtils.exe' if is_windows else 'RoUtils-Linux'
                download_url = f'https://github.com/offp001/routils/releases/download/{latest}/{archive_name}'
                safe_version = re.sub(r'[^A-Za-z0-9._-]', '_', str(latest))
                updates_root = os.path.join(DATA_DIR, 'updates')
                target_dir = os.path.join(updates_root, safe_version)
                temp_path = os.path.join(tempfile.gettempdir(), f'{archive_name}.{safe_version}.download')
                self.after(0, lambda: self._set_update_progress(0, 0, True))
                self.after(0, lambda v=latest: self._console_log(UI_TEXT['m10'].format(p0=v)))
                with _routils_request(download_url, timeout=60, headers={'Accept': 'application/octet-stream, */*'}) as response:
                    total = int(response.headers.get('Content-Length', '0') or 0)
                    downloaded = 0
                    with open(temp_path, 'wb') as out:
                        while True:
                            chunk = response.read(1024 * 256)
                            if not chunk:
                                break
                            out.write(chunk)
                            downloaded += len(chunk)
                            self.after(0, lambda d=downloaded, t=total: self._set_update_progress(d, t, True))
                if not os.path.isfile(temp_path) or os.path.getsize(temp_path) < 1024:
                    raise RuntimeError(f'{archive_name} download is invalid.')
                os.makedirs(updates_root, exist_ok=True)
                if os.path.isdir(target_dir):
                    shutil.rmtree(target_dir)
                os.makedirs(target_dir, exist_ok=True)
                with zipfile.ZipFile(temp_path, 'r') as archive:
                    invalid_member = archive.testzip()
                    if invalid_member:
                        raise RuntimeError(f'ZIP integrity check failed: {invalid_member}')
                    root_real = os.path.realpath(target_dir)
                    for info in archive.infolist():
                        destination = os.path.realpath(os.path.join(root_real, info.filename))
                        if os.path.commonpath((root_real, destination)) != root_real:
                            raise RuntimeError('The update archive contains an unsafe file path.')
                    archive.extractall(target_dir)
                executable_path = None
                for folder, _, filenames in os.walk(target_dir):
                    if executable_name in filenames:
                        executable_path = os.path.join(folder, executable_name)
                        break
                if not executable_path or not os.path.isfile(executable_path):
                    raise RuntimeError(f'{executable_name} was not found in {archive_name}.')
                if not is_windows:
                    os.chmod(executable_path, os.stat(executable_path).st_mode | 0o111)
                self.after(0, lambda p=executable_path: self._console_log(UI_TEXT['n10'].format(p0=p)))
                launch_options = {'cwd': os.path.dirname(executable_path), 'close_fds': True}
                if is_windows:
                    launch_options['creationflags'] = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)
                else:
                    launch_options['start_new_session'] = True
                subprocess.Popen([executable_path], **launch_options)
                self.after(0, lambda: (self._set_update_progress(0, 0, False), self._on_close(force=True)))
            except Exception as error:
                self._auto_update_in_progress = False
                try:
                    self.after(0, lambda err=str(error): self._console_log(UI_TEXT['o10'].format(p0=err)))
                except Exception:
                    pass
                try:
                    self.after(0, lambda: self._set_update_progress(0, 0, False))
                except Exception:
                    pass
                try:
                    if temp_path and os.path.isfile(temp_path):
                        os.remove(temp_path)
                except Exception:
                    pass
                try:
                    self.after(0, lambda err=str(error): self._show_update_error(err))
                except Exception:
                    pass
        threading.Thread(target=worker, daemon=True, name='RoUtils-AutoUpdate').start()

    def _show_update_error(self, error):
        self._auto_update_in_progress = False
        try:
            messagebox.showwarning(UI_TEXT['p10'], UI_TEXT['q10'].format(p0=error), parent=self)
        except Exception:
            pass

    def _start_version_check(self):
        if getattr(self, '_version_check_started', False):
            return
        self._version_check_started = True
        self._version_check_result_queue = queue.Queue()
        current = self._local_version()
        try:
            self.home_version_value.configure(text=current)
            self.home_version_state.configure(text='Checking...', foreground='#f2c94c')
            self.home_version_var.set(UI_TEXT['r10'].format(p0=current, p1='Checking...'))
        except Exception:
            pass
        def worker():
            current_version = current
            errors = []
            latest = ''
            endpoints = (
                ('https://api.github.com/repos/offp001/routils/releases/latest', 'single'),
                ('https://api.github.com/repos/offp001/routils/releases?per_page=1', 'list'),
            )
            for url, response_kind in endpoints:
                try:
                    with _routils_request(url, timeout=2.5, headers={'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}) as response:
                        payload = response.read(256 * 1024)
                    data = json.loads(payload.decode('utf-8', 'replace'))
                    if response_kind == 'list':
                        if not isinstance(data, list) or not data:
                            raise ValueError('No published releases were returned')
                        release = data[0]
                    else:
                        release = data
                    if not isinstance(release, dict):
                        raise ValueError('Invalid release response')
                    tag = str(release.get('tag_name', '')).strip()
                    if not tag:
                        raise ValueError('The release response did not contain tag_name')
                    latest = tag.lstrip('vV').strip()
                    if not latest:
                        raise ValueError('The release tag was empty')
                    break
                except Exception as error:
                    errors.append(f'{url}: {error}')
            if latest:
                try:
                    outdated = self._is_newer_version(latest, current_version)
                    state = 'Outdated' if outdated else 'Latest'
                    color = '#ff5f57' if outdated else '#65d98b'
                    result = {'current': current_version, 'latest': latest, 'state': state, 'color': color, 'outdated': outdated, 'error': ''}
                except Exception as error:
                    result = {'current': current_version, 'latest': '', 'retry': True, 'error': str(error)}
            else:
                result = {'current': current_version, 'latest': '', 'retry': True, 'error': ' | '.join(errors) or 'Version endpoint unavailable'}
            try:
                self._version_check_result_queue.put_nowait(result)
            except Exception:
                pass
        self._version_check_worker = threading.Thread(target=worker, daemon=True, name='RoUtils-VersionCheck')
        self._version_check_worker.start()
        try:
            self._version_check_poll_after = self.after(40, self._poll_version_check_result)
        except Exception:
            self._version_check_poll_after = None

    def _retry_version_check(self):
        self._version_check_retry_after = None
        self._version_check_started = False
        try:
            if self.winfo_exists():
                self._start_version_check()
        except Exception:
            pass

    def _poll_version_check_result(self):
        try:
            result_queue = getattr(self, '_version_check_result_queue', None)
            result = result_queue.get_nowait() if result_queue is not None else None
        except queue.Empty:
            result = None
        except Exception:
            result = None
        if result is None:
            try:
                if self.winfo_exists():
                    self._version_check_poll_after = self.after(60, self._poll_version_check_result)
            except Exception:
                self._version_check_poll_after = None
            return
        current = str(result.get('current') or self._local_version())
        if result.get('retry'):
            try:
                self.home_version_value.configure(text=current)
                self.home_version_state.configure(text='Checking...', foreground='#f2c94c')
                self.home_version_var.set(UI_TEXT['r10'].format(p0=current, p1='Checking...'))
            except Exception:
                pass
            try:
                logging.getLogger('RoUtils').debug('Version check will retry: %s', result.get('error', 'unavailable'))
            except Exception:
                pass
            try:
                if self.winfo_exists():
                    old_job = getattr(self, '_version_check_retry_after', None)
                    if old_job:
                        try:
                            self.after_cancel(old_job)
                        except Exception:
                            pass
                    self._version_check_retry_after = self.after(2500, self._retry_version_check)
            except Exception:
                self._version_check_retry_after = None
            return
        latest = str(result.get('latest') or current)
        state = str(result.get('state') or 'Latest')
        color = str(result.get('color') or '#65d98b')
        self._latest_version = latest
        try:
            self.home_version_value.configure(text=current)
            self.home_version_state.configure(text=state, foreground=color)
            self.home_version_var.set(UI_TEXT['r10'].format(p0=current, p1=state))
        except Exception:
            pass
        if result.get('outdated'):
            if self.auto_update.get():
                self._start_auto_update(latest)
            else:
                self._show_outdated_dialog(latest)
