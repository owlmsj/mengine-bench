# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **62.4** | 74.5 | 15/29 | 59.8 | 37.8 | 28 min 39 s | $0.00 (local) | 6.68M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; finetune=harness-hub/Qwen3.8-27B-super-adapter rev 3358a715, THINKING OFF; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of super-adapter merge; cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; sampling=temperature 0.5 (forced), top_k 20, top_p 0.95; study=temperature 0.5 vs 0.6 (2026-11-22); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-22, started 2026-11-22T14:47:30Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 78 | 2 min 10 s | 0.0000 | 36 | 35 | 0.4 | 9.6k | 0.0k | 35 s |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 62 | 1 min 00 s | 0.0000 | 19 | 19 | 0.0 | 7.3k | 0.0k | 5 s |
| ds-ab-playtest | ok | 100% | 5/5 | 92 | 48.0 s | 0.0000 | 8 | 8 | 0.0 | 2.2k | 0.0k | 33 s |
| bo-pnl-runway | ok | 100% | 6/6 | 76 | 24.8 s | 0.0000 | 9 | 11 | 0.0 | 2.5k | 0.0k | 9 s |
| bo-reconcile | ok | 100% | 5/5 | 75 | 15.6 s | 0.0000 | 6 | 7 | 0.0 | 1.5k | 0.0k | 6 s |
| cmp-handoff | timeout (timeout) | 27% | 4/12 | 24 | 1 min 30 s | 0.0000 | 34 | 33 | 0.0 | 13.8k | 0.0k | 8 s |
| cfg-source-drift | ok | 100% | 5/5 | 96 | 15.9 s | 0.0000 | 8 | 11 | 0.0 | 1.5k | 0.0k | 7 s |
| doc-lab-pdf | ok | 100% | 7/7 | 66 | 22.7 s | 0.0000 | 7 | 6 | 0.0 | 2.8k | 0.0k | 5 s |
| ds-sql-funnel | ok | 25% | 2/5 | 33 | 21.8 s | 0.0000 | 9 | 9 | 0.0 | 2.3k | 0.0k | 3 s |
| ue-packaged-bug | ok | 80% | 5/6 | 32 | 18.3 s | 0.0000 | 7 | 10 | 0.0 | 1.9k | 0.0k | 6 s |
| git-merge-conflict | ok | 100% | 7/7 | 94 | 14.2 s | 0.0000 | 7 | 6 | 0.4 | 1.1k | 0.0k | 5 s |
| infra-gpu-fit | ok | 100% | 7/7 | 92 | 15.3 s | 0.0000 | 5 | 6 | 0.0 | 1.7k | 0.0k | 5 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 5 | 1 min 00 s | 0.0000 | 2 | 5 | 0.0 | 0.4k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 68 | 21.2 s | 0.0000 | 9 | 23 | 0.0 | 2.1k | 0.0k | 12 s |
| media-voice | ok | 100% | 4/4 | 84 | 20.7 s | 0.0000 | 9 | 8 | 0.5 | 1.6k | 0.0k | 10 s |
| file-media-edit | ok | 50% | 6/10 | 47 | 1 min 02 s | 0.0000 | 21 | 20 | 0.4 | 5.5k | 0.0k | 18 s |
| txt-regex-log | ok | 100% | 5/5 | 83 | 47.5 s | 0.0000 | 12 | 11 | 0.0 | 6.4k | 0.0k | 3 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (19968)) | 83% | 8/9 | 69 | 44.5 s | 0.0000 | 19 | 20 | 0.0 | 4.8k | 0.0k | 5 s |
| sec-leak-fix | ok | 88% | 9/10 | 77 | 14.7 s | 0.0000 | 7 | 10 | 0.0 | 1.5k | 0.0k | 6 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 88 | 34.6 s | 0.0000 | 25 | 25 | 0.0 | 2.2k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 17 | 1 min 00 s | 0.0000 | 15 | 14 | 0.3 | 6.7k | 0.0k | 16 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 72 | 28.2 s | 0.0000 | 9 | 11 | 0.0 | 2.4k | 0.0k | 9 s |
| ts-plugin-bug | ok | 100% | 8/8 | 90 | 45.6 s | 0.0000 | 19 | 23 | 0.0 | 5.1k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 83 | 25.9 s | 0.0000 | 6 | 5 | 0.4 | 3.0k | 0.0k | 12 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.14 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 53 | 1 min 33 s | 0.0000 | 31 | 30 | 0.0 | 9.8k | 0.0k | 20 s |
| web-fact-search | timeout (timeout) | 0% | 1/8 | 10 | 1 min 00 s | 0.0000 | 20 | 23 | 0.4 | 2.0k | 0.0k | - |
| cu-webmail | timeout (timeout, write routes (observation only): {"origin": "http://127.0.0.1:55798", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 50% | 6/9 | 21 | 3 min 00 s | 0.0000 | 52 | 52 | 0.0 | 22.0k | 0.0k | 35 s |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 4 | 3 min 30 s | 0.0000 | 31 | 30 | 1.2 | 2.8k | 0.0k | - |
| web-word-universe | ok | 50% | 5/9 | 42 | 3 min 53 s | 0.0000 | 40 | 40 | 0.0 | 28.0k | 0.0k | 8 s |

## Failed checks

- `cmp-handoff` summary exists and fits in 1000 characters: 1164 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 276}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 65}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'tutorial_complete', 'steamdeck': 'tutorial_complete'}
- `ue-packaged-bug` crash fixed: the score tracker survives garbage collection: ScoreTracker is not kept alive by UPROPERTY, TStrongObjectPtr, AddToRoot or a reported reference
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
- `rs-lock-bug` hidden a transfer to the same player changes nothing: expected 'a_transfer_to_the_same_player_changes_nothing passed', received False
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
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
- `cu-webmail` reply sent in the invoice conversation: expected 'one reply in thread 19a2f4c81e7b30d5', received []
- `cu-webmail` reply addressed to the sender: expected ['[REDACTED:email]'], received []
- `cu-webmail` reply states the invoice total: expected 1205.77, received ''
- `web-plan-ranking` all six plans recorded: expected ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real'], received []
- `web-plan-ranking` launch dates: expected {'Cruzado': ['1986-02-28'], 'Bresser': ['1987-06-12'], 'Verao': ['1989-01-15'], 'Collor I': ['1990-03-16'], 'Collor II': ['1991-01-31'], 'Real': ['1994-03-01', '1994-07-01']}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1], 'Real': [2477.15, 22.41]}, received {'Cruzado': [None, None], 'Bresser': [None, None], 'Verao': [None, None], 'Collor I': [None, None], 'Collor
- `web-plan-ranking` months lasted: expected {'Cruzado': [15], 'Bresser': [19], 'Verao': [14], 'Collor I': [10], 'Collor II': [37, 41], 'Real': [60]}, received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': None, 'Bresser': None, 'Verao': None, 'Collor I': None, 'Collor II': None, 'Real': None}
- `web-plan-ranking` top 3: expected ['Real', 'Collor I', 'Collor II'], received None
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 0, 'urls': 0, 'plans': []}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 50 (acougueiro, aflicao, agua, almoco, amanha)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acougueiro: missing 0 (none), extra 3 (enfermeira, pescador, tarde)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'relations': 832, 'words': 250, 'most_connected': 'palavra'}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país does not show its 5 relations, missing nação

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 3); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 4); recorded the result (call 10)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 3); ran the integration test (call 8); ran the whole suite (call 23)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 4)
- `file-media-edit`: read the details (call 2); made the feed photo (call 7); filled the permit (call 7)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 9)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 4); read the config (call 2); ran the tests (call 9)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); wrote the JSON (call 11)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 5); read the settings (call 2); read the owner notes (call 3); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 10)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 1); looked at it in a browser (call 3); recorded the result (call 2)
- `web-fact-search`: not seen: searched the web; not seen: recorded the result; opened a source (call 3)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 7)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 9); looked at it in a browser (call 12); recorded the result (call 7)
