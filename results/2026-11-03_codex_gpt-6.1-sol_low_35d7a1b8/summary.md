# mengine-bench 2.5.1: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **73.8** | 96.6 | 25/28 | 82.0 | 20.6 | 24 min 50 s | n/a | 5.60M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-03, started 2026-11-04T01:53:21Z; bench at 6eb25b45a8e8; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 93 | 41.5 s | - | 1 | 8 | - | 1.9k | 0.1k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 88 | 41.6 s | - | 1 | 4 | - | 2.1k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 84 | 1 min 08 s | - | 1 | 5 | - | 3.4k | 0.1k | - |
| bo-reconcile | ok | 100% | 5/5 | 83 | 25.0 s | - | 1 | 4 | - | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 86 | 32.8 s | - | 2 | 5 | - | 1.0k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 87 | 29.7 s | - | 1 | 7 | - | 0.9k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 73 | 33.2 s | - | 1 | 6 | - | 1.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 90 | 32.0 s | - | 1 | 4 | - | 1.4k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 85 | 38.3 s | - | 1 | 6 | - | 1.7k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 85 | 1 min 00 s | - | 1 | 7 | - | 2.8k | 0.2k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 79 | 17.3 s | - | 1 | 2 | - | 0.8k | 0.0k | - |
| ir-server-logs | ok | 100% | 7/7 | 87 | 22.9 s | - | 1 | 4 | - | 0.9k | 0.0k | - |
| gd-integration-repo | ok | 100% | 10/10 | 90 | 53.7 s | - | 1 | 10 | - | 2.5k | 0.2k | - |
| media-voice | ok | 100% | 4/4 | 92 | 19.2 s | - | 1 | 3 | - | 0.6k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 63 | 45.9 s | - | 1 | 6 | - | 1.7k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 97 | 33.5 s | - | 1 | 3 | - | 1.6k | 0.2k | - |
| rs-lock-bug | ok | 100% | 9/9 | 94 | 51.1 s | - | 1 | 6 | - | 2.3k | 0.1k | - |
| sec-leak-fix | ok | 100% | 10/10 | 86 | 48.5 s | - | 1 | 5 | - | 2.3k | 0.3k | - |
| cu-social-cycle | ok | 44% | 6/11 | 37 | 47.6 s | - | 1 | 10 | - | 1.5k | 0.2k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 88 | 31.1 s | - | 1 | 3 | - | 1.4k | 0.1k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 89 | 34.0 s | - | 1 | 5 | - | 1.5k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 89 | 34.2 s | - | 1 | 5 | - | 1.5k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 87 | 1 min 15 s | - | 1 | 6 | - | 4.1k | 0.2k | - |
| 3d-print-homage | ok | 100% | 13/13 | 83 | 2 min 42 s | - | 1 | 10 | - | 7.5k | 1.0k | - |
| web-fact-search | ok | 86% | 7/8 | 56 | 33.5 s | - | 1 | 6 | - | 1.0k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:65039", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156."}) | 100% | 9/9 | 89 | 40.2 s | - | 1 | 11 | - | 1.3k | 0.1k | - |
| web-plan-ranking | ok | 75% | 7/9 | 61 | 1 min 53 s | - | 1 | 10 | - | 5.5k | 0.6k | - |
| web-word-universe | ok | 100% | 9/9 | 75 | 3 min 46 s | - | 1 | 21 | - | 10.1k | 1.2k | - |

## Failed checks

- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['9040be5399ae8a8ed92cd79507b28463be3b500e11007e72beec00090743f732'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['unicode_15_0_characters_added']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 5988, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Left open

- `rs-lock-bug`: still running: vctip.exe (15692)

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 3); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 3); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 2); used the chart of accounts (call 2); used the cash balance (call 2); recorded the result (call 4)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 4)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 3); recorded the result (call 4)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 3); recorded the result (call 5)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 3); ran the whole suite (call 10)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 2)
- `file-media-edit`: read the details (call 2); made the feed photo (call 4); filled the permit (call 4)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 3)
- `cu-social-cycle`: made the image (call 5); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); read the owner notes (call 2); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; recorded the result (call 4); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 5); replied (call 9)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 10); wrote the dossier (call 10); not seen: opened a source
- `web-word-universe`: walked the site (call 3); wrote words.json (call 6); wrote the page (call 7); looked at it in a browser (call 3); recorded the result (call 6)
