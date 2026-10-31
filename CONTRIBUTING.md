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

Keep tasks moderate: one clear job, solvable by a good agent in a few minutes.

**Gold self-test rule.** Every task has a hermetic test in `tests/` (no network,
no model) proving the reference **passes** and the untouched folder **fails**;
when you fix a lenient check, add the wrong answer that used to pass. Then
regenerate the tables and run everything:

```
uv run mengine-bench tasks-doc --write    # docs/TASKS.md
uv run mengine-bench tasks-doc --readme   # README task table
uv run pytest -q
```

Adding, removing or changing a task, prompt or check is a new bench minor
version (1.3.0): runs of different minor versions are never ranked together.

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
