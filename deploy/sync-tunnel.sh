#!/usr/bin/env bash
# Copy the SSH gate pieces the ForceCommand actually runs.
# Repo stays canonical; /opt/cursor-agent-tunnel is what sshd execs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST=/opt/cursor-agent-tunnel
sudo mkdir -p "$DEST/scripts"
sudo cp -a "$ROOT/scripts/ssh_resume.py" "$DEST/ssh_resume.py"
sudo cp -a "$ROOT/scripts/ssh_resume.py" "$DEST/scripts/ssh_resume.py"
sudo cp -a "$ROOT/tunnel-gate.py" "$DEST/tunnel-gate.py"
sudo cp -a "$ROOT/run-agent.sh" "$DEST/run-agent.sh"
sudo cp -a "$ROOT/scripts/guest_identity_harden.py" "$DEST/guest_identity_harden.py"
sudo cp -a "$ROOT/tunnel/guest-AGENTS.md" "$DEST/guest-AGENTS.md"
echo "synced ssh_resume + tunnel-gate + run-agent + identity-hard → $DEST"
