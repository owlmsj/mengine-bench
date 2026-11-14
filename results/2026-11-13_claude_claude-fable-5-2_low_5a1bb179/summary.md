# mengine-bench 2.8.0: claude 2.1.325 (Claude Code) / claude-fable-5-2 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **86.6** | 98.7 | 27/29 | 83.9 | 53.0 | 24 min 05 s | $15.62 | 5.03M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-13, started 2026-11-14T02:28:18Z; bench at 435581dfc7d7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 90 | 2 min 09 s | 1.0392 | 3 | 3 | 1.2 | 12.9k | 1.4k | - |
| py-async-cancel | ok | 100% | 6/6 | 90 | 31.0 s | 0.3876 | 2 | 2 | 1.8 | 2.6k | 0.6k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 40.7 s | 0.4477 | 4 | 3 | 1.2 | 3.2k | 0.3k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 35.5 s | 0.4653 | 3 | 2 | 2.0 | 2.8k | 0.3k | - |
| bo-reconcile | ok | 100% | 5/5 | 67 | 23.3 s | 0.3843 | 3 | 2 | 0.6 | 1.8k | 0.6k | - |
| cmp-handoff | ok | 100% | 12/12 | 90 | 37.0 s | 0.7019 | 6 | 5 | 0.2 | 2.3k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 100 | 23.5 s | 0.3465 | 4 | 3 | 0.8 | 1.3k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 84 | 25.5 s | 0.3565 | 3 | 2 | 1.5 | 1.8k | 0.3k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 83 | 26.7 s | 0.3648 | 3 | 2 | 1.4 | 1.9k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 31.6 s | 0.4188 | 4 | 3 | 0.8 | 2.2k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 98 | 29.1 s | 0.3788 | 4 | 3 | 1.1 | 1.8k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 64 | 20.6 s | 0.3281 | 3 | 2 | 1.1 | 1.3k | 0.2k | - |
| ir-server-logs | ok | 100% | 7/7 | 80 | 27.0 s | 0.5421 | 4 | 3 | 0.6 | 1.6k | 0.2k | - |
| gd-integration-repo | ok | 100% | 10/10 | 88 | 44.2 s | 0.5171 | 5 | 4 | 1.1 | 3.4k | 0.4k | - |
| media-voice | ok | 100% | 4/4 | 81 | 13.4 s | 0.2814 | 2 | 1 | 1.2 | 0.7k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 84 | 38.1 s | 0.4221 | 4 | 3 | 0.9 | 2.7k | 0.5k | - |
| txt-regex-log | ok | 100% | 5/5 | 91 | 27.4 s | 0.3531 | 2 | 1 | 2.7 | 2.0k | 0.7k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (18424)) | 100% | 9/9 | 94 | 38.3 s | 0.4290 | 3 | 2 | 3.0 | 2.9k | 0.3k | - |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 40.2 s | 0.4494 | 3 | 2 | 2.4 | 3.2k | 0.2k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 91 | 2 min 35 s | 1.1274 | 15 | 25 | 3.5 | 5.7k | 0.1k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 84 | 35.2 s | 0.3997 | 3 | 2 | 1.5 | 2.6k | 0.5k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 93 | 38.2 s | 0.4610 | 5 | 4 | 1.0 | 2.5k | 0.2k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 90 | 40.0 s | 0.4563 | 4 | 3 | 1.8 | 3.1k | 0.3k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 92 | 1 min 05 s | 0.6261 | 5 | 5 | 1.1 | 5.9k | 0.7k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.605 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 83 | 2 min 44 s | 1.1543 | 5 | 6 | 0.7 | 14.7k | 5.4k | - |
| web-fact-search | ok | 100% | 8/8 | 95 | 20.7 s | 0.3180 | 2 | 2 | 2.1 | 1.3k | 0.2k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 100% | 9/9 | 95 | 54.4 s | 0.8501 | 8 | 8 | 1.0 | 3.6k | 0.3k | - |
| web-plan-ranking | ok | 75% | 7/9 | 44 | 1 min 01 s | 0.5866 | 4 | 8 | 3.8 | 4.5k | 1.3k | - |
| web-word-universe | ok | 88% | 8/9 | 32 | 2 min 10 s | 1.0229 | 8 | 9 | 1.0 | 11.6k | 1.0k | - |

## Failed checks

- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Collor II']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2046, 'urls': 2, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` page runs without script errors: Uncaught SyntaxError: Identifier 'top' has already been declared

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); not seen: looked at it in a browser
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; not seen: read the invoices; not seen: read the statement; recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 2); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 4)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 2); filled the permit (call 2)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 2)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); deleted the test post (call 23)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 1)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); not seen: read the owner notes; recorded the result (call 4)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 4); replied (call 4)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 2); recorded the result (call 7); wrote the dossier (call 7); opened a source (call 3)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 3); wrote the page (call 3); not seen: looked at it in a browser; recorded the result (call 3)
