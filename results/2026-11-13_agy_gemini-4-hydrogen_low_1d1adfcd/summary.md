# mengine-bench 2.8.0: agy 1.5.8 / gemini-4-hydrogen (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **85.3** | 96.8 | 26/29 | 78.2 | 65.7 | 20 min 17 s | n/a | 3.30M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Cost warning: no list price for gemini-4-hydrogen; add it to prices.py
- Config: personal_instructions=~/.gemini/GEMINI.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-13, started 2026-11-14T02:06:08Z; bench at 435581dfc7d7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 77 | 1 min 05 s | - | 4 | 3 | 1.8 | 12.6k | 1.3k | - |
| py-async-cancel | ok | 100% | 6/6 | 89 | 19.0 s | - | 3 | 2 | 1.8 | 2.2k | 1.0k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 82 | 30.1 s | - | 5 | 5 | 1.2 | 2.1k | 0.6k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 26.2 s | - | 5 | 6 | 1.0 | 3.0k | 0.6k | - |
| bo-reconcile | ok | 100% | 5/5 | 83 | 18.3 s | - | 4 | 5 | 0.3 | 1.8k | 0.3k | - |
| cmp-handoff | ok | 100% | 12/12 | 91 | 35.1 s | - | 8 | 7 | 1.6 | 3.0k | 1.3k | - |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 22.6 s | - | 5 | 7 | 1.4 | 1.5k | 0.3k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 64 | 21.4 s | - | 4 | 4 | 0.6 | 2.5k | 1.2k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 80 | 25.1 s | - | 5 | 5 | 1.9 | 2.0k | 0.3k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 78 | 21.9 s | - | 4 | 8 | 1.0 | 2.6k | 1.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 35.1 s | - | 7 | 6 | 2.1 | 2.1k | 0.9k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 62 | 25.0 s | - | 3 | 4 | 0.1 | 2.4k | 1.2k | - |
| ir-server-logs | ok | 100% | 7/7 | 86 | 26.0 s | - | 6 | 7 | 1.5 | 2.1k | 0.6k | - |
| gd-integration-repo | ok | 88% | 9/10 | 60 | 47.0 s | - | 9 | 14 | 1.7 | 2.4k | 0.9k | - |
| media-voice | ok | 100% | 4/4 | 86 | 10.0 s | - | 2 | 1 | 1.7 | 0.8k | 0.2k | - |
| file-media-edit | ok | 100% | 10/10 | 90 | 47.6 s | - | 6 | 9 | 2.6 | 4.3k | 1.4k | - |
| txt-regex-log | ok | 100% | 5/5 | 95 | 30.5 s | - | 5 | 4 | 1.7 | 4.0k | 1.9k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (21820)) | 100% | 9/9 | 91 | 35.2 s | - | 6 | 7 | 1.8 | 3.4k | 1.3k | - |
| sec-leak-fix | ok | 100% | 10/10 | 85 | 38.6 s | - | 7 | 12 | 1.8 | 2.5k | 0.9k | - |
| cu-social-cycle | ok | 44% | 6/11 | 25 | 2 min 01 s | - | 21 | 21 | 2.2 | 10.8k | 4.4k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 80 | 36.2 s | - | 6 | 7 | 1.6 | 3.2k | 0.9k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 77 | 31.3 s | - | 7 | 9 | 1.6 | 2.9k | 0.7k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 36.0 s | - | 6 | 11 | 1.7 | 2.9k | 0.8k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 76 | 38.9 s | - | 4 | 3 | 1.6 | 7.8k | 1.5k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.474 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 62 | 53.6 s | - | 5 | 4 | 1.3 | 8.7k | 1.4k | - |
| web-fact-search | ok | 100% | 8/8 | 79 | 24.9 s | - | 4 | 5 | 2.7 | 1.4k | 0.4k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "Python-urllib/3.13"}) | 100% | 9/9 | 85 | 1 min 55 s | - | 17 | 16 | 2.3 | 6.8k | 2.4k | - |
| web-plan-ranking | ok | 75% | 7/9 | 55 | 59.4 s | - | 7 | 9 | 2.5 | 8.3k | 1.2k | - |
| web-word-universe | ok | 100% | 9/9 | 72 | 2 min 01 s | - | 16 | 15 | 1.7 | 17.7k | 4.1k | - |

## Failed checks

- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['048ec2c626abbf70bf49e06c8c953cf550ffa10115e05bfbd657cffc465c37f9'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3132, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); not seen: tested significance; recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); not seen: recorded the result
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); not seen: recorded the result
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); not seen: recorded the result
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 4); recorded the result (call 8)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 6)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 1); not seen: ran the integration test; not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); not seen: filled the permit
- `txt-regex-log`: wrote the regex (call 3); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 2)
- `sec-leak-fix`: read the service (call 5); read the config (call 4); ran the tests (call 1)
- `cu-social-cycle`: made the image (call 2); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 8); read the settings (call 3); read the owner notes (call 2); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 3); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 5); opened a source (call 4)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 10); replied (call 7)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 5); recorded the result (call 8); wrote the dossier (call 9); not seen: opened a source
- `web-word-universe`: walked the site (call 4); not seen: wrote words.json; not seen: wrote the page; not seen: looked at it in a browser; not seen: recorded the result
