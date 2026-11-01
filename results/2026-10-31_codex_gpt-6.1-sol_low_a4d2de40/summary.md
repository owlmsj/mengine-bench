# mengine-bench 1.3.4: codex codex-cli 0.165.0 / gpt-6.1-sol (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **93.1** | 100.0 | 13/14 | 88.7 | 72.9 | 11 min 47 s | n/a | 1.20M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: harness=codex; tier=0; role=default; service_tier=fast; personal_instructions=~/.codex/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-11-01T01:55:30Z; bench at 20e01db73fef; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 80 | 14.2 s | - | 1 | 2 | 0.9k | 0.0k | - |
| bo-pnl-runway | ok | 100% | 11/11 | 86 | 13.9 s | - | 1 | 2 | 1.0k | 0.0k | - |
| bo-reconcile | ok | 100% | 4/4 | 84 | 12.0 s | - | 1 | 2 | 0.6k | 0.0k | - |
| cmp-handoff | ok | 100% | 11/11 | 91 | 17.3 s | - | 2 | 3 | 0.6k | 0.0k | - |
| lc-changelog | ok | 100% | 5/5 | 100 | 4.5 s | - | 1 | 0 | 0.1k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 100 | 6.4 s | - | 1 | 0 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 86 | 13.4 s | - | 1 | 2 | 0.7k | 0.0k | - |
| gd-astar-doors | ok | 100% | 1/1 | 92 | 16.9 s | - | 1 | 3 | 1.1k | 0.0k | - |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 98 | 14.4 s | - | 1 | 6 | 0.5k | 0.0k | - |
| ir-studio-wiki | ok | 100% | 6/6 | 87 | 12.9 s | - | 1 | 4 | 0.5k | 0.0k | - |
| ir-server-logs | ok | 100% | 6/6 | 85 | 16.9 s | - | 1 | 5 | 0.8k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 97 | 35.2 s | - | 1 | 11 | 2.4k | 0.3k | - |
| web-mondrian-landing | ok | 100% | 9/9 | 81 | 48.8 s | - | 1 | 3 | 4.7k | 0.1k | - |
| 3d-voxel-landscape | timeout (timeout) | 100% | 6/6 | 75 | 8 min 00 s | - | 1 | 15 | 8.2k | 1.3k | - |
