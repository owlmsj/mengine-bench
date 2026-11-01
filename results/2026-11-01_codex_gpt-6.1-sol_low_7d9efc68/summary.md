# mengine-bench 1.4.0: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **97.2** | 100.0 | 14/14 | 89.0 | 100.0 | 4 min 04 s | n/a | 0.91M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=codex default clean install; service_tier=fast; personal_instructions=none
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T12:47:46Z; bench at d68a55e8bebe; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 87 | 11.3 s | - | 1 | 2 | 0.7k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 84 | 11.8 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 83 | 9.4 s | - | 1 | 2 | 0.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 92 | 15.1 s | - | 2 | 3 | 0.5k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 4.2 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 3.1 s | - | 1 | 0 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 82 | 10.8 s | - | 1 | 2 | 0.7k | 0.0k | - |
| gd-astar-doors | ok | 100% | 5/5 | 94 | 11.8 s | - | 1 | 3 | 0.7k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 100 | 10.8 s | - | 1 | 4 | 0.4k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 87 | 10.4 s | - | 1 | 3 | 0.4k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 87 | 14.6 s | - | 1 | 5 | 0.6k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 95 | 30.5 s | - | 1 | 9 | 1.9k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 83 | 44.2 s | - | 1 | 3 | 4.5k | 0.0k | - |
| 3d-voxel-landscape | ok | 100% | 8/8 | 72 | 56.0 s | - | 1 | 3 | 5.0k | 0.0k | - |
