import ctypes
import ctypes.wintypes
import os


def _windows_process_path(pid):
    handle = None
    try:
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel32.OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
        kernel32.OpenProcess.restype = ctypes.wintypes.HANDLE
        handle = kernel32.OpenProcess(4096, False, int(pid))
        if not handle:
            return ''
        buffer = ctypes.create_unicode_buffer(32768)
        size = ctypes.wintypes.DWORD(len(buffer))
        kernel32.QueryFullProcessImageNameW.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.LPWSTR, ctypes.POINTER(ctypes.wintypes.DWORD)]
        kernel32.QueryFullProcessImageNameW.restype = ctypes.wintypes.BOOL
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return buffer.value
    except Exception:
        return ''
    finally:
        if handle:
            try:
                ctypes.WinDLL('kernel32', use_last_error=True).CloseHandle(handle)
            except Exception:
                pass
    return ''


def _windows_clients():
    clients = []
    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ('dwSize', ctypes.wintypes.DWORD),
            ('cntUsage', ctypes.wintypes.DWORD),
            ('th32ProcessID', ctypes.wintypes.DWORD),
            ('th32DefaultHeapID', ctypes.c_size_t),
            ('th32ModuleID', ctypes.wintypes.DWORD),
            ('cntThreads', ctypes.wintypes.DWORD),
            ('th32ParentProcessID', ctypes.wintypes.DWORD),
            ('pcPriClassBase', ctypes.c_long),
            ('dwFlags', ctypes.wintypes.DWORD),
            ('szExeFile', ctypes.wintypes.WCHAR * 260),
        ]
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = ctypes.wintypes.HANDLE
    kernel32.Process32FirstW.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32FirstW.restype = ctypes.wintypes.BOOL
    kernel32.Process32NextW.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32NextW.restype = ctypes.wintypes.BOOL
    kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    kernel32.CloseHandle.restype = ctypes.wintypes.BOOL
    snapshot = kernel32.CreateToolhelp32Snapshot(2, 0)
    if not snapshot or ctypes.cast(snapshot, ctypes.c_void_p).value == ctypes.c_void_p(-1).value:
        return clients
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(entry)
    try:
        if kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            while True:
                executable = str(entry.szExeFile or '')
                if executable.casefold() == 'robloxplayerbeta.exe':
                    pid = int(entry.th32ProcessID)
                    clients.append({'pid': pid, 'process': executable, 'path': _windows_process_path(pid)})
                if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                    break
    finally:
        kernel32.CloseHandle(snapshot)
    clients.sort(key=lambda item: item['pid'])
    return clients


def _linux_clients():
    clients = []
    try:
        from sober_support import sober_process_pids
        pids = sober_process_pids()
    except Exception:
        pids = []
    for pid in pids:
        try:
            process_root = f'/proc/{int(pid)}'
            with open(f'{process_root}/comm', 'r', encoding='utf-8', errors='replace') as source:
                process = source.read().strip()
            try:
                path = os.readlink(f'{process_root}/exe')
            except OSError:
                path = ''
            clients.append({'pid': int(pid), 'process': process or 'Sober', 'path': path})
        except (OSError, ValueError, PermissionError):
            continue
    if not clients:
        try:
            entries = os.listdir('/proc')
        except OSError:
            entries = []
        for entry in entries:
            if not entry.isdigit():
                continue
            pid = int(entry)
            try:
                with open(f'/proc/{pid}/cmdline', 'rb') as source:
                    command = source.read(65536).replace(b'\0', b' ').decode('utf-8', 'replace').strip()
                with open(f'/proc/{pid}/comm', 'r', encoding='utf-8', errors='replace') as source:
                    process = source.read().strip()
                try:
                    path = os.readlink(f'/proc/{pid}/exe')
                except OSError:
                    path = ''
                if 'robloxplayerbeta' in ' '.join((process, path, command)).casefold():
                    clients.append({'pid': pid, 'process': process or 'RobloxPlayerBeta', 'path': path})
            except (OSError, ValueError, PermissionError):
                continue
    return clients


def list_roblox_clients():
    if os.name == 'nt':
        try:
            return _windows_clients()
        except Exception:
            return []
    if os.path.isdir('/proc'):
        return _linux_clients()
    return []
