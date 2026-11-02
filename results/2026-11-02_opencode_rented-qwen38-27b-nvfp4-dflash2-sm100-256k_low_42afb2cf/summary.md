# mengine-bench 2.0.0: opencode opencode v2.2.5 / rented/qwen38-27b-nvfp4-dflash2-sm100-256k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **81.1** | 98.8 | 17/20 | 84.0 | 37.2 | 20 min 43 s | >= $0.00 (harness) | 4.37M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=3; role=default; provider=nebius spot us-central1; server_gpu=1x B200; model=Qwen3.8-27B; runtime=SGLang 0.5.21; quant=NVFP4; drafter=DFlash2; ctx=256k; rented_usd_h=3.998; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T23:00:07Z; bench at d5cea094f23f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 86 | 28.3 s | 0.0000 | 9 | 9 | 6.5k | 0.0k | 9 s |
| bo-pnl-runway | ok | 100% | 5/5 | 73 | 25.7 s | 0.0000 | 10 | 11 | 7.2k | 0.0k | 20 s |
| bo-reconcile | ok | 100% | 4/4 | 91 | 18.6 s | 0.0000 | 10 | 12 | 5.9k | 0.0k | 6 s |
| cmp-handoff | ok | 91% | 10/11 | 75 | 29.9 s | 0.0000 | 12 | 15 | 8.6k | 0.0k | 7 s |
| cfg-source-drift | ok | 100% | 3/3 | 89 | 15.9 s | 0.0000 | 7 | 16 | 5.1k | 0.0k | 8 s |
| doc-lab-pdf | ok | 100% | 6/6 | 86 | 40.2 s | 0.0000 | 9 | 8 | 14.4k | 0.0k | 33 s |
| ds-sql-funnel | ok | 100% | 3/3 | 91 | 39.9 s | 0.0000 | 17 | 18 | 10.4k | 0.0k | 4 s |
| ue-packaged-bug | ok | 100% | 5/5 | 90 | 24.7 s | 0.0000 | 10 | 17 | 7.0k | 0.0k | 14 s |
| git-merge-conflict | ok | 100% | 6/6 | 97 | 16.6 s | 0.0000 | 8 | 7 | 3.4k | 0.0k | 10 s |
| infra-gpu-fit | ok | 100% | 6/6 | 82 | 9.6 s | 0.0000 | 4 | 5 | 2.8k | 0.0k | 5 s |
| ir-server-logs | ok | 100% | 6/6 | 95 | 20.0 s | 0.0000 | 8 | 11 | 4.7k | 0.0k | 13 s |
| gd-integration-repo | ok | 100% | 8/8 | 92 | 35.2 s | 0.0000 | 16 | 35 | 10.2k | 0.0k | 20 s |
| rs-lock-bug | ok | 100% | 6/6 | 84 | 1 min 44 s | 0.0000 | 23 | 29 | 12.3k | 0.0k | 20 s |
| sec-leak-fix | ok | 86% | 7/8 | 86 | 33.0 s | 0.0000 | 11 | 17 | 8.8k | 0.0k | 13 s |
| hw-stutter-tuning | ok | 100% | 6/6 | 88 | 34.7 s | 0.0000 | 10 | 12 | 9.8k | 0.0k | 8 s |
| ts-plugin-bug | ok | 100% | 7/7 | 97 | 28.2 s | 0.0000 | 14 | 18 | 7.3k | 0.0k | 8 s |
| web-mondrian-landing | ok | 100% | 10/10 | 78 | 1 min 48 s | 0.0000 | 17 | 18 | 24.6k | 0.0k | 47 s |
| 3d-print-homage | ok | 100% | 11/11 | 53 | 2 min 33 s | 0.0000 | 11 | 15 | 40.3k | 0.0k | 43 s |
| web-plan-ranking | ok | 100% | 8/8 | 73 | 1 min 57 s | 0.0000 | 12 | 21 | 28.8k | 0.0k | 96 s |
| web-word-universe | timeout (timeout) | 100% | 8/8 | 73 | 6 min 00 s | - | 57 | 56 | 45.7k | 0.0k | 14 s |

## Failed checks

- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'scripts/start_server.ps1 (local9 block) with --no-mmproj-offload and -ub 512; decode benchmark, median of 3 runs'
- `sec-leak-fix` the old token is out of the final answers: the token literal appears in answer(s) [0]; expected it in none

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 3); read the data (call 2); removed duplicate sessions (call 3); tested significance (call 7); recorded the result (call 7)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 8)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 1); read the statement (call 1); recorded the result (call 6)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 7); recorded the result (call 14)
- `cfg-source-drift`: read the readme (call 1); ran the generator (call 1)
- `doc-lab-pdf`: opened the exams (call 1); extracted the text (call 3); recorded the result (call 6)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 3); excluded test accounts (call 7); recorded the result (call 12)
- `ue-packaged-bug`: read the crash log (call 2); read the game mode (call 3); recorded the result (call 11)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 3); committed (call 7)
- `infra-gpu-fit`: read the offers (call 1); read the model (call 2); read the policy (call 3); recorded the result (call 5)
- `ir-server-logs`: read the notes (call 2); read the logs (call 1); recorded the result (call 9)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 5); ran the whole suite (call 5)
- `rs-lock-bug`: read the crate (call 5); ran the tests (call 12)
- `sec-leak-fix`: read the service (call 1); read the config (call 1); ran the tests (call 4)
- `hw-stutter-tuning`: read the frame capture (call 1); read the sensor log (call 1); read the settings (call 1); read the owner notes (call 1); recorded the result (call 11)
- `ts-plugin-bug`: read the bus (call 4); ran the tests (call 2)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 3)
- `3d-print-homage`: wrote the scene (call 4); looked at it in a browser (call 5); recorded the result (call 3)
- `web-plan-ranking`: read the rubric (call 1); not seen: searched the web; opened a source (call 5); recorded the result (call 18); wrote the dossier (call 17)
- `web-word-universe`: walked the site (call 2); wrote words.json (call 16); wrote the page (call 23); looked at it in a browser (call 28); recorded the result (call 23)
