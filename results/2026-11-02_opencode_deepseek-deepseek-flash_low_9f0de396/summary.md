# mengine-bench 2.0.0: opencode opencode v2.2.5 / deepseek/deepseek-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **70.4** | 94.5 | 17/20 | 85.0 | 3.9 | 29 min 01 s | >= $0.18 (harness) | 7.43M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T20:30:07Z; bench at fa60fc805d87; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 80 | 2 min 28 s | 0.0103 | 17 | 18 | 13.8k | 6.2k | 131 s |
| bo-pnl-runway | ok | 100% | 5/5 | 85 | 49.0 s | 0.0065 | 13 | 16 | 7.3k | 1.9k | 7 s |
| bo-reconcile | ok | 100% | 4/4 | 94 | 26.2 s | 0.0034 | 8 | 9 | 3.3k | 1.2k | 10 s |
| cmp-handoff | ok | 91% | 10/11 | 74 | 29.8 s | 0.0041 | 10 | 9 | 3.1k | 1.1k | 9 s |
| cfg-source-drift | ok | 100% | 3/3 | 93 | 39.4 s | 0.0050 | 14 | 20 | 5.2k | 0.8k | 6 s |
| doc-lab-pdf | ok | 100% | 6/6 | 86 | 24.1 s | 0.0027 | 9 | 10 | 2.5k | 0.9k | 16 s |
| ds-sql-funnel | ok | 0% | 0/3 | 58 | 45.3 s | 0.0050 | 17 | 17 | 5.1k | 1.5k | 8 s |
| ue-packaged-bug | ok | 100% | 5/5 | 86 | 36.2 s | 0.0046 | 11 | 16 | 4.6k | 1.9k | 16 s |
| git-merge-conflict | ok | 100% | 6/6 | 100 | 23.8 s | 0.0030 | 9 | 12 | 2.4k | 0.7k | 10 s |
| infra-gpu-fit | ok | 100% | 6/6 | 88 | 15.4 s | 0.0022 | 5 | 6 | 2.0k | 0.5k | 6 s |
| ir-server-logs | ok | 100% | 6/6 | 89 | 34.9 s | 0.0056 | 13 | 13 | 4.0k | 1.6k | 18 s |
| gd-integration-repo | ok | 100% | 8/8 | 94 | 46.4 s | 0.0066 | 11 | 26 | 6.6k | 3.4k | 23 s |
| rs-lock-bug | ok | 100% | 6/6 | 88 | 56.3 s | 0.0077 | 6 | 7 | 8.0k | 5.5k | 39 s |
| sec-leak-fix | ok | 100% | 8/8 | 91 | 59.3 s | 0.0073 | 12 | 19 | 8.9k | 4.2k | 26 s |
| hw-stutter-tuning | ok | 100% | 6/6 | 91 | 50.6 s | 0.0066 | 9 | 10 | 7.1k | 4.6k | 42 s |
| ts-plugin-bug | ok | 100% | 7/7 | 94 | 25.1 s | 0.0034 | 7 | 10 | 3.6k | 0.9k | 7 s |
| web-mondrian-landing | timeout (timeout) | 100% | 10/10 | 72 | 5 min 00 s | - | 59 | 60 | 33.3k | 19.5k | 70 s |
| 3d-print-homage | ok | 100% | 11/11 | 73 | 6 min 11 s | 0.0397 | 40 | 71 | 51.9k | 26.1k | 92 s |
| web-plan-ranking | ok | 100% | 8/8 | 84 | 1 min 14 s | 0.0228 | 17 | 28 | 11.0k | 4.1k | 53 s |
| web-word-universe | ok | 100% | 8/8 | 80 | 4 min 47 s | 0.0348 | 61 | 61 | 39.4k | 15.1k | 9 s |

## Failed checks

- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'pwsh ./scripts/start_server.ps1 -Profile local-9b --no-mmproj-offload -ub 512'
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 1); read the data (call 1); removed duplicate sessions (call 3); tested significance (call 10); recorded the result (call 16)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 12)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 5); recorded the result (call 9)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 2); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 3); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 7); ran the tests (call 3); committed (call 7)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 3)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 1); read the config (call 1); ran the tests (call 5)
- `hw-stutter-tuning`: read the frame capture (call 1); read the sensor log (call 1); read the settings (call 1); read the owner notes (call 1); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 1); ran the tests (call 2)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 6); recorded the result (call 41)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 4); opened a source (call 4); recorded the result (call 26); wrote the dossier (call 27)
- `web-word-universe`: walked the site (call 3); wrote words.json (call 17); wrote the page (call 20); looked at it in a browser (call 22); recorded the result (call 17)
