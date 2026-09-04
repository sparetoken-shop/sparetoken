"""Two locales only: Brazil (pt-BR) and United States (en-US).

IP of the device picks the first paint. Cookie and ?lang= win after that.
Brazil → Portuguese. Everywhere else → English (US flag).
"""

from __future__ import annotations

import gzip
import ipaddress
import json
import re
import struct
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parent
GEO = ROOT / "geo" / "br-ranges.bin.gz"

COOKIE = "wdtsot_lang"
LOCALES = ("pt-BR", "en-US")
DEFAULT = "pt-BR"
HTML_LANG = {"pt-BR": "pt-BR", "en-US": "en"}
HREFLANG = {"pt-BR": "pt-BR", "en-US": "en-US"}

# Gold-standard catalog. Source HTML stays Portuguese so existing file tests hold.
STRINGS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "spare tokens — we deserve to share our tokens",
        "description": "Marketplace de token sobrando. Cards de R$5 · 5h. Pix, convite ?code=, reseller fuzzy. Sem mensalidade.",
        "locale.aria": "Idioma",
        "locale.br": "Brasil",
        "locale.us": "Estados Unidos",
        "nav.market": "Mercado",
        "nav.price": "R$5 / 5h",
        "nav.terminal": "Terminal",
        "nav.faq": "FAQ",
        "hero.kicker": "GROK 4.6 High Fast",
        "hero.line": "we deserve to share our tokens.",
        "hero.lede": "Five hours. Five reais.",
        "hero.sub": "As 5h são o tempo que o GROK ficou pensando — não o tempo da aba aberta, nem o que você leva digitando.",
        "hero.try": "Experimentar agora",
        "hero.terminal": ">_ Terminal",
        "term.remaining": "remaining",
        "term.processed": "processed",
        "chat.sys": "Comece por qualquer coisa. Uma ideia, um texto, um problema.",
        "chat.placeholder": "Pergunte ou peça o que quiser...",
        "chat.send": "Enviar",
        "chat.hint50": "50 mensagens para experimentar",
        "clock.chat1": "Chat 1",
        "clock.new": "Novo chat",
        "clock.copy": "Copiar link",
        "resume.back": "Fechar",
        "resume.name": "Chat",
        "resume.web": "web",
        "resume.ssh": "ssh",
        "resume.copy": "copiar",
        "resume.open": "abrir",
        "market.kicker": "marketplace",
        "market.h2": "cinco reais na prateleira.",
        "market.muted": "Um card. Um reseller. Pix de um passo. O primeiro nome na mesa é <strong>fuzzy</strong>.",
        "price.model": "5 horas · GROK 4.6 High Fast",
        "check.1": "digitar o prompt não desconta",
        "check.2": "aba aberta não desconta",
        "check.3": "vários chats somam no mesmo código",
        "check.4": "web ou SSH, mesma carteira",
        "pay": "Pagar R$5",
        "paid_already": "Já paguei",
        "pay.note": "Pix de um passo. O código do bloco é o login — e o mesmo <code>?code=</code> é o convite.",
        "pay.noscript": "Abrir pagamento R$5",
        "block.keep": "guarde este código:",
        "invite.send": "manda este link:",
        "invite.copy": "copiar",
        "referral.note": "10% em compute · Pix aos R$5 · primeiro indicador: fuzzy",
        "claim.label": "código do bloco ou link do Pix",
        "claim.placeholder": "wdtsot-7K2M ou o link que você pagou",
        "claim.submit": "Liberar sessão",
        "sell.kicker": "hora sobrando?",
        "sell.copy": "O mesmo card R$5 / 5h. Primeiro na prateleira continua <strong>fuzzy</strong>.",
        "sell.cta": "Venda seus tokens",
        "rail.1.k": "01 · paga",
        "rail.1.t": "Pix. R$5.",
        "rail.1.p": "Sem recorrência. Sem segundo caixa.",
        "rail.2.k": "02 · guarda",
        "rail.2.t": "wdtsot-XXXX",
        "rail.2.p": "O código do bloco é o login das 5h.",
        "rail.3.k": "03 · indica",
        "rail.3.t": "o mesmo ?code=",
        "rail.3.p": "10% em compute. Pix aos R$5. Primeiro indicador: fuzzy.",
        "shelf.open": "O próximo card não é vapor: <a href=\"#vender\">venda seus tokens</a> — SSH + <strong>10 links</strong> conta.vc. Heartbeat todo dia às <strong>23:30</strong> — <a href=\"https://x.com/sparetoken?utm_source=shop&amp;utm_medium=web&amp;utm_campaign=shelf\" data-track=\"out-x\">@sparetoken</a>.",
        "tally.visits": "visitas",
        "tally.pix": "cliques Pix",
        "tally.blocks": "blocos liberados",
        "tally.sell": "quero vender",
        "term.kicker": "experiência dois",
        "term.h2": "SSH is one command away.",
        "term.note": "Use it from the browser. Or don’t. The same model, in an isolated workspace — not an open Linux shell.",
        "term.copy": "copiar",
        "term.sshnote": "O SSH pede só o código do bloco (wdtsot-XXXX). Se ainda não pagou, mostra um Pix Open. Depois de pagar, a mesma carteira das 5h — só o tempo de processamento do modelo. O mesmo código indica um amigo.",
        "why.kicker": "por quê",
        "why.h2": "um caderno, não um pitch.",
        "why.1": "We work with AI every day. We pay for compute every month.",
        "why.2": "Some days we use everything. Some days we don’t. Either way, unused capacity disappears.",
        "why.3": "That feels wasteful.",
        "why.4": "The experiment has two axes: a marketplace of leftover tokens, and a self-evolving agent that ships every night at 23:30.",
        "why.5": "We think useful intelligence should be easier to access, skills should be easier to share, and experimentation should be cheap.",
        "why.sign": "we deserve to share.",
        "skills.kicker": "prateleira",
        "skills.h2": "três agents curtos — o resto ainda chega.",
        "skills.muted": "Skill = manifesto curto + quais CLIs podem rodá-lo: cursor, codex, claude, antigravity, metamuse. Clique e o brief cai no mesmo chat. O caixa continua R$5 / 5h. Sem segundo preço.",
        "skill.use": "usar no chat",
        "skill.soon": "em breve",
        "skill.mkt.t": "Post curto",
        "skill.mkt.p": "280 caracteres. R$5 / 5h. Sem cara. O mesmo Pix.",
        "skill.copy.t": "Texto de prateleira",
        "skill.copy.p": "Um parágrafo. Token sobrando. Sem assinatura.",
        "skill.viral.t": "Gancho de convite",
        "skill.viral.p": "3 linhas. O convite é o mesmo ?code=.",
        "skill.design.t": "Design Critic",
        "skill.design.p": "olhar frio para layout e tipo.",
        "skill.image.t": "Image Prompt Director",
        "skill.image.p": "direção visual, não prompt soup.",
        "skill.research.t": "Research Agent",
        "skill.research.p": "perguntas melhores, fontes mais limpas.",
        "faq.kicker": "perguntas",
        "faq.h2": "sem cadastro. sem plano.",
        "faq.q1": "Quanto custa?",
        "faq.a1": "R$5 por 5 horas de GROK 4.6 High Fast. Pix de um passo. Sem mensalidade.",
        "faq.q2": "Como entro depois de pagar?",
        "faq.a2": "O código do bloco (<code>wdtsot-XXXX</code>) é o login na web e no SSH. O mesmo <code>?code=</code> indica um amigo.",
        "faq.q3": "Como indico um amigo?",
        "faq.a3": "O mesmo código do bloco. O link é <code>sparetoken.shop/?code=wdtsot-XXXX</code>. 10% (R$0,50) em compute por amigo que fechou o Pix. Pix aos R$5. O primeiro indicador é fuzzy. Sem e-mail.",
        "faq.q4": "O que é um skill na prateleira?",
        "faq.a4": "Um manifesto curto e o allowlist de CLI (cursor, codex, claude, antigravity, metamuse). O Pix continua R$5 / 5h. Sem segundo caixa.",
        "faq.q5": "O que os agents curtos fazem?",
        "faq.a5": "Post, prateleira, convite. Abrem no chat de cima. Não abrem outro caixa.",
        "faq.q6": "Como vendo meus tokens?",
        "faq.a6": "O mesmo card R$5 / 5h. Dez links conta.vc no painel <a href=\"#vender\">Venda seus tokens</a>. O primeiro nome na prateleira continua fuzzy. O pedido entra em revisão — o estoque é sagrado. Sem segundo caixa.",
        "split.open.h": "Built in the open.",
        "split.open.p": "The interface, session layer and skill format are designed to be inspectable, forkable and improvable. Código em <a href=\"https://github.com/sparetoken-shop/sparetoken?utm_source=shop&amp;utm_medium=web&amp;utm_campaign=home\" data-track=\"out-gh\">github.com/sparetoken-shop/sparetoken</a>.",
        "split.privacy.h": "Privacy by default.",
        "split.privacy.p": "Não vendemos conversas. Não mostramos a de um visitante para outro. Não há prompt escondido colhendo a sua chave. O contrato de privacidade está no repo: github.com/sparetoken-shop/sparetoken.",
        "final.h2": "Useful intelligence should be easier to access.",
        "final.p": "Fifty prompts in the browser. Or one SSH command, when you want the long table.",
        "exp.kicker": "se você leu até aqui",
        "exp.h2": "esperamos que este produto não te incomode.",
        "exp.1": "Ele é um experimento. Cinco reais por cinco horas de um modelo de fronteira é barato — é dado, é quase de graça. A ideia é, quando for possível e quando houver folga, compartilhar um pouco dos tokens com os amigos. Não transformar isso num negócio para escalar sem limite.",
        "exp.2": "O outro eixo é o mercado: um card na prateleira, um nome de reseller, o mesmo Pix. E o self-evolving agent que, toda noite, tenta deixar a prateleira um pouco menos vazia.",
        "footer.1": "spare tokens · we deserve to share our tokens.",
        "footer.2": "marketplace · reseller fuzzy · <a href=\"https://x.com/sparetoken?utm_source=shop&amp;utm_medium=web&amp;utm_campaign=footer\" data-track=\"out-x\">@sparetoken</a> · 23:30",
        "modal.pay.h": "Antes do Pix",
        "modal.pay.p": "O link do conta.vc (fuzzy) só cobra. Ele <strong>não</strong> libera o GROK sozinho.",
        "modal.pay.1": "Pague e espere o Pix confirmar.",
        "modal.pay.2": "Volte nesta página.",
        "modal.pay.3": "Clique em <strong>Já paguei</strong> com o código <strong>wdtsot-XXXX</strong>.",
        "modal.pay.4": "Guarde o código <strong>wdtsot-XXXX</strong> — é o login das 5h, na web e no SSH.",
        "modal.pay.note": "Conta só o tempo que o GROK 4.6 High Fast fica gerando a resposta.",
        "modal.pay.later": "agora não",
        "modal.pay.ok": "entendi, abrir o Pix",
        "sell.close": "fechar",
        "sell.h3": "Venda seus tokens",
        "sell.lead": "Tem hora GROK sobrando? Coloca na prateleira. O mesmo card: R$5 / 5h. O primeiro nome na mesa continua <strong>fuzzy</strong>.",
        "sell.t1": "Isto é um mercado-experimento. Você lista compute pessoal que sobrou — acesso por código de carteira, web ou SSH. Não é um contrato de nuvem.",
        "sell.t2": "Os links Pix (conta.vc) são seus. Imposto, reembolso, chargeback e o que rodar na sua máquina também. A responsabilidade é sua.",
        "sell.t3": "A prateleira, o shop e os agents não guardam dinheiro, não prometem uptime, não mediamos briga entre quem compra e quem vende. Não respondemos por sessão SSH, perda de dado, ou por conta.vc / o modelo cair.",
        "sell.t4": "Quem compra paga Pix no seu link. Liberar o GROK segue o fluxo de sempre: charge fechado, código <code>wdtsot-XXXX</code>.",
        "sell.t5": "Você afirma que a capacidade é sua e que não vai vender o que não consegue cumprir.",
        "sell.handle": "apelido na prateleira (minúsculo, curto — sem @, sem telefone)",
        "sell.links": "10 links conta.vc (um por linha)",
        "sell.note": "nota (opcional)",
        "sell.note.ph": "fim de semana, fuso BRT…",
        "sell.ack": "Li e aceito os termos. A responsabilidade é minha.",
        "sell.submit": "Enviar para revisão",
        "sell.ssh.k": "como entra no SSH",
        "sell.ssh.1": "O produto é um comando. Sem app para baixar.",
        "sell.ssh.2": "macOS e Linux: o comando acima. Windows: Windows Terminal ou OpenSSH — o mesmo comando.",
        "sell.ssh.3": "Enter vazio no login = Pix ainda Open. Depois de pagar, o código <code>wdtsot-XXXX</code> é o login — web e SSH. Conta só o tempo que o modelo gera.",
        "sell.ssh.4": "<a href=\"#terminal\">seção Terminal</a> — a mesma mesa, sem segundo caixa.",
        "js.copied": "copiado",
        "js.copy_fail": "selecione e copie",
        "js.copy": "copiar",
        "js.copy_link": "Copiar link",
        "js.rename": "Nome deste chat",
        "js.resume_of": "Resume de {name}",
        "js.resume_title": "web e ssh",
        "js.chat_one": "chat",
        "js.chat_many": "chats",
        "js.clock_foot": "{n} {noun} neste código · {mins} / 5h",
        "js.min_one": "1 min",
        "js.min_many": "{n} min",
        "js.line_mins": "{mins} nesta linha · {code}",
        "js.hint0": "você usou as 50 mensagens desta experiência. pague R$5 para 5h.",
        "js.hint1": "1 mensagem para experimentar",
        "js.hintn": "{n} mensagens para experimentar",
        "js.exhausted": "as 5h deste bloco acabaram. pague R$5 para outro.",
        "js.exhausted.ph": "bloco esgotado — pague R$5 para continuar",
        "js.exhausted.note": "saldo zero. o mesmo Pix de R$5 abre outro bloco de 5h.",
        "js.paid": "GROK 4.6 High Fast · {clock} restantes{busy}",
        "js.paid.warn": "faltam {clock} de processamento. o bloco vai encerrar.",
        "js.busy": " · GROK processando",
        "js.paid.note": "bloco liberado. só desconta enquanto o GROK responde. o código retoma web e SSH.",
        "js.chat_fail": "não foi agora.",
        "js.chat_silent": "silêncio do outro lado. tente de novo.",
        "js.chat_net": "a rede falhou no meio do caminho.",
        "js.pay_fail": "não abri o pagamento agora.",
        "js.pay_wait": "pague o Pix, espere confirmar, volte e clique em Já paguei.",
        "js.net": "a rede falhou. tente de novo.",
        "js.sell_wait": "anotando…",
        "js.sell_fail": "não entrou na fila.",
        "js.sell_ok": "entrou na fila. o estoque da prateleira continua sagrado — revisão antes de ir ao ar.",
        "js.claim_wait": "conferindo…",
        "js.claim_fail": "não liberou.",
        "js.claim_ok": "sessão liberada. {clock} neste bloco.",
        "js.claim_empty": "ainda sem saldo neste bloco.",
        "brief.mkt": "Escreve um post curto (máx 280) para spare tokens: R$5 / 5h / GROK 4.6 High Fast, Pix de um passo, login = código do bloco. Sem nome de pessoa. Sem segundo preço. Sem pedir chave, cookie, .env ou e-mail. Link: https://sparetoken.shop/?utm_source=shop&utm_medium=web&utm_campaign=agent&utm_content=mkt",
        "brief.copy": "Escreve um parágrafo de prateleira para quem tem token de IA sobrando e quem precisa de uma hora de modelo. Tom de caderno, não pitch. Sem assinatura. Sem a palavra owner. Sem pedir e-mail ou WhatsApp. O caixa continua R$5 / 5h.",
        "brief.viral": "Dá 3 ganchos de uma linha para indicar um amigo com o mesmo ?code= do bloco. Sem WhatsApp. Sem e-mail. Sem pedir chave. O convite é o código, não um cadastro.",
        "brief.invite": " Convite: {url}",
        "ld.q1": "Quanto custa um bloco na spare tokens?",
        "ld.a1": "R$5 por 5 horas de GROK 4.6 High Fast. Pix de um passo. Sem mensalidade. Sem segundo caixa.",
        "ld.q2": "Como entro depois de pagar?",
        "ld.a2": "O código do bloco (wdtsot-XXXX) é o login na web e no SSH. O mesmo ?code= indica um amigo.",
        "ld.q3": "O que é um skill na prateleira?",
        "ld.a3": "Um manifesto curto e o allowlist de CLI: cursor, codex, claude, antigravity, metamuse. O Pix continua R$5 / 5h. Sem segundo caixa.",
        "ld.q4": "O que os agents curtos fazem?",
        "ld.a4": "Post curto, texto de prateleira e gancho de convite. Abrem no mesmo chat. O caixa continua R$5 / 5h.",
        "ld.q5": "Como indico um amigo?",
        "ld.a5": "O mesmo código do bloco. O link é sparetoken.shop/?code=wdtsot-XXXX. 10% (R$0,50) em compute por amigo que fechou o Pix. Pix aos R$5. O primeiro indicador é fuzzy. Sem e-mail.",
        "ld.q6": "Como vendo meus tokens?",
        "ld.a6": "O mesmo card R$5 / 5h. Dez links conta.vc. O primeiro nome na prateleira continua fuzzy. O pedido entra em revisão — o estoque da loja é sagrado. Sem segundo caixa.",
    },
    "en-US": {
        "title": "spare tokens — we deserve to share our tokens",
        "description": "Leftover-token marketplace. R$5 · 5h cards. Pix, invite ?code=, reseller fuzzy. No subscription.",
        "locale.aria": "Language",
        "locale.br": "Brazil",
        "locale.us": "United States",
        "nav.market": "Market",
        "nav.price": "R$5 / 5h",
        "nav.terminal": "Terminal",
        "nav.faq": "FAQ",
        "hero.kicker": "GROK 4.6 High Fast",
        "hero.line": "we deserve to share our tokens.",
        "hero.lede": "Five hours. Five reais.",
        "hero.sub": "The 5 hours are the time GROK spent thinking — not the tab left open, and not the time you spend typing.",
        "hero.try": "Try it now",
        "hero.terminal": ">_ Terminal",
        "term.remaining": "remaining",
        "term.processed": "processed",
        "chat.sys": "Start with anything. An idea, a draft, a problem.",
        "chat.placeholder": "Ask or request whatever you need...",
        "chat.send": "Send",
        "chat.hint50": "50 messages to try it",
        "clock.chat1": "Chat 1",
        "clock.new": "New chat",
        "clock.copy": "Copy link",
        "resume.back": "Close",
        "resume.name": "Chat",
        "resume.web": "web",
        "resume.ssh": "ssh",
        "resume.copy": "copy",
        "resume.open": "open",
        "market.kicker": "marketplace",
        "market.h2": "five reais on the shelf.",
        "market.muted": "One card. One reseller. One-step Pix. The first name on the table is <strong>fuzzy</strong>.",
        "price.model": "5 hours · GROK 4.6 High Fast",
        "check.1": "typing the prompt does not bill",
        "check.2": "an open tab does not bill",
        "check.3": "several chats share the same code",
        "check.4": "web or SSH, same wallet",
        "pay": "Pay R$5",
        "paid_already": "I already paid",
        "pay.note": "One-step Pix. The block code is the login — and the same <code>?code=</code> is the invite.",
        "pay.noscript": "Open R$5 payment",
        "block.keep": "keep this code:",
        "invite.send": "send this link:",
        "invite.copy": "copy",
        "referral.note": "10% in compute · Pix at R$5 · first indicator: fuzzy",
        "claim.label": "block code or Pix link",
        "claim.placeholder": "wdtsot-7K2M or the link you paid",
        "claim.submit": "Unlock session",
        "sell.kicker": "hours left over?",
        "sell.copy": "The same R$5 / 5h card. First name on the shelf stays <strong>fuzzy</strong>.",
        "sell.cta": "Sell your tokens",
        "rail.1.k": "01 · pay",
        "rail.1.t": "Pix. R$5.",
        "rail.1.p": "No subscription. No second till.",
        "rail.2.k": "02 · keep",
        "rail.2.t": "wdtsot-XXXX",
        "rail.2.p": "The block code is the 5-hour login.",
        "rail.3.k": "03 · invite",
        "rail.3.t": "the same ?code=",
        "rail.3.p": "10% in compute. Pix at R$5. First indicator: fuzzy.",
        "shelf.open": "The next card is not vapor: <a href=\"#vender\">sell your tokens</a> — SSH + <strong>10</strong> conta.vc links. Heartbeat every day at <strong>23:30</strong> — <a href=\"https://x.com/sparetoken?utm_source=shop&amp;utm_medium=web&amp;utm_campaign=shelf\" data-track=\"out-x\">@sparetoken</a>.",
        "tally.visits": "visits",
        "tally.pix": "Pix clicks",
        "tally.blocks": "blocks unlocked",
        "tally.sell": "want to sell",
        "term.kicker": "second experience",
        "term.h2": "SSH is one command away.",
        "term.note": "Use it from the browser. Or don’t. The same model, in an isolated workspace — not an open Linux shell.",
        "term.copy": "copy",
        "term.sshnote": "SSH asks only for the block code (wdtsot-XXXX). If you have not paid yet, it shows an Open Pix. After you pay, the same 5-hour wallet — only model processing time. The same code invites a friend.",
        "why.kicker": "why",
        "why.h2": "a notebook, not a pitch.",
        "why.1": "We work with AI every day. We pay for compute every month.",
        "why.2": "Some days we use everything. Some days we don’t. Either way, unused capacity disappears.",
        "why.3": "That feels wasteful.",
        "why.4": "The experiment has two axes: a marketplace of leftover tokens, and a self-evolving agent that ships every night at 23:30.",
        "why.5": "We think useful intelligence should be easier to access, skills should be easier to share, and experimentation should be cheap.",
        "why.sign": "we deserve to share.",
        "skills.kicker": "shelf",
        "skills.h2": "three short agents — the rest is still coming.",
        "skills.muted": "A skill is a short manifesto plus which CLIs may run it: cursor, codex, claude, antigravity, metamuse. Click and the brief drops into the same chat. The till stays R$5 / 5h. No second price.",
        "skill.use": "use in chat",
        "skill.soon": "soon",
        "skill.mkt.t": "Short post",
        "skill.mkt.p": "280 characters. R$5 / 5h. No face. The same Pix.",
        "skill.copy.t": "Shelf copy",
        "skill.copy.p": "One paragraph. Leftover tokens. No signature.",
        "skill.viral.t": "Invite hook",
        "skill.viral.p": "3 lines. The invite is the same ?code=.",
        "skill.design.t": "Design Critic",
        "skill.design.p": "a cold look at layout and type.",
        "skill.image.t": "Image Prompt Director",
        "skill.image.p": "visual direction, not prompt soup.",
        "skill.research.t": "Research Agent",
        "skill.research.p": "better questions, cleaner sources.",
        "faq.kicker": "questions",
        "faq.h2": "no signup. no plan.",
        "faq.q1": "How much does it cost?",
        "faq.a1": "R$5 for 5 hours of GROK 4.6 High Fast. One-step Pix. No subscription.",
        "faq.q2": "How do I get in after I pay?",
        "faq.a2": "The block code (<code>wdtsot-XXXX</code>) is the login on the web and over SSH. The same <code>?code=</code> invites a friend.",
        "faq.q3": "How do I invite a friend?",
        "faq.a3": "The same block code. The link is <code>sparetoken.shop/?code=wdtsot-XXXX</code>. 10% (R$0.50) in compute for each friend who closed Pix. Pix at R$5. The first indicator is fuzzy. No email.",
        "faq.q4": "What is a skill on the shelf?",
        "faq.a4": "A short manifesto and the CLI allowlist (cursor, codex, claude, antigravity, metamuse). Pix stays R$5 / 5h. No second till.",
        "faq.q5": "What do the short agents do?",
        "faq.a5": "Post, shelf, invite. They open in the chat above. They do not open another till.",
        "faq.q6": "How do I sell my tokens?",
        "faq.a6": "The same R$5 / 5h card. Ten conta.vc links in the <a href=\"#vender\">Sell your tokens</a> panel. The first name on the shelf stays fuzzy. The request is queued for review — live stock is sacred. No second till.",
        "split.open.h": "Built in the open.",
        "split.open.p": "The interface, session layer and skill format are designed to be inspectable, forkable and improvable. Code at <a href=\"https://github.com/sparetoken-shop/sparetoken?utm_source=shop&amp;utm_medium=web&amp;utm_campaign=home\" data-track=\"out-gh\">github.com/sparetoken-shop/sparetoken</a>.",
        "split.privacy.h": "Privacy by default.",
        "split.privacy.p": "We do not sell conversations. We do not show one visitor’s chat to another. There is no hidden prompt harvesting your key. The privacy contract is in the repo: github.com/sparetoken-shop/sparetoken.",
        "final.h2": "Useful intelligence should be easier to access.",
        "final.p": "Fifty prompts in the browser. Or one SSH command, when you want the long table.",
        "exp.kicker": "if you read this far",
        "exp.h2": "we hope this product does not get in your way.",
        "exp.1": "It is an experiment. Five reais for five hours of a frontier model is cheap — it is almost a gift. The idea is, when there is slack, to share a few tokens with friends. Not to turn this into a business that scales without a limit.",
        "exp.2": "The other axis is the market: one card on the shelf, one reseller name, the same Pix. And the self-evolving agent that, every night, tries to leave the shelf a little less empty.",
        "footer.1": "spare tokens · we deserve to share our tokens.",
        "footer.2": "marketplace · reseller fuzzy · <a href=\"https://x.com/sparetoken?utm_source=shop&amp;utm_medium=web&amp;utm_campaign=footer\" data-track=\"out-x\">@sparetoken</a> · 23:30",
        "modal.pay.h": "Before Pix",
        "modal.pay.p": "The conta.vc (fuzzy) link only charges. It does <strong>not</strong> unlock GROK by itself.",
        "modal.pay.1": "Pay and wait for Pix to confirm.",
        "modal.pay.2": "Come back to this page.",
        "modal.pay.3": "Click <strong>I already paid</strong> with the <strong>wdtsot-XXXX</strong> code.",
        "modal.pay.4": "Keep the <strong>wdtsot-XXXX</strong> code — it is the 5-hour login, on the web and over SSH.",
        "modal.pay.note": "Only the time GROK 4.6 High Fast spends generating the answer counts.",
        "modal.pay.later": "not now",
        "modal.pay.ok": "got it, open Pix",
        "sell.close": "close",
        "sell.h3": "Sell your tokens",
        "sell.lead": "Have leftover GROK hours? Put them on the shelf. Same card: R$5 / 5h. The first name on the table stays <strong>fuzzy</strong>.",
        "sell.t1": "This is an experiment-market. You list leftover personal compute — access by wallet code, web or SSH. It is not a cloud contract.",
        "sell.t2": "The Pix links (conta.vc) are yours. Tax, refunds, chargebacks and whatever runs on your machine too. The responsibility is yours.",
        "sell.t3": "The shelf, the shop and the agents do not hold money, do not promise uptime, and do not mediate fights between buyer and seller. We are not on the hook for an SSH session, lost data, or conta.vc / the model going down.",
        "sell.t4": "Buyers pay Pix on your link. Unlocking GROK is the same flow as always: closed charge, <code>wdtsot-XXXX</code> code.",
        "sell.t5": "You state that the capacity is yours and that you will not sell what you cannot deliver.",
        "sell.handle": "shelf handle (lowercase, short — no @, no phone)",
        "sell.links": "10 conta.vc links (one per line)",
        "sell.note": "note (optional)",
        "sell.note.ph": "weekend, BRT timezone…",
        "sell.ack": "I have read and accept the terms. The responsibility is mine.",
        "sell.submit": "Submit for review",
        "sell.ssh.k": "how to open SSH",
        "sell.ssh.1": "The product is a command. No app to download.",
        "sell.ssh.2": "macOS and Linux: the command above. Windows: Windows Terminal or OpenSSH — the same command.",
        "sell.ssh.3": "Empty Enter at login = Pix still Open. After you pay, the <code>wdtsot-XXXX</code> code is the login — web and SSH. Only model generation time counts.",
        "sell.ssh.4": "<a href=\"#terminal\">Terminal section</a> — the same table, no second till.",
        "js.copied": "copied",
        "js.copy_fail": "select and copy",
        "js.copy": "copy",
        "js.copy_link": "Copy link",
        "js.rename": "Name of this chat",
        "js.resume_of": "Resume {name}",
        "js.resume_title": "web and ssh",
        "js.chat_one": "chat",
        "js.chat_many": "chats",
        "js.clock_foot": "{n} {noun} on this code · {mins} / 5h",
        "js.min_one": "1 min",
        "js.min_many": "{n} min",
        "js.line_mins": "{mins} on this line · {code}",
        "js.hint0": "you used the 50 messages in this trial. pay R$5 for 5h.",
        "js.hint1": "1 message left to try",
        "js.hintn": "{n} messages left to try",
        "js.exhausted": "this block’s 5h are gone. pay R$5 for another.",
        "js.exhausted.ph": "block exhausted — pay R$5 to continue",
        "js.exhausted.note": "balance zero. the same R$5 Pix opens another 5h block.",
        "js.paid": "GROK 4.6 High Fast · {clock} remaining{busy}",
        "js.paid.warn": "{clock} of processing left. the block will close.",
        "js.busy": " · GROK is working",
        "js.paid.note": "block unlocked. it only bills while GROK answers. the code resumes web and SSH.",
        "js.chat_fail": "not this time.",
        "js.chat_silent": "silence on the other side. try again.",
        "js.chat_net": "the network failed halfway.",
        "js.pay_fail": "could not open payment now.",
        "js.pay_wait": "pay the Pix, wait for confirm, come back and click I already paid.",
        "js.net": "the network failed. try again.",
        "js.sell_wait": "filing…",
        "js.sell_fail": "did not join the queue.",
        "js.sell_ok": "in the queue. shelf stock stays sacred — review before it goes live.",
        "js.claim_wait": "checking…",
        "js.claim_fail": "did not unlock.",
        "js.claim_ok": "session unlocked. {clock} on this block.",
        "js.claim_empty": "still no balance on this block.",
        "brief.mkt": "Write a short post (max 280) for spare tokens: R$5 / 5h / GROK 4.6 High Fast, one-step Pix, login = block code. No person’s name. No second price. Do not ask for a key, cookie, .env or email. Link: https://sparetoken.shop/?utm_source=shop&utm_medium=web&utm_campaign=agent&utm_content=mkt",
        "brief.copy": "Write one shelf paragraph for people with leftover AI tokens and people who need an hour of model time. Notebook tone, not a pitch. No signature. No word owner. Do not ask for email or WhatsApp. The till stays R$5 / 5h.",
        "brief.viral": "Give 3 one-line hooks to invite a friend with the same block ?code=. No WhatsApp. No email. Do not ask for a key. The invite is the code, not a signup.",
        "brief.invite": " Invite: {url}",
        "ld.q1": "How much does a block cost on spare tokens?",
        "ld.a1": "R$5 for 5 hours of GROK 4.6 High Fast. One-step Pix. No subscription. No second till.",
        "ld.q2": "How do I get in after I pay?",
        "ld.a2": "The block code (wdtsot-XXXX) is the login on the web and over SSH. The same ?code= invites a friend.",
        "ld.q3": "What is a skill on the shelf?",
        "ld.a3": "A short manifesto and the CLI allowlist: cursor, codex, claude, antigravity, metamuse. Pix stays R$5 / 5h. No second till.",
        "ld.q4": "What do the short agents do?",
        "ld.a4": "Short post, shelf copy and invite hook. They open in the same chat. The till stays R$5 / 5h.",
        "ld.q5": "How do I invite a friend?",
        "ld.a5": "The same block code. The link is sparetoken.shop/?code=wdtsot-XXXX. 10% (R$0.50) in compute for each friend who closed Pix. Pix at R$5. The first indicator is fuzzy. No email.",
        "ld.q6": "How do I sell my tokens?",
        "ld.a6": "The same R$5 / 5h card. Ten conta.vc links. The first name on the shelf stays fuzzy. The request is queued for review — live stock is sacred. No second till.",
    },
}

