import ntpath
import tempfile
import unittest
from pathlib import Path

from client.global_settings import default_global_settings_path, read_global_settings, save_global_settings


class GlobalSettingsTests(unittest.TestCase):
    def test_windows_default_path(self):
        path = default_global_settings_path("nt", local_app_data=r"C:\Users\Example\AppData\Local")
        self.assertEqual(ntpath.normpath(str(path)), r"C:\Users\Example\AppData\Local\Roblox\GlobalBasicSettings_13.xml")

    def test_sober_default_path(self):
        path = default_global_settings_path("posix", home="/home/example")
        self.assertEqual(
            path,
            Path("/home/example/.var/app/org.vinegarhq.Sober/data/sober/appData/GlobalBasicSettings_13.xml"),
        )

    def test_load_and_save_leaf_values_and_create_backup(self):
        original = b'''<?xml version="1.0" encoding="UTF-8"?>\n<roblox version="4">\n  <!-- keep this comment -->\n  <Item class="UserGameSettings">\n    <Properties>\n      <bool name="Fullscreen">false</bool>\n      <int name="FramerateCap">60</int>\n      <string name="WindowMode">windowed</string>\n    </Properties>\n  </Item>\n</roblox>\n'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "GlobalBasicSettings_13.xml"
            path.write_bytes(original)
            rows, digest = read_global_settings(path)
            self.assertEqual([row["name"] for row in rows], ["Fullscreen", "FramerateCap", "WindowMode"])
            backup, _ = save_global_settings(
                path,
                {tuple(rows[0]["path"]): "true", tuple(rows[1]["path"]): "144"},
                digest,
            )
            self.assertEqual(backup.read_bytes(), original)
            updated_rows, _ = read_global_settings(path)
            self.assertEqual([row["value"] for row in updated_rows], ["true", "144", "windowed"])
            self.assertIn(b"<!-- keep this comment -->", path.read_bytes())

    def test_rejects_invalid_typed_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.xml"
            path.write_text('<roblox><bool name="Fullscreen">false</bool></roblox>', encoding="utf-8")
            rows, digest = read_global_settings(path)
            with self.assertRaises(ValueError):
                save_global_settings(path, {tuple(rows[0]["path"]): "yes"}, digest)

    def test_refuses_to_overwrite_a_changed_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.xml"
            path.write_text('<roblox><int name="FramerateCap">60</int></roblox>', encoding="utf-8")
            rows, digest = read_global_settings(path)
            path.write_text('<roblox><int name="FramerateCap">75</int></roblox>', encoding="utf-8")
            with self.assertRaises(RuntimeError):
                save_global_settings(path, {tuple(rows[0]["path"]): "120"}, digest)


if __name__ == "__main__":
    unittest.main()
