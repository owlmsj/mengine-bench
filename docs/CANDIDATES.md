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
`run --tasks <id>` runs a candidate for its probe, never ranked (#153).

| id | module | adds over the catalog (closest task) | limit | saturation risk | diagnosing a failure by hand |
| --- | --- | --- | --- | --- | --- |
| `bo-safe-conversion` | `hard_context` | Circular dilution: SAFE conversion with a pool increase in the pre-money (`bo-pnl-runway`) | 3 min | Medium: fixed financial inputs | Recompute conversion prices, pool shares and founder ownership from the term sheet in `rodada/` |
| `gd-lockstep-desync` | `hard_context` | Cross-process replay determinism (`gd-integration-repo`) | 5 min | Medium: familiar RNG and ordering defects | Compare replay hashes across hash seeds, then RNG ownership and action order against RULES.md |
| `lc-contract` | `hard_context` | Price precedence across a long contract and its annexes (`doc-lab-pdf`) | 3 min | High: searchable document with fixed terms | Read clause 7, the volume and prepayment discounts and signed annex C; recompute the annual quote |
| `cmp-meeting-decisions` | `compaction_web` | Decisions, owners, deadlines and a conditional hire carried to a fresh session (`cmp-handoff`) | 3 min per step | High | Compare the meeting's decision turns with `DECISIONS.md` and `result.json` |
| `web-archery-game` | `archery` | An open game brief judged by play (#214): before the vote the judge plays the page, start to game over, and reads the log of the sounds it started (#213) (`web-mondrian-landing`) | 5 min | Low: an open brief graded mostly by play | Open `game/index.html` and play one game: start, pull and shoot, pop a balloon, reach the end, restart; read `judge/<task>-play.json` |
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

## Proposals

Computer use beyond bench 2.3 (#153; `cu-social-cycle`, `cu-webmail`, `web-fact-search`, `file-media-edit` and
`media-voice` are in the catalog):

- `cu-profile-verify`: replicas of profiles on three networks plus a studio site; list the official accounts that
  show at least two ownership signals, with two impostors in the set; graded as exact JSON.
- `cu-video-audit`: a video-site replica; the six newest regular videos (no Shorts, no lives) with views and duration
  from the page's embedded data, plus a vision label per thumbnail; graded per CSV field.

git lost-work variant of `git-merge-conflict`: the feature commit lives only on a detached HEAD (Terminal-Bench
`fix-git`), so the agent must find it in the reflog before merging; hardens the existing task without making it
longer (#151).
