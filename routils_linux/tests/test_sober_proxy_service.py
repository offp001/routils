import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

try:
    from sober_proxy.service import SoberProxyService
except ImportError:
    SoberProxyService = None


@unittest.skipIf(SoberProxyService is None, "cryptography dependency is not installed")
class SoberProxyServiceTests(unittest.TestCase):
    def test_patches_and_restores_an_existing_overlay(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            service = SoberProxyService(base / "data")
            service.overlay_path = base / "sober" / "asset_overlay" / "ssl" / "cacert.pem"
            service.overlay_path.parent.mkdir(parents=True)
            original = b"existing-ca-bundle\n"
            service.overlay_path.write_bytes(original)
            ca = service._make_ca()
            service._patch_overlay(ca)
            patched = service.overlay_path.read_bytes()
            self.assertIn(original, patched)
            self.assertIn(ca.strip(), patched)
            service._restore_overlay()
            self.assertEqual(service.overlay_path.read_bytes(), original)

    def test_removes_overlay_created_by_proxy(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            service = SoberProxyService(base / "data")
            service.overlay_path = base / "sober" / "asset_overlay" / "ssl" / "cacert.pem"
            ca = service._make_ca()
            service._patch_overlay(ca)
            self.assertTrue(service.overlay_path.is_file())
            service._restore_overlay()
            self.assertFalse(service.overlay_path.exists())

    def test_port_owner_uses_sudo_ss_and_parses_program_name(self):
        service = SoberProxyService(Path(tempfile.gettempdir()) / "routils-port-test")
        output = 'State Recv-Q Send-Q Local Address:Port Peer Address:Port Process\nLISTEN 0 128 127.0.0.1:58443 0.0.0.0:* users:(("other-app",pid=424242,fd=7))\n'
        called = []

        def fake_run(command, **kwargs):
            called.append(command)
            return SimpleNamespace(returncode=0, stdout=output, stderr='')

        def fake_which(name):
            return {"sudo": "/usr/bin/sudo", "ss": "/usr/bin/ss"}.get(name)

        with patch("sober_proxy.service.shutil.which", side_effect=fake_which), patch("sober_proxy.service.subprocess.run", side_effect=fake_run):
            owner = service._port_owner(58443)

        self.assertEqual(owner["pid"], 424242)
        self.assertEqual(owner["name"], "other-app")
        self.assertEqual(called[0], ["/usr/bin/sudo", "-n", "/usr/bin/ss", "-lptn", "sport = :58443"])


if __name__ == "__main__":
    unittest.main()
