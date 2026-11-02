# mengine-bench 2.0.0: claude 2.1.316 (Claude Code) / claude-sonnet-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **90.6** | 100.0 | 20/20 | 81.0 | 73.8 | 11 min 32 s | $2.54 (harness) | 3.73M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T18:31:27Z; bench at 1f752608d540; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 77 | 36.0 s | 0.1952 | 6 | 5 | 3.1k | 0.4k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 77 | 20.6 s | 0.1119 | 4 | 3 | 1.8k | 0.2k | - |
| bo-reconcile | ok | 100% | 4/4 | 85 | 21.2 s | 0.0955 | 4 | 3 | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 83 | 57.0 s | 0.2042 | 9 | 8 | 3.1k | 0.4k | - |
| cfg-source-drift | ok | 100% | 3/3 | 97 | 15.9 s | 0.0907 | 4 | 3 | 1.0k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 70 | 17.4 s | 0.0864 | 3 | 2 | 1.5k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 81 | 19.9 s | 0.0910 | 4 | 3 | 1.5k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 88 | 32.9 s | 0.1049 | 4 | 3 | 2.0k | 0.1k | - |
| git-merge-conflict | ok | 100% | 6/6 | 96 | 27.6 s | 0.0959 | 4 | 3 | 1.4k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 67 | 24.8 s | 0.0831 | 3 | 2 | 1.1k | 0.2k | - |
| ir-server-logs | ok | 100% | 6/6 | 71 | 40.8 s | 0.1165 | 6 | 5 | 1.5k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 85 | 43.2 s | 0.1242 | 6 | 5 | 2.4k | 0.2k | - |
| rs-lock-bug | ok | 100% | 6/6 | 88 | 37.0 s | 0.1123 | 5 | 4 | 2.5k | 0.3k | - |
| sec-leak-fix | ok | 100% | 8/8 | 92 | 27.2 s | 0.0990 | 4 | 3 | 1.8k | 0.2k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 83 | 22.7 s | 0.1311 | 6 | 5 | 2.4k | 0.3k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 93 | 21.2 s | 0.1086 | 5 | 4 | 2.1k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 91 | 32.9 s | 0.1087 | 3 | 2 | 3.1k | 0.3k | - |
| 3d-print-homage | ok | 100% | 11/11 | 47 | 45.3 s | 0.1387 | 3 | 2 | 4.9k | 1.0k | - |
| web-plan-ranking | ok | 100% | 8/8 | 75 | 1 min 30 s | 0.2627 | 12 | 17 | 5.8k | 0.9k | - |
| web-word-universe | ok | 100% | 8/8 | 74 | 58.3 s | 0.1785 | 8 | 7 | 6.2k | 0.4k | - |

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 5)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 3); not seen: used the cash balance; recorded the result (call 3)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 3)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 3); ran the whole suite (call 3)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 3)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: not seen: wrote the scene; not seen: looked at it in a browser; recorded the result (call 2)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 2); opened a source (call 2); recorded the result (call 15); wrote the dossier (call 16)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 5); wrote the page (call 6); not seen: looked at it in a browser; recorded the result (call 5)
