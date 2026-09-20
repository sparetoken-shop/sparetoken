"""The PULSE_FAIL lock is runtime, not grep. D12 11/09.

Wrappers stamp PULSE_FAIL when run-cursor-agent.sh dies (PR #1 unique
lock, no re-merge of the diverged tip). This test executes the runner
for real: missing agent binary must exit non-zero with PULSE_FAIL.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ceo" / "launch" / "run-cursor-agent.sh"


def _run(args: list[str], extra_env: dict[str, str]):
    env = dict(os.environ)
    env.update(extra_env)
    return subprocess.run(
        ["/bin/bash", str(RUNNER), *args],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )


def _no_agent_env(empty: Path) -> dict[str, str]:
    # resolve_agent checks CURSOR_AGENT_BIN, AGENT_BIN, then PATH + HOME.
    gone = str(empty / "no-agent-here")
    return {
        "CURSOR_AGENT_BIN": gone,
        "AGENT_BIN": gone,
        "PATH": str(empty),
        "HOME": str(empty),
    }


class PulseAgentTrapTest(unittest.TestCase):
    def test_missing_agent_fails_with_pulse_fail(self):
        with tempfile.TemporaryDirectory() as td:
            proc = _run(["heartbeat"], _no_agent_env(Path(td)))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("PULSE_FAIL", proc.stdout + proc.stderr)

    def test_missing_agent_fails_on_sell_too(self):
        with tempfile.TemporaryDirectory() as td:
            proc = _run(["sell"], _no_agent_env(Path(td)))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("PULSE_FAIL", proc.stdout + proc.stderr)

    def test_unknown_pulse_exits_2(self):
        proc = _run(["nope"], {})
        self.assertEqual(proc.returncode, 2)


class PulseChapterClosedTest(unittest.TestCase):
    """D21 19/09: trap stayed green, timer 7200s alive. PR #1 chapter closes.

    Unreleased stays Planned-only. No re-merge of the diverged tip.
    The public pulse only paints when the runtime trap lock is present.
    """

    def test_unreleased_is_planned_only(self):
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        start = text.find("## [Unreleased]")
        self.assertGreater(start, -1)
        nxt = text.find("\n## [", start + 1)
        section = text[start:nxt]
        self.assertIn("### Planned", section)
        self.assertNotIn("### Added", section)
        self.assertNotIn("### Changed", section)
        self.assertNotIn("re-merge", section.lower())
        self.assertNotIn("PR #1", section)

    def test_pulse_units_timeout_is_7200(self):
        for name in ("sparetoken-heartbeat.service", "sparetoken-sell.service"):
            body = (ROOT / "ceo" / "launch" / "units" / name).read_text(encoding="utf-8")
            self.assertIn("TimeoutStartSec=7200", body)

    def test_landing_pulse_carries_runtime_trap_lock(self):
        html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
        js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
        pulse = html.find('id="pulso-heartbeat"')
        tag_open = html.rfind("<p", 0, pulse)
        tag_end = html.find(">", pulse)
        self.assertIn('data-trap="runtime"', html[tag_open:tag_end])
        fn = js.split("function fillPulse", 1)[1].split("fetch(", 1)[0]
        self.assertIn("data-trap", fn)
        self.assertIn("runtime", fn)
