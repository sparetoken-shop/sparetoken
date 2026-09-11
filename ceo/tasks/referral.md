# Referral v0 — 10%, Pix depois de R$5

Óbvio. Entra no 7-day e não sai até existir. Independente de quem publicou no marketplace.

## Regras (primeira versão)

- Indicador: qualquer um. O **primeiro reseller na prateleira é o fuzzy** (nome, não alias).
- Convite = o mesmo `?code=` da carteira (login pós-Pix). Popup rápido. Sem cadastro extra.
- O código eterno **só valida** se a **primeira** indicação fechou (charge paid). Clique sem Pix não cria indicador.
- Por amigo que **pagou**: 10% (R$0,50) — pode ficar como **centavos de compute** na carteira.
- Quando a comissão somada ≥ **R$5**: a pessoa **escolhe** receber Pix (o que estiver no conta.vc do fuzzy e, depois, de outros).
- Independente de quem publicou o skill. Mesmo SKU. Sem cupom SaaS. Sem recorrência.

Schema no ar (0.2.20 / 02/09): `referral.py` + rail/FAQ. Contar atribuição = D3 (0.2.21). Ledger ao vivo na linha do convite = D7 (0.2.29). Visita `?code=` de carteira paga = atribuição, não login = D7c (0.2.31). Teto de 10 amigos no rail; card acende só se ≥1 paid = D10 (0.2.33). Sem pay.py. Sem tela de pessoas enquanto atribuição fechada = 0.

## Ship mínimo (quando for o dia do 7-day)

1. Código de indicação no fuzzy (ou no `wdtsot-XXXX` de quem já pagou).
2. Contar sessões **pagas** atribuídas (charge fechado, não clique).
3. Quando ≥ R$5: Pix manual na primeira versão está ok. Automático depois.
4. Zero mudança no mint da skill conta.vc.

## D+7 típico

Automação do Pix de comissão, ainda no trilho atual — ou recusa se for inventar processador.
