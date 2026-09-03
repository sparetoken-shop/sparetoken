"""Product pulse cannot stamp PULSE_OK without a live matching VERSION."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from verify_heartbeat_live import read_version, verify_health  # noqa: E402

HB_SH = (ROOT / "ceo" / "launch" / "heartbeat.sh").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


def _fetch(status: int, payload: dict | str):
    body = payload if isinstance(payload, str) else json.dumps(payload)

    def inner(_url: str):
        return status, body

    return inner


class VerifyHeartbeatLiveTest(unittest.TestCase):
    def test_accepts_matching_health(self):
        ver = read_version(ROOT)
        ok, reason = verify_health(
            ver,
            "https://sparetoken.shop/api/health",
            fetch=_fetch(200, {"ok": True, "service": "sparetoken", "version": ver}),
        )
        self.assertTrue(ok, reason)

    def test_rejects_stale_version(self):
        ok, reason = verify_health(
            "0.2.21",
            "https://sparetoken.shop/api/health",
            fetch=_fetch(200, {"ok": True, "service": "sparetoken", "version": "0.2.20"}),
        )
        self.assertFalse(ok)
        self.assertIn("mismatch", reason)

    def test_rejects_health_without_version(self):
        ok, reason = verify_health(
            "0.2.21",
            "https://sparetoken.shop/api/health",
            fetch=_fetch(200, {"ok": True, "service": "sparetoken"}),
        )
        self.assertFalse(ok)
        self.assertIn("missing", reason)

    def test_rejects_http_error(self):
        ok, _ = verify_health(
            "0.2.21",
            "https://sparetoken.shop/api/health",
            fetch=_fetch(500, {"ok": False}),
        )
        self.assertFalse(ok)

    def test_wrapper_dies_without_verify(self):
        self.assertIn("verify_heartbeat_live.py", HB_SH)
        self.assertIn("PULSE_DEAD", HB_SH)
        self.assertIn("exit 78", HB_SH)
        lines = [ln for ln in HB_SH.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        verify_i = next(i for i, ln in enumerate(lines) if "verify_heartbeat_live.py" in ln)
        ok_i = next(i for i, ln in enumerate(lines) if "PULSE_OK" in ln)
        self.assertLess(verify_i, ok_i)

    def test_health_handler_exposes_version(self):
        self.assertIn('"version": app_version()', SERVER)
        self.assertIn("def app_version()", SERVER)
