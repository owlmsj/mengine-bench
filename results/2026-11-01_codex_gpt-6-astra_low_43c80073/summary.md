# mengine-bench 1.5.0: codex codex-cli 0.165.0 / gpt-6-astra (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **96.2** | 100.0 | 14/14 | 90.4 | 90.7 | 7 min 19 s | n/a | 1.64M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T14:47:04Z; bench at 71c53d6a44bf; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 89 | 14.8 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 90 | 24.3 s | - | 1 | 3 | 1.6k | 0.1k | - |
| bo-reconcile | ok | 100% | 4/4 | 84 | 13.3 s | - | 1 | 2 | 0.7k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 91 | 13.9 s | - | 2 | 3 | 0.5k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 4.4 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 3.3 s | - | 1 | 0 | 0.0k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 93 | 18.7 s | - | 1 | 3 | 1.1k | 0.0k | - |
| gd-astar-doors | ok | 100% | 5/5 | 94 | 17.8 s | - | 1 | 6 | 1.1k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 98 | 13.2 s | - | 1 | 4 | 0.5k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 88 | 14.1 s | - | 1 | 4 | 0.5k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 84 | 18.9 s | - | 1 | 5 | 0.7k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 96 | 44.8 s | - | 1 | 9 | 2.7k | 0.1k | - |
| web-mondrian-landing | ok | 100% | 11/11 | 86 | 59.0 s | - | 1 | 4 | 4.6k | 0.2k | - |
| 3d-voxel-landscape | ok (stopped after its final event) | 100% | 8/8 | 73 | 2 min 58 s | - | 1 | 15 | 9.8k | 1.7k | - |
