"""Public shelf remaining. Count only. Never a pay URL."""

from __future__ import annotations

import os
import re
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
RESTOCK_BELOW = 3
SKU_BRL = 5
SKU_HOURS = 5
_OPEN_STATUSES = ("idle", "open", "reserved")
_CONTA = re.compile(r"https://app\.conta\.vc/pay/fuzzy/c/[A-Za-z0-9_-]+")


def _db_path(root: Path) -> Path:
    if root == ROOT:
        env = os.environ.get("WDTSOT_DB")
        if env:
            return Path(env)
    return root / "data" / "wdtsot.sqlite"


def _links_path(root: Path) -> Path:
    if root == ROOT:
        env = os.environ.get("WDTSOT_LINKS_FILE")
        if env:
            return Path(env)
    return root / "data" / "conta-links.txt"


def count_open_db(db: Path) -> int | None:
    if not db.is_file():
        return None
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            row = con.execute(
                "SELECT COUNT(*) FROM pay_links WHERE status IN (?,?,?)",
                _OPEN_STATUSES,
            ).fetchone()
        finally:
            con.close()
    except sqlite3.Error:
        return None
    return int(row[0]) if row else 0


def count_open_file(path: Path) -> int | None:
    if not path.is_file():
        return None
    n = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if _CONTA.search(line):
            n += 1
    return n


def public_shelf(
    root: Path | None = None,
    *,
    db: Path | None = None,
    links: Path | None = None,
) -> dict[str, Any]:
    root = root or ROOT
    open_n = count_open_db(db or _db_path(root))
    if open_n is None:
        open_n = count_open_file(links or _links_path(root))
    if open_n is None:
        return {
            "open": None,
            "restock": False,
            "sku_brl": SKU_BRL,
            "sku_hours": SKU_HOURS,
        }
    return {
        "open": open_n,
        "restock": open_n < RESTOCK_BELOW,
        "sku_brl": SKU_BRL,
        "sku_hours": SKU_HOURS,
    }


def shelf_display(shelf: dict[str, Any]) -> str:
    open_n = shelf.get("open")
    if open_n is None:
        return ""
    line = f"{open_n} Open"
    if shelf.get("restock"):
        line += " · restock"
    return line
