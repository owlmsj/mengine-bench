# mengine-bench 1.3.0: opencode opencode v2.2.2 / zai/glm-5.3-flash (max)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **85.2** | 100.0 | 14/14 | 81.1 | 33.0 | 21 min 44 s | n/a | 1.20M |

- Judge: claude-opus-5-5@xhigh, rubric 2.3
- Config: provider=zai-api; model=GLM 5.3 Flash; quant=full-weights-api; ctx=1M; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T22:01:56Z; bench at 1e46213f80a7; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 88 | 33.2 s | - | 4 | 4 | 0.8k | 0.2k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 80 | 1 min 02 s | - | 6 | 8 | 2.3k | 0.5k | 36 s |
| bo-reconcile | ok | 100% | 4/4 | 66 | 32.0 s | - | 3 | 3 | 1.2k | 1.1k | 18 s |
| cmp-handoff | ok | 100% | 11/11 | 85 | 53.1 s | - | 6 | 4 | 1.4k | 1.0k | 20 s |
| lc-changelog | ok | 100% | 5/5 | 81 | 16.1 s | - | 2 | 1 | 0.3k | 0.2k | - |
| vis-chart | ok | 100% | 4/4 | 78 | 14.4 s | - | 1 | 0 | - | - | - |
| ds-sql-funnel | ok | 100% | 3/3 | 78 | 1 min 20 s | - | 9 | 8 | 2.4k | 1.5k | 12 s |
| gd-astar-doors | ok | 100% | 1/1 | 82 | 25.6 s | - | 4 | 4 | 0.6k | 0.0k | 10 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 92 | 30.0 s | - | 6 | 9 | 0.6k | 0.1k | 19 s |
| ir-studio-wiki | ok | 100% | 6/6 | 77 | 26.7 s | - | 6 | 7 | 0.4k | 0.1k | 13 s |
| ir-server-logs | ok | 100% | 6/6 | 80 | 55.8 s | - | 6 | 6 | 1.5k | 1.2k | 39 s |
| gd-integration-repo | ok | 100% | 8/8 | 91 | 3 min 25 s | - | 10 | 21 | 9.2k | 7.3k | 161 s |
| web-mondrian-landing | ok | 100% | 9/9 | 87 | 4 min 18 s | - | 9 | 8 | 13.8k | 7.8k | 220 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 71 | 6 min 53 s | - | 11 | 21 | 21.1k | 11.5k | 216 s |
