# mengine-bench 2.3.1: claude 2.1.317 (Claude Code) / claude-sonnet-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **85.1** | 98.7 | 25/28 | 79.1 | 56.7 | 15 min 49 s | $3.19 (harness) | 5.39M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-03, started 2026-11-03T13:41:30Z; bench at 84df6a867512; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 5/5 | 91 | 21.8 s | 0.0888 | 2 | 1 | 2.0k | 0.4k | - |
| ds-ab-playtest | ok | 100% | 4/4 | 78 | 33.0 s | 0.1046 | 6 | 5 | 2.8k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 5/5 | 79 | 27.8 s | 0.0910 | 4 | 3 | 1.7k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 77 | 15.9 s | 0.0955 | 5 | 4 | 1.7k | 0.1k | - |
| cmp-handoff | ok | 100% | 11/11 | 72 | 34.3 s | 0.1744 | 8 | 7 | 2.9k | 0.2k | - |
| cfg-source-drift | ok | 100% | 3/3 | 96 | 15.8 s | 0.0791 | 4 | 3 | 1.0k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 6/6 | 72 | 18.3 s | 0.0732 | 3 | 2 | 1.3k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 70 | 21.8 s | 0.0789 | 4 | 3 | 1.5k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 5/5 | 83 | 21.8 s | 0.0916 | 4 | 3 | 1.9k | 0.1k | - |
| git-merge-conflict | ok | 100% | 6/6 | 98 | 24.9 s | 0.0854 | 5 | 4 | 1.4k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 6/6 | 67 | 14.7 s | 0.0700 | 3 | 2 | 1.0k | 0.2k | - |
| ir-server-logs | ok | 100% | 6/6 | 70 | 18.5 s | 0.1045 | 4 | 3 | 1.3k | 0.2k | - |
| gd-integration-repo | ok | 100% | 8/8 | 89 | 26.6 s | 0.1023 | 5 | 4 | 1.9k | 0.2k | - |
| media-voice | ok | 100% | 3/3 | 86 | 11.2 s | 0.0592 | 2 | 1 | 0.7k | 0.1k | - |
| file-media-edit | ok | 100% | 9/9 | 84 | 24.7 s | 0.0993 | 6 | 6 | 2.2k | 0.2k | - |
| txt-regex-log | ok | 100% | 4/4 | 73 | 26.0 s | 0.0815 | 3 | 2 | 2.0k | 0.8k | - |
| rs-lock-bug | ok | 100% | 6/6 | 89 | 45.9 s | 0.1027 | 5 | 4 | 2.7k | 0.2k | - |
| sec-leak-fix | ok | 100% | 8/8 | 91 | 31.4 s | 0.0905 | 4 | 3 | 1.9k | 0.1k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 88% | 8/9 | 66 | 1 min 49 s | 0.3151 | 14 | 30 | 5.3k | 0.5k | - |
| ds-sqlite-recover | ok | 100% | 5/5 | 78 | 27.4 s | 0.0856 | 4 | 3 | 1.9k | 0.2k | - |
| hw-stutter-tuning | ok | 100% | 6/6 | 86 | 39.7 s | 0.1164 | 6 | 5 | 2.3k | 0.3k | - |
| ts-plugin-bug | ok | 100% | 7/7 | 92 | 20.1 s | 0.0943 | 5 | 4 | 1.9k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 10/10 | 90 | 34.8 s | 0.1095 | 3 | 2 | 3.9k | 0.3k | - |
| 3d-print-homage | ok | 100% | 11/11 | 50 | 50.4 s | 0.1489 | 4 | 3 | 6.2k | 0.7k | - |
| web-fact-search | ok | 100% | 6/6 | 85 | 25.2 s | 0.0828 | 4 | 5 | 1.0k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:57987", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156."}) | 100% | 7/7 | 81 | 1 min 30 s | 0.2647 | 14 | 21 | 4.0k | 0.3k | - |
| web-plan-ranking | ok | 88% | 7/8 | 60 | 37.6 s | 0.1331 | 5 | 6 | 3.3k | 1.0k | - |
| web-word-universe | ok | 88% | 7/8 | 63 | 1 min 21 s | 0.1701 | 8 | 7 | 6.2k | 0.6k | - |

## Failed checks

- `cu-social-cycle` test post carries cover.png: expected ['4c66702b49b283e7c455efb92fd000d7c7fdeadf0785c0c2e9397eba8ca36efd'], received ['332f11c631efd15f860bcc5ba71513b785345912083c1fcbcaa367e334e644c7']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ URLs, 3+ plans', received {'chars': 1490, 'urls': 1, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país shows mãe, which has no link with it

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 4)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 3); not seen: used the cash balance; recorded the result (call 3)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 3)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 2); committed (call 4)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 3); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 5); filled the permit (call 6)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 3)
- `cu-social-cycle`: made the image (call 3); opened the site (call 1); deleted the test post (call 27)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; opened a source (call 1); recorded the result (call 5)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 5); replied (call 18)
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 2); opened a source (call 2); recorded the result (call 6); wrote the dossier (call 6)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 5); wrote the page (call 6); not seen: looked at it in a browser; recorded the result (call 5)
