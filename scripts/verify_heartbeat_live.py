#!/usr/bin/env python3
"""Prove the product pulse actually shipped. PULSE_OK is illegal without this.

Same bar as verify_sell_live: a GET, not a log line.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = "https://sparetoken.shop/api/health"
UA = "sparetoken-heartbeat-verify/0.2.21"


def read_version(root: Path | None = None) -> str:
    path = (root or ROOT) / "VERSION"
    return path.read_text(encoding="utf-8").strip()


def default_fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read(20_000).decode("utf-8", errors="replace")
            return int(resp.status), body
    except urllib.error.HTTPError as exc:
        raw = exc.read(20_000) if exc.fp else b""
        return int(exc.code), raw.decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"fetch failed: {exc}") from exc


def verify_health(
    expected_version: str,
    url: str,
    *,
    fetch=None,
) -> tuple[bool, str]:
    if not expected_version:
        return False, "missing VERSION"
    getter = fetch or default_fetch
    try:
        status, body = getter(url)
    except Exception as exc:  # noqa: BLE001
        return False, f"fetch error: {exc}"
    if status != 200:
        return False, f"http {status}"
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return False, "health is not json"
    if not isinstance(data, dict) or not data.get("ok"):
        return False, "health not ok"
    live = str(data.get("version") or "").strip()
    if live != expected_version:
        return False, f"version mismatch live={live or 'missing'} want={expected_version}"
    if data.get("service") != "sparetoken":
        return False, "service is not sparetoken"
    return True, f"ok {expected_version}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    expected = read_version(Path(args.root))
    ok, reason = verify_health(expected, args.url)
    print(f"verify_heartbeat_live {args.url} → {ok} {reason}")
    return 0 if ok else 78


if __name__ == "__main__":
    sys.exit(main())
