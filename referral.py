"""Referral v0 schema. Fuzzy is first. 10%. Pix at R$5. No second till."""

from __future__ import annotations

import time

import invite

FIRST_INDICATOR = "fuzzy"
SKU_CENTS = 500
RATE_BPS = 1000  # 10%
COMMISSION_CENTS = SKU_CENTS * RATE_BPS // 10_000
PAYOUT_CENTS = 500
PAYOUT_VIA = "pix"
FRIENDS_TO_PAYOUT = PAYOUT_CENTS // COMMISSION_CENTS
_CLOSED = frozenset({"paid", "closed", "confirmed"})


def commission_cents(paid_closed_friends: int) -> int:
    if paid_closed_friends < 0:
        raise ValueError("paid_closed_friends")
    return COMMISSION_CENTS * int(paid_closed_friends)


def can_choose_pix(accrued_cents: int) -> bool:
    return int(accrued_cents) >= PAYOUT_CENTS


def friends_until_pix(paid_closed_friends: int) -> int:
    accrued = commission_cents(paid_closed_friends)
    if accrued >= PAYOUT_CENTS:
        return 0
    return (PAYOUT_CENTS - accrued) // COMMISSION_CENTS


def indicator_for(code: str | None, paid_referrals: int = 0) -> str:
    """A wallet code lasts only after the first friend paid. Until then: fuzzy."""
    clean = invite.normalize_code(code)
    if clean and int(paid_referrals) >= 1:
        return clean
    return FIRST_INDICATOR


def accrues(status: str | None) -> bool:
    return (status or "").strip().lower() in _CLOSED


def should_accrue(indicator: str, buyer_code: str | None, status: str) -> bool:
    if not accrues(status):
        return False
    buyer = invite.normalize_code(buyer_code)
    if not buyer:
        return False
    name = (indicator or "").strip()
    if name == buyer:
        return False
    if name != FIRST_INDICATOR and invite.normalize_code(name) is None:
        return False
    return True


def public_schema() -> dict:
    return {
        "first_indicator": FIRST_INDICATOR,
        "rate": "0.10",
        "commission_brl": "0.50",
        "payout_brl": "5.00",
        "payout_via": PAYOUT_VIA,
        "friends_to_payout": FRIENDS_TO_PAYOUT,
    }


def public_ledger(paid_closed_friends: int) -> dict:
    n = int(paid_closed_friends)
    accrued = commission_cents(n)
    out = public_schema()
    out["paid_closed_friends"] = n
    out["accrued_cents"] = accrued
    out["friends_until_pix"] = friends_until_pix(n)
    out["can_choose_pix"] = can_choose_pix(accrued)
    return out


def remember_referrer(conn, session_id: str, inbound: str | None) -> str | None:
    """Stamp the inbound invite once. Never overwrite. Never self-refer."""
    clean = invite.normalize_code(inbound)
    if not clean or not session_id:
        return None
    own = conn.execute(
        """SELECT payment_reference FROM purchases
           WHERE session_id = ? AND payment_reference IS NOT NULL
           ORDER BY created_at DESC LIMIT 1""",
        (session_id,),
    ).fetchone()
    if own and invite.normalize_code(own["payment_reference"]) == clean:
        return None
    row = conn.execute(
        "SELECT referred_by FROM user_sessions WHERE id = ?", (session_id,)
    ).fetchone()
    if row and row["referred_by"]:
        return str(row["referred_by"])
    conn.execute(
        "UPDATE user_sessions SET referred_by = ? WHERE id = ?",
        (clean, session_id),
    )
    conn.commit()
    return clean


def count_closed(conn, source_code: str | None) -> int:
    clean = invite.normalize_code(source_code)
    if not clean:
        return 0
    n = conn.execute(
        "SELECT COUNT(*) FROM referral_attributions WHERE source_code = ?",
        (clean,),
    ).fetchone()[0]
    return int(n)


def sync_paid(conn, session_id: str) -> int:
    """Attribute each paid purchase on this session to referred_by. Closed only."""
    row = conn.execute(
        "SELECT referred_by FROM user_sessions WHERE id = ?", (session_id,)
    ).fetchone()
    source = invite.normalize_code(row["referred_by"] if row else None)
    if not source:
        return 0
    added = 0
    paid = conn.execute(
        """SELECT id, payment_reference FROM purchases
           WHERE session_id = ? AND status = 'paid' AND payment_reference IS NOT NULL""",
        (session_id,),
    )
    for purchase in paid:
        buyer = invite.normalize_code(purchase["payment_reference"])
        if not should_accrue(source, buyer, "paid"):
            continue
        n = count_closed(conn, source)
        indicator = indicator_for(source, n)
        cur = conn.execute(
            """INSERT OR IGNORE INTO referral_attributions
               (purchase_id, source_code, indicator, buyer_code, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (purchase["id"], source, indicator, buyer, time.time()),
        )
        if cur.rowcount:
            added += 1
    if added:
        conn.commit()
    return added
