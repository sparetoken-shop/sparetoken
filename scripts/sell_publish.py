#!/usr/bin/env python3
"""Sell pulse publisher. No live URL, no SELL_OK."""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pulse_fallback import publish_fallback, shop_link  # noqa: E402
from pulse_vnc import start as vnc_start, stop as vnc_stop  # noqa: E402
from venue_signup import try_devto  # noqa: E402
from verify_sell_live import verify_url  # noqa: E402
from zapi_notify import notify_all  # noqa: E402

PROOF = Path(os.environ.get("SELL_PROOF_FILE", str(ROOT / "data" / "sell-proof.jsonl")))
VENUES = ROOT / "ceo" / "launch" / "venues.json"
COPY_FILE = ROOT / "data" / "sell-copy.txt"


def today() -> str:
    return os.environ.get("SELL_DAY") or date.today().isoformat()


def utm_content_for(day: str) -> str:
    forced = os.environ.get("SELL_UTM_CONTENT")
    if forced:
        return forced
    compact = day.replace("-", "")
    return "s" + compact[4:]  # sMMDD → s0831


def load_venue(day: str) -> dict:
    data = json.loads(VENUES.read_text(encoding="utf-8"))
    row = dict(data.get("default") or {})
    row.update(data.get(day) or {})
    return row


def allows_fallback(venue: dict) -> bool:
    flag = venue.get("fallback", True)
    if flag is False:
        return False
    return str(flag).lower() not in {"0", "false", "no"}


def signup_for(venue: dict):
    host = (venue.get("host") or "").lower()
    if host in {"devto", "dev.to"}:
        return try_devto
    return lambda: {
        "challenge": False,
        "venue": host,
        "steps": [f"no autodrive for {host} — login wall is not whatsapp"],
    }


def public_copy(day: str, utm: str, venue: dict) -> str:
    link = shop_link(venue.get("host") or "web", utm)
    return (
        f"sparetoken sell pulse {day}\n\n"
        "Leftover model time on a shelf. Community-driven token shop — "
        "a railway for sharing idle hours, not a company.\n"
        "R$5 · 5h · 4.6 High Fast. Pix of one step.\n\n"
        f"{link}\n\n"
        "No founder name. No wallet codes. Building in public.\n"
        f"utm_campaign=sell utm_content={utm}\n"
    )


def human_wait_sec() -> int:
    return int(os.environ.get("SELL_HUMAN_WAIT_SEC", "900"))


def append_proof(row: dict) -> None:
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    with PROOF.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=True) + "\n")


def _verify(url: str, utm: str, fetch=None) -> bool:
    ok, reason = verify_url(url, utm, fetch=fetch)
    print(f"verify {url} → {ok} {reason}", flush=True)
    return ok


def run(
    *,
    fetch=None,
    notify=None,
    start_vnc=None,
    stop_vnc=None,
    fallback=None,
    inspect=None,
    signup=None,
    sleep=None,
) -> int:
    day = today()
    utm = utm_content_for(day)
    venue = load_venue(day)
    copy = public_copy(day, utm, venue)
    COPY_FILE.parent.mkdir(parents=True, exist_ok=True)
    COPY_FILE.write_text(copy, encoding="utf-8")
    print(f"venue={venue.get('host')} url={venue.get('url')} utm={utm}", flush=True)

    notifier = notify or notify_all
    proof_url = os.environ.get("SELL_PROOF_URL", "").strip()
    if proof_url and _verify(proof_url, utm, fetch=fetch):
        append_proof({"day": day, "url": proof_url, "via": "proof-env", "utm_content": utm})
        return 0

    starter = start_vnc or vnc_start
    stopper = stop_vnc or vnc_stop
    wait = human_wait_sec()
    vnc_url = ""
    try:
        vnc_state = starter(venue["url"], copy_path=COPY_FILE)
        vnc_url = vnc_state.get("url") or ""
        signup_fn = signup or signup_for(venue)
        driven = signup_fn()
        print(f"signup={driven}", flush=True)
        if driven.get("challenge"):
            msg = (
                f"sparetoken sell {day}: conta preenchida em {venue.get('host')}. "
                f"Captcha visivel no VNC agora. 15 min. Marca o box e Sign up. "
                f"{vnc_url}"
            )
            ok_n, total = notifier(msg)
            print(f"zapi {ok_n}/{total} challenge=1", flush=True)
            sleeper = sleep or time.sleep
            sleeper(wait)
            proof_url = os.environ.get("SELL_PROOF_URL", "").strip()
            proof_file = Path(os.environ.get("SELL_PROOF_URL_FILE", str(ROOT / "data" / "sell-proof-url.txt")))
            if proof_file.is_file():
                proof_url = proof_file.read_text(encoding="utf-8").strip() or proof_url
            if proof_url and _verify(proof_url, utm, fetch=fetch):
                append_proof({"day": day, "url": proof_url, "via": "human", "utm_content": utm})
                return 0
        else:
            print("no visible captcha — no whatsapp", flush=True)
    finally:
        try:
            stopper()
        except Exception as exc:  # noqa: BLE001
            print(f"vnc stop: {exc}", flush=True)

    if not allows_fallback(venue):
        print("SELL_DEAD: venue forbids first-party fallback", flush=True)
        append_proof(
            {
                "day": day,
                "via": "no-fallback",
                "utm_content": utm,
                "host": venue.get("host"),
            }
        )
        return 78

    print("fallback shop + github", flush=True)
    fb = fallback or publish_fallback
    result = fb(day, utm)
    shop_url = result.get("shop_url") or ""
    gh_url = result.get("github_url") or ""
    shop_ok = bool(shop_url) and _verify(shop_url, utm, fetch=fetch)
    gh_ok = bool(gh_url) and _verify(gh_url, utm, fetch=fetch)
    append_proof(
        {
            "day": day,
            "shop_url": shop_url,
            "github_url": gh_url,
            "shop_ok": shop_ok,
            "github_ok": gh_ok,
            "via": "fallback",
            "utm_content": utm,
        }
    )
    if shop_ok and gh_ok:
        return 0
    print("SELL_DEAD: fallback missing a live URL", flush=True)
    return 78


def main() -> int:
    return run()


if __name__ == "__main__":
    sys.exit(main())
