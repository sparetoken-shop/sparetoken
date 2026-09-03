# Harness — o CEO não viaja sem cinto

A IA deste projeto **não** é livre. O cérebro (`CEO.md`) manda; o harness **impede** o pulso de quebrar a loja ou doxxar quem compra/vende.

Começa meio shady (um fuzzy, um Pix, um shop anônimo). A função séria é **aparecer** e virar compute sharing robusto. Sem harness, o agent “melhora o Pix” e mata o experimento.

## Mínimo absoluto (protege `main`)

```
PR / push → unittest do MVP → (depois) Playwright visual + jornada SSH
main vermelha = não merge = não deploy
```

Arquivo: `.github/workflows/protect-main.yml`

O essencial que **nunca NUNCA** para (já coberto por `python3 -m unittest discover -s tests -v`):

| Superfície | Testes hoje | E2E depois |
|---|---|---|
| Pagar / claim / charge fechado | `test_pay.py` | Playwright: PIX fácil, **sem** mintar na CI |
| Relógio 5h, pause, resume | `test_credits.py` `test_clock.py` | Visual do relógio + SSH statusline |
| Chat parse / db / statusline | `test_chat_parse` `test_db` `test_statusline` | Jornada web `?code=` |
| Anonimato no estático | `test_anonymity_public.py` | Print sem PII (ver e2e) |

Playwright **não** autentica conta.vc. **Não** cria charge. Compra na CI = HTML público Open/Closed + fluxo local mockado. Mint continua na skill, no Mac.

SSH na CI: smoke do comando e da statusline se houver fixture. Login real de visitante **não** entra no log.

## Pulso (nunca teatro)

`SELL_OK` só depois de `scripts/verify_sell_live.py`: HTTP 2xx, host **fora do Twitter**, corpo com `sparetoken.shop` + `utm_campaign=sell` + `utm_content=sNNN`.

`PULSE_OK` só depois de `scripts/verify_heartbeat_live.py`: HTTP 200 em `/api/health`, `version` = `VERSION` local. Log do agent **não** substitui o GET.

Ordem de venda: criar conta no terceiro → Z-API **somente** com captcha/OTP visível no VNC → fallback `/pulse` + issue. Login wall sem desafio **não** notifica. Fila sem URL = morto. Exit 78. Segredo só em `~/.anon-secrets/sell.env`.

| Superfície | Testes |
|---|---|
| URL de venda ao vivo | `test_sell_live.py` `test_sell_publish.py` |
| Heartbeat ao vivo | `test_heartbeat_live.py` |
| Fallback loja + GitHub | `test_pulse_fallback.py` |
| Notify (mock) | `test_zapi_notify.py` `test_human_needed.py` |
| Guest isolation / identity | `tests/guest-isolation.sh` `test_guest_identity_hard.py` |

## Controles que o CEO favorece (todo pulso)

1. Teste **antes** de feature nova (TDD). Vermelho primeiro no essencial, depois o incremento.
2. Gate de merge = estes testes. Sem “eu vi no browser”.
3. Artefato de e2e: print **anonimizado** (sem e-mail, WhatsApp, `wdtsot-XXXX` real, foto). Código de carteira em fixture é fake.
4. `deny` de túnel / `PAYMENT.md` / skill de mint — o agent não “contorna”.
5. Memória do progresso em `ceo/PROGRESS.md` (sem PII). `MEMORY.md` da VPS não vai ao git.

## Product-led, ainda no cinto

Popup / convite / `?code=` no site é feature. Tem que ter teste de “o link de indicar é o mesmo código da carteira” **antes** de um modal bonito. Pix continua um clique. Sem signup extra para pagar.
