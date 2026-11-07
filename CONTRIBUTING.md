# Contributing

Two kinds of contribution, both by pull request: **results** (a run of your
agent) and **tasks**. Development uses uv only (`uv sync`, `uv run pytest -q`).
`main` takes pull requests only, merged with a merge commit; there is no CI and
no bot. Questions and bug reports go in issues.

## Submitting a result

Run the bench (README, "Run it") and submit with `run --submit` or
`uv run mengine-bench submit results/<run>`. The pull request adds one
`results/<run>/` folder written by `mengine-bench run`, not edited by hand, and
nothing else. Describe your setup with `--config key=value` so others can
compare: harness, model and effort are recorded automatically; provider,
server hardware, quantization, context size, MCP servers and skills are not.

## Adding a task

A task is an `EvalTask` in a module of `mengine_bench/tasks/` listed in its
`TASKS` list; the catalog finds it automatically. It has:

1. **Fixture**: `setup(ws)` writes the starting folder. Deterministic and offline.
2. **Prompt(s)**: one or more `Step`s in English. A second step must be a
   `fresh_session` (new agent process) and names the files it keeps in `carry`.
3. **Reference solution**: `reference(ws)` solves the task and returns the
   answer text(s) a correct agent would give.
4. **Checks**: `check(ws, answers)` returns a `CheckResult`. Scored checks map
   to requirements the agent delivers (hidden tests, exact numbers, file state).
   Integrity rules such as "existing tests untouched" are `mandatory` gates:
   they never earn points, and a failed gate scores the task 0.
5. **Metadata**: a stable `id`, a `category`, a one-sentence beginner `summary`
   (the README TL;DR), `provenance`, `timeout_s`, and `deliverables` for files
   the judge must see verbatim (for example a page it renders).

Keep tasks basic: one clear job, easy to understand and to diagnose by hand, that a top agent finishes in under a
minute. The prompt is an open brief: the context, the problem and the outcome wanted, never the method or the cause.
Harden a task by removing hints and splitting checks, not by making the job longer or harder, and keep traps few.

**Inputs.** Fixtures are offline. A task that needs the web says so in its prompt (only `web-plan-ranking` today),
and its checks stay offline. A toolchain beyond Python (cargo, node, git) goes in the README's task section. Images
and other assets are public domain or your own, credited in the README.

**Probe with the judge model.** Before the pull request, run the new task once with Claude Opus 5.5 xhigh and judge
that bundle; a run with `--tasks` is never ranked:

```
uv run mengine-bench run --agent claude --model claude-opus-5-5 --effort xhigh --tasks <id> --out tmp/probe
uv run mengine-bench judge tmp/probe/<run>
```

Say in the pull request if Opus refused or failed, as agent or as judge: the maintainer then picks another harness
and model for that task. A failure that is the check's fault (a valid route scored 0) is fixed with a test. A visual
task also needs its judge reference, `mengine_bench/assets/references/<id>.png`: the page Opus 5.5 xhigh made in
that probe, rendered with `mengine_bench.visual.render_headless` at 8 s.

**Gold self-test rule.** Every task has a hermetic test in `tests/` (no network,
no model) proving the reference **passes** and the untouched folder **fails**;
when you fix a lenient check, add the wrong answer that used to pass. Then
regenerate the tables and run everything:

```
uv run mengine-bench tasks-doc --write    # docs/TASKS.md
uv run mengine-bench tasks-doc --readme   # README task table
uv run pytest -q
```

Consulting the reference, the hidden tests or a published answer, from this repo or the web, gets a run
rejected on transcript review.

Adding, removing or changing a task, prompt or check is a new bench minor
version (1.7.0), and a new catalog is a major one (2.0.0). The ranking stays alive across minors (owner, 2026-11-07,
#218): a new minor adds its version to `RANKED_WITH_CURRENT` with every version already ranked, and each row shows
its bench version and date; it is never wiped. Only an explicit owner decision moves runs to history (#187). Add every id that came or went to
`TASKS_THAT_CAME_AND_WENT` in `mengine_bench/leaderboard.py`, or the older
complete runs drop out of the leaderboard history.

**Content rules.** No personal data, company names, secrets, tokens or absolute
local paths in tasks or fixtures. Use neutral fictional names and public topics.

## Maintainer: reviewing a result

```
gh pr checkout <n>
git diff --stat main...HEAD                    # only new files in one results/<run>/
uv run mengine-bench judge results/<run>       # Claude Opus 5.5 xhigh, one vote per task
uv run mengine-bench leaderboard               # rewrites LEADERBOARD.md
git add results/<run> LEADERBOARD.md          # result.json, summary.md, judge screenshots
git commit -m "judge and rank <run>"
git push                                       # lands on the contributor's PR branch
gh pr merge <n> --merge
```

Before merging (the folder is public once merged), skim `summary.md` and the
transcripts for personal data the redaction cannot know (names, companies,
private projects) and for an agent reading outside its folder or looking up
this repo's answers; reject or ask for a rerun.

`judge` runs once per run folder (it refuses a judged one) through your `claude`
login, so it uses your Claude plan, not API credits, as long as no
`ANTHROPIC_API_KEY` is set. For the visual tasks it renders the stored page with
a local Chromium-family browser (Edge, Chrome or Chromium, or
`MENGINE_BENCH_BROWSER`); never run it as root. If `git push` to the
contributor's branch is refused (the PR does not allow maintainer edits), merge
first and land the LEADERBOARD.md commit in a pull request of your own.

## Maintainer: releasing a bench version

Fixes are cheap and runs are not, so versions ship in trains, not per fix (#185). There is no CI by decision (#11):
the checklist below is the gate, run by the maintainer on the release branch.

- **Cadence.** At most one minor per week. Between trains `main` stays releasable and carries no version bump; the
  bump is one pull request whose body holds this checklist with its outputs.
- **Patch** (2.6.x): grader or runner fixes that change no task, prompt or limit. Published runs that kept their
  workspaces are regraded with `mengine-bench regrade results/<run>`, never run again.
- **Minor** (2.7.0): a task, prompt, limit, check, rubric or Score formula change (#210). The catalog changes only on a train, and a
  candidate waits in `docs/CANDIDATES.md` until then.
- **Checklist**, in order, every output quoted in the PR:
  1. `uv run pytest -q` green on the release branch (load-sensitive tests run alone when the host is busy).
  2. Rubric or judge input changed: `mengine-bench judge-calibrate` against the owner's audit votes, mean and count
     beyond 8 points not worse than the recorded baseline; then `RUBRIC_VERSION` bumped.
  3. bench-audit (`.claude/skills/bench-audit`) on two published runs with the release's checks.
  4. One validation run per harness family (Claude Code, Codex, opencode) on the release branch, kept as an
     observation, never ranked.
  5. Ranked runs regraded (patch) or re-judged once (rubric change), `mengine-bench leaderboard` regenerated,
     the SCORING.md paragraph for the version written, `tasks-doc` regenerated when a task moved.
