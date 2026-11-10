# mengine-bench 2.8.0: claude 2.1.322 (Claude Code) / claude-fable-5-2 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **89.4** | 99.1 | 27/29 | 84.8 | 68.4 | 19 min 28 s | $14.99 | 4.78M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-10, started 2026-11-10T19:42:36Z; bench at 4e7bdaad7a6a (dirty tree); submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 82 | 1 min 49 s | 0.9637 | 3 | 3 | 2.0 | 11.6k | 0.9k | - |
| py-async-cancel | ok | 100% | 6/6 | 86 | 26.4 s | 0.3867 | 2 | 2 | 1.2 | 2.6k | 0.6k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 85 | 28.6 s | 0.4046 | 3 | 2 | 1.3 | 2.7k | 0.2k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 79 | 32.9 s | 0.4907 | 4 | 3 | 0.4 | 3.2k | 0.2k | - |
| bo-reconcile | ok | 100% | 5/5 | 86 | 21.2 s | 0.3850 | 3 | 2 | 1.0 | 1.8k | 0.3k | - |
| cmp-handoff | ok | 100% | 12/12 | 92 | 32.0 s | 0.7227 | 6 | 5 | 0.2 | 2.8k | 0.3k | - |
| cfg-source-drift | ok | 100% | 5/5 | 95 | 14.9 s | 0.3312 | 3 | 2 | 1.2 | 1.0k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 82 | 20.7 s | 0.3563 | 3 | 2 | 1.1 | 1.8k | 0.3k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 83 | 21.8 s | 0.3593 | 3 | 2 | 1.0 | 1.8k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 24.5 s | 0.4031 | 3 | 2 | 1.2 | 2.3k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 85 | 34.8 s | 0.4395 | 4 | 3 | 1.8 | 2.9k | 0.3k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 79 | 18.8 s | 0.3416 | 3 | 2 | 1.0 | 1.6k | 0.3k | - |
| ir-server-logs | ok | 100% | 7/7 | 74 | 20.7 s | 0.5388 | 4 | 3 | 0.4 | 1.6k | 0.2k | - |
| gd-integration-repo | ok | 100% | 10/10 | 87 | 29.0 s | 0.4637 | 5 | 4 | 0.6 | 2.4k | 0.2k | - |
| media-voice | ok | 100% | 4/4 | 83 | 10.6 s | 0.2851 | 2 | 1 | 1.3 | 0.8k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 94 | 24.7 s | 0.3667 | 3 | 2 | 1.4 | 2.0k | 0.4k | - |
| txt-regex-log | ok | 100% | 5/5 | 94 | 24.6 s | 0.3570 | 2 | 1 | 1.7 | 2.1k | 0.8k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (19812)) | 100% | 9/9 | 89 | 32.1 s | 0.4256 | 4 | 3 | 1.7 | 2.8k | 0.2k | - |
| sec-leak-fix | ok | 100% | 10/10 | 96 | 30.4 s | 0.4319 | 3 | 2 | 1.6 | 2.9k | 0.1k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 91 | 1 min 35 s | 1.0439 | 13 | 20 | 3.7 | 5.6k | 0.4k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 80 | 24.9 s | 0.3833 | 3 | 2 | 1.1 | 2.3k | 0.4k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 88 | 33.9 s | 0.4725 | 4 | 4 | 1.4 | 2.8k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 22.2 s | 0.3755 | 4 | 3 | 1.1 | 1.8k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 91 | 50.7 s | 0.5658 | 4 | 3 | 0.0 | 5.1k | 0.8k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.581 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 78 | 2 min 49 s | 1.1818 | 5 | 6 | 0.8 | 15.3k | 5.9k | - |
| web-fact-search | ok | 86% | 7/8 | 87 | 15.8 s | 0.3161 | 2 | 2 | 1.6 | 1.3k | 0.2k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 100% | 9/9 | 91 | 34.6 s | 0.6006 | 9 | 8 | 0.5 | 2.8k | 0.2k | - |
| web-plan-ranking | ok | 100% | 9/9 | 77 | 57.5 s | 0.5954 | 5 | 8 | 4.2 | 4.7k | 1.2k | - |
| web-word-universe | ok | 88% | 8/9 | 35 | 1 min 47 s | 1.0031 | 8 | 8 | 0.7 | 11.0k | 0.8k | - |

## Failed checks

- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-word-universe` page runs without script errors: Uncaught SyntaxError: Identifier 'top' has already been declared

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); not seen: looked at it in a browser
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 2); recorded the result (call 2)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 2); committed (call 2)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 4)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 2); filled the permit (call 2)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 2)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); deleted the test post (call 18)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 2)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 2); not seen: read the owner notes; recorded the result (call 4)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 2)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 4); recorded the result (call 3)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); not seen: opened a source
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 6); replied (call 8)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 2); recorded the result (call 8); wrote the dossier (call 8); opened a source (call 3)
- `web-word-universe`: walked the site (call 5); wrote words.json (call 5); wrote the page (call 5); not seen: looked at it in a browser; recorded the result (call 5)
