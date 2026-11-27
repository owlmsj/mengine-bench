# mengine-bench 2.8.0: opencode opencode v2.3.2 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **76.2** | 86.2 | 19/29 | 70.2 | 65.9 | 20 min 13 s | $0.00 (local) | 4.24M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090; model=Qwen3.8-27B; ctx=256k; clock_cap=2900 MHz both GPUs; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pilot7-a1-dpo50 (50% step-15 DPO on A1 SFT); cache=FP16; drafter=MTP n4 dynamic; layout=native TP 2x RTX 5090; temperature=0.6; finetune=pilot7-a1-dpo50 (0.5x B DPO step-15 on pilot7-a1-sft), THINKING OFF; study=mengine-qlora#42 pilot 7 A1+50%DPO eval run 1; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-26, started 2026-11-26T23:24:58Z; bench at f17d96721857; submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 78 | 1 min 11 s | 0.0000 | 14 | 13 | 0.4 | 7.6k | 0.0k | 33 s |
| py-async-cancel | ok | 100% | 6/6 | 85 | 29.8 s | 0.0000 | 9 | 8 | 0.0 | 3.5k | 0.0k | 5 s |
| ds-ab-playtest | ok | 100% | 5/5 | 90 | 48.2 s | 0.0000 | 8 | 8 | 0.1 | 2.3k | 0.0k | 32 s |
| bo-pnl-runway | ok | 100% | 6/6 | 77 | 22.0 s | 0.0000 | 6 | 8 | 0.0 | 2.4k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 5/5 | 79 | 21.2 s | 0.0000 | 8 | 9 | 0.2 | 2.0k | 0.0k | 7 s |
| cmp-handoff | ok | 100% | 12/12 | 87 | 45.6 s | 0.0000 | 22 | 20 | 0.0 | 4.6k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 5/5 | 91 | 17.1 s | 0.0000 | 9 | 12 | 0.0 | 1.7k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 7/7 | 74 | 35.8 s | 0.0000 | 12 | 11 | 0.4 | 4.3k | 0.0k | 5 s |
| ds-sql-funnel | ok | 25% | 2/5 | 38 | 21.7 s | 0.0000 | 9 | 9 | 0.4 | 2.1k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 80 | 17.8 s | 0.0000 | 5 | 11 | 0.1 | 1.8k | 0.0k | 9 s |
| git-merge-conflict | ok | 100% | 7/7 | 93 | 17.4 s | 0.0000 | 7 | 6 | 0.7 | 1.3k | 0.0k | 7 s |
| infra-gpu-fit | ok | 100% | 7/7 | 88 | 16.2 s | 0.0000 | 6 | 7 | 0.1 | 1.7k | 0.0k | 5 s |
| ir-server-logs | timeout (timeout) | 0% | 1/7 | 6 | 1 min 00 s | 0.0000 | 2 | 5 | 0.1 | 0.4k | 0.0k | - |
| gd-integration-repo | ok | 88% | 9/10 | 61 | 24.1 s | 0.0000 | 6 | 14 | 0.1 | 2.0k | 0.0k | 12 s |
| media-voice | ok | 67% | 3/4 | 48 | 33.7 s | 0.0000 | 13 | 12 | 0.8 | 1.3k | 0.0k | - |
| file-media-edit | ok | 100% | 10/10 | 76 | 1 min 01 s | 0.0000 | 22 | 23 | 0.6 | 4.7k | 0.0k | 15 s |
| txt-regex-log | ok | 75% | 4/5 | 47 | 46.8 s | 0.0000 | 16 | 15 | 0.0 | 5.7k | 0.0k | 3 s |
| rs-lock-bug | ok | 100% | 9/9 | 84 | 17.1 s | 0.0000 | 6 | 7 | 0.0 | 1.6k | 0.0k | 7 s |
| sec-leak-fix | ok | 88% | 9/10 | 82 | 15.7 s | 0.0000 | 7 | 11 | 0.0 | 1.5k | 0.0k | 6 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 83 | 30.5 s | 0.0000 | 26 | 27 | 0.0 | 2.4k | 0.0k | - |
| ds-sqlite-recover | timeout (timeout) | 20% | 2/6 | 12 | 1 min 00 s | 0.0000 | 24 | 24 | 0.3 | 6.4k | 0.0k | 19 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 90 | 25.4 s | 0.0000 | 9 | 9 | 0.3 | 2.3k | 0.0k | 16 s |
| ts-plugin-bug | ok | 100% | 8/8 | 91 | 20.5 s | 0.0000 | 8 | 11 | 0.1 | 2.0k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 74 | 40.6 s | 0.0000 | 11 | 10 | 0.1 | 5.2k | 0.0k | 21 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.565 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 58 | 44.2 s | 0.0000 | 8 | 7 | 0.4 | 5.5k | 0.0k | 2 s |
| web-fact-search | timeout (timeout) | 100% | 8/8 | 71 | 1 min 00 s | 0.0000 | 12 | 22 | 0.2 | 2.1k | 0.0k | 11 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:51066", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/158.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 90 | 33.4 s | 0.0000 | 24 | 23 | 0.0 | 2.3k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 88% | 8/9 | 61 | 3 min 30 s | 0.0000 | 55 | 55 | 0.3 | 9.8k | 0.0k | 186 s |
| web-word-universe | ok | 50% | 5/9 | 41 | 1 min 06 s | 0.0000 | 17 | 17 | 0.5 | 6.0k | 0.0k | 15 s |

