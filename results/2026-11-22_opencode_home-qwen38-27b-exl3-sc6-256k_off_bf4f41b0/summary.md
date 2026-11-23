# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (off)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **72.1** | 84.0 | 16/29 | 64.8 | 58.7 | 22 min 23 s | $0.00 (local) | 8.61M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=SGLang lmsysorg/sglang:latest; quant=super-adapter merge, mixed NVFP4 (MLP NVFP4, attention + DeltaNet FP8); cache=fp8_e4m3; drafter=DFlash2 incoai (base-trained), 8 drafts; layout=TP 2x RTX 5090, chunked prefill 4096, mem-fraction-static 0.80; sampling=temperature 0.6, top_k 20, top_p 0.95 (server preferred params); study=SGLang with thinking really off (2026-11-22): no reasoning_effort sent; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T15:36:34Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 72 | 1 min 30 s | 0.0000 | 25 | 24 | 0.6 | 9.7k | 0.0k | 24 s |
| py-async-cancel | ok | 80% | 5/6 | 63 | 21.5 s | 0.0000 | 7 | 6 | 1.1 | 2.2k | 0.0k | 2 s |
| ds-ab-playtest | ok | 100% | 5/5 | 89 | 36.3 s | 0.0000 | 7 | 7 | 0.5 | 1.9k | 0.0k | 25 s |
| bo-pnl-runway | ok | 100% | 6/6 | 72 | 21.0 s | 0.0000 | 7 | 9 | 0.5 | 2.2k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 88 | 24.9 s | 0.0000 | 13 | 15 | 0.6 | 2.6k | 0.0k | 9 s |
| cmp-handoff | ok | 100% | 12/12 | 82 | 27.5 s | 0.0000 | 14 | 12 | 0.5 | 3.4k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 92 | 12.9 s | 0.0000 | 7 | 8 | 0.5 | 1.2k | 0.0k | 5 s |
| doc-lab-pdf | ok | 83% | 6/7 | 62 | 15.6 s | 0.0000 | 7 | 6 | 0.8 | 1.7k | 0.0k | 8 s |
| ds-sql-funnel | ok | 25% | 2/5 | 37 | 25.9 s | 0.0000 | 12 | 12 | 0.9 | 3.5k | 0.0k | 5 s |
| ue-packaged-bug | ok | 100% | 6/6 | 76 | 18.2 s | 0.0000 | 6 | 11 | 0.7 | 2.1k | 0.0k | 9 s |
| git-merge-conflict | crash (crash) | 0% | 2/7 | 9 | 7.3 s | 0.0000 | 2 | 2 | 0.8 | 0.2k | 0.0k | - |
| infra-gpu-fit | ok | 100% | 7/7 | 79 | 12.4 s | 0.0000 | 4 | 5 | 0.5 | 1.7k | 0.0k | 6 s |
| ir-server-logs | ok | 100% | 7/7 | 84 | 27.2 s | 0.0000 | 10 | 10 | 0.6 | 1.7k | 0.0k | 15 s |
| gd-integration-repo | ok | 75% | 8/10 | 50 | 18.1 s | 0.0000 | 10 | 26 | 0.4 | 2.5k | 0.0k | 11 s |
| media-voice | ok | 100% | 4/4 | 73 | 52.0 s | 0.0000 | 19 | 18 | 0.9 | 3.7k | 0.0k | 5 s |
| file-media-edit | ok | 88% | 9/10 | 57 | 53.4 s | 0.0000 | 19 | 18 | 0.8 | 4.1k | 0.0k | - |
| txt-regex-log | ok | 75% | 4/5 | 43 | 23.2 s | 0.0000 | 9 | 8 | 0.6 | 3.1k | 0.0k | 5 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (25512)) | 100% | 9/9 | 80 | 1 min 05 s | 0.0000 | 30 | 31 | 0.8 | 7.2k | 0.0k | 4 s |
| sec-leak-fix | ok | 88% | 9/10 | 73 | 19.7 s | 0.0000 | 8 | 11 | 0.3 | 2.0k | 0.0k | 6 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 86 | 38.0 s | 0.0000 | 27 | 26 | 0.1 | 2.4k | 0.0k | 1 s |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 19 | 1 min 00 s | 0.0000 | 6 | 6 | 1.1 | 8.5k | 0.0k | 9 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 82 | 29.2 s | 0.0000 | 10 | 13 | 0.6 | 3.1k | 0.0k | 21 s |
| ts-plugin-bug | ok | 100% | 8/8 | 98 | 20.9 s | 0.0000 | 13 | 14 | 0.3 | 2.4k | 0.0k | 7 s |
| web-mondrian-landing | ok | 100% | 11/11 | 64 | 31.6 s | 0.0000 | 8 | 7 | 0.5 | 4.0k | 0.0k | 12 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.357 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 80% | 10/12 | 47 | 1 min 23 s | 0.0000 | 15 | 14 | 1.3 | 10.4k | 0.0k | 23 s |
| web-fact-search | timeout (timeout) | 71% | 6/8 | 28 | 1 min 00 s | 0.0000 | 6 | 7 | 0.4 | 0.8k | 0.0k | 1 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:55058", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 84 | 1 min 23 s | 0.0000 | 29 | 28 | 0.6 | 3.8k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 36 | 2 min 43 s | 0.0000 | 21 | 22 | 0.6 | 5.8k | 0.0k | 130 s |
| web-word-universe | ok | 75% | 7/9 | 53 | 3 min 21 s | 0.0000 | 64 | 71 | 1.0 | 22.2k | 0.0k | 19 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 5.3}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `git-merge-conflict` main is a merge commit of the old main and the branch: expected "a merge in main's ancestry with parents ['1fd1a0574f6f43fdb28ac67cbaf7f8aa7e874fb8', 'b24e86bca76d6922a26109b3561fc797f6a5b718']", received []
- `git-merge-conflict` no conflict markers in tracked files: expected [], received ['loot.py', 'loot.py', 'loot.py']
- `git-merge-conflict` hidden pity timer tests pass: SyntaxError: unterminated triple-quoted string literal (detected at line 37)
- `git-merge-conflict` hidden event multiplier tests pass: SyntaxError: unterminated triple-quoted string literal (detected at line 37)
- `git-merge-conflict` hidden test with both together passes: SyntaxError: unterminated triple-quoted string literal (detected at line 37)
- `gd-integration-repo` hidden half up tie rounds up: FAIL: test_half_up_tie_rounds_up (test_hidden_gold.Hidden.test_half_up_tie_rounds_up) | AssertionError: 1420 != 1430
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2024-13-02', '2024-00-11', '2024-05-32', '2024-08-00', '2023-02-30', '2023-06-31', '2023-02-29', '2023-09-30', '2023-10-31']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `3d-print-homage` counted the boats in the print: expected 3, received None
- `3d-print-homage` named the mountain: expected 'Mount Fuji', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received '2022-10-17'
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received 1619
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1]}, received {'Cruzado': [264.65, 453.65], 'Bresser': [236.01, 764.5], 'Verao': [764.5, 5789.54], 'Collor I': [1974.17, 2555.7], 'Collor II': [578
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received ['Real', 'Collor II', 'Bresser']
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'avó: missing 2 (avô, pai), extra 0 (none)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 630, 'most_connected': 'tempo'}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 4); read the statement (call 3); recorded the result (call 12)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 12)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 5)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 4); read the game mode (call 5); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 2); not seen: ran the tests; not seen: committed
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 9); ran the whole suite (call 26)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 9); filled the permit (call 10)
- `txt-regex-log`: wrote the regex (call 4); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 9)
- `sec-leak-fix`: read the service (call 2); read the config (call 4); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 2)
- `hw-stutter-tuning`: read the frame capture (call 8); read the sensor log (call 8); read the settings (call 2); read the owner notes (call 3); recorded the result (call 12)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 1); recorded the result (call 6)
- `web-fact-search`: not seen: searched the web; recorded the result (call 1); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 9); replied (call 20)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 19); wrote the dossier (call 18); opened a source (call 5)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 9); wrote the page (call 9); looked at it in a browser (call 40); recorded the result (call 9)
