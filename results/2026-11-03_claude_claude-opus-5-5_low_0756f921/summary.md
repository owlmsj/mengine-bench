# mengine-bench 2.4.0: claude 2.1.317 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **88.0** | 98.7 | 27/28 | 78.2 | 69.0 | 12 min 45 s | $6.42 (harness) | 4.37M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-03, started 2026-11-03T22:12:36Z; bench at 2faa69ddb27b (dirty tree); submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 5/5 | 95 | 20.8 s | 0.1789 | 2 | 1 | 1.9 | 1.7k | 0.2k | - |
| ds-ab-playtest | ok | 100% | 4/4 | 85 | 15.8 s | 0.1900 | 3 | 2 | 0.5 | 1.4k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 77 | 22.7 s | 0.2295 | 4 | 3 | 0.3 | 2.3k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 86 | 16.2 s | 0.1892 | 3 | 2 | 0.5 | 1.4k | 0.2k | - |
| cmp-handoff | ok | 100% | 11/11 | 79 | 33.8 s | 0.3526 | 7 | 5 | 0.2 | 2.4k | 0.1k | - |
| cfg-source-drift | ok | 100% | 3/3 | 100 | 19.4 s | 0.1801 | 4 | 3 | 0.4 | 1.1k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 68 | 17.2 s | 0.1743 | 3 | 2 | 0.6 | 1.4k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 85 | 23.7 s | 0.1765 | 3 | 2 | 0.5 | 1.4k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 89 | 23.0 s | 0.2017 | 4 | 3 | 0.2 | 1.7k | 0.0k | - |
| git-merge-conflict | ok | 100% | 6/6 | 87 | 21.8 s | 0.1839 | 4 | 3 | 0.5 | 1.3k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 65 | 15.5 s | 0.1696 | 3 | 2 | 0.4 | 1.2k | 0.2k | - |
| ir-server-logs | ok | 100% | 6/6 | 73 | 27.7 s | 0.2417 | 5 | 4 | 0.2 | 1.3k | 0.1k | - |
| gd-integration-repo | ok | 100% | 8/8 | 88 | 26.6 s | 0.2269 | 5 | 4 | 0.7 | 2.1k | 0.2k | - |
| media-voice | ok | 100% | 3/3 | 86 | 13.8 s | 0.1428 | 2 | 1 | 0.7 | 0.6k | 0.0k | - |
| file-media-edit | ok | 100% | 9/9 | 85 | 21.8 s | 0.1881 | 4 | 3 | 0.5 | 1.6k | 0.1k | - |
| txt-regex-log | ok | 100% | 4/4 | 87 | 23.3 s | 0.1772 | 2 | 1 | 0.8 | 1.9k | 0.7k | - |
| rs-lock-bug | ok | 100% | 6/6 | 89 | 27.4 s | 0.2154 | 5 | 4 | 0.8 | 2.2k | 0.1k | - |
| sec-leak-fix | ok | 100% | 8/8 | 82 | 19.5 s | 0.1820 | 3 | 2 | 0.6 | 1.4k | 0.0k | - |
| cu-social-cycle | ok (route observed: scripted HTTP (0 of 3 writes with Sec-Fetch-*; user agents ['Python-urllib'])) | 100% | 10/10 | 68 | 1 min 03 s | 0.4706 | 9 | 8 | 0.3 | 2.8k | 0.2k | - |
| ds-sqlite-recover | ok | 100% | 5/5 | 80 | 28.5 s | 0.2168 | 4 | 3 | 0.3 | 2.2k | 0.2k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 79 | 25.6 s | 0.2472 | 6 | 5 | 0.3 | 2.0k | 0.2k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 92 | 38.1 s | 0.2147 | 6 | 5 | 0.7 | 1.8k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 88 | 37.8 s | 0.2429 | 4 | 3 | 0.2 | 3.7k | 0.2k | - |
| 3d-print-homage | ok | 100% | 11/11 | 54 | 48.0 s | 0.2700 | 3 | 2 | 0.4 | 4.6k | 0.2k | - |
| web-fact-search | ok | 100% | 6/6 | 42 | 11.4 s | 0.1487 | 2 | 1 | 0.7 | 0.8k | 0.1k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 100% | 8/8 | 93 | 37.6 s | 0.3199 | 12 | 11 | 0.3 | 2.6k | 0.2k | - |
| web-plan-ranking | ok | 100% | 8/8 | 40 | 35.3 s | 0.2290 | 3 | 2 | 0.5 | 3.4k | 0.8k | - |
| web-word-universe | ok | 62% | 5/8 | 48 | 49.5 s | 0.4645 | 7 | 6 | 0.3 | 4.8k | 0.3k | - |

## Failed checks

- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: coração: missing 2 (avô, pulmão), extra 0 (none)
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 732, 'most_connected': 'tempo'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); not seen: removed duplicate sessions; tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 2); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 3); filled the permit (call 3)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); deleted the test post (call 8)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 1)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); not seen: read the settings; not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; opened a source (call 1); recorded the result (call 1)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 7); replied (call 3)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; opened a source (call 2); recorded the result (call 2); wrote the dossier (call 2)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 2); wrote the page (call 4); looked at it in a browser (call 5); recorded the result (call 2)
