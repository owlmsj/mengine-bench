# mengine-bench 2.0.0: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **84.7** | 99.4 | 19/20 | 84.5 | 56.0 | 16 min 00 s | n/a | 3.84M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T19:02:10Z; bench at 8f250b297086; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 86 | 39.9 s | - | 1 | 5 | - | 2.2k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 86 | 57.0 s | - | 1 | 9 | - | 4.4k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 83 | 18.4 s | - | 1 | 3 | - | 1.0k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 85 | 32.5 s | - | 2 | 7 | - | 1.5k | 0.0k | - |
| cfg-source-drift | ok | 100% | 3/3 | 87 | 25.3 s | - | 1 | 6 | - | 1.2k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 80 | 29.6 s | - | 1 | 6 | - | 1.4k | 0.1k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 91 | 40.1 s | - | 1 | 8 | - | 2.1k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 88 | 29.2 s | - | 1 | 5 | - | 1.6k | 0.0k | - |
| git-merge-conflict | ok | 100% | 6/6 | 81 | 34.1 s | - | 1 | 6 | - | 1.7k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 79 | 18.4 s | - | 1 | 2 | - | 1.0k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 85 | 20.9 s | - | 1 | 4 | - | 1.0k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 87 | 54.9 s | - | 1 | 15 | - | 2.9k | 0.2k | - |
| rs-lock-bug | ok | 100% | 6/6 | 91 | 44.2 s | - | 1 | 5 | - | 2.3k | 0.3k | - |
| sec-leak-fix | ok | 100% | 8/8 | 89 | 1 min 01 s | - | 1 | 10 | - | 3.0k | 0.5k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 91 | 28.6 s | - | 1 | 5 | - | 1.5k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 94 | 27.4 s | - | 1 | 6 | - | 1.5k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 89 | 1 min 05 s | - | 1 | 6 | - | 4.7k | 0.3k | - |
| 3d-print-homage | ok | 100% | 11/11 | 73 | 2 min 45 s | - | 1 | 13 | - | 7.4k | 0.9k | - |
| web-plan-ranking | ok | 100% | 8/8 | 88 | 1 min 10 s | - | 1 | 11 | - | 5.2k | 0.1k | - |
| web-word-universe | ok | 88% | 7/8 | 58 | 1 min 40 s | - | 1 | 11 | - | 7.7k | 0.3k | - |

## Failed checks

- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); not seen: recorded the result
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 8)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 4)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 3)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 1); read the config (call 1); ran the tests (call 2)
- `hw-stutter-tuning`: read the frame capture (call 2); read the sensor log (call 2); read the settings (call 1); read the owner notes (call 1); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 1); ran the tests (call 1)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 4)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; opened a source (call 5); recorded the result (call 3); wrote the dossier (call 3)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 7); looked at it in a browser (call 8); recorded the result (call 5)
