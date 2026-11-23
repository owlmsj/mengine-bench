# Dossier: which of Brazil's anti-inflation plans delivered?

**Method (per RUBRIC.md).** Inflation is annual IPCA (IBGE), calendar year. For a plan launched in year Y: ipca_before = IPCA of Y-1, ipca_after = IPCA of Y+1. score_drop = clamp(1 - after/before, 0, 1); months_lasted = whole calendar months to the next plan's launch (Real: 60); score_durability = min(months, 60)/60; score = 0.7*drop + 0.3*durability.

**Data sources.** IPCA annual series 1985-1995 from IBGE SIDRA table 1737 (https://sidra.ibge.gov.br/tabela/1737). Launch dates from Planalto/LexML/BCB legal instruments (see per-plan sources).

| Plan | Launch | IPCA before | IPCA after | Months lasted | score_drop | score_dur | **Score** |
|---|---|---|---|---|---|---|---|
| Cruzado | 28 Feb 1986 | 242.23% (1985) | 363.41% (1987) | 15 | 0.0000 | 0.2500 | **0.0750** |
| Bresser | 12 Jun 1987 | 79.66% (1986) | 980.22% (1988) | 19 | 0.0000 | 0.3167 | **0.0950** |
| Verao | 15 Jan 1989 | 980.22% (1988) | 1620.97% (1990) | 14 | 0.0000 | 0.2333 | **0.0700** |
| Collor I | 16 Mar 1990 | 1972.91% (1989) | 472.70% (1991) | 10 | 0.7604 | 0.1667 | **0.5823** |
| Collor II | 31 Jan 1991 | 1620.97% (1990) | 1119.10% (1992) | 36 | 0.3096 | 0.6000 | **0.3967** |
| Real | 27 Feb 1994 | 2477.15% (1993) | 22.41% (1995) | 60 (capped) | 0.9910 | 1.0000 | **0.9937** |

**Ranking (best first): 1. Real (0.9937), 2. Collor I (0.5823), 3. Collor II (0.3967).**

**Per-plan notes.**
- **Real** — only plan that cut inflation an order of magnitude (2477% -> 22%); full durability credit. Sources: https://sidra.ibge.gov.br/tabela/1737; launch MP 434 (URV) 27 Feb 1994, https://www.planalto.gov.br/.
- **Collor I** — 1989's 1972.91% fell to 472.70% by 1991 (drop 0.76), but lasted only 10 months. Sources: https://sidra.ibge.gov.br/tabela/1737; MP 168, 16 Mar 1990, https://www.lexml.gov.br/.
- **Collor II** — moderate drop (1620.97% -> 1119.10%), 36 months. Sources: https://sidra.ibge.gov.br/tabela/1737; MP 294/295, 31 Jan 1991, https://www.bcb.gov.br/.
- **Cruzado** — inflation rose 242.23% -> 363.41%; zero drop credit. Sources: https://sidra.ibge.gov.br/tabela/1737; Decreto-Lei 2.283, 27/28 Feb 1986, https://www.planalto.gov.br/.
- **Bresser** — 79.66% -> 980.22%; zero drop credit. Sources: https://sidra.ibge.gov.br/tabela/1737; Decreto-Lei 2.335, 12 Jun 1987, https://www.planalto.gov.br/.
- **Verao** — 980.22% -> 1620.97%; zero drop credit. Sources: https://sidra.ibge.gov.br/tabela/1737; MP 32 / Lei 7.730, 15 Jan 1989, https://www.lexml.gov.br/.

**Assumptions.** (1) Plan launch = date of the enabling legal instrument (Cruzado DL 2.283 effective 28 Feb 1986; Real = URV start 27 Feb 1994, not the 1 Jul 1994 currency swap). (2) IPCA values as reported by IBGE SIDRA table 1737. (3) months_lasted counts whole calendar months between launch dates.