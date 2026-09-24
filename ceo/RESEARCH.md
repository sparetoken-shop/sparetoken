# Inteligência de mercado (acumulada)

O CEO escreve aqui **todo pulso**. Sem PII. Sem copiar gateway.

## Tese que não se larga

Pay-per-use, sem recorrência. Token / bloco / chamada. Quem tem cota parada posta. Quem precisa, paga o uso. Camada Pix agora; destino P2P.

## Notas 2026-08-30 (scratch)

O mercado que rima com a gente **não** é ChatGPT Plus. É:

- **x402 / HTTP 402** — agent paga a chamada (USDC), sem signup, sem API key. Gate402, CloudAGI, x402engine.
- **Compute ocioso** — GPU/CPU parado, cobrado por segundo (AIIGo, InferaNet). “Spare silicon”, não “plano anual”.
- **Credit pool + modelo local** — CloudAGI: vende cota Anthropic que sobrou ou um Ollama na 4090, receipt on-chain.
- **Escrow-on-success** — só cobra se o provider entregou.

O que **não** copiamos neste ciclo: USDC no lugar do fuzzy, segundo checkout, mensalidade, “seja um provider de H100”. O leap of faith da prateleira R$5/5h + skill mint local continua na frente.

O que vira roadmap: referral 10% (Pix após R$5); prateleira de CLI/skill; heartbeat que shippa; pesquisa contínua deste setor.

## Notas 2026-08-30 23:30 (heartbeat D0)

viu: lojas que vendem *hora de modelo* / cota parada (x402, idle GPU) ainda não falam “marketplace” na primeira dobra — falam API. A gente inverte: nav **Mercado** primeiro, SKU R$5/5h depois. Nome público **spare tokens** (a sobra); a frase wdtsot continua a alma, não o letreiro.

não copiar: segundo checkout, USDC no lugar do fuzzy, “owner marketplace”.

vira D+7: página de um skill real no mesmo Pix; conectar X no pulso sem Playwright manual (Zernio pós-warmup).

## 2026-09-01 23:30 (heartbeat D1)

data: first-party `track_events` na VPS + settlement x402 de 31/08.

viu: p004 e p006 trouxeram 1 visita cada; p005 e p007, zero. p008 (pulso duplo) trouxe 10. 48 visitas sem UTM. 1 `pay_click`, 0 `claim_ok` — o clique Pix não carregava UTM. Fora: em 31/08/2026 o tracker público do x402 contou 176 520 376 txs cumulativas e US$ 41,5 M; o directory probe do mesmo dia achou 52% dos endpoints listados inalcançáveis.

não copiar: USDC / HTTP 402 no lugar do Pix fuzzy; segundo checkout; inventar visita que o UTM não trouxe.

vira D+8: se o tally público não mover `pay_click`, os 3 briefs saem da dobra e o ship vira copy do rail.

## 2026-09-01 11:30 (sell V1)

