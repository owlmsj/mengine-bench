# mengine-bench 1.1.0: opencode opencode v2.2.2 / zai/glm-5.3 (low)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **87.8** | 95.2 | 13/14 | 70.4 | 7 min 28 s | n/a | 0.94M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: provider=zai-api; model=GLM 5.3; quant=full-weights-api; ctx=1M; tier=1; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T13:32:19Z; bench at a0ad088f706f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 82 | 35.6 s | - | 7 | 7 | 1.2k | 0.1k | 21 s |
| bo-pnl-runway | ok | 100% | 11/11 | 78 | 27.6 s | - | 5 | 6 | 1.3k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 63 | 17.4 s | - | 3 | 3 | 0.4k | 0.3k | 6 s |
| cmp-handoff | ok | 100% | 10/10 | 68 | 20.0 s | - | 5 | 3 | 0.4k | 0.0k | 5 s |
| lc-changelog | ok | 100% | 5/5 | 76 | 5.8 s | - | 1 | 0 | - | - | - |
| vis-chart | ok | 100% | 4/4 | 66 | 25.2 s | - | 3 | 2 | 0.2k | 0.1k | - |
| ds-sql-funnel | ok | 33% | 1/3 | 41 | 24.1 s | - | 6 | 5 | 1.0k | 0.0k | 16 s |
| gd-astar-doors | ok | 100% | 1/1 | 90 | 22.4 s | - | 6 | 6 | 1.1k | 0.1k | 8 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 81 | 39.8 s | - | 12 | 14 | 1.3k | 0.6k | 12 s |
| ir-studio-wiki | ok | 100% | 6/6 | 82 | 19.1 s | - | 6 | 8 | 0.3k | 0.0k | 13 s |
| ir-server-logs | ok | 100% | 6/6 | 70 | 26.4 s | - | 8 | 7 | 0.5k | 0.1k | 20 s |
| gd-integration-repo | ok | 100% | 7/7 | 85 | 48.6 s | - | 12 | 26 | 1.3k | 0.6k | 35 s |
| web-mondrian-landing | ok | 100% | 9/9 | 52 | 47.9 s | - | 3 | 2 | 4.4k | 0.0k | 41 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 52 | 1 min 28 s | - | 7 | 6 | 5.6k | 0.2k | 53 s |
