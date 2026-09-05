# Publish kill-switch — attempt counter

Standing rule: `.cursor/rules/publish-or-delete.mdc` (alwaysApply).

## Definitions

| Term | Meaning |
|---|---|
| **Attempt** | A real public-publish try that the agent triad validated (and later revalidated). Not a draft, not a queue row, not a VNC note. |
| **Success** | Live permalink a stranger can open. Sell: `scripts/verify_sell_live.py` passes. |
| **Triad** | CEO / Oraculus / Groko (or equivalent agent identities). Count is shared across all three. |
| **Threshold** | 50 validated attempts with **zero** successes in the campaign window → delete or publicly archive/abandon `sparetoken-shop/sparetoken`. Project conceded. |

## What never increments success

- `enfileirou` / human-needed / VNC-blocked without live URL
- X-only when sell verification was required
- Local git / PR / research without a public live URL

## Counter stub (campaign window)

Update this table when a triad-validated attempt lands. Do not invent rows.

| # | Date (America/Sao_Paulo) | Agent | Channel / host | Validated? | Live permalink | `verify_sell_live` | Notes |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | _no attempts logged yet_ |

**Validated attempts:** 0 / 50  
**Successful public publishes:** 0  
**Kill-switch armed:** yes (fires at 50 / 0)

## Related hard rules

- VNC / noVNC banned as handoff.
- No second till without Open USDT charge (see `ceo/PAYMENT.md`).
