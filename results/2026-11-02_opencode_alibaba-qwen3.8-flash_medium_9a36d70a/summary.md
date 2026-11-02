# mengine-bench 1.7.3: opencode opencode v2.2.2 / alibaba/qwen3.8-flash (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **76.5** | 95.3 | 13/15 | 76.3 | 1.4 | 29 min 39 s | >= $0.10 (harness) | 1.46M |

- Judge: claude-opus-5-5@xhigh, rubric 2.5
- Config: harness=opencode default clean install; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-02, started 2026-11-02T06:08:19Z; bench at 060d984b322e; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 4/4 | 85 | 1 min 06 s | 0.0037 | 9 | 9 | 2.5k | 0.6k | 23 s |
| bo-pnl-runway | ok | 100% | 5/5 | 69 | 1 min 25 s | 0.0055 | 9 | 10 | 3.8k | 0.5k | 25 s |
| bo-reconcile | ok | 100% | 4/4 | 82 | 45.5 s | 0.0034 | 5 | 6 | 1.9k | 1.1k | 26 s |
| cmp-handoff | ok | 100% | 11/11 | 72 | 1 min 45 s | 0.0078 | 16 | 14 | 4.2k | 2.4k | 19 s |
| lc-changelog | ok | 100% | 5/5 | 99 | 25.6 s | 0.0076 | 2 | 1 | 0.3k | 0.2k | 5 s |
| vis-chart | ok | 100% | 4/4 | 97 | 24.6 s | 0.0017 | 3 | 2 | 0.3k | 0.2k | 8 s |
| ds-sql-funnel | ok | 67% | 2/3 | 73 | 1 min 03 s | 0.0035 | 8 | 8 | 2.3k | 1.0k | 7 s |
| ue-packaged-bug | ok | 100% | 5/5 | 75 | 51.1 s | 0.0033 | 5 | 8 | 2.0k | 0.8k | 24 s |
| ir-studio-wiki | ok | 100% | 6/6 | 83 | 1 min 03 s | 0.0042 | 11 | 10 | 2.0k | 1.5k | 49 s |
| ir-server-logs | ok | 100% | 6/6 | 67 | 1 min 33 s | 0.0102 | 7 | 7 | 3.9k | 2.1k | 65 s |
| gd-integration-repo | ok | 100% | 8/8 | 84 | 1 min 48 s | 0.0065 | 9 | 12 | 4.2k | 2.7k | 77 s |
| rs-lock-bug | ok | 100% | 6/6 | 85 | 1 min 40 s | 0.0057 | 10 | 13 | 4.1k | 2.0k | 46 s |
| web-mondrian-landing | ok | 100% | 10/10 | 72 | 4 min 19 s | 0.0179 | 19 | 21 | 12.0k | 5.1k | 64 s |
| 3d-voxel-landscape | ok | 100% | 7/7 | 64 | 5 min 30 s | 0.0234 | 16 | 22 | 19.1k | 10.0k | 151 s |
| web-word-universe | timeout (timeout) | 62% | 5/8 | 37 | 6 min 00 s | - | 24 | 33 | 19.6k | 7.8k | 49 s |

## Failed checks

- `ds-sql-funnel` biggest drop on each platform: expected {'pc': 'purchase', 'steamdeck': 'tutorial_complete'}, received {'pc': {'step': 'purchase', 'conversion': 0.8252, 'from_step': 'first_match', 'players_lost': 57}, 'steamdeck': {'step': 'tutorial_complete', 'conversion': 0.6667, 'from_step': 'install', 'players_lost': 64}}
- `web-word-universe` collected exactly the site's words: missing 52 (aflição, almoço, amanhã, angústia, açougueiro), extra 52 (acougueiro, acucar, aflicao, agua, almoco)
- `web-word-universe` relations of a sample of words: saudade: missing 1 (esperança), extra 1 (esperanca)
- `web-word-universe` opening the page with ?word= shows that word's relations: ?word=saudade does not show its 5 relations, missing esperança

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 1); read the data (call 1); removed duplicate sessions (call 2); tested significance (call 5); recorded the result (call 7)
- `bo-pnl-runway`: read the notes (call 1); read the ledger (call 1); used the chart of accounts (call 1); used the cash balance (call 1); recorded the result (call 9)
- `bo-reconcile`: read the notes (call 1); read the invoices (call 1); read the statement (call 1); recorded the result (call 5)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 3); recorded the result (call 14)
- `lc-changelog`: recorded the result (call 1)
- `vis-chart`: recorded the result (call 2)
- `ds-sql-funnel`: read the rules (call 1); looked at the schema (call 2); excluded test accounts (call 4); recorded the result (call 6)
- `ue-packaged-bug`: read the crash log (call 1); read the game mode (call 1); recorded the result (call 8)
- `ir-studio-wiki`: followed the bug (call 2); checked the approvals (call 2); read the postmortem (call 2); recorded the result (call 10)
- `ir-server-logs`: read the notes (call 1); read the logs (call 1); recorded the result (call 6)
- `gd-integration-repo`: read the docs (call 1); ran the integration test (call 2); ran the whole suite (call 4)
- `rs-lock-bug`: read the crate (call 1); ran the tests (call 8)
- `web-mondrian-landing`: read the fact sheet (call 1); wrote the page (call 2); looked at it in a browser (call 15)
- `3d-voxel-landscape`: wrote the scene (call 1); looked at it in a browser (call 7)
- `web-word-universe`: walked the site (call 1); wrote words.json (call 10); wrote the page (call 16); not seen: looked at it in a browser; recorded the result (call 10)
