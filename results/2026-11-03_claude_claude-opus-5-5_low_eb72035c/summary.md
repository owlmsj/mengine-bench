# mengine-bench 2.5.2: claude 2.1.318 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **84.5** | 97.3 | 23/28 | 78.0 | 67.1 | 13 min 14 s | $6.65 (harness) | 5.23M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-03, started 2026-11-04T02:45:56Z; bench at 1009d24b0f4f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 89 | 25.3 s | 0.1826 | 2 | 1 | 1.4 | 1.8k | 0.3k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 83 | 19.0 s | 0.1787 | 3 | 2 | 0.6 | 1.3k | 0.1k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 72 | 37.3 s | 0.2375 | 5 | 4 | 0.2 | 2.3k | 0.1k | - |
| bo-reconcile | ok | 100% | 5/5 | 78 | 13.1 s | 0.1831 | 3 | 2 | 0.5 | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 84 | 35.2 s | 0.3813 | 9 | 7 | 0.2 | 2.4k | 0.0k | - |
| cfg-source-drift | ok | 100% | 5/5 | 90 | 11.2 s | 0.1666 | 3 | 2 | 0.6 | 0.9k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 69 | 14.6 s | 0.1712 | 3 | 2 | 0.6 | 1.3k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 80 | 15.8 s | 0.1758 | 3 | 2 | 0.6 | 1.5k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 91 | 20.9 s | 0.2066 | 4 | 3 | 0.3 | 1.9k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 88 | 21.0 s | 0.1817 | 4 | 3 | 0.5 | 1.2k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 76 | 12.4 s | 0.1658 | 3 | 2 | 0.5 | 1.0k | 0.2k | - |
| ir-server-logs | ok | 100% | 7/7 | 75 | 19.9 s | 0.2327 | 4 | 3 | 0.2 | 1.3k | 0.1k | - |
| gd-integration-repo | ok | 100% | 10/10 | 90 | 22.0 s | 0.2258 | 5 | 4 | 0.3 | 2.1k | 0.1k | - |
| media-voice | ok | 100% | 4/4 | 85 | 8.6 s | 0.1420 | 2 | 1 | 0.8 | 0.6k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 85 | 21.1 s | 0.1989 | 4 | 3 | 0.6 | 1.9k | 0.1k | - |
| txt-regex-log | ok | 100% | 5/5 | 90 | 17.6 s | 0.1709 | 2 | 1 | 0.9 | 1.5k | 0.5k | - |
| rs-lock-bug | ok | 100% | 9/9 | 79 | 25.1 s | 0.1863 | 4 | 3 | 0.8 | 1.5k | 0.1k | - |
| sec-leak-fix | ok | 100% | 10/10 | 89 | 19.1 s | 0.1857 | 3 | 2 | 0.8 | 1.6k | 0.1k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 89% | 10/11 | 58 | 2 min 08 s | 0.9413 | 22 | 32 | 2.4 | 5.6k | 0.2k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 82 | 19.9 s | 0.1752 | 3 | 2 | 0.6 | 1.4k | 0.1k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 87 | 25.0 s | 0.2215 | 6 | 5 | 0.3 | 1.5k | 0.1k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 91 | 18.1 s | 0.1908 | 4 | 3 | 0.5 | 1.5k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 89 | 34.7 s | 0.2199 | 3 | 2 | 0.5 | 3.1k | 0.0k | - |
| 3d-print-homage | ok | 91% | 12/13 | 55 | 54.1 s | 0.2721 | 3 | 2 | 0.5 | 4.7k | 0.3k | - |
| web-fact-search | ok | 86% | 7/8 | 36 | 9.0 s | 0.1478 | 2 | 1 | 0.9 | 0.7k | 0.1k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 83% | 8/9 | 83 | 42.7 s | 0.3562 | 13 | 12 | 0.3 | 2.9k | 0.2k | - |
| web-plan-ranking | ok | 75% | 7/9 | 33 | 33.9 s | 0.2222 | 3 | 2 | 0.5 | 3.1k | 0.8k | - |
| web-word-universe | ok | 100% | 9/9 | 76 | 1 min 10 s | 0.3332 | 7 | 6 | 0.3 | 5.4k | 0.5k | - |

## Failed checks

- `cu-social-cycle` test post carries cover.png: expected ['73ed1020ae69a1627303deb9e253a45b02ded18248096572886214c69bd88347'], received ['5ea3459b538aa533ec4bb69ed5e696603193bcc66aae67c5f0e56e8ed9689582']
- `3d-print-homage` render keeps the print's composition (blue layout): expected 'a blue-layout similarity to great-wave.jpg of at least 0.4 on a 4x3 grid', received 0.369
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `cu-webmail` closed the tabs and apps it opened: 0 tab(s) still open; still running: sleep.exe
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 1699, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}

## Left open

- `cu-webmail`: still running: sleep.exe (11868)

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); not seen: removed duplicate sessions; tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 3)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 5); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 3)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 4)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 2); filled the permit (call 2)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); deleted the test post (call 28)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 2)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); not seen: opened a source
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 4); replied (call 4)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 2); wrote the dossier (call 2); not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 2); wrote the page (call 2); not seen: looked at it in a browser; recorded the result (call 2)
