import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

SOBER_APP_ID = "org.vinegarhq.Sober"
SOBER_LEGACY_APP_IDS = (SOBER_APP_ID, "net.sober.Sober")
_SOBER_LOCK = threading.RLock()
_FFLAG_PREFIXES = (
    "DFDouble", "DFFloat", "DFInt", "DFString", "DFFlag", "DFLog",
    "FDouble", "FFloat", "FInt", "FString", "FFlag", "FLog",
    "SFDouble", "SFFloat", "SFFlag", "SFInt", "SFString", "SFLog"
)


def _home():
    return Path.home()


def _normalise_app_root(path):
    path = Path(path).expanduser()
    if path.name == "appData" and path.parent.name == "sober" and path.parent.parent.name == "data":
        return path.parent.parent.parent
    if path.name == "sober" and path.parent.name in {"data", "config", "cache"}:
        return path.parent.parent
    if path.name in {"data", "config", "cache"} and path.parent.name in SOBER_LEGACY_APP_IDS:
        return path.parent
    return path


def _app_roots():
    explicit = os.environ.get("SOBER_APP_ROOT", "").strip()
    roots = [_normalise_app_root(explicit)] if explicit else [_home() / ".var" / "app" / app_id for app_id in SOBER_LEGACY_APP_IDS]
    result = []
    seen = set()
    for root in roots:
        value = str(root.resolve(strict=False))
        if value not in seen:
            seen.add(value)
            result.append(Path(value))
    return result


def _data_root_from_path(path):
    path = Path(path).expanduser()
    if path.name == "appData" and path.parent.name == "sober":
        return path.parent
    if path.name == "sober" and path.parent.name == "data":
        return path
    if path.name == "data":
        return path / "sober"
    if path.name in SOBER_LEGACY_APP_IDS:
        return path / "data" / "sober"
    if (path / "appData").is_dir() or (path / "rbx-storage.db").is_file():
        return path
    return path / "data" / "sober"


def sober_data_root():
    explicit = os.environ.get("SOBER_DATA_DIR", "").strip()
    if explicit:
        return _data_root_from_path(Path(explicit))
    roots = _app_roots()
    for root in roots:
        candidate = root / "data" / "sober"
        if candidate.exists():
            return candidate
    return roots[0] / "data" / "sober"


def sober_appdata_root():
    return sober_data_root() / "appData"


def sober_config_path():
    explicit = os.environ.get("SOBER_CONFIG_PATH", "").strip()
    if explicit:
        return Path(explicit).expanduser()
    roots = _app_roots()
    for root in roots:
        candidate = root / "config" / "sober" / "config.json"
        if candidate.is_file():
            return candidate
    for root in roots:
        if (root / "data" / "sober").exists() or (root / "config" / "sober").exists():
            return root / "config" / "sober" / "config.json"
    data_root = sober_data_root()
    if data_root.parent.name == "data":
        return data_root.parent.parent / "config" / "sober" / "config.json"
    return roots[0] / "config" / "sober" / "config.json"


def _root_from_data_root(data_root):
    data_root = Path(data_root)
    if data_root.name == "sober" and data_root.parent.name == "data":
        return data_root.parent.parent
    return None


def sober_cache_root():
    explicit = os.environ.get("SOBER_CACHE_DIR", "").strip()
    if explicit:
        path = Path(explicit).expanduser()
        if path.name == "rbx-storage":
            return path.parent
        if path.name == "sober":
            return path
        return path / "sober"
    roots = _app_roots()
    data_root = sober_data_root()
    derived = _root_from_data_root(data_root)
    if derived is not None and derived not in roots:
        roots.insert(0, derived)
    for root in roots:
        candidate = root / "cache" / "sober"
        if candidate.is_dir():
            return candidate
    return roots[0] / "cache" / "sober"


def resolve_storage_selection(saved_db, saved_shards, default_db, default_shards):
    saved_db = str(saved_db or "")
    saved_shards = str(saved_shards or "")
    default_db = str(default_db or "")
    default_shards = str(default_shards or "")
    if default_db and os.path.isfile(default_db):
        return default_db, default_shards
    if saved_db and os.path.isfile(saved_db):
        shard_root = saved_shards if saved_shards and os.path.isdir(saved_shards) else default_shards
        return saved_db, shard_root
    shard_root = saved_shards if saved_shards and os.path.isdir(saved_shards) else default_shards
    return saved_db or default_db, shard_root


