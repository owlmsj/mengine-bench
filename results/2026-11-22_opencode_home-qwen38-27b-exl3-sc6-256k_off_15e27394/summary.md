# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (off)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **70.0** | 80.5 | 16/29 | 63.3 | 63.1 | 21 min 04 s | $0.00 (local) | 5.95M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=SGLang lmsysorg/sglang:latest; quant=super-adapter merge, mixed NVFP4 (MLP NVFP4, attention + DeltaNet FP8); cache=fp8_e4m3; drafter=DFlash2 incoai (base-trained), 8 drafts; layout=TP 2x RTX 5090, chunked prefill 4096, mem-fraction-static 0.80; sampling=temperature 0.6, top_k 20, top_p 0.95 (server preferred params); study=SGLang with thinking really off, run 2 (2026-11-22): tier admission fix installed; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T17:11:57Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 68 | 2 min 39 s | 0.0000 | 31 | 30 | 0.7 | 12.2k | 0.0k | 32 s |
| py-async-cancel | ok | 80% | 5/6 | 64 | 22.6 s | 0.0000 | 8 | 7 | 0.9 | 2.5k | 0.0k | 2 s |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 34.9 s | 0.0000 | 6 | 6 | 0.2 | 2.0k | 0.0k | 26 s |
| bo-pnl-runway | ok | 100% | 6/6 | 87 | 18.6 s | 0.0000 | 7 | 8 | 0.3 | 2.3k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 14.5 s | 0.0000 | 5 | 6 | 0.2 | 1.4k | 0.0k | - |
| cmp-handoff | ok | 91% | 11/12 | 47 | 20.4 s | 0.0000 | 7 | 5 | 0.2 | 2.1k | 0.0k | 6 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 12.6 s | 0.0000 | 8 | 11 | 0.3 | 1.5k | 0.0k | 5 s |
| doc-lab-pdf | ok | 83% | 6/7 | 55 | 16.9 s | 0.0000 | 7 | 6 | 0.6 | 2.0k | 0.0k | 8 s |
| ds-sql-funnel | ok | 25% | 2/5 | 29 | 18.6 s | 0.0000 | 10 | 10 | 0.6 | 2.3k | 0.0k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 72 | 21.6 s | 0.0000 | 7 | 14 | 0.5 | 2.6k | 0.0k | 12 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 17.2 s | 0.0000 | 9 | 8 | 0.8 | 1.5k | 0.0k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 76 | 12.4 s | 0.0000 | 5 | 6 | 0.5 | 1.7k | 0.0k | 4 s |
| ir-server-logs | ok | 100% | 7/7 | 89 | 29.3 s | 0.0000 | 7 | 7 | 0.6 | 1.6k | 0.0k | 21 s |
| gd-integration-repo | ok | 88% | 9/10 | 76 | 19.6 s | 0.0000 | 12 | 27 | 0.4 | 2.7k | 0.0k | 11 s |
| media-voice | ok | 100% | 4/4 | 71 | 14.9 s | 0.0000 | 7 | 6 | 1.1 | 1.3k | 0.0k | - |
| file-media-edit | ok | 50% | 6/10 | 47 | 1 min 25 s | 0.0000 | 27 | 27 | 1.6 | 6.4k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 75% | 4/5 | 36 | 1 min 00 s | 0.0000 | 28 | 28 | 0.7 | 8.9k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (28836)) | 67% | 7/9 | 36 | 18.8 s | 0.0000 | 8 | 9 | 0.6 | 1.5k | 0.0k | 8 s |
| sec-leak-fix | ok | 75% | 8/10 | 70 | 15.4 s | 0.0000 | 7 | 9 | 0.6 | 1.8k | 0.0k | 4 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 77 | 37.5 s | 0.0000 | 30 | 30 | 0.1 | 2.9k | 0.0k | 4 s |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 4 | 1 min 00 s | 0.0000 | 6 | 5 | 1.7 | 7.9k | 0.0k | 33 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 70 | 1 min 03 s | 0.0000 | 14 | 14 | 1.3 | 4.5k | 0.0k | 45 s |
| ts-plugin-bug | ok | 100% | 8/8 | 100 | 23.3 s | 0.0000 | 9 | 12 | 0.5 | 2.4k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 69 | 1 min 07 s | 0.0000 | 19 | 18 | 1.0 | 8.6k | 0.0k | 20 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.35 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 56 | 58.4 s | 0.0000 | 11 | 11 | 1.3 | 6.2k | 0.0k | 21 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 10 | 1 min 00 s | 0.0000 | 14 | 16 | 1.3 | 1.4k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:53609", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 84 | 1 min 55 s | 0.0000 | 28 | 27 | 0.3 | 4.4k | 0.0k | 32 s |
| web-plan-ranking | ok | 50% | 5/9 | 43 | 1 min 20 s | 0.0000 | 12 | 13 | 0.8 | 5.5k | 0.0k | 55 s |
| web-word-universe | ok | 50% | 5/9 | 37 | 1 min 27 s | 0.0000 | 29 | 29 | 0.4 | 9.7k | 0.0k | 10 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` summary exists and fits in 1000 characters: 1840 characters
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 4.98}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2024-13-02', '2023-02-30', '2023-06-31', '2023-02-29', '2023-09-30', '2023-10-31']
- `rs-lock-bug` hidden opposite transfers do not hang: expected 'opposite_transfers_do_not_hang passed', received False
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
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
- `web-plan-ranking` launch dates: expected {'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor II': ['1991-01-31']}, received {'Bresser': '1987-01-28', 'Verao': '1989-08-15', 'Collor II': '1991-03-15'}
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41]}, received {'Cruzado': 10, 'Bresser': 30, 'Verao': 7, 'Collor I': 12, 'Collor II': 35}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3370, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 62 (aflição, almoço, amanhã, angústia, avó), extra 63 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 1 (sílaba), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 251, 'relations': 755, 'most_connected': {'word': 'tempo', 'degree': 28}}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 4); read the invoices (call 2); read the statement (call 3); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 2); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 6); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 6); committed (call 6)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 4); ran the integration test (call 11); ran the whole suite (call 27)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 3)
- `file-media-edit`: read the details (call 2); made the feed photo (call 7); filled the permit (call 8)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 9)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 2); read the config (call 4); ran the tests (call 8)
- `cu-social-cycle`: made the image (call 1); opened the site (call 5); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 3); read the owner notes (call 2); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 2); recorded the result (call 9)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 4)
- `cu-webmail`: opened the mail app (call 1); downloaded the invoice (call 2); replied (call 21)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 12); wrote the dossier (call 11); not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 8); wrote the page (call 15); looked at it in a browser (call 17); recorded the result (call 8)
