# mengine-bench 1.3.1: opencode opencode v2.2.2 / home/qwen38-flash-next-exl3-605-256k (xhigh)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **96.2** | 100.0 | 14/14 | 88.9 | 93.5 | 6 min 38 s | >= $0.00 (price) | 1.18M |

- Judge: claude-opus-5-5@xhigh, rubric 2.4
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4-3600; model=Qwen3.8-Flash-Next; runtime=exllamav3 1.6.4 + TabbyAPI 2fd6cc7; quant=turboderp-6.05bpw; ctx=256k; drafter=MTP n6 dynamic; role=default; disk=Linux SSD; temperature=0.5; personal_instructions=~/.config/opencode/AGENTS.md, ~/.claude/CLAUDE.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-10-31, started 2026-10-31T22:41:29Z; bench at 5f03b429b00f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | generated | reasoning | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 6/6 | 89 | 15.8 s | 0.0000 | 5 | 5 | 1.2k | 0.0k | 5 s |
| bo-pnl-runway | ok | 100% | 11/11 | 83 | 22.9 s | 0.0000 | 6 | 5 | 1.9k | 0.0k | 8 s |
| bo-reconcile | ok | 100% | 4/4 | 90 | 19.8 s | 0.0000 | 8 | 7 | 1.7k | 0.0k | 8 s |
| cmp-handoff | ok | 100% | 11/11 | 81 | 16.9 s | 0.0000 | 7 | 6 | 1.1k | 0.0k | 5 s |
| lc-changelog | ok | 100% | 5/5 | 100 | 12.6 s | 0.0000 | 2 | 1 | 0.2k | 0.0k | - |
| vis-chart | ok | 100% | 4/4 | 92 | 18.3 s | 0.0000 | 6 | 5 | 1.6k | 0.0k | - |
| ds-sql-funnel | ok | 100% | 3/3 | 87 | 21.4 s | 0.0000 | 9 | 8 | 2.2k | 0.0k | 3 s |
| gd-astar-doors | ok | 100% | 1/1 | 94 | 20.6 s | 0.0000 | 8 | 8 | 2.0k | 0.0k | 8 s |
| gd-ecs-collision-bug | ok | 100% | 3/3 | 98 | 13.8 s | 0.0000 | 8 | 11 | 1.2k | 0.0k | 7 s |
| ir-studio-wiki | ok | 100% | 6/6 | 96 | 12.4 s | 0.0000 | 7 | 11 | 0.9k | 0.0k | 7 s |
| ir-server-logs | ok | 100% | 6/6 | 86 | 21.7 s | 0.0000 | 8 | 7 | 1.9k | 0.0k | - |
| gd-integration-repo | ok | 100% | 8/8 | 92 | 1 min 10 s | 0.0000 | 17 | 27 | 5.9k | 0.0k | 28 s |
| web-mondrian-landing | ok | 100% | 9/9 | 79 | 44.7 s | 0.0000 | 11 | 10 | 6.1k | 0.0k | 26 s |
| 3d-voxel-landscape | ok | 100% | 6/6 | 77 | 1 min 28 s | 0.0000 | 6 | 8 | 9.9k | 0.0k | 51 s |
