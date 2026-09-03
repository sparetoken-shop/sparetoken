"""Z-API helper talks only via env; tests never hit the network."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from zapi_notify import notify_all, phones_from_env, send_text  # noqa: E402


class ZapiNotifyTest(unittest.TestCase):
    def test_phones_split_and_digits_only(self):
        self.assertEqual(
            phones_from_env("55 41 90000-0001, 5541900000002"),
            ["5541900000001", "5541900000002"],
        )

    def test_send_text_requires_env(self):
        ok, reason = send_text("5541900000001", "hi", url="", token="")
        self.assertFalse(ok)
        self.assertIn("required", reason)

    def test_send_text_posts_json_with_client_token(self):
        seen = {}

        def post(url, data, headers):
            seen["url"] = url
            seen["data"] = data
            seen["headers"] = headers
            return 200, '{"id":"ok"}'

        ok, _ = send_text(
            "5541900000001",
            "captcha 15 min",
            url="https://example.invalid/send-text",
            token="test-token",
            post=post,
        )
        self.assertTrue(ok)
        self.assertEqual(seen["headers"]["Client-Token"], "test-token")
        self.assertIn(b"5541900000001", seen["data"])
        self.assertIn(b"captcha", seen["data"])

    def test_notify_all_uses_env_phones(self):
        calls = []

        def post(url, data, headers):
            calls.append(data)
            return 200, "{}"

        import os

        old = os.environ.get("ZAPI_NOTIFY_PHONES")
        os.environ["ZAPI_NOTIFY_PHONES"] = "5541900000001,5541900000002"
        os.environ["ZAPI_SEND_TEXT_URL"] = "https://example.invalid/send-text"
        os.environ["ZAPI_CLIENT_TOKEN"] = "test-token"
        try:
            ok_n, total = notify_all("vnc link", post=post)
        finally:
            if old is None:
                os.environ.pop("ZAPI_NOTIFY_PHONES", None)
            else:
                os.environ["ZAPI_NOTIFY_PHONES"] = old
        self.assertEqual((ok_n, total), (2, 2))
        self.assertEqual(len(calls), 2)
