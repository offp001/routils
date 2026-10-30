import json
import tempfile
import time
import unittest
from pathlib import Path

from sober_proxy.fflag_catalog import FFLAG_CATALOG_URL, _entries_from_payload, fetch_fflag_catalog


class SoberFFlagCatalogTests(unittest.TestCase):
    def test_catalog_displays_name_and_value_without_offsets(self):
        payload = {f"DFFlagEntry{i:04d}": bool(i % 2) for i in range(501)}
        payload["DFIntSample"] = 240
        entries = _entries_from_payload(payload)
        self.assertGreaterEqual(len(entries), 500)
        self.assertEqual(entries, sorted(entries, key=lambda item: item[0].casefold()))
        values = dict(entries)
        self.assertEqual(values["DFFlagEntry0000"], "false")
        self.assertEqual(values["DFFlagEntry0001"], "true")
        self.assertEqual(values["DFIntSample"], "240")
        self.assertTrue(all(len(item) == 2 for item in entries))

    def test_fresh_cache_is_used_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            entries = [[f"DFFlagEntry{i:04d}", "true"] for i in range(501)]
            cache = Path(directory) / "fflag_catalog_cache.json"
            cache.write_text(json.dumps({"source": FFLAG_CATALOG_URL, "fetched_at": time.time(), "entries": entries}), encoding="utf-8")
            result = fetch_fflag_catalog(directory)
            self.assertTrue(result["cached"])
            self.assertEqual(len(result["entries"]), 501)
            self.assertIn("Cache", result["status"])


if __name__ == "__main__":
    unittest.main()
