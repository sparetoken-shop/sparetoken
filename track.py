"""First-party click / land / engage events. No email, no phone, no third-party pixel."""

from __future__ import annotations

import re
import time
from typing import Any

ALLOWED_EVENTS = frozenset(
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
)
# Public funnel tallies stay these four only — summarize() shape is frozen.
FUNNEL_EVENTS = ("visit", "pay_click", "claim_ok", "sell_click")

_UTM = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_CODE = re.compile(r"^wdtsot-[A-Za-z0-9]{3,16}$")
_LABEL = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_SID = re.compile(r"^[A-Za-z0-9._-]{8,64}$")
_UTM_KEYS = ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term")
_SCROLL_DEPTHS = frozenset({25, 50, 75, 100})


def _as_int(raw: Any, *, lo: int, hi: int) -> int | None:
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return None
    if n < lo or n > hi:
        return None
    return n


def sanitize_payload(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    event = str(raw.get("event") or "").strip().lower()
    if event not in ALLOWED_EVENTS:
        return None
    out: dict[str, Any] = {"event": event}
    for key in _UTM_KEYS:
        val = str(raw.get(key) or "").strip()[:64]
        if val and _UTM.match(val):
            out[key] = val
    code = str(raw.get("code") or "").strip()
    if _CODE.match(code):
        out["code"] = code
    label = str(raw.get("label") or "").strip()[:64]
    if label and _LABEL.match(label):
        out["label"] = label
    sid = str(raw.get("sid") or "").strip()[:64]
    if sid and _SID.match(sid):
        out["sid"] = sid
    ms = _as_int(raw.get("ms"), lo=0, hi=86_400_000)
    if ms is not None:
        out["ms"] = ms
    depth = _as_int(raw.get("depth"), lo=0, hi=100)
    if depth is not None and (event != "scroll_depth" or depth in _SCROLL_DEPTHS):
        if event == "scroll_depth":
            out["depth"] = depth
        elif depth in _SCROLL_DEPTHS:
            out["depth"] = depth
    return out


def record_event(conn, raw: dict[str, Any] | None) -> bool:
    clean = sanitize_payload(raw)
    if not clean:
        return False
    conn.execute(
        """
        INSERT INTO track_events (
            event, utm_source, utm_medium, utm_campaign, utm_content, utm_term,
            code, label, sid, ms, depth, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            clean["event"],
            clean.get("utm_source"),
            clean.get("utm_medium"),
            clean.get("utm_campaign"),
            clean.get("utm_content"),
            clean.get("utm_term"),
            clean.get("code"),
            clean.get("label"),
            clean.get("sid"),
            clean.get("ms"),
            clean.get("depth"),
            time.time(),
        ),
    )
    conn.commit()
    return True


def summarize(conn) -> dict[str, int]:
    """Public click tallies. Counts only — no codes, no UTM, no PII.

    Shape is frozen: visit / pay_click / claim_ok / sell_click.
    Extra first-party events (ui_click, engage_tick, …) stay off this endpoint.
    """
    out = {event: 0 for event in FUNNEL_EVENTS}
    for event, n in conn.execute("SELECT event, COUNT(*) FROM track_events GROUP BY 1"):
        if event in out:
            out[event] = int(n)
    return out
