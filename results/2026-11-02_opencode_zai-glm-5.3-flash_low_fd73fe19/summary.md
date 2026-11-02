# mengine-bench 1.7.2: opencode opencode v2.2.2 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **76.2** | 90.7 | 12/15 | 73.5 | 24.7 | 23 min 50 s | >= $0.11 (harness) | 2.13M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T04:02:31Z; bench at 5408b5d5a504; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 74 | 1 min 06 s | 0.0106 | 6 | 6 | 0.8k | 0.0k | 30 s |
| bo-pnl-runway | ok | 40% | 2/5 | 43 | 55.0 s | 0.0036 | 5 | 7 | 1.0k | 0.2k | 32 s |
| bo-reconcile | ok | 100% | 4/4 | 82 | 55.0 s | 0.0026 | 6 | 7 | 0.9k | 0.2k | 33 s |
| cmp-handoff | ok | 100% | 11/11 | 75 | 1 min 06 s | 0.0041 | 8 | 6 | 0.7k | 0.0k | 12 s |
| lc-changelog | ok | 100% | 5/5 | 96 | 18.4 s | 0.0057 | 2 | 1 | 0.2k | 0.1k | 3 s |
| vis-chart | ok | 100% | 4/4 | 95 | 21.4 s | 0.0005 | 2 | 1 | 0.1k | 0.1k | 2 s |
| ds-sql-funnel | ok | 33% | 1/3 | 39 | 1 min 25 s | 0.0046 | 12 | 12 | 1.3k | 0.0k | 21 s |
| ue-packaged-bug | ok | 100% | 5/5 | 76 | 53.2 s | 0.0020 | 5 | 8 | 0.7k | 0.1k | 18 s |
| ir-studio-wiki | ok | 100% | 6/6 | 86 | 38.2 s | 0.0021 | 6 | 7 | 0.2k | 0.0k | 21 s |
| ir-server-logs | ok | 100% | 6/6 | 74 | 47.2 s | 0.0034 | 6 | 5 | 0.5k | 0.1k | 28 s |
| gd-integration-repo | ok | 100% | 8/8 | 82 | 1 min 42 s | 0.0077 | 9 | 18 | 2.6k | 1.1k | 63 s |
| rs-lock-bug | ok | 100% | 6/6 | 85 | 2 min 07 s | 0.0177 | 15 | 14 | 2.9k | 0.9k | 36 s |
| web-mondrian-landing | ok | 100% | 10/10 | 73 | 1 min 27 s | 0.0054 | 7 | 6 | 3.0k | 0.2k | 47 s |
| 3d-voxel-landscape | ok | 100% | 7/7 | 59 | 4 min 59 s | 0.0205 | 17 | 35 | 10.5k | 2.8k | 68 s |
| web-word-universe | ok | 88% | 7/8 | 64 | 5 min 09 s | 0.0227 | 26 | 25 | 9.6k | 1.8k | 52 s |

## Failed checks

- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 268}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 60}
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 743, 'most_connected': {'tempo': 16, 'palavra': 16, 'pescador': 9, 'advogado': 9, 'capital': 9, 'alma': 9, 'almoço': 9, 'madrugada': 9, 'pais': 9, 'herança': 9}}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 7)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 6)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 1)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 8)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 1); read the postmortem (call 1); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 14)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 6)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-voxel-landscape`: wrote the scene (call 1); looked at it in a browser (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 16); looked at it in a browser (call 18); recorded the result (call 5)
