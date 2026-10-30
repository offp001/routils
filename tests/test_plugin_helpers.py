import importlib
import importlib.util
import os
import re
import sys
import types
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_FILES = [
    ROOT / "routils_linux/plugins/plugins.py",
    ROOT / "routils_windows/plugins/plugins.py",
]


def load_plugin_mixin(path):
    host = types.ModuleType("main")
    host.os = os
    host.re = re
    host.uuid = uuid
    host.importlib = importlib
    host.UI_TEXT = {
        "b29": "Plugin could not be loaded.",
        "c29": "Plugin must define register().",
    }
    previous = sys.modules.get("main")
    sys.modules["main"] = host
    try:
        spec = importlib.util.spec_from_file_location(
            f"plugin_test_{path.parent.parent.name}",
            path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.PluginsMixin()
    finally:
        if previous is None:
            sys.modules.pop("main", None)
        else:
            sys.modules["main"] = previous


@pytest.fixture(params=PLUGIN_FILES, ids=["linux", "windows"])
def plugin(request, tmp_path):
    instance = load_plugin_mixin(request.param)
    instance.plugins_dir = str(tmp_path)
    return instance


def test_plugin_files_returns_sorted_python_files(plugin, tmp_path):
    (tmp_path / "z_plugin.py").write_text("VALUE = 1", encoding="utf-8")
    (tmp_path / "a_plugin.PY").write_text("VALUE = 2", encoding="utf-8")
    (tmp_path / "guide.txt").write_text("Guide", encoding="utf-8")

    assert [Path(path).name for path in plugin._plugin_files()] == [
        "a_plugin.PY",
        "z_plugin.py",
    ]


def test_plugin_files_returns_empty_for_missing_directory(plugin, tmp_path):
    plugin.plugins_dir = str(tmp_path / "missing")

    assert plugin._plugin_files() == []


def test_plugin_load_python_accepts_valid_plugin(plugin, tmp_path):
    path = tmp_path / "sample_plugin.py"
    path.write_text(
        "PLUGIN_DESCRIPTION = 'Test plugin'\ndef register(app):\n    return None\n",
        encoding="utf-8",
    )

    module = plugin._plugin_load_python(str(path))

    assert module.PLUGIN_DESCRIPTION == "Test plugin"
    assert callable(module.register)


def test_plugin_load_python_rejects_missing_register(plugin, tmp_path):
    path = tmp_path / "invalid_plugin.py"
    path.write_text("VALUE = 42\n", encoding="utf-8")

    with pytest.raises(ValueError, match="register"):
        plugin._plugin_load_python(str(path))
