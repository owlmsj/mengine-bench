# Dossier: which of Brazil's anti-inflation plans delivered?

**Method (per RUBRIC.md).** For each plan launched in year Y: ipca_before = annual IPCA (IBGE) of Y-1, ipca_after = annual IPCA of Y+1. score_drop = clamp(1 - ipca_after/ipca_before, 0, 1); months_lasted = whole calendar months to the next plan's launch (Real: 60 by rubric); score_durability = min(months_lasted, 60)/60; score = 0.7*score_drop + 0.3*score_durability.

**Assumptions (stated, since the brief leaves them open).**
- Launch dates: Cruzado 1986-02-15; Bresser 1987-02-15; Verao 1989-03-15; Collor I 1990-03-15 (Collor took office); Collor II 1991-03-15 (second package); Real 1994-07-01 (new currency in circulation).
- IPCA figures are IBGE's official annual (Dec-to-Dec) rates, as published in IBGE's SIDRA table 1737 (https://sidra.ibge.gov.br/tabela/1737).

## Annual IPCA used (IBGE, https://sidra.ibge.gov.br/tabela/1737)

| Year | IPCA % |
|---|---|
| 1985 | 242.23 |
| 1986 | 79.66 |
| 1987 | 363.41 |
| 1988 | 980.21 |
| 1989 | 1972.91 |
| 1990 | 1620.97 |
| 1991 | 472.70 |
| 1992 | 1119.10 |
| 1993 | 2477.15 |
| 1994 | 916.46 |
| 1995 | 22.41 |

## Scores

| Plan | Launch | IPCA before | IPCA after | Months | score_drop | score_dur | **Score** |
|---|---|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 (1993) | 22.41 (1995) | 60 | 0.9910 | 1.0000 | **0.9937** |
| Collor I | 1990-03-15 | 1972.91 (1989) | 472.70 (1991) | 12 | 0.7604 | 0.2000 | **0.5923** |
| Collor II | 1991-03-15 | 1620.97 (1990) | 1119.10 (1992) | 35 | 0.3158 | 0.5833 | **0.3917** |
| Bresser | 1987-02-15 | 79.66 (1986) | 980.21 (1988) | 25 | 0.0000 | 0.4167 | **0.1250** |
| Cruzado | 1986-02-15 | 242.23 (1985) | 363.41 (1987) | 12 | 0.0000 | 0.2000 | **0.0600** |
| Verao | 1989-03-15 | 980.21 (1988) | 1620.97 (1990) | 12 | 0.0000 | 0.2000 | **0.0600** |

## Top 3 (best first)

1. **Real** (0.9937) - the only plan that actually cut inflation: 2477.15% (1993) down to 22.41% (1995).
2. **Collor I** (0.5923) - inflation fell from 1972.91% (1989) to 472.70% (1991), but the plan lasted only 12 months.
3. **Collor II** (0.3917) - modest drop (1620.97% to 1119.10%) over 35 months.

The three pre-Collor plans (Cruzado, Bresser, Verao) all scored near zero: inflation rose in the year after each launched, so score_drop clamped to 0.

**Source for every number:** https://sidra.ibge.gov.br/tabela/1737 (IBGE, annual IPCA).