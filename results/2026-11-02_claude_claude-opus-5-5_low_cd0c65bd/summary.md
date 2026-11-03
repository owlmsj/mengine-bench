# mengine-bench 2.1.0: claude 2.1.317 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **90.9** | 98.1 | 19/20 | 77.0 | 83.7 | 9 min 04 s | $3.99 (harness) | 2.81M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code default clean install; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-03T01:56:34Z; bench at b50de1b0190f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 82 | 15.8 s | 0.1564 | 3 | 2 | 1.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 79 | 23.3 s | 0.2022 | 4 | 3 | 2.1k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 83 | 17.2 s | 0.1622 | 3 | 2 | 1.1k | 0.1k | - |
| cmp-handoff | ok | 100% | 11/11 | 82 | 46.1 s | 0.3171 | 8 | 6 | 2.5k | 0.0k | - |
| cfg-source-drift | ok | 100% | 3/3 | 93 | 10.4 s | 0.1408 | 3 | 2 | 0.7k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 67 | 14.7 s | 0.1511 | 3 | 2 | 1.4k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 79 | 17.2 s | 0.1547 | 3 | 2 | 1.6k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 86 | 17.9 s | 0.1742 | 4 | 3 | 1.6k | 0.1k | - |
| git-merge-conflict | ok | 100% | 6/6 | 93 | 20.4 s | 0.1584 | 4 | 3 | 1.2k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 65 | 15.6 s | 0.1449 | 3 | 2 | 1.1k | 0.2k | - |
| ir-server-logs | ok | 100% | 6/6 | 75 | 17.9 s | 0.2275 | 6 | 5 | 1.3k | 0.1k | - |
| gd-integration-repo | ok | 100% | 8/8 | 87 | 27.9 s | 0.1914 | 5 | 4 | 1.9k | 0.1k | - |
| rs-lock-bug | ok | 100% | 6/6 | 79 | 19.3 s | 0.1649 | 4 | 3 | 1.5k | 0.2k | - |
| sec-leak-fix | ok | 100% | 8/8 | 90 | 23.1 s | 0.1701 | 4 | 3 | 1.6k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 83 | 24.7 s | 0.2097 | 6 | 5 | 1.7k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 83 | 14.1 s | 0.1517 | 4 | 3 | 1.0k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 91 | 38.0 s | 0.2110 | 3 | 2 | 3.6k | 0.0k | - |
| 3d-print-homage | ok | 100% | 11/11 | 53 | 40.5 s | 0.2234 | 3 | 2 | 3.7k | 0.0k | - |
| web-plan-ranking | ok | 100% | 8/8 | 41 | 29.5 s | 0.1922 | 3 | 2 | 2.9k | 0.8k | - |
| web-word-universe | ok | 62% | 5/8 | 48 | 1 min 50 s | 0.4841 | 9 | 8 | 11.5k | 0.6k | - |

## Failed checks

- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: coração: missing 2 (avô, pulmão), extra 0 (none)
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 732, 'most_connected': 'palavra', 'most_connected_degree': 16}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 6)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 4)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; opened a source (call 2); recorded the result (call 2); wrote the dossier (call 2)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 3); wrote the page (call 5); not seen: looked at it in a browser; recorded the result (call 3)
