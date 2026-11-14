# mengine-bench 2.8.0: codex codex-cli 0.167.0 / gpt-6.1-terra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **91.0** | 98.0 | 26/29 | 81.0 | 93.0 | 12 min 06 s | ~$1.97 | 5.02M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-13, started 2026-11-14T01:49:52Z; bench at 435581dfc7d7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 75 | 56.2 s | - | 1 | 7 | - | 5.3k | 0.2k | - |
| py-async-cancel | ok | 100% | 6/6 | 91 | 22.8 s | - | 1 | 4 | - | 1.5k | 0.1k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 88 | 23.4 s | - | 1 | 5 | - | 2.1k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 85 | 19.5 s | - | 1 | 4 | - | 1.9k | 0.1k | - |
| bo-reconcile | ok | 100% | 5/5 | 81 | 11.3 s | - | 1 | 3 | - | 0.7k | 0.0k | - |
| cmp-handoff | ok | 91% | 11/12 | 73 | 22.7 s | - | 2 | 7 | - | 1.6k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 88 | 24.9 s | - | 1 | 7 | - | 2.1k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 61 | 13.0 s | - | 1 | 4 | - | 0.8k | 0.1k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 92 | 19.0 s | - | 1 | 5 | - | 1.5k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 85 | 14.0 s | - | 1 | 3 | - | 1.0k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 89 | 24.3 s | - | 1 | 6 | - | 1.4k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 79 | 9.9 s | - | 1 | 2 | - | 0.7k | 0.1k | - |
| ir-server-logs | ok | 100% | 7/7 | 86 | 14.7 s | - | 1 | 4 | - | 0.7k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 89 | 22.8 s | - | 1 | 6 | - | 1.8k | 0.1k | - |
| media-voice | ok | 100% | 4/4 | 85 | 10.2 s | - | 1 | 2 | - | 0.5k | 0.0k | - |
| file-media-edit | ok (workspace not kept: 90.09 MiB) | 100% | 10/10 | 67 | 42.9 s | - | 1 | 13 | - | 2.0k | 0.1k | - |
| txt-regex-log | ok | 100% | 5/5 | 89 | 22.1 s | - | 1 | 5 | - | 1.4k | 0.2k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (18276)) | 100% | 9/9 | 92 | 24.1 s | - | 1 | 4 | - | 1.9k | 0.1k | - |
| sec-leak-fix | ok | 100% | 10/10 | 87 | 29.9 s | - | 1 | 7 | - | 1.7k | 0.2k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 84 | 33.3 s | - | 1 | 16 | - | 1.5k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 88 | 20.5 s | - | 1 | 5 | - | 1.9k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 80 | 16.6 s | - | 1 | 5 | - | 1.0k | 0.0k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 90 | 16.9 s | - | 1 | 4 | - | 1.1k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 85 | 28.1 s | - | 1 | 8 | - | 3.0k | 0.1k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.642 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 64 | 43.3 s | - | 1 | 6 | - | 4.7k | 0.1k | - |
| web-fact-search | ok | 100% | 8/8 | 94 | 13.4 s | - | 1 | 3 | - | 0.7k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:56077", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157."}) | 100% | 9/9 | 88 | 27.5 s | - | 1 | 12 | - | 1.3k | 0.2k | - |
| web-plan-ranking | ok | 62% | 6/9 | 37 | 39.6 s | - | 1 | 6 | - | 4.1k | 0.2k | - |
| web-word-universe | ok | 88% | 8/9 | 57 | 1 min 00 s | - | 1 | 12 | - | 6.2k | 0.3k | - |

## Failed checks

- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received 'scripts/start_server.ps1 (local9 block) and profiles/local/local-9b.json; line numbers not provided'
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': '1986-02', 'Bresser': '1987-06', 'Verao': '1989-01', 'Collor I': '1990-03', 'Collor II': '1991
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 4256, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 2); looked at it in a browser (call 3)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 3); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 3); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 5); committed (call 6)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 6)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 5)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 5)
- `cu-social-cycle`: made the image (call 2); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 2); wrote the page (call 4); looked at it in a browser (call 6)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 3); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 6); replied (call 9)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 5); wrote the dossier (call 5); not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 6); wrote the page (call 7); looked at it in a browser (call 8); recorded the result (call 6)
