# mengine-bench 1.5.0: opencode opencode v2.2.2 / home/qwen38-flash-next-exl3-605-256k (xhigh)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **96.3** | 100.0 | 14/14 | 89.5 | 93.1 | 6 min 43 s | >= $0.00 (price) | 1.22M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; temperature=0.5; tier=2; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-01, started 2026-11-01T14:25:36Z; bench at c03f1d9ce9cd; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 88 | 13.8 s | 0.0000 | 5 | 5 | 1.2k | 0.0k | 5 s |
| bo-pnl-runway | ok | 100% | 11/11 | 89 | 35.9 s | 0.0000 | 10 | 9 | 3.5k | 0.0k | 17 s |
| bo-reconcile | ok | 100% | 4/4 | 86 | 23.1 s | 0.0000 | 8 | 9 | 2.3k | 0.0k | 6 s |
| cmp-handoff | ok | 100% | 11/11 | 84 | 25.9 s | 0.0000 | 9 | 8 | 2.0k | 0.0k | 7 s |
| lc-changelog | ok | 100% | 5/5 | 100 | 15.2 s | 0.0000 | 2 | 1 | 0.6k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 96 | 14.0 s | 0.0000 | 5 | 4 | 1.5k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 86 | 20.8 s | 0.0000 | 8 | 7 | 2.1k | 0.0k | 5 s |
| gd-astar-doors | ok | 100% | 5/5 | 88 | 20.7 s | 0.0000 | 6 | 6 | 1.3k | 0.0k | 6 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 99 | 12.7 s | 0.0000 | 9 | 8 | 0.7k | 0.0k | 6 s |
| ir-studio-wiki | ok | 100% | 6/6 | 90 | 20.3 s | 0.0000 | 9 | 8 | 1.4k | 0.0k | 12 s |
| ir-server-logs | ok | 100% | 6/6 | 93 | 25.7 s | 0.0000 | 11 | 10 | 2.0k | 0.0k | 17 s |
| gd-integration-repo | ok | 100% | 8/8 | 92 | 44.3 s | 0.0000 | 12 | 23 | 4.8k | 0.0k | 30 s |
| web-mondrian-landing | ok | 100% | 11/11 | 84 | 53.8 s | 0.0000 | 11 | 12 | 6.7k | 0.0k | 30 s |
| 3d-voxel-landscape | ok | 100% | 8/8 | 78 | 1 min 17 s | 0.0000 | 7 | 9 | 9.9k | 0.0k | 54 s |
