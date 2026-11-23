# Dossier: Which Brazilian anti-inflation plan delivered?

For the policy newsletter. Rubric: score = 0.7 * (inflation drop) + 0.3 * (durability), each 0-1. Inflation is annual IPCA (IBGE). Drop = 1 - IPCA(Y+1)/IPCA(Y-1), clamped 0-1. Durability = months to the next plan (capped at 60) / 60.

## The ranking

| Rank | Plan | Launched | IPCA before (Y-1) | IPCA after (Y+1) | Months lasted | Score |
|---|---|---|---|---|---|---|
| 1 | Real | 1994-06-30 | 2,477.15% (1993) | 22.41% (1995) | 60 (capped) | 0.994 |
| 2 | Collor I | 1990-03-15 | 1,972.91% (1989) | 472.70% (1991) | 10 | 0.582 |
| 3 | Collor II | 1991-01-31 | 1,620.97% (1990) | 1,119.10% (1992) | 41 | 0.422 |
| 4 | Bresser | 1987-06-12 | 79.66% (1986) | 980.21% (1988) | 19 | 0.095 |
| 5 | Cruzado | 1986-02-28 | 242.23% (1985) | 363.41% (1987) | 16 | 0.080 |
| 6 | Verao | 1989-01-15 | 980.21% (1988) | 1,620.97% (1990) | 14 | 0.070 |

## What the numbers say

**Real (1994) is the clear winner.** It cut annual inflation from 2,477.15% (1993) to 22.41% (1995) - a 99.1% drop - and is the only plan that held for the full 60-month durability cap. Score 0.994. It is the one plan that delivered what it promised.

**Collor I (1990) is a strong second on the drop alone.** It cut inflation from 1,972.91% (1989) to 472.70% (1991), a 76% drop, but it lasted only 10 months before being replaced by Collor II. Score 0.582.

**Collor II (1991) is a modest third.** It cut inflation from 1,620.97% (1990) to 1,119.10% (1992), a 31% drop, and lasted 41 months. Score 0.422.

**The 1980s plans (Cruzado, Bresser, Verao) all failed the drop test.** Each one's IPCA the year after its launch was higher than the year before, so score_drop clamps to 0 and their scores come only from durability. Cruzado (0.080) and Bresser (0.095) are near the bottom; Verao (0.070) is last.

## Assumptions

- Launch dates are the official decree/announcement dates (Cruzado 28 Feb 1986, Bresser 12 Jun 1987, Verao 15 Jan 1989, Collor I 15 Mar 1990, Collor II 31 Jan 1991, Real 30 Jun 1994).
- "Months lasted" counts whole calendar months from one plan's launch to the next plan's launch; Real has no successor, so it uses the rubric's 60-month cap.
- IPCA is the IBGE annual (Dec-over-Dec) figure for the calendar year.

## Sources

- IPCA annual series (IBGE/ipeadata): https://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1410807112&oper=view
- Cruzado - Decreto-Lei 2.283/1986: https://www2.camara.gov.br/legin/fed/declei/1980-1987/decreto-lei-2283-27-fevereiro-1986-366999-publicacaooriginal-1-pe.html
- Bresser - Decreto-Lei 2.335/1987: https://www.planalto.gov.br/ccivil_03/decreto-lei/del2335.htm
- Verao - Medida Provisoria 32/1989: https://www.planalto.gov.br/ccivil_03/mp/1988-1994/MP32.htm
- Collor I - Medida Provisoria 168/1990: https://www.planalto.gov.br/ccivil_03/mp/1988-1994/MP168.htm
- Collor II - Medida Provisoria 294/1991: https://www.planalto.gov.br/ccivil_03/mp/1988-1994/MP294.htm
- Real - Medida Provisoria 542/1994: https://www.planalto.gov.br/ccivil_03/mp/1994-1996/MP542.htm