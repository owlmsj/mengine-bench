# mengine-bench 1.7.3: opencode opencode v2.2.2 / qwen-cloud/qwen3.8-flash (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **78.4** | 94.9 | 12/15 | 78.7 | 12.6 | 26 min 51 s | >= $0.00 (harness) | 1.54M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T05:36:33Z; bench at 060d984b322e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 86 | 1 min 04 s | 0.0000 | 10 | 10 | 2.9k | 0.9k | 18 s |
| bo-pnl-runway | ok | 100% | 5/5 | 82 | 1 min 27 s | 0.0000 | 9 | 8 | 5.1k | 2.4k | 23 s |
| bo-reconcile | ok | 100% | 4/4 | 87 | 51.0 s | 0.0000 | 5 | 6 | 2.5k | 1.8k | - |
| cmp-handoff | ok | 91% | 10/11 | 63 | 1 min 07 s | 0.0000 | 13 | 11 | 2.3k | 0.9k | 18 s |
| lc-changelog | ok | 100% | 5/5 | 100 | 26.1 s | 0.0000 | 2 | 1 | 0.5k | 0.4k | 8 s |
| vis-chart | ok | 100% | 4/4 | 80 | 1 min 09 s | 0.0000 | 7 | 6 | 2.9k | 1.6k | 49 s |
| ds-sql-funnel | ok | 67% | 2/3 | 68 | 52.0 s | 0.0000 | 7 | 7 | 2.2k | 0.6k | 7 s |
| ue-packaged-bug | ok | 100% | 5/5 | 89 | 53.9 s | 0.0000 | 6 | 11 | 2.0k | 1.1k | 30 s |
| ir-studio-wiki | ok | 100% | 6/6 | 85 | 35.4 s | 0.0000 | 7 | 10 | 0.8k | 0.3k | 22 s |
| ir-server-logs | ok | 100% | 6/6 | 78 | 50.5 s | 0.0000 | 6 | 6 | 1.9k | 1.2k | 36 s |
| gd-integration-repo | ok | 100% | 8/8 | 80 | 2 min 07 s | 0.0000 | 10 | 20 | 6.9k | 4.5k | 96 s |
| rs-lock-bug | ok | 100% | 6/6 | 94 | 1 min 39 s | 0.0000 | 11 | 12 | 4.2k | 2.0k | 34 s |
| web-mondrian-landing | ok | 100% | 10/10 | 81 | 2 min 56 s | 0.0000 | 18 | 21 | 10.1k | 3.6k | 70 s |
| 3d-voxel-landscape | ok | 100% | 7/7 | 65 | 4 min 53 s | 0.0000 | 15 | 24 | 18.0k | 7.7k | 189 s |
| web-word-universe | timeout (timeout) | 67% | 4/6 | 43 | 6 min 00 s | - | 10 | 14 | 22.9k | 7.0k | 68 s |

## Failed checks

- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received "Re-run the local9 server block (scripts/start_server.ps1:165 / profiles/local/local-9b.json) launching Q5_K_M with '-ctx 131072 --no-mmproj-o
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.8252}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': 0.6667}}
- `web-word-universe` the page has a search field: no input, contenteditable or searchbox in universe/index.html
- `web-word-universe` opening the page with ?word= shows that word's relations: no universe/index.html

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 1); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 4)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 6); recorded the result (call 11)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 10)
- `ir-studio-wiki`: followed the bug (call 2); checked the approvals (call 2); read the postmortem (call 2); recorded the result (call 10)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 15)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 2); wrote the page (call 3); looked at it in a browser (call 1)
- `3d-voxel-landscape`: wrote the scene (call 4); looked at it in a browser (call 1)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 8); wrote the page (call 12); not seen: looked at it in a browser; recorded the result (call 8)
