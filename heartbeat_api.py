"""Public pulse stub: last ship, current 7-day line, last research.

Same R$5 / 5h SKU. No pay rail. No visitor prompt. No PII.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SKU_BRL = 5
SKU_HOURS = 5

_SHIP_HEAD = re.compile(r"^## \[(\d+\.\d+\.\d+)\] — (\d{4}-\d{2}-\d{2})\s*$", re.M)
_MD_HEAD = re.compile(r"^## (.+?)\s*$", re.M)
_DAY_ROW = re.compile(r"^\| (D\d+[a-z]?) \|")


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def _version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def last_ship(root: Path | None = None) -> dict[str, str]:
    root = root or ROOT
    version = _version(root)
    text = _read(root, "CHANGELOG.md")
    for match in _SHIP_HEAD.finditer(text):
        if match.group(1) != version:
            continue
        title = ""
        for line in text[match.end() :].splitlines():
            blob = line.strip()
            if not blob or blob.startswith("###"):
                continue
            if blob.startswith("## "):
                break
            if blob.startswith("-"):
                break
            title = blob
            break
        return {"version": version, "date": match.group(2), "title": title}
    return {"version": version, "date": "", "title": ""}


def _seven_day_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not _DAY_ROW.match(line):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        rows.append(
            {
                "day": parts[0],
                "anchor": parts[1],
                "ship": parts[2],
                "research": parts[3],
                "planted": parts[4],
            }
        )
    return rows


def _anchor_date(anchor: str, year: int) -> date | None:
    try:
        day_s, month_s = anchor.split("/", 1)
        return date(year, int(month_s), int(day_s))
    except ValueError:
        return None


def seven_day(root: Path | None = None, today: date | None = None) -> dict[str, str]:
    root = root or ROOT
    today = today or date.today()
    version = _version(root)
    rows = _seven_day_rows(_read(root, "ceo/ROADMAP-7D.md"))
    for row in reversed(rows):
        if version in row["ship"]:
            return row
    stamp = today.strftime("%d/%m")
    todays = [row for row in rows if row["anchor"] == stamp]
    if todays:
        return todays[-1]
    upcoming: list[tuple[date, dict[str, str]]] = []
    for row in rows:
        when = _anchor_date(row["anchor"], today.year)
        if when and when > today:
            upcoming.append((when, row))
    if upcoming:
        upcoming.sort(key=lambda item: item[0])
        return upcoming[0][1]
    return rows[-1] if rows else {"day": "", "anchor": "", "ship": "", "research": "", "planted": ""}


def last_research(root: Path | None = None) -> dict[str, str]:
    root = root or ROOT
    text = _read(root, "ceo/RESEARCH.md")
    for match in reversed(list(_MD_HEAD.finditer(text))):
        heading = match.group(1).strip()
        low = heading.lower()
        if low.startswith("template") or low.startswith("tese") or "scratch" in low:
            continue
        body = text[match.end() :]
        nxt = re.search(r"^## ", body, re.M)
        if nxt:
            body = body[: nxt.start()]
        line = ""
        for raw in body.splitlines():
            blob = raw.strip()
            if blob.startswith(("viu:", "saiu:", "data:")):
                line = blob
                break
        if not line:
            for raw in body.splitlines():
                blob = raw.strip()
                if blob and not blob.startswith("#") and not blob.startswith("```"):
                    line = blob
                    break
        return {"when": heading, "line": line}
    return {"when": "", "line": ""}


def public_pulse(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    return {
        "version": _version(root),
        "sku_brl": SKU_BRL,
        "sku_hours": SKU_HOURS,
        "last_ship": last_ship(root),
        "seven_day": seven_day(root),
        "last_research": last_research(root),
    }