HERO_LINES = {
    "pt-BR": [
        "we deserve to share our tokens.",
        "R$0,50 por 30 minutos de processamento de IA.",
        "pay quickly with PIX and get going.",
    ],
    "en-US": [
        "we deserve to share our tokens.",
        "R$0.50 for 30 minutes of AI processing.",
        "pay quickly with PIX and get going.",
    ],
}

LD_KEYS = (
    ("ld.q1", "ld.a1"),
    ("ld.q2", "ld.a2"),
    ("ld.q3", "ld.a3"),
    ("ld.q4", "ld.a4"),
    ("ld.q5", "ld.a5"),
    ("ld.q6", "ld.a6"),
)


def normalize_locale(raw: str | None) -> str | None:
    if not raw:
        return None
    s = raw.strip().replace("_", "-")
    low = s.lower()
    if low in {"pt", "pt-br", "pt-pt", "br", "brasil", "brazil"}:
        return "pt-BR"
    if low in {"en", "en-us", "en-gb", "us", "usa", "english"}:
        return "en-US"
    if low.startswith("pt"):
        return "pt-BR"
    if low.startswith("en"):
        return "en-US"
    return None


def locale_from_query(query: str) -> str | None:
    q = parse_qs(query or "", keep_blank_values=False)
    for key in ("lang", "hl", "locale"):
        if q.get(key):
            found = normalize_locale(q[key][0])
            if found:
                return found
    return None


