# mengine-bench 1.0.0: opencode opencode v2.2.2 / ds41/deepseek-v4.1-flash (default effort)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **71.0** | 71.4 | 10/14 | 70.1 | 69 min 02 s | >= $0.00 (price) | 1.35M |

- Judge: claude-opus-5-5@xhigh, rubric 2.0
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=DeepSeek-V4.1-Flash-1017; runtime=Project Maya v1.1.41; quant=Maya-S; ctx=256k; drafter=DSpark; disk=Engram on SSD, weights on USB SSD; temperature=1.0; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T01:56:48Z; bench at 10413e1bb932; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 90 | 2 min 53 s | 0.0000 |
| bo-pnl-runway | ok | 100% | 11/11 | 86 | 2 min 16 s | 0.0000 |
| bo-reconcile | ok | 0% | 0/4 | 40 | 1 min 45 s | 0.0000 |
| cmp-handoff | ok | 100% | 10/10 | 79 | 2 min 46 s | 0.0000 |
| lc-changelog | ok | 100% | 5/5 | 68 | 1 min 38 s | 0.0000 |
| vis-chart | ok | 100% | 4/4 | 72 | 1 min 05 s | 0.0000 |
| ds-sql-funnel | ok | 100% | 3/3 | 72 | 2 min 21 s | 0.0000 |
| gd-astar-doors | ok | 100% | 1/1 | 85 | 2 min 03 s | 0.0000 |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 86 | 1 min 33 s | 0.0000 |
| ir-studio-wiki | ok | 100% | 6/6 | 87 | 1 min 54 s | 0.0000 |
| ir-server-logs | ok | 100% | 6/6 | 91 | 3 min 49 s | 0.0000 |
| gd-integration-repo | timeout (timeout) | 0% | 7/7 | 60 | 15 min 00 s | 0.0000 |
| web-mondrian-landing | timeout (timeout) | 0% | 9/9 | 66 | 15 min 00 s | 0.0000 |
| 3d-voxel-landscape | timeout (timeout) | 0% | 1/6 | 0 | 15 min 00 s | 0.0000 |
