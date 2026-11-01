# mengine-bench 1.3.4: claude 2.1.316 (Claude Code) / claude-sonnet-5-5 (high)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **95.3** | 100.0 | 14/14 | 83.7 | 95.9 | 6 min 01 s | $2.02 (harness) | 1.96M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=claude-code; tier=0; role=default; personal_instructions=~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-11-01T02:27:29Z; bench at 20e01db73fef; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 86 | 12.7 s | 0.0958 | 3 | 3 | 1.5k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 83 | 17.4 s | 0.1121 | 4 | 3 | 2.1k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 81 | 10.8 s | 0.0991 | 3 | 2 | 1.1k | 0.1k | - |
| cmp-handoff | ok | 100% | 11/11 | 69 | 21.8 s | 0.1873 | 5 | 3 | 1.8k | 0.4k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 4.0 s | 0.2167 | 1 | 0 | 0.2k | 0.1k | - |
| vis-chart | ok | 100% | 4/4 | 86 | 4.2 s | 0.0758 | 2 | 1 | 0.2k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 72 | 13.6 s | 0.1012 | 4 | 3 | 1.5k | 0.2k | - |
| gd-astar-doors | ok | 100% | 1/1 | 84 | 11.6 s | 0.0949 | 3 | 4 | 1.4k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 93 | 13.8 s | 0.1025 | 5 | 4 | 0.8k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 91 | 17.2 s | 0.1144 | 6 | 6 | 1.6k | 0.5k | - |
| ir-server-logs | ok | 100% | 6/6 | 70 | 13.4 s | 0.1106 | 5 | 4 | 1.0k | 0.1k | - |
| gd-integration-repo | ok | 100% | 8/8 | 90 | 17.9 s | 0.1204 | 4 | 3 | 2.1k | 0.2k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 88 | 37.3 s | 0.1696 | 4 | 3 | 6.5k | 0.1k | - |
| 3d-voxel-landscape | ok | 100% | 6/6 | 79 | 2 min 45 s | 0.4216 | 4 | 4 | 24.3k | 11.6k | - |
