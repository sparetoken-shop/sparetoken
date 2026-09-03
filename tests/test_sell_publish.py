"""Publisher returns 0 only after verify; 78 on empty theater."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sell_publish as sp  # noqa: E402


GOOD = (
    '<html>sparetoken.shop utm_campaign=sell utm_content=s0831 '
    '<a href="https://sparetoken.shop/?utm_source=x&utm_medium=comment'
    '&utm_campaign=sell&utm_content=s0831">x</a></html>'
)


class SellPublishTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["SELL_DAY"] = "2026-08-31"
        os.environ["SELL_UTM_CONTENT"] = "s0831"
        os.environ["SELL_HUMAN_WAIT_SEC"] = "0"
        os.environ["SELL_PROOF_FILE"] = str(Path(self.tmp.name) / "proof.jsonl")

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("SELL_PROOF_URL", None)

    def test_human_proof_url_short_circuits(self):
        os.environ["SELL_PROOF_URL"] = "https://dev.to/sparetoken/ok"

        def fetch(_url: str):
            return 200, "https://dev.to/sparetoken/ok", GOOD

        code = sp.run(
            fetch=fetch,
            notify=lambda _m: (2, 2),
            start_vnc=lambda *_a, **_k: {"url": "https://sparetoken.shop/pulse-vnc/x/"},
            stop_vnc=lambda: None,
            signup=lambda: {"challenge": False},
            sleep=lambda _s: None,
            fallback=lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("no fallback")),
        )
        self.assertEqual(code, 0)

    def test_fallback_needs_both_live_urls(self):
        def fetch(url: str):
            return 200, url, GOOD

        def fallback(_day, _utm):
            return {
                "shop_url": "https://sparetoken.shop/pulse/2026-08-31.html",
                "github_url": "https://github.com/sparetoken-shop/sparetoken/issues/9",
            }

        notes = []
        code = sp.run(
            fetch=fetch,
            notify=lambda m: notes.append(m) or (0, 2),
            start_vnc=lambda *_a, **_k: {"url": "https://sparetoken.shop/pulse-vnc/x/"},
            stop_vnc=lambda: None,
            signup=lambda: {"challenge": False},
            sleep=lambda _s: None,
            fallback=fallback,
        )
        self.assertEqual(code, 0)
        self.assertEqual(notes, [])

    def test_fallback_dead_without_github(self):
        def fetch(url: str):
            if "github.com" in url:
                return 404, url, "missing"
            return 200, url, GOOD

        def fallback(_day, _utm):
            return {
                "shop_url": "https://sparetoken.shop/pulse/2026-08-31.html",
                "github_url": "",
            }

        notes = []
        code = sp.run(
            fetch=fetch,
            notify=lambda m: notes.append(m) or (2, 2),
            start_vnc=lambda *_a, **_k: {"url": "https://sparetoken.shop/pulse-vnc/x/"},
            stop_vnc=lambda: None,
            signup=lambda: {"challenge": True, "url": "https://dev.to/users/sign_up"},
            sleep=lambda _s: None,
            fallback=fallback,
        )
        self.assertEqual(code, 78)
        self.assertEqual(len(notes), 1)
        self.assertIn("Captcha visivel", notes[0])

    def test_no_fallback_venue_exits_78_without_pulse(self):
        os.environ["SELL_DAY"] = "2026-09-02"
        os.environ["SELL_UTM_CONTENT"] = "s0902"
        called = []
        code = sp.run(
            fetch=lambda url: (200, url, GOOD),
            notify=lambda m: called.append(("zapi", m)) or (0, 0),
            start_vnc=lambda *_a, **_k: {"url": "https://sparetoken.shop/pulse-vnc/x/"},
            stop_vnc=lambda: None,
            signup=lambda: {"challenge": False},
            sleep=lambda _s: None,
            fallback=lambda *_a, **_k: called.append("fallback") or {},
        )
        self.assertEqual(code, 78)
        self.assertNotIn("fallback", called)
        self.assertEqual(called, [])

    def test_signup_for_skips_devto_on_indiehackers(self):
        fn = sp.signup_for({"host": "indiehackers"})
        self.assertIsNot(fn, sp.try_devto)
        self.assertFalse(fn().get("challenge"))
