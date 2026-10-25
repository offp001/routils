import asyncio
import importlib.util
import os
import sys
import types
import time
import unittest
from unittest.mock import patch
from pathlib import Path


class FakeOptions:
    def __init__(self):
        self.calls = []

    def update(self, **kwargs):
        self.calls.append(kwargs)


class FakeLog:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(("info", message))

    def debug(self, message):
        self.messages.append(("debug", message))

    def warn(self, message):
        self.messages.append(("warn", message))


class SoberProxyInterceptionTests(unittest.TestCase):
    def _load_addon(self):
        fake_ctx = types.SimpleNamespace(options=FakeOptions(), log=FakeLog())
        fake_mitmproxy = types.ModuleType("mitmproxy")
        fake_mitmproxy.ctx = fake_ctx
        previous = sys.modules.get("mitmproxy")
        sys.modules["mitmproxy"] = fake_mitmproxy
        module_name = "routils_test_mitm_addon"
        source = Path(__file__).resolve().parents[1] / "sober_proxy" / "mitm_addon.py"
        try:
            spec = importlib.util.spec_from_file_location(module_name, source)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        finally:
            if previous is None:
                sys.modules.pop("mitmproxy", None)
            else:
                sys.modules["mitmproxy"] = previous
        return module.SoberFastFlagAddon(), fake_ctx, module

    def test_interception_waits_for_sober_bootstrap_and_custom_flags(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "20"}):
            addon, fake_ctx, module = self._load_addon()
        self.assertEqual(addon._intercept_delay, 20.0)
        self.assertFalse(addon._interception_enabled)
        real_sleep = asyncio.sleep

        async def quick_sleep(delay):
            self.assertLessEqual(delay, 0.5)
            await real_sleep(0)

        async def exercise():
            with patch.object(addon, "_sober_process_started_at", return_value=time.time() - 20.5), patch.object(addon, "_custom_flags_enabled", return_value=True), patch.object(module.asyncio, "sleep", new=quick_sleep):
                addon.running()
                await real_sleep(0)
                await real_sleep(0)
                self.assertTrue(addon._interception_enabled)
                addon.done()
                await real_sleep(0)

        asyncio.run(exercise())
        self.assertEqual(len(fake_ctx.options.calls), 1)
        value = fake_ctx.options.calls[0]["ignore_hosts"]
        self.assertEqual(value, [r"^(?!(?:clientsettings|clientsettingscdn)\.roblox\.com:443$).*"])

    def test_interception_stays_tunneled_when_custom_flags_are_empty(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "20"}):
            addon, fake_ctx, module = self._load_addon()
        real_sleep = asyncio.sleep

        async def quick_sleep(delay):
            await real_sleep(0)

        async def exercise():
            with patch.object(addon, "_sober_process_started_at", return_value=time.time() - 30), patch.object(addon, "_custom_flags_enabled", return_value=False), patch.object(module.asyncio, "sleep", new=quick_sleep):
                addon.running()
                await real_sleep(0)
                await real_sleep(0)
                self.assertFalse(addon._interception_enabled)
                addon.done()
                await real_sleep(0)

        asyncio.run(exercise())
        self.assertEqual(fake_ctx.options.calls, [])

    def test_cache_validators_are_removed_for_clientsettings(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "0"}):
            addon, _fake_ctx, _module = self._load_addon()
        addon.running()
        headers = {"If-None-Match": "test-etag", "If-Modified-Since": "yesterday"}
        request = types.SimpleNamespace(
            pretty_host="clientsettings.roblox.com",
            pretty_url="https://clientsettings.roblox.com/v2/settings/application",
            headers=headers,
        )
        addon.request(types.SimpleNamespace(request=request))
        self.assertNotIn("If-None-Match", headers)
        self.assertNotIn("If-Modified-Since", headers)
        self.assertEqual(headers["Cache-Control"], "no-cache")
        self.assertEqual(headers["Pragma"], "no-cache")


    def test_response_applies_custom_flags_to_clientsettings_payload(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "0"}):
            addon, fake_ctx, _module = self._load_addon()
        addon.running()
        old_path = os.environ.get("ROUTILS_FFLAGS_PATH")
        try:
            with __import__("tempfile").TemporaryDirectory() as directory:
                flags_path = Path(directory) / "routils_fflags.json"
                flags_path.write_text(
                    '[{"name":"FFlagExisting","value":"true","type":"bool"},'
                    '{"name":"DFIntRoUtilsCustomUnlistedValue","value":"987654","type":"int"}]',
                    encoding="utf-8",
                )
                os.environ["ROUTILS_FFLAGS_PATH"] = str(flags_path)
                class FakeResponse:
                    def __init__(self):
                        self.content = b'{"applicationSettings":[{"name":"FFlagExisting","value":"false"}]}'
                        self.text = self.content.decode("utf-8")

                    def get_text(self, strict=False):
                        return self.text

                    def set_text(self, value):
                        self.text = value
                        self.content = value.encode("utf-8")

                request = types.SimpleNamespace(
                    pretty_host="clientsettings.roblox.com",
                    pretty_url="https://clientsettings.roblox.com/v2/settings/application",
                )
                response = FakeResponse()
                addon.response(types.SimpleNamespace(request=request, response=response))
                import json
                result = json.loads(response.text)
                values = {item["name"]: item["value"] for item in result["applicationSettings"]}
                self.assertEqual(values["FFlagExisting"], "true")
                self.assertEqual(values["DFIntRoUtilsCustomUnlistedValue"], "987654")
                self.assertEqual(values["DFIntSecondsBetweenDynamicVariableReloading"], "1")
                self.assertNotIn("DFFlagHttpUseEmbeddedCaCerts", values)
                self.assertTrue(any("merged 3 live FastFlags" in message for level, message in fake_ctx.log.messages))
        finally:
            if old_path is None:
                os.environ.pop("ROUTILS_FFLAGS_PATH", None)
            else:
                os.environ["ROUTILS_FFLAGS_PATH"] = old_path

    def test_empty_custom_flag_list_leaves_clientsettings_unchanged(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "0"}):
            addon, _fake_ctx, _module = self._load_addon()
        addon.running()
        old_path = os.environ.get("ROUTILS_FFLAGS_PATH")
        try:
            with __import__("tempfile").TemporaryDirectory() as directory:
                os.environ["ROUTILS_FFLAGS_PATH"] = str(Path(directory) / "missing.json")
                class FakeResponse:
                    def __init__(self):
                        self.content = b'{"applicationSettings":[]}'
                        self.text = self.content.decode("utf-8")
                    def get_text(self, strict=False):
                        return self.text
                    def set_text(self, value):
                        self.text = value
                        self.content = value.encode("utf-8")
                request = types.SimpleNamespace(pretty_host="clientsettings.roblox.com", pretty_url="https://clientsettings.roblox.com/v2/settings/application")
                response = FakeResponse()
                addon.response(types.SimpleNamespace(request=request, response=response))
                import json
                values = {item["name"]: item["value"] for item in json.loads(response.text)["applicationSettings"]}
                self.assertEqual(values, {})
                self.assertEqual(response.content, b'{"applicationSettings":[]}')
        finally:
            if old_path is None:
                os.environ.pop("ROUTILS_FFLAGS_PATH", None)
            else:
                os.environ["ROUTILS_FFLAGS_PATH"] = old_path

    def test_live_response_reads_updated_flag_values_from_disk(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "0"}):
            addon, _fake_ctx, _module = self._load_addon()
        addon.running()
        old_path = os.environ.get("ROUTILS_FFLAGS_PATH")
        try:
            with __import__("tempfile").TemporaryDirectory() as directory:
                flags_path = Path(directory) / "routils_fflags.json"
                os.environ["ROUTILS_FFLAGS_PATH"] = str(flags_path)
                class FakeResponse:
                    def __init__(self):
                        self.content = b'{"applicationSettings":[]}'
                        self.text = self.content.decode("utf-8")
                    def get_text(self, strict=False):
                        return self.text
                    def set_text(self, value):
                        self.text = value
                        self.content = value.encode("utf-8")
                request = types.SimpleNamespace(pretty_host="clientsettings.roblox.com", pretty_url="https://clientsettings.roblox.com/v2/settings/application")
                for value in ("100", "250"):
                    flags_path.write_text('[{"name":"DFIntDynamicLiveTest","value":"' + value + '","type":"int"}]', encoding="utf-8")
                    response = FakeResponse()
                    addon.response(types.SimpleNamespace(request=request, response=response))
                    import json
                    values = {item["name"]: item["value"] for item in json.loads(response.text)["applicationSettings"]}
                    self.assertEqual(values["DFIntDynamicLiveTest"], value)
                    self.assertEqual(values["DFIntSecondsBetweenDynamicVariableReloading"], "1")
        finally:
            if old_path is None:
                os.environ.pop("ROUTILS_FFLAGS_PATH", None)
            else:
                os.environ["ROUTILS_FFLAGS_PATH"] = old_path

    def test_other_hosts_are_not_modified_by_request_hook(self):
        with patch.dict(os.environ, {"ROUTILS_SOBER_INTERCEPT_DELAY": "0"}):
            addon, _fake_ctx, _module = self._load_addon()
        addon.running()
        headers = {"If-None-Match": "test-etag"}
        request = types.SimpleNamespace(
            pretty_host="www.roblox.com",
            pretty_url="https://www.roblox.com/",
            headers=headers,
        )
        addon.request(types.SimpleNamespace(request=request))
        self.assertEqual(headers, {"If-None-Match": "test-etag"})


if __name__ == "__main__":
    unittest.main()
