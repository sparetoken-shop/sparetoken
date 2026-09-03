"""Two official pulses: 11:30 sell, 23:30 ship. Both plant a D+8 task."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HB = (ROOT / "ceo" / "HEARTBEAT.md").read_text(encoding="utf-8")
HB_SH = (ROOT / "ceo" / "launch" / "heartbeat.sh").read_text(encoding="utf-8")
SELL = (ROOT / "ceo" / "launch" / "sell.sh").read_text(encoding="utf-8")
RUNNER = (ROOT / "ceo" / "launch" / "run-cursor-agent.sh").read_text(encoding="utf-8")
VENUES = (ROOT / "ceo" / "VENUES.md").read_text(encoding="utf-8")


class DualPulseTest(unittest.TestCase):
    def test_two_clocks_are_official(self):
        self.assertIn("11:30", HB)
        self.assertIn("23:30", HB)
        self.assertIn("venda", HB.lower())
        self.assertIn("produto", HB.lower())

    def test_morning_script_exists_and_forbids_git(self):
        self.assertIn("git is forbidden", SELL)
        self.assertIn("VENUES", SELL)

    def test_both_pulses_wake_cursor_agent(self):
        self.assertIn("run-cursor-agent.sh", HB_SH)
        self.assertIn("run-cursor-agent.sh", SELL)
        self.assertIn("AGENT: on", RUNNER)
        self.assertIn("-p", RUNNER)
        self.assertIn("--trust", RUNNER)
        self.assertIn("--force", RUNNER)
        self.assertNotIn("AGENT: off", HB_SH)
        self.assertNotIn("AGENT: off", SELL)
        self.assertTrue((ROOT / "ceo" / "launch" / "prompts" / "heartbeat.txt").is_file())
        self.assertTrue((ROOT / "ceo" / "launch" / "prompts" / "sell.txt").is_file())

    def test_both_scripts_must_fail_if_agent_dies(self):
        """PR #1 unique lock: no stamp-only pulse. Keep run-cursor-agent.sh."""
        for name, body in ("heartbeat.sh", HB_SH), ("sell.sh", SELL):
            with self.subTest(script=name):
                self.assertIn("run-cursor-agent.sh", body)
                self.assertIn("PULSE_FAIL", body)
                self.assertIn("AGENT_RC", body)
                self.assertNotIn("AGENT: off", body)
                self.assertIn("git is forbidden", body)
                lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("#")]
                fail_i = next(i for i, ln in enumerate(lines) if "PULSE_FAIL" in ln)
                ok_token = "PULSE_OK" if name.startswith("heartbeat") else "SELL_OK"
                ok_i = next(i for i, ln in enumerate(lines) if f'echo "{ok_token}' in ln)
                self.assertLess(fail_i, ok_i)

    def test_docs_forbid_agent_off_success(self):
        self.assertIn("cursor-agent", HB.lower())
        self.assertIn("pulso morto", HB.lower())
        self.assertIn("agent: off", HB.lower())
        self.assertIn("pulse_fail", HB.lower())

    def test_venues_are_not_x_replies(self):
        self.assertIn("utm_", VENUES.lower())
        self.assertNotIn("reply farm", VENUES.lower())
        self.assertIn("warmup", VENUES.lower())