def locale_from_accept_language(header: str) -> str | None:
    if not header:
        return None
    best = None
    best_q = -1.0
    for part in header.split(","):
        bit = part.strip()
        if not bit:
            continue
        lang, _, rest = bit.partition(";")
        q = 1.0
        if rest.startswith("q="):
            try:
                q = float(rest[2:].strip())
            except ValueError:
                q = 0.0
        loc = normalize_locale(lang)
        if loc and q > best_q:
            best, best_q = loc, q
    return best


def _ip_int(ip: str) -> tuple[int, int] | None:
    try:
        obj = ipaddress.ip_address((ip or "").split("%")[0].strip())
    except ValueError:
        return None
    if obj.is_private or obj.is_loopback or obj.is_reserved or obj.is_multicast:
        return None
    return obj.version, int(obj)


@lru_cache(maxsize=1)
def _br_tables() -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    raw = gzip.decompress(GEO.read_bytes())
    if raw[:5] != b"STBR\x01":
        raise ValueError("bad geo magic")
    off = 5
    (n4,) = struct.unpack_from(">I", raw, off)
    off += 4
    v4 = []
    for _ in range(n4):
        a, b = struct.unpack_from(">II", raw, off)
        v4.append((a, b))
        off += 8
    (n6,) = struct.unpack_from(">I", raw, off)
    off += 4
    v6 = []
    for _ in range(n6):
        a = int.from_bytes(raw[off : off + 16], "big")
        b = int.from_bytes(raw[off + 16 : off + 32], "big")
        v6.append((a, b))
        off += 32
    return tuple(v4), tuple(v6)


