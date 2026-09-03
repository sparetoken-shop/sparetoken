"""Sell pulse cannot stamp OK without a live non-Twitter URL."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from verify_sell_live import is_blocked_host, verify_url  # noqa: E402

SELL_SH = (ROOT / "ceo" / "launch" / "sell.sh").read_text(encoding="utf-8")
PUBLISH = (ROOT / "scripts" / "sell_publish.py").read_text(encoding="utf-8")
GOOD_HTML = (
    '<html><a href="https://sparetoken.shop/?utm_source=devto'
    '&utm_medium=comment&utm_campaign=sell&utm_content=s000">shop</a></html>'
)


def _fetch(status: int, final: str, body: str):
    def inner(_url: str):
        return status, final, body

    return inner


class VerifySellLiveTest(unittest.TestCase):
    def test_rejects_twitter_hosts(self):
        for url in (
            "https://x.com/sparetoken/status/1",
            "https://twitter.com/sparetoken",
            "https://t.co/abc",
            "https://mobile.twitter.com/x",
            "https://nitter.net/sparetoken",
        ):
            self.assertTrue(is_blocked_host(url), url)
            ok, reason = verify_url(url, "s000", fetch=_fetch(200, url, GOOD_HTML))
            self.assertFalse(ok, url)
            self.assertIn("blocked", reason)

    def test_rejects_redirect_to_x(self):
        ok, reason = verify_url(
            "https://example.com/out",
            "s000",
            fetch=_fetch(200, "https://x.com/sparetoken", GOOD_HTML),
        )
        self.assertFalse(ok)
        self.assertIn("blocked", reason)

    def test_rejects_http_404(self):
        ok, reason = verify_url(
            "https://example.com/missing",
            "s000",
            fetch=_fetch(404, "https://example.com/missing", GOOD_HTML),
        )
        self.assertFalse(ok)
        self.assertIn("404", reason)

    def test_rejects_body_without_utm(self):
        ok, reason = verify_url(
            "https://example.com/post",
            "s000",
            fetch=_fetch(200, "https://example.com/post", "<html>sparetoken.shop</html>"),
        )
        self.assertFalse(ok)
        self.assertIn("utm_campaign", reason)

    def test_rejects_wrong_utm_content(self):
        ok, _ = verify_url(
            "https://example.com/post",
            "s001",
            fetch=_fetch(200, "https://example.com/post", GOOD_HTML),
        )
        self.assertFalse(ok)

    def test_accepts_live_third_party_html(self):
        ok, reason = verify_url(
            "https://dev.to/sparetoken/pulse",
            "s000",
            fetch=_fetch(200, "https://dev.to/sparetoken/pulse", GOOD_HTML),
        )
        self.assertTrue(ok, reason)

    def test_venues_kill_dead_utms_and_point_today_at_gpubridge(self):
        venues = (ROOT / "ceo" / "launch" / "venues.json").read_text(encoding="utf-8")
        table = (ROOT / "ceo" / "VENUES.md").read_text(encoding="utf-8")
        self.assertIn("leftoverpzero", venues)
        self.assertIn("s0901", venues + table)
        self.assertIn("indiehackers", venues.lower() + table.lower())
        self.assertIn("s0902", venues + table)
        self.assertIn("gpubridge", venues.lower() + table.lower())
        self.assertIn("s0903", venues + table)
        self.assertIn("MORTO", table)
        self.assertIn("s0831", table)
        self.assertIn('"fallback": false', venues)

    def test_pulse_vnc_exposes_cdp_for_captcha_detect(self):
        src = (ROOT / "scripts" / "pulse_vnc.py").read_text(encoding="utf-8")
        self.assertIn("--remote-debugging-port=9222", src)
        self.assertIn("/tmp/sparetoken-sell-chrome", src)

    def test_sell_sh_never_stamps_ok_without_publisher(self):
        self.assertIn("sell_publish.py", SELL_SH)
        self.assertNotIn("queued-or-published", SELL_SH)
        self.assertIn("verify_sell_live", PUBLISH)
        # SELL_OK may only be echoed after the publisher exits 0
        lines = [ln.strip() for ln in SELL_SH.splitlines() if ln.strip()]
        ok_idx = next(i for i, ln in enumerate(lines) if ln.startswith("echo \"SELL_OK"))
        pub_idx = next(i for i, ln in enumerate(lines) if "sell_publish.py" in ln)
        self.assertLess(pub_idx, ok_idx)
        self.assertIn("exit 78", SELL_SH)
