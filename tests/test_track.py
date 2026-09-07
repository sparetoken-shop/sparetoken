"""First-party visit / pay / claim / sell + engage — no PII, no pixel."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db import connect
from track import ALLOWED_EVENTS, FUNNEL_EVENTS, record_event, sanitize_payload, summarize


class TrackSanitizeTest(unittest.TestCase):
    def test_keeps_known_event_and_short_utms(self):
        clean = sanitize_payload(
            {
                "event": "visit",
                "utm_source": "x",
                "utm_medium": "social",
                "utm_campaign": "heartbeat",
                "utm_content": "p004",
                "code": "wdtsot-7K2M",
                "email": "nope@example.com",
                "contact": "11999990000",
            }
        )
        self.assertEqual(clean["event"], "visit")
        self.assertEqual(clean["utm_source"], "x")
        self.assertEqual(clean["utm_content"], "p004")
        self.assertEqual(clean["code"], "wdtsot-7K2M")
        self.assertNotIn("email", clean)
        self.assertNotIn("contact", clean)

    def test_drops_unknown_event_and_garbage_code(self):
        clean = sanitize_payload({"event": "hack", "code": "DROP TABLE", "utm_source": "x" * 200})
        self.assertIsNone(clean)

    def test_allowed_events_include_engage_family(self):
        self.assertEqual(
            ALLOWED_EVENTS,
            frozenset(
                {
                    "visit",
                    "pay_click",
                    "claim_ok",
                    "sell_click",
                    "ui_click",
                    "engage_tick",
                    "page_leave",
                    "scroll_depth",
                }
            ),
        )
        self.assertEqual(FUNNEL_EVENTS, ("visit", "pay_click", "claim_ok", "sell_click"))

    def test_sanitizes_label_sid_ms_depth(self):
        clean = sanitize_payload(
            {
                "event": "ui_click",
                "label": "hero-try",
                "sid": "sabcdef12xyz99",
                "ms": 15000,
                "depth": 50,
                "email": "x@y.z",
            }
        )
        self.assertEqual(clean["label"], "hero-try")
        self.assertEqual(clean["sid"], "sabcdef12xyz99")
        self.assertEqual(clean["ms"], 15000)
        self.assertEqual(clean["depth"], 50)
        self.assertNotIn("email", clean)

    def test_rejects_bad_sid_label_and_scroll_depth(self):
        self.assertNotIn("sid", sanitize_payload({"event": "visit", "sid": "short"}))
        self.assertNotIn("label", sanitize_payload({"event": "ui_click", "label": "bad label!"}))
        bad_depth = sanitize_payload({"event": "scroll_depth", "depth": 33})
        self.assertNotIn("depth", bad_depth)
        ok = sanitize_payload({"event": "scroll_depth", "depth": 75})
        self.assertEqual(ok["depth"], 75)


class TrackDbTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "t.sqlite")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_record_visit_then_count(self):
        ok = record_event(
            self.conn,
            {"event": "visit", "utm_source": "x", "utm_content": "p004"},
        )
        self.assertTrue(ok)
        n = self.conn.execute("SELECT COUNT(*) FROM track_events").fetchone()[0]
        self.assertEqual(n, 1)
        row = self.conn.execute(
            "SELECT event, utm_source, utm_content, code FROM track_events"
        ).fetchone()
        self.assertEqual(tuple(row), ("visit", "x", "p004", None))

    def test_refuse_pii_payload(self):
        ok = record_event(self.conn, {"event": "visit", "contact": "hi@x.com"})
        self.assertTrue(ok)
        stored = dict(self.conn.execute("SELECT * FROM track_events").fetchone())
        self.assertNotIn("hi@x.com", str(stored))

    def test_summarize_is_counts_only_no_code_no_utm(self):
        record_event(self.conn, {"event": "visit", "utm_source": "x", "utm_content": "p004", "code": "wdtsot-7K2M"})
        record_event(self.conn, {"event": "visit", "utm_source": "x", "utm_content": "p006"})
        record_event(self.conn, {"event": "pay_click"})
        record_event(self.conn, {"event": "ui_click", "label": "hero-try", "sid": "sabcdef12xyz99"})
        record_event(self.conn, {"event": "engage_tick", "ms": 15000, "sid": "sabcdef12xyz99"})
        record_event(self.conn, {"event": "scroll_depth", "depth": 50, "sid": "sabcdef12xyz99"})
        tallies = summarize(self.conn)
        self.assertEqual(tallies, {"visit": 2, "pay_click": 1, "claim_ok": 0, "sell_click": 0})
        self.assertEqual(set(tallies), {"visit", "pay_click", "claim_ok", "sell_click"})
        blob = str(tallies)
        self.assertNotIn("wdtsot-", blob)
        self.assertNotIn("p004", blob)
        self.assertNotIn("@", blob)
        self.assertNotIn("hero-try", blob)

    def test_migrate_adds_engage_columns(self):
        cols = {row[1] for row in self.conn.execute("PRAGMA table_info(track_events)")}
        for col in ("label", "sid", "ms", "depth"):
            self.assertIn(col, cols)
        ok = record_event(
            self.conn,
            {
                "event": "page_leave",
                "sid": "sabcdef12xyz99",
                "ms": 42000,
                "label": "n/a-skip",  # label with slash rejected
            },
        )
        self.assertTrue(ok)
        row = dict(self.conn.execute("SELECT event, sid, ms, label FROM track_events").fetchone())
        self.assertEqual(row["event"], "page_leave")
        self.assertEqual(row["sid"], "sabcdef12xyz99")
        self.assertEqual(row["ms"], 42000)
        self.assertIsNone(row["label"])


if __name__ == "__main__":
    unittest.main()
