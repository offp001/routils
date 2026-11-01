import json
import tempfile
import unittest
from pathlib import Path

from sober_proxy.fflags import load_routils_flags, merge_clientsettings_payload


class SoberProxyFlagTests(unittest.TestCase):
    def test_merges_and_appends_application_settings(self):
        payload = {"applicationSettings": [{"name": "FFlagExisting", "value": "false", "source": "server"}]}
        merged, count = merge_clientsettings_payload(payload, {"FFlagExisting": True, "DFIntNewValue": 8})
        values = {item["name"]: item["value"] for item in merged["applicationSettings"]}
        self.assertEqual(values["FFlagExisting"], "true")
        self.assertEqual(values["DFIntNewValue"], "8")
        self.assertEqual(count, 2)
        self.assertEqual(merged["applicationSettings"][0]["source"], "server")

    def test_merges_case_insensitively_without_duplicate_keys(self):
        payload = [{"name": "FFlagExisting", "value": "false"}]
        merged, count = merge_clientsettings_payload(payload, {"fflagexisting": "true"})
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["value"], "true")
        self.assertEqual(count, 1)

    def test_reads_and_normalizes_routils_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "routils_fflags.json"
            path.write_text(json.dumps([
                {"name": "EnableFeature", "prefix": "FFlag", "value": "true", "type": "bool"},
                {"name": "FrameRate", "prefix": "DFInt", "value": "240", "type": "int"},
            ]), encoding="utf-8")
            self.assertEqual(load_routils_flags(path), {"FFlagEnableFeature": True, "DFIntFrameRate": 240})


    def test_merges_flat_payload_with_metadata_and_preserves_native_values(self):
        payload = {"applicationSettings": {"DFFlagExisting": False, "DFIntExisting": 1}, "version": "2"}
        merged, count = merge_clientsettings_payload(payload, {"DFFlagExisting": True, "DFIntExisting": 240, "DFIntNew": 360})
        settings = merged["applicationSettings"]
        self.assertIs(settings["DFFlagExisting"], True)
        self.assertEqual(settings["DFIntExisting"], 240)
        self.assertEqual(settings["DFIntNew"], 360)
        self.assertEqual(merged["version"], "2")
        self.assertEqual(count, 3)

    def test_merges_custom_flag_without_local_allowlist_filter(self):
        payload = {"applicationSettings": [{"name": "FFlagExisting", "value": "false"}]}
        custom_flag = "DFIntRoUtilsCustomUnlistedValue"
        merged, count = merge_clientsettings_payload(payload, {custom_flag: 987654})
        values = {item["name"]: item["value"] for item in merged["applicationSettings"]}
        self.assertEqual(values[custom_flag], "987654")
        self.assertEqual(count, 1)

    def test_noop_for_non_settings_payload(self):
        payload = {"message": "not settings", "code": 200}
        merged, count = merge_clientsettings_payload(payload, {"FFlagOne": True})
        self.assertEqual(merged, payload)
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
