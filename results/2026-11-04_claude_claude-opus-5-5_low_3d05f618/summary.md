# mengine-bench 2.6.0: claude 2.1.318 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **80.5** | 97.3 | 25/28 | 77.9 | 50.9 | 17 min 17 s | $6.40 (harness) | 5.08M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-04, started 2026-11-04T21:38:04Z; bench at 0016e3a2fcfb; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 92 | 23.3 s | 0.1660 | 2 | 1 | 4.9 | 1.8k | 0.2k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 18.0 s | 0.1642 | 3 | 2 | 1.8 | 1.3k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 24.9 s | 0.2139 | 4 | 3 | 0.6 | 2.1k | 0.1k | - |
| bo-reconcile | ok | 100% | 5/5 | 80 | 20.8 s | 0.1743 | 3 | 2 | 1.6 | 1.0k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 75 | 37.0 s | 0.3461 | 7 | 5 | 0.4 | 2.5k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 95 | 23.2 s | 0.1559 | 3 | 2 | 2.1 | 0.9k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 64 | 23.2 s | 0.1679 | 3 | 2 | 1.7 | 1.5k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 78 | 21.5 s | 0.1733 | 3 | 2 | 1.7 | 1.8k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 87 | 22.1 s | 0.1931 | 4 | 3 | 0.9 | 1.8k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 92 | 29.5 s | 0.1820 | 5 | 4 | 1.2 | 1.5k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 66 | 25.2 s | 0.1611 | 3 | 2 | 1.5 | 1.2k | 0.2k | - |
| ir-server-logs | ok | 100% | 7/7 | 69 | 17.9 s | 0.2246 | 4 | 3 | 0.6 | 1.2k | 0.2k | - |
| gd-integration-repo | ok | 100% | 10/10 | 86 | 31.7 s | 0.2078 | 5 | 4 | 1.2 | 1.9k | 0.1k | - |
| media-voice | ok | 100% | 4/4 | 87 | 14.0 s | 0.1345 | 2 | 1 | 0.8 | 0.6k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 89 | 33.9 s | 0.2059 | 5 | 4 | 0.6 | 2.3k | 0.2k | - |
| txt-regex-log | ok | 100% | 5/5 | 94 | 22.4 s | 0.1656 | 2 | 1 | 2.9 | 1.7k | 0.6k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (10728)) | 100% | 9/9 | 90 | 25.9 s | 0.1948 | 4 | 3 | 1.2 | 2.1k | 0.2k | - |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 29.9 s | 0.1828 | 4 | 3 | 0.8 | 1.6k | 0.0k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 94 | 2 min 24 s | 0.5315 | 15 | 28 | 3.7 | 4.2k | 0.1k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 80 | 31.1 s | 0.2067 | 5 | 4 | 0.7 | 2.3k | 0.1k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 77 | 37.4 s | 0.2111 | 5 | 4 | 0.8 | 1.6k | 0.2k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 93 | 31.4 s | 0.1936 | 5 | 4 | 1.6 | 1.7k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 83 | 29.1 s | 0.2016 | 3 | 2 | 1.6 | 2.7k | 0.0k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.332 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 54 | 39.0 s | 0.2373 | 3 | 2 | 1.4 | 3.7k | 0.0k | - |
| web-fact-search | ok | 86% | 7/8 | 39 | 18.2 s | 0.1402 | 2 | 1 | 2.6 | 0.8k | 0.1k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61359", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156."}) | 100% | 9/9 | 83 | 2 min 40 s | 0.7137 | 22 | 28 | 2.3 | 6.8k | 0.6k | - |
| web-plan-ranking | ok | 75% | 7/9 | 25 | 33.8 s | 0.2147 | 3 | 2 | 1.6 | 3.2k | 0.7k | - |
| web-word-universe | ok | 62% | 6/9 | 61 | 1 min 08 s | 0.3350 | 9 | 8 | 0.8 | 5.5k | 0.4k | - |

## Failed checks

- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 1700, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 4)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 1); not seen: ran the integration test; not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 2); filled the permit (call 2)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 2)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 3)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); deleted the test post (call 23)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 1)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 4)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); not seen: opened a source
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 5); replied (call 20)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 2); wrote the dossier (call 2); not seen: opened a source
- `web-word-universe`: not seen: walked the site; wrote words.json (call 2); wrote the page (call 7); not seen: looked at it in a browser; recorded the result (call 2)
