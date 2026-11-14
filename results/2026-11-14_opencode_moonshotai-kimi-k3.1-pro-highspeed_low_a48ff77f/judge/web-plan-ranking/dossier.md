# Dossiê: quais planos anti-inflacionários entregaram o prometido?

**Conclusão editorial.** O **Real** lidera com folga, seguido por **Collor I** e **Collor II**. O resultado vem da aplicação literal da rubrica, não de uma avaliação ampla de crescimento, emprego ou distribuição de renda.

## Ranking completo

| Posição | Plano; lançamento | IPCA anterior → posterior (% ao ano) | Meses até o plano seguinte | Nota |
|---:|---|---|---:|---:|
| 1 | Real; [1994-02-28](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [2477,15 → 22,41](https://sidra.ibge.gov.br/tabela/1737) | [60, por convenção da rubrica](https://sidra.ibge.gov.br/tabela/1737) | [0,9936673193](https://sidra.ibge.gov.br/tabela/1737) |
| 2 | Collor I; [1990-03-16](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [1782,89 → 472,70](https://sidra.ibge.gov.br/tabela/1737) | [10](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [0,5644080678](https://sidra.ibge.gov.br/tabela/1737) |
| 3 | Collor II; [1991-01-31](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [1620,97 → 2477,15](https://sidra.ibge.gov.br/tabela/1737) | [36](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [0,1800000000](https://sidra.ibge.gov.br/tabela/1737) |
| 4 | Bresser; [1987-06-12](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [62,39 → 980,21](https://sidra.ibge.gov.br/tabela/1737) | [19](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [0,0950000000](https://sidra.ibge.gov.br/tabela/1737) |
| 5 | Cruzado; [1986-02-28](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [242,23 → 363,41](https://sidra.ibge.gov.br/tabela/1737) | [15](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [0,0750000000](https://sidra.ibge.gov.br/tabela/1737) |
| 6 | Verão; [1989-01-15](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [980,21 → 1620,97](https://sidra.ibge.gov.br/tabela/1737) | [14](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios) | [0,0700000000](https://sidra.ibge.gov.br/tabela/1737) |

## Método e premissas

A fonte dos preços é a série histórica anual do IPCA do [IBGE, tabela SIDRA 1737](https://sidra.ibge.gov.br/tabela/1737), conferida contra as observações mensais da [série SGS 433 do Banco Central](https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/1985&dataFinal=31/12/1995). As datas seguem os padrões monetários do [Banco Central](https://www.bcb.gov.br/cedulas-e-moedas/padroes-monetarios). Para o Real, adoto a criação da URV como lançamento, coerente com a cronologia monetária oficial, em vez da circulação física da nova moeda. Meses são meses completos entre lançamentos; o Real recebe a duração fixada pela rubrica.

Para cada plano, o componente de queda é a redução proporcional entre os dois IPCA acima, limitada ao intervalo da rubrica; o componente de duração é proporcional ao teto da rubrica. A nota combina esses componentes com os pesos da rubrica. Valores truncados em zero explicam por que planos seguidos de aceleração inflacionária recebem pontos apenas por duração. Os resultados são reproduzíveis a partir de `result.json` e das mesmas fontes.
