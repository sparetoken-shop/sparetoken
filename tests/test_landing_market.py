"""Marketplace shelf: one R$5 card, a how-it-works rail — never 'alias'."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")
JS = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


class LandingMarketTest(unittest.TestCase):
    def test_brand_is_spare_tokens(self):
        self.assertIn("<title>spare tokens", HTML.lower())
        self.assertIn(">spare tokens<", HTML.lower())

    def test_nav_leads_with_marketplace(self):
        nav = HTML.split("<nav", 1)[1].split("</nav>", 1)[0]
        self.assertLess(nav.find("#mercado"), nav.find("#preco"))
        self.assertIn("#mercado", nav)
        self.assertIn("#terminal", nav)

    def test_public_copy_never_says_reseller_alias(self):
        self.assertNotIn("reseller alias", HTML.lower())
        self.assertNotIn("alias:", HTML.lower())

    def test_shelf_is_one_buy_card_not_a_dashed_twin(self):
        self.assertIn('id="mercado"', HTML)
        self.assertIn('class="shelf"', HTML)
        self.assertIn("shelf-card", HTML)
        self.assertIn('data-reseller="fuzzy"', HTML)
        self.assertIn("fuzzy", HTML)
        self.assertNotIn("shelf-card-open", HTML)
        self.assertNotIn("seu nome de reseller", HTML.lower())

    def test_shelf_rail_explains_without_a_second_sku(self):
        self.assertIn("shelf-rail", HTML)
        self.assertIn("wdtsot-", HTML)
        self.assertIn("?code=", HTML)

    def test_rail_copy_is_one_click_pix_not_a_heading_swap(self):
        """D8: track-report commands the rail. Heading and briefs stay."""
        import i18n

        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertIn("5h de GROK 4.6 High Fast. Sem cadastro", HTML)
        self.assertNotIn(">Pix. R$5.<", HTML)
        self.assertEqual(i18n.STRINGS["pt-BR"]["rail.1.t"], "um clique. Pix R$5.")
        self.assertIn("Sem cadastro", i18n.STRINGS["pt-BR"]["rail.1.p"])
        self.assertIn("one click", i18n.STRINGS["en-US"]["rail.1.t"].lower())
        self.assertIn("from ~$1", i18n.STRINGS["en-US"]["rail.1.t"])
        self.assertIn("no signup", i18n.STRINGS["en-US"]["rail.1.p"].lower())
        self.assertIn("we deserve to share our tokens", HTML.lower())
        self.assertIn("r$0,50 por 30 minutos", HTML.lower())
        self.assertIn('data-brief="mkt"', HTML)
        self.assertIn('data-brief="copy"', HTML)
        self.assertIn('data-brief="viral"', HTML)
        self.assertIn("10 amigos", HTML)
        self.assertIn("10 amigos", i18n.STRINGS["pt-BR"]["rail.3.p"])
        self.assertIn("10 friends", i18n.STRINGS["en-US"]["rail.3.p"].lower())

    def test_experiment_is_market_and_self_evolving_agent(self):
        blob = HTML.lower()
        self.assertIn("self-evolving", blob)
        self.assertIn("marketplace", blob)

    def test_market_section_invites(self):
        self.assertIn("10 links", HTML)
        self.assertIn("23:30", HTML)
        self.assertIn("#vender", HTML)
        self.assertIn("não é vapor", HTML.lower())

    def test_seller_cta_after_fuzzy_card(self):
        fuzzy = HTML.find('data-reseller="fuzzy"')
        article_end = HTML.find("</article>", fuzzy)
        cta = HTML.find("Venda seus tokens")
        rail = HTML.find("shelf-rail")
        self.assertGreater(fuzzy, 0)
        self.assertLess(article_end, cta)
        self.assertLess(cta, rail)
        self.assertIn('class="btn btn-sell"', HTML)
        self.assertIn('data-track="sell_click"', HTML)
        self.assertIn('id="vender"', HTML)
        self.assertIn(".btn-sell", CSS)
        self.assertIn("/api/seller-apply", JS)
        self.assertIn("/api/seller-apply", SERVER)

    def test_design_tokens_file_exists(self):
        tokens = Path(__file__).resolve().parents[1] / "static" / "tokens.css"
        self.assertTrue(tokens.is_file())
        self.assertIn("--paper", tokens.read_text(encoding="utf-8"))
        self.assertIn("tokens.css", CSS)

    def test_outbound_shop_links_keep_utm_hooks(self):
        self.assertIn("utm_source", HTML)
        self.assertIn("data-track", HTML)

    def test_claim_is_code_only_not_civil_identity(self):
        self.assertNotIn("claim-contact", HTML)
        self.assertNotIn("whatsapp", HTML.lower())
        self.assertNotIn("e-mail ou", HTML.lower())

    def test_hero_rotates_three_lines(self):
        self.assertIn("we deserve to share our tokens", HTML.lower())
        self.assertIn("r$0,50 por 30 minutos", HTML.lower())
        self.assertIn("pay quickly with pix and get going", HTML.lower())
        self.assertIn("hero-line", HTML)

    def test_three_short_agents_open_the_same_chat(self):
        self.assertIn('data-brief="mkt"', HTML)
        self.assertIn('data-brief="copy"', HTML)
        self.assertIn('data-brief="viral"', HTML)
        self.assertIn("is-live", HTML)
        self.assertIn("const BRIEFS", JS)
        self.assertNotIn("R$10", HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)

    def test_click_tally_is_public_counts_only(self):
        self.assertIn('id="pulso-tally"', HTML)
        self.assertIn("/api/track/summary", JS)
        self.assertIn("/api/track/summary", SERVER)
        self.assertIn("track.summarize", SERVER)

    def test_heartbeat_line_sits_with_the_tally(self):
        self.assertIn('id="pulso-heartbeat"', HTML)
        self.assertIn('data-pulse="ship"', HTML)
        self.assertIn('data-pulse="research"', HTML)
        self.assertIn('data-pulse="shelf"', HTML)
        self.assertIn("/api/heartbeat", JS)
        self.assertIn("pulso-heartbeat", JS)
        self.assertIn(".pulso-heartbeat", CSS)
        self.assertIn("data.shelf", JS)
        self.assertNotIn("conta.vc", JS.split("function fillPulse", 1)[1].split("fetch(", 1)[0])
        tally = HTML.find('id="pulso-tally"')
        pulse = HTML.find('id="pulso-heartbeat"')
        self.assertLess(HTML.find("shelf-rail"), tally)
        self.assertLess(tally, pulse)
        self.assertNotIn("import pay", (ROOT / "heartbeat_api.py").read_text())

    def test_d15_pulse_stays_under_tally_card_stays_rail(self):
        """D15 (13/09): visit rose, pay_click did not. Pulse stays under the
        tally (never hero); the card stays on the one-click rail."""
        self.assertEqual(HTML.count('id="pulso-heartbeat"'), 1)
        pulse = HTML.find('id="pulso-heartbeat"')
        tag_open = HTML.rfind("<p", 0, pulse)
        tag_end = HTML.find(">", pulse)
        self.assertIn('data-placement="under-tally"', HTML[tag_open:tag_end])
        hero = HTML.split('<section class="wrap hero">', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("pulso-heartbeat", hero)
        mercado = HTML.find('id="mercado"')
        tally = HTML.find('id="pulso-tally"')
        self.assertLess(mercado, tally)
        self.assertLess(tally, pulse)
        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)

    def test_d16_stock_stays_in_pulse_never_card(self):
        """D16 (14/09): pay_click stuck at 2, pool Open 0. The stock number
        stays in the pulse line (never the card, rail, or hero)."""
        import re

        self.assertEqual(HTML.count('data-pulse="shelf"'), 1)
        pulse = HTML.find('id="pulso-heartbeat"')
        tag_open = HTML.rfind("<p", 0, pulse)
        tag_end = HTML.find(">", pulse)
        self.assertIn('data-stock="pulse-only"', HTML[tag_open:tag_end])
        self.assertIn('data-placement="under-tally"', HTML[tag_open:tag_end])
        shelf_slot = HTML.find('data-pulse="shelf"')
        pulse_close = HTML.find("</p>", shelf_slot)
        self.assertLess(pulse, shelf_slot)
        self.assertLess(shelf_slot, pulse_close)
        shelf_block = HTML[HTML.find('id="mercado"') : HTML.find('id="pulso-tally"')]
        self.assertNotRegex(shelf_block, r"\d+\s+Open")
        hero = HTML.split('<section class="wrap hero">', 1)[1].split("</section>", 1)[0]
        self.assertNotRegex(hero, r"\d+\s+Open")
        self.assertIn('box.querySelector(\'[data-pulse="shelf"]\')', JS)
        self.assertNotIn('document.querySelector(\'[data-pulse="shelf"]\')', JS)
        self.assertIn('data-stock', JS)

    def test_d21_trap_chapter_closed_runtime_lock(self):
        """D21 (19/09): trap-test green, timer 7200s alive. PR #1 chapter
        closes. The pulse line only paints with data-trap=runtime."""
        self.assertEqual(HTML.count('data-trap="runtime"'), 1)
        pulse = HTML.find('id="pulso-heartbeat"')
        tag_open = HTML.rfind("<p", 0, pulse)
        tag_end = HTML.find(">", pulse)
        self.assertIn('data-trap="runtime"', HTML[tag_open:tag_end])
        self.assertIn('data-placement="under-tally"', HTML[tag_open:tag_end])
        self.assertIn('data-stock="pulse-only"', HTML[tag_open:tag_end])
        hero = HTML.split('<section class="wrap hero">', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("data-trap", hero)
        fn = JS.split("function fillPulse", 1)[1].split("fetch(", 1)[0]
        self.assertIn("data-trap", fn)
        self.assertIn("runtime", fn)
        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)

    def test_d22_skill_stays_optional_launcher_waits(self):
        """D22 (20/09): 0 extra-CLI applies. #vender skill stays optional.
        Live briefs stay cursor. No launch stub for a second CLI."""
        self.assertEqual(HTML.count('id="vender"'), 1)
        tag_open = HTML.find("<dialog")
        vender = HTML.find('id="vender"')
        tag_open = HTML.rfind("<dialog", 0, vender + 1)
        tag_end = HTML.find(">", vender)
        self.assertIn('data-skill="optional"', HTML[tag_open:tag_end])
        self.assertEqual(HTML.count('data-skill="optional"'), 1)
        for field_id in (
            "seller-skill-title",
            "seller-skill-manifesto",
            "seller-skill-cli",
        ):
            start = HTML.find(f'id="{field_id}"')
            self.assertGreater(start, 0)
            tag_end = HTML.find(">", start)
            self.assertNotIn("required", HTML[start:tag_end])
        self.assertEqual(HTML.count('data-cli="cursor"'), 3)
        self.assertNotIn('data-cli="codex"', HTML)
        self.assertNotIn('data-cli="claude"', HTML)
        fn = JS.split("if (sellerForm)", 1)[1].split("if (claimForm)", 1)[0]
        self.assertIn("data-skill", fn)
        self.assertIn("optional", fn)
        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)

    def test_d23_released_proof_sits_on_the_rail(self):
        """D23 (21/09): D19 never pulled the briefs; pay_click still 2.
        The card gets a short claim_ok proof on the rail (never hero,
        never Open stock on the card)."""
        self.assertEqual(HTML.count('data-proof="rail"'), 1)
        rail_open = HTML.find('class="shelf-rail"')
        self.assertGreater(rail_open, 0)
        tag_open = HTML.rfind("<ol", 0, rail_open + 1)
        tag_end = HTML.find(">", rail_open)
        self.assertIn('data-proof="rail"', HTML[tag_open:tag_end])
        rail_close = HTML.find("</ol>", rail_open)
        rail = HTML[tag_open:rail_close]
        self.assertIn('data-proof="released"', rail)
        self.assertIn("data-proof-n", rail)
        self.assertIn("blocos liberados", rail)
        self.assertIn("tally.blocks", rail)
        hero = HTML.split('<section class="wrap hero">', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("data-proof", hero)
        self.assertNotIn("data-proof-n", hero)
        shelf_block = HTML[HTML.find('id="mercado"') : HTML.find('id="pulso-tally"')]
        self.assertNotRegex(shelf_block, r"\d+\s+Open")
        fn = JS.split("function fillRailProof", 1)[1].split("fetch(", 1)[0]
        self.assertIn("data-proof", fn)
        self.assertIn("rail", fn)
        self.assertIn("claim_ok", fn)
        self.assertNotIn("data.shelf", fn)
        self.assertIn("fillRailProof", JS)
        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertIn('data-brief="mkt"', HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)
        self.assertIn(".rail-proof", CSS)

    def test_d27_briefs_stay_campaign_stamp_waits(self):
        """D27 (25/09): briefs stayed on the fold, pay_click still 2.
        The chat brief does not carry utm_content=mkt|copy|viral
        until the click moves. data-stamp=wait strips that link."""
        import i18n

        self.assertEqual(HTML.count('data-stamp="wait"'), 3)
        for key in ("mkt", "copy", "viral"):
            start = HTML.find(f'data-brief="{key}"')
            self.assertGreater(start, 0)
            tag_open = HTML.rfind("<article", 0, start)
            tag_end = HTML.find(">", start)
            tag = HTML[tag_open:tag_end]
            self.assertIn('data-stamp="wait"', tag)
            self.assertIn('data-cli="cursor"', tag)
            self.assertIn("is-live", tag)
        design = HTML.find('data-i18n="skill.design.t"')
        soon_open = HTML.rfind("<article", 0, design)
        soon_end = HTML.find(">", design)
        self.assertNotIn("data-stamp", HTML[soon_open:soon_end])
        self.assertNotIn("data-brief", HTML[soon_open:soon_end])
        fn = JS.split("function briefText", 1)[1].split("function fillBrief", 1)[0]
        self.assertIn("data-stamp", fn)
        self.assertIn("wait", fn)
        self.assertIn("utm_content=(?:mkt|copy|viral)", fn)
        self.assertNotIn("utm_content=${", fn)
        self.assertNotIn("utm_content=copy", fn)
        self.assertNotIn("utm_content=viral", fn)
        for loc in ("pt-BR", "en-US"):
            pack = i18n.STRINGS[loc]
            self.assertIn("utm_content=mkt", pack["brief.mkt"])
            self.assertNotIn("utm_content=", pack["brief.copy"])
            self.assertNotIn("utm_content=", pack["brief.viral"])
        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)

    def test_d24_zero_pool_keeps_restock_and_rail_stays(self):
        """D24 (22/09): Mac refill did not land (pool Open 0).
        The pulse keeps 0 Open · restock. The rail stays visible.
        A recovered pool (>=3) shows N Open without the restock suffix."""
        self.assertEqual(HTML.count('data-refill="pending"'), 1)
        pulse = HTML.find('id="pulso-heartbeat"')
        tag_open = HTML.rfind("<p", 0, pulse)
        tag_end = HTML.find(">", pulse)
        tag = HTML[tag_open:tag_end]
        self.assertIn('data-refill="pending"', tag)
        self.assertIn('data-stock="pulse-only"', tag)
        self.assertIn('data-placement="under-tally"', tag)
        rail_open = HTML.find('class="shelf-rail"')
        rail_tag_open = HTML.rfind("<ol", 0, rail_open + 1)
        rail_tag_end = HTML.find(">", rail_open)
        rail_tag = HTML[rail_tag_open:rail_tag_end]
        self.assertIn('data-rail="stays"', rail_tag)
        self.assertNotIn("hidden", rail_tag)
        hero = HTML.split('<section class="wrap hero">', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("data-refill", hero)
        self.assertNotIn("data-rail", hero)
        shelf_block = HTML[HTML.find('id="mercado"') : HTML.find('id="pulso-tally"')]
        self.assertNotRegex(shelf_block, r"\d+\s+Open")
        fn = JS.split("function fillPulse", 1)[1].split("fetch(", 1)[0]
        self.assertIn("data-refill", fn)
        self.assertIn("pending", fn)
        self.assertIn("0 Open · restock", fn)
        self.assertIn("n >= 3", fn)
        self.assertIn("data-rail", fn)
        self.assertIn("stays", fn)
        self.assertIn("rail.hidden = false", fn)
        self.assertIn('.shelf-rail[data-rail="stays"]', CSS)
        self.assertIn("um clique. Pix R$5.", HTML)
        self.assertEqual(HTML.count('id="pay"'), 1)

    def test_mobile_puts_chat_first_and_hides_demo_term(self):
        mobile = CSS.split("@media (max-width: 860px)", 1)[1]
        self.assertIn(".hero > .chat", mobile)
        self.assertIn("order: 1", mobile)
        self.assertIn(".term { display: none; }", mobile)
        self.assertNotIn(".header-links { display: none; }", mobile)

    def test_faq_is_machine_citable_without_a_second_sku(self):
        self.assertIn("application/ld+json", HTML)
        self.assertIn("FAQPage", HTML)
        self.assertIn('id="faq"', HTML)
        faq = HTML.split('id="faq"', 1)[1].lower()
        self.assertIn("r$5", faq)
        self.assertNotIn("plano mensal", faq)
        self.assertNotIn("reseller alias", faq)
        self.assertIn("como vendo meus tokens", faq)
