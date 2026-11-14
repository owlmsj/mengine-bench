# mengine-bench 2.8.0: agy 1.5.5 / gemini-4-carbon (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **57.8** | 74.8 | 5/29 | 58.4 | 0.0 | 64 min 46 s | >= ~$1.86 | 0.64M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.gemini/GEMINI.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-10, started 2026-11-10T20:21:29Z; bench at eadb58f7001c; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 83% | 7/8 | 59 | 5 min 00 s | - | 5 | 8 | 1.9 | 23.2k | 0.0k | - |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 4 | 1 min 00 s | - | 2 | 2 | 2.1 | 3.1k | 2.9k | - |
| ds-ab-playtest | timeout (timeout) | 0% | 1/5 | 17 | 3 min 00 s | - | 8 | 9 | 1.8 | 8.1k | 1.2k | - |
| bo-pnl-runway | timeout (timeout) | 100% | 6/6 | 59 | 2 min 30 s | - | 8 | 11 | 1.9 | 4.2k | 0.0k | - |
| bo-reconcile | ok | 100% | 5/5 | 92 | 1 min 07 s | - | 6 | 7 | 1.1 | 2.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 12/12 | 88 | 2 min 12 s | - | 13 | 12 | 1.7 | 4.1k | 0.0k | - |
| cfg-source-drift | timeout (timeout) | 75% | 4/5 | 33 | 1 min 00 s | - | 4 | 9 | 1.2 | 0.6k | 0.0k | - |
| doc-lab-pdf | timeout (timeout) | 100% | 7/7 | 80 | 1 min 00 s | - | 4 | 5 | 1.5 | 0.6k | 0.0k | - |
| ds-sql-funnel | timeout (timeout) | 100% | 5/5 | 83 | 1 min 30 s | - | 7 | 8 | 1.8 | 3.0k | 0.0k | - |
| ue-packaged-bug | timeout (timeout) | 100% | 6/6 | 82 | 1 min 30 s | - | 5 | 11 | 1.6 | 4.0k | 3.0k | - |
| git-merge-conflict | ok | 100% | 7/7 | 100 | 1 min 15 s | - | 7 | 9 | 1.7 | 2.6k | 0.0k | - |
| infra-gpu-fit | timeout (timeout) | 100% | 7/7 | 68 | 1 min 00 s | - | 3 | 5 | 0.5 | 1.7k | 1.0k | - |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 12 | 1 min 00 s | - | 4 | 5 | 1.6 | 1.1k | 0.3k | - |
| gd-integration-repo | timeout (timeout) | 100% | 10/10 | 54 | 2 min 30 s | - | 8 | 29 | 1.8 | 3.3k | 0.0k | - |
| media-voice | ok | 100% | 4/4 | 85 | 49.2 s | - | 4 | 3 | 1.8 | 1.6k | 0.0k | - |
| file-media-edit | timeout (timeout) | 100% | 10/10 | 78 | 1 min 30 s | - | 5 | 10 | 1.9 | 2.7k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 100% | 5/5 | 88 | 1 min 00 s | - | 3 | 5 | 1.9 | 1.9k | 0.0k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (16456)) | 100% | 9/9 | 91 | 2 min 21 s | - | 9 | 20 | 1.7 | 7.1k | 0.0k | - |
| sec-leak-fix | timeout (timeout) | 100% | 10/10 | 57 | 1 min 30 s | - | 4 | 9 | 1.8 | 1.7k | 0.0k | - |
| cu-social-cycle | timeout (timeout) | 44% | 6/11 | 22 | 3 min 00 s | - | 8 | 19 | 1.8 | 3.1k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 100% | 6/6 | 71 | 1 min 00 s | - | 4 | 4 | 1.8 | 1.5k | 0.0k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 17 | 1 min 30 s | - | 7 | 10 | 1.4 | 2.6k | 0.0k | - |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 64 | 1 min 00 s | - | 5 | 10 | 1.8 | 1.6k | 0.0k | - |
| web-mondrian-landing | timeout (timeout) | 100% | 11/11 | 77 | 5 min 00 s | - | 13 | 23 | 2.1 | 14.5k | 0.0k | - |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.521 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 74 | 7 min 00 s | - | 9 | 14 | 2.1 | 21.1k | 0.0k | - |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 17 | 1 min 00 s | - | 3 | 6 | 4.8 | 0.8k | 0.0k | - |
| cu-webmail | timeout (timeout, write routes (observation only): {"user-agent": "Python-urllib/3.13"}) | 100% | 9/9 | 75 | 3 min 00 s | - | 10 | 14 | 2.4 | 2.7k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 16 | 3 min 30 s | - | 10 | 18 | 4.0 | 5.5k | 0.0k | - |
| web-word-universe | timeout (timeout) | 67% | 5/7 | 32 | 6 min 00 s | - | 12 | 17 | 1.9 | 18.6k | 7.9k | - |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [0, 0, 0, 0, 0, 0]
- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `ds-ab-playtest` deduplicated session counts: expected {'sessions_a': 900, 'sessions_b': 900}, received {'sessions_a': None, 'sessions_b': None}
- `ds-ab-playtest` completion rates: expected (0.38, 0.4666666666666667), received {'completion_rate_a': None, 'completion_rate_b': None}
- `ds-ab-playtest` the gain is significant: expected '0.000198469 +/- 0.00015 (pooled two-sided z-test or equivalent), or a containing upper bound <= 0.001', received None
- `ds-ab-playtest` ship decision: expected True, received None
- `cfg-source-drift` the delivered configs equal what the source generates: expected 'every out/ file as gen.py writes it', received "['out/codex.toml', 'out/claude.json'] differ from a fresh generation"
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `cu-social-cycle` test post published with the exact text: expected 'Testing the new Bluehaze uploader: Harbor Day is on.', received []
- `cu-social-cycle` test post carries cover.png: expected ['76e910b1b9350746f0f8932e3fc7c74e9bb1d31058b5264e140e2819c6f8ba22'], received []
- `cu-social-cycle` image has the given alt text: expected ['Poster with the title Harbor Day 2026.'], received []
- `cu-social-cycle` test post deleted: expected 'deleted', received 'never posted'
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [-1, None]
- `hw-stutter-tuning` average FPS: expected 137.3, received None
- `hw-stutter-tuning` 1% low FPS: expected 45.4, received None
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received None
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received []
- `hw-stutter-tuning` GPU link speed kept: expected 'changes that leave the link speed alone', received []
- `hw-stutter-tuning` BIOS overclock kept: expected 'no XMP, PBO or core ratio change', received []
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` the page has a search field: no input, contenteditable or searchbox in universe/index.html
- `web-word-universe` opening the page with ?word= shows that word's relations: no universe/index.html

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 6); looked at it in a browser (call 5)
- `py-async-cancel`: not seen: wrote run.py; ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); not seen: tested significance; not seen: recorded the result
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 9)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 5); recorded the result (call 11)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 8); committed (call 9)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 5); ran the integration test (call 7); not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 1); made the feed photo (call 8); filled the permit (call 9)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 3); read the config (call 4); not seen: ran the tests
- `cu-social-cycle`: made the image (call 14); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 4)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 9); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 11); looked at it in a browser (call 6); recorded the result (call 8)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 6)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 8); replied (call 11)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 6)
- `web-word-universe`: walked the site (call 4); not seen: wrote words.json; not seen: wrote the page; not seen: looked at it in a browser; not seen: recorded the result
