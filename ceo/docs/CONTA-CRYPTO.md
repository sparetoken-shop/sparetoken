# Alma: charge cripto na mesma conta.vc (rail aberto, SKU fixo ainda não)

Isto **prepara** o rail internacional. Não é um segundo caixa. Não minta. Não liga botão sem charge Open no pool.

A conta `@fuzzy` em [conta.vc](https://conta.vc) já liquida on-chain. Pix continua a borda do Brasil.

## Realidade 2026-09-04 (humano)

Mint de **valor fixo** equivalente a R$5 **não fechou** no Chrome (conta.vc). O mínimo útil que a conta permite hoje é **a partir de ~US$1 / ~1 USDT**.

Até existir URL `/pay/fuzzy/c/…` de um charge cripto **Open** no pool:

| Quem | Faz |
|---|---|
| Chrome local, já logado | Pode mintar charge cripto **open-amount from ~$1** com descrição `wdtsot · 5h · 4.6 High Fast` (mesmo SKU de tempo) |
| VPS | Só lê a página pública `/pay/fuzzy/c/…`. Credita se ≠ Open |
| Copy da loja (en-US) | Pode dizer **from ~$1 USDT** pelo mesmo shelf — sem inventar botão segundo |

## Regras iguais ao Pix

- Um SKU de tempo: **5h**. Sem recorrência. Sem segundo preço de produto.
- URL que importa: `https://app.conta.vc/pay/fuzzy/c/…`
- `Já paguei` / claim só libera com evidência.
- Quem indica e quem vende skill usam a **mesma** prateleira.

## O que ainda é proibido

- Segundo botão “Pay USDT” sem charge Open no pool.
- Trocar o Pix do BR por cripto.
- Mint na VPS. Reciclar um link.
- Custodiar chave. Falar em gateway próprio.
- Celebrar venda cripto sem charge ≠ Open.

Ver skill `conta-wdtsot-charges` + `CONTA-CHARGES.md`. Quando o mint cripto existir no Chrome, o mesmo `ingest_conta_links.py --append`.
