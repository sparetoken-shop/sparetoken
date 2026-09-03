#!/usr/bin/env python3
"""Durable human-needed flag + optional Slack ping + OSS captcha assist.

Silent human-needed is dead. When a sell/product pulse hits captcha, a Google
login wall, or a VNC click, persist:

- a durable stamp in ceo/QUEUE.md
- a note in ceo/PROGRESS.md
- data/human-needed-alert.json (gitignored on the VPS) so Groko can Slack-ping

Slack: channel C0BSDQDMZ71, thread 1788232177.124409. Incoming webhook only if
SLACK_WEBHOOK_URL or WDTSOT_SLACK_WEBHOOK_URL is already in the environment.
Never invent a secret.

OSS assist: Tesseract CLI and/or a local Buster extension dir. Ollama vision
only if a vision model is already listed in the local cache. Never pull an Ollama model.
Never a paid solver. Assist failure soft-fails to notify.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")

REASONS = frozenset({"captcha", "google_login_wall", "vnc_click"})
PAID_SOLVERS_FORBIDDEN = ("2captcha", "capmonster")

SLACK_CHANNEL = "C0BSDQDMZ71"
SLACK_THREAD_TS = "1788232177.124409"
WEBHOOK_ENV_KEYS = ("SLACK_WEBHOOK_URL", "WDTSOT_SLACK_WEBHOOK_URL")

ALERT_REL = Path("data") / "human-needed-alert.json"
QUEUE_REL = Path("ceo") / "QUEUE.md"
PROGRESS_REL = Path("ceo") / "PROGRESS.md"

DURABLE_HEADING = "## Human-needed (durable)"
VISION_MODEL_HINTS = (
    "llava",
    "bakllava",
    "minicpm-v",
    "minicpmv",
    "qwen2-vl",
    "qwen-vl",
    "qwen2.5vl",
    "moondream",
    "llama3.2-vision",
    "llama3.2vision",
    "gemma3",
    "granite3.2-vision",
)

ROW_RE = re.compile(
    r"^\|\s*(?P<id>[^|]+?)\s*\|\s*(?P<pulse>[^|]+?)\s*\|\s*(?P<channel>[^|]+?)\s*\|\s*(?P<note>[^|]+?)\s*\|\s*(?P<status>[^|]+?)\s*\|$",
    re.M,
)


def now_local(now: datetime | None = None) -> datetime:
    if now is not None:
        if now.tzinfo is None:
            return now.replace(tzinfo=TZ)
        return now.astimezone(TZ)
    return datetime.now(TZ)


def iso_stamp(now: datetime | None = None) -> str:
    return now_local(now).strftime("%Y-%m-%dT%H:%M:%S%z")


def day_stamp(now: datetime | None = None) -> str:
    return now_local(now).strftime("%Y-%m-%d")


def repo_root(explicit: str | Path | None = None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get("WDTSOT_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[1]


def normalize_reason(raw: str) -> str:
    key = (raw or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "google": "google_login_wall",
        "google_login": "google_login_wall",
        "login_wall": "google_login_wall",
        "vnc": "vnc_click",
        "novnc": "vnc_click",
    }
    key = aliases.get(key, key)
    if key not in REASONS:
        raise ValueError(f"unknown human-needed reason: {raw!r} (use captcha|google_login_wall|vnc_click)")
    return key


def webhook_url(env: dict[str, str] | None = None) -> str | None:
    src = env if env is not None else os.environ
    for key in WEBHOOK_ENV_KEYS:
        val = (src.get(key) or "").strip()
        if val:
            return val
    return None


def scan_queue_rows(queue_text: str) -> list[dict[str, str]]:
    """Rows in the live queue table whose status is still human-needed."""
    found: list[dict[str, str]] = []
    in_table = False
    for line in queue_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("| id |"):
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            match = ROW_RE.match(stripped)
            if not match:
                continue
            status = match.group("status").strip().lower()
            if "human-needed" in status and "killed" not in status:
                found.append(
                    {
                        "id": match.group("id").strip(),
                        "pulse": match.group("pulse").strip(),
                        "channel": match.group("channel").strip(),
                        "note": match.group("note").strip(),
                        "status": match.group("status").strip(),
                    }
                )
            continue
        if in_table and stripped and not stripped.startswith("|"):
            in_table = False
    return found


def _reason_from_row(row: dict[str, str]) -> str:
    blob = f"{row.get('channel', '')} {row.get('note', '')} {row.get('status', '')}".lower()
    if "google" in blob or "login wall" in blob or "signup" in blob:
        return "google_login_wall"
    if "vnc" in blob:
        return "vnc_click"
    if "captcha" in blob:
        return "captcha"
    return "captcha"


def stamp_queue(queue_text: str, items: list[dict[str, str]], *, now: datetime | None = None) -> str:
    """Ensure a durable table lists every active human-needed id."""
    day = day_stamp(now)
    stamp = iso_stamp(now)
    lines = [
        DURABLE_HEADING,
        "",
        "Silent human-needed is dead. Pulse writes this table **and** `data/human-needed-alert.json` so Groko Slack-pings `C0BSDQDMZ71` thread `1788232177.124409`.",
        "",
        "| stamped | id | pulse | reason | slack |",
        "|---|---|---|---|---|",
    ]
    existing: dict[str, str] = {}
    if DURABLE_HEADING in queue_text:
        start = queue_text.index(DURABLE_HEADING)
        rest = queue_text[start:]
        for match in re.finditer(
            r"^\|\s*(\d{4}-\d{2}-\d{2}[^|]*)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
            rest,
            re.M,
        ):
            eid = match.group(2).strip()
            existing[eid] = match.group(0)
    for row in items:
        rid = row["id"]
        reason = row.get("reason") or _reason_from_row(row)
        pulse = row.get("pulse") or "sell"
        slack = "alert json + thread ping"
        lines.append(f"| {day} | {rid} | {pulse} | {reason} | {slack} |")
    block = "\n".join(lines) + "\n"
    if DURABLE_HEADING in queue_text:
        start = queue_text.index(DURABLE_HEADING)
        after = queue_text[start:]
        nxt = re.search(r"\n## ", after[4:])
        if nxt:
            end = start + 4 + nxt.start()
            return queue_text[:start] + block + "\n" + queue_text[end:].lstrip()
        return queue_text[:start] + block
    text = queue_text.rstrip() + "\n\n" + block
    if stamp:
        pass
    return text if text.endswith("\n") else text + "\n"


def stamp_progress(
    progress_text: str,
    items: list[dict[str, str]],
    *,
    now: datetime | None = None,
) -> str:
    day = day_stamp(now)
    heading = f"## {day} (human-needed notify)"
    if heading in progress_text:
        return progress_text
    ids = ", ".join(row["id"] for row in items) or "(none)"
    reasons = ", ".join(sorted({row.get("reason") or _reason_from_row(row) for row in items})) or "n/a"
    block = (
        f"{heading}\n\n"
        f"```\n"
        f"tokens_pulso: ~magro (human-needed notify + OSS captcha assist)\n"
        f"canal: slack C0BSDQDMZ71 thread 1788232177.124409\n"
        f"```\n\n"
        f"- Flag durável: {ids} ({reasons}). `data/human-needed-alert.json` + tabela em QUEUE.md.\n"
        f"- Assist OSS: Tesseract/Buster; Ollama vision só se já estiver no cache. Sem pull. Sem solver pago.\n"
        f"- Soft-fail do assist = ping humano, nunca solver pago.\n"
    )
    return progress_text.rstrip() + "\n\n" + block + "\n"


def build_alert(
    items: list[dict[str, str]],
    *,
    pulse: str,
    now: datetime | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "kind": "human-needed",
        "pulse": pulse,
        "stamped": iso_stamp(now),
        "day": day_stamp(now),
        "slack": {
            "channel": SLACK_CHANNEL,
            "thread_ts": SLACK_THREAD_TS,
            "hint": "Groko: ping this thread. Webhook only if env already set.",
        },
        "items": [
            {
                "id": row["id"],
                "pulse": row.get("pulse") or pulse,
                "channel": row.get("channel", ""),
                "reason": row.get("reason") or _reason_from_row(row),
                "note": row.get("note", ""),
                "status": row.get("status", "human-needed"),
            }
            for row in items
        ],
        "paid_solvers_forbidden": list(PAID_SOLVERS_FORBIDDEN),
    }
    if extra:
        payload.update(extra)
    return payload


def write_alert(root: Path, payload: dict[str, Any]) -> Path:
    path = root / ALERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def slack_text(payload: dict[str, Any]) -> str:
    items = payload.get("items") or []
    bits = []
    for row in items:
        bits.append(f"{row.get('id')} {row.get('reason')} ({row.get('channel') or 'n/a'})")
    joined = "; ".join(bits) or "human-needed (no row id)"
    return f"human-needed · pulse={payload.get('pulse')} · {joined} · click VNC/Google/captcha on the Mac"


def notify_slack(payload: dict[str, Any], *, env: dict[str, str] | None = None, opener=None) -> dict[str, Any]:
    url = webhook_url(env)
    if not url:
        return {"ok": False, "skipped": True, "reason": "no-webhook-env"}
    body = {
        "channel": SLACK_CHANNEL,
        "thread_ts": SLACK_THREAD_TS,
        "text": slack_text(payload),
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    open_fn = opener or urllib.request.urlopen
    try:
        with open_fn(req, timeout=8) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return {"ok": True, "skipped": False, "status": getattr(resp, "status", 200), "body": raw[:200]}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"ok": False, "skipped": False, "reason": str(exc)}


def tesseract_bin() -> str | None:
    return shutil.which("tesseract")


def buster_dir(env: dict[str, str] | None = None) -> Path | None:
    src = env if env is not None else os.environ
    raw = (src.get("BUSTER_EXTENSION_DIR") or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if path.is_dir():
        return path
    return None


def cached_ollama_vision_models(*, runner=None) -> list[str]:
    """Return locally cached vision-ish model names. Never pull."""
    run = runner or subprocess.run
    exe = shutil.which("ollama")
    if runner is None and not exe:
        return []
    exe = exe or "ollama"
    try:
        proc = run(
            [exe, "list"],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    names: list[str] = []
    for line in (proc.stdout or "").splitlines()[1:]:
        name = line.split()[0].strip() if line.strip() else ""
        if not name:
            continue
        low = name.lower()
        if any(hint in low for hint in VISION_MODEL_HINTS):
            names.append(name)
    return names


def run_tesseract(image: Path, *, runner=None) -> dict[str, Any]:
    exe = tesseract_bin()
    if not exe:
        return {"ok": False, "method": "tesseract", "reason": "tesseract-missing"}
    if not image.is_file():
        return {"ok": False, "method": "tesseract", "reason": "image-missing"}
    run = runner or subprocess.run
    try:
        proc = run(
            [exe, str(image), "stdout", "--psm", "7"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "method": "tesseract", "reason": str(exc)}
    text = (proc.stdout or "").strip()
    if proc.returncode != 0 or not text:
        return {"ok": False, "method": "tesseract", "reason": "empty-ocr", "text": text}
    return {"ok": True, "method": "tesseract", "text": text}


def run_ollama_vision(image: Path, *, runner=None, models: list[str] | None = None) -> dict[str, Any]:
    cached = models if models is not None else cached_ollama_vision_models(runner=runner)
    if not cached:
        return {"ok": False, "method": "ollama-vision", "reason": "no-cached-vision-model"}
    if not image.is_file():
        return {"ok": False, "method": "ollama-vision", "reason": "image-missing"}
    exe = shutil.which("ollama")
    if not exe:
        return {"ok": False, "method": "ollama-vision", "reason": "ollama-missing"}
    run = runner or subprocess.run
    model = cached[0]
    prompt = "Read the captcha characters only. Reply with the characters, nothing else."
    try:
        proc = run(
            [exe, "run", model, prompt, str(image)],
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "method": "ollama-vision", "reason": str(exc), "model": model}
    text = (proc.stdout or "").strip()
    if proc.returncode != 0 or not text:
        return {"ok": False, "method": "ollama-vision", "reason": "empty", "model": model}
    return {"ok": True, "method": "ollama-vision", "model": model, "text": text}


def assist_captcha(
    image: Path | None,
    *,
    env: dict[str, str] | None = None,
    runner=None,
) -> dict[str, Any]:
    """Best-effort OSS assist. Soft-fail — never a paid solver, never pull an Ollama model."""
    attempts: list[dict[str, Any]] = []
    if image is None or not image.is_file():
        attempts.append({"ok": False, "method": "image", "reason": "no-screenshot"})
    else:
        tess = run_tesseract(image, runner=runner)
        attempts.append(tess)
        if tess.get("ok"):
            return {"ok": True, "method": tess["method"], "text": tess.get("text"), "attempts": attempts}
        bdir = buster_dir(env)
        if bdir is not None:
            attempts.append(
                {
                    "ok": False,
                    "method": "buster",
                    "reason": "extension-present-no-headed-session",
                    "dir": str(bdir),
                }
            )
        else:
            attempts.append({"ok": False, "method": "buster", "reason": "buster-extension-missing"})
        ollama = run_ollama_vision(image, runner=runner)
        attempts.append(ollama)
        if ollama.get("ok"):
            return {"ok": True, "method": ollama["method"], "text": ollama.get("text"), "attempts": attempts}
    return {"ok": False, "method": "none", "soft_fail": "human-needed-notify", "attempts": attempts}


def persist(
    root: Path,
    *,
    pulse: str,
    items: list[dict[str, str]] | None = None,
    reason: str | None = None,
    item_id: str | None = None,
    channel: str | None = None,
    note: str | None = None,
    now: datetime | None = None,
    env: dict[str, str] | None = None,
    slack: bool = True,
    opener=None,
) -> dict[str, Any]:
    queue_path = root / QUEUE_REL
    progress_path = root / PROGRESS_REL
    queue_text = queue_path.read_text(encoding="utf-8") if queue_path.is_file() else ""
    scanned = scan_queue_rows(queue_text)
    if items is None:
        items = list(scanned)
    if item_id:
        row = {
            "id": item_id,
            "pulse": pulse,
            "channel": channel or "",
            "note": note or "",
            "status": "human-needed",
            "reason": normalize_reason(reason) if reason else "captcha",
        }
        if reason:
            row["reason"] = normalize_reason(reason)
        if not any(r["id"] == item_id for r in items):
            items.append(row)
        else:
            for r in items:
                if r["id"] == item_id:
                    r.update({k: v for k, v in row.items() if v})
    if reason and items:
        nr = normalize_reason(reason)
        for r in items:
            r.setdefault("reason", nr)
    if not items and reason:
        items = [
            {
                "id": item_id or "unknown",
                "pulse": pulse,
                "channel": channel or "",
                "note": note or "",
                "status": "human-needed",
                "reason": normalize_reason(reason),
            }
        ]
    if not items:
        return {"ok": True, "empty": True, "items": []}

    for r in items:
        r["reason"] = r.get("reason") or _reason_from_row(r)

    if queue_path.is_file():
        queue_path.write_text(stamp_queue(queue_text, items, now=now), encoding="utf-8")
    if progress_path.is_file():
        progress_path.write_text(
            stamp_progress(progress_path.read_text(encoding="utf-8"), items, now=now),
            encoding="utf-8",
        )
    payload = build_alert(items, pulse=pulse, now=now)
    alert_path = write_alert(root, payload)
    slack_result = {"ok": False, "skipped": True, "reason": "disabled"}
    if slack:
        slack_result = notify_slack(payload, env=env, opener=opener)
    payload["slack_result"] = slack_result
    alert_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "empty": False,
        "alert": str(alert_path),
        "items": payload["items"],
        "slack": slack_result,
    }


def pulse_hook(root: Path, pulse: str, *, now: datetime | None = None, env: dict[str, str] | None = None) -> dict[str, Any]:
    shot = None
    for candidate in (
        root / "data" / "captcha.png",
        root / "data" / "human-needed-screenshot.png",
    ):
        if candidate.is_file():
            shot = candidate
            break
    assist = assist_captcha(shot, env=env)
    if assist.get("ok"):
        return {"ok": True, "assist": assist, "persisted": False, "note": "OSS assist produced text; human still confirms"}
    result = persist(root, pulse=pulse, now=now, env=env)
    result["assist"] = assist
    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="human-needed persist + OSS captcha assist")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("persist", "scan", "pulse-hook", "assist", "notify"):
        sp = sub.add_parser(name)
        sp.add_argument("--root", default=None)
        sp.add_argument("--pulse", default="sell")
        sp.add_argument("--reason", default=None)
        sp.add_argument("--id", dest="item_id", default=None)
        sp.add_argument("--channel", default=None)
        sp.add_argument("--note", default=None)
        sp.add_argument("--image", default=None)
        sp.add_argument("--no-slack", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root(args.root)
    if args.cmd == "assist":
        image = Path(args.image) if args.image else None
        out = assist_captcha(image)
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0 if out.get("ok") else 2
    if args.cmd == "scan":
        queue_path = root / QUEUE_REL
        text = queue_path.read_text(encoding="utf-8") if queue_path.is_file() else ""
        rows = scan_queue_rows(text)
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.cmd == "notify":
        queue_path = root / QUEUE_REL
        text = queue_path.read_text(encoding="utf-8") if queue_path.is_file() else ""
        rows = scan_queue_rows(text)
        payload = build_alert(rows, pulse=args.pulse)
        write_alert(root, payload)
        result = notify_slack(payload)
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    if args.cmd == "pulse-hook":
        out = pulse_hook(root, args.pulse)
        json.dump({k: v for k, v in out.items() if k != "items" or True}, sys.stdout, ensure_ascii=False, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    out = persist(
        root,
        pulse=args.pulse,
        reason=args.reason,
        item_id=args.item_id,
        channel=args.channel,
        note=args.note,
        slack=not args.no_slack,
    )
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
