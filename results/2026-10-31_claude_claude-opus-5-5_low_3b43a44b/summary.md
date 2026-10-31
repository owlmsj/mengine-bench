# mengine-bench 1.1.0: claude 2.1.316 (Claude Code) / claude-opus-5-5 (low)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **95.7** | 100.0 | 14/14 | 85.7 | 13 min 21 s | $5.15 (harness) | 2.50M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T17:36:26Z; bench at 53bb6f00db9b; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 86 | 21.7 s | 0.2134 | 8 | 4 | 0.1k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 90 | 22.5 s | 0.2514 | 6 | 3 | 0.1k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 85 | 16.8 s | 0.2095 | 5 | 3 | 0.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 10/10 | 88 | 23.7 s | 0.3805 | 7 | 4 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 72 | 2.7 s | 0.4245 | 1 | 0 | 0.0k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 75 | 4.2 s | 0.1406 | 2 | 1 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 89 | 18.3 s | 0.2043 | 4 | 2 | 0.2k | 0.0k | - |
| gd-astar-doors | ok | 100% | 1/1 | 89 | 19.9 s | 0.2079 | 8 | 6 | 0.2k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 91 | 13.0 s | 0.2032 | 10 | 9 | 0.3k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 84 | 18.4 s | 0.2319 | 15 | 13 | 0.2k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 91 | 25.6 s | 0.2440 | 7 | 4 | 0.9k | 0.0k | - |
| gd-integration-repo | ok | 100% | 7/7 | 87 | 2 min 48 s | 0.3950 | 13 | 7 | 0.1k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 88 | 2 min 04 s | 0.7929 | 41 | 34 | 0.9k | 0.0k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 85 | 5 min 22 s | 1.2502 | 28 | 18 | 0.2k | 0.0k | - |
