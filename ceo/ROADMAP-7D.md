# Próximos 7 dias (rolante)

Produto no ar: **0.2.24**. Pulsos **11:30 venda** e **23:30 produto**. Login = código do bloco. Cada pulso planta D+8. Sem publicação de manhã, a venda falhou — **não** some o D+8.

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
| D5 | 05/09 | `/api/heartbeat` stub: last ship, 7-day, last research line | HTTP 402 / x402 — só nota, sem implementar | Heartbeat na landing |
| D6 | 06/09 | Regressão do pagar + **restock pela skill** (mint local, ingest, 10 Open) | Idle GPU markets — por que a gente vende *hora de modelo*, não H100 | Sweep automático do pool |
| D7 | 07/09 | Feature nascida do D0: `launch/heartbeat.sh` executa o agent (ainda sem cron até “publique”) + **referral v0 se D2–D3 estiverem verdes** | O CEO escolhe a próxima janela com RESEARCH + leap of faith | D14: janela nova, escrita pelo próprio agent |
| D8 | 09/09 | se `pay_click` ainda for 1, os 3 briefs saem da primeira dobra e o ship é copy do rail — `track-report` manda, não o heading | o tally público moveu clique ou só visita? | D16: os briefs que ficaram carimbam `utm_content=mkt\|copy\|viral` no link |
| D9 | 09/09 | **plantado 01/09 23:30:** visit com `?code=` de carteira paga vira atribuição no sqlite (ainda sem comissão). Popup só se `claim_ok` > 0 | o convite visível gerou visit? | Pix de comissão continua D3 |
| D10 | 10/09 | **plantado 02/09 23:30:** se D3 ainda não gravou charge fechado atribuído, o teto dos 10 amigos fica só no rail — sem tela de pessoas. Se ≥1 paid, o card mostra quantos faltam pro Pix (contador, sem nome) | o schema de 10%/Pix-aos-5 moveu clique ou só texto? | D18: centavos de compute no relógio (não Pix) quando accrued > 0 e < 5 |
| D11 | 11/09 | **plantado 03/09:** se `s0903` = 0 visit, mata GPU-Bridge; próximo sell sem captcha-first | o ledger de atribuição moveu claim_ok? | D19: `?ref=` na landing ao lado do `?code=` login |
| D12 | 11/09 | **plantado 03/09 pulso produto:** `PULSE_FAIL` ainda trava stamp-only; PRs #1/#4/#5/#6 continuam fechados, sem re-merge do tip divergente | o wrapper ainda chama `run-cursor-agent.sh` e morre sem agent? | D20: se o cron 90s ainda matar o agent, o unit já tem 7200s — só conferir o timer vivo |
| D13 | 12/09 | **plantado 03/09 23:30:** se o catálogo ainda for só `cursor` nos 3 briefs, o launcher Codex/Claude espera. Se `validate_skill` aceitar um CLI extra no catálogo (ou o #vender mandar manifesto+CLI), aí o stub `launch/` — **pay.py intacto** | o contrato `/api/marketplace` moveu clique ou só texto? | D21: se sell_click continuar ≥2, o apply pede manifesto+CLI além dos 10 links — ainda queue, sem stock |

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
