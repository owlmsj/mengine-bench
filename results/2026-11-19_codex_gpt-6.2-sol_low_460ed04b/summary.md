# mengine-bench 2.8.0: codex codex-cli 0.167.0 / gpt-6.2-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **84.8** | 96.6 | 26/29 | 86.1 | 43.6 | 26 min 56 s | ~$5.08 | 6.37M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T13:13:28Z; bench at 0b7d01bbdec2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 87 | 3 min 23 s | - | 1 | 7 | - | 10.2k | 0.4k | - |
| py-async-cancel | ok | 100% | 6/6 | 95 | 25.8 s | - | 1 | 5 | - | 1.2k | 0.1k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 27.7 s | - | 1 | 4 | - | 1.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 94 | 1 min 02 s | - | 1 | 7 | - | 3.4k | 0.2k | - |
| bo-reconcile | ok | 100% | 5/5 | 91 | 31.4 s | - | 1 | 6 | - | 1.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 88 | 38.1 s | - | 2 | 7 | - | 1.5k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 15.6 s | - | 1 | 3 | - | 0.6k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 85 | 28.7 s | - | 1 | 5 | - | 1.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 92 | 22.7 s | - | 1 | 3 | - | 1.0k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 88 | 25.2 s | - | 1 | 5 | - | 1.0k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 86 | 28.8 s | - | 1 | 6 | - | 1.3k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 73 | 21.6 s | - | 1 | 4 | - | 1.0k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 92 | 21.1 s | - | 1 | 4 | - | 0.8k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 86 | 50.0 s | - | 1 | 15 | - | 2.3k | 0.4k | - |
| media-voice | ok | 100% | 4/4 | 88 | 36.1 s | - | 1 | 5 | - | 1.4k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 88 | 44.0 s | - | 1 | 7 | - | 1.9k | 0.1k | - |
| txt-regex-log | ok | 100% | 5/5 | 95 | 22.7 s | - | 1 | 2 | - | 1.1k | 0.2k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (27904)) | 100% | 9/9 | 86 | 1 min 05 s | - | 1 | 10 | - | 3.0k | 0.9k | - |
| sec-leak-fix | ok | 100% | 10/10 | 89 | 49.8 s | - | 1 | 8 | - | 2.5k | 0.4k | - |
| cu-social-cycle | ok | 44% | 6/11 | 25 | 1 min 26 s | - | 1 | 11 | - | 4.6k | 0.6k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 89 | 18.4 s | - | 1 | 3 | - | 0.8k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 92 | 33.4 s | - | 1 | 7 | - | 1.2k | 0.0k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 27.2 s | - | 1 | 6 | - | 1.1k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 89 | 1 min 38 s | - | 1 | 8 | - | 5.4k | 0.6k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.729 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 87 | 3 min 34 s | - | 1 | 10 | - | 12.3k | 1.4k | - |
| web-fact-search | ok | 100% | 8/8 | 86 | 17.6 s | - | 1 | 2 | - | 0.8k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:53120", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157."}) | 100% | 9/9 | 94 | 37.1 s | - | 1 | 12 | - | 1.1k | 0.1k | - |
| web-plan-ranking | ok | 75% | 7/9 | 67 | 1 min 08 s | - | 1 | 10 | - | 3.3k | 0.2k | - |
| web-word-universe | ok | 100% | 9/9 | 90 | 3 min 18 s | - | 1 | 13 | - | 11.6k | 0.4k | - |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['a459b3c6a35b5fd1974f9fc31221c29a324da9b09cb6374a1b40eaf7c547f76c'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 4673, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 2); looked at it in a browser (call 1)
- `py-async-cancel`: wrote run.py (call 3); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 3); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 4)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 4); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 3)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 4)
- `git-merge-conflict`: merged the branch (call 2); not seen: ran the tests; committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 3)
- `ir-server-logs`: read the notes (call 2); read the logs (call 2); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 4); filled the permit (call 4)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 5)
- `sec-leak-fix`: read the service (call 3); read the config (call 3); ran the tests (call 6)
- `cu-social-cycle`: made the image (call 5); opened the site (call 7); deleted the test post (call 4)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 2); read the owner notes (call 2); recorded the result (call 6)
- `ts-plugin-bug`: read the bus (call 2); not seen: ran the tests
- `web-mondrian-landing`: read the fact sheet (call 2); wrote the page (call 3); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 2); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 2); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 5); replied (call 8)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 7); wrote the dossier (call 7); not seen: opened a source
- `web-word-universe`: walked the site (call 3); wrote words.json (call 6); wrote the page (call 7); looked at it in a browser (call 3); recorded the result (call 6)
