# mengine-bench 2.0.0: claude 2.1.316 (Claude Code) / claude-fable-5-1 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **82.5** | 99.4 | 19/20 | 85.0 | 40.8 | 19 min 47 s | $16.00 (harness) | 4.56M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T21:29:06Z; bench at d5cea094f23f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 80 | 23.9 s | 0.8905 | 3 | 2 | 1.7k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 84 | 1 min 54 s | 0.6436 | 4 | 3 | 3.5k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 84 | 18.1 s | 0.4510 | 3 | 2 | 1.3k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 86 | 46.0 s | 0.8871 | 6 | 4 | 2.4k | 0.0k | - |
| cfg-source-drift | ok | 100% | 3/3 | 100 | 18.1 s | 0.4391 | 4 | 3 | 1.1k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 80 | 34.7 s | 0.4555 | 3 | 2 | 1.8k | 0.3k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 86 | 22.9 s | 0.4385 | 3 | 2 | 1.6k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 88 | 51.5 s | 0.5680 | 4 | 3 | 2.7k | 0.3k | - |
| git-merge-conflict | ok | 100% | 6/6 | 84 | 29.3 s | 0.4687 | 4 | 3 | 1.5k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 86 | 22.9 s | 0.4496 | 3 | 2 | 1.8k | 0.3k | - |
| ir-server-logs | ok | 100% | 6/6 | 82 | 26.0 s | 0.6579 | 5 | 4 | 1.7k | 0.2k | - |
| gd-integration-repo | ok | 100% | 8/8 | 93 | 1 min 12 s | 0.6116 | 6 | 5 | 2.9k | 0.1k | - |
| rs-lock-bug | ok | 100% | 6/6 | 94 | 51.2 s | 0.5894 | 5 | 4 | 3.3k | 0.3k | - |
| sec-leak-fix | ok | 100% | 8/8 | 98 | 28.4 s | 0.4841 | 3 | 2 | 2.1k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 89 | 34.1 s | 0.6145 | 5 | 4 | 2.4k | 0.2k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 89 | 29.6 s | 0.4909 | 3 | 2 | 2.1k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 86 | 2 min 47 s | 1.9033 | 9 | 8 | 12.6k | 0.3k | - |
| 3d-print-homage | ok | 100% | 11/11 | 73 | 3 min 32 s | 2.5176 | 19 | 18 | 16.6k | 1.4k | - |
| web-plan-ranking | ok | 100% | 8/8 | 77 | 1 min 27 s | 0.9497 | 8 | 18 | 6.7k | 1.4k | - |
| web-word-universe | ok | 88% | 7/8 | 60 | 1 min 39 s | 1.4933 | 9 | 8 | 7.7k | 0.4k | - |

## Failed checks

- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 3); recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 4)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 2); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); not seen: ran the whole suite
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); not seen: read the owner notes; recorded the result (call 4)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 2)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 6)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 5); recorded the result (call 2)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 2); opened a source (call 2); recorded the result (call 17); wrote the dossier (call 18)
- `web-word-universe`: walked the site (call 3); wrote words.json (call 2); wrote the page (call 5); looked at it in a browser (call 6); recorded the result (call 2)
