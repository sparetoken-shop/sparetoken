const log = document.getElementById("log");
const form = document.getElementById("form");
const input = document.getElementById("input");
const send = document.getElementById("send");
const hint = document.getElementById("hint");
const payBtn = document.getElementById("pay");
const payNote = document.getElementById("pay-note");
const blockWrap = document.getElementById("block-wrap");
const blockCode = document.getElementById("block-code");
const claimForm = document.getElementById("claim");
const claimCode = document.getElementById("claim-code");
const claimStatus = document.getElementById("claim-status");
const clock = document.getElementById("hero-clock") || document.querySelector(".clock");
const heroUsed = document.getElementById("hero-used");
const usedRow = document.getElementById("used-row");
const clockWrap = document.getElementById("clock-wrap");
const clockBtn = document.getElementById("clock-btn");
const clockBtnTitle = document.getElementById("clock-btn-title");
const clockMenu = document.getElementById("clock-menu");
const clockRows = document.getElementById("clock-rows");
const clockFoot = document.getElementById("clock-foot");
const btnNew = document.getElementById("btn-new");
const btnCopy = document.getElementById("btn-copy");
const resumeSheet = document.getElementById("resume-sheet");
const resumeName = document.getElementById("resume-name");
const resumeMeta = document.getElementById("resume-meta");
const resumeWebCmd = document.getElementById("resume-web-cmd");
const resumeSshCmd = document.getElementById("resume-ssh-cmd");
const resumeBack = document.getElementById("resume-back");
const resumeCopyWeb = document.getElementById("resume-copy-web");
const resumeOpenWeb = document.getElementById("resume-open-web");
const resumeCopySsh = document.getElementById("resume-copy-ssh");
const payModal = document.getElementById("pay-modal");
const sellOpen = document.getElementById("sell-open");
const sellModal = document.getElementById("vender");
const sellerForm = document.getElementById("seller-form");
const sellerStatus = document.getElementById("seller-status");
const sellerSubmit = document.getElementById("seller-submit");
let paidTimer = 0;
let lastSession = null;
let menuOpen = false;
let resumeView = null;

function t(key, vars) {
  return window.ST && typeof window.ST.t === "function" ? window.ST.t(key, vars) : key;
}

function addBubble(role, text) {
  const el = document.createElement("div");
  el.className = `bubble ${role}`;
  el.textContent = text;
  log.appendChild(el);
  log.scrollTop = log.scrollHeight;
  return el;
}

function resetLog() {
  log.innerHTML = "";
  addBubble("sys", t("chat.sys"));
}

function renderMessages(messages) {
  log.innerHTML = "";
  if (!messages || !messages.length) {
    addBubble("sys", t("chat.sys"));
    return;
  }
  messages.forEach((item) => {
    const role = item.role === "assistant" ? "ai" : item.role === "user" ? "you" : "sys";
    addBubble(role, item.body || "");
  });
}

function setResumeUrl(code, id) {
  if (!code || !id) return;
  const next = new URL(location.href);
  next.searchParams.set("code", code);
  next.searchParams.set("resume", id);
  history.replaceState({}, "", `${next.pathname}${next.search}${next.hash}`);
}

function resumeHref(data) {
  return (data && data.return_url) || (data && data.block_code
    ? `https://wdtsot.shop/?code=${data.block_code}`
    : location.href);
}

function webResumeUrl(code, id) {
  return `https://wdtsot.shop/?code=${encodeURIComponent(code)}&resume=${encodeURIComponent(id)}`;
}

function sshResumeCmd(id) {
  return `ssh -t agent-guest@wdtsot.shop resume ${id}`;
}

async function copyLabel(btn, text, label) {
  if (!btn || !text) return;
  try {
    await navigator.clipboard.writeText(text);
    btn.textContent = t("js.copied");
    setTimeout(() => {
      btn.textContent = label;
    }, 1400);
  } catch (_) {
    btn.textContent = t("js.copy_fail");
  }
}