def sober_storage_paths():
    db_override = os.environ.get("SOBER_STORAGE_DB_PATH", "").strip()
    shard_override = os.environ.get("SOBER_SHARD_ROOT", "").strip()
    data_root = sober_data_root()
    roots = _app_roots()
    derived = _root_from_data_root(data_root)
    if derived is not None and derived not in roots:
        roots.insert(0, derived)
    db_candidates = []
    shard_candidates = []
    if db_override:
        db_candidates.append(Path(db_override).expanduser())
    if shard_override:
        shard_candidates.append(Path(shard_override).expanduser())
    db_candidates.extend((data_root / "appData" / "rbx-storage.db", data_root / "rbx-storage.db"))
    shard_candidates.append(sober_cache_root() / "rbx-storage")
    for root in roots:
        root_data = root / "data" / "sober"
        db_candidates.extend((root_data / "appData" / "rbx-storage.db", root_data / "rbx-storage.db"))
        shard_candidates.extend((root / "cache" / "sober" / "rbx-storage", root_data / "appData" / "rbx-storage", root_data / "rbx-storage"))
    unique_db = []
    unique_shards = []
    seen = set()
    for path in db_candidates:
        key = str(path.resolve(strict=False))
        if key not in seen:
            seen.add(key)
            unique_db.append(path)
    seen = set()
    for path in shard_candidates:
        key = str(path.resolve(strict=False))
        if key not in seen:
            seen.add(key)
            unique_shards.append(path)
    db_path = next((path for path in unique_db if path.is_file()), unique_db[0])
    shard_root = next((path for path in unique_shards if path.is_dir()), unique_shards[0])
    return str(db_path), str(shard_root)


def sober_logs_dir():
    data = sober_data_root()
    candidates = (data / "sober_logs", data / "logs", data / "appData" / "logs", data / "appData")
    for candidate in candidates:
        if candidate.is_dir() and any(candidate.glob("*.log")):
            return str(candidate)
    return str(candidates[0])