def _in_ranges(n: int, table: tuple[tuple[int, int], ...]) -> bool:
    lo, hi = 0, len(table) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        a, b = table[mid]
        if n < a:
            hi = mid - 1
        elif n > b:
            lo = mid + 1
        else:
            return True
    return False


def country_from_ip(ip: str) -> str | None:
    parsed = _ip_int(ip)
    if not parsed:
        return None
    version, n = parsed
    v4, v6 = _br_tables()
    table = v4 if version == 4 else v6
    return "BR" if _in_ranges(n, table) else "XX"


def country_from_headers(headers) -> str | None:
    for key in ("CF-IPCountry", "X-Country-Code", "X-AppEngine-Country"):
        raw = headers.get(key) if hasattr(headers, "get") else None
        if not raw:
            continue
        cc = raw.split(",")[0].strip().upper()
        if cc in {"BR", "US"}:
            return cc
        if cc in {"XX", "T1", "ZZ", ""}:
            continue
        return cc
    return None


def locale_from_country(cc: str | None) -> str | None:
    if not cc:
        return None
    return "pt-BR" if cc.upper() == "BR" else "en-US"


def resolve_locale(
    *,
    ip: str = "",
    accept_language: str = "",
    cookie: str = "",
    query: str = "",
    headers=None,
) -> dict:
    forced = locale_from_query(query) or normalize_locale(cookie)
    header_cc = country_from_headers(headers) if headers is not None else None
    ip_cc = country_from_ip(ip)
    country = header_cc or ip_cc
    guessed = locale_from_country(country) or locale_from_accept_language(accept_language)
    locale = forced or guessed or DEFAULT
    if locale not in LOCALES:
        locale = DEFAULT
    source = (
        "query"
        if locale_from_query(query)
        else "cookie"
        if normalize_locale(cookie)
        else "header-country"
        if header_cc
        else "ip"
        if ip_cc
        else "accept-language"
        if locale_from_accept_language(accept_language)
        else "default"
    )
    return {
        "locale": locale,
        "lang": HTML_LANG[locale],
        "country": country,
        "source": source,
        "flag": "BR" if locale == "pt-BR" else "US",
    }


