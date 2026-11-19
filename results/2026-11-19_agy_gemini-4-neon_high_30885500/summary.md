# mengine-bench 2.8.0: agy 1.5.12 / gemini-4-neon (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **56.4** | 70.8 | 7/29 | 59.9 | 0.0 | 63 min 45 s | >= ~$4.58 | 1.28M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: personal_instructions=~/.gemini/GEMINI.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-19, started 2026-11-19T10:56:15Z; bench at 2cb7694dcf77; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | timeout (timeout) | 0% | 1/5 | 3 | 5 min 00 s | - | 3 | 4 | 2.3 | 1.0k | 0.6k | - |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 2 | 1 min 00 s | - | 1 | 1 | 2.0 | 0.1k | 0.1k | - |
| ds-ab-playtest | timeout (timeout) | 100% | 5/5 | 70 | 3 min 00 s | - | 11 | 12 | 1.9 | 13.3k | 4.1k | - |
| bo-pnl-runway | timeout (timeout) | 100% | 6/6 | 71 | 2 min 30 s | - | 6 | 9 | 1.5 | 10.2k | 3.7k | - |
| bo-reconcile | ok | 100% | 5/5 | 93 | 47.2 s | - | 5 | 6 | 0.5 | 3.6k | 1.3k | - |
| cmp-handoff | ok | 100% | 12/12 | 94 | 1 min 52 s | - | 9 | 9 | 1.8 | 8.7k | 5.3k | - |
| cfg-source-drift | timeout (timeout) | 100% | 5/5 | 83 | 1 min 00 s | - | 6 | 14 | 1.0 | 2.3k | 0.7k | - |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 11 | 1 min 00 s | - | 3 | 5 | 1.8 | 3.5k | 2.7k | - |
| ds-sql-funnel | ok | 100% | 5/5 | 90 | 1 min 29 s | - | 7 | 7 | 1.7 | 6.5k | 1.7k | - |
| ue-packaged-bug | timeout (timeout) | 100% | 6/6 | 90 | 1 min 30 s | - | 5 | 14 | 1.2 | 6.9k | 5.7k | - |
| git-merge-conflict | timeout (timeout) | 100% | 7/7 | 89 | 1 min 30 s | - | 8 | 10 | 1.9 | 4.7k | 2.9k | - |
| infra-gpu-fit | timeout (timeout) | 100% | 7/7 | 66 | 1 min 00 s | - | 4 | 7 | 1.6 | 5.0k | 2.9k | - |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 16 | 1 min 00 s | - | 6 | 8 | 1.7 | 2.6k | 1.0k | - |
| gd-integration-repo | timeout (timeout) | 0% | 2/10 | 14 | 2 min 30 s | - | 9 | 22 | 1.8 | 6.2k | 4.5k | - |
| media-voice | ok | 100% | 4/4 | 78 | 43.2 s | - | 5 | 5 | 1.9 | 2.4k | 0.8k | - |
| file-media-edit | timeout (timeout) | 100% | 10/10 | 78 | 1 min 30 s | - | 3 | 6 | 2.8 | 7.0k | 4.9k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 5 | 1 min 00 s | - | 2 | 2 | 0.9 | 5.0k | 4.8k | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (33240)) | 100% | 9/9 | 93 | 2 min 50 s | - | 11 | 12 | 1.7 | 13.7k | 8.5k | - |
| sec-leak-fix | timeout (timeout) | 100% | 10/10 | 52 | 1 min 30 s | - | 4 | 7 | 1.0 | 8.9k | 6.3k | - |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 92 | 2 min 47 s | - | 10 | 15 | 1.5 | 15.3k | 5.5k | - |
| ds-sqlite-recover | timeout (timeout) | 100% | 6/6 | 83 | 1 min 00 s | - | 3 | 3 | 1.9 | 4.6k | 1.8k | - |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 17 | 1 min 30 s | - | 6 | 10 | 1.8 | 5.7k | 1.1k | - |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 79 | 1 min 00 s | - | 4 | 8 | 1.1 | 3.8k | 2.7k | - |
| web-mondrian-landing | timeout (timeout) | 100% | 11/11 | 78 | 5 min 00 s | - | 8 | 19 | 2.4 | 28.0k | 7.8k | - |
| 3d-print-homage | timeout (timeout, blue-layout similarity to the print: 0.396 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 55 | 7 min 00 s | - | 5 | 9 | 1.7 | 26.9k | 7.3k | - |
| web-fact-search | ok | 86% | 7/8 | 93 | 55.8 s | - | 5 | 7 | 3.9 | 3.4k | 1.6k | - |
| cu-webmail | ok (write routes (observation only): {"user-agent": "Python-urllib/3.13"}) | 100% | 9/9 | 90 | 2 min 19 s | - | 9 | 10 | 2.2 | 8.8k | 5.1k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 16 | 3 min 30 s | - | 8 | 15 | 5.3 | 9.5k | 3.2k | - |
| web-word-universe | timeout (timeout) | 67% | 5/7 | 36 | 6 min 00 s | - | 13 | 13 | 2.1 | 23.8k | 9.2k | - |

## Failed checks

- `web-archery-game` index.html exists with content
- `web-archery-game` takes the mouse: press and release
- `web-archery-game` makes its own sound
- `web-archery-game` needs nothing beside the page: expected [], received []
- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden config override and persistence: FAIL: test_config_override_and_persistence (test_hidden_gold.Hidden.test_config_override_and_persistence) | AssertionError: 0 != 1690
- `gd-integration-repo` hidden env float wins over file: FAIL: test_env_float_wins_over_file (test_hidden_gold.Hidden.test_env_float_wins_over_file) | AssertionError: 0 != 1050
- `gd-integration-repo` hidden round trip keeps everything: FAIL: test_round_trip_keeps_everything (test_hidden_gold.Hidden.test_round_trip_keeps_everything) | AssertionError: Tuples differ: (7, 0, ['a', 'b']) != (7, 640, ['a', 'b'])
- `gd-integration-repo` hidden half up tie rounds up: FAIL: test_half_up_tie_rounds_up (test_hidden_gold.Hidden.test_half_up_tie_rounds_up) | AssertionError: 0 != 1430
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 0 != 1500
- `gd-integration-repo` hidden persisted name survives: FAIL: test_persisted_name_survives (test_hidden_gold.Hidden.test_persisted_name_survives) | AssertionError: Tuples differ: ('Player One', 0) != ('Player One', 960)
- `gd-integration-repo` hidden real environment when env is none: FAIL: test_real_environment_when_env_is_none (test_hidden_gold.Hidden.test_real_environment_when_env_is_none) | AssertionError: 50 != 80
- `gd-integration-repo` existing test suite passes
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `hw-stutter-tuning` average FPS: expected 137.3, received None
- `hw-stutter-tuning` 1% low FPS: expected 45.4, received None
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received None
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received []
- `hw-stutter-tuning` GPU link speed kept: expected 'changes that leave the link speed alone', received []
- `hw-stutter-tuning` BIOS overclock kept: expected 'no XMP, PBO or core ratio change', received []
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date']
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

- `web-archery-game`: not seen: wrote the game; looked at it in a browser (call 1)
- `py-async-cancel`: not seen: wrote run.py; ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 5); tested significance (call 12); recorded the result (call 10)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); not seen: recorded the result
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 6)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 8)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 2); not seen: extracted the text; not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 8); committed (call 9)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 6)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 4); ran the integration test (call 2); ran the whole suite (call 20)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 3)
- `file-media-edit`: read the details (call 1); made the feed photo (call 6); not seen: filled the permit
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 5)
- `sec-leak-fix`: read the service (call 4); read the config (call 3); not seen: ran the tests
- `cu-social-cycle`: made the image (call 10); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 6); looked at it in a browser (call 5)
- `3d-print-homage`: wrote the scene (call 7); looked at it in a browser (call 3); recorded the result (call 6)
- `web-fact-search`: not seen: searched the web; recorded the result (call 6); opened a source (call 5)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 6); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); searched the web (call 13); not seen: recorded the result; not seen: wrote the dossier; opened a source (call 3)
- `web-word-universe`: walked the site (call 1); not seen: wrote words.json; not seen: wrote the page; looked at it in a browser (call 10); not seen: recorded the result
