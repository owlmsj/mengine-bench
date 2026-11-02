# mengine-bench 1.7.2: claude 2.1.316 (Claude Code) / claude-sonnet-5-5 (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **87.5** | 93.3 | 14/15 | 78.1 | 85.5 | 8 min 38 s | $2.18 (harness) | 2.85M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code default clean install; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-02T00:25:07Z; bench at 53f8ae3bf614; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 73 | 19.3 s | 0.0931 | 5 | 4 | 2.1k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 80 | 27.5 s | 0.1207 | 5 | 4 | 3.1k | 0.3k | - |
| bo-reconcile | ok | 100% | 4/4 | 77 | 13.3 s | 0.0875 | 4 | 3 | 1.3k | 0.0k | - |
| cmp-handoff | ok | 0% | 0/11 | 34 | 29.1 s | 0.1642 | 8 | 7 | 2.2k | 0.3k | - |
| lc-changelog | ok | 100% | 5/5 | 94 | 10.8 s | 0.2272 | 2 | 1 | 1.0k | 0.2k | - |
| vis-chart | ok | 100% | 4/4 | 98 | 9.3 s | 0.0657 | 3 | 2 | 0.6k | 0.1k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 83 | 16.2 s | 0.0850 | 4 | 4 | 1.8k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 93 | 17.3 s | 0.0888 | 4 | 3 | 1.7k | 0.2k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 94 | 15.0 s | 0.0900 | 6 | 5 | 1.4k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 68 | 21.4 s | 0.1201 | 7 | 6 | 2.0k | 0.2k | - |
| gd-integration-repo | ok | 100% | 8/8 | 94 | 26.0 s | 0.1096 | 5 | 4 | 2.3k | 0.2k | - |
| rs-lock-bug | ok | 100% | 6/6 | 89 | 21.4 s | 0.0914 | 4 | 3 | 2.2k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 76 | 29.6 s | 0.1204 | 4 | 4 | 4.4k | 0.3k | - |
| 3d-voxel-landscape | ok | 100% | 7/7 | 79 | 3 min 26 s | 0.5404 | 8 | 8 | 31.6k | 9.7k | - |
| web-word-universe | ok | 100% | 8/8 | 40 | 55.8 s | 0.1790 | 8 | 7 | 6.5k | 0.7k | - |

## Failed checks

- `cmp-handoff` summary exists and fits in 1000 characters: no summary file
- `cmp-handoff` summary keeps `--no-mmproj-offload`: `--no-mmproj-offload` is not in the summary
- `cmp-handoff` summary keeps `-ub 512`: `-ub 512` is not in the summary
- `cmp-handoff` summary keeps `7697`: `7697` is not in the summary
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for \\bQ6(?:_?K)?\\b', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 4)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 3); not seen: used the cash balance; recorded the result (call 3)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 7)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 2); read the postmortem (call 1); recorded the result (call 5)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 3); ran the whole suite (call 4)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); not seen: looked at it in a browser
- `3d-voxel-landscape`: wrote the scene (call 1); looked at it in a browser (call 1)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 5); wrote the page (call 6); not seen: looked at it in a browser; recorded the result (call 5)
