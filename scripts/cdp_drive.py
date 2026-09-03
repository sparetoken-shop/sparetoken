#!/usr/bin/env python3
"""Drive the headed Chromium via CDP. No WhatsApp here."""
from __future__ import annotations

import json
import time
import urllib.request
from typing import Any

import websocket

CHALLENGE_JS = r"""
(() => {
  const visible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const st = getComputedStyle(el);
    return r.width > 20 && r.height > 20 && st.visibility !== 'hidden' && st.display !== 'none';
  };
  const sel = [
    'iframe[src*="recaptcha"]', 'iframe[src*="hcaptcha"]',
    'iframe[src*="turnstile"]', 'iframe[src*="challenges.cloudflare"]',
    '.cf-turnstile', '#challenge-form', '#cf-challenge-running',
    'input[name*="otp"]', 'input[autocomplete="one-time-code"]'
  ].join(',');
  const vis = [...document.querySelectorAll(sel)].filter(visible);
  const body = (document.body && document.body.innerText || '').toLowerCase();
  const phrases = [
    'verify you are human', 'i am not a robot', 'complete the captcha',
    'enter the code we sent', 'unusual traffic', 'are you a robot',
    'select all images', 'solve the puzzle'
  ];
  const phraseHit = phrases.some(p => body.includes(p));
  return {
    challenge: vis.length > 0 || phraseHit,
    url: location.href,
    title: document.title,
    visible: vis.map(el => el.tagName + ':' + (el.src||el.name||'').slice(0,80)),
    iframe: [...document.querySelectorAll('iframe')].map(i => i.src).slice(0, 8)
  };
})()
"""


class Cdp:
    def __init__(self, port: int = 9222):
        self.port = port
        self.ws = None
        self._id = 0

    def connect_page(self, url_substr: str = "dev.to") -> dict:
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json").read())
        page = next(
            t
            for t in tabs
            if t.get("type") == "page" and url_substr in (t.get("url") or "")
        )
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=20)
        self.call("Page.enable")
        self.call("Runtime.enable")
        return page

    def call(self, method: str, params: dict | None = None) -> dict:
        assert self.ws is not None
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                return msg

    def eval(self, expression: str) -> Any:
        r = self.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        res = r.get("result", {}).get("result", {})
        return res.get("value")

    def navigate(self, url: str, wait: float = 3.0) -> None:
        self.call("Page.navigate", {"url": url})
        time.sleep(wait)

    def challenge(self) -> dict:
        data = self.eval(CHALLENGE_JS)
        return data if isinstance(data, dict) else {"challenge": False}

    def close(self) -> None:
        if self.ws:
            self.ws.close()
            self.ws = None


def click_text(cdp: Cdp, needle: str) -> bool:
    js = f"""
(() => {{
  const n = {json.dumps(needle)}.toLowerCase();
  const els = [...document.querySelectorAll('a,button,input,[role="button"]')];
  const el = els.find(e => (e.innerText||e.value||'').trim().toLowerCase() === n)
          || els.find(e => (e.innerText||e.value||'').trim().toLowerCase().includes(n));
  if (!el) return false;
  el.click();
  return true;
}})()
"""
    return bool(cdp.eval(js))


def fill_named(cdp: Cdp, name: str, value: str) -> bool:
    js = f"""
(() => {{
  const name = {json.dumps(name)};
  const val = {json.dumps(value)};
  const el = document.querySelector('input[name="' + CSS.escape(name) + '"]')
          || document.getElementById(name)
          || document.getElementById(name.replaceAll('[','_').replaceAll(']',''));
  if (!el) return false;
  el.focus();
  el.value = val;
  el.dispatchEvent(new Event('input', {{bubbles: true}}));
  el.dispatchEvent(new Event('change', {{bubbles: true}}));
  return true;
}})()
"""
    return bool(cdp.eval(js))
