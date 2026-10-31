# mengine-bench 1.1.0: opencode opencode v2.2.2 / qwen-cloud/qwen3.8-max (max)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **87.0** | 91.4 | 12/14 | 76.9 | 68 min 05 s | n/a | 1.71M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: provider=qwen-cloud-api; model=Qwen3.8 Max; quant=full-weights-api; ctx=1M; tier=1; role=default; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T14:13:13Z; bench at b5ddd3d09d77; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 89 | 2 min 24 s | - | 6 | 6 | 4.0k | 2.1k | 88 s |
| bo-pnl-runway | ok | 100% | 11/11 | 85 | 3 min 39 s | - | 6 | 8 | 7.2k | 5.3k | 132 s |
| bo-reconcile | ok | 100% | 4/4 | 85 | 1 min 57 s | - | 5 | 5 | 4.3k | 3.4k | 75 s |
| cmp-handoff | ok | 100% | 10/10 | 88 | 2 min 13 s | - | 6 | 6 | 3.0k | 2.1k | 74 s |
| lc-changelog | ok | 80% | 4/5 | 58 | 16.0 s | - | 1 | 0 | - | - | - |
| vis-chart | ok | 100% | 4/4 | 72 | 14.2 s | - | 2 | 1 | 0.2k | 0.1k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 84 | 2 min 11 s | - | 9 | 8 | 3.8k | 2.0k | 13 s |
| gd-astar-doors | ok | 100% | 1/1 | 90 | 2 min 38 s | - | 7 | 7 | 4.9k | 3.4k | 122 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 80 | 1 min 05 s | - | 7 | 14 | 1.7k | 0.5k | 41 s |
| ir-studio-wiki | ok | 100% | 6/6 | 91 | 1 min 20 s | - | 7 | 11 | 1.9k | 0.7k | 47 s |
| ir-server-logs | ok | 100% | 6/6 | 90 | 2 min 21 s | - | 10 | 11 | 4.2k | 2.4k | 109 s |
| gd-integration-repo | ok | 100% | 7/7 | 84 | 6 min 48 s | - | 17 | 28 | 11.0k | 8.0k | 282 s |
| web-mondrian-landing | ok | 100% | 9/9 | 81 | 10 min 59 s | - | 13 | 13 | 23.8k | 16.5k | 559 s |
| 3d-voxel-landscape | timeout (timeout) | 0% | 1/6 | 0 | 30 min 00 s | - | 1 | 0 | - | - | - |
