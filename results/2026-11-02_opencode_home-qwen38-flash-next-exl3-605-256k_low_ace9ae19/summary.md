# mengine-bench 2.0.0: opencode opencode v2.2.5 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **78.1** | 95.0 | 18/20 | 81.2 | 37.7 | 20 min 34 s | $0.00 (price) | 4.02M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; temperature=0.5; tier=2; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T19:28:04Z; bench at 8f250b297086; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 89 | 41.7 s | 0.0000 | 10 | 10 | 4.8k | 0.0k | 10 s |
| bo-pnl-runway | ok | 100% | 5/5 | 87 | 38.9 s | 0.0000 | 9 | 11 | 4.9k | 0.0k | 10 s |
| bo-reconcile | ok | 100% | 4/4 | 89 | 26.6 s | 0.0000 | 9 | 10 | 3.1k | 0.0k | 9 s |
| cmp-handoff | ok | 100% | 11/11 | 89 | 40.1 s | 0.0000 | 13 | 11 | 4.5k | 0.0k | 13 s |
| cfg-source-drift | ok | 100% | 3/3 | 99 | 19.2 s | 0.0000 | 9 | 13 | 1.9k | 0.0k | 6 s |
| doc-lab-pdf | ok | 100% | 6/6 | 82 | 27.1 s | 0.0000 | 9 | 9 | 3.5k | 0.0k | 5 s |
| ds-sql-funnel | ok | 100% | 3/3 | 87 | 36.5 s | 0.0000 | 14 | 16 | 4.3k | 0.0k | 3 s |
| ue-packaged-bug | ok | 100% | 5/5 | 87 | 20.8 s | 0.0000 | 7 | 10 | 2.4k | 0.0k | 8 s |
| git-merge-conflict | ok | 100% | 6/6 | 88 | 28.1 s | 0.0000 | 13 | 15 | 2.9k | 0.0k | 10 s |
| infra-gpu-fit | ok | 100% | 6/6 | 88 | 14.9 s | 0.0000 | 5 | 6 | 1.9k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 6/6 | 85 | 26.3 s | 0.0000 | 8 | 8 | 2.7k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 93 | 1 min 52 s | 0.0000 | 30 | 41 | 12.2k | 0.0k | 52 s |
| rs-lock-bug | timeout (timeout) | 25% | 3/6 | 28 | 3 min 00 s | 0.0000 | 10 | 10 | 3.0k | 0.0k | 10 s |
| sec-leak-fix | ok | 100% | 8/8 | 85 | 46.5 s | 0.0000 | 16 | 21 | 4.8k | 0.0k | 20 s |
| hw-stutter-tuning | ok | 100% | 6/6 | 87 | 43.4 s | 0.0000 | 16 | 16 | 5.0k | 0.0k | 12 s |
| ts-plugin-bug | ok | 100% | 7/7 | 89 | 47.3 s | 0.0000 | 10 | 16 | 5.7k | 0.0k | 20 s |
| web-mondrian-landing | ok | 100% | 10/10 | 89 | 41.1 s | 0.0000 | 7 | 7 | 5.4k | 0.0k | 26 s |
| 3d-print-homage | ok | 100% | 11/11 | 66 | 1 min 52 s | 0.0000 | 13 | 18 | 14.4k | 0.0k | 46 s |
| web-plan-ranking | ok | 75% | 6/8 | 37 | 2 min 44 s | 0.0000 | 14 | 14 | 21.8k | 0.0k | 113 s |
| web-word-universe | ok | 100% | 8/8 | 81 | 2 min 47 s | 0.0000 | 45 | 46 | 20.8k | 0.0k | 18 s |

## Failed checks

- `rs-lock-bug` hidden awards from many threads all count: awards_from_many_threads_all_count failed
- `rs-lock-bug` hidden opposite transfers do not hang: opposite_transfers_do_not_hang failed
- `rs-lock-bug` hidden a transfer to the same player changes nothing: a_transfer_to_the_same_player_changes_nothing failed
- `web-plan-ranking` inflation before and after: expected {'Cruzado': [242.23, 363.41], 'Bresser': [79.66, 980.21], 'Verao': [980.21, 1620.97], 'Collor I': [1972.91, 472.7], 'Collor II': [1620.97, 1119.1]}, received {'Cruzado': [235.65, 228.61], 'Bresser': [27.1, 933.34], 'Verao': [933.34, 1620.66], 'Collor I': [1764.92, 472.26], 'Collor II': [162
- `web-plan-ranking` scores follow the rubric: expected "0.7*drop + 0.3*durability from the row's own numbers", received {'Cruzado': 0.075}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 2); removed duplicate sessions (call 3); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 7)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 6)
- `cmp-handoff`: read the session (call 2); wrote the handoff (call 4); recorded the result (call 9)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 4); recorded the result (call 7)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 7); recorded the result (call 8)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 9)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 13); committed (call 13)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 1); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 3); read the logs (call 1); recorded the result (call 8)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 3); ran the whole suite (call 3)
- `rs-lock-bug`: read the crate (call 2); ran the tests (call 6)
- `sec-leak-fix`: read the service (call 2); read the config (call 2); ran the tests (call 5)
- `hw-stutter-tuning`: read the frame capture (call 4); read the sensor log (call 4); read the settings (call 2); read the owner notes (call 2); recorded the result (call 14)
- `ts-plugin-bug`: read the bus (call 2); ran the tests (call 3)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 4)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 8); recorded the result (call 3)
- `web-plan-ranking`: read the rubric (call 2); not seen: searched the web; opened a source (call 3); recorded the result (call 11); wrote the dossier (call 12)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 6); wrote the page (call 20); looked at it in a browser (call 21); recorded the result (call 6)
