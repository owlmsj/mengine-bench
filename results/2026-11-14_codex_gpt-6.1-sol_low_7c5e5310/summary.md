# mengine-bench 2.8.0: codex codex-cli 0.167.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **86.9** | 99.4 | 28/29 | 85.7 | 48.6 | 25 min 25 s | ~$4.58 | 5.68M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-14, started 2026-11-14T08:13:29Z; bench at 53610619ea57; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 77 | 2 min 10 s | - | 1 | 11 | - | 7.1k | 0.4k | - |
| py-async-cancel | ok | 100% | 6/6 | 88 | 30.7 s | - | 1 | 3 | - | 1.4k | 0.1k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 89 | 45.3 s | - | 1 | 5 | - | 2.1k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 88 | 1 min 06 s | - | 1 | 7 | - | 3.2k | 0.0k | - |
| bo-reconcile | ok | 100% | 5/5 | 80 | 24.4 s | - | 1 | 3 | - | 1.0k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 83 | 38.9 s | - | 2 | 8 | - | 1.5k | 0.1k | - |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 28.2 s | - | 1 | 7 | - | 1.0k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 71 | 31.2 s | - | 1 | 5 | - | 1.0k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 94 | 55.4 s | - | 1 | 4 | - | 1.4k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 34.2 s | - | 1 | 8 | - | 1.5k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 83 | 42.2 s | - | 1 | 6 | - | 1.8k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 79 | 18.0 s | - | 1 | 2 | - | 0.8k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 93 | 26.4 s | - | 1 | 5 | - | 1.0k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 92 | 38.5 s | - | 1 | 7 | - | 1.7k | 0.1k | - |
| media-voice | ok | 100% | 4/4 | 89 | 28.8 s | - | 1 | 5 | - | 1.0k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 65 | 49.7 s | - | 1 | 7 | - | 1.8k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 97 | 30.9 s | - | 1 | 2 | - | 1.7k | 0.2k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (6996)) | 100% | 9/9 | 92 | 1 min 01 s | - | 1 | 7 | - | 2.3k | 0.2k | - |
| sec-leak-fix | ok | 100% | 10/10 | 81 | 47.1 s | - | 1 | 5 | - | 2.1k | 0.3k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 91 | 55.5 s | - | 1 | 13 | - | 1.6k | 0.1k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 89 | 29.4 s | - | 1 | 3 | - | 1.3k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 92 | 31.1 s | - | 1 | 5 | - | 1.4k | 0.0k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 35.6 s | - | 1 | 5 | - | 1.6k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 86 | 1 min 36 s | - | 1 | 9 | - | 4.7k | 0.2k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.509 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 77 | 2 min 09 s | - | 1 | 8 | - | 6.2k | 1.1k | - |
| web-fact-search | ok | 100% | 8/8 | 90 | 22.4 s | - | 1 | 3 | - | 0.7k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:62879", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157."}) | 100% | 9/9 | 90 | 57.4 s | - | 1 | 15 | - | 1.5k | 0.2k | - |
| web-plan-ranking | ok | 100% | 9/9 | 77 | 1 min 41 s | - | 1 | 11 | - | 4.7k | 0.2k | - |
| web-word-universe | ok | 100% | 9/9 | 77 | 2 min 20 s | - | 1 | 13 | - | 7.3k | 0.3k | - |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 3); looked at it in a browser (call 4)
- `py-async-cancel`: wrote run.py (call 2); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 3); used the chart of accounts (call 3); used the cash balance (call 3); not seen: recorded the result
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 5)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 3); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 7)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 1); made the feed photo (call 7); filled the permit (call 7)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 3)
- `cu-social-cycle`: made the image (call 3); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 3); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; recorded the result (call 3); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 4); replied (call 11)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 9); wrote the dossier (call 9); opened a source (call 6)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 11); wrote the page (call 7); looked at it in a browser (call 7); recorded the result (call 11)
