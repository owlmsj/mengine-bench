# mengine-bench 2.8.0: claude 2.1.325 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **88.4** | 98.2 | 26/29 | 77.3 | 83.4 | 14 min 59 s | $6.83 | 4.94M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-13, started 2026-11-14T01:33:18Z; bench at 435581dfc7d7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 80 | 1 min 07 s | 0.3500 | 3 | 2 | 1.2 | 7.0k | 0.2k | - |
| py-async-cancel | ok | 100% | 6/6 | 92 | 19.4 s | 0.1706 | 2 | 1 | 2.7 | 1.6k | 0.2k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 80 | 18.6 s | 0.1803 | 3 | 2 | 1.6 | 1.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 73 | 21.7 s | 0.2090 | 3 | 2 | 1.2 | 1.8k | 0.1k | - |
| bo-reconcile | ok | 100% | 5/5 | 85 | 16.1 s | 0.1896 | 3 | 2 | 1.4 | 1.2k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 81 | 33.5 s | 0.3641 | 7 | 5 | 0.6 | 2.4k | 0.1k | - |
| cfg-source-drift | ok | 100% | 5/5 | 84 | 15.0 s | 0.1619 | 3 | 2 | 1.9 | 0.8k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 69 | 19.4 s | 0.1773 | 3 | 2 | 1.7 | 1.5k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 80 | 19.6 s | 0.1773 | 3 | 2 | 1.5 | 1.5k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 84 | 22.4 s | 0.2081 | 4 | 3 | 0.7 | 1.8k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 91 | 22.9 s | 0.1975 | 5 | 4 | 1.3 | 1.3k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 70 | 18.1 s | 0.1739 | 3 | 2 | 1.8 | 1.3k | 0.2k | - |
| ir-server-logs | ok | 100% | 7/7 | 72 | 22.0 s | 0.2360 | 4 | 3 | 0.9 | 1.4k | 0.1k | - |
| gd-integration-repo | ok | 100% | 10/10 | 89 | 32.4 s | 0.2455 | 6 | 5 | 0.9 | 2.5k | 0.3k | - |
| media-voice | ok | 100% | 4/4 | 82 | 12.0 s | 0.1456 | 2 | 1 | 1.8 | 0.7k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 87 | 23.4 s | 0.1937 | 4 | 3 | 1.1 | 1.8k | 0.2k | - |
| txt-regex-log | ok | 100% | 5/5 | 92 | 24.2 s | 0.1812 | 2 | 1 | 2.7 | 2.0k | 0.6k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (32192)) | 100% | 9/9 | 94 | 27.5 s | 0.2037 | 4 | 3 | 2.7 | 2.0k | 0.1k | - |
| sec-leak-fix | ok | 100% | 10/10 | 84 | 22.8 s | 0.1895 | 3 | 2 | 1.8 | 1.6k | 0.1k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 90 | 2 min 02 s | 0.6494 | 18 | 28 | 2.7 | 4.8k | 0.2k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 81 | 30.7 s | 0.2142 | 4 | 3 | 0.9 | 2.4k | 0.4k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 85 | 25.6 s | 0.2272 | 6 | 5 | 0.8 | 1.7k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 21.9 s | 0.1962 | 5 | 4 | 1.1 | 1.4k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 76 | 36.0 s | 0.2431 | 4 | 3 | 0.5 | 3.6k | 0.2k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.356 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 47 | 42.8 s | 0.2592 | 4 | 3 | 0.5 | 3.8k | 0.1k | - |
| web-fact-search | ok | 86% | 7/8 | 36 | 11.8 s | 0.1500 | 2 | 1 | 2.3 | 0.8k | 0.1k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 100% | 9/9 | 88 | 45.8 s | 0.3308 | 11 | 10 | 0.7 | 3.6k | 0.2k | - |
| web-plan-ranking | ok | 75% | 7/9 | 36 | 28.0 s | 0.2058 | 3 | 2 | 1.1 | 2.5k | 0.9k | - |
| web-word-universe | ok | 88% | 8/9 | 40 | 1 min 16 s | 0.3958 | 9 | 8 | 1.1 | 7.1k | 0.7k | - |

## Failed checks

- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2296, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` page runs without script errors: Uncaught SyntaxError: Identifier 'top' has already been declared

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); not seen: looked at it in a browser
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); not seen: removed duplicate sessions; tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 4); committed (call 4)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 5)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 2); filled the permit (call 2)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 2)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); deleted the test post (call 24)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 1)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); not seen: read the settings; not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); not seen: opened a source
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 6); replied (call 4)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 2); wrote the dossier (call 2); not seen: opened a source
- `web-word-universe`: walked the site (call 4); wrote words.json (call 4); wrote the page (call 7); not seen: looked at it in a browser; recorded the result (call 4)
