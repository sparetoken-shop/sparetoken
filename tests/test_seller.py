"""Seller apply: 10 conta.vc links, ack required, queue only — never live stock."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import seller


ROOT = Path(__file__).resolve().parents[1]
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "static" / "app.js").read_text(encoding="utf-8")


def _ten_links(handle: str = "oraculus") -> list[str]:
    return [
        f"https://app.conta.vc/pay/{handle}/c/Link{i:02d}AbcdEfghIjkl"
        for i in range(10)
    ]


def _ok_payload(**overrides) -> dict:
    body = {
        "handle": "oraculus",
        "links": "\n".join(_ten_links()),
        "note": "horas sobrando no fim de semana",
        "ack": True,
    }
    body.update(overrides)
    return body


class SellerValidateTest(unittest.TestCase):
    def test_ten_valid_links_and_ack_pass(self):
        clean = seller.validate(_ok_payload())
        self.assertEqual(clean["handle"], "oraculus")
        self.assertEqual(len(clean["links"]), 10)
        self.assertTrue(clean["ack"])
        self.assertTrue(all(u.startswith("https://app.conta.vc/pay/") for u in clean["links"]))

    def test_rejects_nine_links(self):
        with self.assertRaises(seller.SellerError) as ctx:
            seller.validate(_ok_payload(links="\n".join(_ten_links()[:9])))
        self.assertIn("10", str(ctx.exception))

    def test_rejects_bad_url(self):
        links = _ten_links()
        links[3] = "https://example.com/pay/nope"
        with self.assertRaises(seller.SellerError) as ctx:
            seller.validate(_ok_payload(links="\n".join(links)))
        self.assertIn("conta.vc", str(ctx.exception).lower())

    def test_rejects_http_and_receive_paths(self):
        links = _ten_links()
        links[0] = "http://app.conta.vc/pay/oraculus/c/Abcdefghijkl"
        with self.assertRaises(seller.SellerError):
            seller.validate(_ok_payload(links="\n".join(links)))
        links[0] = "https://app.conta.vc/receive/link/charge/new"
        with self.assertRaises(seller.SellerError):
            seller.validate(_ok_payload(links="\n".join(links)))

    def test_requires_ack(self):
        with self.assertRaises(seller.SellerError) as ctx:
            seller.validate(_ok_payload(ack=False))
        self.assertIn("termo", str(ctx.exception).lower())

    def test_rejects_at_and_phone_handles(self):
        with self.assertRaises(seller.SellerError):
            seller.validate(_ok_payload(handle="foo@bar"))
        with self.assertRaises(seller.SellerError):
            seller.validate(_ok_payload(handle="11999998888"))
        with self.assertRaises(seller.SellerError):
            seller.validate(_ok_payload(handle="fuzzy"))


class SellerStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.queue = self.root / "seller-applications"
        self.stock = self.root / "conta-links.txt"
        self.stock.write_text("https://app.conta.vc/pay/fuzzy/c/KeepMeSacred\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_apply_queues_json_and_leaves_stock_alone(self):
        result = seller.apply(self.queue, _ok_payload())
        self.assertTrue(result["ok"])
        files = list(self.queue.glob("*.json"))
        self.assertEqual(len(files), 1)
        stored = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(stored["handle"], "oraculus")
        self.assertEqual(len(stored["links"]), 10)
        self.assertEqual(
            self.stock.read_text(encoding="utf-8"),
            "https://app.conta.vc/pay/fuzzy/c/KeepMeSacred\n",
        )
        self.assertNotIn("conta-links", files[0].read_text(encoding="utf-8"))

    def test_apply_error_writes_nothing(self):
        with self.assertRaises(seller.SellerError):
            seller.apply(self.queue, _ok_payload(ack=False))
        self.assertEqual(list(self.queue.glob("*.json")), [])


class SellerSurfaceTest(unittest.TestCase):
    def test_api_route_is_wired(self):
        self.assertIn("/api/seller-apply", SERVER)
        self.assertIn("seller.apply", SERVER)
        self.assertIn("seller-applications", SERVER)

    def test_landing_cta_and_panel(self):
        self.assertIn("Venda seus tokens", HTML)
        self.assertIn('data-track="sell_click"', HTML)
        self.assertIn('id="vender"', HTML)
        self.assertIn("/api/seller-apply", JS)
        self.assertIn('ping("sell_click")', JS)
        self.assertNotIn("download app", HTML.lower())
        self.assertNotIn("baixe o app", HTML.lower())
