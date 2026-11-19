# mengine-bench 2.8.0: opencode opencode v2.2.5 / deepseek/deepseek-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **80.0** | 99.4 | 24/29 | 84.3 | 5.3 | 38 min 25 s | >= $0.18 | 7.17M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=deepseek; tier=1; role=default; model_version=DeepSeek-V4.1-Flash-1017 (no fast tier on the DeepSeek API); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T16:38:42Z; bench at 0b7d01bbdec2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 80 | 4 min 33 s | 0.0259 | 38 | 49 | 0.9 | 29.1k | 8.5k | 58 s |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 74 | 1 min 00 s | - | 6 | 6 | 2.2 | 4.6k | 1.4k | 4 s |
| ds-ab-playtest | ok | 100% | 5/5 | 89 | 1 min 12 s | 0.0072 | 18 | 18 | 1.1 | 8.9k | 1.8k | 7 s |
| bo-pnl-runway | ok | 100% | 6/6 | 69 | 1 min 32 s | 0.0110 | 22 | 25 | 0.7 | 12.1k | 2.9k | 63 s |
| bo-reconcile | ok | 100% | 5/5 | 81 | 14.3 s | 0.0019 | 6 | 5 | 0.6 | 1.2k | 0.1k | 7 s |
| cmp-handoff | ok | 100% | 12/12 | 89 | 29.4 s | 0.0041 | 11 | 9 | 0.5 | 3.0k | 1.3k | 10 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 16.6 s | 0.0022 | 7 | 10 | 0.4 | 1.6k | 0.2k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 84 | 27.9 s | 0.0032 | 8 | 9 | 0.7 | 3.3k | 1.5k | 16 s |
| ds-sql-funnel | ok | 100% | 5/5 | 85 | 27.7 s | 0.0032 | 9 | 8 | 0.9 | 3.2k | 0.8k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 93 | 28.4 s | 0.0034 | 7 | 9 | 0.5 | 3.5k | 1.7k | 12 s |
| git-merge-conflict | ok | 100% | 7/7 | 92 | 19.7 s | 0.0023 | 8 | 9 | 0.7 | 1.8k | 0.2k | 9 s |
| infra-gpu-fit | ok | 100% | 7/7 | 91 | 12.6 s | 0.0018 | 4 | 5 | 0.4 | 1.5k | 0.3k | 4 s |
| ir-server-logs | ok | 83% | 6/7 | 60 | 24.7 s | 0.0033 | 10 | 9 | 0.6 | 2.0k | 0.6k | 17 s |
| gd-integration-repo | ok | 100% | 10/10 | 91 | 29.0 s | 0.0043 | 8 | 22 | 0.9 | 3.7k | 0.9k | 16 s |
| media-voice | timeout (timeout) | 100% | 4/4 | 70 | 1 min 00 s | - | 10 | 12 | 0.8 | 2.2k | 0.4k | 4 s |
| file-media-edit | ok | 100% | 10/10 | 92 | 32.0 s | 0.0031 | 9 | 12 | 1.2 | 2.7k | 0.9k | - |
| txt-regex-log | ok | 100% | 5/5 | 98 | 38.8 s | 0.0046 | 8 | 9 | 0.4 | 5.8k | 3.4k | 18 s |
| rs-lock-bug | ok | 100% | 9/9 | 92 | 1 min 05 s | 0.0041 | 9 | 11 | 0.6 | 4.5k | 1.6k | 13 s |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 43.7 s | 0.0055 | 10 | 14 | 0.9 | 6.4k | 2.6k | 16 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 85 | 1 min 42 s | 0.0120 | 43 | 52 | 0.4 | 7.3k | 2.1k | 16 s |
| ds-sqlite-recover | ok | 100% | 6/6 | 85 | 53.5 s | 0.0063 | 6 | 6 | 0.8 | 8.5k | 6.6k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 1 min 01 s | 0.0089 | 14 | 13 | 1.1 | 7.5k | 4.4k | 52 s |
| ts-plugin-bug | ok | 100% | 8/8 | 94 | 27.9 s | 0.0031 | 12 | 11 | 0.6 | 2.7k | 0.4k | 11 s |
| web-mondrian-landing | timeout (timeout) | 100% | 11/11 | 76 | 5 min 00 s | - | 58 | 58 | 1.1 | 28.2k | 12.3k | 53 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.404 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 70 | 4 min 19 s | 0.0286 | 25 | 37 | 1.3 | 38.5k | 21.1k | 91 s |
| web-fact-search | ok | 100% | 8/8 | 90 | 13.1 s | 0.0059 | 5 | 6 | 0.6 | 1.1k | 0.3k | 7 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:58312", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 89 | 1 min 03 s | 0.0076 | 27 | 30 | 0.5 | 5.4k | 1.5k | - |
| web-plan-ranking | ok | 100% | 9/9 | 83 | 1 min 37 s | 0.0174 | 17 | 22 | 0.7 | 14.7k | 8.4k | 75 s |
| web-word-universe | timeout (timeout) | 100% | 9/9 | 68 | 6 min 00 s | - | 53 | 56 | 1.5 | 57.3k | 18.1k | 62 s |

## Failed checks

- `ir-server-logs` June availability: expected 99.9170910493827, received 99.9503

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 4)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 5); tested significance (call 7); recorded the result (call 15)
- `bo-pnl-runway`: read the notes (call 5); read the ledger (call 6); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 9)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 4)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 4); recorded the result (call 7)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 3); recorded the result (call 7)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 8)
- `git-merge-conflict`: merged the branch (call 6); ran the tests (call 8); committed (call 8)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 3); ran the whole suite (call 22)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 6)
- `file-media-edit`: read the details (call 1); made the feed photo (call 7); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 5)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 16); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 5); wrote the JSON (call 5)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 4); read the owner notes (call 4); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 2); recorded the result (call 5)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 9); downloaded the invoice (call 9); replied (call 19)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 16); wrote the dossier (call 17); opened a source (call 4)
- `web-word-universe`: walked the site (call 5); wrote words.json (call 11); wrote the page (call 18); looked at it in a browser (call 23); recorded the result (call 15)
