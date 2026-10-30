import importlib.util
import json
import os
import sys
import types
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SETTINGS_FILES = [
    ROOT / "routils_linux/settings/settings.py",
    ROOT / "routils_windows/settings/settings.py",
]


def load_settings_mixin(path):
    host = types.ModuleType("main")
    host.os = os
    host.sys = sys
    host.json = json
    host.zipfile = zipfile
    host.UI_TEXT = {
        "c19": "Import RoUtils Config",
        "w18": "RoUtils Config",
        "x18": "ZIP archive",
        "y18": "JSON settings",
        "z7": "All files",
        "h32": "Settings file must contain a JSON object.",
        "p18": "Config Backup",
        "f19": "Could not import config: {p0}",
        "e19": "Config imported successfully.",
        "d19": "Imported RoUtils config from {p0}",
    }
    previous = sys.modules.get("main")
    sys.modules["main"] = host
    try:
        spec = importlib.util.spec_from_file_location(
            f"settings_test_{path.parent.parent.name}",
            path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.SettingsMixin(), module
    finally:
        if previous is None:
            sys.modules.pop("main", None)
        else:
            sys.modules["main"] = previous


class Variable:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class Dialogs:
    def __init__(self, path):
        self.path = str(path)

    def askopenfilename(self, **kwargs):
        return self.path


class Messages:
    def __init__(self):
        self.errors = []
        self.infos = []

    def showerror(self, *args, **kwargs):
        self.errors.append(args)

    def showinfo(self, *args, **kwargs):
        self.infos.append(args)


@pytest.fixture(params=SETTINGS_FILES, ids=["linux", "windows"])
def context(request, tmp_path):
    instance, module = load_settings_mixin(request.param)
    messages = Messages()
    module.filedialog = Dialogs(tmp_path / "settings.json")
    module.messagebox = messages
    module.DATA_DIR = str(tmp_path / "data")
    instance.settings = {}
    instance.fps_limit = Variable(0)
    instance._save_settings = lambda: None
    instance._load_fflag_flags = lambda: None
    instance._console_log = lambda *_: None
    return instance, module, messages, tmp_path


def test_import_settings_from_json(context):
    instance, module, messages, tmp_path = context
    source = tmp_path / "settings.json"
    source.write_text(
        json.dumps({"theme": "Ocean", "fps_limit": 60}),
        encoding="utf-8",
    )
    module.filedialog.path = str(source)

    instance._import_settings()

    assert instance.settings["theme"] == "Ocean"
    assert instance.settings["fps_limit"] == 60
    assert not messages.errors
    assert messages.infos


def test_import_settings_rejects_non_object_json(context):
    instance, module, messages, tmp_path = context
    source = tmp_path / "settings.json"
    source.write_text(json.dumps(["invalid"]), encoding="utf-8")
    module.filedialog.path = str(source)

    instance._import_settings()

    assert not instance.settings
    assert messages.errors


def test_import_settings_rejects_archive_without_settings(context):
    instance, module, messages, tmp_path = context
    source = tmp_path / "invalid.rconfig"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("readme.txt", "No settings")
    module.filedialog.path = str(source)

    instance._import_settings()

    assert not instance.settings
    assert messages.errors
