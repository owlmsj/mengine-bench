# Dossier: Which of Brazil's anti-inflation plans delivered?

**Method.** Scored per RUBRIC.md. IPCA = IBGE annual calendar-year inflation (% a.a.),
sourced from Ipeadata (IPEA/IBGE): https://www.ipeadata.gov.br
Launch dates from public sources (see per-plan sources below).
score = 0.7 * clamp(1 - ipca_after/ipca_before, 0, 1) + 0.3 * min(months_lasted, 60)/60.

**Assumptions.**
- "Launch date" = date the plan's measures took effect (Cruzado: Decree-Law 2.283, 28/02/1986;
  Bresser: 12/06/1987; Verao: 15/01/1989; Collor I: 16/03/1990; Collor II: 31/01/1991;
  Real: 01/07/1994, official launch of the currency; the URV MP 434 was 27/02/1994).
- months_lasted = whole calendar months launch-to-next-launch; Real capped at 60 per rubric.
- ipca_before = year Y-1, ipca_after = year Y+1 (calendar years, not plan lifetimes).

**Data (annual IPCA, % a.a. — Ipeadata/IBGE, https://www.ipeadata.gov.br):**
1985: 242.23 | 1986: 79.66 | 1987: 363.41 | 1988: 980.21 | 1989: 1972.91 |
1990: 1620.97 | 1991: 472.70 | 1992: 1119.10 | 1993: 2477.15 | 1994: 916.46 | 1995: 22.41

| Plan | Launch | IPCA Y-1 | IPCA Y+1 | Months | Score |
|---|---|---|---|---|---|
| Real | 1994-07-01 | 2477.15 | 22.41 | 60 | **0.9937** |
| Collor I | 1990-03-16 | 1972.91 | 472.70 | 10 | **0.5823** |
| Collor II | 1991-01-31 | 1620.97 | 1119.10 | 42 | **0.4267** |
| Bresser | 1987-06-12 | 79.66 | 980.21 | 19 | 0.0950 |
| Cruzado | 1986-02-28 | 242.23 | 363.41 | 16 | 0.0800 |
| Verao | 1989-01-15 | 980.21 | 1620.97 | 14 | 0.0700 |

**Top 3 (best first): Real, Collor I, Collor II.**

**Reading for the editor.** Only the Real plan delivered its promise on the rubric:
inflation fell from 2477.15% (1993) to 22.41% (1995) and it lasted the full 60-month
cap — score 0.9937. Collor I cut 1990 inflation to a third of 1989's level but lasted
only 10 months before its successor (0.5823). Collor II improved the level (1119.10% in
1992 vs 1620.97% in 1990) and lasted 42 months (0.4267). The three 1980s plans all
scored under 0.10: each was replaced before it could bend the inflation path, and
inflation rose in the year after each launch (Cruzado 242.23→363.41; Bresser 79.66→980.21;
Verao 980.21→1620.97), so their drop component is zero.

**Per-plan sources.**
- IPCA series (all figures above): Ipeadata/IBGE — https://www.ipeadata.gov.br
- Cruzado 28/02/1986 (Decree-Law 2.283): Senado Federal / FGV (via agy search)
- Bresser 12/06/1987: Mais Retorno (via agy search)
- Verao 15/01/1989: Mais Retorno / Secretaria de Planejamento RS (via agy search)
- Collor I 16/03/1990: Wikipedia "Plano Collor" — https://pt.wikipedia.org/wiki/Plano_Collor
- Collor II 31/01/1991: FGV / Wikipedia (via agy search)
- Real 01/07/1994: Banco Central do Brasil — https://www.bcb.gov.br