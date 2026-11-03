# Brazil’s stabilization plans: an auditable ranking

**Real wins, followed by Collor I and Collor II.** This is the supplied rubric’s ranking, not proof that the runners-up delivered lasting price stability.

Inflation cells show calendar-year IPCA percentages and observation years, linked to IBGE. Dates link to launch evidence. Months and scores are our calculations from those inputs, not published observations.

| Plan (best first) | Launch date | IPCA before, % (year) | IPCA after, % (year) | Whole months | Score |
|---|---|---|---|---|---|
| Real | [1994-07-01][D5] | [2477.15 (1993)][I] | [22.41 (1995)][I] | 60 ([start][D5]; rubric cap) | [0.993667][I] (derived; date sources at left) |
| Collor I | [1990-03-16][D3] | [1972.91 (1989)][I] | [472.70 (1991)][I] | 10 ([start][D3] / [next][D4]) | [0.582283][I] (derived; date sources at left) |
| Collor II | [1991-01-31][D4] | [1620.97 (1990)][I] | [1119.10 (1992)][I] | 41 ([start][D4] / [next][D5]) | [0.421728][I] (derived; date sources at left) |
| Bresser | [1987-06-12][D1] | [79.66 (1986)][I] | [980.21 (1988)][I] | 19 ([start][D1] / [next][D2]) | [0.095000][I] (derived; date sources at left) |
| Cruzado | [1986-02-28][D0] | [242.23 (1985)][I] | [363.41 (1987)][I] | 15 ([start][D0] / [next][D1]) | [0.075000][I] (derived; date sources at left) |
| Verao | [1989-01-15][D2] | [980.21 (1988)][I] | [1620.97 (1990)][I] | 14 ([start][D2] / [next][D3]) | [0.070000][I] (derived; date sources at left) |

**Method and assumptions.** Apply [RUBRIC.md](./RUBRIC.md): score = 0.7 × clamp(1 − after/before, 0, 1) + 0.3 × min(months, 60)/60. These constants are prescribed, not empirical estimates. “Whole months” means completed calendar-month anniversaries: subtract a month if the successor’s day-of-month precedes the launch day. Follow only the rubric’s successor list, including where intervening policies existed. Real starts at its [currency launch][D5], rather than its earlier preparation; its duration is the rubric’s fixed cap. Rank at full precision; displayed scores are rounded.

**Interpretation.** Real combines the largest proportional inflation decline with maximum durability credit. Collor I’s greater proportional decline outweighs Collor II’s longer interval. Cruzado, Bresser and Verao receive no inflation-reduction credit because after-year inflation exceeds before-year inflation; elapsed time alone determines their order. These are calculations from the [IBGE inputs][I] and the linked dates.

**Editorial limits.** Observation windows overlap policies: Cruzado’s after-year includes Bresser; Verao’s includes Collor I; Collor I’s includes Collor II. Time until a named successor does not establish how long a freeze worked or inflation stayed low. The measure excludes output losses, distributional effects and savings restrictions. Call the leaders “highest-scoring under this rubric,” not independently proven policy successes.

**Verification.** Annual IPCA values agree across [the main IBGE bulletin][I] and a [separately indexed IBGE bulletin][J]. Direct PDF opens returned access errors; figures were read from publicly indexed table text. Launch evidence uses the presidential archive, Bresser’s hosted historical account, a contemporary academic document, FGV and the central bank. The JSON preserves URLs, input years, component scores and calculation rules.

[I]: https://biblioteca.ibge.gov.br/visualizacao/periodicos/236/inpc_ipca_2012_abr.pdf
[J]: https://www.ibge.gov.br/biblioteca/visualizacao/periodicos/236/inpc_ipca_2009_mar.pdf
[D0]: https://www.biblioteca.presidencia.gov.br/presidencia/ex-presidentes/jose-sarney/discursos/1986/22.pdf/view
[D1]: https://www.bresserpereira.org.br/books/jogoaberto/0-Introducao.pdf
[D2]: https://www.biblioteca.presidencia.gov.br/presidencia/ex-presidentes/jose-sarney/discursos/1989
[D3]: https://new.scielo.br/j/rep/a/6frHrrTHcVjfYgZMkQFfMMj/?lang=pt
[D4]: https://atlas.fgv.br/verbete/6296
[D5]: https://www.bcb.gov.br/controleinflacao/planoreal?modalAberto=30anosreal_noticia4