function closeResume() {
  resumeView = null;
  if (resumeSheet) resumeSheet.hidden = true;
}

function openResume(chat, title, code) {
  if (!resumeSheet || !chat || !code) return;
  resumeView = { id: chat.id, title, code, used: chat.used_seconds };
  if (resumeName) resumeName.textContent = title;
  if (resumeMeta) {
    resumeMeta.textContent = t("js.line_mins", {
      mins: minutesLabel(chat.used_seconds),
      code,
    });
  }
  if (resumeWebCmd) resumeWebCmd.textContent = webResumeUrl(code, chat.id);
  if (resumeSshCmd) resumeSshCmd.textContent = sshResumeCmd(chat.id);
  resumeSheet.hidden = false;
  setMenu(false);
}

function setRemaining(n) {
  if (typeof n !== "number") return;
  if (hint.dataset.paid === "1") return;
  hint.textContent =
    n <= 0 ? t("js.hint0") : n === 1 ? t("js.hint1") : t("js.hintn", { n });
}

function showInvite(code, urlFromApi) {
  const wrap = document.getElementById("invite-wrap");
  const urlEl = document.getElementById("invite-url");
  const copyBtn = document.getElementById("invite-copy");
  if (!wrap || !urlEl) return;
  let url = urlFromApi || "";
  if (!url) {
    const clean = (code || "").trim();
    if (/^wdtsot-[A-Za-z0-9]{3,16}$/.test(clean)) {
      url = `https://sparetoken.shop/?code=${encodeURIComponent(clean)}`;
    }
  }
  if (!url) {
    wrap.hidden = true;
    return;
  }
  urlEl.textContent = url;
  wrap.hidden = false;
  if (copyBtn) copyBtn.dataset.copy = url;
}

function showBlock(code, inviteFromApi) {
  if (!code || !blockWrap || !blockCode) return;
  blockCode.textContent = code;
  blockWrap.hidden = false;
  if (claimCode && !claimCode.value) claimCode.value = code;
  showInvite(code, inviteFromApi);
}

function isGenericLabel(label) {
  const s = (label || "").trim();
  return !s || s === "web" || s === "ssh" || /^session-\d{8}-\d{6}-/i.test(s) || /^web-\d+$/i.test(s);
}

function titlesFor(chats) {
  const chrono = [...(chats || [])].reverse();
  const map = {};
  (chats || []).forEach((chat) => {
    if (!isGenericLabel(chat.label)) {
      map[chat.id] = chat.label;
      return;
    }
    map[chat.id] = `Chat ${chrono.findIndex((c) => c.id === chat.id) + 1}`;
  });
  return map;
}

function minutesLabel(seconds) {
  const n = Math.max(0, Math.floor((seconds || 0) / 60));
  return n === 1 ? t("js.min_one") : t("js.min_many", { n });
}

function setMenu(open) {
  menuOpen = !!open;
  if (clockMenu) clockMenu.hidden = !menuOpen;
  if (clockBtn) clockBtn.setAttribute("aria-expanded", menuOpen ? "true" : "false");
}

