# mengine-bench 2.1.0: claude 2.1.317 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **91.4** | 98.8 | 19/20 | 79.0 | 82.1 | 9 min 28 s | $4.39 (harness) | 2.93M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-03T01:36:54Z; bench at b50de1b0190f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 82 | 16.0 s | 0.1880 | 3 | 2 | 1.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 79 | 26.3 s | 0.2307 | 4 | 3 | 2.3k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 79 | 16.8 s | 0.1815 | 3 | 2 | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 84 | 26.6 s | 0.3532 | 7 | 5 | 2.1k | 0.0k | - |
| cfg-source-drift | ok | 100% | 3/3 | 95 | 14.1 s | 0.1651 | 3 | 2 | 0.9k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 72 | 19.3 s | 0.1753 | 3 | 3 | 1.4k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 77 | 19.3 s | 0.1783 | 3 | 2 | 1.6k | 0.2k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 85 | 21.2 s | 0.2089 | 4 | 3 | 1.9k | 0.1k | - |
| git-merge-conflict | ok | 100% | 6/6 | 92 | 17.2 s | 0.1849 | 4 | 3 | 1.4k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 77 | 15.1 s | 0.1724 | 3 | 2 | 1.3k | 0.3k | - |
| ir-server-logs | ok | 100% | 6/6 | 71 | 22.6 s | 0.2302 | 4 | 3 | 1.2k | 0.1k | - |
| gd-integration-repo | ok | 100% | 8/8 | 92 | 39.0 s | 0.2381 | 6 | 5 | 2.3k | 0.1k | - |
| rs-lock-bug | ok | 100% | 6/6 | 82 | 16.6 s | 0.1769 | 3 | 2 | 1.4k | 0.1k | - |
| sec-leak-fix | ok | 100% | 8/8 | 90 | 25.3 s | 0.1842 | 3 | 2 | 1.5k | 0.1k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 84 | 40.5 s | 0.2265 | 6 | 5 | 1.6k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 86 | 33.2 s | 0.2097 | 5 | 4 | 1.9k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 90 | 47.1 s | 0.2631 | 5 | 4 | 4.0k | 0.2k | - |
| 3d-print-homage | ok | 100% | 11/11 | 65 | 49.2 s | 0.2715 | 3 | 2 | 4.6k | 0.3k | - |
| web-plan-ranking | ok | 100% | 8/8 | 35 | 30.1 s | 0.2211 | 3 | 2 | 3.1k | 0.7k | - |
| web-word-universe | ok | 75% | 6/8 | 62 | 1 min 12 s | 0.3286 | 8 | 7 | 5.4k | 0.4k | - |

## Failed checks

- `web-word-universe` relations of a sample of words: avó: missing 2 (avô, pai), extra 0 (none)
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 734, 'most_connected': ['palavra', 'tempo']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); not seen: removed duplicate sessions; tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 5)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 2)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; opened a source (call 2); recorded the result (call 2); wrote the dossier (call 2)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 2); wrote the page (call 7); not seen: looked at it in a browser; recorded the result (call 2)
