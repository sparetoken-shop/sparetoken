#!/usr/bin/env python3
"""Create the venue account. Notify is the caller's job, only if challenge is real."""
from __future__ import annotations

import os
import time
from pathlib import Path

from cdp_drive import Cdp, click_text, fill_named

ROOT = Path(__file__).resolve().parents[1]


def _email() -> str:
    return os.environ.get("SELL_SIGNUP_EMAIL", "")


def _password() -> str:
    return os.environ.get("SELL_SIGNUP_PASSWORD", "")


def try_devto() -> dict:
    """Walk DEV.to email signup until a real challenge or a filled form submit."""
    cdp = Cdp()
    out = {"venue": "devto", "challenge": False, "url": "", "title": "", "steps": []}
    try:
        cdp.connect_page("dev.to")
        cdp.navigate("https://dev.to/enter?state=new-user", wait=4)
        out["steps"].append("opened new-user")
        if click_text(cdp, "Sign up with Email"):
            out["steps"].append("clicked email signup")
            time.sleep(3)
        email, password = _email(), _password()
        if not email or not password:
            out["steps"].append("missing SELL_SIGNUP_EMAIL/PASSWORD")
            return out
        filled = 0
        for name, val in (
            ("user_name", "sparetoken"),
            ("user_username", "sparetoken"),
            ("user_email", email),
            ("user_password", password),
            ("user_password_confirmation", password),
        ):
            if fill_named(cdp, name, val):
                filled += 1
        if filled == 0:
            for name, val in (
                ("user[name]", "sparetoken"),
                ("user[username]", "sparetoken"),
                ("user[email]", email),
                ("user[password]", password),
                ("user[password_confirmation]", password),
            ):
                if fill_named(cdp, name, val):
                    filled += 1
        out["steps"].append(f"filled {filled} fields")
        time.sleep(0.4)
        # Do not submit if a visible captcha is already on the form — human clicks it.
        cdp.eval(
            "document.querySelector('iframe[src*=\"recaptcha\"]')"
            "&& document.querySelector('iframe[src*=\"recaptcha\"]').scrollIntoView({block:'center'})"
        )
        ch = cdp.challenge()
        out.update({k: ch.get(k) for k in ("challenge", "url", "title")})
        if ch.get("challenge"):
            out["steps"].append("challenge after fill — waiting human")
            return out
        if click_text(cdp, "Sign up") or click_text(cdp, "Create account") or click_text(cdp, "Continue"):
            out["steps"].append("submitted")
            time.sleep(4)
        ch = cdp.challenge()
        out.update({k: ch.get(k) for k in ("challenge", "url", "title")})
        out["steps"].append("after submit")
        return out
    finally:
        cdp.close()


def main() -> int:
    result = try_devto()
    print(result)
    return 0 if result.get("challenge") or "submitted" in result.get("steps", []) else 78


if __name__ == "__main__":
    raise SystemExit(main())
