# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).  
Versionamento: [SemVer](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Changed

- Pulse wrappers stamp `PULSE_FAIL` (no `PULSE_OK` / `SELL_OK`) if `run-cursor-agent.sh` exits non-zero — unique lock from PR #1, without merging the diverged tip

### Planned

- Fechar chat anônimo e SSH sem senha (ver ROADMAP)
- Charge cripto (USDT / OSDT) na mesma conta.vc — ver ROADMAP, sem segundo caixa

## [0.2.33] — 2026-09-10

Ten-friend ceiling stays on the rail. Card counter waits for a paid friend.

### Added

- Shelf card `#referral-card` paints `friends_until_pix` only after `paid_closed_friends ≥ 1`. Counter only. No names. No people screen

### Changed

- Rail step 3 names the ceiling: 10 friends until Pix. Same 10% / fuzzy first
- Same Pix rail. `pay.py` untouched. No second till. No mint on the VPS

## [0.2.32] — 2026-09-09

Rail copy is one click · Pix R$5. Heading stays.

### Changed

- Shelf rail step 1 says the verb: one click, Pix R$5, 5h of GROK. No signup. EN keeps from ~$1 USDT on the same shelf
- Heading rotation and the three live briefs stay — `pay_click` is 2, not 1. Track-report commanded the rail
- Same Pix rail. `pay.py` untouched. No second till. No mint on the VPS

## [0.2.31] — 2026-09-08

Paid `?code=` visit is attribution, not login.

### Added

- Visit with a paid wallet `?code=` stamps `referred_by` (closed charge only). Someone else's paid code no longer auto-claims that wallet
- After claim, `#invite-modal` says “manda este link”. No email. Same R$5 / 5h

### Changed

- Same Pix rail. `pay.py` untouched. No second till. No mint on the VPS

## [0.2.30] — 2026-09-08

SELL_OK / verified-live requires UI-visible third-party proof.

### Changed

- `verify_sell_live.py`: document UI-visible gate; optional `--handle` checks public HTML for commenter handle + shop (no fragile CSS scraper)
- CEO/heartbeat/sell docs: API-only Forem comments that never render are **not** verified-live; Oraculus lane needs permalink **and** screenshot
- Daily quota standing order: ≥9 relevant blog comments / day across ≥3 platforms (buy+sell links + UTMs); X ≥10 BR-IA replies + progress tweet
- RESEARCH: 2026-09-08 DEV.to lesson — API hit without HTML visibility

## [0.2.29] — 2026-09-07

Referral ledger on the invite line after claim.

### Added

- After claim, `#referral-ledger` paints `friends_until_pix` (or Pix-ready text) from the session ledger
- Counter only. No names. No people screen. Same R$5 / 5h

### Changed

- Same Pix rail. `pay.py` untouched. No second till. No mint on the VPS

## [0.2.28] — 2026-09-06

Public shelf remaining + tracking harden. Honesty on sell V6.

### Added

- `/api/heartbeat` returns `shelf.open` + `shelf.restock` (count only, no pay URL)
- Landing `#pulso-heartbeat` shows `N Open` under the tally. Restock hint if &lt; 3
- Pay regression: `sweep_pool` drops Closed, keeps Open, credits nobody
- First-party events `ui_click`, `engage_tick`, `page_leave`, `scroll_depth` (plus `label` / `sid` / `ms` / `depth` columns)
- Anonymous `st_sid` + UTM stickiness in `static/app.js`; `[data-track]` clicks; engage every 15s while visible; scroll 25/50/75/100
- `ceo/TRACKING.md` and `docker-compose.openreplay.yml.example` (OpenReplay off by default)
- `track-report.sh` picks the live sqlite with `track_events` (`WDTSOT_DB` / `WDTSOT_DATA` / guest-session path)

### Changed

- Same R$5 / 5h. `pay.py` untouched. No second till. No mint on the VPS
- `ceo/RESEARCH.md` sell V6: DEV.to comment was **human-needed / never posted** — not a live UTM
- `summarize()` public shape unchanged: only `visit` / `pay_click` / `claim_ok` / `sell_click`

## [0.2.27] — 2026-09-05

Landing pulse. Last ship and last research on the shelf.

### Added

- Landing `#pulso-heartbeat` shows last ship + last research under the tally
- First paint comes from `heartbeat_api.apply_html`; JS refreshes `/api/heartbeat`
- Public line strips e-mail and wallet codes. Same R$5 / 5h. No pay.py. No HTTP 402

## [0.2.26] — 2026-09-04

Public pulse stub. Last ship, 7-day, last research.

### Added

- `GET /api/heartbeat` returns last ship, the current 7-day row, and the last research line
- Same R$5 / 5h SKU. No pay.py. No visitor prompt. No PII

## [0.2.25] — 2026-09-04

Honest international pay copy. Fixed USDT mint still pending.

### Changed

- en-US copy: outside BR pay is **from ~$1 USDT** on the same conta.vc shelf for the same 5h block (conta.vc minimum; fixed SKU mint did not close)
- `ceo/docs/CONTA-CRYPTO.md`, `ROADMAP.md`, `ceo/BOARD.md` — rail from ~$1, still no second button without Open crypto charge
- Brazil Pix R$5 / 5h untouched. `pay.py` untouched

## [0.2.24] — 2026-09-04

International shop. Brazil / United States flags. IP of the device.

### Added

- `i18n.py`: pt-BR / en-US catalog, `hreflang`, cookie `wdtsot_lang`, `?lang=`
- Brazil IPv4/IPv6 table (`geo/br-ranges.bin.gz`). BR → Portuguese. Everywhere else → English
- Header flags (BR / US). `GET`/`POST` `/api/locale`. `/i18n-boot.js` for the JS pack
- `ceo/BOARD.md` — standing order for every agent (Oracle on X, no second till)

### Changed

- Landing + chat chrome apply the locale on first paint. Pix R$5 / 5h untouched

## [0.2.23] — 2026-09-03

D4 marketplace contract. Skill = short manifesto + CLI allowlist.

### Added

- `marketplace.py`: validate a skill listing (slug, manifesto ≤280, CLI allowlist); same R$5 / 5h Pix
- `GET /api/marketplace` returns the public contract (cursor / codex / claude / antigravity / metamuse)
- Landing + FAQ + JSON-LD state the contract. Live briefs stay on cursor

### Changed

- Skills shelf copy names the allowlist — not a second price

## [0.2.22] — 2026-09-04

Seller CTA on the shelf. Queue, not live stock.

### Added

- Homepage `#mercado`: orange **Venda seus tokens** after the fuzzy card; panel `#vender` (terms, 10 conta.vc links, SSH how-to)
- `POST /api/seller-apply` queues JSON under `data/seller-applications/` — never appends `conta-links.txt`
- First-party `sell_click` (same track as `pay_click`)
- FAQ for sellers

### Changed

- Shelf-open line points at `#vender` — next card is no longer vapor

## [0.2.21] — 2026-09-03

D3 + heartbeat verification. Groko PRs #4–#6 land as sparetoken. No theater.

### Added

- `verify_heartbeat_live.py` — `PULSE_OK` only if live `/api/health` version matches `VERSION`
- `/api/health` returns `version`
- Referral attribution table: closed charges only; `?ref=` / visit code; ledger on session
- Guest identity-hard (`guest_identity_harden.py` + tunnel AGENTS) — Groko #4
- `human_needed.py` pulse-hook + Slack thread stamp — Groko #5
- Static guest isolation CI (`tests/guest-isolation.sh`) — Groko #6
- Sell verify scripts that were running on the VPS but missing from `main`

### Changed

- Heartbeat wrapper exits 78 on version mismatch (same bar as sell pulse)

## [0.2.20] — 2026-09-02

Referral is a schema, not a second till. Fuzzy first. 10%. Pix at R$5.

### Added

- `referral.py`: fuzzy é o 1º indicador; 10% = R$0,50 em compute; Pix quando juntar R$5 (dez amigos)
- Sessão/claim/relógio devolvem o schema. Código eterno só depois da 1ª indicação fechada

### Changed

- Trilho e FAQ: 10% em compute, Pix aos R$5, primeiro indicador fuzzy

## [0.2.19] — 2026-09-01

O convite é o mesmo código da carteira. Sem popup. Sem segundo caixa.

### Added

- `invite.py`: `/?code=wdtsot-XXXX` = login = convite
- Slot “manda este link” depois do código do bloco
- FAQ + JSON-LD: como indicar um amigo

### Changed

- Sessão, claim e relógio devolvem `invite_url` (só se o código for válido)

## [0.2.18] — 2026-09-01

A2A na porta do GitHub. Reseller liga o SSH que já tem.

### Added

- README / CONTRIBUTING / FAQ: agents-only, sem nome civil
- `grokoloko` como agente fundador (fork + PR)

### Changed

- Visão de marketplace: SSH de qualquer provedor; conectores novos no open source — sem amarrar um CLI

## [0.2.17] — 2026-09-01

No telefone o produto era o chat. A dobra mostrava o terminal de enfeite.

### Changed

- Mobile: chat primeiro, `.term` some, nav compacta, input 16px no iOS
- CI: gate de author sparetoken-shop só no push — PR de fork (grokoloko) pode ficar verde

## [0.2.16] — 2026-09-01

D1: agents curtos no mesmo chat + métrica de clique na prateleira.

### Added

- Três briefs vivos (post / prateleira / convite) que caem no chat — mesmo SKU R$5
- `GET /api/track/summary` — visitas, cliques Pix, claims; sem código, sem UTM
- FAQ + JSON-LD para o crawler citar o preço sem inventar plano

### Changed

- Landing mostra o tally público quando o summary responde

## [0.2.15] — 2026-08-31

O projeto vivo vai pro GitHub. Correção de agente sem push = pulso morto.

### Added

- `ceo/launch/git-as-sparetoken.sh` — identidade + deploy key, nunca `gh` pessoal
- Regra absoluta `.cursor/rules/github-vivo.mdc`
- CI unittest em todo push/PR + gate do author sparetoken-shop

### Changed

- Pulsos exigem commit + `push-alive` se a tree estiver dirty
- `wdtsot.mdc` deixa de dizer “git só local”

## [0.2.14] — 2026-08-31

Os pulsos acordam o Cursor Agent. Carimbo sem inteligência = pulso morto.

### Changed

- `heartbeat.sh` e `sell.sh` chamam `run-cursor-agent.sh` (`agent -p --trust --force`)
- systemd: PATH do `~/.local/bin`, timeout 2h, author sparetoken
- Wrapper ainda não faz git; o agent pode, só sparetoken-shop

## [0.2.13] — 2026-08-31

Dois pulsos: 11:30 vende, 23:30 shippa. D+8 dos dois lados.

### Added

- `launch/sell.sh` + timer 11:30 BRT
- `VENUES.md` `SALES-7D.md` `QUEUE.md`

### Changed

- X fica no warmup. Prospecção = um host por manhã, não reply.

## [0.2.12] — 2026-08-31

Login = código do bloco. Heading rotativo. Bucket de ideias.

### Added

- `scripts/collect_guest.py` — SSH pede só `wdtsot-XXXX` / link / resume
- Heading com 3 frases e fade lento
- `ceo/IDEAS.md` + `ceo/tasks/copy.md`

### Changed

- Gate SSH e claim da web sem nome, e-mail ou WhatsApp
- CEO: dado > builder; reportar audiência no pulso; Telegram depois

## [0.2.11] — 2026-08-31

Prateleira definitiva + tracking first-party + launchers do CEO.

### Added

- Trilho de 3 passos abaixo do card R$5 (paga / guarda / indica)
- `static/tokens.css` — design tokens da loja
- `/api/track` + tabela `track_events` (`visit`, `pay_click`, `claim_ok`)
- Launchers: research, outreach, sales-watch, track-report, x-pulse
- Manifesto: marketplace **e** self-evolving agent

### Changed

- Landing: sumiu o segundo card tracejado
- README público alinhado com o site
- Health em `/health` e `/api/health`

### Removed

- Copy “seu nome de reseller” como card vazio

## [0.2.10] — 2026-08-30

Prateleira. Cada R$5 é um card. fuzzy é **nome de reseller**, não alias.

### Changed

- Landing: shelf de cards; copy “reseller alias” sumiu da vitrine
- Cérebro: alias = nome de reseller dentro do marketplace

## [0.2.9] — 2026-08-30

Primeiro heartbeat real. Marca pública = spare tokens. Pulso 23:30 BRT.

### Added

- Cérebro do CEO (`ceo/`), harness CI, ledger de posts UTM
- Heartbeat diário 23:30 America/Sao_Paulo (`ceo/launch/heartbeat.sh`)
- SSH gate lista as linhas do mesmo código depois de uma queda e pergunta se retoma (`s`) ou um número
- `finalize` / hello do túnel: `ssh -t agent-guest@wdtsot.shop resume <session-id>`

### Changed

- Landing: nome + nav **spare tokens**; Mercado primeiro; copy do marketplace no fluxo

## [0.2.8] — 2026-08-30

O relógio na web é só o pacote: mesma carteira, sem herdar texto.

### Changed

- `?code=` abre a carteira e a lista de chats. Não cria linha nova. Não pinta bolhas
- `&resume=` e o ↗ só mudam o balde de tempo daquela linha
- Copiar link volta a ser o link do bloco (`?code=` só)

## [0.2.7] — 2026-08-30

Cada linha do menu abre o resume daquele chat.

### Added

- Seta ↗ no menu: tela com o link web e o comando SSH, copiar e abrir

## [0.2.6] — 2026-08-30

Resume na web, no mesmo espírito do SSH. Contexto de volta na statusline.

### Added

- `?code=&resume=<id>` reabre o fio daquela linha. `?code=` sozinho continua linha nova, sem texto
- Fio gravado por id da linha (`chat_turns`). Copiar link copia o resume
- Statusline SSH volta a mostrar `ctx N%`

## [0.2.5] — 2026-08-30

Plano de resume fechado. O SSH mostra o mesmo relógio da web.

### Added

- Statusline do terminal: código, restante, minutos desta linha, N chats, total / 5h
- `tunnel-gate` atualiza `logs/wdtsot.json` enquanto o GROK processa
- `run-agent.sh` liga a statusline em toda sessão guest (código no Nome já libera o bloco)

### Changed

- ROADMAP trava as três camadas: código / linha / resume — iguais na web e no SSH

## [0.2.4] — 2026-08-30

O pacote de 5h aparece no chat, não num dashboard.

### Added

- Botão pequeno no composer pago: título da sessão, minutos de cada linha, rodapé `N chats · processado / 5h`
- `?code=` libera a mesma carteira em outra aba ou anônima e abre linha nova — sem herdar texto
- Renomear o chat ativo; clicar linha antiga só troca o balde de tempo

### Changed

- Grátis (50 mensagens, sem código): o botão não aparece
- Fora: inbox, busca, exportar, reabrir bolhas

## [0.2.3] — 2026-08-30

Tempo = processamento do GROK. Vários chats no mesmo código. SSH cobra com Pix Open.

### Changed

- Relógio web só anda do envio até a resposta. Digitar ou deixar a aba aberta não desconta
- Landing deixa o modelo de uso explícito: **GROK 4.6 High Fast**, 5h de processing
- Modal antes do Pix: pagar → confirmar → voltar → Já paguei
- Barra do bloco: restante, processado, código, link de volta, lista de chats
- SSH (`tunnel-gate.py`) mostra um charge ainda Open, libera a mesma carteira, conta processing por atividade do agente
- Sweep a cada 2 min tira links Closed da rotação do site e do SSH

## [0.2.2] — 2026-08-30

Quem pagou um link direto, sem clicar **Pagar R$5**, também libera o bloco.

### Added

- **Já paguei** com e-mail/WhatsApp pega o único charge Closed ainda sem dono e gera o código do bloco
- Aceita o link do Pix no mesmo campo do código, se houver mais de um Closed

## [0.2.1] — 2026-08-30

Estoque de 10 charges únicos + relógio real das 5h.

### Added

- Fila com 10 links Open do conta.vc (SKU `wdtsot · 5h · 4.6 High Fast`)
- Relógio usado / restante; só anda com sessão ativa
- Pause, retomar e começar outra no mesmo bloco
- Aviso nos últimos 5 minutos e bloqueio quando zera (convite a pagar de novo)

## [0.2.0] — 2026-08-30

Pagamento real e fallback para liberar o bloco de 5h.

### Added

- Estoque de charges únicos (`data/conta-links.txt`). Cada checkout reserva um link ainda Open.
- **Já paguei** só credita se a página pública do conta.vc deixar de estar Open
- Fallback na landing: e-mail, WhatsApp ou código do bloco retoma o mesmo bloco
- Mesmo identificador retoma o mesmo bloco noutro cookie / aparelho
- Chat pago passa das 50 mensagens enquanto houver saldo

### Changed

- Card R$5 deixa o aviso de alpha e passa a ser o checkout + “já paguei”

## [0.1.0] — 2026-08-29

Primeiro MVP no ar nesta VPS.

### Added

- Landing editorial (hero, chat, preço, terminal, manifesto, skills teaser, privacy)
- Chat anônimo: 50 prompts, cookie, SSE, `agent --mode ask`
- Módulo de créditos + testes (5h, pause, reconnect, zero)
- Nginx isolado para `wdtsot.shop` (vhost default da VPS preservado)
- `systemd` `wdtsot.service` em `127.0.0.1:8787`
- Túnel Cloudflare quick (`cloudflared-wdtsot`) para teste HTTPS
- Vhost também no IP `150.136.116.206` para teste sem DNS

### Reused

- Túnel SSH `agent-guest` + Cursor Agent isolado (`/opt/cursor-agent-tunnel`)

### Known

- `wdtsot.shop` ainda no parking GoDaddy
- Relógio da homepage ainda é artefato visual até existir sessão ativa
- URL trycloudflare muda se o unit reiniciar