function renderClock(data) {
  const paid = !!(data && (data.paid || data.exhausted) && data.block_code);
  if (clockWrap) clockWrap.hidden = !paid;
  if (!paid) {
    setMenu(false);
    closeResume();
    return;
  }
  const chats = data.chats || [];
  const names = titlesFor(chats);
  const activeId = data.active_chat_id;
  const active = chats.find((c) => c.id === activeId) || chats[0];
  if (clockBtnTitle) clockBtnTitle.textContent = active ? names[active.id] : t("clock.chat1");
  if (clockRows) {
    clockRows.innerHTML = "";
    chats.forEach((chat) => {
      const li = document.createElement("li");
      if (chat.id === activeId) li.className = "active";
      if (chat.id === activeId) {
        const field = document.createElement("input");
        field.className = "rename";
        field.value = names[chat.id];
        field.maxLength = 80;
        field.setAttribute("aria-label", t("js.rename"));
        field.addEventListener("click", (event) => event.stopPropagation());
        field.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            field.blur();
          }
        });
        field.addEventListener("blur", () => {
          const next = field.value.trim();
          if (!next || next === names[chat.id]) {
            field.value = names[chat.id];
            return;
          }
          clockAction("rename", { id: chat.id, title: next });
        });
        li.appendChild(field);
      } else {
        const pick = document.createElement("button");
        pick.type = "button";
        pick.textContent = names[chat.id];
        pick.addEventListener("click", () => {
          clockAction("use", { id: chat.id });
        });
        li.appendChild(pick);
      }
      const mins = document.createElement("span");
      mins.className = "mins";
      mins.textContent = minutesLabel(chat.used_seconds);
      li.appendChild(mins);
      const go = document.createElement("button");
      go.type = "button";
      go.className = "go";
      go.textContent = "↗";
      go.setAttribute("aria-label", t("js.resume_of", { name: names[chat.id] }));
      go.title = t("js.resume_title");
      go.addEventListener("click", (event) => {
        event.stopPropagation();
        openResume(chat, names[chat.id], data.block_code);
      });
      li.appendChild(go);
      clockRows.appendChild(li);
    });
  }
  if (clockFoot) {
    const n = chats.length;
    const noun = n === 1 ? t("js.chat_one") : t("js.chat_many");
    clockFoot.textContent = t("js.clock_foot", {
      n,
      noun,
      mins: minutesLabel(data.used_seconds),
    });
  }
}

function applySession(data) {
  if (!data) return;
  lastSession = data;
  if (data.exhausted) {
    hint.dataset.paid = "1";
    hint.className = "hint exhausted";
    hint.textContent = t("js.exhausted");
    if (clock) clock.textContent = "00:00:00";
    if (send) send.disabled = true;
    if (input) {
      input.disabled = true;
      input.placeholder = t("js.exhausted.ph");
    }
    renderClock(data);
    stopPaidLoop();
    if (payNote) payNote.textContent = t("js.exhausted.note");
    if (data.block_code) showBlock(data.block_code, data.invite_url);
    return;
  }
  if (data.ok === false) return;
  if (data.paid) {
    hint.dataset.paid = "1";
    hint.className = data.warn ? "hint warn" : "hint";
    const busy = data.processing ? t("js.busy") : "";
    hint.textContent = data.warn
      ? t("js.paid.warn", { clock: data.remaining_clock })
      : t("js.paid", { clock: data.remaining_clock, busy });
    if (clock && data.remaining_clock) clock.textContent = data.remaining_clock;
    if (heroUsed && data.used_clock) heroUsed.textContent = data.used_clock;
    if (usedRow) usedRow.hidden = false;
    renderClock(data);
    if (send) send.disabled = false;
    if (input) {
      input.disabled = false;
      input.placeholder = t("chat.placeholder");
    }
    if (payNote) {
      payNote.textContent = t("js.paid.note");
    }
    startPaidLoop();
  } else if (data.remaining_messages != null) {
    hint.dataset.paid = "";
    hint.className = "hint";
    renderClock(data);
    setRemaining(data.remaining_messages);
  }
  if (data.block_code) showBlock(data.block_code, data.invite_url);
}

async function clockAction(action, extra) {
  try {
    const res = await fetch("/api/clock", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, ...(extra || {}) }),
    });
    const data = await res.json();
    applySession(data);
    if (!res.ok && data.error) setClaimStatus(data.error, "err");
    return data;
  } catch (_) {
    return null;
  }
}

function stopPaidLoop() {
  if (paidTimer) {
    clearInterval(paidTimer);
    paidTimer = 0;
  }
}

