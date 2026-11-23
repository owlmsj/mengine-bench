# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **73.2** | 81.8 | 17/29 | 66.7 | 73.1 | 18 min 04 s | $0.00 (local) | 4.45M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; sampling=temperature 0.6 (forced), top_k 20, top_p 0.95; study=serve A run 2 at 2900 MHz (mengine#1090 roadmap item 1, 2026-11-23); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-23, started 2026-11-23T12:51:09Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 77 | 1 min 10 s | 0.0000 | 10 | 9 | 0.5 | 6.8k | 0.0k | 33 s |
| py-async-cancel | ok | 80% | 5/6 | 72 | 22.8 s | 0.0000 | 7 | 6 | 0.4 | 2.3k | 0.0k | 6 s |
| ds-ab-playtest | ok | 100% | 5/5 | 85 | 43.7 s | 0.0000 | 6 | 6 | 0.0 | 1.9k | 0.0k | 33 s |
| bo-pnl-runway | ok | 100% | 6/6 | 81 | 20.2 s | 0.0000 | 6 | 8 | 0.0 | 2.2k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 84 | 15.4 s | 0.0000 | 6 | 7 | 0.0 | 1.5k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 12/12 | 72 | 44.4 s | 0.0000 | 22 | 20 | 0.0 | 4.8k | 0.0k | 8 s |
| cfg-source-drift | ok | 100% | 5/5 | 94 | 20.5 s | 0.0000 | 11 | 14 | 0.0 | 2.1k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 76 | 18.6 s | 0.0000 | 9 | 8 | 0.2 | 1.9k | 0.0k | 8 s |
| ds-sql-funnel | ok | 25% | 2/5 | 35 | 32.2 s | 0.0000 | 14 | 14 | 0.0 | 3.7k | 0.0k | 3 s |
| ue-packaged-bug | ok | 100% | 6/6 | 86 | 17.1 s | 0.0000 | 6 | 11 | 0.0 | 1.8k | 0.0k | 6 s |
| git-merge-conflict | ok | 100% | 7/7 | 96 | 18.5 s | 0.0000 | 9 | 8 | 0.4 | 1.3k | 0.0k | 9 s |
| infra-gpu-fit | ok | 100% | 7/7 | 89 | 13.2 s | 0.0000 | 5 | 6 | 0.0 | 1.4k | 0.0k | 5 s |
| ir-server-logs | ok | 100% | 7/7 | 90 | 17.6 s | 0.0000 | 8 | 7 | 0.0 | 1.7k | 0.0k | 8 s |
| gd-integration-repo | ok | 88% | 9/10 | 62 | 35.4 s | 0.0000 | 7 | 18 | 0.0 | 3.8k | 0.0k | 26 s |
| media-voice | timeout (timeout, evidence 'announcement.wav' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 0% | 1/4 | 8 | 1 min 00 s | 0.0000 | 20 | 19 | 0.4 | 6.7k | 0.0k | 12 s |
| file-media-edit | ok | 50% | 6/10 | 40 | 37.8 s | 0.0000 | 14 | 14 | 0.4 | 4.0k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 25% | 2/5 | 28 | 1 min 00 s | 0.0000 | 5 | 4 | 0.0 | 2.0k | 0.0k | 2 s |
| rs-lock-bug | ok | 83% | 8/9 | 38 | 22.3 s | 0.0000 | 8 | 12 | 0.0 | 2.2k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 78 | 14.7 s | 0.0000 | 7 | 10 | 0.0 | 1.5k | 0.0k | 6 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 86 | 33.4 s | 0.0000 | 26 | 25 | 0.0 | 2.2k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 16 | 1 min 00 s | 0.0000 | 17 | 16 | 0.3 | 6.6k | 0.0k | 14 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 81 | 23.3 s | 0.0000 | 8 | 9 | 0.3 | 2.2k | 0.0k | 10 s |
| ts-plugin-bug | ok | 100% | 8/8 | 89 | 16.1 s | 0.0000 | 7 | 10 | 0.0 | 1.4k | 0.0k | 5 s |
| web-mondrian-landing | ok | 100% | 11/11 | 78 | 29.9 s | 0.0000 | 7 | 6 | 0.2 | 3.8k | 0.0k | 15 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.23 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 90% | 11/12 | 37 | 1 min 06 s | 0.0000 | 15 | 14 | 0.0 | 8.1k | 0.0k | 25 s |
| web-fact-search | ok | 100% | 8/8 | 80 | 53.8 s | 0.0000 | 10 | 14 | 0.4 | 1.8k | 0.0k | 35 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:57846", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 84 | 44.7 s | 0.0000 | 24 | 23 | 0.0 | 4.2k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 53 | 1 min 08 s | 0.0000 | 9 | 8 | 0.0 | 4.0k | 0.0k | 46 s |
| web-word-universe | ok | 50% | 5/9 | 38 | 1 min 45 s | 0.0000 | 34 | 33 | 0.3 | 12.1k | 0.0k | 8 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'tutorial_complete', 'steamdeck': 'tutorial_complete'}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `media-voice` announcement.wav is a valid WAV: expected 'a RIFF/WAVE file with audio', received 'no file'
- `media-voice` lasts 4 to 8 s: expected (4.0, 8.0), received 0.0
- `media-voice` whisper tiny hears the sentence: expected 'WER <= 0.2', received "'' (WER 1.00)"
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received '����������������'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received '����������'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received '���������������'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received '��������'
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2025-08-14', '2019-05-31']
- `txt-regex-log` lines without a valid address match nothing: expected ['2024-09-09', '2025-01-23'], received []
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2023-10-31']
- `rs-lock-bug` hidden awards from many threads all count: expected 'awards_from_many_threads_all_count passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `3d-print-homage` counted the boats in the print: expected 3, received {'count': 9, 'note': 'The print shows nine fishing boats (funaya): three clustered in the claw of the great wave on the left, three in the troughs on the right, and three in the foreground. Each is a low-poly hull with a row of crew figures, matching the print.'}
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2821, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 68 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acento: missing 0 (none), extra 1 (silaba)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 517, 'most_connected': {'word': 'tempo', 'degree': 13}}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 2)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 20)
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 7)
- `ue-packaged-bug`: read the crash log (call 5); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 4); ran the tests (call 7); committed (call 8)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 3); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 5)
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 5); ran the whole suite (call 18)
- `media-voice`: used a speech engine (call 3); not seen: wrote the audio
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 7)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 3)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 5); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; recorded the result (call 14); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 18)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 7); wrote the dossier (call 6); not seen: opened a source
- `web-word-universe`: walked the site (call 2); wrote words.json (call 4); wrote the page (call 6); looked at it in a browser (call 7); recorded the result (call 4)
