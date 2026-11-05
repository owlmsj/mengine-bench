# mengine-bench 2.6.0: opencode opencode v2.2.5 / home/glm53-flash-exl3-sc260-512k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **46.8** | 66.9 | 9/21 | 53.4 | 0.0 | 34 min 38 s | $0.00 (price) | 1.96M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=GLM-5.3-Flash; runtime=exllamav3 0c325eff + TabbyAPI 8f92fac5; ctx=512k; drafter=MTP n5 dynamic; role=advisor; tier=2; temperature=1.0; quant=turboderp-sc_2.60bpw; cache=Q8, 60 experts on CPU; disk=USB SSD 20 Gbps; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-05, started 2026-11-05T17:29:52Z; bench at f343274bbb4f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 55 | 1 min 00 s | 0.0000 | 5 | 5 | 0.0 | 2.2k | 0.0k | 20 s |
| bo-pnl-runway | ok | 100% | 6/6 | 71 | 1 min 19 s | 0.0000 | 9 | 8 | 0.3 | 2.8k | 0.0k | 55 s |
| cfg-source-drift | ok | 100% | 5/5 | 93 | 40.6 s | 0.0000 | 8 | 10 | 0.0 | 0.9k | 0.0k | 20 s |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 8 | 1 min 00 s | 0.0000 | 6 | 6 | 0.2 | 0.2k | 0.0k | - |
| ds-sql-funnel | ok | 25% | 2/5 | 31 | 48.9 s | 0.0000 | 9 | 9 | 0.3 | 1.3k | 0.0k | 9 s |
| ue-packaged-bug | ok | 100% | 6/6 | 92 | 59.0 s | 0.0000 | 7 | 11 | 0.0 | 2.0k | 0.0k | 34 s |
| ir-server-logs | ok | 100% | 7/7 | 84 | 40.4 s | 0.0000 | 6 | 6 | 0.3 | 0.9k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 70 | 1 min 02 s | 0.0000 | 9 | 15 | 0.0 | 1.3k | 0.0k | 42 s |
| media-voice | ok | 100% | 4/4 | 82 | 21.4 s | 0.0000 | 3 | 2 | 0.5 | 0.5k | 0.0k | - |
| file-media-edit | timeout (timeout) | 50% | 6/10 | 22 | 1 min 30 s | 0.0000 | 15 | 16 | 0.5 | 2.2k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (3516)) | 83% | 8/9 | 46 | 1 min 03 s | 0.0000 | 13 | 13 | 0.0 | 1.5k | 0.0k | 13 s |
| sec-leak-fix | ok | 100% | 10/10 | 90 | 53.4 s | 0.0000 | 8 | 10 | 0.0 | 1.2k | 0.0k | 22 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 77 | 1 min 36 s | 0.0000 | 31 | 31 | 0.0 | 1.4k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 21 | 1 min 00 s | 0.0000 | 4 | 3 | 0.3 | 1.2k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 79 | 2 min 31 s | 0.0000 | 20 | 20 | 0.0 | 4.7k | 0.0k | 47 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.367 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 80% | 10/12 | 49 | 4 min 30 s | 0.0000 | 19 | 20 | 0.0 | 10.8k | 0.0k | 50 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 12 | 1 min 00 s | 0.0000 | 3 | 4 | 0.9 | 0.1k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:55333", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 81 | 2 min 13 s | 0.0000 | 29 | 29 | 0.0 | 3.4k | 0.0k | 66 s |
| web-plan-ranking | timeout (timeout) | 50% | 5/9 | 36 | 3 min 30 s | 0.0000 | 13 | 13 | 0.0 | 7.2k | 0.0k | 124 s |
| web-word-universe | timeout (timeout) | 50% | 5/9 | 23 | 6 min 00 s | 0.0000 | 42 | 42 | 0.3 | 14.0k | 0.0k | 70 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `rs-lock-bug` hidden opposite transfers do not hang: expected 'opposite_transfers_do_not_hang passed', received False
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received "[{'item': None, 'price': 'trail map'}, {'item': None, 'price': 'matchbox'}, {'item': None, 'price': 'tent stake'}, {'ite"
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `3d-print-homage` counted the boats in the print: expected 3, received None
- `3d-print-homage` named the mountain: expected 'Mount Fuji', received None
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Collor II': [1620.97, 1119.1]}, received {'Cruzado': [242.23, 79.66], 'Collor II': [1620.97, 472.7]}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received ['Real', 'Collor II', 'Collor I']
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3807, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (coracoes, paixoes, saudades)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'advogado: missing 0 (none), extra 1 (coracoes)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 757, 'most_connected': {'word': 'palavra', 'degree': 16}}
- `web-word-universe` page runs without script errors: Uncaught TypeError: Cannot read properties of undefined (reading 'add')

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 3); used the chart of accounts (call 3); used the cash balance (call 3); recorded the result (call 7)
- `cfg-source-drift`: read the readme (call 7); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 10)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); not seen: ran the integration test; not seen: ran the whole suite
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 6); filled the permit (call 8)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 7)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 2)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 1)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 18)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 6); wrote the dossier (call 6); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 31); looked at it in a browser (call 38); recorded the result (call 5)
