"""Human-needed notify + OSS captcha assist. No paid solver. No ollama pull."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import human_needed as hn  # noqa: E402

TZ = ZoneInfo("America/Sao_Paulo")
FIXED = datetime(2026, 9, 2, 18, 40, tzinfo=TZ)

QUEUE_SAMPLE = """# Fila

| id | pulso | canal | texto / destino | status |
|---|---|---|---|---|
| s001 | 11:30 01/09 | leftoverpzero DEV.to | captcha no VNC | **killed 02/09** |
| s002 | 11:30 02/09 | Indie Hackers | **humano no Mac:** Google signup (login wall). UTM `s0902`. | **human-needed** |
| p010 | 23:30 01/09 | X (warmup) | copy | a colar no Mac |
"""


class HumanNeededTest(unittest.TestCase):
    def test_scan_skips_killed_keeps_google_wall(self):
        rows = hn.scan_queue_rows(QUEUE_SAMPLE)
        self.assertEqual([r["id"] for r in rows], ["s002"])
        self.assertEqual(hn._reason_from_row(rows[0]), "google_login_wall")

    def test_stamp_queue_and_progress_are_durable(self):
        q = hn.stamp_queue(QUEUE_SAMPLE, hn.scan_queue_rows(QUEUE_SAMPLE), now=FIXED)
        self.assertIn(hn.DURABLE_HEADING, q)
        self.assertIn("| 2026-09-02 | s002 |", q)
        self.assertIn("google_login_wall", q)
        self.assertIn("C0BSDQDMZ71", q)
        self.assertIn("1788232177.124409", q)
        p = hn.stamp_progress("# Progresso\n", hn.scan_queue_rows(QUEUE_SAMPLE), now=FIXED)
        self.assertIn("## 2026-09-02 (human-needed notify)", p)
        twice = hn.stamp_progress(p, hn.scan_queue_rows(QUEUE_SAMPLE), now=FIXED)
        self.assertEqual(p.count("## 2026-09-02 (human-needed notify)"), 1)
        self.assertEqual(twice, p)

    def test_persist_writes_alert_json_and_skips_slack_without_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ceo").mkdir()
            (root / "ceo" / "QUEUE.md").write_text(QUEUE_SAMPLE, encoding="utf-8")
            (root / "ceo" / "PROGRESS.md").write_text("# Progresso\n", encoding="utf-8")
            out = hn.persist(root, pulse="sell", now=FIXED, env={}, slack=True)
            self.assertTrue(out["ok"])
            alert = json.loads((root / "data" / "human-needed-alert.json").read_text(encoding="utf-8"))
            self.assertEqual(alert["slack"]["channel"], "C0BSDQDMZ71")
            self.assertEqual(alert["slack"]["thread_ts"], "1788232177.124409")
            self.assertEqual(alert["items"][0]["id"], "s002")
            self.assertTrue(out["slack"]["skipped"])
            q = (root / "ceo" / "QUEUE.md").read_text(encoding="utf-8")
            self.assertIn(hn.DURABLE_HEADING, q)
            self.assertIn("s002", (root / "ceo" / "PROGRESS.md").read_text(encoding="utf-8"))

    def test_slack_posts_only_when_webhook_env_exists(self):
        payload = hn.build_alert(
            [{"id": "s002", "pulse": "sell", "channel": "Indie Hackers", "reason": "google_login_wall", "note": "", "status": "human-needed"}],
            pulse="sell",
            now=FIXED,
        )
        captured: dict = {}

        class FakeResp(io.BytesIO):
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def opener(req, timeout=8):
            captured["url"] = req.full_url
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResp(b"ok")

        skipped = hn.notify_slack(payload, env={})
        self.assertTrue(skipped["skipped"])
        sent = hn.notify_slack(payload, env={"SLACK_WEBHOOK_URL": "https://hooks.example.test/hook"}, opener=opener)
        self.assertTrue(sent["ok"])
        self.assertEqual(captured["url"], "https://hooks.example.test/hook")
        self.assertEqual(captured["body"]["channel"], "C0BSDQDMZ71")
        self.assertEqual(captured["body"]["thread_ts"], "1788232177.124409")
        self.assertIn("s002", captured["body"]["text"])

    def test_assist_soft_fails_without_image_and_never_pulls(self):
        out = hn.assist_captcha(None)
        self.assertFalse(out["ok"])
        self.assertEqual(out["soft_fail"], "human-needed-notify")
        src = Path(hn.__file__).read_text(encoding="utf-8")
        self.assertNotIn('["ollama", "pull"]', src)
        self.assertNotIn('[exe, "pull"]', src)
        for brand in hn.PAID_SOLVERS_FORBIDDEN:
            self.assertIn(brand, src)
            self.assertNotIn(f"{brand}.com", src)
            self.assertNotIn(f"api.{brand}", src.lower())

    def test_cached_ollama_vision_uses_list_only(self):
        calls: list[list[str]] = []

        class Result:
            stdout = "NAME\nllava:latest    4GB\nllama3.2    2GB\n"
            returncode = 0

        def runner(cmd, **kwargs):
            calls.append(cmd)
            return Result()

        models = hn.cached_ollama_vision_models(runner=runner)
        self.assertEqual(models, ["llava:latest"])
        self.assertTrue(calls)
        self.assertEqual(calls[0][1], "list")
        self.assertNotIn("pull", " ".join(calls[0]))

    def test_tesseract_success_short_circuits_assist(self):
        with tempfile.TemporaryDirectory() as tmp:
            img = Path(tmp) / "c.png"
            img.write_bytes(b"fake")

            class Result:
                stdout = "QK3P\n"
                returncode = 0

            def runner(cmd, **kwargs):
                self.assertEqual(cmd[0], "tesseract")
                self.assertNotIn("pull", cmd)
                return Result()

            orig = hn.tesseract_bin
            hn.tesseract_bin = lambda: "tesseract"
            try:
                out = hn.assist_captcha(img, runner=runner, env={})
            finally:
                hn.tesseract_bin = orig
            self.assertTrue(out["ok"])
            self.assertEqual(out["text"], "QK3P")
            self.assertEqual(out["method"], "tesseract")

    def test_reason_rejects_unknown(self):
        with self.assertRaises(ValueError):
            hn.normalize_reason("paid-solver")


class PulseWiringTest(unittest.TestCase):
    def test_wrappers_and_prompts_call_the_helper(self):
        sell = (ROOT / "ceo" / "launch" / "sell.sh").read_text(encoding="utf-8")
        hb = (ROOT / "ceo" / "launch" / "heartbeat.sh").read_text(encoding="utf-8")
        sell_p = (ROOT / "ceo" / "launch" / "prompts" / "sell.txt").read_text(encoding="utf-8")
        hb_p = (ROOT / "ceo" / "launch" / "prompts" / "heartbeat.txt").read_text(encoding="utf-8")
        heart = (ROOT / "ceo" / "HEARTBEAT.md").read_text(encoding="utf-8")
        queue = (ROOT / "ceo" / "QUEUE.md").read_text(encoding="utf-8")
        for blob in (sell, hb):
            self.assertIn("human_needed.py", blob)
            self.assertIn("pulse-hook", blob)
        for blob in (sell_p, hb_p, heart):
            self.assertIn("human_needed.py", blob)
            self.assertIn("C0BSDQDMZ71", blob)
        self.assertIn("s002", queue)
        self.assertIn("human-needed", queue.lower())
        self.assertIn("1788232177.124409", heart)
        self.assertNotRegex(sell + hb + sell_p + hb_p, r"\bollama pull\b")


if __name__ == "__main__":
    unittest.main()
