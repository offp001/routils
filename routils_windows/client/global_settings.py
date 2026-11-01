import hashlib
import os
import re
import shutil
import stat
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def default_global_settings_path(platform=None, local_app_data=None, home=None):
    platform = str(platform or os.name).lower()
    if platform not in {"nt", "win32", "windows"}:
        raise OSError("The Windows version only supports the Roblox Global Settings path.")
    home_path = Path(home).expanduser() if home is not None else Path.home()
    local_path = Path(local_app_data).expanduser() if local_app_data else home_path / "AppData" / "Local"
    return local_path / "Roblox" / "GlobalBasicSettings_13.xml"


def _xml_parser():
    return ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))


def _leaf_rows(root):
    rows = []

    def visit(node, path):
        element_children = []
        for index, child in enumerate(list(node)):
            if isinstance(child.tag, str):
                element_children.append((index, child))
                visit(child, path + (index,))
        if isinstance(node.tag, str) and "name" in node.attrib and not element_children:
            rows.append({
                "path": path,
                "name": str(node.attrib.get("name", "")),
                "type": str(node.tag),
                "value": node.text or "",
            })

    visit(root, ())
    return rows


def read_global_settings(path):
    target = Path(path).expanduser()
    raw = target.read_bytes()
    root = ET.fromstring(raw, parser=_xml_parser())
    return _leaf_rows(root), hashlib.sha256(raw).hexdigest()


def _validate_value(kind, value):
    normalized = str(kind).casefold()
    text = str(value)
    if normalized == "bool" and text.strip().casefold() not in {"true", "false"}:
        raise ValueError("Boolean values must be true or false.")
    if normalized in {"int", "token"}:
        try:
            int(text.strip(), 10)
        except ValueError as error:
            raise ValueError("This setting requires a whole number.") from error
    if normalized in {"float", "double"}:
        try:
            float(text.strip())
        except ValueError as error:
            raise ValueError("This setting requires a numeric value.") from error


def save_global_settings(path, updates, expected_digest=None):
    target = Path(path).expanduser()
    raw = target.read_bytes()
    current_digest = hashlib.sha256(raw).hexdigest()
    if expected_digest and current_digest != expected_digest:
        raise RuntimeError("The settings file changed after it was loaded. Refresh it before saving.")
    if re.search(rb"<!DOCTYPE", raw, re.IGNORECASE):
        raise ValueError("This XML file contains a document type declaration and cannot be safely rewritten.")
    root = ET.fromstring(raw, parser=_xml_parser())
    for node_path, value in updates.items():
        node = root
        for index in tuple(node_path):
            node = node[index]
        if not isinstance(node.tag, str) or any(isinstance(child.tag, str) for child in list(node)):
            raise ValueError("A setting entry is no longer a simple value. Refresh the list and try again.")
        _validate_value(node.tag, value)
        node.text = str(value)
    declaration = raw.lstrip().startswith(b"<?xml")
    match = re.search(rb"encoding\s*=\s*['\"]([^'\"]+)['\"]", raw[:512], re.IGNORECASE)
    encoding = match.group(1).decode("ascii", errors="strict") if match else "utf-8"
    mode = stat.S_IMODE(target.stat().st_mode)
    backup = target.with_name(target.name + ".routils-backup")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(descriptor, "wb") as stream:
            ET.ElementTree(root).write(stream, encoding=encoding, xml_declaration=declaration, short_empty_elements=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        if not backup.exists():
            shutil.copy2(target, backup)
        os.replace(temporary, target)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
    updated = target.read_bytes()
    return backup, hashlib.sha256(updated).hexdigest()
