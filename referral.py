"""Referral v0 schema. Fuzzy is first. 10%. Pix at R$5. No second till."""

from __future__ import annotations

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
