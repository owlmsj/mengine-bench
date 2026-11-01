# mengine-bench 1.5.0: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **97.2** | 100.0 | 14/14 | 88.9 | 100.0 | 4 min 46 s | n/a | 1.37M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T13:21:25Z; bench at 69c38ab55bb3; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 89 | 11.2 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 86 | 15.8 s | - | 1 | 2 | 1.3k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 77 | 9.6 s | - | 1 | 2 | 0.5k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 93 | 15.0 s | - | 2 | 3 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 3.3 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 3.4 s | - | 1 | 0 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 91 | 14.3 s | - | 1 | 3 | 0.9k | 0.0k | - |
| gd-astar-doors | ok | 100% | 5/5 | 92 | 17.0 s | - | 1 | 6 | 1.0k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 98 | 13.3 s | - | 1 | 4 | 0.5k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 87 | 14.4 s | - | 1 | 4 | 0.4k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 84 | 12.7 s | - | 1 | 4 | 0.7k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 94 | 37.3 s | - | 1 | 9 | 2.3k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 83 | 45.8 s | - | 1 | 3 | 4.4k | 0.1k | - |
| 3d-voxel-landscape | ok | 100% | 8/8 | 71 | 1 min 13 s | - | 1 | 7 | 5.7k | 0.2k | - |
