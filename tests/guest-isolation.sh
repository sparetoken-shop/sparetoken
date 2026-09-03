#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
LAUNCHER="${ROOT}/run-agent.sh"
fail() {
  printf 'guest-isolation: FAIL: %s\n' "$*" >&2
  exit 1
}

require_literal() {
  local literal="$1"
  grep -Fq -- "$literal" "$LAUNCHER" ||
    fail "launcher is missing required literal: ${literal}"
}

forbid_literal() {
  local literal="$1"
  if grep -Fq -- "$literal" "$LAUNCHER"; then
    fail "launcher contains forbidden literal: ${literal}"
  fi
}

[[ -f "$LAUNCHER" ]] || fail "canonical launcher not found: ${LAUNCHER}"

# CI does not have the production host paths, bwrap privileges, or a live
# Cursor Agent. Verify the kernel-enforced namespace construction statically.
require_literal '--ro-bind / /'
require_literal '--tmpfs "${REAL_HOME}"'
require_literal '--dir "${REAL_HOME}/development"'
require_literal '--dir "${REAL_HOME}/development/guest-sessions"'
require_literal '--bind "${SESSION_DIR}" "${SESSION_DIR}"'
require_literal '--bind "${CURSOR_STATE}" "${REAL_HOME}/.cursor"'
require_literal '--chdir "${WORKSPACE}"'
require_literal '--setenv HOME "${REAL_HOME}"'

# The agent executable itself must be the bwrap child. A wrapper around only
# shell/exec would leave higher-level Read/Write/Edit operations unconfined.
# Launcher may split `-- \` and `"${AGENT_BIN}"` across lines.
require_literal '"${AGENT_BIN}"'
require_literal '--workspace "${WORKSPACE}"'
if ! awk '
  /--[[:space:]]*\\$/ { want=1; next }
  want && /"\$\{AGENT_BIN\}"/ { found=1; exit }
  want && NF { want=0 }
  END { exit found ? 0 : 1 }
' "$LAUNCHER"; then
  fail "launcher does not exec AGENT_BIN as the bwrap child"
fi

# Do not accidentally turn the older broad config mount back into the
# canonical launcher. Host Cursor auth is currently a documented residual
# risk and must not be expanded beyond the explicit current mount.
forbid_literal '--ro-bind "${REAL_HOME}/.config" "${REAL_HOME}/.config"'

printf 'guest-isolation: PASS (static bwrap launcher checks)\n'
