# mengine-bench 1.7.0: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **94.1** | 99.2 | 14/15 | 87.3 | 85.8 | 8 min 32 s | n/a | 2.30M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T23:41:44Z; bench at 651cc32f887e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 86 | 36.1 s | - | 1 | 5 | 2.7k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 89 | 44.1 s | - | 1 | 6 | 3.4k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 85 | 16.6 s | - | 1 | 3 | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 86 | 30.8 s | - | 2 | 7 | 1.2k | 0.1k | - |
| lc-changelog | ok | 100% | 5/5 | 96 | 8.9 s | - | 1 | 2 | 0.5k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 98 | 7.9 s | - | 1 | 1 | 0.4k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 96 | 20.8 s | - | 1 | 4 | 1.5k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 91 | 25.8 s | - | 1 | 7 | 1.7k | 0.1k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 86 | 15.6 s | - | 1 | 4 | 0.8k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 92 | 19.6 s | - | 1 | 4 | 1.1k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 94 | 28.9 s | - | 1 | 9 | 2.0k | 0.1k | - |
| rs-lock-bug | ok | 100% | 6/6 | 95 | 33.9 s | - | 1 | 4 | 2.0k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 88 | 48.8 s | - | 1 | 6 | 4.5k | 0.1k | - |
| 3d-voxel-landscape | ok | 100% | 7/7 | 58 | 1 min 13 s | - | 1 | 7 | 5.9k | 0.4k | - |
| web-word-universe | ok | 88% | 7/8 | 70 | 1 min 41 s | - | 1 | 19 | 8.7k | 0.3k | - |

## Failed checks

- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 1); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 3); recorded the result (call 3)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 7)
- `lc-changelog`: recorded the result (call 2)
- `vis-chart`: recorded the result (call 1)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 2); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 6)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 1); read the postmortem (call 1); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 2)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-voxel-landscape`: wrote the scene (call 4); looked at it in a browser (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 16); wrote the page (call 8); looked at it in a browser (call 10); recorded the result (call 16)
