#!/usr/bin/env bash
# Cron helper: wake Cursor Agent on the VPS. heartbeat.sh + sell.sh call this.
# The wrapper never stubs `git` inside the agent process.
set -euo pipefail

pulse="${1:?pulse: heartbeat|sell}"
ROOT="${ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
export PATH="${HOME}/.local/bin:/usr/local/bin:/usr/bin:/bin:${PATH}"

resolve_agent() {
  if [[ -n "${CURSOR_AGENT_BIN:-}" && -x "${CURSOR_AGENT_BIN}" ]]; then
    printf '%s\n' "${CURSOR_AGENT_BIN}"
    return 0
  fi
  if [[ -n "${AGENT_BIN:-}" && -x "${AGENT_BIN}" ]]; then
    printf '%s\n' "${AGENT_BIN}"
    return 0
  fi
  local c
  for c in agent cursor-agent "${HOME}/.local/bin/agent" "${HOME}/.local/bin/cursor-agent"; do
    if [[ -x "$c" ]]; then
      printf '%s\n' "$c"
      return 0
    fi
    if command -v "$c" >/dev/null 2>&1; then
      command -v "$c"
      return 0
    fi
  done
  return 1
}

case "$pulse" in
  heartbeat) prompt_file="$ROOT/ceo/launch/prompts/heartbeat.txt" ;;
  sell) prompt_file="$ROOT/ceo/launch/prompts/sell.txt" ;;
  *)
    echo "run-cursor-agent: unknown pulse $pulse" >&2
    exit 2
    ;;
esac

AGENT_BIN="$(resolve_agent || true)"
if [[ -z "${AGENT_BIN}" ]]; then
  echo "PULSE_FAIL AGENT: missing (cursor-agent not on PATH)" >&2
  echo "AGENT_MISSING" >&2
  exit 1
fi
if [[ ! -f "$prompt_file" ]]; then
  echo "PULSE_FAIL AGENT_PROMPT_MISSING $prompt_file" >&2
  exit 1
fi

echo "AGENT: on pulse=$pulse bin=$AGENT_BIN workspace=$ROOT"
# -p = non-interactive log to journal. --trust --force = no TTY hang on cron.
if [[ -n "${CURSOR_AGENT_MODEL:-}" ]]; then
  "$AGENT_BIN" -p --trust --force --workspace "$ROOT" --model "${CURSOR_AGENT_MODEL}" "$(cat "$prompt_file")"
else
  "$AGENT_BIN" -p --trust --force --workspace "$ROOT" "$(cat "$prompt_file")"
fi
echo "AGENT_DONE pulse=$pulse"