def _linux_process_details(pid):
    proc = Path("/proc") / str(int(pid))
    try:
        name = (proc / "comm").read_text(encoding="utf-8", errors="replace").strip().lower()
    except OSError:
        name = ""
    try:
        command = (proc / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace").strip().lower()
    except OSError:
        command = ""
    try:
        cgroup = (proc / "cgroup").read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        cgroup = ""
    try:
        executable = str((proc / "exe").resolve(strict=False))
    except OSError:
        executable = ""
    return name, command, cgroup, executable


def is_sober_process(pid):
    try:
        pid = int(pid)
        if pid <= 0:
            return False
    except (TypeError, ValueError):
        return False
    name, command, cgroup, executable = _linux_process_details(pid)
    marker = any(app_id.lower() in cgroup for app_id in SOBER_LEGACY_APP_IDS)
    marker = marker or "org.vinegarhq.sober" in command or "net.sober.sober" in command
    if marker:
        return True
    if name in {"sober", "sober-wrapper"}:
        return True
    return "com.roblox.client" in command and ("flatpak" in command or "sober" in executable or "sober" in cgroup)


def _flatpak_sober_instances():
    flatpak = shutil.which("flatpak")
    if not flatpak or os.name == "nt":
        return False, []
    try:
        result = subprocess.run([flatpak, "ps", "--columns=application,pid"], capture_output=True, text=True, timeout=4)
        if result.returncode != 0:
            return False, []
        found = False
        pids = []
        for line in result.stdout.splitlines():
            parts = line.strip().split()
            if not any(part in SOBER_LEGACY_APP_IDS for part in parts):
                continue
            found = True
            for part in parts:
                if part.isdigit() and int(part) > 0:
                    pids.append(int(part))
        return found, list(dict.fromkeys(pids))
    except (OSError, subprocess.SubprocessError):
        return False, []


def sober_process_pids():
    if os.name == "nt":
        return []
    candidates = []
    fallbacks = []
    try:
        with os.scandir("/proc") as entries:
            for entry in entries:
                if not entry.name.isdigit():
                    continue
                pid = int(entry.name)
                name, command, cgroup, executable = _linux_process_details(pid)
                marker = any(app_id.lower() in cgroup for app_id in SOBER_LEGACY_APP_IDS)
                if marker:
                    score = 0 if name == "main" else 1 if "com.roblox.client" in command else 2 if name in {"sober", "sober-wrapper"} else 3
                    candidates.append((score, pid))
                elif name in {"sober", "sober-wrapper"} or "org.vinegarhq.sober" in command or "net.sober.sober" in command:
                    fallbacks.append(pid)
                elif "com.roblox.client" in command and ("sober" in executable or "sober" in cgroup):
                    fallbacks.append(pid)
    except OSError:
        pass
    selected = [pid for _, pid in sorted(candidates)]
    selected.extend(pid for pid in fallbacks if pid not in selected)
    if not selected:
        _running, flatpak_pids = _flatpak_sober_instances()
        selected.extend(pid for pid in flatpak_pids if pid not in selected)
    return selected


def sober_process_pid():
    pids = sober_process_pids()
    return int(pids[0]) if pids else 0


def sober_flatpak_running():
    if os.name == "nt":
        return bool(sober_process_pids())
    found, pids = _flatpak_sober_instances()
    return found or bool(pids) or bool(sober_process_pids())


def _focused_window_pid():
    if os.environ.get("DISPLAY") and shutil.which("xdotool"):
        try:
            result = subprocess.run([shutil.which("xdotool"), "getwindowfocus", "getwindowpid"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return int(result.stdout.strip().splitlines()[-1])
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
    if shutil.which("hyprctl"):
        try:
            result = subprocess.run([shutil.which("hyprctl"), "activewindow", "-j"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                value = json.loads(result.stdout or "{}")
                pid = int(value.get("pid") or 0)
                if pid:
                    return pid
        except (OSError, ValueError, TypeError, subprocess.SubprocessError):
            pass
    if shutil.which("swaymsg"):
        try:
            result = subprocess.run([shutil.which("swaymsg"), "-t", "get_tree", "-r"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                tree = json.loads(result.stdout or "{}")
                stack = [tree]
                while stack:
                    node = stack.pop()
                    if node.get("focused") and node.get("pid"):
                        return int(node["pid"])
                    stack.extend(node.get("nodes") or [])
                    stack.extend(node.get("floating_nodes") or [])
        except (OSError, ValueError, TypeError, subprocess.SubprocessError):
            pass
    return 0


def sober_is_focused(expected_pid=0):
    focused_pid = _focused_window_pid()
    if not focused_pid:
        return False
    if is_sober_process(focused_pid):
        return True
    if expected_pid and focused_pid == int(expected_pid):
        return True
    current = focused_pid
    for _ in range(10):
        try:
            status = (Path("/proc") / str(current) / "status").read_text(encoding="utf-8", errors="replace")
            parent_line = next((line for line in status.splitlines() if line.startswith("PPid:")), "")
            parent = int(parent_line.split(":", 1)[1].strip()) if parent_line else 0
        except (OSError, ValueError):
            return False
        if parent <= 1 or parent == current:
            return False
        if expected_pid and parent == int(expected_pid):
            return True
        if is_sober_process(parent):
            return True
        current = parent
    return False


def type_sober_emote(dance, expected_pid=0):
    command_name = str(dance or "").strip()
    if command_name.lower().startswith("/e "):
        command_name = command_name[3:].strip()
    command_name = command_name.strip(" \"'")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", command_name):
        return False, "Emote names may contain only English letters, numbers, underscores, or hyphens."
    if not sober_process_pid():
        return False, "Sober client was not found."
    if not sober_is_focused(expected_pid):
        return False, "The Sober window is not focused; the command was not sent."
    text = f"//e {command_name}"
    if os.environ.get("WAYLAND_DISPLAY"):
        wtype = shutil.which("wtype")
        if not wtype:
            return False, "wtype is not installed for Wayland."
        try:
            typed = subprocess.run([wtype, "-d", "5", "--", text], capture_output=True, text=True, timeout=5)
            if typed.returncode != 0:
                return False, (typed.stderr or typed.stdout or "wtype could not type the text.").strip()
            returned = subprocess.run([wtype, "-k", "Return"], capture_output=True, text=True, timeout=3)
            if returned.returncode != 0:
                return False, (returned.stderr or returned.stdout or "Could not send the Enter key.").strip()
            return True, f"Command {command_name} was sent to Sober."
        except (OSError, subprocess.SubprocessError) as error:
            return False, str(error)
    xdotool = shutil.which("xdotool")
    if not xdotool:
        return False, "xdotool is not installed for X11."
    try:
        typed = subprocess.run([xdotool, "type", "--clearmodifiers", "--delay", "5", text], capture_output=True, text=True, timeout=5)
        if typed.returncode != 0:
            return False, (typed.stderr or typed.stdout or "xdotool could not type the text.").strip()
        returned = subprocess.run([xdotool, "key", "Return"], capture_output=True, text=True, timeout=3)
        if returned.returncode != 0:
            return False, (returned.stderr or returned.stdout or "Could not send the Enter key.").strip()
        return True, f"Command {command_name} was sent to Sober."
    except (OSError, subprocess.SubprocessError) as error:
        return False, str(error)

def _prefix_from_name(name):
    name = str(name or "").strip()
    for prefix in _FFLAG_PREFIXES:
        if name.startswith(prefix) and len(name) > len(prefix):
            return prefix
    return ""


def _infer_value_type(value, declared=None):
    declared = str(declared or "").strip().lower()
    if declared in {"bool", "boolean"}:
        return "bool"
    if declared in {"int", "integer"}:
        return "int"
    if declared in {"float", "double", "number"}:
        return "float"
    if declared in {"string", "str"}:
        return "string"
    text = str(value).strip().lower()
    if text in {"true", "false"}:
        return "bool"
    try:
        int(text, 10)
        return "int"
    except (TypeError, ValueError):
        try:
            float(text)
            return "float"
        except (TypeError, ValueError):
            return "string"


def _flag_config_value(flag):
    value = flag.get("value", "")
    raw_name = str(flag.get("name", "")).strip()
    prefix = _prefix_from_name(raw_name) or str(flag.get("prefix", "")).strip()
    prefix_types = {
        "DFDouble": "float", "DFFloat": "float", "FDouble": "float", "FFloat": "float", "SFDouble": "float", "SFFloat": "float",
        "DFInt": "int", "FInt": "int", "SFInt": "int", "DFLog": "int", "FLog": "int", "SFLog": "int",
        "DFFlag": "bool", "FFlag": "bool", "SFFlag": "bool",
        "DFString": "string", "FString": "string", "SFString": "string",
    }
    value_type = prefix_types.get(prefix, _infer_value_type(value, flag.get("type")))
    if value_type == "bool":
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text not in {"true", "false", "1", "0"}:
            raise ValueError(f"Invalid boolean value for {flag.get('name', '')}")
        return text in {"true", "1"}
    if value_type == "int":
        return int(str(value).strip(), 10)
    if value_type == "float":
        number = float(str(value).strip())
        if not math.isfinite(number):
            raise ValueError(f"Invalid numeric value for {flag.get('name', '')}")
        return number
    return str(value)


def _flag_config_name(flag):
    raw_name = str(flag.get("name", "")).strip()
    prefix = _prefix_from_name(raw_name) or str(flag.get("prefix", "")).strip()
    if prefix and prefix not in _FFLAG_PREFIXES:
        prefix = ""
    bare = raw_name[len(prefix):] if prefix and raw_name.startswith(prefix) else raw_name
    if not prefix:
        value_type = _infer_value_type(flag.get("value", ""), flag.get("type"))
        prefix = {"bool": "DFFlag", "int": "DFInt", "float": "DFFloat", "string": "DFString"}[value_type]
    if not bare or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", bare):
        raise ValueError(f"Invalid FFlag name: {raw_name}")
    return prefix + bare


def _strip_json_comments(source):
    output = []
    index = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            index += 2
            while index < len(source) and source[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and next_char == "*":
            index += 2
            while index < len(source) and not (source[index] == "*" and index + 1 < len(source) and source[index + 1] == "/"):
                if source[index] in "\r\n":
                    output.append(source[index])
                index += 1
            index = min(len(source), index + 2)
            continue
        output.append(char)
        index += 1
    return "".join(output)


def _remove_trailing_commas(source):
    output = []
    index = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == ",":
            lookahead = index + 1
            while lookahead < len(source) and source[lookahead].isspace():
                lookahead += 1
            if lookahead < len(source) and source[lookahead] in "]}":
                index += 1
                continue
        output.append(char)
        index += 1
    return "".join(output)


def _jsonc_loads(source):
    text = _remove_trailing_commas(_strip_json_comments(source))
    value = json.loads(text)
    return value


def _leading_json_comments(source):
    lines = source.splitlines(keepends=True)
    output = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        if in_block:
            output.append(line)
            if "*/" in line:
                in_block = False
            continue
        if not stripped:
            if output:
                output.append(line)
                continue
            continue
        if stripped.startswith("//"):
            output.append(line)
            continue
        if stripped.startswith("/*"):
            output.append(line)
            in_block = "*/" not in stripped
            continue
        break
    return "".join(output)


def _read_json_object(path):
    try:
        source = path.read_text(encoding="utf-8")
        value = _jsonc_loads(source)
        if not isinstance(value, dict):
            raise ValueError(f"Expected a JSON object in {path}")
        return value
    except FileNotFoundError:
        return {}


def _write_json_atomic(path, value, prefix=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            if prefix:
                stream.write(prefix)
                if not prefix.endswith("\n"):
                    stream.write("\n")
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def _write_sober_config_atomic(path, value, prefix=""):
    _write_json_atomic(path, value, prefix=prefix)


def apply_sober_fflags(flags, data_dir):
    config_path = sober_config_path()
    state_path = Path(data_dir) / "sober_fflags_state.json"
    with _SOBER_LOCK:
        config_existed = config_path.is_file()
        raw_config = config_path.read_text(encoding="utf-8") if config_existed else ""
        prefix = _leading_json_comments(raw_config)
        original_config = _jsonc_loads(raw_config) if raw_config.strip() else {}
        if not isinstance(original_config, dict):
            raise ValueError(f"Sober config is not a JSON object: {config_path}")
        config = dict(original_config)
        previous_fflags_value = config.get("fflags")
        previous_fflags = dict(previous_fflags_value) if isinstance(previous_fflags_value, dict) else {}
        state = _read_json_object(state_path)
        if not state.get("active") or state.get("config_path") != str(config_path):
            state = {
                "active": True,
                "config_path": str(config_path),
                "config_existed": config_existed,
                "fflags_existed": isinstance(previous_fflags_value, dict),
                "original_fflags": previous_fflags,
                "saved_at": time.time(),
            }
            _write_json_atomic(state_path, state)
        merged = dict(previous_fflags)
        applied = 0
        skipped = []
        for item in flags:
            if not isinstance(item, dict):
                continue
            try:
                key = _flag_config_name(item)
                merged[key] = _flag_config_value(item)
                applied += 1
            except (TypeError, ValueError) as error:
                skipped.append(str(error))
        config["fflags"] = merged
        backup_path = config_path.with_name("config.json.routils-backup")
        if config_existed and not backup_path.exists():
            shutil.copy2(config_path, backup_path)
        if config != original_config:
            _write_sober_config_atomic(config_path, config, prefix=prefix)
        return {"path": str(config_path), "applied": applied, "total": len(flags), "skipped": skipped}


def restore_sober_fflags(data_dir):
    state_path = Path(data_dir) / "sober_fflags_state.json"
    with _SOBER_LOCK:
        state = _read_json_object(state_path)
        if not state.get("active"):
            raise FileNotFoundError("No RoUtils Sober FFlag backup is available.")
        config_path = Path(str(state.get("config_path", sober_config_path()))).expanduser()
        raw_config = config_path.read_text(encoding="utf-8") if config_path.is_file() else ""
        prefix = _leading_json_comments(raw_config)
        config = _jsonc_loads(raw_config) if raw_config.strip() else {}
        if not isinstance(config, dict):
            raise ValueError(f"Sober config is not a JSON object: {config_path}")
        if state.get("fflags_existed"):
            config["fflags"] = state.get("original_fflags", {})
        else:
            config.pop("fflags", None)
        if config:
            _write_sober_config_atomic(config_path, config, prefix=prefix)
        else:
            try:
                config_path.unlink()
            except FileNotFoundError:
                pass
        try:
            state_path.unlink()
        except OSError:
            pass
        return str(config_path)


def set_sober_fps_cap(fps):
    value = max(0, min(1000, int(fps)))
    roots = [sober_appdata_root()]
    roots.extend(root / "data" / "sober" for root in _app_roots())
    paths = []
    for root in roots:
        candidate = root / "GlobalBasicSettings_13.xml"
        if candidate not in paths:
            paths.append(candidate)
    target = next((path for path in paths if path.is_file()), None)
    if target is None:
        raise FileNotFoundError("GlobalBasicSettings_13.xml was not found. Launch Sober once, close it, then apply the FPS setting.")
    with _SOBER_LOCK:
        text = target.read_text(encoding="utf-8", errors="replace")
        replacement = f'<int name="FramerateCap">{value}</int>'
        pattern = r'<int\s+name=["\']FramerateCap["\']\s*>.*?</int>'
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            updated = re.sub(pattern, replacement, text, count=1, flags=re.IGNORECASE | re.DOTALL)
        else:
            marker = "</roblox>"
            updated = text.replace(marker, f"  {replacement}\n{marker}", 1) if marker in text else f"{text}\n{replacement}\n"
        if updated != text:
            backup = target.with_suffix(target.suffix + ".routils-backup")
            if not backup.exists():
                shutil.copy2(target, backup)
            _write_text_atomic(target, updated)
    return str(target), value


def _write_text_atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def open_path(target):
    value = str(target)
    if os.name == "nt":
        os.startfile(value)
        return
    opener = shutil.which("xdg-open")
    if opener:
        subprocess.Popen([opener, value], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        return
    if value.startswith(("http://", "https://")):
        import webbrowser
        webbrowser.open(value)
        return
    raise FileNotFoundError("xdg-open was not found on this Linux system.")
