# mengine-bench 2.6.0: opencode opencode v2.2.5 / home/glm53-flash-exl3-sc310-512k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **48.2** | 70.0 | 10/21 | 52.7 | 0.0 | 35 min 48 s | $0.00 (price) | 2.30M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=GLM-5.3-Flash; runtime=exllamav3 0c325eff + TabbyAPI 8f92fac5; ctx=512k; drafter=MTP n5 dynamic; role=advisor; tier=2; temperature=1.0; quant=turboderp-sc_3.10bpw; cache=Q8, 100 experts on CPU; disk=Linux SSD; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-05, started 2026-11-05T18:07:24Z; bench at f343274bbb4f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 1 min 46 s | 0.0000 | 9 | 11 | 0.0 | 3.2k | 0.0k | 38 s |
| cfg-source-drift | ok | 100% | 5/5 | 86 | 39.9 s | 0.0000 | 6 | 6 | 0.0 | 0.7k | 0.0k | 14 s |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 5 | 1 min 00 s | 0.0000 | 6 | 6 | 0.0 | 0.2k | 0.0k | - |
| ds-sql-funnel | ok | 25% | 2/5 | 33 | 1 min 09 s | 0.0000 | 11 | 11 | 0.0 | 1.7k | 0.0k | 11 s |
| ue-packaged-bug | ok | 100% | 6/6 | 88 | 56.9 s | 0.0000 | 6 | 10 | 0.0 | 1.2k | 0.0k | 23 s |
| ir-server-logs | ok | 100% | 7/7 | 70 | 43.3 s | 0.0000 | 6 | 6 | 0.2 | 1.1k | 0.0k | 22 s |
| gd-integration-repo | ok | 88% | 9/10 | 61 | 1 min 11 s | 0.0000 | 6 | 6 | 0.3 | 1.3k | 0.0k | 49 s |
| media-voice | ok | 100% | 4/4 | 85 | 23.9 s | 0.0000 | 3 | 2 | 0.3 | 0.4k | 0.0k | - |
| file-media-edit | timeout (timeout) | 38% | 5/10 | 35 | 1 min 30 s | 0.0000 | 16 | 18 | 0.4 | 1.6k | 0.0k | 30 s |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 21 | 1 min 00 s | 0.0000 | 3 | 3 | 0.0 | 2.0k | 0.0k | 46 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (12884)) | 100% | 9/9 | 85 | 1 min 50 s | 0.0000 | 13 | 13 | 0.0 | 2.5k | 0.0k | 36 s |
| sec-leak-fix | ok | 100% | 10/10 | 87 | 53.0 s | 0.0000 | 10 | 12 | 0.0 | 1.0k | 0.0k | 15 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 78 | 2 min 21 s | 0.0000 | 36 | 36 | 0.0 | 1.9k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 12 | 1 min 00 s | 0.0000 | 6 | 5 | 0.3 | 1.7k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 64 | 1 min 54 s | 0.0000 | 8 | 7 | 0.4 | 3.3k | 0.0k | 58 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.289 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 51 | 4 min 05 s | 0.0000 | 11 | 11 | 0.3 | 9.6k | 0.0k | 11 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 10 | 1 min 00 s | 0.0000 | 2 | 3 | 1.0 | 0.1k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:52704", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 83% | 8/9 | 42 | 2 min 24 s | 0.0000 | 22 | 22 | 0.0 | 2.5k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 100% | 9/9 | 66 | 3 min 30 s | 0.0000 | 7 | 8 | 0.0 | 6.1k | 0.0k | 142 s |
| web-word-universe | ok | 62% | 6/9 | 51 | 5 min 30 s | 0.0000 | 41 | 41 | 0.3 | 8.6k | 0.0k | 52 s |

## Failed checks

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
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.7822}, 'steamdeck': {'step': 'purchase', 'conversion': 0.6207}}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2025-10-02', '2024-06-30', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31']
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `cu-webmail` invoice PDF saved byte for byte: expected 'a file with the sha256 of LP-2026-0418.pdf', received ['AGENTS.md', 'LP-2026-0418.pdf']
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 7 (coracoes, em-construcao, link-antigo, pagina-removida, paixoes)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'advogado: missing 0 (none), extra 1 (coracoes)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 257, 'relations': 762, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: not seen: wrote run.py; not seen: ran it
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 3); used the chart of accounts (call 4); used the cash balance (call 5); recorded the result (call 7)
- `cfg-source-drift`: not seen: read the readme; ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; not seen: recorded the result
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 9)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 2); ran the whole suite (call 6)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 9); filled the permit (call 15)
- `txt-regex-log`: wrote the regex (call 3); not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 11)
- `cu-social-cycle`: made the image (call 5); opened the site (call 1); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 1); wrote the JSON (call 5)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 9); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 7); wrote the dossier (call 7); opened a source (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 6); wrote the page (call 21); looked at it in a browser (call 24); recorded the result (call 21)
