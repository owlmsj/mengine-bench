# mengine-bench 2.8.0: opencode opencode v2.2.5 / home/qwen38-27b-exl3-sc6-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **69.7** | 85.3 | 16/29 | 70.6 | 18.3 | 34 min 31 s | >= $0.00 | 7.51M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; model=Qwen3.8-27B; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-recipe SC_6.00bpw_H6_V6 of pilot5 merge; ctx=256k; cache=FP16; layout=native TP 2x RTX 5090; drafter=MTP n4 dynamic; tier=2; temperature=0.6; finetune=mengine-qlora pilot5-data5 (bf16 LoRA r16, SFT 377 ex); mengine=2.8.0 installed; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-18, started 2026-11-18T10:42:40Z; bench at ac16be22ea10 (dirty tree); submitter -

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web-archery-game | ok | 100% | 8/8 | 62 | 1 min 14 s | 0.0000 | 10 | 9 | 0.8 | 8.7k | 0.0k | 42 s |
| py-async-cancel | timeout (timeout) | 80% | 5/6 | 43 | 1 min 00 s | - | 2 | 2 | 0.0 | 6.2k | 0.0k | 44 s |
| ds-ab-playtest | ok | 100% | 5/5 | 87 | 43.5 s | 0.0000 | 6 | 6 | 0.0 | 1.7k | 0.0k | 32 s |
| bo-pnl-runway | ok | 40% | 3/6 | 50 | 50.0 s | 0.0000 | 13 | 14 | 0.0 | 6.1k | 0.0k | 20 s |
| bo-reconcile | ok | 100% | 5/5 | 89 | 45.9 s | 0.0000 | 10 | 12 | 0.0 | 6.9k | 0.0k | 26 s |
| cmp-handoff | timeout (timeout) | 27% | 4/12 | 28 | 1 min 30 s | - | 15 | 14 | 0.0 | 10.9k | 0.0k | 12 s |
| cfg-source-drift | ok | 100% | 5/5 | 91 | 15.8 s | 0.0000 | 8 | 13 | 0.0 | 1.5k | 0.0k | 6 s |
| doc-lab-pdf | ok | 83% | 6/7 | 45 | 19.9 s | 0.0000 | 7 | 7 | 0.3 | 2.2k | 0.0k | 9 s |
| ds-sql-funnel | ok | 100% | 5/5 | 84 | 54.3 s | 0.0000 | 16 | 16 | 0.3 | 6.9k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 6/6 | 89 | 56.1 s | 0.0000 | 8 | 14 | 0.0 | 7.4k | 0.0k | 38 s |
| git-merge-conflict | ok | 100% | 7/7 | 96 | 22.2 s | 0.0000 | 9 | 13 | 0.0 | 2.1k | 0.0k | 11 s |
| infra-gpu-fit | ok | 100% | 7/7 | 85 | 15.6 s | 0.0000 | 6 | 7 | 0.0 | 1.6k | 0.0k | 4 s |
| ir-server-logs | ok | 100% | 7/7 | 90 | 39.8 s | 0.0000 | 8 | 9 | 0.0 | 2.1k | 0.0k | 28 s |
| gd-integration-repo | ok | 88% | 9/10 | 69 | 23.4 s | 0.0000 | 9 | 21 | 0.0 | 2.2k | 0.0k | 15 s |
| media-voice | ok | 100% | 4/4 | 73 | 27.1 s | 0.0000 | 4 | 3 | 0.5 | 3.0k | 0.0k | - |
| file-media-edit | ok | 38% | 5/10 | 44 | 35.2 s | 0.0000 | 15 | 16 | 0.4 | 3.4k | 0.0k | - |
| txt-regex-log | timeout (timeout) | 100% | 5/5 | 90 | 1 min 00 s | - | 9 | 8 | 0.3 | 8.1k | 0.0k | 39 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (8340)) | 100% | 9/9 | 91 | 1 min 19 s | 0.0000 | 14 | 16 | 0.0 | 10.7k | 0.0k | 37 s |
| sec-leak-fix | ok | 88% | 9/10 | 82 | 1 min 28 s | 0.0000 | 12 | 17 | 0.0 | 12.8k | 0.0k | 55 s |
| cu-social-cycle | timeout (timeout, route observed: browser (2 of 2 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 67% | 8/11 | 45 | 3 min 00 s | - | 39 | 44 | 0.0 | 21.8k | 0.0k | 11 s |
| ds-sqlite-recover | timeout (timeout) | 100% | 6/6 | 73 | 1 min 00 s | - | 15 | 14 | 0.3 | 6.8k | 0.0k | 32 s |
| hw-stutter-tuning | ok | 100% | 7/7 | 87 | 41.2 s | 0.0000 | 11 | 13 | 0.0 | 4.5k | 0.0k | 26 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 22.4 s | 0.0000 | 8 | 11 | 0.0 | 2.3k | 0.0k | 6 s |
| web-mondrian-landing | ok | 100% | 11/11 | 71 | 1 min 05 s | 0.0000 | 22 | 21 | 0.0 | 7.8k | 0.0k | 20 s |
| 3d-print-homage | ok (blue-layout similarity to the print: 0.501 against great-wave.jpg on a 4x3 grid (0.4 once scored; a note since 2.6)) | 100% | 12/12 | 52 | 1 min 54 s | 0.0000 | 17 | 18 | 0.0 | 14.8k | 0.0k | 58 s |
| web-fact-search | timeout (timeout) | 100% | 8/8 | 69 | 1 min 00 s | - | 11 | 15 | 0.3 | 5.3k | 0.0k | 49 s |
| cu-webmail | ok (write routes (observation only): {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Microsoft Windows 10.0.26200; pt-BR) PowerShell/7.6.9"}) | 100% | 9/9 | 92 | 1 min 08 s | 0.0000 | 27 | 30 | 0.3 | 7.9k | 0.0k | - |
| web-plan-ranking | timeout (timeout) | 0% | 1/9 | 9 | 3 min 30 s | - | 13 | 24 | 0.5 | 15.1k | 0.0k | - |
| web-word-universe | ok | 62% | 6/9 | 65 | 5 min 49 s | 0.0000 | 65 | 68 | 0.0 | 44.7k | 0.0k | 19 s |

## Failed checks

- `py-async-cancel` Ctrl+C with jobs queued starts none and cleans up the rest: expected {'started': 2, 'finished': 0, 'cleaned': 2}, received {'started': 2, 'finished': 0, 'cleaned': 0}
- `bo-pnl-runway` ebitda per month: 2026-01: expected -210278.96, received -203812.19
- `bo-pnl-runway` 3-month average burn: expected 197288.23, received 190820.54
- `bo-pnl-runway` runway in months: expected 9.363713182484327, received 9.68
- `cmp-handoff` summary exists and fits in 1000 characters: 1175 characters
- `cmp-handoff` answer file_line: expected 'a match for \\bstart_server\\.ps1\\b.{0,40}?\\b165\\b', received None
- `cmp-handoff` answer final_decode: expected 'a match for ^(?!.*37[.,]8)(?=.*(?<![\\w.,+-])38(?:[.,]0+)?(?!\\d|[.,]\\d))', received None
- `cmp-handoff` answer final_vram_mib: expected 'a match for (?<![\\w.,+-])7697(?:[.,]0+)?(?!\\w|[.,]\\d)', received ''
- `cmp-handoff` answer discarded_quant: expected 'a match for ^(?=.*\\bQ6(?:_?K)?\\b)(?!.*\\b(?!Q6(?:_?K)?\\b)(?:I?Q\\d+[A-Z0-9_]*|BF16|FP(?:16|32)|F(?:16|32))\\b)', received None
- `cmp-handoff` answer pending: expected 'a match for ^(?!.*\\broot\\b)(?=.*\\bREADME\\b)(?=.*\\b(?:update|fix|remove|edit|replace|check_vision|evals|stale|out of date))', received None
- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received None
- `cmp-handoff` does not repeat the spilled VRAM as final: expected 'not 7881', received None
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {'2026-02-10': 5.4, '2026-08-18': 3.4}
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received ''
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received ''
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received ''
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received ''
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'fields still editable'
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `cu-social-cycle` test post deleted: expected 'deleted', received 'still there'
- `cu-social-cycle` nothing else published: expected [], received ['Testing the new Bluehaze uploader: Harbor Day is on.']
- `cu-social-cycle` post, then delete: expected 'post < delete in the journal', received [2, None]
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
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 255, 'relations': 750, 'most_connected': {'links': 16, 'word': 'palavra'}}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `web-archery-game`: wrote the game (call 1); looked at it in a browser (call 2)
- `py-async-cancel`: wrote run.py (call 1); not seen: ran it
- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 6); tested significance (call 4); recorded the result (call 4)
- `bo-pnl-runway`: read the notes (call 3); read the ledger (call 5); used the chart of accounts (call 4); used the cash balance (call 2); recorded the result (call 9)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 2); read the statement (call 4); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); not seen: recorded the result
- `cfg-source-drift`: read the readme (call 3); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 5); recorded the result (call 5)
- `ue-packaged-bug`: read the crash log (call 6); read the game mode (call 4); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 8); ran the tests (call 12); committed (call 13)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 1); read the policy (call 2); recorded the result (call 4)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 7)
- `gd-integration-repo`: read the docs (call 4); ran the integration test (call 6); ran the whole suite (call 21)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 1)
- `file-media-edit`: read the details (call 2); made the feed photo (call 8); filled the permit (call 11)
- `txt-regex-log`: wrote the regex (call 6); tried it in Python (call 4)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 11)
- `cu-social-cycle`: made the image (call 16); opened the site (call 1); deleted the test post (call 22)
- `ds-sqlite-recover`: read the raw bytes (call 5); wrote the JSON (call 5)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 6); read the settings (call 5); read the owner notes (call 3); recorded the result (call 11)
- `ts-plugin-bug`: read the bus (call 6); ran the tests (call 9)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 3); looked at it in a browser (call 8); recorded the result (call 4)
- `web-fact-search`: not seen: searched the web; recorded the result (call 12); opened a source (call 2)
- `cu-webmail`: opened the mail app (call 18); downloaded the invoice (call 8); replied (call 17)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; not seen: recorded the result; not seen: wrote the dossier; opened a source (call 3)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 12); wrote the page (call 23); looked at it in a browser (call 26); recorded the result (call 12)
