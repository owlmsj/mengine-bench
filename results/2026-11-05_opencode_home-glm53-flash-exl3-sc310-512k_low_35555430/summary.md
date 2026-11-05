# mengine-bench 2.6.0: opencode opencode v2.2.5 / home/glm53-flash-exl3-sc310-512k (low)

| Score | Correct % | Solved | Judge | Speed | Time | Cost | Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **92.7** | 100.0 | 6/7 | 80.6 | 90.1 | 7 min 28 s | $0.00 (price) | 0.40M |

- Judge: claude-opus-5-5@xhigh, rubric 2.6
- Config: provider=local; server_gpu=2x RTX 5090 + 2x RTX 4090; server_cpu=i9-14900KF; server_ram=128 GB DDR4; model=GLM-5.3-Flash; runtime=exllamav3 0c325eff + TabbyAPI 8f92fac5; quant=turboderp-sc_3.10bpw; ctx=512k; cache=Q8, 100 experts on CPU; drafter=MTP n5 dynamic; role=advisor; disk=Linux SSD; tier=2; temperature=1.0; personal_instructions=~/.config/opencode/AGENTS.md
- Machine: Windows 11, AMD Ryzen 9 8945HS w/ Radeon 780M Graphics (16 threads), 31.3 GB RAM, GPU NVIDIA GeForce RTX 4070 Laptop GPU (8 GB)
- Run: 2026-11-05, started 2026-11-05T17:02:13Z; bench at f343274bbb4f; submitter owlmsj

| task | status | correct | checks | judge | time | cost (USD) | turns | tools | tool s | generated | thinking | first write |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ds-ab-playtest | ok | 100% | 5/5 | 76 | 1 min 20 s | 0.0000 | 9 | 9 | 0.3 | 1.8k | 0.0k | 55 s |
| bo-reconcile | ok | 100% | 5/5 | 78 | 38.2 s | 0.0000 | 5 | 4 | 0.3 | 0.8k | 0.0k | 21 s |
| cmp-handoff | ok | 100% | 12/12 | 86 | 1 min 21 s | 0.0000 | 12 | 12 | 0.1 | 2.1k | 0.0k | 20 s |
| git-merge-conflict | ok | 100% | 7/7 | 85 | 1 min 13 s | 0.0000 | 12 | 12 | 0.2 | 1.3k | 0.0k | 35 s |
| infra-gpu-fit | ok | 100% | 7/7 | 84 | 35.6 s | 0.0000 | 4 | 5 | 0.0 | 0.7k | 0.0k | 16 s |
| hw-stutter-tuning | timeout (timeout) | 100% | 7/7 | 63 | 1 min 30 s | 0.0000 | 7 | 8 | 0.2 | 1.6k | 0.0k | 72 s |
| ts-plugin-bug | ok | 100% | 8/8 | 92 | 50.5 s | 0.0000 | 8 | 9 | 0.0 | 0.9k | 0.0k | 19 s |

## Checkpoints

Key actions found in the tool calls. Diagnosis only: they change no grade, and "not seen" can be a different route.

- `ds-ab-playtest`: read the notes (call 2); read the data (call 3); removed duplicate sessions (call 4); tested significance (call 4); recorded the result (call 9)
- `bo-reconcile`: read the notes (call 2); read the invoices (call 2); read the statement (call 2); recorded the result (call 4)
- `cmp-handoff`: read the session (call 1); wrote the handoff (call 4); recorded the result (call 12)
- `git-merge-conflict`: merged the branch (call 2); ran the tests (call 10); committed (call 10)
- `infra-gpu-fit`: read the offers (call 3); read the model (call 2); read the policy (call 1); recorded the result (call 5)
- `hw-stutter-tuning`: read the frame capture (call 6); read the sensor log (call 5); read the settings (call 4); read the owner notes (call 3); recorded the result (call 7)
- `ts-plugin-bug`: read the bus (call 3); ran the tests (call 7)
