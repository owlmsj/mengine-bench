# mengine-bench 1.1.0: claude 2.1.316 (Claude Code) / claude-sonnet-5-5 (medium)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **93.1** | 100.0 | 14/14 | 76.9 | 6 min 56 s | $2.03 (harness) | 1.80M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T17:53:06Z; bench at cdab20642f43; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 81 | 13.5 s | 0.0949 | 5 | 3 | 0.3k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 76 | 15.7 s | 0.1035 | 6 | 3 | 0.8k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 80 | 12.1 s | 0.0950 | 4 | 2 | 0.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 10/10 | 69 | 19.7 s | 0.1813 | 6 | 3 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 73 | 4.9 s | 0.2134 | 2 | 0 | 0.0k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 74 | 5.1 s | 0.0699 | 2 | 1 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 75 | 14.2 s | 0.0934 | 6 | 3 | 0.2k | 0.0k | - |
| gd-astar-doors | ok | 100% | 1/1 | 78 | 10.7 s | 0.0884 | 5 | 4 | 0.2k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 85 | 12.1 s | 0.0940 | 6 | 4 | 0.3k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 81 | 10.2 s | 0.0926 | 5 | 3 | 0.4k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 86 | 14.1 s | 0.1089 | 7 | 5 | 0.6k | 0.0k | - |
| gd-integration-repo | ok | 100% | 7/7 | 70 | 17.5 s | 0.1159 | 7 | 4 | 0.6k | 0.0k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 84 | 25.4 s | 0.1311 | 3 | 2 | 0.3k | 0.0k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 65 | 4 min 00 s | 0.5527 | 5 | 2 | 0.6k | 0.0k | - |
