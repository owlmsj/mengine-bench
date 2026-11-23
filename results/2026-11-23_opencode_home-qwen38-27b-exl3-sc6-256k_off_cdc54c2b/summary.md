# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (off)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **71.4** | 82.4 | 15/29 | 64.7 | 61.4 | 21 min 35 s | $0.00 (local) | 5.17M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic, chunk 2048, batch 2; layout=native TP 2x RTX 5090; sampling=temperature 0.64 (forced), top_k 20, top_p 0.95, min_p 0 (client sends none); study=final fair A vs B, order ABBA (mengine#1090, 2026-11-23): A run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-23, started 2026-11-23T16:57:51Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 83% | 7/8 | 39 | 1 min 22 s | 0.0000 | 24 | 23 | 0.1 | 8.8k | 0.0k | 32 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 39 | 1 min 00 s | 0.0000 | 17 | 16 | 0.0 | 6.9k | 0.0k | 4 s |
| ds-ab-playtest | ok | 100% | 5/5 | 91 | 47.6 s | 0.0000 | 8 | 9 | 0.0 | 2.4k | 0.0k | 33 s |
| bo-pnl-runway | ok | 100% | 6/6 | 78 | 27.2 s | 0.0000 | 12 | 14 | 0.0 | 2.7k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 82 | 20.7 s | 0.0000 | 10 | 11 | 0.0 | 1.9k | 0.0k | 6 s |
| cmp-handoff | ok | 91% | 11/12 | 51 | 20.8 s | 0.0000 | 6 | 5 | 0.0 | 1.9k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 84 | 11.4 s | 0.0000 | 5 | 7 | 0.1 | 0.8k | 0.0k | 4 s |
| doc-lab-pdf | ok | 100% | 7/7 | 65 | 23.9 s | 0.0000 | 10 | 9 | 0.4 | 2.6k | 0.0k | 6 s |
| ds-sql-funnel | ok | 50% | 3/5 | 44 | 18.6 s | 0.0000 | 8 | 8 | 0.2 | 1.9k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 85 | 16.6 s | 0.0000 | 7 | 11 | 0.0 | 1.7k | 0.0k | 5 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 18.4 s | 0.0000 | 9 | 8 | 0.5 | 1.3k | 0.0k | 8 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 13.7 s | 0.0000 | 5 | 6 | 0.0 | 1.4k | 0.0k | 5 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 5 | 1 min 00 s | 0.0000 | 2 | 5 | 0.1 | 0.3k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 65 | 25.1 s | 0.0000 | 11 | 26 | 0.0 | 2.6k | 0.0k | 14 s |
| media-voice | ok | 100% | 4/4 | 86 | 19.3 s | 0.0000 | 7 | 6 | 0.7 | 1.4k | 0.0k | 8 s |
| file-media-edit | ok | 38% | 5/10 | 56 | 32.7 s | 0.0000 | 13 | 12 | 0.5 | 2.9k | 0.0k | - |
| txt-regex-log | ok | 100% | 5/5 | 87 | 54.4 s | 0.0000 | 11 | 10 | 0.0 | 7.5k | 0.0k | 14 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (11612)) | 67% | 7/9 | 34 | 14.7 s | 0.0000 | 7 | 9 | 0.0 | 1.2k | 0.0k | 5 s |
| sec-leak-fix | ok | 75% | 8/10 | 71 | 17.4 s | 0.0000 | 9 | 10 | 0.0 | 1.8k | 0.0k | 5 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 83 | 33.4 s | 0.0000 | 24 | 23 | 0.0 | 2.3k | 0.0k | - |
| ds-sqlite-recover | ok | 100% | 6/6 | 75 | 36.9 s | 0.0000 | 12 | 11 | 0.4 | 4.1k | 0.0k | 19 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 90 | 27.6 s | 0.0000 | 9 | 10 | 0.4 | 2.5k | 0.0k | 19 s |
| ts-plugin-bug | timeout (timeout) | 100% | 8/8 | 74 | 1 min 00 s | 0.0000 | 24 | 29 | 0.0 | 7.2k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 75 | 45.9 s | 0.0000 | 15 | 14 | 0.0 | 5.6k | 0.0k | 22 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.284 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 80% | 10/12 | 46 | 1 min 30 s | 0.0000 | 9 | 9 | 0.0 | 11.3k | 0.0k | 30 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 11 | 1 min 00 s | 0.0000 | 13 | 18 | 0.4 | 1.5k | 0.0k | - |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:61150", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 80 | 1 min 06 s | 0.0000 | 35 | 35 | 0.0 | 6.8k | 0.0k | - |
| web-plan-ranking | ok | 75% | 7/9 | 56 | 2 min 56 s | 0.0000 | 15 | 16 | 0.3 | 5.6k | 0.0k | 105 s |
| web-word-universe | ok | 62% | 6/9 | 45 | 1 min 55 s | 0.0000 | 32 | 33 | 0.0 | 14.6k | 0.0k | 11 s |

## Failed checks

- `web-archery-game` a scripted basic play raises the score: expected 'a score that rises after a few shots', received [None, None, None, None, None, None]
- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `cmp-handoff` summary exists and fits in 1000 characters: 1331 characters
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 268}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 60}
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `rs-lock-bug` hidden opposite transfers do not hang: expected 'opposite_transfers_do_not_hang passed', received False
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
- `3d-print-homage` counted the boats in the print: expected 3, received None
- `3d-print-homage` named the mountain: expected 'Mount Fuji', received None
- `web-fact-search` sqlite_3_40_0_release_date value: expected '2022-11-16', received None
- `web-fact-search` sqlite_3_40_0_release_date primary source: expected 'an http(s) URL on sqlite.org', received None
- `web-fact-search` postgresql_15_0_release_date value: expected '2022-10-13', received None
- `web-fact-search` postgresql_15_0_release_date primary source: expected 'an http(s) URL on postgresql.org', received None
- `web-fact-search` unicode_15_0_characters_added value: expected 4489, received None
- `web-fact-search` unicode_15_0_characters_added primary source: expected 'an http(s) URL on unicode.org', received None
- `web-fact-search` cited primary sources were fetched: expected "each cited source's host in a fetch action", received ['sqlite_3_40_0_release_date', 'postgresql_15_0_release_date', 'unicode_15_0_characters_added']
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': '28-02-1986', 'Bresser': '12-06-1987', 'Verao': '15-01-1989', 'Collor I': '16-03-1990', 'Collo
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 3065, 'urls': 2, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 10 (contato, coracoes, em-construção, link-antigo, pagina-removida)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'advogado: missing 0 (none), extra 1 (coracoes)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 255, 'relations': 764, 'most_connected': ['palavra', 'tempo']}

## Left open

- `media-voice`: still running: pwsh.exe (22604)

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 2); read the ledger (call 4); used the chart of accounts (call 5); used the cash balance (call 3); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 3); recorded the result (call 5)
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 2)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 4)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 4); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 6); committed (call 7)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 8); ran the whole suite (call 26)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 2)
- `file-media-edit`: read the details (call 2); made the feed photo (call 5); filled the permit (call 7)
- `txt-regex-log`: wrote the regex (call 8); tried it in Python (call 2)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 2); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 2); wrote the JSON (call 7)
- `hw-stutter-tuning`: read the frame capture (call 5); read the sensor log (call 4); read the settings (call 2); read the owner notes (call 3); recorded the result (call 9)
- `ts-plugin-bug`: read the bus (call 7); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 5); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); replied (call 29)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 10); wrote the dossier (call 14); opened a source (call 4)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 5); wrote the page (call 9); looked at it in a browser (call 12); recorded the result (call 5)
