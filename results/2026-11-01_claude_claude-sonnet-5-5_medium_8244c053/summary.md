# mengine-bench 1.7.2: claude 2.1.316 (Claude Code) / claude-sonnet-5-5 (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **93.1** | 99.2 | 14/15 | 81.8 | 88.3 | 7 min 55 s | $1.99 (harness) | 3.06M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-02T00:48:53Z; bench at ff77cdc41a04; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 88 | 29.1 s | 0.1083 | 6 | 5 | 2.9k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 73 | 21.4 s | 0.1110 | 5 | 4 | 2.4k | 0.2k | - |
| bo-reconcile | ok | 100% | 4/4 | 86 | 16.0 s | 0.0863 | 4 | 3 | 1.3k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 79 | 32.0 s | 0.1808 | 8 | 9 | 3.2k | 0.4k | - |
| lc-changelog | ok | 100% | 5/5 | 95 | 13.7 s | 0.0726 | 2 | 1 | 1.1k | 0.3k | - |
| vis-chart | ok | 100% | 4/4 | 93 | 8.7 s | 0.0662 | 3 | 2 | 0.7k | 0.1k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 82 | 16.2 s | 0.0815 | 4 | 3 | 1.6k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 88 | 17.7 s | 0.0898 | 4 | 3 | 1.7k | 0.2k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 89 | 13.1 s | 0.0829 | 4 | 3 | 1.3k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 83 | 22.8 s | 0.1104 | 8 | 7 | 1.9k | 0.2k | - |
| gd-integration-repo | ok | 100% | 8/8 | 91 | 19.5 s | 0.1065 | 5 | 4 | 2.2k | 0.2k | - |
| rs-lock-bug | ok | 100% | 6/6 | 85 | 21.6 s | 0.0947 | 4 | 3 | 2.4k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 82 | 35.1 s | 0.1313 | 5 | 5 | 4.9k | 0.6k | - |
| 3d-voxel-landscape | ok | 100% | 7/7 | 78 | 2 min 04 s | 0.3827 | 7 | 7 | 21.1k | 2.3k | - |
| web-word-universe | ok | 88% | 7/8 | 35 | 1 min 24 s | 0.2802 | 10 | 9 | 12.1k | 0.6k | - |

## Failed checks

- `web-word-universe` page runs without script errors: Uncaught SyntaxError: Identifier 'top' has already been declared

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 5)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 3)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 9)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 3)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 2); read the postmortem (call 1); recorded the result (call 3)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 3); ran the whole suite (call 4)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); not seen: looked at it in a browser
- `3d-voxel-landscape`: wrote the scene (call 1); looked at it in a browser (call 3)
- `web-word-universe`: walked the site (call 3); wrote words.json (call 5); wrote the page (call 6); not seen: looked at it in a browser; recorded the result (call 5)