function startPaidLoop() {
  if (paidTimer) return;
  paidTimer = setInterval(() => {
    if (document.visibilityState === "visible") clockAction("tick");
  }, 15000);
}

function setClaimStatus(text, kind) {
  if (!claimStatus) return;
  claimStatus.textContent = text;
  claimStatus.className = `claim-status ${kind || ""}`.trim();
}

function blockCodeFromPage() {
  const params = new URLSearchParams(location.search);
  return (params.get("code") || "").trim();
}

async function loadSession() {
  try {
    const params = new URLSearchParams(location.search);
    const code = (params.get("code") || "").trim();
    const resume = (params.get("resume") || "").trim();
    const qs = new URLSearchParams();
    if (code) qs.set("code", code);
    if (resume) qs.set("resume", resume);
    const url = qs.toString() ? `/api/session?${qs}` : "/api/session";
    const res = await fetch(url, { credentials: "same-origin" });
    const data = await res.json();
    applySession(data);
    return data;
  } catch (_) {
    return null;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text || send.disabled) return;
  input.value = "";
  resize();
  addBubble("you", text);
  const ai = addBubble("ai", "");
  send.disabled = true;
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    if (!res.ok || !res.body) {
      let err = t("js.chat_fail");
      try {
        const data = await res.json();
        err = data.error || err;
        if (data.exhausted || data.remaining_clock) applySession(data);
        else if (data.remaining_messages != null) setRemaining(data.remaining_messages);
      } catch (_) {}
      ai.textContent = err;
      return;
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";
      for (const part of parts) {
        const line = part.split("\n").find((l) => l.startsWith("data:"));
        if (!line) continue;
        let payload;
        try {
          payload = JSON.parse(line.slice(5).trim());
        } catch (_) {
          continue;
        }
        if (payload.remaining_clock || payload.exhausted) applySession(payload);
        else if (payload.remaining_messages != null) setRemaining(payload.remaining_messages);
        if (payload.text) ai.textContent += payload.text;
        if (payload.error) ai.textContent = payload.error;
        log.scrollTop = log.scrollHeight;
      }
    }
    if (!ai.textContent) ai.textContent = t("js.chat_silent");
  } catch (_) {
    ai.textContent = t("js.chat_net");
  } finally {
    send.disabled = false;
    input.focus();
  }
});

function resize() {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 140) + "px";
}
input.addEventListener("input", resize);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

const TRACK_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "code"];

function captureLanding() {
  const params = new URLSearchParams(location.search);
  let bag = {};
  try {
    bag = JSON.parse(localStorage.getItem("st_utm") || "{}") || {};
  } catch (_) {
    bag = {};
  }
  TRACK_KEYS.forEach((key) => {
    const val = params.get(key);
    if (val) bag[key] = String(val).slice(0, 64);
  });
  bag.landed_at = Date.now();
  try {
    localStorage.setItem("st_utm", JSON.stringify(bag));
  } catch (_) {}
  return bag;
}

function ping(event) {
  const bag = (() => {
    try {
      return JSON.parse(localStorage.getItem("st_utm") || "{}") || {};
    } catch (_) {
      return {};
    }
  })();
  const body = { event };
  TRACK_KEYS.forEach((key) => {
    if (bag[key]) body[key] = bag[key];
  });
  fetch("/api/track", {
    method: "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    keepalive: true,
  }).catch(() => {});
}

