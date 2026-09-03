#!/usr/bin/env python3
"""WhatsApp ping for captcha / human click. Secrets only from env."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


def phones_from_env(raw: str | None = None) -> list[str]:
    text = raw if raw is not None else os.environ.get("ZAPI_NOTIFY_PHONES", "")
    out: list[str] = []
    for part in text.replace(";", ",").split(","):
        digits = "".join(ch for ch in part if ch.isdigit())
        if digits:
            out.append(digits)
    return out


def send_text(
    phone: str,
    message: str,
    *,
    url: str | None = None,
    token: str | None = None,
    post=None,
) -> tuple[bool, str]:
    endpoint = url or os.environ.get("ZAPI_SEND_TEXT_URL", "")
    client = token if token is not None else os.environ.get("ZAPI_CLIENT_TOKEN", "")
    if not endpoint or not client:
        return False, "ZAPI_SEND_TEXT_URL and ZAPI_CLIENT_TOKEN required"
    payload = json.dumps({"phone": phone, "message": message}).encode("utf-8")

    def _default_post(target: str, data: bytes, headers: dict[str, str]) -> tuple[int, str]:
        req = urllib.request.Request(target, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return int(resp.status), resp.read(4000).decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = exc.read(4000).decode("utf-8", errors="replace") if exc.fp else ""
            return int(exc.code), body

    poster = post or _default_post
    status, body = poster(
        endpoint,
        payload,
        {
            "Content-Type": "application/json",
            "Client-Token": client,
        },
    )
    if status < 200 or status >= 300:
        return False, f"http {status}"
    return True, body[:200]


def notify_all(message: str, *, post=None) -> tuple[int, int]:
    phones = phones_from_env()
    ok_n = 0
    for phone in phones:
        ok, _ = send_text(phone, message, post=post)
        if ok:
            ok_n += 1
    return ok_n, len(phones)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: zapi_notify.py MESSAGE", file=sys.stderr)
        return 78
    message = " ".join(argv)
    ok_n, total = notify_all(message)
    print(f"notified {ok_n}/{total}")
    return 0 if total and ok_n == total else 78


if __name__ == "__main__":
    sys.exit(main())
