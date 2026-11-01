import asyncio
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from mitmproxy import ctx
from sober_proxy.fflags import load_routils_flags, merge_clientsettings_payload
from sober_support import sober_process_pids

_ALLOWED_HOSTS = {"clientsettings.roblox.com", "clientsettingscdn.roblox.com"}
_DYNAMIC_RELOAD_FLAG = "DFIntSecondsBetweenDynamicVariableReloading"
_DYNAMIC_RELOAD_VALUE = "1"
_INTERCEPT_PATTERN = r"^(?!(?:clientsettings|clientsettingscdn)\.roblox\.com:443$).*"


class SoberFastFlagAddon:
    def __init__(self):
        self._interception_enabled = False
        self._intercept_task = None
        self._stopped = False
        try:
            self._intercept_delay = max(0.0, min(180.0, float(os.environ.get("ROUTILS_SOBER_INTERCEPT_DELAY", "20"))))
        except (TypeError, ValueError):
            self._intercept_delay = 20.0

    def running(self):
        self._stopped = False
        if self._intercept_delay <= 0:
            self._enable_interception()
            return
        self._intercept_task = asyncio.get_running_loop().create_task(self._enable_interception_after_delay())

    def done(self):
        self._stopped = True
        if self._intercept_task is not None and not self._intercept_task.done():
            self._intercept_task.cancel()

    def _sober_process_started_at(self):
        clock_ticks = os.sysconf("SC_CLK_TCK")
        boot_time = None
        try:
            for line in Path("/proc/stat").read_text(encoding="ascii").splitlines():
                if line.startswith("btime "):
                    boot_time = float(line.split()[1])
                    break
        except (OSError, ValueError, IndexError):
            boot_time = None
        for pid in sober_process_pids():
            try:
                stat = Path("/proc", str(int(pid)), "stat").read_text(encoding="ascii")
                fields = stat[stat.rfind(")") + 2:].split()
                start_ticks = int(fields[19])
                if boot_time is not None:
                    return boot_time + start_ticks / clock_ticks
            except (OSError, ValueError, IndexError, TypeError):
                continue
        return None

    def _custom_flags_enabled(self):
        flags_path = os.environ.get("ROUTILS_FFLAGS_PATH", "")
        if not flags_path:
            data_home = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share")))
            flags_path = str(data_home / "RoUtils" / "routils_fflags.json")
        return bool(load_routils_flags(flags_path))

    async def _enable_interception_after_delay(self):
        while not self._stopped:
            process_started_at = self._sober_process_started_at()
            delay_elapsed = process_started_at is not None and time.time() - process_started_at >= self._intercept_delay
            should_intercept = bool(delay_elapsed and self._custom_flags_enabled())
            if should_intercept and not self._interception_enabled:
                self._enable_interception()
            elif not should_intercept and self._interception_enabled:
                self._disable_interception()
            await asyncio.sleep(0.5)

    def _enable_interception(self):
        if self._interception_enabled:
            return
        ctx.options.update(ignore_hosts=[_INTERCEPT_PATTERN])
        self._interception_enabled = True
        ctx.log.info(f"RoUtils ClientSettings interception enabled after {self._intercept_delay:.1f}s Sober bootstrap tunnel")

    def _disable_interception(self):
        if not self._interception_enabled:
            return
        ctx.options.update(ignore_hosts=[".*"])
        self._interception_enabled = False
        ctx.log.info("RoUtils ClientSettings interception disabled because custom FastFlags are empty or Sober is not running")

    def request(self, flow):
        if not self._interception_enabled:
            return
        host = str(flow.request.pretty_host or "").lower().rstrip(".")
        if host not in _ALLOWED_HOSTS:
            return
        path = urlsplit(str(flow.request.pretty_url or "")).path.lower()
        if "/v2/settings/application" not in path and "/settings/application" not in path:
            return
        for header in list(flow.request.headers):
            if str(header).lower() in {"if-none-match", "if-modified-since"}:
                flow.request.headers.pop(header, None)
        flow.request.headers["Cache-Control"] = "no-cache"
        flow.request.headers["Pragma"] = "no-cache"

    def response(self, flow):
        if not self._interception_enabled:
            return
        host = str(flow.request.pretty_host or "").lower().rstrip(".")
        if host not in _ALLOWED_HOSTS:
            return
        path = urlsplit(str(flow.request.pretty_url or "")).path.lower()
        if "/v2/settings/application" not in path and "/settings/application" not in path:
            return
        response = flow.response
        if response is None or not response.content:
            return
        try:
            payload = json.loads(response.get_text(strict=False))
            flags_path = os.environ.get("ROUTILS_FFLAGS_PATH", "")
            if not flags_path:
                data_home = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share")))
                flags_path = str(data_home / "RoUtils" / "routils_fflags.json")
            flags = load_routils_flags(flags_path)
            if not flags:
                ctx.log.debug(f"RoUtils has no custom FastFlags to apply to {host}{path}")
                return
            flags[_DYNAMIC_RELOAD_FLAG] = _DYNAMIC_RELOAD_VALUE
            merged, count = merge_clientsettings_payload(payload, flags)
            if count:
                response.set_text(json.dumps(merged, ensure_ascii=False, separators=(",", ":")))
                ctx.log.info(f"RoUtils merged {count} live FastFlags into {host}{path}")
            else:
                ctx.log.debug(f"RoUtils found no FastFlags to change in {host}{path}")
        except Exception as error:
            ctx.log.warn(f"RoUtils ClientSettings interception skipped: {error}")


addons = [SoberFastFlagAddon()]
