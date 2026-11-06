# mengine-bench 2.6.1: claude 2.1.319 (Claude Code) / claude-opus-5-5 (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **81.2** | 99.2 | 26/28 | 83.4 | 43.4 | 19 min 09 s | >= $7.25 (harness) | 5.03M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T18:37:29Z; bench at ac936902aacf; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 94 | 27.3 s | 0.2069 | 2 | 1 | 1.5 | 2.7k | 0.5k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 88 | 20.4 s | 0.1988 | 3 | 2 | 0.4 | 2.0k | 0.2k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 80 | 36.6 s | 0.2875 | 6 | 5 | 0.2 | 3.6k | 0.4k | - |
| bo-reconcile | ok | 100% | 5/5 | 87 | 17.4 s | 0.1973 | 3 | 2 | 0.4 | 1.6k | 0.1k | - |
| cmp-handoff | ok | 100% | 12/12 | 84 | 35.4 s | 0.4250 | 11 | 9 | 0.1 | 3.1k | 0.2k | - |
| cfg-source-drift | ok | 100% | 5/5 | 98 | 14.7 s | 0.1930 | 4 | 3 | 0.3 | 1.2k | 0.1k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 69 | 19.5 s | 0.1908 | 3 | 2 | 0.4 | 2.0k | 0.3k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 86 | 20.9 s | 0.1973 | 4 | 3 | 0.2 | 1.9k | 0.1k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 22.4 s | 0.2180 | 4 | 3 | 0.2 | 2.3k | 0.1k | - |
| git-merge-conflict | ok | 100% | 7/7 | 97 | 21.3 s | 0.2104 | 5 | 4 | 0.5 | 1.8k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 78 | 15.8 s | 0.1783 | 3 | 2 | 0.4 | 1.5k | 0.3k | - |
| ir-server-logs | ok | 100% | 7/7 | 79 | 24.3 s | 0.2908 | 5 | 4 | 0.2 | 1.9k | 0.4k | - |
| gd-integration-repo | ok | 100% | 10/10 | 88 | 43.2 s | 0.3139 | 9 | 8 | 0.4 | 4.1k | 0.4k | - |
| media-voice | ok | 100% | 4/4 | 85 | 12.5 s | 0.1542 | 2 | 1 | 0.7 | 1.1k | 0.1k | - |
| file-media-edit | ok | 100% | 10/10 | 88 | 30.4 s | 0.2339 | 5 | 4 | 0.9 | 2.8k | 0.4k | - |
| txt-regex-log | ok | 100% | 5/5 | 93 | 26.5 s | 0.1937 | 2 | 1 | 0.7 | 2.4k | 1.1k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (15988)) | 100% | 9/9 | 92 | 39.0 s | 0.2639 | 5 | 4 | 0.5 | 4.0k | 0.7k | - |
| sec-leak-fix | ok | 100% | 10/10 | 94 | 28.2 s | 0.2172 | 4 | 3 | 0.6 | 2.5k | 0.2k | - |
| cu-social-cycle | timeout (timeout, route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 89% | 10/11 | 76 | 3 min 00 s | - | 19 | 34 | 3.6 | 0.7k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 85 | 23.3 s | 0.2076 | 4 | 3 | 0.3 | 2.1k | 0.2k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 87 | 29.6 s | 0.2790 | 6 | 5 | 0.2 | 2.7k | 0.4k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 93 | 24.0 s | 0.2181 | 4 | 3 | 0.7 | 2.2k | 0.3k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 81 | 1 min 46 s | 0.5459 | 7 | 6 | 0.1 | 13.2k | 0.8k | - |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.588 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 81 | 2 min 36 s | 0.6351 | 8 | 7 | 0.2 | 15.0k | 5.0k | - |
| web-fact-search | ok | 100% | 8/8 | 92 | 16.4 s | 0.1825 | 3 | 5 | 2.3 | 1.5k | 0.2k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 100% | 9/9 | 89 | 38.8 s | 0.3232 | 9 | 8 | 0.3 | 3.0k | 0.4k | - |
| web-plan-ranking | ok | 100% | 9/9 | 44 | 53.7 s | 0.3066 | 6 | 6 | 1.7 | 4.8k | 1.3k | - |
| web-word-universe | ok | 88% | 8/9 | 36 | 1 min 05 s | 0.3801 | 8 | 7 | 0.3 | 6.8k | 0.4k | - |

## Failed checks

- `cu-social-cycle` closed the tabs and apps it opened: 1 tab(s) still open
- `web-word-universe` page runs without script errors: Uncaught SyntaxError: Identifier 'top' has already been declared

## Left open

- `cu-social-cycle`: 1 tab(s) open

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 9)
- `cfg-source-drift`: not seen: read the readme; ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 3)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 3); committed (call 4)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 2); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 3); filled the permit (call 3)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 4)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 3)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); deleted the test post (call 31)
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 2)
- `hw-stutter-tuning`: read the frame capture (call 3); read the sensor log (call 3); read the settings (call 2); not seen: read the owner notes; recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 3); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); opened a source (call 3)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 5); replied (call 5)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 6); wrote the dossier (call 6); opened a source (call 3)
- `web-word-universe`: not seen: walked the site; wrote words.json (call 5); wrote the page (call 6); not seen: looked at it in a browser; recorded the result (call 5)
