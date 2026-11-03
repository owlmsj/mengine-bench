# mengine-bench 2.1.1: agy 1.4.12 / gemini-4-argon (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **70.9** | 98.3 | 13/20 | 79.5 | 0.0 | 42 min 08 s | n/a | 1.40M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: provider=agy-subscription; model=Gemini 4 Argon; harness=agy; role=default; personal_instructions=~/.gemini/GEMINI.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-03, started 2026-11-03T03:32:37Z; bench at 5d927dfc4cc2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 80 | 2 min 25 s | - | 13 | 13 | 8.6k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 82 | 1 min 43 s | - | 7 | 9 | 7.0k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 85 | 50.5 s | - | 5 | 6 | 3.0k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 89 | 1 min 22 s | - | 8 | 7 | 3.4k | 0.0k | - |
| cfg-source-drift | timeout (timeout) | 100% | 3/3 | 92 | 1 min 00 s | - | 5 | 13 | 0.8k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 78 | 45.9 s | - | 5 | 5 | 2.6k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 94 | 1 min 09 s | - | 5 | 6 | 3.4k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 92 | 1 min 08 s | - | 5 | 12 | 3.5k | 0.0k | - |
| git-merge-conflict | ok | 100% | 6/6 | 94 | 1 min 18 s | - | 8 | 8 | 2.4k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 84 | 40.7 s | - | 4 | 5 | 2.5k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 84 | 51.9 s | - | 6 | 7 | 2.5k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 85 | 2 min 17 s | - | 10 | 25 | 3.5k | 0.0k | - |
| rs-lock-bug | ok | 100% | 6/6 | 87 | 1 min 27 s | - | 8 | 9 | 4.8k | 0.0k | - |
| sec-leak-fix | ok | 100% | 8/8 | 86 | 1 min 10 s | - | 7 | 10 | 3.0k | 0.0k | - |
| hw-stutter-tuning | timeout (timeout) | 100% | 6/6 | 73 | 1 min 30 s | - | 8 | 11 | 2.1k | 0.0k | - |
| ts-plugin-bug | timeout (timeout) | 100% | 7/7 | 68 | 1 min 00 s | - | 6 | 9 | 2.0k | 0.0k | - |
| web-mondrian-landing | timeout (timeout) | 100% | 10/10 | 71 | 5 min 00 s | - | 17 | 19 | 17.1k | 0.0k | - |
| 3d-print-homage | timeout (timeout) | 100% | 11/11 | 64 | 7 min 00 s | - | 14 | 18 | 29.9k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 100% | 8/8 | 68 | 3 min 30 s | - | 10 | 12 | 13.1k | 0.0k | - |
| web-word-universe | timeout (timeout) | 67% | 4/6 | 34 | 6 min 00 s | - | 11 | 27 | 8.9k | 0.0k | - |

## Failed checks

- `web-word-universe` the page has a search field: no input, contenteditable or searchbox in universe/index.html
- `web-word-universe` opening the page with ?word= shows that word's relations: no universe/index.html

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 5); read the data (call 3); removed duplicate sessions (call 10); tested significance (call 16); recorded the result (call 24)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 3); used the chart of accounts (call 3); used the cash balance (call 3); recorded the result (call 14)
- `bo-reconcile`: read the notes (call 5); read the invoices (call 3); read the statement (call 3); recorded the result (call 9)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 6); recorded the result (call 14)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 3); not seen: extracted the text; recorded the result (call 8)
- `ds-sql-funnel`: read the rules (call 3); looked at the schema (call 4); excluded test accounts (call 4); recorded the result (call 10)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 3); recorded the result (call 13)
- `git-merge-conflict`: merged the branch (call 8); ran the tests (call 6); committed (call 14)
- `infra-gpu-fit`: read the offers (call 5); read the model (call 3); read the policy (call 4); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 3); read the logs (call 3); recorded the result (call 11)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 3); ran the whole suite (call 22)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 11)
- `sec-leak-fix`: read the service (call 3); read the config (call 3); ran the tests (call 13)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 3); recorded the result (call 20)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 13)
- `web-mondrian-landing`: read the fact sheet (call 3); wrote the page (call 7); looked at it in a browser (call 29)
- `3d-print-homage`: wrote the scene (call 11); looked at it in a browser (call 13); recorded the result (call 9)
- `web-plan-ranking`: read the rubric (call 3); searched the web (call 8); opened a source (call 8); recorded the result (call 23); wrote the dossier (call 24)
- `web-word-universe`: walked the site (call 3); wrote words.json (call 35); not seen: wrote the page; not seen: looked at it in a browser; recorded the result (call 35)