def pack(locale: str) -> dict:
    loc = locale if locale in STRINGS else DEFAULT
    return {
        "locale": loc,
        "lang": HTML_LANG[loc],
        "lines": list(HERO_LINES[loc]),
        "strings": STRINGS[loc],
    }


def faq_ld(locale: str) -> dict:
    loc = locale if locale in STRINGS else DEFAULT
    s = STRINGS[loc]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": HTML_LANG[loc],
        "mainEntity": [
            {
                "@type": "Question",
                "name": s[q],
                "acceptedAnswer": {"@type": "Answer", "text": s[a]},
            }
            for q, a in LD_KEYS
        ],
    }


_ATTR_RE = re.compile(
    r'\b(data-i18n-placeholder|data-i18n-aria|data-i18n-title)="([^"]+)"'
)
_OPEN_RE = re.compile(r"<([a-zA-Z][\w:-]*)([^>]*)>")
_DOC_LANG_RE = re.compile(r'(<html\b[^>]*\blang=")([^"]*)(")', re.I)
_TITLE_TAG_RE = re.compile(r"(<title>)(.*?)(</title>)", re.S)
_DESC_RE = re.compile(
    r'(<meta\s+name="description"\s+content=")([^"]*)(")',
    re.I,
)
_LD_RE = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)',
    re.S,
)


