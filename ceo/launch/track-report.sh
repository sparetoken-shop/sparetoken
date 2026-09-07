#!/usr/bin/env bash
# Read-only UTM / click report. No PII dump.
set -euo pipefail
export TZ=America/Sao_Paulo
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

pick_db() {
  local candidate counts
  local -a candidates=()
  if [[ -n "${WDTSOT_DB:-}" ]]; then
    candidates+=("$WDTSOT_DB")
  fi
  if [[ -n "${WDTSOT_DATA:-}" ]]; then
    candidates+=("${WDTSOT_DATA%/}/wdtsot.sqlite")
  fi
  candidates+=(
    "$ROOT/data/wdtsot.sqlite"
    "$ROOT/wdtsot.sqlite"
    "/home/ubuntu/development/guest-sessions/session-20260829-212831-83c1eb/workspace/wdtsot/data/wdtsot.sqlite"
    "/home/ubuntu/development/guest-sessions/session-20260829-212831-83c1eb/workspace/wdtsot/wdtsot.sqlite"
  )
  local best="" best_n=-1
  for candidate in "${candidates[@]}"; do
    [[ -f "$candidate" ]] || continue
    counts="$(sqlite3 -readonly "$candidate" "SELECT COUNT(*) FROM track_events;" 2>/dev/null || echo 0)"
    counts="${counts:-0}"
    if [[ "$counts" =~ ^[0-9]+$ ]] && (( counts > best_n )); then
      best="$candidate"
      best_n="$counts"
    fi
  done
  if [[ -n "$best" ]]; then
    printf '%s\n' "$best"
    return 0
  fi
  return 1
}

echo "=== track-report $(date +%Y-%m-%dT%H:%M:%S%z) ==="
if ! DB="$(pick_db)"; then
  echo "no sqlite with track_events here. set WDTSOT_DB (or WDTSOT_DATA) on the VPS."
  exit 0
fi
echo "db: $DB"
cols="$(sqlite3 -readonly "$DB" "PRAGMA table_info(track_events);" | awk -F'|' '{print $2}')"
if echo "$cols" | grep -qx label; then
  sqlite3 -readonly "$DB" <<'SQL'
SELECT IFNULL(event,'?'), IFNULL(utm_source,'-'), IFNULL(utm_content,'-'), IFNULL(label,'-'), COUNT(*)
FROM track_events
GROUP BY 1, 2, 3, 4
ORDER BY 5 DESC
LIMIT 30;
SELECT event, COUNT(*) FROM track_events GROUP BY 1 ORDER BY 2 DESC;
SQL
else
  sqlite3 -readonly "$DB" <<'SQL'
SELECT IFNULL(event,'?'), IFNULL(utm_source,'-'), IFNULL(utm_content,'-'), COUNT(*)
FROM track_events
GROUP BY 1, 2, 3
ORDER BY 4 DESC
LIMIT 30;
SELECT event, COUNT(*) FROM track_events GROUP BY 1 ORDER BY 2 DESC;
SQL
fi
