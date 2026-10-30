import importlib.util
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import types
import zipfile
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CACHE_FILES = [
    ROOT / "routils_linux/cache/cache.py",
    ROOT / "routils_windows/cache/cache.py",
]


def load_cache_mixin(path):
    host = types.ModuleType("main")
    host.os = os
    host.re = re
    host.sqlite3 = sqlite3
    host.shutil = shutil
    host.tempfile = tempfile
    host.zipfile = zipfile
    host.json = json
    host.datetime = datetime
    previous = sys.modules.get("main")
    sys.modules["main"] = host
    try:
        spec = importlib.util.spec_from_file_location(
            f"cache_test_{path.parent.parent.name}",
            path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.CacheMixin()
    finally:
        if previous is None:
            sys.modules.pop("main", None)
        else:
            sys.modules["main"] = previous


@pytest.fixture(params=CACHE_FILES, ids=["linux", "windows"])
def cache(request):
    return load_cache_mixin(request.param)


def test_safe_name_replaces_invalid_characters(cache):
    assert cache._cc_safe_name('Test<>:"/\\|?*') == "Test_________"


def test_safe_name_removes_surrounding_spaces_and_dots(cache):
    assert cache._cc_safe_name("  Config...  ") == "Config"


def test_safe_name_uses_default_for_empty_name(cache):
    assert cache._cc_safe_name(" ... ") == "Config"


def test_unique_path_returns_original_when_available(cache, tmp_path):
    assert cache._cc_unique_path(str(tmp_path), "config.ccdb") == str(
        tmp_path / "config.ccdb"
    )


def test_unique_path_adds_incrementing_suffix(cache, tmp_path):
    (tmp_path / "config.ccdb").touch()
    (tmp_path / "config (1).ccdb").touch()
    assert cache._cc_unique_path(str(tmp_path), "config.ccdb") == str(
        tmp_path / "config (2).ccdb"
    )


def test_snapshot_database_copies_sqlite_data(cache, tmp_path):
    source = tmp_path / "source.db"
    destination = tmp_path / "nested" / "snapshot.db"

    with sqlite3.connect(source) as connection:
        connection.execute("CREATE TABLE test (value TEXT)")
        connection.execute("INSERT INTO test VALUES (?)", ("RoUtils",))

    cache._cc_snapshot_database(str(source), str(destination))

    with sqlite3.connect(destination) as connection:
        result = connection.execute("SELECT value FROM test").fetchone()

    assert result == ("RoUtils",)


def test_snapshot_database_rejects_missing_source(cache, tmp_path):
    with pytest.raises(FileNotFoundError):
        cache._cc_snapshot_database(
            str(tmp_path / "missing.db"),
            str(tmp_path / "snapshot.db"),
        )


def test_read_package_info_reads_valid_package(cache, tmp_path):
    package = tmp_path / "config.ccdb"
    metadata = {
        "format": "RoUtils CConfigs",
        "version": 1,
        "name": "Test Config",
        "created_at": "2026-10-30T12:00:00",
        "applied_caches": [],
    }

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("config.json", json.dumps(metadata))
        archive.writestr("rbx-storage.db", b"database")

    result = cache._cc_read_package_info(str(package))

    assert result["name"] == "Test Config"
    assert result["version"] == 1
    assert result["raw_db"] is False


def test_read_package_info_rejects_package_without_metadata(cache, tmp_path):
    package = tmp_path / "invalid.ccdb"

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("rbx-storage.db", b"database")

    with pytest.raises(ValueError, match="not a valid CConfigs"):
        cache._cc_read_package_info(str(package))


def test_read_package_info_rejects_package_without_database(cache, tmp_path):
    package = tmp_path / "invalid.ccdb"

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("config.json", json.dumps({"name": "Test"}))

    with pytest.raises(ValueError, match="missing rbx-storage.db"):
        cache._cc_read_package_info(str(package))


def test_read_package_info_reads_raw_database(cache, tmp_path):
    database = tmp_path / "legacy.db"

    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE test (value TEXT)")

    result = cache._cc_read_package_info(str(database))

    assert result == {
        "name": "legacy",
        "created_at": "",
        "applied_caches": [],
        "raw_db": True,
    }


def test_snapshot_database_overwrites_existing_destination(cache, tmp_path):
    source = tmp_path / "source.db"
    destination = tmp_path / "snapshot.db"

    with sqlite3.connect(source) as connection:
        connection.execute("CREATE TABLE source_data (value TEXT)")
        connection.execute("INSERT INTO source_data VALUES ('source')")

    with sqlite3.connect(destination) as connection:
        connection.execute("CREATE TABLE old_data (value TEXT)")

    cache._cc_snapshot_database(str(source), str(destination))

    with sqlite3.connect(destination) as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        result = connection.execute("SELECT value FROM source_data").fetchone()

    assert tables == [("source_data",)]
    assert result == ("source",)


def test_read_package_info_rejects_invalid_json(cache, tmp_path):
    package = tmp_path / "invalid.ccdb"

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("config.json", "{invalid")
        archive.writestr("rbx-storage.db", b"database")

    with pytest.raises(json.JSONDecodeError):
        cache._cc_read_package_info(str(package))


def test_read_package_info_rejects_non_object_metadata(cache, tmp_path):
    package = tmp_path / "invalid.ccdb"

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("config.json", json.dumps(["unexpected"]))
        archive.writestr("rbx-storage.db", b"database")

    with pytest.raises(TypeError):
        cache._cc_read_package_info(str(package))


def test_read_package_info_rejects_corrupt_zip(cache, tmp_path):
    package = tmp_path / "invalid.ccdb"
    package.write_bytes(b"not a zip archive")

    with pytest.raises(zipfile.BadZipFile):
        cache._cc_read_package_info(str(package))


def test_read_package_info_rejects_invalid_utf8_metadata(cache, tmp_path):
    package = tmp_path / "invalid.ccdb"

    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("config.json", b"\xff\xfe")
        archive.writestr("rbx-storage.db", b"database")

    with pytest.raises(UnicodeDecodeError):
        cache._cc_read_package_info(str(package))
