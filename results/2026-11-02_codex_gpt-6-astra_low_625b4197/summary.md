# mengine-bench 2.0.0: codex codex-cli 0.165.0 / gpt-6-astra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **85.0** | 100.0 | 20/20 | 87.0 | 53.2 | 16 min 42 s | n/a | 3.57M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T21:54:43Z; bench at d5cea094f23f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 91 | 44.9 s | - | 1 | 5 | - | 3.0k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 86 | 48.0 s | - | 1 | 5 | - | 3.2k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 84 | 23.7 s | - | 1 | 3 | - | 1.1k | 0.1k | - |
| cmp-handoff | ok | 100% | 11/11 | 82 | 36.3 s | - | 2 | 6 | - | 1.3k | 0.0k | - |
| cfg-source-drift | ok | 100% | 3/3 | 86 | 37.5 s | - | 1 | 8 | - | 1.9k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 79 | 39.5 s | - | 1 | 7 | - | 2.0k | 0.1k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 92 | 23.2 s | - | 1 | 3 | - | 1.6k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 89 | 40.8 s | - | 1 | 9 | - | 2.0k | 0.1k | - |
| git-merge-conflict | ok | 100% | 6/6 | 87 | 39.0 s | - | 1 | 6 | - | 2.4k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 83 | 16.4 s | - | 1 | 2 | - | 1.0k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 87 | 22.4 s | - | 1 | 4 | - | 1.0k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 95 | 48.6 s | - | 1 | 8 | - | 2.8k | 0.2k | - |
| rs-lock-bug | ok | 100% | 6/6 | 84 | 39.8 s | - | 1 | 7 | - | 2.2k | 0.2k | - |
| sec-leak-fix | ok | 100% | 8/8 | 91 | 39.3 s | - | 1 | 4 | - | 1.9k | 0.3k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 93 | 28.5 s | - | 1 | 5 | - | 1.5k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 94 | 32.1 s | - | 1 | 7 | - | 1.7k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 86 | 58.2 s | - | 1 | 5 | - | 4.2k | 0.1k | - |
| 3d-print-homage | ok | 100% | 11/11 | 83 | 2 min 27 s | - | 1 | 12 | - | 7.5k | 1.0k | - |
| web-plan-ranking | ok | 100% | 8/8 | 85 | 1 min 37 s | - | 1 | 13 | - | 4.6k | 0.4k | - |
| web-word-universe | ok | 100% | 8/8 | 83 | 2 min 20 s | - | 1 | 13 | - | 8.8k | 0.5k | - |

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 3); recorded the result (call 3)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 1); recorded the result (call 3)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 6)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 2)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 1); read the config (call 1); ran the tests (call 2)
- `hw-stutter-tuning`: read the frame capture (call 2); read the sensor log (call 2); read the settings (call 1); read the owner notes (call 1); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 1); ran the tests (call 2)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 2)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 2); recorded the result (call 4)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: opened a source; recorded the result (call 3); wrote the dossier (call 3)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 6); wrote the page (call 7); looked at it in a browser (call 7); recorded the result (call 6)