async function openCheckout() {
  if (!payBtn) return;
  payBtn.disabled = true;
  ping("pay_click");
  try {
    const res = await fetch("/api/pay", {
      method: "POST",
      credentials: "same-origin",
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      setClaimStatus(data.error || t("js.pay_fail"), "err");
      return;
    }
    showBlock(data.block_code);
    setClaimStatus(t("js.pay_wait"), "");
    if (data.pay_url) window.open(data.pay_url, "_blank", "noopener");
  } catch (_) {
    setClaimStatus(t("js.net"), "err");
  } finally {
    payBtn.disabled = false;
  }
}

if (payBtn) {
  payBtn.addEventListener("click", () => {
    if (payModal && typeof payModal.showModal === "function") payModal.showModal();
    else openCheckout();
  });
}
if (payModal) {
  payModal.addEventListener("close", () => {
    if (payModal.returnValue === "ok") openCheckout();
  });
}

function setSellerStatus(text, kind) {
  if (!sellerStatus) return;
  sellerStatus.textContent = text || "";
  sellerStatus.className = "claim-status" + (kind ? ` ${kind}` : "");
}

function openSeller(event) {
  if (event) event.preventDefault();
  ping("sell_click");
  if (sellModal && typeof sellModal.showModal === "function") {
    sellModal.showModal();
    return;
  }
  location.hash = "vender";
}

if (sellOpen) sellOpen.addEventListener("click", openSeller);
document.querySelectorAll('a[href="#vender"]').forEach((el) => {
  if (el === sellOpen) return;
  el.addEventListener("click", openSeller);
});
if (location.hash === "#vender") openSeller();
if (sellModal) {
  sellModal.querySelectorAll('a[href="#terminal"]').forEach((el) => {
    el.addEventListener("click", () => {
      if (typeof sellModal.close === "function") sellModal.close();
    });
  });
}

if (sellerForm) {
  sellerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const handle = (document.getElementById("seller-handle") || {}).value || "";
    const links = (document.getElementById("seller-links") || {}).value || "";
    const note = (document.getElementById("seller-note") || {}).value || "";
    const ack = !!(document.getElementById("seller-ack") || {}).checked;
    if (sellerSubmit) sellerSubmit.disabled = true;
    setSellerStatus(t("js.sell_wait"), "");
    try {
      const res = await fetch("/api/seller-apply", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          handle: handle.trim(),
          links,
          note: note.trim(),
          ack,
        }),
      });
      const data = await res.json();
      if (!res.ok || !data.ok) {
        setSellerStatus(data.error || t("js.sell_fail"), "err");
        return;
      }
      setSellerStatus(t("js.sell_ok"), "ok");
      sellerForm.reset();
    } catch (_) {
      setSellerStatus(t("js.net"), "err");
    } finally {
      if (sellerSubmit) sellerSubmit.disabled = false;
    }
  });
}

if (claimForm) {
  claimForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    setClaimStatus(t("js.claim_wait"), "");
    try {
      const res = await fetch("/api/claim", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: claimCode ? claimCode.value.trim() : "",
        }),
      });
      const data = await res.json();
      if (!res.ok || !data.ok) {
        setClaimStatus(data.error || t("js.claim_fail"), "err");
        return;
      }
      applySession(data);
      if (data.paid) {
        ping("claim_ok");
        startPaidLoop();
      }
      setClaimStatus(
        data.paid
          ? t("js.claim_ok", { clock: data.remaining_clock })
          : t("js.claim_empty"),
        data.paid ? "ok" : "err",
      );
    } catch (_) {
      setClaimStatus(t("js.net"), "err");
    }
  });
}

document.querySelectorAll("[data-copy]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      btn.textContent = t("js.copied");
      setTimeout(() => {
        btn.textContent = t("js.copy");
      }, 1400);
    } catch (_) {
      btn.textContent = t("js.copy_fail");
    }
  });
});

