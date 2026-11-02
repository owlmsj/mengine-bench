# mengine-bench 1.7.2: opencode opencode v2.2.2 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **81.8** | 89.2 | 12/15 | 70.7 | 79.1 | 10 min 14 s | >= $0.06 (harness) | 0.93M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode default clean install; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T04:31:19Z; bench at 5408b5d5a504; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 74 | 34.9 s | 0.0081 | 5 | 5 | 0.4k | 0.0k | 21 s |
| bo-pnl-runway | ok | 100% | 5/5 | 63 | 28.8 s | 0.0026 | 5 | 7 | 0.8k | 0.1k | 14 s |
| bo-reconcile | ok | 50% | 2/4 | 41 | 19.1 s | 0.0010 | 3 | 2 | 0.5k | 0.2k | 8 s |
| cmp-handoff | ok | 100% | 11/11 | 81 | 39.6 s | 0.0037 | 8 | 7 | 0.8k | 0.2k | 12 s |
| lc-changelog | ok | 100% | 5/5 | 95 | 9.8 s | 0.0044 | 2 | 1 | 0.1k | 0.1k | 1 s |
| vis-chart | ok | 100% | 4/4 | 100 | 11.8 s | 0.0005 | 2 | 1 | 0.3k | 0.1k | 5 s |
| ds-sql-funnel | ok | 0% | 0/3 | 33 | 33.0 s | 0.0024 | 9 | 9 | 1.1k | 0.2k | 5 s |
| ue-packaged-bug | ok | 100% | 5/5 | 76 | 22.3 s | 0.0015 | 5 | 8 | 0.7k | 0.1k | 7 s |
| ir-studio-wiki | ok | 100% | 6/6 | 90 | 19.8 s | 0.0022 | 6 | 8 | 0.3k | 0.0k | 9 s |
| ir-server-logs | ok | 100% | 6/6 | 83 | 25.5 s | 0.0019 | 6 | 6 | 0.4k | 0.0k | 14 s |
| gd-integration-repo | ok | 100% | 8/8 | 78 | 53.5 s | 0.0054 | 9 | 19 | 2.8k | 1.3k | 30 s |
| rs-lock-bug | ok | 100% | 6/6 | 77 | 48.3 s | 0.0036 | 12 | 13 | 1.3k | 0.4k | 20 s |
| web-mondrian-landing | ok | 100% | 10/10 | 72 | 54.0 s | 0.0025 | 3 | 2 | 2.5k | 0.1k | 35 s |
| 3d-voxel-landscape | ok | 100% | 7/7 | 43 | 1 min 17 s | 0.0064 | 11 | 11 | 5.0k | 0.2k | 44 s |
| web-word-universe | ok | 88% | 7/8 | 55 | 2 min 16 s | 0.0129 | 18 | 17 | 8.6k | 1.0k | 26 s |

## Failed checks

- `bo-reconcile` mismatched amounts: expected ['INV-1021', 'INV-1036'], received ['INV-1021']
- `bo-reconcile` invoiced vs paid on mismatches: expected [{'id': 'INV-1021', 'invoiced': 21320.36, 'paid': 21070.36}, {'id': 'INV-1036', 'invoiced': 8619.16, 'paid': 7757.24}], received [{'id': 'INV-1021', 'invoiced': 21320.36, 'paid': 21070.36}]
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'steamdeck': 'purchase', 'pc': 'purchase'}
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 743, 'most_connected': [{'word': 'palavra', 'degree': 16}, {'word': 'tempo', 'degree': 16}, {'word': 'advogado', 'degree': 9}, {'word': 'alma', 'degree': 9}, {'word': 'almoço', 'de

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 2)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 7)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 1)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 8)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 1); read the postmortem (call 1); recorded the result (call 8)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); not seen: ran the whole suite
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 5)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-voxel-landscape`: wrote the scene (call 1); not seen: looked at it in a browser
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 8); not seen: looked at it in a browser; recorded the result (call 5)
