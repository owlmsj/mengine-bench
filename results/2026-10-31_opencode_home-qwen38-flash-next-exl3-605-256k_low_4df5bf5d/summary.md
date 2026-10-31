# mengine-bench 1.1.0: opencode opencode v2.2.2 / home/qwen38-flash-next-exl3-605-256k (low)

| Score | Correct % | Solved | Judge | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| **94.6** | 100.0 | 14/14 | 81.9 | 7 min 59 s | >= $0.00 (price) | 2.01M |

- Judge: claude-opus-5-5@xhigh, rubric 2.1
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; temperature=0.5; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T15:48:34Z; bench at cbeee4573585; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 87 | 14.0 s | 0.0000 | 5 | 5 | 1.3k | 0.0k | 6 s |
| bo-pnl-runway | ok | 100% | 11/11 | 86 | 28.3 s | 0.0000 | 8 | 7 | 2.7k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 4/4 | 84 | 24.6 s | 0.0000 | 5 | 5 | 3.1k | 0.0k | 16 s |
| cmp-handoff | ok | 100% | 10/10 | 78 | 23.0 s | 0.0000 | 8 | 8 | 1.9k | 0.0k | 8 s |
| lc-changelog | ok | 100% | 5/5 | 80 | 14.7 s | 0.0000 | 2 | 1 | 0.5k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 82 | 3.4 s | 0.0000 | 2 | 1 | 0.1k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 78 | 25.5 s | 0.0000 | 15 | 14 | 2.5k | 0.0k | 2 s |
| gd-astar-doors | ok | 100% | 1/1 | 79 | 15.9 s | 0.0000 | 7 | 7 | 1.6k | 0.0k | 5 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 88 | 11.8 s | 0.0000 | 6 | 11 | 0.8k | 0.0k | 7 s |
| ir-studio-wiki | ok | 100% | 6/6 | 89 | 14.8 s | 0.0000 | 7 | 11 | 1.2k | 0.0k | 9 s |
| ir-server-logs | ok | 100% | 6/6 | 73 | 49.9 s | 0.0000 | 7 | 10 | 2.5k | 0.0k | 39 s |
| gd-integration-repo | ok | 100% | 7/7 | 90 | 1 min 22 s | 0.0000 | 17 | 28 | 8.8k | 0.0k | 69 s |
| web-mondrian-landing | ok | 100% | 9/9 | 82 | 53.5 s | 0.0000 | 14 | 13 | 7.0k | 0.0k | 26 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 70 | 1 min 58 s | 0.0000 | 8 | 11 | 16.1k | 0.0k | 96 s |
