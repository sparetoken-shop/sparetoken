"""Shop pulse page + GitHub issue body carry sell UTM."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pulse_fallback import (  # noqa: E402
    create_github_issue,
    issue_body,
    pulse_html,
    publish_fallback,
    write_shop_pulse,
)


class PulseFallbackTest(unittest.TestCase):
    def test_html_has_shop_and_utm(self):
        html = pulse_html(
            "2026-08-31",
            "s0831",
            "https://sparetoken.shop/?utm_source=pulse&utm_medium=comment&utm_campaign=sell&utm_content=s0831",
            "correction",
        )
        self.assertIn("sparetoken.shop", html)
        self.assertIn("utm_campaign=sell", html)
        self.assertIn("utm_content=s0831", html)
        self.assertNotIn("wdtsot-", html)

    def test_writes_static_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_shop_pulse("2026-08-31", "s0831", static_dir=Path(tmp))
            self.assertTrue(path.is_file())
            text = path.read_text(encoding="utf-8")
            self.assertIn("utm_campaign=sell", text)

    def test_github_issue_uses_token_and_returns_url(self):
        def post(url, data, headers):
            self.assertIn("sparetoken-shop/sparetoken/issues", url)
            self.assertTrue(headers["Authorization"].startswith("Bearer "))
            return 201, {"html_url": "https://github.com/sparetoken-shop/sparetoken/issues/9"}

        ok, issue_url = create_github_issue("t", "b", token="ghs_test", post=post)
        self.assertTrue(ok)
        self.assertIn("/issues/9", issue_url)

    def test_github_missing_token_fails(self):
        ok, reason = create_github_issue("t", "b", token="")
        self.assertFalse(ok)
        self.assertIn("GITHUB_TOKEN", reason)

    def test_issue_body_is_verifiable(self):
        body = issue_body("2026-08-31", "s0831", "https://sparetoken.shop/pulse/2026-08-31.html")
        self.assertIn("utm_campaign=sell", body)
        self.assertIn("utm_content=s0831", body)
        self.assertIn("sparetoken.shop", body)

    def test_publish_fallback_records_both_urls(self):
        def post(url, data, headers):
            return 201, {"html_url": "https://github.com/sparetoken-shop/sparetoken/issues/9"}

        with tempfile.TemporaryDirectory() as tmp:
            import os

            os.environ["GITHUB_TOKEN"] = "ghs_test"
            result = publish_fallback(
                "2026-08-31",
                "s0831",
                static_dir=Path(tmp),
                github_post=post,
            )
        self.assertTrue(result["github_ok"])
        self.assertTrue(result["shop_url"].endswith("/pulse/2026-08-31.html"))
