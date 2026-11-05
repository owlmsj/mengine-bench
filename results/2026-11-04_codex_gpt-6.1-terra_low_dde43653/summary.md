# mengine-bench 2.6.0: codex codex-cli 0.166.0 / gpt-6.1-terra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **88.4** | 99.1 | 27/28 | 83.7 | 72.5 | 11 min 53 s | $1.74 (price) | 4.72M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-04, started 2026-11-04T23:31:55Z; bench at 58ebdf80fa3f; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 89 | 17.5 s | 0.0420 | 1 | 3 | - | 1.3k | 0.1k | - |
| ds-ab-playtest | ok (stopped after its final event) | 100% | 5/5 | 84 | 22.3 s | 0.0599 | 1 | 5 | - | 2.1k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 21.3 s | 0.0783 | 1 | 4 | - | 2.0k | 0.0k | - |
| bo-reconcile | ok | 100% | 5/5 | 83 | 11.8 s | 0.0408 | 1 | 3 | - | 0.7k | 0.0k | - |
| cmp-handoff | ok (stopped after its final event) | 100% | 12/12 | 76 | 25.0 s | 0.0707 | 2 | 7 | - | 1.3k | 0.1k | - |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 21.2 s | 0.0376 | 1 | 6 | - | 1.0k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 75 | 18.2 s | 0.0362 | 1 | 4 | - | 0.9k | 0.1k | - |
| ds-sql-funnel | ok (stopped after its final event) | 100% | 5/5 | 93 | 18.8 s | 0.0315 | 1 | 4 | - | 1.3k | 0.0k | - |
| ue-packaged-bug | ok (stopped after its final event) | 100% | 6/6 | 80 | 19.0 s | 0.0779 | 1 | 4 | - | 1.2k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 21.1 s | 0.0341 | 1 | 5 | - | 1.2k | 0.0k | - |
| infra-gpu-fit | ok (stopped after its final event) | 100% | 7/7 | 83 | 11.5 s | 0.0199 | 1 | 2 | - | 0.7k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 86 | 19.2 s | 0.1079 | 1 | 5 | - | 0.9k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 91 | 30.8 s | 0.0531 | 1 | 8 | - | 1.8k | 0.1k | - |
| media-voice | ok (stopped after its final event) | 100% | 4/4 | 81 | 13.6 s | 0.0191 | 1 | 2 | - | 0.6k | 0.0k | - |
| file-media-edit | ok (stopped after its final event) | 100% | 10/10 | 64 | 47.6 s | 0.0812 | 1 | 10 | - | 2.3k | 0.1k | - |
| txt-regex-log | ok | 100% | 5/5 | 94 | 13.1 s | 0.0229 | 1 | 2 | - | 1.0k | 0.1k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (18152)) | 100% | 9/9 | 92 | 24.2 s | 0.0444 | 1 | 4 | - | 2.0k | 0.1k | - |
| sec-leak-fix | ok | 100% | 10/10 | 84 | 21.6 s | 0.0385 | 1 | 4 | - | 1.7k | 0.2k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 87 | 38.6 s | 0.1152 | 1 | 16 | - | 1.3k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 87 | 17.3 s | 0.0337 | 1 | 4 | - | 1.0k | 0.1k | - |
| hw-stutter-tuning | ok (stopped after its final event) | 100% | 7/7 | 85 | 18.2 s | 0.0361 | 1 | 5 | - | 1.1k | 0.0k | - |
| ts-plugin-bug | ok (stopped after its final event) | 100% | 8/8 | 89 | 18.6 s | 0.0404 | 1 | 4 | - | 1.3k | 0.0k | - |
| web-mondrian-landing | ok (stopped after its final event) | 100% | 11/11 | 85 | 32.0 s | 0.0940 | 1 | 7 | - | 2.7k | 0.1k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.526 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 77 | 49.8 s | 0.0930 | 1 | 6 | - | 3.9k | 0.1k | - |
| web-fact-search | ok | 100% | 8/8 | 94 | 17.2 s | 0.0476 | 1 | 3 | - | 0.7k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:56539", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156."}) | 100% | 9/9 | 92 | 43.8 s | 0.1216 | 1 | 11 | - | 1.2k | 0.1k | - |
| web-plan-ranking | ok | 75% | 7/9 | 53 | 33.7 s | 0.1054 | 1 | 6 | - | 2.6k | 0.1k | - |
| web-word-universe | ok | 100% | 9/9 | 77 | 1 min 05 s | 0.1606 | 1 | 15 | - | 6.7k | 0.4k | - |

## Failed checks

- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 4209, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 3); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 3)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 4)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 8)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 6)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 3)
- `cu-social-cycle`: made the image (call 2); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 3); wrote the page (call 4); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 3); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 5); replied (call 8)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 5); wrote the dossier (call 6); not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 5); wrote the page (call 9); looked at it in a browser (call 10); recorded the result (call 5)
