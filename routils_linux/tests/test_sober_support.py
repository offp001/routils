import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

import sober_support


class SoberSupportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app_root = self.root / ".var" / "app" / "org.vinegarhq.Sober"
        self.config = self.app_root / "config" / "sober" / "config.json"
        self.data = self.app_root / "data" / "sober"
        self.appdata = self.data / "appData"
        self.config.parent.mkdir(parents=True)
        self.appdata.mkdir(parents=True)
        self.old_env = {key: os.environ.get(key) for key in ("SOBER_CONFIG_PATH", "SOBER_APP_ROOT", "SOBER_DATA_DIR")}
        os.environ["SOBER_CONFIG_PATH"] = str(self.config)
        os.environ["SOBER_APP_ROOT"] = str(self.app_root)
        os.environ.pop("SOBER_DATA_DIR", None)

    def tearDown(self):
        for key, value in self.old_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.temp.cleanup()

    def test_jsonc_apply_restore_preserves_settings_and_comments(self):
        header = "// Sober's configuration warning\n// Keep local changes backed up\n"
        original_fflags = {"DFFlagExisting": True, "DFStringNumber": "123"}
        original = header + json.dumps({"enable_gamemode": True, "fflags": original_fflags}, indent=2) + "\n"
        self.config.write_text(original, encoding="utf-8")
        flags = [
            {"name": "Number", "prefix": "DFString", "value": "456", "type": "int"},
            {"name": "NewFlag", "prefix": "FFlag", "value": "true", "type": "string"},
            {"name": "FrameRate", "prefix": "DFInt", "value": "240", "type": "int"},
        ]
        result = sober_support.apply_sober_fflags(flags, self.root / "state")
        self.assertEqual(result["applied"], 3)
        self.assertEqual(result["total"], 3)
        written = self.config.read_text(encoding="utf-8")
        self.assertTrue(written.startswith(header))
        config = sober_support._jsonc_loads(written)
        self.assertIs(config["enable_gamemode"], True)
        self.assertEqual(config["fflags"]["DFStringNumber"], "456")
        self.assertIs(config["fflags"]["FFlagNewFlag"], True)
        self.assertEqual(config["fflags"]["DFIntFrameRate"], 240)
        sober_support.restore_sober_fflags(self.root / "state")
        restored = self.config.read_text(encoding="utf-8")
        restored_config = sober_support._jsonc_loads(restored)
        self.assertTrue(restored.startswith(header))
        self.assertEqual(restored_config["fflags"], original_fflags)
        self.assertIs(restored_config["enable_gamemode"], True)

    def test_detects_linux_storage_paths(self):
        db = self.appdata / "rbx-storage.db"
        shards = self.app_root / "cache" / "sober" / "rbx-storage"
        shards.mkdir(parents=True)
        db.write_bytes(b"")
        found_db, found_shards = sober_support.sober_storage_paths()
        self.assertEqual(Path(found_db), db)
        self.assertEqual(Path(found_shards), shards)

    def test_finds_existing_cache_shards_when_database_path_is_separate(self):
        db = self.appdata / "rbx-storage.db"
        db.write_bytes(b"")
        shards = self.app_root / "cache" / "sober" / "rbx-storage"
        shards.mkdir(parents=True)
        (shards / "ab").mkdir()
        (shards / "ab" / "ab1234").write_bytes(b"asset")
        found_db, found_shards = sober_support.sober_storage_paths()
        self.assertEqual(Path(found_db), db)
        self.assertTrue((Path(found_shards) / "ab" / "ab1234").is_file())

    def test_environment_can_override_database_and_shards_independently(self):
        db = self.root / "other" / "rbx-storage.db"
        db.parent.mkdir(parents=True)
        db.write_bytes(b"")
        shards = self.root / "cache_override"
        shards.mkdir()
        os.environ["SOBER_STORAGE_DB_PATH"] = str(db)
        os.environ["SOBER_SHARD_ROOT"] = str(shards)
        try:
            found_db, found_shards = sober_support.sober_storage_paths()
            self.assertEqual(Path(found_db), db)
            self.assertEqual(Path(found_shards), shards)
        finally:
            os.environ.pop("SOBER_STORAGE_DB_PATH", None)
            os.environ.pop("SOBER_SHARD_ROOT", None)

    def test_detects_sober_logs_directory(self):
        logs = self.data / "sober_logs"
        logs.mkdir()
        (logs / "session.log").write_text("ok", encoding="utf-8")
        self.assertEqual(Path(sober_support.sober_logs_dir()), logs)

    def test_default_sober_database_overrides_stale_saved_database(self):
        default_db = self.appdata / "rbx-storage.db"
        default_db.write_bytes(b"sober")
        saved_db = self.root / "old" / "rbx-storage.db"
        saved_db.parent.mkdir(parents=True)
        saved_db.write_bytes(b"old")
        default_shards = self.app_root / "cache" / "sober" / "rbx-storage"
        default_shards.mkdir(parents=True)
        result = sober_support.resolve_storage_selection(str(saved_db), "", str(default_db), str(default_shards))
        self.assertEqual(result, (str(default_db), str(default_shards)))

    def test_saved_database_is_used_when_sober_database_does_not_exist(self):
        saved_db = self.root / "custom" / "rbx-storage.db"
        saved_db.parent.mkdir(parents=True)
        saved_db.write_bytes(b"custom")
        saved_shards = self.root / "custom-shards"
        saved_shards.mkdir()
        default_db = self.appdata / "rbx-storage.db"
        default_shards = self.app_root / "cache" / "sober" / "rbx-storage"
        result = sober_support.resolve_storage_selection(str(saved_db), str(saved_shards), str(default_db), str(default_shards))
        self.assertEqual(result, (str(saved_db), str(saved_shards)))

    def test_detects_sober_flatpak_instance_pid(self):
        fake_flatpak = Mock(return_value='/usr/bin/flatpak')
        result = Mock(returncode=0, stdout='APPLICATION PID\norg.vinegarhq.Sober 4821\n', stderr='')
        with patch.object(sober_support.shutil, 'which', fake_flatpak), patch.object(sober_support.subprocess, 'run', return_value=result):
            found, pids = sober_support._flatpak_sober_instances()
        self.assertTrue(found)
        self.assertEqual(pids, [4821])

    def test_rejects_invalid_flag_values(self):
        with self.assertRaises(ValueError):
            sober_support._flag_config_value({"name": "Bad", "prefix": "DFFlag", "value": "maybe"})


if __name__ == "__main__":
    unittest.main()
