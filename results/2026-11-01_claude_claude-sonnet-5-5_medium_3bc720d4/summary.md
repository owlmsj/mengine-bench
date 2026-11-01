# mengine-bench 1.5.0: claude 2.1.316 (Claude Code) / claude-sonnet-5-5 (medium)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **95.3** | 100.0 | 14/14 | 81.1 | 100.0 | 4 min 46 s | $1.79 (harness) | 1.81M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T14:57:56Z; bench at 71c53d6a44bf; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 84 | 13.7 s | 0.0914 | 3 | 3 | 1.1k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 82 | 17.9 s | 0.1006 | 3 | 2 | 1.7k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 63 | 12.7 s | 0.0970 | 3 | 2 | 1.0k | 0.4k | - |
| cmp-handoff | ok | 100% | 11/11 | 67 | 21.9 s | 0.1828 | 5 | 3 | 1.4k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 4.9 s | 0.2176 | 1 | 0 | 0.2k | 0.2k | - |
| vis-chart | ok | 100% | 4/4 | 77 | 4.8 s | 0.0765 | 2 | 1 | 0.2k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 74 | 14.8 s | 0.0997 | 4 | 3 | 1.3k | 0.2k | - |
| gd-astar-doors | ok | 100% | 5/5 | 85 | 17.6 s | 0.0942 | 3 | 4 | 1.3k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 91 | 15.8 s | 0.1015 | 6 | 5 | 0.7k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 91 | 19.4 s | 0.1068 | 6 | 5 | 1.1k | 0.1k | - |
| ir-server-logs | ok | 100% | 6/6 | 71 | 16.5 s | 0.1093 | 5 | 4 | 1.0k | 0.1k | - |
| gd-integration-repo | ok | 100% | 8/8 | 89 | 16.4 s | 0.1131 | 4 | 3 | 1.6k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 91 | 24.9 s | 0.1266 | 3 | 2 | 3.7k | 0.0k | - |
| 3d-voxel-landscape | ok | 100% | 8/8 | 70 | 1 min 25 s | 0.2702 | 3 | 2 | 14.0k | 1.3k | - |
