# mengine-bench 2.6.0: opencode opencode v2.2.5 / maritaca/S5 (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **55.9** | 80.9 | 15/28 | 61.7 | 0.0 | 36 min 59 s | >= $0.00 (harness) | 1.59M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=maritaca; model=S5; tier=1; role=dev-r; account_limits=tier 0: 60 RPM, 128k TPM in, 10k TPM out; price_source=docs.maritaca.ai/pt/precos BRL at USD-BRL 5.4933 (2026-11-06); personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-06, started 2026-11-06T13:28:02Z; bench at ea25e4e2b89b; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| py-async-cancel | timeout (timeout) | 100% | 6/6 | 64 | 1 min 00 s | - | 10 | 10 | 0.4 | 7.8k | 5.3k | 16 s |
| ds-ab-playtest | ok | 100% | 5/5 | 81 | 35.0 s | 0.0000 | 9 | 9 | 0.3 | 5.6k | 3.1k | 12 s |
| bo-pnl-runway | ok | 100% | 6/6 | 61 | 49.4 s | 0.0000 | 11 | 14 | 0.1 | 7.3k | 2.6k | 25 s |
| bo-reconcile | ok | 100% | 5/5 | 69 | 34.1 s | 0.0000 | 7 | 8 | 0.3 | 4.5k | 2.2k | 16 s |
| cmp-handoff | ok | 91% | 11/12 | 53 | 46.9 s | 0.0000 | 11 | 10 | 0.1 | 6.1k | 4.1k | 22 s |
| cfg-source-drift | ok | 100% | 5/5 | 92 | 27.7 s | 0.0000 | 9 | 12 | 0.1 | 2.8k | 1.4k | 12 s |
| doc-lab-pdf | timeout (timeout) | 0% | 1/7 | 8 | 1 min 00 s | - | 7 | 8 | 0.1 | 5.2k | 3.3k | 23 s |
| ds-sql-funnel | ok | 75% | 4/5 | 52 | 1 min 21 s | 0.0000 | 17 | 17 | 0.3 | 9.1k | 4.5k | 13 s |
| ue-packaged-bug | ok | 100% | 6/6 | 71 | 1 min 24 s | 0.0000 | 14 | 17 | 0.1 | 14.7k | 12.4k | 55 s |
| git-merge-conflict | ok | 100% | 7/7 | 87 | 48.4 s | 0.0000 | 14 | 13 | 0.6 | 6.7k | 4.5k | 14 s |
| infra-gpu-fit | ok | 100% | 7/7 | 68 | 42.9 s | 0.0000 | 8 | 9 | 0.0 | 7.7k | 6.8k | 29 s |
| ir-server-logs | ok | 100% | 7/7 | 79 | 45.8 s | 0.0000 | 9 | 9 | 0.4 | 4.9k | 3.5k | 30 s |
| gd-integration-repo | ok | 88% | 9/10 | 66 | 1 min 19 s | 0.0000 | 13 | 22 | 0.1 | 11.1k | 8.9k | 36 s |
| media-voice | ok | 100% | 4/4 | 68 | 36.5 s | 0.0000 | 7 | 6 | 0.9 | 2.7k | 1.3k | - |
| file-media-edit | timeout (timeout, evidence 'out/permit-filled.pdf' skipped: received FileNotFoundError; expected a regular workspace file without symlinks, at most 5242880 bytes) | 38% | 5/10 | 32 | 1 min 30 s | - | 12 | 16 | 0.5 | 9.2k | 6.6k | - |
| txt-regex-log | timeout (timeout) | 50% | 3/5 | 32 | 1 min 00 s | - | 8 | 8 | 0.0 | 9.5k | 6.4k | 10 s |
| rs-lock-bug | ok (left running, not attributed: vctip.exe (16596)) | 100% | 9/9 | 77 | 1 min 02 s | 0.0000 | 10 | 11 | 0.1 | 8.6k | 6.4k | 9 s |
| sec-leak-fix | ok | 88% | 9/10 | 81 | 35.0 s | 0.0000 | 10 | 11 | 0.0 | 4.6k | 2.9k | 20 s |
| cu-social-cycle | ok (route observed: browser (3 of 3 writes with Sec-Fetch-*; user agents ['Mozilla'])) | 100% | 11/11 | 83 | 1 min 11 s | 0.0000 | 31 | 33 | 0.0 | 6.4k | 3.0k | - |
| ds-sqlite-recover | timeout (timeout) | 0% | 1/6 | 11 | 1 min 00 s | - | 11 | 11 | 0.3 | 7.5k | 5.2k | 20 s |
| hw-stutter-tuning | timeout (timeout) | 0% | 1/7 | 29 | 1 min 30 s | - | 19 | 21 | 0.2 | 11.3k | 5.3k | 21 s |
| ts-plugin-bug | ok | 100% | 8/8 | 95 | 32.7 s | 0.0000 | 9 | 12 | 0.1 | 3.9k | 1.7k | 7 s |
| web-mondrian-landing | ok | 100% | 11/11 | 72 | 1 min 32 s | 0.0000 | 21 | 22 | 0.1 | 15.4k | 7.1k | 19 s |
| 3d-print-homage | crash (crash, page not run: render failed: timeout after 120s; stderr: [9304:4724:1106/105430.648:WARNING:chrome\browser\extensions\external_registry_loader_win.cc:283] Error observing HKLM: 5 | [9304:4724:1106/105430.783:ERROR:chrome\browser\component_updater\edge_optimization_guide_models_manifest_installer.cc:264] Edge LLM: catalog update failed: 5 | [9304:4724:1106/105430.789:ERROR:chrome\browser\component_updater\edge_language_detection_model_installer.cc:97] Edge Language Detection Model: On-demand update failed with error: 5 | [9304:4724:1106/105430.805:INFO:CONSOLE:6233] "[ProtocolLaunch] handler constructed; wiring port events.", source: chrome-extension://ndcpkimcihhghdcddljkfmmjccdmcmof/background.rollup.js (6233) | [9304:4724:1106/105431.073:WARNING:components\signin\internal\identity_manager\account_fetcher_service.cc:252] Edge does not support fetching account capabilities | [9304:4724:1106/105431.073:WARNING:components\signin\internal\identity_manager\account_fetcher_service.cc:213] Should not execute: Tests depending on this function may fail | [9304:4724:1106/105431.114:ERROR:components\edge_auth\edge_auth_errors.cc:561] EDGE_IDENTITY: Image Fetch FAILED: Error: Primary Error: kUrlRequestError, Secondary Error: kURLResponseNot200, Platform error: 0, Error string: [empty] | [9304:9716:1106/105431.128:WARNING:components\sync\engine\syncer_proto_util.cc:677] Error posting from syncer: Response Code (bogus on error): -1 Content-Length (bogus on error): -1 X-AFS-Tracking:  Server Status: CONNECTION_UNAVAILABLE) | 100% | 10/10 | 36 | 4 min 04 s | - | 46 | 46 | 0.1 | 32.4k | 17.4k | 84 s |
| web-fact-search | ok | 100% | 8/8 | 90 | 16.7 s | 0.0000 | 3 | 5 | 0.7 | 2.2k | 1.3k | 5 s |
| cu-webmail | ok (write routes (observation only): {"origin": "http://127.0.0.1:59980", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 "}) | 100% | 9/9 | 79 | 1 min 43 s | 0.0000 | 32 | 33 | 0.3 | 9.7k | 3.7k | - |
| web-plan-ranking | ok | 75% | 7/9 | 54 | 2 min 51 s | 0.0000 | 17 | 15 | 0.3 | 23.8k | 14.5k | 91 s |
| web-word-universe | timeout (timeout) | 62% | 6/9 | 37 | 6 min 00 s | - | 46 | 46 | 0.3 | 51.0k | 25.3k | 130 s |

## Failed checks

- `cmp-handoff` summary exists and fits in 1000 characters: 1072 characters
- `doc-lab-pdf` hba1c history: expected {'2026-02-10': 5.4, '2026-08-18': 5.54}, received {}
- `doc-lab-pdf` glucose history: expected {'2026-02-10': 92.0, '2026-08-18': 109.9}, received {}
- `doc-lab-pdf` ldl history: expected {'2026-02-10': 118.0, '2026-08-18': 143.08}, received {}
- `doc-lab-pdf` creatinine history: expected {'2026-02-10': 0.95, '2026-08-18': 0.86}, received {}
- `doc-lab-pdf` flags what got worse and left the range: expected ['glucose', 'ldl'], received None
- `doc-lab-pdf` leaves out what stayed in range: expected ['glucose', 'ldl'], received None
- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.8252, 'players_before': 326, 'players_at_step': 269, 'lost': 57}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': 0.6667, 'players_before': 192, 'players_at_step': 128, 'lost'
- `gd-integration-repo` hidden half up fractional multiplier: FAIL: test_half_up_fractional_multiplier (test_hidden_gold.Hidden.test_half_up_fractional_multiplier) | AssertionError: 1490 != 1500
- `file-media-edit` permit organizer filled: expected "'Tidewater Studio' shown in the Organizer box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit event_date filled: expected "'2026-12-05' shown in the Event date (YYYY-MM-DD) box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit location filled: expected "'North Cove Lawn' shown in the Location in the park box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit attendees filled: expected "'40' shown in the Expected attendees box", received 'no out/permit-filled.pdf'
- `file-media-edit` permit flattened: expected 'no form fields or widgets left', received 'no out/permit-filled.pdf'
- `txt-regex-log` impossible dates match nothing: expected ['2023-02-29', '2023-09-30', '2023-10-31'], received ['2024-08-00', '2023-02-29', '2023-09-30', '2023-10-31']
- `txt-regex-log` dates glued to letters or digits match nothing: expected ['2024-03-18', '2024-03-20'], received ['2024-03-16', '2024-03-17', '2024-03-18', '2024-03-20']
- `sec-leak-fix` hidden a missing BACKUP_TOKEN raises a clear error: FAIL: test_case (test_hidden_gold.HiddenCase.test_case) | AssertionError: no error without BACKUP_TOKEN
- `ds-sqlite-recover` recovered.json is a list of item and price rows: expected '[{"item": "...", "price": N}, ...]', received 'None'
- `ds-sqlite-recover` rows stored as whole numbers recovered: expected ['camp stove', 'lantern', 'rope coil', 'sleeping bag'], received []
- `ds-sqlite-recover` rows with fractional prices recovered: expected ['compass', 'first aid kit', 'tent stake', 'water filter'], received []
- `ds-sqlite-recover` rows stored as the constants 0 and 1 recovered: expected ['matchbox', 'trail map'], received []
- `ds-sqlite-recover` no row that is not in the table: expected 'only real rows', received []
- `hw-stutter-tuning` average FPS: expected 137.3, received None
- `hw-stutter-tuning` 1% low FPS: expected 45.4, received None
- `hw-stutter-tuning` cause named: expected "the GPU link's power-saving state (ASPM L1 on its root port)", received None
- `hw-stutter-tuning` ASPM off on the GPU root port: expected 'pcie_aspm_rp1_gpu -> disabled', received []
- `hw-stutter-tuning` GPU link speed kept: expected 'changes that leave the link speed alone', received []
- `hw-stutter-tuning` BIOS overclock kept: expected 'no XMP, PBO or core ratio change', received []
- `web-plan-ranking` every plan has a source: expected 'a cited http(s) URL on a fetched host for every plan', received ['Cruzado', 'Bresser', 'Verao', 'Collor I', 'Collor II', 'Real']
- `web-plan-ranking` dossier: expected '600+ chars, 3+ cited URLs on fetched hosts, 3+ plans', received {'chars': 4377, 'urls': 0, 'plans': ['bresser', 'collor', 'cruzado', 'real', 'verao']}
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 56 (_meta, acougueiro, acucar, aflicao, agua)
- `web-word-universe` relations of a sample of words: expected 'all relations from the site', received '_meta: missing 0 (none), extra 3 (generator, note, source)'
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 250, 'relations': 743, 'most_connected': [{'word': 'palavra', 'degree': 16}, {'word': 'tempo', 'degree': 16}]}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `py-async-cancel`: wrote run.py (call 3); ran it (call 1)
- `ds-ab-playtest`: read the notes (call 3); read the data (call 4); removed duplicate sessions (call 6); tested significance (call 6); recorded the result (call 6)
- `bo-pnl-runway`: read the notes (call 4); read the ledger (call 5); used the chart of accounts (call 7); used the cash balance (call 6); recorded the result (call 13)
- `bo-reconcile`: read the notes (call 3); read the invoices (call 5); read the statement (call 4); recorded the result (call 7)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 7); recorded the result (call 10)
- `cfg-source-drift`: read the readme (call 2); ran the generator (call 4)
- `doc-lab-pdf`: opened the exams (call 1); not seen: extracted the text; recorded the result (call 7)
- `ds-sql-funnel`: read the rules (call 2); looked at the schema (call 5); excluded test accounts (call 8); recorded the result (call 10)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 5); recorded the result (call 17)
- `git-merge-conflict`: merged the branch (call 10); ran the tests (call 12); committed (call 13)
- `infra-gpu-fit`: read the offers (call 2); read the model (call 1); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 5); ran the integration test (call 7); ran the whole suite (call 17)
- `media-voice`: used a speech engine (call 1); wrote the audio (call 4)
- `file-media-edit`: read the details (call 3); made the feed photo (call 16); not seen: filled the permit
- `txt-regex-log`: wrote the regex (call 2); tried it in Python (call 7)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 8)
- `sec-leak-fix`: read the service (call 3); read the config (call 2); ran the tests (call 10)
- `cu-social-cycle`: made the image (call 3); opened the site (call 4); not seen: deleted the test post
- `ds-sqlite-recover`: read the raw bytes (call 3); not seen: wrote the JSON
- `hw-stutter-tuning`: read the frame capture (call 7); read the sensor log (call 6); read the settings (call 4); read the owner notes (call 3); not seen: recorded the result
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 6); looked at it in a browser (call 10)
- `3d-print-homage`: wrote the scene (call 6); looked at it in a browser (call 11); recorded the result (call 10)
- `web-fact-search`: not seen: searched the web; recorded the result (call 4); opened a source (call 1)
- `cu-webmail`: opened the mail app (call 3); downloaded the invoice (call 9); replied (call 24)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; recorded the result (call 7); wrote the dossier (call 5); not seen: opened a source
- `web-word-universe`: walked the site (call 1); wrote words.json (call 30); wrote the page (call 42); not seen: looked at it in a browser; recorded the result (call 30)
