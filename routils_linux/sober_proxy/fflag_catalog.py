import json
import os
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import urllib.error
import urllib.request
from pathlib import Path

FFLAG_CATALOG_URL = "https://raw.githubusercontent.com/MaximumADHD/Roblox-FFlag-Tracker/refs/heads/main/PCDesktopClient.json"
FFLAG_CATALOG_TTL = 900
FFLAG_CATALOG_MAX_BYTES = 8 * 1024 * 1024


def _retry_after_seconds(error):
    headers = getattr(error, "headers", None)
    if headers is None:
        return None
    value = headers.get("Retry-After", "")
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        try:
            retry_at = parsedate_to_datetime(str(value))
            if retry_at.tzinfo is None:
                retry_at = retry_at.replace(tzinfo=timezone.utc)
            return max(0.0, (retry_at - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return None


def _open_with_retries(request, timeout, attempts=4):
    transient_statuses = {408, 425, 429, 500, 502, 503, 504}
    method = str(request.get_method() or "GET").upper()
    retryable = method in {"GET", "HEAD"} and getattr(request, "data", None) is None
    total_attempts = max(1, min(5, int(attempts))) if retryable else 1
    for attempt in range(total_attempts):
        try:
            return urllib.request.urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            if not retryable or error.code not in transient_statuses or attempt + 1 >= total_attempts:
                raise
            retry_after = _retry_after_seconds(error)
            try:
                error.close()
            except Exception:
                pass
            delay = min(6.0, max(0.5 * (2 ** attempt), retry_after or 0.0))
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as error:
            if not retryable or attempt + 1 >= total_attempts:
                raise
            time.sleep(min(4.0, 0.5 * (2 ** attempt)))
    raise RuntimeError("The request could not be completed.")


def _display_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _entries_from_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("The FFlag source did not return a JSON object.")
    entries = []
    for name, value in payload.items():
        if not isinstance(name, str) or not name.strip():
            continue
        if isinstance(value, (dict, list)):
            continue
        entries.append((name, _display_value(value)))
    if len(entries) < 500:
        raise ValueError("The FFlag source returned too few entries.")
    entries.sort(key=lambda item: item[0].casefold())
    return entries


def _read_cache(cache_path):
    try:
        data = json.loads(Path(cache_path).read_text(encoding="utf-8"))
        if data.get("source") != FFLAG_CATALOG_URL or not isinstance(data.get("entries"), list):
            return None
        entries = []
        for item in data["entries"]:
            if isinstance(item, list) and len(item) == 2:
                entries.append((str(item[0]), str(item[1])))
        if len(entries) < 500:
            return None
        return float(data.get("fetched_at", 0)), entries
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return None


def fetch_fflag_catalog(data_dir, force=False, timeout=15):
    cache_path = Path(data_dir).expanduser() / "fflag_catalog_cache.json"
    cached = _read_cache(cache_path)
    now = time.time()
    if not force and cached and now - cached[0] <= FFLAG_CATALOG_TTL:
        return {"entries": cached[1], "status": f"Cache · {len(cached[1]):,} FFlags", "cached": True}
    request = urllib.request.Request(
        FFLAG_CATALOG_URL,
        headers={"Accept": "application/json", "User-Agent": "RoUtils/1.0"},
        method="GET",
    )
    try:
        with _open_with_retries(request, timeout=timeout) as response:
            body = response.read(FFLAG_CATALOG_MAX_BYTES + 1)
        if len(body) > FFLAG_CATALOG_MAX_BYTES:
            raise ValueError("The FFlag source is larger than expected.")
        payload = json.loads(body.decode("utf-8-sig"))
        entries = _entries_from_payload(payload)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = cache_path.with_name(cache_path.name + ".tmp")
        temporary.write_text(
            json.dumps(
                {"source": FFLAG_CATALOG_URL, "fetched_at": now, "entries": entries},
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
        os.replace(temporary, cache_path)
        return {"entries": entries, "status": f"Updated · {len(entries):,} FFlags", "cached": False}
    except Exception as error:
        if cached:
            return {
                "entries": cached[1],
                "status": f"Offline cache · {len(cached[1]):,} FFlags · {error}",
                "cached": True,
                "error": str(error),
            }
        raise RuntimeError(f"The FFlag catalog could not be downloaded: {error}") from error