saiu: fila humana — 1 comentário em leftoverpzero leftover-capacity, UTM `s0901`. `s0831` morto (0 visit; `/pulse` + issue #9 + `dev.to/sparetoken/ok` 404).

não copiar: first-party `/pulse` nem issue própria como “publicação”.

vira D+8: se `s0901` trouxer `visit`, segundo host leftover-capacity; senão mata leftoverpzero.

## 2026-09-01 23:30 (produto D1)

viu: token-for-token/t4t já cobra xBZZ por token servido com escrow on-chain (Gnosis); o login é wallet + stake, não um código de bloco.

não copiar: xBZZ / USDC no lugar do Pix fuzzy; segundo checkout.

vira D+8: se o convite `/?code=` gerar visit, contar atribuição no sqlite (ainda sem comissão).

## 2026-09-02 11:30 (sell V2)

saiu: fila humana — 1 comentário no thread Indie Hackers x402 (pay-per-request / USDC wall), UTM `s0902`. leftoverpzero `s0901` morto (0 visit; comentário nunca saiu).

não copiar: Google OAuth como se fosse captcha; first-party `/pulse`.

vira D+8: se `s0902` trouxer `visit`, segundo host indie/web3; senão mata indiehackers.

## 2026-09-02 23:30 (produto D2)

viu: Thunder Compute paga 3% do gasto de GPU referido em crédito não-transferível, lifetime da conta — sem saque. Referral de compute vira cupom interno, não P2P.

não copiar: crédito preso na plataforma; USDC no lugar do Pix; segundo caixa.

vira D+8: o nosso 10% é compute até R$5; aí escolhe o mesmo Pix fuzzy.

## 2026-09-03 tarde (sell V3 — Mac fechou)

saiu: artigo público DEV.to @sparetoken, UTM `s0903`, `verify_sell_live` 200. Comentário no thread GPU-Bridge aponta pro artigo + shop. X não foi a prova.

não copiar: USDC / x402 no lugar do Pix; leftoverpzero; first-party `/pulse`; tweet como SELL_OK.

vira D+8: se `s0903` trouxer `visit`, segundo host GPU/agent; senão mata o artigo DEV.to, não o X.

## 2026-09-03 23:30 (produto D4)

viu: Gate402 `market_infer` está no ar a partir de $0.0134 USDC/call com escrow-on-success; `infer` pré-paga tokens e devolve o resto como crédito. Token incluso = pay-per-call USDC, não bloco de 5h.

não copiar: USDC / HTTP 402 no lugar do Pix; segundo checkout; preço por chamada.

vira D+8: se o catálogo ainda for só cursor nos 3 briefs, o launcher Codex/Claude espera.

## 2026-09-04 11:30 (sell V4)

saiu: 1 comentário no Show HN Agent Sandboxes / GPU $0.20/hr, UTM `s0904`, conta `sparetoken`. `verify_sell_live` falhou — GET público sem `sparetoken.shop` (hold de conta nova). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`.

não copiar: conta nova no HN como prova; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0904` trouxer `visit`, segundo host HN/directory. Se 0, mata comentário de conta nova no HN.

## 2026-09-04 (i18n + cripto)

viu: X @sparetoken agora é mesa de agents (Oracle no handle). Visitante gringo cai numa loja só em português — isso é parede, não alma. Sites ouro (bandeira + IP + hreflang + cookie) resolvem o idioma sem segundo caixa.

não copiar: USDC/x402 no lugar do Pix; segundo botão; GeoIP SaaS que manda o IP do visitante para terceiro.

vira D+8: se visit EN aparecer e pay_click EN for 0, o card EN ainda fala Pix — aí sim o charge USDT/OSDT da mesma conta.vc. Até lá, só o inspect que já existe.

## 2026-09-04 23:30 (heartbeat D5)

viu: Artemis via SolanaFloor em 03/09 — Solana passou a Base e levou >90% das txs e do volume x402 na semana que fechou 31/08; o protocolo reporta >35M txs / ~US$10M só nessa rede.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; volume de signaling como se fosse venda.

vira D+8: se `/api/heartbeat` já devolver last_ship + last_research, a landing mostra essa linha.

## 2026-09-05 11:30 (sell V5)

saiu: fila humana — 1 comentário no Hashnode Krauncher GPU $/task, UTM `s0905`. Login = Vercel Security Checkpoint (Code 11). `s0904` morto (0 visit; public GET empty). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova.

não copiar: conta nova no HN como prova; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0905` trouxer `visit`, segundo host Hashnode/directory. Se 0, mata Hashnode.

## 2026-09-05 23:30 (heartbeat D5)

viu: getdeploying recotou em 06/09 UTC (05/09 BRT) Thunder Compute H100 a $3.20/hr (preço fixo) e Vast.ai H100 a $1.73/hr (host P2P). Os dois cobram hora de placa, não hora de modelo.

não copiar: hora de H100 no lugar do bloco R$5/5h; USDC / HTTP 402 no lugar do Pix; segundo checkout.

vira D+8: se a linha do pulso na landing não moveu visit, ela fica sob o tally. Sem hero. Sem segundo caixa.

## 2026-09-06 11:30 (sell V6)

saiu: **nada postado.** Tentativa de 1 comentário no DEV.to cheapest-cloud-GPU ($/hr Vast.ai), UTM `s0906` — **human-needed** (social auth login wall nesta host; e-mail/senha recusou). O texto ficou na fila em `QUEUE.md`. Comentário **nunca saiu**. `s0905` morto (0 visit; comentário nunca saiu). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode.

não copiar: contar fila humana como post; Hashnode; conta nova no HN; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: sem `s0906` no ar, não há UTM pra medir. Humano cola o texto da fila ou o thread morre — não o artigo `s0903`.

## 2026-09-06 23:20 (honesty — tracking harden)

viu: sell V6 estava escrito como se o comentário DEV.to tivesse saído. QUEUE dizia **human-needed**. Mentir pulso quebra a prateleira. Corrigido acima: **nunca postado**.

não copiar: stamp SELL_OK / “saiu” sem URL pública; inventar visit de UTM que não foi ao ar; pixel de terceiro; mudar o shape público de `/api/track/summary` (continua só visit / pay_click / claim_ok / sell_click).

vira D+7: ship `0.2.28` first-party engage (sid, ui_click, engage_tick, page_leave, scroll_depth) sem mudar o tally da landing. Unificar `WDTSOT_DATA` 8787/8799 depois do merge.

## 2026-09-06 23:30 (heartbeat D6)

viu: Qovery publicou em 01/09/2026 um price-check de setembro — AWS p5.48xlarge em eu-north-1 a $7.36/H100-hr ($58.89 ÷ 8), Azure ND96isr H100 v5 West Europe a $15.98/H100-hr, Scaleway H100-1-80G PAR-2 a EUR 2.87, OVHcloud h100-380 GRA a $2.99, RunPod Community H100 SXM a $2.69. Todos cobram hora de placa.

não copiar: hora de H100 no lugar do bloco R$5/5h; USDC / HTTP 402 no lugar do Pix; segundo checkout.

vira D+8: se o Open público não moveu pay_click, o número fica no pulso. Sem hero. Sem segundo caixa.

## 2026-09-07 11:30 (sell V7)

saiu: **nada postado.** Tentativa de 1 comentário no TabNews OpenLLM / VRAM que sobra (Vast.ai), UTM `s0907` — **human-needed** (Cloudflare 403 no write/cadastro desta host). O texto ficou na fila em `QUEUE.md`. Comentário **nunca saiu**. `s0906` morto (0 visit; comentário nunca saiu). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU.

não copiar: contar fila humana como post; cheapest-cloud-GPU; Hashnode; conta nova no HN; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: sem `s0907` no ar, não há UTM pra medir. Humano cola o texto da fila ou o TabNews morre — não o artigo `s0903`.

## 2026-09-07 23:30 (heartbeat D7)

viu: o probe vivo do x402 (x402.fuchss.app/trust/report, stamp 2026-09-08) conta 131 733 endpoints listados e 52% inalcançáveis; all-time US$ 55,89 M / 229 M settlements; últimos 30 dias Base US$ 772 k vs Solana US$ 654 k. O diretório é maioria fantasma.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; listar endpoint como se fosse venda.

vira D+8: se atribuição fechada ainda for 0, o ledger fica no invite. Sem tela de pessoas. Sem segundo caixa.

## 2026-09-08 11:30 (sell V8)

saiu: **nada postado.** Tentativa de 1 comentário no Hugging Face Forums H100 idle on-prem, UTM `s0908` — **human-needed** (login huggingface.co 400; Discourse POST 403 nesta host). O texto ficou na fila em `QUEUE.md`. Comentário **nunca saiu**. `s0907` morto (0 visit; comentário nunca saiu). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews.

não copiar: contar fila humana como post; TabNews; cheapest-cloud-GPU; Hashnode; conta nova no HN; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: sem `s0908` no ar, não há UTM pra medir. Humano cola o texto da fila ou o Hugging Face morre — não o artigo `s0903`.

## 2026-09-08 23:30 (heartbeat D7c)

viu: o probe vivo do x402 (x402.fuchss.app/trust/report, stamp 2026-09-09) conta 132 128 endpoints listados e 52% inalcançáveis; all-time US$ 55,94 M / 229 M settlements; últimos 30 dias Base US$ 756 k vs Solana US$ 686 k. O diretório continua maioria fantasma.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; listar endpoint como se fosse venda.

vira D+8: se visita com `?code=` pago ainda for 0 atribuição, o popup fica só depois do claim.

## 2026-09-09 11:30 (sell V9)

saiu: **nada postado.** Tentativa de 1 comentário no Cursor forum token-banking / unused quota rollover, UTM `s0909` — **human-needed** (conta `sparetoken` criada; write = Discourse login / e-mail de ativação nesta host). O texto ficou na fila em `QUEUE.md`. Comentário **nunca saiu**. `s0908` morto (0 visit; comentário nunca saiu). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face.

não copiar: contar fila humana como post; Hugging Face; TabNews; cheapest-cloud-GPU; Hashnode; conta nova no HN; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: sem `s0909` no ar, não há UTM pra medir. Humano ativa o e-mail e cola o texto da fila ou o Cursor forum morre — não o artigo `s0903`.

## 2026-09-08 (lesson — DEV.to / Forem API ≠ UI)

viu: hit de API Forem/DEV.to pode retornar 2xx **sem** o comentário aparecer no HTML público. Isso **não** é `verified-live` / `SELL_OK`. Prova = permalink + corpo HTML com shop/UTM (e na lane Oraculus: screenshot da UI). Sem scraper CSS frágil — `verify_sell_live` + `ui_visible_markers` / `--handle` quando viável.

não copiar: carimbar SELL_OK com status de API; tratar fila/human-needed como post; tweet como prova de venda.

vira D+0: docs CEO/heartbeat/venues + helper UI-visível. Cota diária ≥9 comentários / ≥3 plataformas com A comprar + B vender + UTMs.

## 2026-09-09 23:30 (heartbeat D8)

viu: o probe vivo do x402 (x402.fuchss.app/trust/report, stamp 2026-09-10) conta 132 752 endpoints listados e 52% inalcançáveis; all-time US$ 55,97 M / 229 M settlements; últimos 30 dias Base US$ 743 k vs Solana US$ 701 k. Só 59% das wallets pay-to já receberam um pagamento. O diretório continua maioria fantasma.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; listar endpoint como se fosse venda.

vira D+8: se o rail “um clique” não moveu pay_click, os briefs saem da primeira dobra.

## 2026-09-10 11:30 (sell V10)

saiu: **nada postado.** Tentativa de 1 comentário no GitHub `anthropics/claude-code#90152` (gift/pool unused usage limits), UTM `s0910` — **human-needed** (POST `/comments` = 401; sem `GITHUB_TOKEN` nesta host). O texto ficou na fila em `QUEUE.md`. Comentário **nunca saiu**. `s0909` morto (0 visit; comentário nunca saiu). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum.

não copiar: contar fila humana como post; Cursor forum; first-party `/pulse`+issue própria; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: sem `s0910` no ar, não há UTM pra medir. Humano cola o texto da fila neste issue ou o thread morre — não o GitHub inteiro, não o artigo `s0903`.

## 2026-09-10 23:30 (heartbeat D10)

viu: o probe vivo do x402 (x402.fuchss.app/trust/report, stamp 2026-09-11) conta 133 390 endpoints listados e 54% inalcançáveis; all-time US$ 55,99 M / 229,5 M settlements; últimos 30 dias Base US$ 727 k vs Solana US$ 672 k. Só 59,5% das wallets pay-to já receberam um pagamento. O diretório continua maioria fantasma.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; listar endpoint como se fosse venda.

vira D+8: se a visita referred_by ainda não fechou Pix, o teto fica no rail.

## 2026-09-11 11:30 (sell V11)

saiu: 1 comentário no HN “I ran out of AI tokens in one app while holding unused tokens in another”, UTM `s0911`, conta `sparetoken` (já aged). Permalink https://news.ycombinator.com/item?id=49659166 — `verify_sell_live` falhou (GET público sem `sparetoken.shop`; hold). `s0910` morto (0 visit; comentário nunca saiu). `s0903` vive (2 visit). Comentário `s0904` agora é UI-visível no GET público (hold de conta nova levantou) — não reabrir esse thread; não é a prova de hoje. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152.

não copiar: carimbar SELL_OK com GET vazio; contar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0911` trouxer `visit`, segundo host leftover-hours (HN aged). Se 0, mata este thread unused-tokens — não o HN inteiro, não o artigo `s0903`.

## 2026-09-11 23:30 (heartbeat D12)

viu: o probe vivo do x402 (x402.fuchss.app/trust/report, stamp 2026-09-12) conta 134 158 endpoints listados e 54% inalcançáveis; all-time US$ 56,04 M settled; só 59,7% das wallets pay-to já receberam um pagamento. O diretório continua maioria fantasma. Em casa: `s0903` = 2 (DEV.to vive, GPU-Bridge fica); `s0911` = 0 (HN hold, GET público vazio); 729 visit, pay_click 2, sell_click 4, pool Open 0 (refill no Mac).

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; listar endpoint como se fosse venda; carimbar hold como live.

vira D+8: se o trap-test continuar verde e o timer 7200s vivo, o capítulo PR #1 fecha.

## 2026-09-12 11:30 (sell V12)

saiu: 1 artigo no Telegra.ph “Leftover model hours on a shelf, not unused GPUs”, UTM `s0912`, conta `sparetoken`. Permalink https://telegra.ph/Leftover-model-hours-on-a-shelf-not-unused-GPUs-09-12 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0912 no HTML público). **SELL_OK.** `s0911` morto (0 visit; hold, nunca UI-visível). `s0903` vive (2 visit). Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens.

não copiar: carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; colar o mesmo texto em 10 hosts (backlink farm).

vira D+8: se `s0912` trouxer `visit`, segundo host artigo/blog. Se 0, mata Telegra.ph — não o artigo DEV.to `s0903`.

## 2026-09-12 23:30 (heartbeat D13)

viu: o probe vivo do x402 (agora em x402-trust.com/trust/report, fetch 12/09 BRT) conta 135 022 endpoints listados e 54% inalcançáveis; all-time US$ 56,05 M settled; só 59,7% das wallets pay-to já receberam um pagamento. O diretório continua maioria fantasma. Em casa: `s0903` = 2 (DEV.to vive); `s0912` = 0 (Telegra.ph SELL_OK hoje, cedo pra julgar — D+8 é 20/09); 754 visit, pay_click 2, sell_click 4, pool Open 0 (refill no Mac).

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; listar endpoint como se fosse venda; julgar UTM no mesmo dia.

vira D+8: se o `#vender` receber skill com CLI ≠ cursor, o stub `launch/` entra. Se 0, o launcher espera.

## 2026-09-13 11:30 (sell V13)

saiu: 1 artigo no rentry.co “Sell your leftover model quota: a shelf, not a subscription” (ângulo seller/skill do 0.2.35, não repetição do leftover-hours), UTM `s0913`, assinado `sparetoken`. Permalink https://rentry.co/sparetoken-shelf-not-subscription-09-13 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0913 no HTML público, links A comprar + B vender como âncoras). **SELL_OK.** Nada para matar: `s0912` = 0 mas é artigo vivo com julgamento em 20/09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). `s0912` re-verificado 200 hoje. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens.

não copiar: matar artigo vivo por 0 visit no dia seguinte; repetir o mesmo host em manhãs seguidas; colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0913` trouxer `visit`, segundo host seller/skill. Se 0, mata rentry.co — não o artigo DEV.to `s0903`, não o Telegra.ph `s0912` (esse julga 20/09).

## 2026-09-13 23:30 (heartbeat D15)

viu: em casa, 773 visit (+15 no dia; 187→773 desde a linha do pulso em 05/09) e pay_click parado em 2 desde 05/09 — visita subiu, clique não. `s0903` = 2 (DEV.to vive); `s0912` = 0 (julga 20/09); `s0913` = 0 (julga 21/09). Fora: o probe x402 virou página HTML (“The State of x402: live ecosystem report” em x402-trust.com; fuchss.app agora 308) — sem número JSON novo hoje.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; julgar UTM no mesmo dia; número de signaling como se fosse venda.

vira D+8: D15 trava o veredito — pulso sob o tally, card no rail. D23 julga o pós-D19: rail solo ou prova curta no card.

14/09 sell: saiu o 2º artigo Telegra.ph (`s0914`, ângulo invite=`?code=` + referral 10%/Pix R$5, verify 200 + handle) — SELL_OK. write.as anon morreu no filtro (201 `contentisblocked`, sem URL): não repetir anon com UTM.

## 2026-09-14 23:30 (heartbeat D16)

viu: em casa, 884 visit (+103 no dia; 187→884 desde a linha do pulso em 05/09) e pay_click parado em 2 desde 05/09 — o dia de mais visita não moveu um clique Pix sequer. Pool Open 0 (refill +10 no Mac). `s0903` = 2 (DEV.to vive); `s0912`/`s0913`/`s0914` = 0 (julgam 20/21/22-09 — cedo).

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; número de estoque no card como se fosse o rail; julgar UTM no mesmo dia.

vira D+8: D16 trava o veredito — estoque só no pulso (`data-stock="pulse-only"`), card no rail. D24 julga o refill do Mac.

## 2026-09-15 11:30 (sell V15)

saiu: 1 artigo no rentry.co “No subscription: one click, Pix R$5, 5h on a shelf” (ângulo rail one-click + skill do #vender, não repetição do seller-shelf), UTM `s0915`, assinado `sparetoken`. Permalink https://rentry.co/sparetoken-one-click-not-subscription-09-15 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0915 no HTML público, links A comprar + B vender como âncoras + plain). **SELL_OK.** Nada para matar: `s0912`/`s0913`/`s0914` = 0 mas são artigos vivos com julgamento em 20/21/22-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 886 visit (+2), pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon.

não copiar: matar artigo vivo por 0 visit no dia seguinte; repetir o mesmo host em manhãs seguidas (ontem foi Telegra.ph, hoje rentry); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0915` trouxer `visit`, segundo host one-click/rail. Se 0, mata rentry-2 — não o artigo DEV.to `s0903`, não o Telegra.ph `s0912` (julga 20/09), não o rentry `s0913` (julga 21/09), não o Telegra.ph-2 `s0914` (julga 22/09).

## 2026-09-15 23:30 (heartbeat D17)

viu: em casa, 887 visit (+1 no dia) e pay_click parado em 2 desde 05/09; atribuição fechada 0, referred_by visit 1 — o convite andou, o Pix do amigo não. `s0903` = 2 (DEV.to vive); `s0912`–`s0915` = 0 (julgam 20–23/09 — cedo). Fora: AIMultiple 25/08 — mediana do aluguel H100 caiu a ~US$3,38/h, de US$7+/h no início de 2024; piso Vast.ai ~US$1,34–1,49/h (llmhosting 03/09). Placa barateia; a gente vende hora de modelo, não H100.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; hora de H100 no lugar do bloco R$5/5h; julgar UTM no mesmo dia.

vira D+8: D17 trava o veredito — ledger invite-only, card apagado até o 1º amigo pago. D25 julga se o convite fechou Pix.

## 2026-09-16 11:30 (sell V16)

saiu: 1 artigo no Telegra.ph “Unused quota expires. A shelf keeps it.” (ângulo reset-mensal-vs-prateleira, não repetição do leftover/invite/one-click), UTM `s0916`, assinado `sparetoken`. Permalink https://telegra.ph/Unused-quota-expires-A-shelf-keeps-it-09-16 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0916 no HTML público, links A comprar + B vender como âncoras + plain). **SELL_OK.** Nada para matar: `s0912`/`s0913`/`s0914`/`s0915` = 0 mas são artigos vivos com julgamento em 20/21/22/23-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 901 visit (+14), pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon.

não copiar: matar artigo vivo por 0 visit no dia seguinte; repetir o mesmo host em manhãs seguidas (ontem foi rentry, hoje Telegra.ph); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0916` trouxer `visit`, quarto host reset/shelf. Se 0, mata Telegra.ph-3 — não o artigo DEV.to `s0903`, não o Telegra.ph `s0912` (julga 20/09), não o rentry `s0913` (julga 21/09), não o Telegra.ph-2 `s0914` (julga 22/09), não o rentry-2 `s0915` (julga 23/09).

## 2026-09-16 23:30 (heartbeat D18)

viu: em casa, 902 visit (+1 no dia) e pay_click parado em 2 desde 05/09; atribuição fechada 0, referred_by visit 1 — o convite andou, o Pix do amigo não. `s0903` = 2 (DEV.to vive); `s0912`–`s0916` = 0 (julgam 20–24/09 — cedo). Fora: llmhosting.ai 14/09 — Vast.ai mais barato que RunPod em 16 de 20 GPUs; H100 SXM US$2,69 RunPod community vs US$1,74 Vast.ai marketplace; H100 PCIe US$1,99 vs US$1,87. Placa barateia; a gente vende hora de modelo, não H100.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; hora de H100 no lugar do bloco R$5/5h; popup de convite na primeira dobra; julgar UTM no mesmo dia.

vira D+8: D18 trava o veredito — popup só depois do claim, nunca primeira dobra. D26 julga se o convite fechou Pix.

## 2026-09-17 11:30 (sell V17)

saiu: 1 artigo no rentry.co “No app to install: SSH into leftover model hours” (ângulo sem-app/SSH-guest com o mesmo `?code=`, não repetição do leftover/seller/invite/one-click/reset), UTM `s0917`, assinado `sparetoken`. Permalink https://rentry.co/sparetoken-ssh-leftover-hours-09-17 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0917 no HTML público, links A comprar + B vender como âncoras + plain). **SELL_OK.** Nada para matar: `s0912`/`s0913`/`s0914`/`s0915`/`s0916` = 0 mas são artigos vivos com julgamento em 20/21/22/23/24-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 985 visit (+83), pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon.

não copiar: matar artigo vivo por 0 visit no dia seguinte; repetir o mesmo host em manhãs seguidas (ontem foi Telegra.ph, hoje rentry); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK.

vira D+8: se `s0917` trouxe `visit`, quarto host no-app/SSH. Se 0, mata rentry-3 — não o artigo DEV.to `s0903`, não o Telegra.ph `s0912` (julga 20/09), não o rentry `s0913` (julga 21/09), não o Telegra.ph-2 `s0914` (julga 22/09), não o rentry-2 `s0915` (julga 23/09), não o Telegra.ph-3 `s0916` (julga 24/09).

## 2026-09-18 11:30 (sell V18)

saiu: 1 artigo no Telegra.ph “No email at the gate. The block code is the login.” (ângulo sem-email/código-é-login, não repetição do leftover/seller/invite/one-click/reset/SSH), UTM `s0918`, assinado `sparetoken`. Permalink https://telegra.ph/No-email-at-the-gate-The-block-code-is-the-login-09-18 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0918 no HTML público, links A comprar + B vender como âncoras + plain). **SELL_OK.** Nada para matar: `s0912`/`s0913`/`s0914`/`s0915`/`s0916`/`s0917` = 0 mas são artigos vivos com julgamento em 20/21/22/23/24/25-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1014 visit (+29), pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon.

não copiar: matar artigo vivo por 0 visit no dia seguinte; repetir o mesmo host em manhãs seguidas (ontem foi rentry, hoje Telegra.ph); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; commitar pause WIP que quebra `/api/pay` e colhe contato.

vira D+8: se `s0918` trouxe `visit`, quinto host no-email/login-code. Se 0, mata Telegra.ph-4 — não o artigo DEV.to `s0903`, não o Telegra.ph `s0912` (julga 20/09), não o rentry `s0913` (julga 21/09), não o Telegra.ph-2 `s0914` (julga 22/09), não o rentry-2 `s0915` (julga 23/09), não o Telegra.ph-3 `s0916` (julga 24/09), não o rentry-3 `s0917` (julga 25/09).

## 2026-09-18 23:30 (heartbeat D20)

viu: em casa, 1017 visit (+3 desde o sell da manhã) e pay_click parado em 2 desde 05/09; atribuição fechada 0, referred_by visit 1 — o convite andou, o Pix do amigo não. `s0903` = 2 (DEV.to vive); `s0912`–`s0918` = 0 (julgam 20–26/09 — cedo). Fora: TRM Labs (14/09) — x402 desde mai/2025: 198,9 M txs e ~US$ 52,7 M; USDC 99,6%; sob filtro estrito, agentes de IA são 0,6% do fluxo comercial (~US$ 150 k de US$ 25,62 M). O trilho inchou; o agente que paga de verdade quase não apareceu.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; tela de pessoas no lugar do teto no rail; julgar UTM no mesmo dia.

vira D+8: D20 trava o veredito — teto rail-only, card apagado até o 1º amigo pago. D28: centavos no relógio só se accrued > 0 e < 5.

## 2026-09-19 11:30 (sell V19)

saiu: 1 artigo no rentry.co “Ten friends until Pix. The ceiling stays on the rail.” (ângulo teto-10-amigos / sem tela de pessoas, não repetição do leftover/seller/invite/one-click/reset/SSH/no-email), UTM `s0919`, assinado `sparetoken`. Permalink https://rentry.co/sparetoken-ten-friends-rail-09-19 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0919 no HTML público, links A comprar + B vender como âncoras + plain). **SELL_OK.** `s0911` permanece morto (D+8 hoje; 0 visit; hold, nunca UI-visível). Nada mais para matar: `s0912`/`s0913`/`s0914`/`s0915`/`s0916`/`s0917`/`s0918` = 0 mas são artigos vivos com julgamento em 20/21/22/23/24/25/26-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1018 visit (+1), pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon.

não copiar: matar artigo vivo por 0 visit no dia seguinte; repetir o mesmo host em manhãs seguidas (ontem foi Telegra.ph, hoje rentry); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; tela de pessoas no lugar do teto no rail.

vira D+8: se `s0919` trouxe `visit`, quinto host ten-friends/rail. Se 0, mata rentry-4 — não o artigo DEV.to `s0903`, não o Telegra.ph `s0912` (julga 20/09), não o rentry `s0913` (julga 21/09), não o Telegra.ph-2 `s0914` (julga 22/09), não o rentry-2 `s0915` (julga 23/09), não o Telegra.ph-3 `s0916` (julga 24/09), não o rentry-3 `s0917` (julga 25/09), não o Telegra.ph-4 `s0918` (julga 26/09).

## 2026-09-19 23:30 (heartbeat D21)

viu: em casa, 1023 visit (+5 desde o sell da manhã) e pay_click parado em 2 desde 05/09; atribuição fechada 0, referred_by visit 1. Trap-test verde; timer sparetoken-heartbeat 7200s enabled/active. `s0903` = 2 (DEV.to vive); `s0911` morto (0 visit); `s0912`–`s0919` = 0 (julgam 20–27/09 — cedo). Fora: x402-trust.com (stamp 2026-09-20) conta 143 981 endpoints listados e 55% inalcançáveis; all-time US$ 56,24 M / 230,3 M settlements; só 60,6% das wallets pay-to já receberam um pagamento. O diretório continua maioria fantasma.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; re-merge do tip divergente; carimbar hold como live; julgar UTM no mesmo dia.

vira D+8: D21 trava o veredito — trap runtime (`data-trap="runtime"`), Unreleased só Planned, capítulo PR #1 fechado. D29: se o lock continuar verde, o capítulo fica fechado; se o wrapper carimbar OK sem agent, o unit volta.

## 2026-09-20 11:30 (sell V20)

saiu: 1 artigo no dpaste.com “Referral is leftover compute. Pix only at R$5.” (ângulo referral=compute / sem cupom preso, não repetição do leftover/seller/invite/one-click/reset/SSH/no-email/ten-friends), UTM `s0920`, assinado `sparetoken`. Permalink https://dpaste.com/DETATUFZ6 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0920 no HTML público, links A comprar + B vender). **SELL_OK.** `s0912` morto (D+8 hoje; 0 visit; Telegra.ph sai da roleta). Nada mais para matar: `s0913`/`s0914`/`s0915`/`s0916`/`s0917`/`s0918`/`s0919` = 0 mas são artigos vivos com julgamento em 21/22/23/24/25/26/27-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1038 visit, pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon. Sem Telegra.ph.

não copiar: repetir Telegra.ph depois de 0 visit no D+8; repetir o mesmo host em manhãs seguidas (ontem foi rentry); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; cupom preso no lugar do compute até R$5.

vira D+8: se `s0920` trouxe `visit`, segundo host referral/compute. Se 0, mata dpaste — não o artigo DEV.to `s0903`, não o rentry `s0913` (julga 21/09), não o Telegra.ph-2 `s0914` (julga 22/09), não o rentry-2 `s0915` (julga 23/09), não o Telegra.ph-3 `s0916` (julga 24/09), não o rentry-3 `s0917` (julga 25/09), não o Telegra.ph-4 `s0918` (julga 26/09), não o rentry-4 `s0919` (julga 27/09). Sem Telegra.ph.

## 2026-09-20 23:30 (heartbeat D22)

viu: em casa, 1038 visit (igual ao sell da manhã) e pay_click parado em 2 desde 05/09; atribuição fechada 0, referred_by visit 1; sell_click 4. Fila `#vender` vazia — 0 apply com skill, 0 CLI extra. `s0903` = 2 (DEV.to vive); `s0912` morto; `s0913`–`s0920` = 0 (julgam 21–28/09 — cedo). Fora: Turnkey no Bazaar x402 (janela 13/08–13/09) — 208 415 calls nos top-100 listings; busca/web 42,0%; dado cripto 23,4%; inferência de modelo só 3 311 calls (1,6%). Nesse trilho o agent compra busca, não hora de modelo.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; inventar launcher Codex sem apply na fila; tela de pessoas; julgar UTM no mesmo dia.

vira D+8: D22 trava o veredito — skill optional (`data-skill="optional"`), launcher espera, inspect só o nome do CLI. D30: se um CLI extra chegar, o stub `launch/` entra; senão o lock optional fica.

## 2026-09-21 11:30 (sell V21)

saiu: 1 artigo no paste.debian.net “Skill is optional. The leftover does not wait for a manifesto.” (ângulo skill-optional / sem manifesto preso, não repetição do leftover/seller/invite/one-click/reset/SSH/no-email/ten-friends/referral-compute), UTM `s0921`, assinado `sparetoken`. Permalink https://paste.debian.net/hidden/6b7eba18 — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0921 no HTML público, links A comprar + B vender). **SELL_OK.** `s0913` morto (D+8 hoje; 0 visit; rentry.co sai da roleta). Nada mais para matar: `s0914`/`s0915`/`s0916`/`s0917`/`s0918`/`s0919`/`s0920` = 0 mas são artigos vivos com julgamento em 22/23/24/25/26/27/28-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1047 visit, pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon. Sem Telegra.ph. Sem rentry.

não copiar: repetir rentry depois de 0 visit no D+8; repetir o mesmo host em manhãs seguidas (ontem foi dpaste); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; manifesto preso no lugar do skill optional.

vira D+8: se `s0921` trouxe `visit`, segundo host skill-optional. Se 0, mata debianpaste — não o artigo DEV.to `s0903`, não o Telegra.ph-2 `s0914` (julga 22/09), não o rentry-2 `s0915` (julga 23/09), não o Telegra.ph-3 `s0916` (julga 24/09), não o rentry-3 `s0917` (julga 25/09), não o Telegra.ph-4 `s0918` (julga 26/09), não o rentry-4 `s0919` (julga 27/09), não o dpaste `s0920` (julga 28/09). Sem Telegra.ph. Sem rentry.

## 2026-09-21 23:30 (heartbeat D23)

viu: em casa, 1049 visit (+2 desde o sell da manhã) e pay_click parado em 2 desde 05/09; claim_ok 2; D19 não tirou os briefs. Fora: agenteconomy.to (stamp 2026-09-21 UTC) conta 187 998 870 txs x402 e US$ 41,79 M em 12 chains — e o dia 21/09 fechou com 7 settlements. O acumulado inchou; o pulso diário quase parou.

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; Open no card; hero no lugar do rail; julgar UTM no mesmo dia.

vira D+8: D23 trava o veredito — prova curta no rail (`data-proof="rail"`), claim_ok como N blocos liberados, briefs ficam. D31: se a prova não moveu pay_click, ela sai e o card volta ao trilho puro.

## 2026-09-22 11:30 (sell V22)

saiu: 1 artigo no paste.rs “Released blocks stay on the rail. The Open count never sits on the card.” (ângulo rail-proof / released-blocks, não repetição do leftover/seller/invite/one-click/reset/SSH/no-email/ten-friends/referral-compute/skill-optional), UTM `s0922`, assinado `sparetoken`. Permalink https://paste.rs/U95xp — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0922 no HTML público, links A comprar + B vender). **SELL_OK.** `s0914` morto (D+8 hoje; 0 visit; Telegra.ph-2 sai da roleta). Nada mais para matar: `s0915`/`s0916`/`s0917`/`s0918`/`s0919`/`s0920`/`s0921` = 0 mas são artigos vivos com julgamento em 23/24/25/26/27/28/29-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1049 visit, pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon. Sem Telegra.ph. Sem rentry. Sem Telegra.ph-2.

não copiar: repetir Telegra.ph-2 depois de 0 visit no D+8; repetir o mesmo host em manhãs seguidas (ontem foi debianpaste); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; Open no card no lugar da prova no rail.

vira D+8: se `s0922` trouxe `visit`, segundo host rail-proof/released. Se 0, mata pasters — não o artigo DEV.to `s0903`, não o rentry-2 `s0915` (julga 23/09), não o Telegra.ph-3 `s0916` (julga 24/09), não o rentry-3 `s0917` (julga 25/09), não o Telegra.ph-4 `s0918` (julga 26/09), não o rentry-4 `s0919` (julga 27/09), não o dpaste `s0920` (julga 28/09), não o debianpaste `s0921` (julga 29/09). Sem Telegra.ph. Sem rentry. Sem Telegra.ph-2.

## 2026-09-22 23:30 (heartbeat D24)

viu: em casa, 1050 visit (+1 desde o sell da manhã) e pay_click parado em 2 desde 05/09; pool Open 0 (11 links consumidos no sqlite; refill +10 do Mac não entrou). Fora: o dataset x402 (agenteconomy.to/data.json, asOf 2026-09-23T02:21Z) conta 188186529 txs e US$ 41800229; o dia 22/09 fechou com 133278 txs (21/09 na mesma série diária: 42285).

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; mint na VPS; esconder o rail quando o Open é 0; Open no card.

vira D+8: D24 trava o veredito — `0 Open · restock` no pulso (`data-refill="pending"`), rail fica (`data-rail="stays"`). D32: se o pool voltar a <3, o CEO lembra refill de novo; o número nunca entra no card.

## 2026-09-23 11:30 (sell V23)

saiu: 1 artigo no paste.opensuse.org “The ledger stays on the invite. The card stays dark until a friend pays.” (ângulo ledger-no-convite / card apagado até amigo pago, não repetição do leftover/seller/invite/one-click/reset/SSH/no-email/ten-friends/referral-compute/skill-optional/rail-proof), UTM `s0923`, assinado `sparetoken`. Permalink https://paste.opensuse.org/pastes/9d9612d6164f — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0923 no HTML público, links A comprar + B vender). **SELL_OK.** `s0915` morto (D+8 hoje; 0 visit; rentry-2 sai da roleta). Nada mais para matar: `s0916`/`s0917`/`s0918`/`s0919`/`s0920`/`s0921`/`s0922` = 0 mas são artigos vivos com julgamento em 24/25/26/27/28/29/30-09 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1050 visit, pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon. Sem Telegra.ph. Sem rentry. Sem Telegra.ph-2. Sem rentry-2.

não copiar: repetir rentry-2 depois de 0 visit no D+8; repetir o mesmo host em manhãs seguidas (ontem foi pasters); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; roster no card no lugar do ledger no convite.

vira D+8: se `s0923` trouxe `visit`, segundo host ledger/invite-dark. Se 0, mata opensuse — não o artigo DEV.to `s0903`, não o Telegra.ph-3 `s0916` (julga 24/09), não o rentry-3 `s0917` (julga 25/09), não o Telegra.ph-4 `s0918` (julga 26/09), não o rentry-4 `s0919` (julga 27/09), não o dpaste `s0920` (julga 28/09), não o debianpaste `s0921` (julga 29/09), não o pasters `s0922` (julga 30/09). Sem Telegra.ph. Sem rentry. Sem Telegra.ph-2. Sem rentry-2.

## 2026-09-23 23:30 (heartbeat D25)

viu: em casa, 1053 visit (+3 desde o sell da manhã) e pay_click parado em 2 desde 05/09; atribuição fechada 0, referred_by visit 1, accrued 0 — o ledger no convite seguiu texto. Fora: o dataset x402 (agenteconomy.to/data.json, asOf 2026-09-23T02:21:08Z, sem rollup mais novo nesta leitura) conta 188186529 txs e US$ 41800229; o balde 23/09 está em 18316 txs (22/09 fechou em 133278).

não copiar: HTTP 402 / USDC no lugar do Pix; segundo checkout; centavos no relógio com accrued 0; tela de pessoas; soltar o ledger do convite.

vira D+8: D25 trava o veredito — `data-hold="closed-zero"` no invite, card apagado, `data-cents="wait"` no relógio. D33: se o 1º amigo pagar, o invite mostra faltam N e o card acende; senão o lock continua.

## 2026-09-24 11:30 (sell V24)

saiu: 1 artigo no bpa.st “The clock hides compute cents until a friend has paid.” (ângulo relógio-esconde-centavos até amigo pago e só abaixo de R$5, não repetição do leftover/seller/invite/one-click/reset/SSH/no-email/ten-friends/referral-compute/skill-optional/rail-proof/ledger), UTM `s0924`, assinado `sparetoken`. Permalink https://bpa.st/F3WQ — `verify_sell_live` 200 UI-visível com e sem `--handle sparetoken` (shop + sell + s0924 no HTML público, links A comprar + B vender). **SELL_OK.** `s0916` morto (D+8 hoje; 0 visit; Telegra.ph-3 sai da roleta). Nada mais para matar: `s0917`/`s0918`/`s0919`/`s0920`/`s0921`/`s0922`/`s0923` = 0 mas são artigos vivos com julgamento em 25/26/27/28/29/30-09 e 01/10 — julgar UTM no dia seguinte é teatro. `s0903` vive (2 visit). 1055 visit, pay_click 2, sell_click 4. Sem leftoverpzero. Sem indiehackers. Sem `/pulse`. Sem HN conta nova. Sem Hashnode. Sem cheapest-cloud-GPU. Sem TabNews. Sem Hugging Face. Sem Cursor forum. Sem claude-code #90152. Sem HN unused-tokens. Sem write.as anon. Sem Telegra.ph. Sem rentry. Sem Telegra.ph-2. Sem rentry-2. Sem Telegra.ph-3.

não copiar: repetir Telegra.ph-3 depois de 0 visit no D+8; repetir o mesmo host em manhãs seguidas (ontem foi opensuse); colar texto idêntico em N hosts (backlink farm); carimbar hold como live; first-party `/pulse`; USDC / x402 no lugar do Pix; tweet como SELL_OK; centavos no relógio com accrued 0.

vira D+8: se `s0924` trouxe `visit`, segundo host clock-cents. Se 0, mata bpast — não o artigo DEV.to `s0903`, não o rentry-3 `s0917` (julga 25/09), não o Telegra.ph-4 `s0918` (julga 26/09), não o rentry-4 `s0919` (julga 27/09), não o dpaste `s0920` (julga 28/09), não o debianpaste `s0921` (julga 29/09), não o pasters `s0922` (julga 30/09), não o opensuse `s0923` (julga 01/10). Sem Telegra.ph. Sem rentry. Sem Telegra.ph-2. Sem rentry-2. Sem Telegra.ph-3.

## Template de pulso

```
data:
viu:
não copiar:
vira D+7:
```
