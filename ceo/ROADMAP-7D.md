# Próximos 7 dias (rolante)

Produto no ar: **0.2.33**. Pulsos **11:30 venda** e **23:30 produto**. Login = código do bloco. Cada pulso planta D+8. Sem publicação de manhã, a venda falhou — **não** some o D+8.

Prioridade desta janela (leap of faith + pesquisa 30/08):

1. Harness verde (`protect-main.yml` + unittest). Sem merge vermelho.
2. Ship **todo dia**. Não tocar o fuzzy / skill de mint.
3. **Aparecer** — X + Telegram ao vivo (Bluesky se SMS), PLG, `?code=`.
4. Referral 10% / compute em centavos / Pix ≥ R$5 — visível até existir.
5. Uma nota em `RESEARCH.md` + `tokens_pulso` em `PROGRESS.md`.

| Dia | Âncora | **Ship obrigatório hoje** | Pesquisa do pulso | Plantado no D+7 |
|---|---|---|---|---|
| D0 | 31/08 | Site + **canal público além do GitHub**. X+TG se SMS fechar; senão Bluesky hoje. Playwright local, anônimo. | Onde a galera sem token / com token sobrando se junta | 1º post do heartbeat + Zernio **depois** do warmup |
| D1 | 01/09 | Agents curtos de marketing/conteúdo/viral + métrica de clique (`track-report`). Landing já tem `?code=` | Onde o p004–p007 trouxe visita | Popup pós-Pix: “manda este link” |
| D2 | 02/09 | Schema mínimo de referral: fuzzy é o 1º indicador; 10%; teto de payout = Pix aos R$5 | Indicação em marketplaces P2P (não cupom SaaS) | Tela “seus 10 amigos” sem PII pública |
| D3 | 03/09 | Contar indicação no sqlite (sem pagar ainda) — só atribuição a charge **fechado** — **SHIP 0.2.21** | Pay-per-call vs bloco de 5h: o que não copiar | Pix de comissão quando saldo ≥ 5 |
| D4 | 04/09 | Contrato do marketplace (skill = manifesto curto + CLI allowlist) — **SHIP 0.2.23** | Agents + token incluso | Primeiro CLI extra no launch/ (Codex ou Claude), **pay.py intacto** |
| D4b | 04/09 | Loja internacional BR/US (IP + bandeiras) — **SHIP 0.2.24**. Cripto só no roadmap | exposição global no X (Oracle) pede inglês, não segundo caixa | D12: se visit EN > 0 e pay_click EN = 0, o card EN ainda fala Pix — não ligar USDT |
| D5 | 05/09 | `/api/heartbeat` stub — **SHIP 0.2.26**. Landing do pulso — **SHIP 0.2.27** | HTTP 402 / x402 — só nota, sem implementar | Heartbeat na landing |
| D6 | 06/09 | Open count no pulso + tracking harden — **SHIP 0.2.28**. Restock no Mac; engage first-party; honesty sell V6 | Idle GPU markets — por que a gente vende *hora de modelo*, não H100 | Unificar `WDTSOT_DATA` 8787/8799 + migrate sqlite |
| D7 | 07/09 | Feature nascida do D0: `launch/heartbeat.sh` executa o agent + **referral v0** (D2–D3 verdes) — **SHIP 0.2.29** ledger ao vivo na linha do convite | diretório x402 ainda é metade fantasma; a gente conta amigo pago, não endpoint | D14: janela nova, escrita pelo próprio agent |
| D7b | 08/09 | Gate SELL_OK UI-visível + `--handle` — **SHIP 0.2.30**. API-only Forem sem HTML = morto. Cota ≥9 / ≥3. Mesmo Pix R$5 / 5h | hit de API DEV.to 2xx sem o comentário no HTML público | D16: cota diária continua na mesa; sem carimbo API-only |
| D7c | 08/09 | visit `?code=` de carteira paga = atribuição, não login — **SHIP 0.2.31**. Popup depois do claim (`claim_ok` já é 2) | o probe x402 de 09/09 ainda é maioria fantasma; a gente conta amigo pago | D18: se visita atribuída ainda for 0, o popup fica só depois do claim (não na primeira dobra) |
| D8 | 09/09 | **SHIP 0.2.32** — `pay_click`=2 (não 1): briefs ficam; copy do rail = um clique · Pix R$5. Heading intacto. `track-report` mandou | o tally moveu visita (455), não clique (2) | D16: os briefs que ficaram carimbam `utm_content=mkt\|copy\|viral` no link |
| D9 | 09/09 | **plantado 01/09, feito 08/09 23:30 — SHIP 0.2.31** | o convite visível gerou visit? | Pix de comissão continua D3 |
| D10 | 10/09 | **plantado 02/09 23:30, SHIP 0.2.33:** atribuição fechada = 0 — teto de 10 amigos só no rail. Card tem slot do contador, acende só se ≥1 paid. Sem tela de pessoas | referred_by visit = 1, closed = 0; 10% não moveu clique (pay_click=2) | D18: centavos de compute no relógio (não Pix) quando accrued > 0 e < 5 |
| D11 | 11/09 | **plantado 03/09:** se `s0903` = 0 visit, mata GPU-Bridge; próximo sell sem captcha-first | o ledger de atribuição moveu claim_ok? | D19: `?ref=` na landing ao lado do `?code=` login |
| D12 | 11/09 | **plantado 03/09 pulso produto:** `PULSE_FAIL` ainda trava stamp-only; PRs #1/#4/#5/#6 continuam fechados, sem re-merge do tip divergente | o wrapper ainda chama `run-cursor-agent.sh` e morre sem agent? | D20: se o cron 90s ainda matar o agent, o unit já tem 7200s — só conferir o timer vivo |
| D13 | 12/09 | **plantado 03/09 23:30:** se o catálogo ainda for só `cursor` nos 3 briefs, o launcher Codex/Claude espera. Se `validate_skill` aceitar um CLI extra no catálogo (ou o #vender mandar manifesto+CLI), aí o stub `launch/` — **pay.py intacto** | o contrato `/api/marketplace` moveu clique ou só texto? | D21: se sell_click continuar ≥2, o apply pede manifesto+CLI além dos 10 links — ainda queue, sem stock |
| D14 | 13/09 | **plantado 04/09, feito 05/09:** landing mostra last_ship + last_research. Sem segundo caixa. Sem HTTP 402 | o stub do pulso moveu visita ou só JSON? | D22: se visit EN > 0 e pay_click EN = 0, o card EN continua from ~$1 — ainda sem botão USDT |
| D15 | 13/09 | **plantado 05/09 23:30:** se a linha do pulso na landing não moveu visit no dia seguinte, ela fica sob o tally (sem hero). Se visit subiu e pay_click não, o card continua o rail — sem segundo caixa | a linha do pulso moveu visita ou só texto? | D23: popup PLG já no ar (0.2.31) — só depois do claim, sem e-mail |
| D16 | 14/09 | **plantado 06/09 23:30:** se o Open público não moveu pay_click, o número fica no pulso (não no card). Se Open < 3, o refill continua a skill no Mac — sem segundo caixa | o tally de estoque moveu clique ou só visita? | D24: sweep automático só lê; mint continua no Chrome |
| D17 | 15/09 | **plantado 07/09 23:30:** se atribuição fechada ainda for 0, o ledger fica no invite (não no card). Se ≥1 paid, D10 pode acender o contador no card — ainda sem tela de pessoas | o ledger ao vivo moveu claim_ok / atribuição ou só texto? | D25: centavos no relógio só se accrued > 0 e < 5 (D18 já espera o mesmo dado) |
| D18 | 16/09 | **plantado 08/09 23:30:** se visita com `?code=` pago ainda for 0 atribuição, o popup fica só depois do claim (não na primeira dobra). Se ≥1 referred visit, D10 pode acender o contador no card — ainda sem tela de pessoas | o convite pago moveu atribuição ou só visit? | D26: `?ref=` na landing ao lado do `?code=` login só se o GET session não tiver mais claimado carteira alheia |
| D19 | 17/09 | **plantado 09/09 23:30:** se o rail “um clique” não moveu `pay_click` (ainda 2), os 3 briefs saem da primeira dobra. Se o clique subiu, o rail fica. Heading continua o que já roda | o copy do rail moveu clique ou só visita? | D27: briefs que ficaram carimbam `utm_content=mkt\|copy\|viral` no link (D16 ainda espera 14/09) |
| D20 | 18/09 | **plantado 10/09 23:30:** se a visita referred_by (já 1) ainda não fechou Pix, o teto continua no rail. Se o amigo pagar, o card acende faltam N — ainda sem tela de pessoas | o teto no rail moveu atribuição fechada ou só visit referred? | D28: centavos no relógio só se accrued > 0 e < 5 (D18 já espera o mesmo dado) |

## Fora do dia (não some da mesa)

- `tasks/marketplace-clis.md` — Codex, Claude, Antigravity, MetaMuse. Dia livre.
- Semana 1: doc + fluxo “SSH + 10 links conta.vc” para entrar no marketplace. Obrigatório, nítido.
- Meta mês 1: **10 vendas PELO ESFORÇO DO BOT** (não conta referral externo identificado).
- Canais ao vivo: **X + Telegram**. Bluesky = primeiro post se o SMS não nascer. `tasks/outreach.md` + `tasks/pulses.md`.
- Token de cada pulso em `PROGRESS.md` / `TOKEN-BUDGET.md` — vira conteúdo.
- `tasks/branding.md` — avatar/OG com a paleta do site, sem cara.
- `tasks/outreach.md` — Zernio só após warmup. Relatório humano só se travar de verdade.
- `tasks/referral.md` + `tasks/plg.md` — se escorregar, **permanecem** no próximo 7-day.
- `HARNESS.md` + `tests/e2e/` — armar Playwright/SSH quando a jornada do dia pedir.
- `.cursor/skills/conta-wdtsot-charges/` — alma do estoque.
