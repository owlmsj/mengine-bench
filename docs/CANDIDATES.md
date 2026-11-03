# Candidates

Tasks written to the bench rules that are not in the catalog. `catalog.all_tasks()` only discovers
`mengine_bench/tasks/`, so nothing here is run, scored or ranked. They came from the evals that lived in the
owlmsj/mengine repo until #127 (`evals/suite`, `evals/cu` at d8344f72) and never entered the public bench.

Promoting one means: move its `EvalTask` into a module under `mengine_bench/tasks/`, add the id to
`TASKS_THAT_CAME_AND_WENT` in `leaderboard.py`, probe it with Opus 5.5 xhigh as agent and judge
(CONTRIBUTING.md), regenerate README and docs/TASKS.md with `tasks-doc`, and release a new minor or major.
The owner picks; adding tasks makes every run longer.

Each candidate has a reference solution that `tests/test_candidates_*.py` proves passes, and an untouched
workspace fails. Agent time is not measured for any of them; the number below is the limit set.

| id | module | adds over the catalog (closest task) | limit | saturation risk | diagnosing a failure by hand |
| --- | --- | --- | --- | --- | --- |
| `bo-safe-conversion` | `hard_context` | Circular dilution: SAFE conversion with a pool increase in the pre-money (`bo-pnl-runway`) | 3 min | Medium: fixed financial inputs | Recompute conversion prices, pool shares and founder ownership from the term sheet in `rodada/` |
| `gd-lockstep-desync` | `hard_context` | Cross-process replay determinism (`gd-integration-repo`) | 5 min | Medium: familiar RNG and ordering defects | Compare replay hashes across hash seeds, then RNG ownership and action order against RULES.md |
| `lc-contract` | `hard_context` | Price precedence across a long contract and its annexes (`doc-lab-pdf`) | 3 min | High: searchable document with fixed terms | Read clause 7, the volume and prepayment discounts and signed annex C; recompute the annual quote |
| `cmp-meeting-decisions` | `compaction_web` | Decisions, owners, deadlines and a conditional hire carried to a fresh session (`cmp-handoff`) | 3 min per step | High | Compare the meeting's decision turns with `DECISIONS.md` and `result.json` |
| `cmp-agent-trajectory` | `compaction_web` | Current state rebuilt from a chronological tool-event log (`cmp-handoff`) | 3 min per step | Medium to high | Read events 96, 150 and 157-159, then compare `STATE.md` and `result.json` |

## Not ported

- `ir-web-facts` (web retrieval with historical anchors): its facts name companies and people, which
  CONTRIBUTING.md excludes, and `web-plan-ranking` is already the one web task. Rewriting it means new
  facts (for example public computing history), so it waits for the owner.
- `tier_s` parity runner (`evals/tier_s/run.py`): it ran the old suite on Claude Code and OpenCode side by side.
  `mengine-bench run` does that job now, so it was retired, not ported.
- The other suite tasks are either in the catalog already (`bo-pnl-runway`, `bo-reconcile`, `cmp-handoff`,
  `ds-ab-playtest`, `ds-sql-funnel`, `gd-integration-repo`, `ir-server-logs`, `web-mondrian-landing`) or were
  retired by the owner as saturated (see `TASKS_THAT_CAME_AND_WENT`).

## Proposal: offline computer use (`cu`)

The mengine `cu` eval (B1-B5) drove a real Bluesky test account: post with an image and alt text, reply,
delete. That does not fit the bench: it needs an account, it writes to a public network and it cannot be
re-run identically. Proposal, no code yet:

- A local, fictional social page served from the workspace, driven only by the harness's own browser.
- Steps: upload an image with alt text, post, reply to a given post, delete the agent's own post, leave the
  others untouched.
- Grading reads the page's saved state plus an append-only event journal: exact text, image hash,
  parent and child, order of deletion, unrelated posts preserved. The journal tells a finished run from an
  untouched empty feed.
- Open questions for the owner: which harnesses expose a browser in a bench run (Claude Code since bench#101;
  the others are unknown), and whether a harness without one scores zero or the task is skipped for it.

## Proposals

git lost-work variant of `git-merge-conflict`: the feature commit lives only on a detached HEAD (Terminal-Bench
`fix-git`), so the agent must find it in the reflog before merging; hardens the existing task without making it
longer (#151).
