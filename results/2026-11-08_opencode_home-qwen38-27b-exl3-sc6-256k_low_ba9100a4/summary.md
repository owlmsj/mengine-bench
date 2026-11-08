# mengine-bench 2.8.0: opencode opencode v2.2.5 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **61.2** | 75.6 | 18/29 | 66.9 | 0.0 | 41 min 34 s | $0.00 (price) | 6.60M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp SC_6.00bpw_H6_V6; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; role=tier 2 reserve; disk=Linux SSD; tier=2; temperature=0.6; mengine=2.7.0 main ea94583c (#955 recipe, policy local protocol v5); host_load=Codex app session + idle Claude Code session on the laptop; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-08, started 2026-11-08T02:50:28Z; bench at 9e552ccee028 (dirty tree); submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 83 | 3 min 27 s | 0.0000 | 28 | 27 | 0.0 | 28.4k | 0.0k | 137 s |
| py-async-cancel | timeout (timeout) | 0% | 1/6 | 0 | 1 min 00 s | 0.0000 | 1 | 0 | - | - | - | - |
| ds-ab-playtest | ok | 100% | 5/5 | 89 | 1 min 03 s | 0.0000 | 6 | 6 | 0.0 | 5.0k | 0.0k | 46 s |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 31.9 s | 0.0000 | 6 | 8 | 0.0 | 4.4k | 0.0k | 12 s |
| bo-reconcile | ok | 100% | 5/5 | 82 | 36.0 s | 0.0000 | 5 | 6 | 0.0 | 6.0k | 0.0k | 27 s |
| cmp-handoff | ok | 100% | 12/12 | 84 | 1 min 13 s | 0.0000 | 18 | 18 | 0.0 | 10.1k | 0.0k | 18 s |
| cfg-source-drift | ok | 100% | 5/5 | 88 | 19.2 s | 0.0000 | 8 | 15 | 0.0 | 2.1k | 0.0k | 7 s |
| doc-lab-pdf | ok | 67% | 5/7 | 60 | 32.2 s | 0.0000 | 8 | 8 | 0.3 | 4.4k | 0.0k | 20 s |
| ds-sql-funnel | ok | 100% | 5/5 | 87 | 39.4 s | 0.0000 | 9 | 9 | 0.0 | 5.2k | 0.0k | 2 s |
| ue-packaged-bug | ok | 100% | 6/6 | 90 | 1 min 14 s | 0.0000 | 6 | 13 | 0.0 | 10.3k | 0.0k | 60 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 32.1 s | 0.0000 | 11 | 10 | 0.3 | 3.6k | 0.0k | 18 s |
| infra-gpu-fit | ok | 100% | 7/7 | 80 | 16.0 s | 0.0000 | 4 | 5 | 0.0 | 2.0k | 0.0k | 9 s |
| ir-server-logs | ok | 100% | 7/7 | 92 | 53.3 s | 0.0000 | 8 | 9 | 0.0 | 4.3k | 0.0k | 43 s |
| gd-integration-repo | ok | 88% | 9/10 | 71 | 1 min 19 s | 0.0000 | 15 | 31 | 0.0 | 11.8k | 0.0k | 57 s |
| media-voice | ok | 100% | 4/4 | 77 | 32.0 s | 0.0000 | 8 | 7 | 0.0 | 3.8k | 0.0k | 5 s |
| file-media-edit | timeout (timeout, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 38% | 5/10 | 48 | 1 min 30 s | 0.0000 | 14 | 16 | 0.4 | 8.8k | 0.0k | 50 s |
| txt-regex-log | timeout (timeout) | 0% | 1/5 | 3 | 1 min 00 s | 0.0000 | 2 | 1 | 0.0 | 0.1k | 0.0k | - |
| rs-lock-bug | timeout (timeout, left running, not attributed: vctip.exe (13856)) | 50% | 6/9 | 33 | 3 min 00 s | 0.0000 | 17 | 19 | 0.0 | 24.4k | 0.0k | 122 s |
| sec-leak-fix | ok | 88% | 9/10 | 82 | 1 min 07 s | 0.0000 | 8 | 13 | 0.0 | 9.6k | 0.0k | 43 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 93 | 54.1 s | 0.0000 | 36 | 37 | 0.0 | 5.7k | 0.0k | 6 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 19 | 1 min 00 s | 0.0000 | 9 | 8 | 0.1 | 5.9k | 0.0k | 5 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 85 | 1 min 24 s | 0.0000 | 13 | 14 | 0.0 | 11.7k | 0.0k | 17 s |
| ts-plugin-bug | ok | 100% | 8/8 | 97 | 43.6 s | 0.0000 | 11 | 15 | 0.0 | 5.5k | 0.0k | 15 s |
| web-mondrian-landing | ok | 100% | 11/11 | 76 | 3 min 13 s | 0.0000 | 10 | 10 | 0.1 | 31.0k | 0.0k | 169 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.359 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 63 | 2 min 41 s | 0.0000 | 12 | 13 | 0.1 | 21.4k | 0.0k | 111 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 11 | 1 min 00 s | 0.0000 | 6 | 13 | 0.3 | 4.4k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:56939", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/157.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 95 | 1 min 29 s | 0.0000 | 29 | 31 | 0.0 | 11.1k | 0.0k | 29 s |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 15 | 3 min 30 s | 0.0000 | 5 | 11 | 0.1 | 6.8k | 0.0k | - |
| web-word-universe | ok | 62% | 6/9 | 66 | 4 min 54 s | 0.0000 | 50 | 63 | 0.0 | 36.6k | 0.0k | 33 s |

## Failed checks

- `py-async-cancel` jobs run side by side up to the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` never more jobs at once than the limit: expected {'started': 2, 'finished': 2, 'cleaned': 2, 'peak': 1}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C below the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C at the limit cleans up every started job: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received "ModuleNotFoundError: No module named 'run'"
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 5.81}
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received ['Glicose em jejum', 'Colesterol LDL', 'Hemoglobina glicada (HbA1c)']
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'no out/permit-filled.pdf'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received 'no pattern in regex.txt'
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received 'no pattern in regex.txt'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received 'no pattern in regex.txt'
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received 'no pattern in regex.txt'
- `rs-lock-bug` hidden awards from many threads all count: expected 'awards_from_many_threads_all_count passed', received False
- `rs-lock-bug` hidden opposite transfers do not hang: expected 'opposite_transfers_do_not_hang passed', received False
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
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
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 5 (em-construção, link-antigo, pagina-removida, rascunho-3, xpto-2)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'arte: missing 0 (none), extra 1 (rascunho-3)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 750, 'most_connected': 'palavra'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 5)
- `py-async-cancel`: not seen: wrote run.py; not seen: ran it
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 3); used the cash balance (call 4); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); recorded the result (call 14)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 7)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 6); ran the tests (call 9); committed (call 8)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 4); ran the integration test (call 9); ran the whole suite (call 25)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 10); filled the permit (call 14)
- `txt-regex-log`: not seen: wrote the regex; not seen: tried it in Python
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 3); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 2); read the owner notes (call 3); recorded the result (call 13)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 11)
- `web-mondrian-landing`: read the fact sheet (call 2); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 3)
- `cu-webmail`: opened the mail app (call 4); downloaded the invoice (call 10); replied (call 17)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 6)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 9); wrote the page (call 32); looked at it in a browser (call 34); recorded the result (call 9)
