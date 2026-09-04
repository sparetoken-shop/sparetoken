/* Locale switch: Brazil / United States. Server paints first. This keeps JS in sync. */
(function () {
  const boot = window.__I18N__ || {
    locale: document.documentElement.lang === "en" ? "en-US" : "pt-BR",
    lang: document.documentElement.lang || "pt-BR",
    lines: [],
    strings: {},
  };

  function format(text, vars) {
    if (!vars) return text;
    return String(text).replace(/\{(\w+)\}/g, (_, key) =>
      Object.prototype.hasOwnProperty.call(vars, key) ? String(vars[key]) : `{${key}}`,
    );
  }

  function t(key, vars) {
    const pack = window.__I18N__ || boot;
    const table = pack.strings || {};
    const raw = table[key];
    if (raw == null) return key;
    return format(raw, vars);
  }

  function setAttr(el, name, value) {
    el.setAttribute(name, value);
  }

  function applyPack(pack) {
    window.__I18N__ = pack;
    document.documentElement.lang = pack.lang || (pack.locale === "en-US" ? "en" : "pt-BR");
    document.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      if (key && pack.strings[key] != null) el.innerHTML = pack.strings[key];
    });
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (key && pack.strings[key] != null) el.textContent = pack.strings[key];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      const key = el.getAttribute("data-i18n-placeholder");
      if (key && pack.strings[key] != null) el.setAttribute("placeholder", pack.strings[key]);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const key = el.getAttribute("data-i18n-aria");
      if (key && pack.strings[key] != null) el.setAttribute("aria-label", pack.strings[key]);
    });
    document.querySelectorAll("[data-i18n-title]").forEach((el) => {
      const key = el.getAttribute("data-i18n-title");
      if (key && pack.strings[key] != null) el.setAttribute("title", pack.strings[key]);
    });
    const hero = document.getElementById("hero-line-text");
    if (hero && pack.lines && pack.lines.length) {
      hero.setAttribute("data-lines", JSON.stringify(pack.lines));
      hero.textContent = pack.lines[0];
    }
    const title = document.querySelector("title");
    if (title && pack.strings.title) title.textContent = pack.strings.title;
    const desc = document.querySelector('meta[name="description"]');
    if (desc && pack.strings.description) desc.setAttribute("content", pack.strings.description);
    document.querySelectorAll(".flag[data-locale]").forEach((btn) => {
      const on = btn.getAttribute("data-locale") === pack.locale;
      btn.classList.toggle("is-on", on);
      setAttr(btn, "aria-pressed", on ? "true" : "false");
    });
    document.dispatchEvent(new CustomEvent("st-locale", { detail: pack }));
  }

  async function choose(locale) {
    try {
      const res = await fetch("/api/locale", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ locale }),
      });
      const data = await res.json();
      if (data && data.ok && data.strings) {
        applyPack(data);
        const url = new URL(location.href);
        url.searchParams.set("lang", locale === "en-US" ? "en" : "pt");
        history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
        return;
      }
    } catch (_) {}
    location.search = `?lang=${locale === "en-US" ? "en" : "pt"}`;
  }

  function bindFlags() {
    document.querySelectorAll(".flag[data-locale]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const locale = btn.getAttribute("data-locale");
        if (!locale || locale === (window.__I18N__ && window.__I18N__.locale)) return;
        choose(locale);
      });
    });
  }

  window.ST = {
    t,
    applyPack,
    choose,
    locale() {
      return (window.__I18N__ && window.__I18N__.locale) || boot.locale;
    },
  };

  if (window.__I18N__ && window.__I18N__.strings) applyPack(window.__I18N__);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindFlags);
  } else {
    bindFlags();
  }
})();