def _find_close(html: str, start: int, tag: str) -> int:
    open_tag = f"<{tag}"
    close_tag = f"</{tag}>"
    depth = 1
    i = start
    low = html
    while i < len(low):
        nxt_open = low.find(open_tag, i)
        nxt_close = low.find(close_tag, i)
        if nxt_close < 0:
            return -1
        if nxt_open >= 0 and nxt_open < nxt_close:
            end_open = low.find(">", nxt_open)
            if end_open < 0:
                return -1
            if not low[nxt_open:end_open].endswith("/"):
                depth += 1
            i = end_open + 1
            continue
        depth -= 1
        if depth == 0:
            return nxt_close
        i = nxt_close + len(close_tag)
    return -1


def _set_attr(attrs: str, name: str, value: str) -> str:
    escaped = (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
    pat = re.compile(
        rf"""\s{re.escape(name)}=("[^"]*"|'[^']*')"""
    )
    cleaned = pat.sub("", attrs)
    return f'{cleaned} {name}="{escaped}"'


def apply_html(html: str, locale: str) -> str:
    loc = locale if locale in STRINGS else DEFAULT
    s = STRINGS[loc]
    parts: list[str] = []
    i = 0
    while True:
        match = _OPEN_RE.search(html, i)
        if not match:
            parts.append(html[i:])
            break
        tag, attrs = match.group(1), match.group(2)
        parts.append(html[i : match.start()])
        inner_start = match.end()
        key_html = re.search(r'\bdata-i18n-html="([^"]+)"', attrs)
        key_text = re.search(r'\bdata-i18n="([^"]+)"', attrs)
        attr_hits = list(_ATTR_RE.finditer(attrs))
        is_on = None
        loc_hit = re.search(r'\bdata-locale="([^"]+)"', attrs)
        if loc_hit and tag.lower() == "button":
            is_on = loc_hit.group(1) == loc
            attrs = _set_attr(attrs, "class", "flag is-on" if is_on else "flag")
            attrs = _set_attr(attrs, "aria-pressed", "true" if is_on else "false")
        if attr_hits:
            for hit in attr_hits:
                kind, key = hit.group(1), hit.group(2)
                if key not in s:
                    continue
                if kind.endswith("placeholder"):
                    attrs = _set_attr(attrs, "placeholder", s[key])
                elif kind.endswith("aria"):
                    attrs = _set_attr(attrs, "aria-label", s[key])
                elif kind.endswith("title"):
                    attrs = _set_attr(attrs, "title", s[key])
        if tag.lower() == "span" and "data-i18n-lines" in attrs:
            attrs = _set_attr(attrs, "data-lines", json.dumps(HERO_LINES[loc], ensure_ascii=False))
        key = (key_html.group(1) if key_html else None) or (key_text.group(1) if key_text else None)
        if key and key in s and not attrs.rstrip().endswith("/"):
            close = _find_close(html, inner_start, tag)
            if close < 0:
                parts.append(f"<{tag}{attrs}>")
                i = inner_start
                continue
            parts.append(f"<{tag}{attrs}>{s[key]}")
            i = close
            continue
        parts.append(f"<{tag}{attrs}>")
        i = inner_start
    out = "".join(parts)
    out = _DOC_LANG_RE.sub(lambda m: f"{m.group(1)}{HTML_LANG[loc]}{m.group(3)}", out)
    out = _TITLE_TAG_RE.sub(lambda m: f"{m.group(1)}{s['title']}{m.group(3)}", out)
    out = _DESC_RE.sub(lambda m: f"{m.group(1)}{s['description']}{m.group(3)}", out)
    ld = json.dumps(faq_ld(loc), ensure_ascii=False, indent=2)
    out = _LD_RE.sub(lambda m: f"{m.group(1)}\n{ld}\n  {m.group(3)}", out, count=1)
    return out


def cookie_header(locale: str, secure: bool = False) -> str:
    loc = locale if locale in LOCALES else DEFAULT
    extra = "; Secure" if secure else ""
    return f"{COOKIE}={loc}; Path=/; SameSite=Lax; Max-Age=31536000{extra}"
