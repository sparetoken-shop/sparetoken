#!/usr/bin/env python3
"""Prove a sell URL is live, public, UI-visible, and not Twitter.

SELL_OK / verified-live is illegal without this returning 0.

Gate (2026-09-08 lesson): third-party proof must be **UI-visible**.
A Forem/DEV.to API 2xx that never renders the comment in public HTML is
NOT verified-live. Oraculus lane also requires a screenshot of the public
UI alongside the permalink. Do not invent fragile CSS/DOM scrapers that
break CI — prefer this GET of public HTML + optional handle/shop markers.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

BLOCKED_HOSTS = (
    "twitter.com",
    "x.com",
    "t.co",
    "nitter.net",
    "nitter.it",
    "nitter.cz",
    "fxtwitter.com",
    "vxtwitter.com",
    "fixupx.com",
)
UTM_CONTENT_RE = re.compile(r"utm_content=s[0-9A-Za-z]{3,}", re.I)
SHOP_MARK = "sparetoken.shop"
CAMPAIGN_MARK = "utm_campaign=sell"
UA = "sparetoken-sell-verify/0.2.30"


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().rstrip(".")


def is_blocked_host(url: str) -> bool:
    host = _host(url)
    if not host:
        return True
    for blocked in BLOCKED_HOSTS:
        if host == blocked or host.endswith("." + blocked):
            return True
    return False


def default_fetch(url: str) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read(800_000)
            body = raw.decode("utf-8", errors="replace")
            return int(resp.status), resp.geturl(), body
    except urllib.error.HTTPError as exc:
        raw = exc.read(800_000) if exc.fp else b""
        body = raw.decode("utf-8", errors="replace")
        return int(exc.code), exc.geturl() or url, body
    except urllib.error.URLError as exc:
        raise RuntimeError(f"fetch failed: {exc}") from exc


def ui_visible_markers(body: str, *, handle: str | None = None) -> tuple[bool, str]:
    """Cheap UI-visibility helper: public HTML must show shop (+ optional handle).

    Not a CSS scraper. When feasible, Oraculus/CEO pass --handle so the
    commenter identity appears in the same public HTML as the shop link.
    API-only hits without these markers fail the gate.
    """
    if not body:
        return False, "empty body (not UI-visible)"
    low = body.lower()
    if SHOP_MARK not in low:
        return False, "public HTML missing sparetoken.shop (API-only / not UI-visible)"
    if handle:
        needle = handle.strip().lstrip("@").lower()
        if not needle:
            return False, "empty handle"
        if needle not in low:
            return False, f"public HTML missing handle {needle} (not UI-visible)"
    return True, "ui-visible markers ok"


def verify_url(
    url: str,
    utm_content: str,
    *,
    fetch=None,
    handle: str | None = None,
) -> tuple[bool, str]:
    if not url or not url.startswith(("http://", "https://")):
        return False, "url must be http(s)"
    if is_blocked_host(url):
        return False, f"blocked host: {_host(url)}"
    if not re.fullmatch(r"s[0-9A-Za-z]{3,}", utm_content):
        return False, "utm_content must look like sNNN"

    getter = fetch or default_fetch
    try:
        status, final, body = getter(url)
    except Exception as exc:  # noqa: BLE001 — pulse must not crash-ok
        return False, f"fetch error: {exc}"

    if is_blocked_host(final):
        return False, f"redirected to blocked host: {_host(final)}"
    if status < 200 or status >= 300:
        return False, f"http {status}"

    low = body.lower()
    if SHOP_MARK not in low:
        return False, "body missing sparetoken.shop"
    if CAMPAIGN_MARK not in low:
        return False, "body missing utm_campaign=sell"
    wanted = f"utm_content={utm_content.lower()}"
    if wanted not in low and not UTM_CONTENT_RE.search(body):
        return False, f"body missing {wanted}"
    if wanted not in low:
        return False, f"body missing exact {wanted}"

    ok_ui, ui_reason = ui_visible_markers(body, handle=handle)
    if not ok_ui:
        return False, ui_reason
    return True, f"ok {status} {_host(final)} ({ui_reason})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify a live sell URL is UI-visible in public HTML. "
            "API-only Forem comments that never render are NOT verified-live."
        )
    )
    parser.add_argument("url")
    parser.add_argument("--utm-content", required=True)
    parser.add_argument(
        "--handle",
        default="",
        help="optional commenter handle that must appear in public HTML (Oraculus lane)",
    )
    args = parser.parse_args(argv)
    handle = (args.handle or "").strip() or None
    ok, reason = verify_url(args.url, args.utm_content, handle=handle)
    print(reason)
    return 0 if ok else 78


if __name__ == "__main__":
    sys.exit(main())
