import json
from pathlib import Path


def _stringify(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def merge_setting_list(items, flags):
    if not isinstance(items, list):
        return items, 0
    normalized = {}
    indexes = {}
    for index, item in enumerate(items):
        if isinstance(item, dict) and item.get("name") is not None:
            name = str(item.get("name", "")).casefold()
            if name:
                normalized[name] = index
                indexes[index] = name
    changed = 0
    for name, value in flags.items():
        key = str(name).strip()
        if not key:
            continue
        lowered = key.casefold()
        text = _stringify(value)
        if lowered in normalized:
            index = normalized[lowered]
            item = dict(items[index])
            if _stringify(item.get("value")) != text:
                item["value"] = text
                items[index] = item
                changed += 1
        else:
            items.append({"name": key, "value": text})
            normalized[lowered] = len(items) - 1
            changed += 1
    return items, changed


def merge_clientsettings_payload(payload, flags):
    if not isinstance(flags, dict) or not flags:
        return payload, 0
    if isinstance(payload, list):
        if all(isinstance(item, dict) for item in payload):
            merged, count = merge_setting_list(payload, flags)
            return merged, count
        return payload, 0
    if not isinstance(payload, dict):
        return payload, 0
    for key in ("applicationSettings", "settings", "settingsList", "data", "values"):
        value = payload.get(key)
        if isinstance(value, list) and (not value or any(isinstance(item, dict) and "name" in item for item in value)):
            copied = dict(payload)
            merged, count = merge_setting_list(list(value), flags)
            copied[key] = merged
            return copied, count
    if payload and all(not isinstance(value, (dict, list)) for value in payload.values()) and all(str(key).startswith(("DFFlag", "DFInt", "DFString", "DFFloat", "DFDouble", "DFLog", "FFlag", "FInt", "FString", "FFloat", "FDouble", "FLog", "SFFlag", "SFInt", "SFString", "SFFloat", "SFDouble", "SFLog")) for key in payload):
        copied = dict(payload)
        count = 0
        normalized = {str(key).casefold(): key for key in copied}
        for name, value in flags.items():
            key = normalized.get(str(name).casefold(), str(name))
            current = copied.get(key)
            if key in copied and _stringify(current) == _stringify(value):
                continue
            if key in copied and isinstance(current, str):
                if isinstance(value, bool):
                    value = "true" if value else "false"
                elif isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                elif value is not None:
                    value = str(value)
            copied[key] = value
            normalized[str(key).casefold()] = key
            count += 1
        return copied, count
    prefixes = (
        "DFFlag", "DFInt", "DFString", "DFFloat", "DFDouble", "DFLog",
        "FFlag", "FInt", "FString", "FFloat", "FDouble", "FLog",
        "SFFlag", "SFInt", "SFString", "SFFloat", "SFDouble", "SFLog",
    )
    flag_keys = {str(key).casefold(): key for key in payload if str(key).startswith(prefixes)}
    if flag_keys:
        copied = dict(payload)
        count = 0
        for name, value in flags.items():
            key = flag_keys.get(str(name).casefold(), str(name))
            current = copied.get(key)
            if key in copied and _stringify(current) == _stringify(value):
                continue
            if key in copied and isinstance(current, str):
                if isinstance(value, bool):
                    value = "true" if value else "false"
                elif value is not None:
                    value = _stringify(value)
            copied[key] = value
            flag_keys[str(key).casefold()] = key
            count += 1
        return copied, count
    for key, value in payload.items():
        if isinstance(value, dict):
            merged, count = merge_clientsettings_payload(value, flags)
            if count:
                copied = dict(payload)
                copied[key] = merged
                return copied, count
    return payload, 0


def load_routils_flags(flags_path):
    path = Path(flags_path).expanduser()
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(parsed, list):
        return {}
    try:
        from sober_support import _flag_config_name, _flag_config_value
    except ImportError:
        return {}
    result = {}
    for item in parsed:
        if not isinstance(item, dict):
            continue
        try:
            result[_flag_config_name(item)] = _flag_config_value(item)
        except (TypeError, ValueError):
            continue
    return result


def load_sober_flags(config_path):
    path = Path(config_path).expanduser()
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    parsed = _jsonc_loads(source)
    if not isinstance(parsed, dict):
        return {}
    flags = parsed.get("fflags", {})
    return dict(flags) if isinstance(flags, dict) else {}


def _jsonc_loads(source):
    output = []
    in_string = False
    escaped = False
    index = 0
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
    text = "".join(output)
    output = []
    in_string = False
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
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
            while lookahead < len(text) and text[lookahead].isspace():
                lookahead += 1
            if lookahead < len(text) and text[lookahead] in "]}":
                index += 1
                continue
        output.append(char)
        index += 1
    return json.loads("".join(output))