## Failed checks

- `ds-sql-funnel` players per step on pc: expected {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 269}, received {'install': 470, 'tutorial_complete': 389, 'first_match': 326, 'purchase': 255}
- `ds-sql-funnel` players per step on steamdeck: expected {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 61}, received {'install': 192, 'tutorial_complete': 128, 'first_match': 87, 'purchase': 54}
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': 'purchase', 'steamdeck': 'purchase'}
- `ir-server-logs` incident start: expected '2026-06-02 03:17:42', received None
- `ir-server-logs` incident end: expected '2026-06-02 03:53:31', received None
- `ir-server-logs` minutes down: expected 35.81666666666667, received None
- `ir-server-logs` June availability: expected 99.9170910493827, received None
- `ir-server-logs` SLO 99.9 met: expected True, received None
- `ir-server-logs` root cause = /data disk full: expected 'the /data disk was full', received None
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `media-voice` whisper tiny hears the sentence: expected 'WER <= 0.2', received "'Welcome to Marty evening fairy. Please keep your bags clear off the doors of our voice. He equals SLT.' (WER 0.77)"
- `txt-regex-log` the last date on each line with an address: expected ['2026-02-11', '2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31'], received ['2025-10-02', '2024-06-30', '2023-04-01', '2023-01-07', '2021-07-19', '2020-11-30', '2019-05-31']
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 2166, 'urls': 2, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 52 (acougueiro, aflicao, agua, almoco, amanha)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received 'acougueiro: missing 0 (none), extra 3 (enfermeira, pescador, tarde)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'most_connected': 'tempo', 'words': 252, 'relations': 832}
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=país does not show its 5 relations, missing nação

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); ran it (call 3)
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); not seen: removed duplicate sessions; tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 6)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 5)
- `cmp-handoff`: read the session (call 3); wrote the handoff (call 4); recorded the result (call 19)
- `cfg-source-drift`: read the readme (call 4); ran the generator (call 3)
- `doc-lab-pdf`: opened the exams (call 2); extracted the text (call 2); recorded the result (call 3)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 6); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 3); read the game mode (call 5); recorded the result (call 7)
- `git-merge-conflict`: merged the branch (call 3); ran the tests (call 5); committed (call 5)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 6)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); not seen: recorded the result
- `gd-integration-repo`: read the docs (call 2); ran the integration test (call 4); ran the whole suite (call 14)
- `media-voice`: used a speech engine (call 2); wrote the audio (call 11)
- `file-media-edit`: read the details (call 2); made the feed photo (call 7); filled the permit (call 7)
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 3)
- `rs-lock-bug`: read the crate (call 3); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 2); read the config (call 3); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 1); opened the site (call 3); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 6); wrote the JSON (call 6)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 6); read the settings (call 3); read the owner notes (call 2); recorded the result (call 8)
- `ts-plugin-bug`: read the bus (call 5); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 2); looked at it in a browser (call 3); recorded the result (call 1)
- `web-fact-search`: not seen: searched the web; recorded the result (call 10); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 2); downloaded the invoice (call 3); not seen: replied
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 53); wrote the dossier (call 54); opened a source (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 4); wrote the page (call 7); looked at it in a browser (call 8); recorded the result (call 4)
