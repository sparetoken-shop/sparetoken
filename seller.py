"""Queue reseller applications. Never append live conta-links stock."""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

HANDLE_RE = re.compile(r"^[a-z][a-z0-9_-]{1,23}$")
PHONE_RE = re.compile(r"^\d{8,15}$")
CONTA_PAY_RE = re.compile(
    r"^https://app\.conta\.vc/pay/[a-z][a-z0-9_-]{0,31}/c/[A-Za-z0-9_-]{8,200}/?$"
)
RESERVED = frozenset({"fuzzy", "sparetoken", "admin", "www", "api", "owner", "dono"})
NOTE_MAX = 280
LINK_COUNT = 10


class SellerError(ValueError):
    pass


def _truthy(raw: Any) -> bool:
    if raw is True:
        return True
    if isinstance(raw, str):
        return raw.strip().lower() in {"1", "true", "on", "yes", "sim"}
    return False


def normalize_handle(raw: Any) -> str:
    text = str(raw or "").strip().lower()
    if "@" in text:
        raise SellerError("handle sem @ — apelido curto, não e-mail.")
    if PHONE_RE.fullmatch(re.sub(r"[\s.+-]", "", text)):
        raise SellerError("handle sem telefone. só um apelido.")
    if not HANDLE_RE.fullmatch(text):
        raise SellerError("handle curto, minúsculo, começa com letra. sem e-mail.")
    if text in RESERVED:
        raise SellerError("esse nome já está na mesa. escolhe outro.")
    return text


def parse_links(raw: Any) -> list[str]:
    if isinstance(raw, list):
        lines = [str(item).strip() for item in raw]
    else:
        lines = [ln.strip() for ln in str(raw or "").splitlines()]
    links = [ln.rstrip("/") for ln in lines if ln]
    if len(links) != LINK_COUNT:
        raise SellerError("precisam ser exatamente 10 links conta.vc, um por linha.")
    if len(set(links)) != LINK_COUNT:
        raise SellerError("os 10 links precisam ser diferentes.")
    bad = [u for u in links if not CONTA_PAY_RE.fullmatch(u)]
    if bad:
        raise SellerError("cada link é https://app.conta.vc/pay/… — só isso.")
    return links


def validate(raw: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise SellerError("pedido inválido.")
    if not _truthy(raw.get("ack")):
        raise SellerError("marca o termo. a responsabilidade é sua.")
    handle = normalize_handle(raw.get("handle"))
    links = parse_links(raw.get("links"))
    note = str(raw.get("note") or "").strip()
    if len(note) > NOTE_MAX:
        raise SellerError("nota curta — no máximo 280 caracteres.")
    return {"handle": handle, "links": links, "note": note, "ack": True}


def apply(dest: Path, raw: dict[str, Any] | None) -> dict[str, Any]:
    clean = validate(raw)
    dest.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    digest = hashlib.sha256(clean["handle"].encode("utf-8")).hexdigest()[:12]
    path = dest / f"{stamp}-{digest}.json"
    payload = {
        "handle": clean["handle"],
        "links": clean["links"],
        "note": clean["note"],
        "ack": True,
        "status": "queued",
        "created_at": stamp,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "queued": True}
