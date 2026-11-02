# mengine-bench 1.7.3: opencode opencode v2.2.2 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **75.0** | 89.8 | 11/15 | 72.9 | 21.2 | 24 min 41 s | >= $0.06 (harness) | 0.82M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode default clean install; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T07:14:25Z; bench at 060d984b322e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 80 | 1 min 03 s | 0.0109 | 7 | 7 | 0.9k | 0.1k | 36 s |
| bo-pnl-runway | ok | 40% | 2/5 | 47 | 1 min 41 s | 0.0043 | 5 | 7 | 3.4k | 0.2k | 69 s |
| bo-reconcile | ok | 100% | 4/4 | 58 | 33.6 s | 0.0019 | 4 | 5 | 0.6k | 0.4k | 16 s |
| cmp-handoff | ok | 91% | 10/11 | 74 | 1 min 37 s | 0.0042 | 10 | 9 | 1.0k | 0.3k | 22 s |
| lc-changelog | ok | 100% | 5/5 | 100 | 13.7 s | 0.0044 | 2 | 1 | 0.1k | 0.1k | 2 s |
| vis-chart | ok | 100% | 4/4 | 93 | 22.5 s | 0.0004 | 2 | 1 | 0.2k | 0.1k | 3 s |
| ds-sql-funnel | ok | 67% | 2/3 | 67 | 2 min 08 s | 0.0046 | 12 | 12 | 2.1k | 0.4k | 15 s |
| ue-packaged-bug | ok | 100% | 5/5 | 80 | 1 min 07 s | 0.0028 | 6 | 9 | 1.1k | 0.3k | 34 s |
| ir-studio-wiki | ok | 100% | 6/6 | 83 | 51.4 s | 0.0025 | 8 | 7 | 0.3k | 0.0k | 38 s |
| ir-server-logs | ok | 100% | 6/6 | 73 | 52.7 s | 0.0027 | 6 | 6 | 0.6k | 0.2k | 23 s |
| gd-integration-repo | ok | 100% | 8/8 | 88 | 1 min 20 s | 0.0047 | 10 | 20 | 1.7k | 0.6k | 33 s |
| rs-lock-bug | ok | 100% | 6/6 | 85 | 2 min 36 s | 0.0057 | 14 | 13 | 3.4k | 1.6k | 30 s |
| web-mondrian-landing | ok | 100% | 10/10 | 77 | 1 min 26 s | 0.0027 | 3 | 2 | 3.1k | 0.1k | 57 s |
| 3d-voxel-landscape | ok | 100% | 7/7 | 57 | 2 min 48 s | 0.0072 | 6 | 5 | 6.7k | 0.5k | 119 s |
| web-word-universe | timeout (timeout) | 50% | 4/8 | 31 | 6 min 00 s | - | 27 | 28 | 11.3k | 2.4k | 80 s |

## Failed checks

- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'Not documented in HANDOFF.md (no benchmark command in the handoff or workspace); re-measure by running scripts/start_server.ps1:165 (local9 b
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.8252, 'lost': 57}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': 0.6667, 'lost': 64}}
- `web-word-universe` relations of a sample of words: saudade: missing 0 (none), extra 13 (amor, café, casa, hoje, janela)
- `web-word-universe` no relation from a sidebar or a footer: 1905 false pairs, such as ['acento - amor', 'acento - café', 'acento - casa']
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 2648, 'most_connected': 'palavra', 'most_connected_degree': 24, 'top10': [['palavra', 24], ['tempo', 24], ['madrugada', 17], ['advogado', 16], ['crepúsculo', 16], ['herança', 16],
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing ansiedade

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 3); read the data (call 1); removed duplicate sessions (call 3); tested significance (call 7); recorded the result (call 7)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 9)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 1)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 9)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 5); read the postmortem (call 1); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 4); ran the whole suite (call 4)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 6)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-voxel-landscape`: wrote the scene (call 1); not seen: looked at it in a browser
- `web-word-universe`: walked the site (call 1); wrote words.json (call 6); wrote the page (call 13); looked at it in a browser (call 23); recorded the result (call 6)
