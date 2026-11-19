# mengine-bench 2.8.0: codex codex-cli 0.167.0 / gpt-6.2-astra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **84.9** | 95.5 | 24/29 | 83.5 | 55.3 | 23 min 24 s | ~$15.09 | 5.19M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T13:55:10Z; bench at 0b7d01bbdec2; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 82 | 2 min 41 s | - | 1 | 10 | - | 5.4k | 0.4k | - |
| py-async-cancel | ok | 100% | 6/6 | 92 | 27.5 s | - | 1 | 4 | - | 0.9k | 0.1k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 93 | 29.0 s | - | 1 | 4 | - | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 80 | 34.6 s | - | 1 | 4 | - | 1.7k | 0.0k | - |
| bo-reconcile | ok | 100% | 5/5 | 83 | 28.8 s | - | 1 | 5 | - | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 92 | 39.4 s | - | 2 | 4 | - | 1.0k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 26.8 s | - | 1 | 4 | - | 0.7k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 76 | 22.5 s | - | 1 | 3 | - | 0.8k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 94 | 25.2 s | - | 1 | 4 | - | 0.9k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 85 | 32.5 s | - | 1 | 5 | - | 0.9k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 81 | 27.3 s | - | 1 | 4 | - | 0.8k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 81 | 24.2 s | - | 1 | 5 | - | 0.7k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 91 | 26.1 s | - | 1 | 4 | - | 0.7k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 97 | 45.2 s | - | 1 | 10 | - | 1.3k | 0.0k | - |
| media-voice | ok | 100% | 4/4 | 92 | 21.4 s | - | 1 | 3 | - | 0.6k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 87 | 39.1 s | - | 1 | 5 | - | 1.3k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 92 | 22.1 s | - | 1 | 2 | - | 0.9k | 0.0k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (30736)) | 100% | 9/9 | 92 | 49.8 s | - | 1 | 7 | - | 1.7k | 0.1k | - |
| sec-leak-fix | ok | 100% | 10/10 | 92 | 34.9 s | - | 1 | 6 | - | 1.1k | 0.1k | - |
| cu-social-cycle | ok | 44% | 6/11 | 28 | 33.6 s | - | 1 | 6 | - | 1.0k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 91 | 19.9 s | - | 1 | 3 | - | 0.6k | 0.0k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 94 | 28.4 s | - | 1 | 4 | - | 0.8k | 0.0k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 90 | 32.2 s | - | 1 | 7 | - | 0.9k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 86 | 1 min 07 s | - | 1 | 6 | - | 3.3k | 0.0k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.636 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 80% | 10/12 | 65 | 3 min 12 s | - | 1 | 13 | - | 7.0k | 0.6k | - |
| web-fact-search | ok | 86% | 7/8 | 46 | 19.7 s | - | 1 | 2 | - | 0.5k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Microsoft Windows 10.0.26200; pt-BR) PowerShell/7.7.0"}) | 100% | 9/9 | 93 | 1 min 02 s | - | 1 | 13 | - | 1.6k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 63 | 1 min 20 s | - | 1 | 9 | - | 2.5k | 0.0k | - |
| web-word-universe | ok | 100% | 9/9 | 88 | 2 min 33 s | - | 1 | 10 | - | 8.1k | 0.3k | - |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['f935989608f2539b472843752bfd0126fab5fca9d6f94e7e1aee3146464f1c43'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `3d-print-homage` imports three.js 0.170.0 from the CDN
- `3d-print-homage` creates a WebGLRenderer
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2826, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 2); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 2); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 3); used the chart of accounts (call 3); used the cash balance (call 3); recorded the result (call 4)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 4)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 4)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 2); recorded the result (call 4)
- `git-merge-conflict`: merged the branch (call 2); not seen: ran the tests; committed (call 4)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 3); ran the whole suite (call 10)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 4); filled the permit (call 4)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 2); not seen: ran the tests
- `sec-leak-fix`: read the service (call 3); read the config (call 3); ran the tests (call 4)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); deleted the test post (call 6)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 2); read the sensor log (call 2); read the settings (call 2); read the owner notes (call 2); recorded the result (call 4)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 4)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 6); looked at it in a browser (call 2); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 2); not seen: opened a source
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 8); replied (call 8)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 6); wrote the dossier (call 6); not seen: opened a source
- `web-word-universe`: walked the site (call 3); wrote words.json (call 6); wrote the page (call 7); looked at it in a browser (call 4); recorded the result (call 6)
