"""Public Open count — never a pay URL, never a second till."""

from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import shelf
from db import connect, upsert_pay_link, consume_pay_link

SRC = (ROOT / "shelf.py").read_text(encoding="utf-8")
URL_A = "https://app.conta.vc/pay/fuzzy/c/SHELFAAA111open"
URL_B = "https://app.conta.vc/pay/fuzzy/c/SHELFBBB222open"
URL_C = "https://app.conta.vc/pay/fuzzy/c/SHELFCCC333open"


class ShelfCountTest(unittest.TestCase):
    def test_file_counts_unique_open_lines_without_returning_urls(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            data = root / "data"
            data.mkdir()
            (data / "conta-links.txt").write_text(
                f"# stock\n{URL_A}\n{URL_B}\n{URL_C}\n",
                encoding="utf-8",
            )
            out = shelf.public_shelf(root)
            self.assertEqual(out["open"], 3)
            self.assertFalse(out["restock"])
            self.assertEqual(out["sku_brl"], 5)
            self.assertEqual(out["sku_hours"], 5)
            blob = str(out)
            self.assertNotIn("conta.vc", blob)
            self.assertNotIn("SHELF", blob)
            self.assertNotIn("pay/fuzzy", blob)

    def test_sqlite_wins_and_drops_consumed(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            data = root / "data"
            data.mkdir()
            (data / "conta-links.txt").write_text(f"{URL_A}\n{URL_B}\n", encoding="utf-8")
            db = data / "wdtsot.sqlite"
            conn = connect(db)
            upsert_pay_link(conn, URL_A)
            upsert_pay_link(conn, URL_B)
            consume_pay_link(conn, URL_A)
            conn.close()
            out = shelf.public_shelf(root)
            self.assertEqual(out["open"], 1)
            self.assertTrue(out["restock"])
            self.assertNotIn("conta.vc", str(out))

    def test_missing_stock_is_unknown_not_zero_theatre(self):
        with tempfile.TemporaryDirectory() as raw:
            out = shelf.public_shelf(Path(raw))
            self.assertIsNone(out["open"])
            self.assertFalse(out["restock"])
            self.assertEqual(shelf.shelf_display(out), "")

    def test_empty_file_is_zero_and_asks_restock(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            data = root / "data"
            data.mkdir()
            (data / "conta-links.txt").write_text("# none\n", encoding="utf-8")
            out = shelf.public_shelf(root)
            self.assertEqual(out["open"], 0)
            self.assertTrue(out["restock"])
            self.assertEqual(shelf.shelf_display(out), "0 Open · restock")

    def test_display_hides_restock_at_three(self):
        self.assertEqual(
            shelf.shelf_display({"open": 3, "restock": False}),
            "3 Open",
        )
        self.assertEqual(
            shelf.shelf_display({"open": 2, "restock": True}),
            "2 Open · restock",
        )

    def test_module_does_not_import_pay(self):
        self.assertNotIn("import pay", SRC)
        self.assertNotIn("from pay", SRC)
        self.assertNotIn("FALLBACK_PAY_URL", SRC)

    def test_corrupt_sqlite_falls_to_file(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            data = root / "data"
            data.mkdir()
            db = data / "wdtsot.sqlite"
            con = sqlite3.connect(db)
            con.execute("CREATE TABLE pay_links (nope TEXT)")
            con.commit()
            con.close()
            (data / "conta-links.txt").write_text(f"{URL_A}\n", encoding="utf-8")
            out = shelf.public_shelf(root)
            self.assertEqual(out["open"], 1)
            self.assertTrue(out["restock"])


if __name__ == "__main__":
    unittest.main()
