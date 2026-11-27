# Dossier: quais planos anti-inflacionários entregaram o que prometeram?

**Método.** Cada plano foi pontuado com a rubrica de ./RUBRIC.md:
score = 0.7 × score_drop + 0.3 × score_durability, onde score_drop = clamp(1 − IPCA(Y+1)/IPCA(Y−1), 0, 1) e score_durability = min(meses até o próximo plano, 60)/60. IPCA anual (IBGE) em %; meses inteiros entre datas de lançamento.

**Fontes dos dados.**
- IPCA anual 1985–1996: IBGE, SIDRA, Tabela 1737 — https://sidra.ibge.gov.br/tabela/1737
- Datas de lançamento: Wikipédia (pt) — https://pt.wikipedia.org/wiki/Plano_Cruzado , https://pt.wikipedia.org/wiki/Plano_Bresser , https://pt.wikipedia.org/wiki/Plano_Ver%C3%A3o , https://pt.wikipedia.org/wiki/Plano_Collor , https://pt.wikipedia.org/wiki/Plano_Real

**Premissas.** (1) "Lançamento" = data de anúncio/instituição do plano (Cruzado 28/02/1986; Bresser 12/06/1987; Verão 15/01/1989; Collor I 16/03/1990; Collor II 31/01/1991; Real 27/02/1994, MP 434/URV). (2) Meses inteiros = diferença de meses completa entre as datas (dia do fim < dia do início conta −1). (3) Real: sem próximo plano, meses_lasted = 60 (teto da rubrica). (4) IPCA do ano de lançamento Y usa Y−1 e Y+1, conforme a rubrica.

## Tabela de pontuação

| Plano | Lançamento | IPCA antes (Y−1) | IPCA depois (Y+1) | Meses | score_drop | score_dur | **score** |
|---|---|---:|---:|---:|---:|---:|---:|
| Real | 27/02/1994 | 2477,15 (1993) | 22,41 (1995) | 60 | 0,9910 | 1,0000 | **0,9937** |
| Collor I | 16/03/1990 | 1972,91 (1989) | 472,70 (1991) | 10 | 0,7604 | 0,1667 | **0,5823** |
| Collor II | 31/01/1991 | 1620,97 (1990) | 1119,10 (1992) | 36 | 0,3096 | 0,6000 | **0,3967** |
| Bresser | 12/06/1987 | 79,66 (1986) | 980,21 (1988) | 19 | 0,0000 | 0,3167 | **0,0950** |
| Cruzado | 28/02/1986 | 242,23 (1985) | 363,41 (1987) | 15 | 0,0000 | 0,2500 | **0,0750** |
| Verão | 15/01/1989 | 980,21 (1988) | 1620,97 (1990) | 14 | 0,0000 | 0,2333 | **0,0700** |

## Top 3 (melhor primeiro)

1. **Plano Real (1994)** — score 0,9937. Único plano a reduzir a inflação de forma duradoura: IPCA caiu de 2477,15% (1993) para 22,41% (1995). Fonte: https://sidra.ibge.gov.br/tabela/1737
2. **Plano Collor I (1990)** — score 0,5823. Redução forte (1972,91% → 472,70%) mas durou só 10 meses até o Collor II. Fonte: https://sidra.ibge.gov.br/tabela/1737
3. **Plano Collor II (1991)** — score 0,3967. Redução moderada (1620,97% → 1119,10%) e durou 36 meses. Fonte: https://sidra.ibge.gov.br/tabela/1737

**Leitura para o editor.** A rubrica premia queda de inflação (70%) e duração (30%). Só o Real entrega as duas; Collor I entrega a queda mas não a duração; os planos de 1986–1989 (Cruzado, Bresser, Verão) não reduziram a inflação no ano seguinte ao lançamento — a inflação acelerou em todos os três —, por isso score_drop = 0 e scores baixos.