if (clockBtn) {
  clockBtn.addEventListener("click", (event) => {
    event.stopPropagation();
    setMenu(!menuOpen);
  });
}
if (btnNew) {
  btnNew.addEventListener("click", async () => {
    const data = await clockAction("new");
    if (data && data.ok) resetLog();
    setMenu(false);
  });
}
if (btnCopy) {
  btnCopy.addEventListener("click", () => copyLabel(btnCopy, resumeHref(lastSession), t("js.copy_link")));
}
if (resumeBack) {
  resumeBack.addEventListener("click", closeResume);
}
if (resumeCopyWeb) {
  resumeCopyWeb.addEventListener("click", () => {
    copyLabel(resumeCopyWeb, resumeWebCmd ? resumeWebCmd.textContent : "", t("js.copy"));
  });
}
if (resumeCopySsh) {
  resumeCopySsh.addEventListener("click", () => {
    copyLabel(resumeCopySsh, resumeSshCmd ? resumeSshCmd.textContent : "", t("js.copy"));
  });
}
if (resumeOpenWeb) {
  resumeOpenWeb.addEventListener("click", async () => {
    if (!resumeView) return;
    const id = resumeView.id;
    closeResume();
    const data = await clockAction("use", { id });
    if (data && data.ok) resetLog();
  });
}
if (resumeSheet) {
  resumeSheet.addEventListener("click", (event) => {
    if (event.target === resumeSheet) closeResume();
  });
}

document.addEventListener("click", (event) => {
  if (!menuOpen || !clockWrap) return;
  if (clockWrap.contains(event.target)) return;
  setMenu(false);
});

document.addEventListener("visibilitychange", () => {
  if (hint.dataset.paid !== "1") return;
  if (document.visibilityState === "visible") clockAction("tick");
});

(function rotateHero() {
  const el = document.getElementById("hero-line-text");
  if (!el) return;
  let lines = [];
  try {
    lines = JSON.parse(el.getAttribute("data-lines") || "[]");
  } catch (_) {
    lines = [];
  }
  if (lines.length < 2) return;
  let i = 0;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  setInterval(() => {
    i = (i + 1) % lines.length;
    if (reduced) {
      el.textContent = lines[i];
      return;
    }
    el.classList.add("is-out");
    setTimeout(() => {
      el.textContent = lines[i];
      el.classList.remove("is-out");
    }, 1100);
  }, 9000);
  document.addEventListener("st-locale", () => {
    try {
      lines = JSON.parse(el.getAttribute("data-lines") || "[]");
    } catch (_) {
      lines = [];
    }
    if (lines[0]) el.textContent = lines[0];
    i = 0;
  });
})();

document.addEventListener("st-locale", () => {
  if (lastSession) applySession(lastSession);
});

const params = new URLSearchParams(location.search);

const BRIEFS = { mkt: "brief.mkt", copy: "brief.copy", viral: "brief.viral" };

function briefText(key) {
  let text = t(`brief.${key}`);
  if (text === `brief.${key}`) text = "";
  const code = ((claimCode && claimCode.value) || params.get("code") || "").trim();
  if (text && /^wdtsot-[A-Za-z0-9]{3,16}$/.test(code)) {
    text += t("brief.invite", {
      url: `https://sparetoken.shop/?code=${encodeURIComponent(code)}`,
    });
  }
  return text;
}

function fillBrief(key) {
  const text = briefText(key);
  if (!text || !input) return;
  input.value = text;
  resize();
  input.focus();
  location.hash = "chat";
}

document.querySelectorAll("[data-brief]").forEach((el) => {
  const run = () => fillBrief(el.dataset.brief);
  el.addEventListener("click", run);
  el.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      run();
    }
  });
});

fetch("/api/track/summary", { credentials: "same-origin" })
  .then((res) => res.json())
  .then((data) => {
    if (!data || !data.ok) return;
    const box = document.getElementById("pulso-tally");
    if (!box) return;
    box.querySelectorAll("[data-tally]").forEach((node) => {
      const key = node.getAttribute("data-tally");
      if (key && Object.prototype.hasOwnProperty.call(data, key)) {
        node.textContent = String(data[key] || 0);
      }
    });
    box.hidden = false;
  })
  .catch(() => {});

captureLanding();
if (params.get("code") && claimCode && !claimCode.value) {
  claimCode.value = params.get("code");
}
ping("visit");

loadSession().then(() => {
  if (hint.dataset.paid === "1") startPaidLoop();
});
