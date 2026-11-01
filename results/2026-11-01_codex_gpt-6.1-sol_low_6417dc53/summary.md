# mengine-bench 1.7.0: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **94.8** | 99.2 | 14/15 | 88.9 | 87.4 | 8 min 10 s | n/a | 1.70M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=codex default clean install; service_tier=fast; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T23:27:42Z; bench at c9b7400328c3; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 93 | 36.3 s | - | 1 | 10 | 2.4k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 86 | 31.4 s | - | 1 | 4 | 2.3k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 91 | 13.6 s | - | 1 | 3 | 0.9k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 90 | 25.1 s | - | 2 | 6 | 1.1k | 0.1k | - |
| lc-changelog | ok | 100% | 5/5 | 98 | 6.0 s | - | 1 | 1 | 0.4k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 94 | 6.9 s | - | 1 | 1 | 0.3k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 92 | 19.8 s | - | 1 | 4 | 1.4k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 95 | 18.1 s | - | 1 | 4 | 1.1k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 94 | 12.9 s | - | 1 | 4 | 0.5k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 86 | 17.3 s | - | 1 | 4 | 0.8k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 98 | 27.1 s | - | 1 | 7 | 2.2k | 0.2k | - |
| rs-lock-bug | ok | 100% | 6/6 | 93 | 26.0 s | - | 1 | 4 | 1.9k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 81 | 51.2 s | - | 1 | 4 | 5.3k | 0.2k | - |
| 3d-voxel-landscape | ok | 100% | 7/7 | 75 | 1 min 48 s | - | 1 | 8 | 7.0k | 0.7k | - |
| web-word-universe | ok | 88% | 7/8 | 67 | 1 min 30 s | - | 1 | 8 | 8.7k | 0.6k | - |

## Failed checks

- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 1); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 6); recorded the result (call 10)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 1)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 2); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 3)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 2); read the postmortem (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 2)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); not seen: looked at it in a browser
- `3d-voxel-landscape`: wrote the scene (call 2); looked at it in a browser (call 3)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 5); wrote the page (call 6); looked at it in a browser (call 4); recorded the result (call 5)
