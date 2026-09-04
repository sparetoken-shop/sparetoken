"""Skill listing = short manifesto + CLI allowlist. Same R$5 SKU."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import marketplace

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")
FAQ = (ROOT / "FAQ.md").read_text(encoding="utf-8")
MARKET_SRC = (ROOT / "marketplace.py").read_text(encoding="utf-8")


def _ok(**overrides) -> dict:
    body = {
        "slug": "mkt",
        "title": "Post curto",
        "manifesto": "280 caracteres. R$5 / 5h. Sem cara. O mesmo Pix.",
        "clis": ["cursor"],
    }
    body.update(overrides)
    return body


class MarketplaceContractTest(unittest.TestCase):
    def test_allowlist_is_the_five_clis_already_on_the_table(self):
        self.assertEqual(
            marketplace.ALLOWED_CLIS,
            ("cursor", "codex", "claude", "antigravity", "metamuse"),
        )

    def test_sku_stays_five_reais_five_hours(self):
        self.assertEqual(marketplace.SKU_BRL, 5)
        self.assertEqual(marketplace.SKU_HOURS, 5)
        self.assertEqual(marketplace.PAYOUT_VIA, "pix")

    def test_live_brief_validates(self):
        clean = marketplace.validate_skill(_ok())
        self.assertEqual(clean["slug"], "mkt")
        self.assertEqual(clean["clis"], ["cursor"])
        self.assertEqual(clean["sku_brl"], 5)

    def test_rejects_unknown_cli(self):
        with self.assertRaises(marketplace.MarketError) as ctx:
            marketplace.validate_skill(_ok(clis=["openai"]))
        self.assertIn("allowlist", str(ctx.exception).lower())

    def test_rejects_empty_manifesto(self):
        with self.assertRaises(marketplace.MarketError) as ctx:
            marketplace.validate_skill(_ok(manifesto="  "))
        self.assertIn("manifesto", str(ctx.exception).lower())

    def test_rejects_second_price(self):
        with self.assertRaises(marketplace.MarketError) as ctx:
            marketplace.validate_skill(_ok(price=10))
        self.assertIn("r$5", str(ctx.exception).lower())

    def test_rejects_empty_clis(self):
        with self.assertRaises(marketplace.MarketError):
            marketplace.validate_skill(_ok(clis=[]))

    def test_public_contract_is_catalog_not_a_second_till(self):
        contract = marketplace.public_contract()
        self.assertEqual(contract["sku_brl"], 5)
        self.assertEqual(contract["payout_via"], "pix")
        self.assertEqual(list(contract["allowed_clis"]), list(marketplace.ALLOWED_CLIS))
        slugs = [s["slug"] for s in contract["skills"]]
        self.assertEqual(slugs, ["mkt", "copy", "viral"])
        for skill in contract["skills"]:
            self.assertEqual(skill["clis"], ["cursor"])
            self.assertTrue(skill["manifesto"])
        self.assertNotIn("pay_url", contract)
        self.assertNotIn("email", contract)


class MarketplaceSurfaceTest(unittest.TestCase):
    def test_api_route_is_wired(self):
        self.assertIn("import marketplace", SERVER)
        self.assertIn("/api/marketplace", SERVER)
        self.assertIn("marketplace.public_contract", SERVER)

    def test_landing_states_manifesto_and_cli_allowlist(self):
        blob = HTML.lower()
        self.assertIn("manifesto curto", blob)
        self.assertIn("cursor", blob)
        self.assertIn("codex", blob)
        self.assertIn("claude", blob)
        self.assertIn("antigravity", blob)
        self.assertIn("metamuse", blob)
        self.assertIn('data-cli="cursor"', HTML)
        self.assertNotIn("r$10", blob)

    def test_faq_names_the_contract(self):
        blob = FAQ.lower()
        self.assertIn("allowlist", blob)
        self.assertIn("codex", blob)
        self.assertIn("r$5", blob)

    def test_module_does_not_import_pay(self):
        self.assertNotIn("import pay", MARKET_SRC)
        self.assertNotIn("from pay", MARKET_SRC)
