# Launch agent — heartbeat

Dois crons: **11:30 sell.sh** · **23:30 heartbeat.sh**. Os dois acordam o Cursor Agent (`run-cursor-agent.sh` → `agent -p --trust --force`). Sem agent = pulso morto (`PULSE_FAIL`). O wrapper não faz git write; o agent sim, só sparetoken-shop.

Antes de qualquer ferramenta, o cérebro é `ceo/CEO.md`. Depois:

1. Colar `ceo/ROADMAP-7D.md` (os 7 dias)
2. Ler `ceo/PAYMENT.md` + `ceo/docs/CONTA-CHARGES.md`
3. Ler `ceo/HARNESS.md`. Rodar unittest. Sem verde, para.
4. **Invocar** `agent -p --trust --force` no workspace via `run-cursor-agent.sh`. Sem binário = `PULSE_FAIL`.
5. Uma nota em `ceo/RESEARCH.md`
6. **Shippar** a linha de hoje. Sem ship, o pulso falhou.
7. Um eixo extra (`tasks/pulses.md`). Sem lista inteira.
8. Se canal existir: 1 post (X+TG juntos quando der). X é warmup. **Não** é a prova do 11:30.
9. Venda: publicar no host da roleta (blog/fórum) e passar `verify_sell_live`. Fila sem GET = pulso morto. Mac usa o cofre. Captcha visível → WhatsApp via Dexter. Telefone do builder **nunca** no git.
10. `PROGRESS.md` com `tokens_pulso`. Referral / `?code=` não some.
11. Sem identidade. Sem segundo Pix. Sem Zernio no dia 0 da conta.
12. Git: `ceo/GIT.md`. Wrapper não commita. Agent publica com `git-as-sparetoken.sh` (commit + push-alive). Tree suja = falhou.
13. Quatro launchers curtos (além do heartbeat): `research` · `outreach` · `sales-watch` · `track-report`. X: `x-pulse.md`. Public sell: `.cursor/rules/public-sell-courage.mdc`.

Cursor se chama em 24h. Codex / Claude / Antigravity / MetaMuse só com `tasks/marketplace-clis.md`.
