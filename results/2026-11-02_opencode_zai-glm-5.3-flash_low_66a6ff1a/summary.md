# mengine-bench 1.7.3: opencode opencode v2.2.2 / zai/glm-5.3-flash (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **79.2** | 97.7 | 13/15 | 73.9 | 14.4 | 26 min 24 s | >= $0.07 (harness) | 1.05M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T06:43:19Z; bench at 060d984b322e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 78 | 51.0 s | 0.0083 | 5 | 5 | 0.6k | 0.1k | 27 s |
| bo-pnl-runway | ok | 100% | 5/5 | 50 | 1 min 28 s | 0.0038 | 6 | 9 | 2.1k | 0.3k | 67 s |
| bo-reconcile | ok | 100% | 4/4 | 60 | 45.2 s | 0.0021 | 4 | 3 | 0.6k | 0.4k | 23 s |
| cmp-handoff | ok | 91% | 10/11 | 69 | 1 min 41 s | 0.0048 | 9 | 8 | 1.5k | 0.5k | 34 s |
| lc-changelog | ok | 100% | 5/5 | 100 | 21.0 s | 0.0052 | 2 | 1 | 0.1k | 0.1k | 3 s |
| vis-chart | ok | 100% | 4/4 | 97 | 21.2 s | 0.0005 | 2 | 1 | 0.2k | 0.1k | 5 s |
| ds-sql-funnel | ok | 100% | 3/3 | 67 | 1 min 28 s | 0.0023 | 7 | 8 | 1.3k | 0.1k | 43 s |
| ue-packaged-bug | ok | 100% | 5/5 | 76 | 1 min 10 s | 0.0025 | 5 | 8 | 0.9k | 0.2k | 27 s |
| ir-studio-wiki | ok | 100% | 6/6 | 84 | 37.5 s | 0.0022 | 5 | 7 | 0.2k | 0.0k | 21 s |
| ir-server-logs | ok | 100% | 6/6 | 73 | 51.8 s | 0.0029 | 6 | 6 | 0.5k | 0.1k | 28 s |
| gd-integration-repo | ok | 100% | 8/8 | 82 | 2 min 09 s | 0.0072 | 11 | 20 | 2.4k | 1.3k | 58 s |
| rs-lock-bug | ok | 100% | 6/6 | 88 | 1 min 14 s | 0.0031 | 7 | 6 | 1.3k | 0.3k | 34 s |
| web-mondrian-landing | ok | 100% | 10/10 | 78 | 2 min 51 s | 0.0108 | 16 | 15 | 3.7k | 0.3k | 65 s |
| 3d-voxel-landscape | ok | 100% | 7/7 | 59 | 4 min 34 s | 0.0131 | 18 | 17 | 7.4k | 1.9k | 108 s |
| web-word-universe | timeout (timeout) | 75% | 6/8 | 48 | 6 min 00 s | - | 29 | 28 | 9.4k | 1.7k | 47 s |

## Failed checks

- `cmp-handoff` answer measure_command: expected 'a match for ^(?!.*-Ctx[\\s:=]+1024\\b)(?!.*-NPredict[\\s:=]+131072\\b)(?=.*\\bmeasure_decode\\.ps1\\b)(?=.*\\b131072\\b)(?=.*\\b1024\\b)', received 'llama-server --no-mmproj-offload -ub 512 ... (HANDOFF.md records only the flags, not a verbatim command; decode was measured as median of 3 a
- `web-word-universe` collected exactly the site's words: missing 0 (none), extra 3 (contato, dicionário criativo, sobre)
- `web-word-universe` result.json has the right words, relations and most_connected: expected {'words': 250, 'relations': 743, 'most_connected': ['palavra', 'tempo']}, received {'words': 253, 'relations': 743, 'most_connected': [['palavra', 16], ['tempo', 16], ['advogado', 9], ['madrugada', 9], ['crepúsculo', 8]]}

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 5); recorded the result (call 5)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 8)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 3)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 8)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 1)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 3); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 8)
- `ir-studio-wiki`: followed the bug (call 1); checked the approvals (call 1); read the postmortem (call 1); recorded the result (call 7)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 1); ran the whole suite (call 2)
- `rs-lock-bug`: read the crate (call 4); ran the tests (call 5)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 3); looked at it in a browser (call 2)
- `3d-voxel-landscape`: wrote the scene (call 1); looked at it in a browser (call 2)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 5); wrote the page (call 18); looked at it in a browser (call 19); recorded the result (call 5)
