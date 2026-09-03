"""Referral schema: fuzzy first, 10%, Pix at R$5. No second till."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import referral

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


class ReferralSchemaTest(unittest.TestCase):
    def test_fuzzy_is_the_first_indicator(self):
        self.assertEqual(referral.FIRST_INDICATOR, "fuzzy")
        self.assertEqual(referral.indicator_for(None, paid_referrals=0), "fuzzy")
        self.assertEqual(referral.indicator_for("wdtsot-7K2M", paid_referrals=0), "fuzzy")

    def test_wallet_becomes_indicator_only_after_first_paid_close(self):
        self.assertEqual(referral.indicator_for("wdtsot-7K2M", paid_referrals=1), "wdtsot-7K2M")
        self.assertEqual(referral.indicator_for("amigo@mail.com", paid_referrals=9), "fuzzy")

    def test_ten_percent_is_fifty_cents_on_the_five_real_sku(self):
        self.assertEqual(referral.SKU_CENTS, 500)
        self.assertEqual(referral.RATE_BPS, 1000)
        self.assertEqual(referral.COMMISSION_CENTS, 50)
        self.assertEqual(referral.commission_cents(1), 50)
        self.assertEqual(referral.commission_cents(10), 500)

    def test_pix_opens_at_five_reais_ten_paid_friends(self):
        self.assertEqual(referral.PAYOUT_CENTS, 500)
        self.assertEqual(referral.PAYOUT_VIA, "pix")
        self.assertEqual(referral.FRIENDS_TO_PAYOUT, 10)
        self.assertFalse(referral.can_choose_pix(referral.commission_cents(9)))
        self.assertTrue(referral.can_choose_pix(referral.commission_cents(10)))
        self.assertEqual(referral.friends_until_pix(0), 10)
        self.assertEqual(referral.friends_until_pix(3), 7)
        self.assertEqual(referral.friends_until_pix(10), 0)

    def test_click_and_open_charge_do_not_accrue(self):
        self.assertFalse(referral.accrues("open"))
        self.assertFalse(referral.accrues("pending"))
        self.assertFalse(referral.accrues("click"))
        self.assertTrue(referral.accrues("paid"))
        self.assertTrue(referral.accrues("closed"))

    def test_self_referral_and_missing_buyer_do_not_accrue(self):
        self.assertFalse(referral.should_accrue("wdtsot-7K2M", "wdtsot-7K2M", "paid"))
        self.assertFalse(referral.should_accrue("fuzzy", None, "paid"))
        self.assertTrue(referral.should_accrue("fuzzy", "wdtsot-7K2M", "paid"))
        self.assertTrue(referral.should_accrue("wdtsot-AAAA", "wdtsot-7K2M", "closed"))

    def test_public_schema_is_the_shelf_contract(self):
        schema = referral.public_schema()
        self.assertEqual(schema["first_indicator"], "fuzzy")
        self.assertEqual(schema["rate"], "0.10")
        self.assertEqual(schema["commission_brl"], "0.50")
        self.assertEqual(schema["payout_brl"], "5.00")
        self.assertEqual(schema["payout_via"], "pix")
        self.assertEqual(schema["friends_to_payout"], 10)
        self.assertNotIn("email", schema)
        self.assertNotIn("whatsapp", schema)


class ReferralSurfaceTest(unittest.TestCase):
    def test_landing_states_pix_at_five_and_fuzzy_first(self):
        blob = HTML.lower()
        self.assertIn("pix aos r$5", blob)
        self.assertIn("primeiro indicador", blob)
        self.assertIn("fuzzy", blob)
        self.assertNotIn("cupom", blob)

    def test_session_exposes_the_schema_not_a_second_checkout(self):
        src = (ROOT / "referral.py").read_text(encoding="utf-8")
        self.assertIn("import referral", SERVER)
        self.assertIn("referral.public_schema()", SERVER)
        self.assertNotIn("import pay", src)
        self.assertNotIn("conta.vc", src)
