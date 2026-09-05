"""GET /api/heartbeat is a public pulse stub — not a second till."""

from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import heartbeat_api

SERVER = (ROOT / "server.py").read_text(encoding="utf-8")
SRC = (ROOT / "heartbeat_api.py").read_text(encoding="utf-8")


def _fixture(tmp: Path) -> Path:
    (tmp / "VERSION").write_text("0.2.26\n", encoding="utf-8")
    (tmp / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        "## [Unreleased]\n\n"
        "## [0.2.26] — 2026-09-04\n\n"
        "Public pulse stub. Last ship, 7-day, last research.\n\n"
        "### Added\n\n"
        "- GET /api/heartbeat\n",
        encoding="utf-8",
    )
    ceo = tmp / "ceo"
    ceo.mkdir()
    (ceo / "ROADMAP-7D.md").write_text(
        "| Dia | Âncora | **Ship obrigatório hoje** | Pesquisa do pulso | Plantado no D+7 |\n"
        "|---|---|---|---|---|\n"
        "| D4b | 04/09 | Loja internacional — **SHIP 0.2.24** | inglês | D12 |\n"
        "| D5 | 05/09 | `/api/heartbeat` stub — **SHIP 0.2.26** | HTTP 402 / x402 — só nota | Heartbeat na landing |\n"
        "| D6 | 06/09 | restock | idle GPU | sweep |\n",
        encoding="utf-8",
    )
    (ceo / "RESEARCH.md").write_text(
        "# Inteligência\n\n"
        "## Tese que não se larga\n\n"
        "Pay-per-use.\n\n"
        "## 2026-09-03 23:30 (produto D4)\n\n"
        "viu: Gate402 old line.\n\n"
        "## 2026-09-04 23:30 (heartbeat D5)\n\n"
        "viu: Artemis/SolanaFloor em 03/09 — Solana >90% do x402 na semana que fechou 31/08.\n\n"
        "não copiar: HTTP 402 no lugar do Pix.\n\n"
        "## Template de pulso\n\n"
        "```\nviu:\n```\n",
        encoding="utf-8",
    )
    return tmp


class HeartbeatParseTest(unittest.TestCase):
    def test_last_ship_reads_current_version_title(self):
        with tempfile.TemporaryDirectory() as raw:
            root = _fixture(Path(raw))
            ship = heartbeat_api.last_ship(root)
            self.assertEqual(ship["version"], "0.2.26")
            self.assertEqual(ship["date"], "2026-09-04")
            self.assertIn("pulse stub", ship["title"].lower())

    def test_seven_day_prefers_the_row_that_names_this_version(self):
        with tempfile.TemporaryDirectory() as raw:
            root = _fixture(Path(raw))
            row = heartbeat_api.seven_day(root, today=date(2026, 9, 4))
            self.assertEqual(row["day"], "D5")
            self.assertEqual(row["anchor"], "05/09")
            self.assertIn("0.2.26", row["ship"])
            self.assertIn("x402", row["research"])

    def test_seven_day_falls_to_today_when_version_is_not_on_the_table(self):
        with tempfile.TemporaryDirectory() as raw:
            root = _fixture(Path(raw))
            (root / "VERSION").write_text("0.2.99\n", encoding="utf-8")
            row = heartbeat_api.seven_day(root, today=date(2026, 9, 4))
            self.assertEqual(row["day"], "D4b")

    def test_last_research_skips_template_and_scratch(self):
        with tempfile.TemporaryDirectory() as raw:
            root = _fixture(Path(raw))
            note = heartbeat_api.last_research(root)
            self.assertTrue(note["when"].startswith("2026-09-04"))
            self.assertTrue(note["line"].startswith("viu:"))
            self.assertIn("Solana", note["line"])
            self.assertNotIn("template", note["when"].lower())


class HeartbeatContractTest(unittest.TestCase):
    def test_sku_stays_five_reais_five_hours(self):
        self.assertEqual(heartbeat_api.SKU_BRL, 5)
        self.assertEqual(heartbeat_api.SKU_HOURS, 5)

    def test_live_pulse_matches_repo_version(self):
        pulse = heartbeat_api.public_pulse(ROOT)
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(pulse["version"], version)
        self.assertEqual(pulse["sku_brl"], 5)
        self.assertEqual(pulse["last_ship"]["version"], version)
        self.assertTrue(pulse["last_ship"]["title"])
        self.assertIn(version, pulse["seven_day"]["ship"])
        self.assertTrue(pulse["last_research"]["line"])
        self.assertNotIn("pay_url", pulse)
        self.assertNotIn("email", pulse)
        blob = str(pulse).lower()
        self.assertNotIn("r$10", blob)
        self.assertNotIn("second till", blob)

    def test_module_does_not_import_pay(self):
        self.assertNotIn("import pay", SRC)
        self.assertNotIn("from pay", SRC)


class HeartbeatSurfaceTest(unittest.TestCase):
    def test_api_route_is_wired(self):
        self.assertIn("import heartbeat_api", SERVER)
        self.assertIn("/api/heartbeat", SERVER)
        self.assertIn("heartbeat_api.public_pulse", SERVER)
        health = SERVER.index('path in {"/api/health", "/health"}')
        pulse = SERVER.index('path == "/api/heartbeat"')
        self.assertLess(health, pulse)


if __name__ == "__main__":
    unittest.main()
