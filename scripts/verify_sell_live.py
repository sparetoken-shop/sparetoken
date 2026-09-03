#!/usr/bin/env python3
"""Prove a sell URL is live, public, and not Twitter.

SELL_OK is illegal without this returning 0.
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
UA = "sparetoken-sell-verify/0.2.14"


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


def verify_url(
    url: str,
    utm_content: str,
    *,
    fetch=None,
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
    return True, f"ok {status} {_host(final)}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a live sell URL")
    parser.add_argument("url")
    parser.add_argument("--utm-content", required=True)
    args = parser.parse_args(argv)
    ok, reason = verify_url(args.url, args.utm_content)
    print(reason)
    return 0 if ok else 78


if __name__ == "__main__":
    sys.exit(main())
