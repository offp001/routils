import importlib.util
import json
import os
import re
import sys
import threading
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FFLAG_FILES = [
    ROOT / "routils_linux/fflag/fflag.py",
    ROOT / "routils_windows/fflag/fflag.py",
]


def load_fflag_mixin(path, history_path):
    host = types.ModuleType("main")
    host.os = os
    host.re = re
    host.json = json
    host.threading = threading
    host.FFLAG_HISTORY_PATH = str(history_path)
    host.fflag_strip_prefix = lambda name: re.sub(
        r"^(?:DFFlag|FFlag|DFInt|FInt|DFString|FString|DFLog|FLog)",
        "",
        name,
        flags=re.IGNORECASE,
    )
    previous = sys.modules.get("main")
    sys.modules["main"] = host
    try:
        spec = importlib.util.spec_from_file_location(
            f"fflag_test_{path.parent.parent.name}",
            path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.FFlagMixin()
    finally:
        if previous is None:
            sys.modules.pop("main", None)
        else:
            sys.modules["main"] = previous


@pytest.fixture(params=FFLAG_FILES, ids=["linux", "windows"])
def fflag(request, tmp_path):
    return load_fflag_mixin(request.param, tmp_path / "history.json")


def test_conflicts_detected_case_insensitively(fflag):
    fflag.fflag_flags = [
        {"name": "FFlagEnableFeature"},
        {"name": "DFFlagenablefeature"},
        {"name": "DFIntUniqueValue"},
    ]
    assert fflag._fflag_conflicts() == {"enablefeature"}


def test_conflicts_ignore_empty_names(fflag):
    fflag.fflag_flags = [
        {"name": ""},
        {"name": "   "},
        {"name": "FFlagUnique"},
    ]
    assert fflag._fflag_conflicts() == set()


def test_history_snapshot_normalizes_flags(fflag):
    flags = [
        {"name": "FFlagEnableFeature", "value": True, "type": "bool"},
        {"name": "DFIntFrameRate", "value": 240, "type": "int"},
        None,
        {"name": "  FStringMessage  ", "value": None},
    ]

    assert fflag._fflag_history_snapshot_from_flags(flags) == [
        {"name": "EnableFeature", "value": "True", "type": "bool", "index": 0},
        {"name": "FrameRate", "value": "240", "type": "int", "index": 1},
        {"name": "Message", "value": "", "type": "", "index": 3},
    ]


def test_history_snapshot_handles_empty_input(fflag):
    assert fflag._fflag_history_snapshot_from_flags(None) == []
    assert fflag._fflag_history_snapshot_from_flags([]) == []


def test_history_load_reads_valid_records(fflag, tmp_path):
    path = tmp_path / "history.json"
    records = [{"event": f"event-{i}"} for i in range(3)]
    path.write_text(json.dumps(records), encoding="utf-8")

    fflag.FFLAG_HISTORY_PATH = str(path)

    assert fflag._fflag_history_load() == records


def test_history_load_filters_non_dict_records(fflag, tmp_path):
    path = tmp_path / "history.json"
    path.write_text(
        json.dumps([{"event": "valid"}, "invalid", 123, None]),
        encoding="utf-8",
    )

    fflag.FFLAG_HISTORY_PATH = str(path)

    assert fflag._fflag_history_load() == [{"event": "valid"}]


def test_history_load_limits_records_to_500(fflag, tmp_path):
    path = tmp_path / "history.json"
    records = [{"event": f"event-{i}"} for i in range(600)]
    path.write_text(json.dumps(records), encoding="utf-8")

    fflag.FFLAG_HISTORY_PATH = str(path)

    result = fflag._fflag_history_load()

    assert len(result) == 500
    assert result[0]["event"] == "event-100"
    assert result[-1]["event"] == "event-599"


def test_history_load_handles_invalid_json(fflag, tmp_path):
    path = tmp_path / "history.json"
    path.write_text("{invalid json", encoding="utf-8")

    fflag.FFLAG_HISTORY_PATH = str(path)

    assert fflag._fflag_history_load() == []


def test_history_load_handles_missing_file(fflag, tmp_path):
    fflag.FFLAG_HISTORY_PATH = str(tmp_path / "missing.json")

    assert fflag._fflag_history_load() == []
