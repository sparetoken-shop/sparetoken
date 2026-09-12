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
