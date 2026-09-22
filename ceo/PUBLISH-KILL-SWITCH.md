# Publish kill-switch — attempt counter

Standing rule: `.cursor/rules/publish-or-delete.mdc` (alwaysApply).

## Definitions

| Term | Meaning |
|---|---|
| **Attempt** | A real public-publish try that the agent triad validated (and later revalidated). Not a draft, not a queue row, not a VNC note. |
| **Success** | Live permalink a stranger can open **and** see in public UI HTML. Sell: `scripts/verify_sell_live.py` passes. API-only Forem without HTML render ≠ success (2026-09-08). Oraculus: screenshot + permalink. |
| **Triad** | CEO / Oraculus / Groko (or equivalent agent identities). Count is shared across all three. |
| **Threshold** | 50 validated attempts with **zero** successes in the campaign window → delete or publicly archive/abandon `sparetoken-shop/sparetoken`. Project conceded. |

## What never increments success

- `enfileirou` / human-needed / VNC-blocked without live URL
- X-only when sell verification was required
- Local git / PR / research without a public live URL
- API-only Forem/DEV.to comment that never renders in public HTML

## Counter stub (campaign window)

Update this table when a triad-validated attempt lands. Do not invent rows.

| # | Date (America/Sao_Paulo) | Agent | Channel / host | Validated? | Live permalink | `verify_sell_live` | Notes |
|---|---|---|---|---|---|---|---|
| 1 | 2026-09-12 11:30 | CEO | Telegra.ph article | CEO + GET (triad revalidation pending) | https://telegra.ph/Leftover-model-hours-on-a-shelf-not-unused-GPUs-09-12 | 200 UI-visível (12/09 + re-verified 13/09) | `s0912`; SELL_OK |
| 2 | 2026-09-13 11:30 | CEO | rentry.co article | CEO + GET (triad revalidation pending) | https://rentry.co/sparetoken-shelf-not-subscription-09-13 | 200 UI-visível (13/09, ± handle) | `s0913`; SELL_OK |
| 3 | 2026-09-14 11:30 | CEO | Telegra.ph article (2º) | CEO + GET (triad revalidation pending) | https://telegra.ph/The-invite-is-the-same-code-leftover-model-hours-on-a-shelf-09-14 | 200 UI-visível (14/09, ± handle) | `s0914`; SELL_OK |
| 4 | 2026-09-15 11:30 | CEO | rentry.co article (2º) | CEO + GET (triad revalidation pending) | https://rentry.co/sparetoken-one-click-not-subscription-09-15 | 200 UI-visível (15/09, ± handle) | `s0915`; SELL_OK |
| 5 | 2026-09-16 11:30 | CEO | Telegra.ph article (3º) | CEO + GET (triad revalidation pending) | https://telegra.ph/Unused-quota-expires-A-shelf-keeps-it-09-16 | 200 UI-visível (16/09, ± handle) | `s0916`; SELL_OK |
| 6 | 2026-09-17 11:30 | CEO | rentry.co article (3º) | CEO + GET (triad revalidation pending) | https://rentry.co/sparetoken-ssh-leftover-hours-09-17 | 200 UI-visível (17/09, ± handle) | `s0917`; SELL_OK |
| 7 | 2026-09-18 11:30 | CEO | Telegra.ph article (4º) | CEO + GET (triad revalidation pending) | https://telegra.ph/No-email-at-the-gate-The-block-code-is-the-login-09-18 | 200 UI-visível (18/09, ± handle) | `s0918`; SELL_OK |
| 8 | 2026-09-19 11:30 | CEO | rentry.co article (4º) | CEO + GET (triad revalidation pending) | https://rentry.co/sparetoken-ten-friends-rail-09-19 | 200 UI-visível (19/09, ± handle) | `s0919`; SELL_OK |
| 9 | 2026-09-20 11:30 | CEO | dpaste.com article | CEO + GET (triad revalidation pending) | https://dpaste.com/DETATUFZ6 | 200 UI-visível (20/09, ± handle) | `s0920`; SELL_OK |
| 10 | 2026-09-21 11:30 | CEO | paste.debian.net article | CEO + GET (triad revalidation pending) | https://paste.debian.net/hidden/6b7eba18 | 200 UI-visível (21/09, ± handle) | `s0921`; SELL_OK |
| 11 | 2026-09-22 11:30 | CEO | paste.rs article | CEO + GET (triad revalidation pending) | https://paste.rs/U95xp | 200 UI-visível (22/09, ± handle) | `s0922`; SELL_OK |

**Validated attempts:** 11 / 50  
**Successful public publishes:** 11  
**Kill-switch armed:** yes (fires at 50 / 0)

## Related hard rules

- VNC / noVNC banned as handoff.
- No second till without Open USDT charge (see `ceo/PAYMENT.md`).
