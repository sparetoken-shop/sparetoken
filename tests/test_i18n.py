"""Brazil / United States locales. IP picks the first paint. Cookie wins."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import i18n

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")
JS = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
I18N_JS = (ROOT / "static" / "i18n.js").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")
GEO = ROOT / "geo" / "br-ranges.bin.gz"


class LocaleDetectTest(unittest.TestCase):
    def test_brazil_ip_is_portuguese(self):
        info = i18n.resolve_locale(ip="200.160.0.8")
        self.assertEqual(info["locale"], "pt-BR")
        self.assertEqual(info["country"], "BR")
        self.assertEqual(info["flag"], "BR")
        self.assertEqual(info["source"], "ip")

    def test_us_ip_is_english(self):
        info = i18n.resolve_locale(ip="8.8.8.8")
        self.assertEqual(info["locale"], "en-US")
        self.assertEqual(info["flag"], "US")
        self.assertEqual(info["source"], "ip")
        self.assertNotEqual(info["country"], "BR")

    def test_other_public_ip_is_the_international_english(self):
        info = i18n.resolve_locale(ip="1.1.1.1")
        self.assertEqual(info["locale"], "en-US")

    def test_brazil_ipv6_is_portuguese(self):
        info = i18n.resolve_locale(ip="2804:14c:85:80a1::")
        self.assertEqual(info["locale"], "pt-BR")
        self.assertEqual(info["country"], "BR")

    def test_cookie_beats_ip(self):
        info = i18n.resolve_locale(ip="8.8.8.8", cookie="pt-BR")
        self.assertEqual(info["locale"], "pt-BR")
        self.assertEqual(info["source"], "cookie")

    def test_query_beats_cookie(self):
        info = i18n.resolve_locale(ip="200.160.0.8", cookie="pt-BR", query="lang=en")
        self.assertEqual(info["locale"], "en-US")
        self.assertEqual(info["source"], "query")

    def test_private_ip_falls_to_accept_language(self):
        info = i18n.resolve_locale(ip="127.0.0.1", accept_language="en-US,en;q=0.8")
        self.assertEqual(info["locale"], "en-US")
        self.assertEqual(info["source"], "accept-language")

    def test_unknown_defaults_to_home_market(self):
        info = i18n.resolve_locale(ip="10.0.0.2")
        self.assertEqual(info["locale"], "pt-BR")
        self.assertEqual(info["source"], "default")

    def test_country_header_wins_over_bad_ip(self):
        info = i18n.resolve_locale(ip="127.0.0.1", headers={"CF-IPCountry": "US"})
        self.assertEqual(info["locale"], "en-US")
        self.assertEqual(info["source"], "header-country")


class CatalogTest(unittest.TestCase):
    def test_both_locales_share_the_same_keys(self):
        self.assertEqual(set(i18n.STRINGS["pt-BR"]), set(i18n.STRINGS["en-US"]))

    def test_english_is_not_a_thin_overlay(self):
        en = i18n.STRINGS["en-US"]
        self.assertIn("Try it now", en["hero.try"])
        self.assertIn("Sell your tokens", en["sell.cta"])
        self.assertIn("How much does it cost?", en["faq.q1"])
        self.assertNotIn("Experimentar agora", en["hero.try"])
        self.assertNotIn("Venda seus tokens", en["sell.cta"])

    def test_sku_does_not_grow_a_second_till(self):
        blob = " ".join(i18n.STRINGS["en-US"].values()).lower()
        self.assertIn("r$5", blob)
        self.assertNotIn("r$10", blob)
        self.assertNotIn("usdt checkout", blob)
        self.assertNotIn("second till", blob.replace("no second till", ""))


class HtmlApplyTest(unittest.TestCase):
    def test_source_html_stays_portuguese_for_file_tests(self):
        self.assertIn("Venda seus tokens", HTML)
        self.assertIn("manda este link", HTML)
        self.assertIn("não é vapor", HTML.lower())
        self.assertIn('data-locale="pt-BR"', HTML)
        self.assertIn('data-locale="en-US"', HTML)
        self.assertIn("hreflang=\"en-US\"", HTML)
        self.assertIn("hreflang=\"pt-BR\"", HTML)

    def test_english_render_flips_visible_copy(self):
        out = i18n.apply_html(HTML, "en-US")
        self.assertIn('lang="en"', out)
        self.assertIn("Try it now", out)
        self.assertIn("Sell your tokens", out)
        self.assertIn("How much does it cost?", out)
        self.assertNotIn("Experimentar agora", out)
        self.assertIn('data-locale="en-US"', out)
        self.assertIn("is-on", out)
        self.assertIn("R$0.50 for 30 minutes", out)

    def test_portuguese_render_keeps_the_shelf(self):
        out = i18n.apply_html(HTML, "pt-BR")
        self.assertIn("Venda seus tokens", out)
        self.assertIn("manda este link", out)
        self.assertIn('lang="pt-BR"', out)

    def test_nested_html_keys_keep_links(self):
        out = i18n.apply_html(HTML, "en-US")
        self.assertIn('href="#vender"', out)
        self.assertIn("sparetoken.shop/?code=", out)
        self.assertIn("@sparetoken", out)


class SurfaceTest(unittest.TestCase):
    def test_geo_table_is_vendored(self):
        self.assertTrue(GEO.is_file())
        self.assertGreater(GEO.stat().st_size, 10000)

    def test_server_wires_locale_routes(self):
        self.assertIn("import i18n", SERVER)
        self.assertIn("/api/locale", SERVER)
        self.assertIn("/i18n-boot.js", SERVER)
        self.assertIn("i18n.apply_html", SERVER)

    def test_flags_are_in_the_header_not_a_select(self):
        self.assertIn("locale-switch", HTML)
        self.assertIn("locale-switch", CSS)
        self.assertIn(".flag.is-on", CSS)
        self.assertNotIn("<select", HTML)

    def test_js_uses_the_catalog_not_a_second_sku(self):
        self.assertIn("function t(", JS)
        self.assertIn("const BRIEFS", JS)
        self.assertIn("/api/locale", I18N_JS)
        self.assertNotIn("R$10", JS)


if __name__ == "__main__":
    unittest.main()
