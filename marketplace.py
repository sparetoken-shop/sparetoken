"""Skill listing = short manifesto + CLI allowlist. Same R$5 SKU. No second till."""

from __future__ import annotations

import re
from typing import Any

ALLOWED_CLIS = ("cursor", "codex", "claude", "antigravity", "metamuse")
SKU_BRL = 5
SKU_HOURS = 5
SKU_MODEL = "4.6 High Fast"
PAYOUT_VIA = "pix"
MANIFESTO_MAX = 280
TITLE_MAX = 48
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}$")


class MarketError(ValueError):
    pass


def _norm_cli(raw: Any) -> str:
    name = str(raw or "").strip().lower()
    if name not in ALLOWED_CLIS:
        raise MarketError("cli fora do allowlist.")
    return name


def validate_skill(raw: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise MarketError("pedido inválido.")
    if raw.get("price") not in (None, "", SKU_BRL, "5", "R$5"):
        raise MarketError("o sku é R$5. sem segundo preço.")
    if raw.get("hours") not in (None, "", SKU_HOURS, "5"):
        raise MarketError("são 5 horas. sem segundo sku.")
    slug = str(raw.get("slug") or "").strip().lower()
    if not SLUG_RE.fullmatch(slug):
        raise MarketError("slug curto, minúsculo.")
    title = str(raw.get("title") or "").strip()
    if not title or len(title) > TITLE_MAX:
        raise MarketError("título curto — manifesto, não pitch.")
    manifesto = str(raw.get("manifesto") or "").strip()
    if not manifesto:
        raise MarketError("falta o manifesto curto.")
    if len(manifesto) > MANIFESTO_MAX:
        raise MarketError("manifesto curto — no máximo 280.")
    clis_raw = raw.get("clis") or raw.get("cli")
    if isinstance(clis_raw, str):
        clis_raw = [part.strip() for part in clis_raw.replace(",", " ").split() if part.strip()]
    if not isinstance(clis_raw, list) or not clis_raw:
        raise MarketError("escolhe ao menos um CLI do allowlist.")
    clis: list[str] = []
    for item in clis_raw:
        name = _norm_cli(item)
        if name not in clis:
            clis.append(name)
    return {
        "slug": slug,
        "title": title,
        "manifesto": manifesto,
        "clis": clis,
        "sku_brl": SKU_BRL,
        "sku_hours": SKU_HOURS,
    }


LIVE_SKILLS = (
    {
        "slug": "mkt",
        "title": "Post curto",
        "manifesto": "280 caracteres. R$5 / 5h. Sem cara. O mesmo Pix.",
        "clis": ["cursor"],
    },
    {
        "slug": "copy",
        "title": "Texto de prateleira",
        "manifesto": "Um parágrafo. Token sobrando. Sem assinatura.",
        "clis": ["cursor"],
    },
    {
        "slug": "viral",
        "title": "Gancho de convite",
        "manifesto": "3 linhas. O convite é o mesmo ?code=.",
        "clis": ["cursor"],
    },
)


def public_contract() -> dict[str, Any]:
    skills = [validate_skill(dict(item)) for item in LIVE_SKILLS]
    return {
        "sku_brl": SKU_BRL,
        "sku_hours": SKU_HOURS,
        "model": SKU_MODEL,
        "payout_via": PAYOUT_VIA,
        "allowed_clis": list(ALLOWED_CLIS),
        "skills": [{key: skill[key] for key in ("slug", "title", "manifesto", "clis")} for skill in skills],
    }
