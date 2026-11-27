# Dossier: which of Brazil's anti-inflation plans delivered?

**Method.** Each plan is scored per RUBRIC.md: `score = 0.7 * score_drop + 0.3 * score_durability`, where `score_drop = clamp(1 - IPCA(Y+1)/IPCA(Y-1), 0, 1)` and `score_durability = min(months_lasted, 60)/60`. Inflation is annual calendar-year IPCA (IBGE). Launch dates are the official announcement/effective dates.

**IPCA annual (IBGE, SIDRA table 1737):** 1985: 242.23% · 1986: 79.66% · 1987: 363.41% · 1988: 980.21% · 1989: 1972.91% · 1990: 1620.97% · 1991: 472.70% · 1992: 1119.10% · 1993: 2477.15% · 1994: 916.46% · 1995: 22.41% — https://sidra.ibge.gov.br/tabela/1737

## Ranking (best first)

| # | Plan | Launched | IPCA before (Y-1) | IPCA after (Y+1) | Months lasted | Score |
|---|------|----------|-------------------|------------------|---------------|-------|
| 1 | Real | 01/07/1994 | 2477.15% (1993) | 22.41% (1995) | 60 (no next plan) | **0.9937** |
| 2 | Collor I | 16/03/1990 | 1972.91% (1989) | 472.70% (1991) | 10 | **0.5823** |
| 3 | Collor II | 31/01/1991 | 1620.97% (1990) | 1119.10% (1992) | 42 | **0.4267** |
| 4 | Bresser | 12/06/1987 | 79.66% (1986) | 980.21% (1988) | 19 | 0.0950 |
| 5 | Cruzado | 28/02/1986 | 242.23% (1985) | 363.41% (1987) | 16 | 0.0800 |
| 6 | Verao | 15/01/1989 | 980.21% (1988) | 1620.97% (1990) | 14 | 0.0700 |

## What the numbers say

- **Real (0.9937)** is the only plan that delivered: IPCA fell from 2477.15% (1993) to 22.41% (1995), a 99.1% drop, and the rubric credits it with the full 60 months of durability. It is the clear, defensible winner.
- **Collor I (0.5823)** cut IPCA from 1972.91% to 472.70% (a 76% drop) but was replaced after only 10 months by its own second shock, so durability dragged the score down.
- **Collor II (0.4267)** held for 42 months but only cut IPCA from 1620.97% to 1119.10% (a 31% drop); inflation re-accelerated to 2477.15% by 1993.
- **Cruzado, Bresser and Verao all failed** the drop test: each was followed by a higher annual IPCA than the year before it (score_drop = 0), so their scores come entirely from durability and sit below 0.10.

## Assumptions

- "Launch date" = official announcement/effective date of each plan (Cruzado 28/02/1986; Bresser 12/06/1987; Verao 15/01/1989; Collor I 16/03/1990; Collor II 31/01/1991; Real 01/07/1994, when the real entered circulation; the URV had been created 27/02/1994).
- Real has no next plan, so months_lasted = 60 per the rubric.
- months_lasted counts whole calendar months between consecutive launch dates.

## Sources

- IPCA annual series (IBGE/SIDRA): https://sidra.ibge.gov.br/tabela/1737
- IPCA page (IBGE): https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html
- Plan launch dates (AGY web search, citing Senado Federal, Câmara dos Deputados, Presidência da República, Fundação FHC, FGV CPDOC, Banco Central do Brasil): https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html (IPCA); plan dates via AGY grounding (Senado/Câmara/Presidência/FHC/FGV/Bacen).