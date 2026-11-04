# mengine-bench 2.5.0: claude 2.1.318 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **79.6** | 92.7 | 22/28 | 77.2 | 60.2 | 14 min 57 s | $6.54 (harness) | 5.12M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-03, started 2026-11-04T00:18:45Z; bench at 529a84d7f0d9; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | ok | 100% | 6/6 | 90 | 25.8 s | 0.1791 | 2 | 1 | 1.2 | 1.7k | 0.2k | - |
| ds-ab-playtest | ok | 100% | 5/5 | 84 | 15.9 s | 0.1901 | 3 | 2 | 0.6 | 1.4k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 24.0 s | 0.2313 | 4 | 3 | 0.3 | 2.4k | 0.1k | - |
| bo-reconcile | ok | 100% | 5/5 | 82 | 17.0 s | 0.1822 | 3 | 2 | 0.5 | 1.1k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 91 | 37.0 s | 0.3729 | 7 | 5 | 0.3 | 2.4k | 0.1k | - |
| cfg-source-drift | ok | 100% | 5/5 | 98 | 13.6 s | 0.1770 | 4 | 3 | 0.5 | 1.0k | 0.0k | - |
| doc-lab-pdf | ok | 100% | 7/7 | 71 | 20.9 s | 0.1759 | 3 | 2 | 0.5 | 1.5k | 0.2k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 83 | 18.4 s | 0.1779 | 3 | 2 | 0.6 | 1.5k | 0.0k | - |
| ue-packaged-bug | ok | 100% | 6/6 | 88 | 21.6 s | 0.2110 | 4 | 3 | 0.3 | 2.1k | 0.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 88 | 17.8 s | 0.1883 | 4 | 3 | 0.6 | 1.5k | 0.1k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 67 | 17.2 s | 0.1701 | 3 | 2 | 0.5 | 1.2k | 0.2k | - |
| ir-server-logs | ok | 100% | 7/7 | 82 | 34.6 s | 0.2411 | 5 | 4 | 0.2 | 1.3k | 0.1k | - |
| gd-integration-repo | ok | 100% | 10/10 | 82 | 42.4 s | 0.2426 | 7 | 6 | 0.2 | 2.0k | 0.1k | - |
| media-voice | ok | 100% | 4/4 | 81 | 9.5 s | 0.1437 | 2 | 1 | 0.8 | 0.7k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 85 | 24.1 s | 0.2170 | 6 | 5 | 0.4 | 2.0k | 0.2k | - |
| txt-regex-log | ok | 100% | 5/5 | 92 | 19.8 s | 0.1726 | 2 | 1 | 0.8 | 1.7k | 0.6k | - |
| rs-lock-bug | ok | 100% | 9/9 | 88 | 32.6 s | 0.2208 | 5 | 4 | 0.8 | 2.4k | 0.0k | - |
| sec-leak-fix | ok | 100% | 10/10 | 86 | 20.9 s | 0.1936 | 3 | 2 | 0.8 | 1.9k | 0.1k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 89% | 10/11 | 63 | 1 min 52 s | 0.6339 | 20 | 25 | 2.2 | 5.2k | 0.2k | - |
| ds-sqlite-recover | ok | 0% | 5/6 | 75 | 51.4 s | 0.2438 | 6 | 5 | 0.3 | 2.9k | 0.8k | - |
| hw-stutter-tuning | ok | 100% | 7/7 | 77 | 39.0 s | 0.2314 | 6 | 5 | 0.3 | 1.8k | 0.2k | - |
| ts-plugin-bug | ok | 100% | 8/8 | 87 | 25.4 s | 0.1957 | 4 | 3 | 0.5 | 1.7k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 89 | 36.5 s | 0.2324 | 3 | 2 | 0.5 | 3.5k | 0.1k | - |
| 3d-print-homage | ok | 100% | 12/12 | 62 | 45.7 s | 0.2601 | 3 | 2 | 0.5 | 4.3k | 0.3k | - |
| web-fact-search | ok | 86% | 7/8 | 37 | 15.2 s | 0.1498 | 2 | 1 | 0.9 | 0.8k | 0.1k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "curl/8.21.0"}) | 83% | 8/9 | 91 | 56.7 s | 0.3177 | 12 | 11 | 0.3 | 2.7k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 32 | 36.1 s | 0.2212 | 3 | 2 | 0.6 | 3.1k | 0.7k | - |
| web-word-universe | ok | 62% | 6/9 | 35 | 1 min 06 s | 0.3676 | 10 | 9 | 0.5 | 5.8k | 0.5k | - |

## Failed checks

- `cu-social-cycle` test post carries cover.png: expected ['dbead9c23768cb69e439e80321f6690c8da4cd8ad8ce5dbefffcdcc4fa53a6b7'], received ['7d65601ea6a85fdc33e228f3eb27ff8d8b6b7b42e119b310e1bfdf3b6ad6122f']
- `ds-sqlite-recover` no writes outside the task workspace
- `web-fact-search` cited primary sources were fetched: expected "each cited URL's host and path in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `cu-webmail` closed the tabs and apps it opened: 0 tab(s) still open; still running: python.exe
- `web-plan-ranking` every plan has a source: expected 'a fetched http(s) URL in sources for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ fetched URLs, 3+ plans', received {'chars': 1699, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'contato: missing 0 (none), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': 'palavra'}

## Left open

- `cu-webmail`: still running: python.exe (20828)

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: not seen: read the notes; read the data (call 2); removed duplicate sessions (call 2); tested significance (call 2); recorded the result (call 2)
- `bo-pnl-runway`: not seen: read the notes; read the ledger (call 2); used the chart of accounts (call 2); not seen: used the cash balance; recorded the result (call 2)
- `bo-reconcile`: not seen: read the notes; read the invoices (call 2); read the statement (call 2); recorded the result (call 2)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 1); recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 1); excluded test accounts (call 2); recorded the result (call 2)
- `ue-packaged-bug`: not seen: read the crash log; read the game mode (call 3); recorded the result (call 3)
- `git-merge-conflict`: merged the branch (call 1); ran the tests (call 3); committed (call 3)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 1); recorded the result (call 2)
- `ir-server-logs`: not seen: read the notes; read the logs (call 1); recorded the result (call 4)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 5); ran the whole suite (call 5)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 1); made the feed photo (call 4); filled the permit (call 4)
- `txt-regex-log`: wrote the regex (call 1); tried it in Python (call 1)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 3)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 2)
- `cu-social-cycle`: made the image (call 1); opened the site (call 1); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 1); recorded the result (call 5)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); not seen: looked at it in a browser
- `3d-print-homage`: wrote the scene (call 2); not seen: looked at it in a browser; recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); not seen: opened a source
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 4); replied (call 4)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 2); wrote the dossier (call 2); not seen: opened a source
- `web-word-universe`: walked the site (call 5); wrote words.json (call 2); wrote the page (call 7); not seen: looked at it in a browser; recorded the result (call 2)
