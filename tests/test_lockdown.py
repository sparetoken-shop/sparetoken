"""Lockdown 2026-09-30: SSH/CLI resale is off. Do not remove without owner sign-off."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "static" / "app.js").read_text(encoding="utf-8")


class LockdownTest(unittest.TestCase):
    def test_kill_switch_defaults_on(self):
        self.assertIn('LOCKED = os.environ.get("SPARETOKEN_LOCKED", "1") != "0"', SERVER)

    def test_pay_and_claim_are_gated(self):
        for route in ('if path == "/api/pay":', 'if path == "/api/claim":'):
            idx = SERVER.find(route)
            self.assertGreater(idx, 0)
            self.assertIn("if LOCKED:", SERVER[idx: idx + 200])
            self.assertIn("410", SERVER[idx: idx + 300])

    def test_health_does_not_advertise_ssh(self):
        idx = SERVER.find('if path in {"/api/health", "/health"}:')
        self.assertNotIn('"ssh"', SERVER[idx: idx + 400])

    def test_landing_has_no_guest_ssh_or_pix(self):
        self.assertIn('href="/lockdown.css"', HTML)
        css = (ROOT / "static" / "lockdown.css").read_text(encoding="utf-8")
        for sel in ("#pay", "#claim", "#pay-modal", "#terminal", ".sell-ssh"):
            self.assertIn(sel, css)
        self.assertIn('id="lockdown-banner"', HTML)
        self.assertNotIn("agent-guest@", HTML)
        self.assertNotIn("agent-guest@", JS)
        self.assertNotIn("conta.vc/pay/fuzzy/c/", HTML)


if __name__ == "__main__":
    unittest.main()
