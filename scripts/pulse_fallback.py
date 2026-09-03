#!/usr/bin/env python3
"""Fallback after the 15 min human window: shop /pulse + GitHub issue."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOP = "https://sparetoken.shop"
REPO = os.environ.get("SELL_GITHUB_REPO", "sparetoken-shop/sparetoken")


def pulse_html(day: str, utm_content: str, shop_link: str, note: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>sparetoken pulse {day}</title>
  <meta name="robots" content="index,follow">
</head>
<body>
  <h1>sparetoken sell pulse {day}</h1>
  <p>Community-driven leftover-token shop. Not a company. Building in public.</p>
  <p>This page is the railway of a token shelf: R$5 · 5h · 4.6 High Fast. Pix of one step.</p>
  <p><a href="{shop_link}">Open the shelf</a></p>
  <p>{note}</p>
  <p>utm_campaign=sell utm_content={utm_content}</p>
</body>
</html>
"""


def shop_link(utm_source: str, utm_content: str) -> str:
    return (
        f"{SHOP}/?utm_source={utm_source}&utm_medium=comment"
        f"&utm_campaign=sell&utm_content={utm_content}"
    )


def write_shop_pulse(
    day: str,
    utm_content: str,
    *,
    static_dir: Path | None = None,
    note: str = "Correction pulse. First empty OK is not a pulse.",
) -> Path:
    target = (static_dir or (ROOT / "static" / "pulse")) 
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{day}.html"
    link = shop_link("pulse", utm_content)
    path.write_text(pulse_html(day, utm_content, link, note), encoding="utf-8")
    return path


def shop_public_url(day: str) -> str:
    return f"{SHOP}/pulse/{day}.html"


def issue_body(day: str, utm_content: str, shop_pulse: str) -> str:
    link = shop_link("github", utm_content)
    return (
        f"Daily sell pulse {day}.\n\n"
        "This experiment is a community-driven leftover-token shop — "
        "a railway for sharing idle model hours, not a company.\n\n"
        f"Shelf: {link}\n"
        f"Pulse page: {shop_pulse}\n\n"
        f"utm_campaign=sell utm_content={utm_content}\n"
        "No wallet codes. No API tokens. No names.\n"
    )


def create_github_issue(
    title: str,
    body: str,
    *,
    token: str | None = None,
    repo: str | None = None,
    post=None,
) -> tuple[bool, str]:
    tok = token if token is not None else os.environ.get("GITHUB_TOKEN", "")
    dest = repo or REPO
    if not tok:
        return False, "GITHUB_TOKEN missing"

    endpoint = f"https://api.github.com/repos/{dest}/issues"
    payload = json.dumps({"title": title, "body": body}).encode("utf-8")

    def _default_post(url: str, data: bytes, headers: dict[str, str]) -> tuple[int, dict]:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
                return int(resp.status), parsed
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            try:
                parsed = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parsed = {"message": raw}
            return int(exc.code), parsed

    poster = post or _default_post
    status, parsed = poster(
        endpoint,
        payload,
        {
            "Authorization": f"Bearer {tok}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "sparetoken-sell-pulse",
        },
    )
    html_url = str(parsed.get("html_url") or "")
    if status < 200 or status >= 300 or not html_url:
        return False, f"github http {status}"
    return True, html_url


def publish_fallback(
    day: str | None = None,
    utm_content: str = "s000",
    *,
    static_dir: Path | None = None,
    github_post=None,
) -> dict:
    day = day or date.today().isoformat()
    path = write_shop_pulse(day, utm_content, static_dir=static_dir)
    pulse_url = shop_public_url(day)
    ok, issue_url = create_github_issue(
        f"sell pulse {day}",
        issue_body(day, utm_content, pulse_url),
        post=github_post,
    )
    return {
        "day": day,
        "shop_path": str(path),
        "shop_url": pulse_url,
        "github_ok": ok,
        "github_url": issue_url if ok else "",
        "github_error": "" if ok else issue_url,
        "utm_content": utm_content,
    }


def main() -> int:
    day = os.environ.get("SELL_DAY") or date.today().isoformat()
    utm = os.environ.get("SELL_UTM_CONTENT", "s000")
    result = publish_fallback(day, utm)
    print(json.dumps(result, ensure_ascii=True))
    return 0 if result["github_ok"] else 78


if __name__ == "__main__":
    sys.exit(main())
