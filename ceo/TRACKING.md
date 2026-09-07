# Tracking (first-party)

Sem pixel de terceiro. Sem e-mail. Sem telefone. Sem OpenReplay ligado por padrão.

## Eventos

| event | o que é | vai pro tally público? |
| --- | --- | --- |
| `visit` | land da página | sim |
| `pay_click` | abriu o Pix / checkout | sim |
| `claim_ok` | bloco liberado | sim |
| `sell_click` | CTA “Venda seus tokens” | sim |
| `ui_click` | clique em `[data-track]` (label sanitizado) | **não** |
| `engage_tick` | a cada ~15s com aba visível (`ms`) | **não** |
| `page_leave` | `visibilitychange` hidden / `pagehide` (`ms`) | **não** |
| `scroll_depth` | 25 / 50 / 75 / 100 (`depth`) | **não** |

`GET /api/track/summary` expõe **somente** as quatro contagens do funil. Shape congelado.

## Campos sanitizados

- UTM: `utm_source|medium|campaign|content|term` — `[A-Za-z0-9._-]{1,64}`
- `code` — só `wdtsot-XXXX`
- `label` — label de UI / `data-track`
- `sid` — id anônimo de browser (localStorage `st_sid`), sem cookie de marketing
- `ms` — duração em ms (0…86400000)
- `depth` — 25/50/75/100

UTM gruda em `localStorage.st_utm` (stickiness). Novo UTM na URL sobrescreve a chave; o resto permanece.

## Relatório

```bash
./ceo/launch/track-report.sh
# ou: WDTSOT_DB=/path/to/wdtsot.sqlite ./ceo/launch/track-report.sh
```

O script escolhe o sqlite com mais `track_events` entre `WDTSOT_DB`, `WDTSOT_DATA`, `data/`, raiz do repo, e o path guest-session live.

## OpenReplay (opcional, off)

Ver `docker-compose.openreplay.yml.example`. **Não** sobe no ship. Só se um humano decidir gravar sessão — e aí atualiza `PRIVACY.md` antes.
