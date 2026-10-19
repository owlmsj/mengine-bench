# Contributing

Two kinds of contribution: new tasks and benchmark results. Both land by pull
request. Development uses uv only (`uv sync`, `uv run pytest -q`).

## Adding a task

A task is a module in `mengine_bench/tasks/` that exposes
`TASKS: list[EvalTask]`. The catalog discovers it automatically. A task has:

1. **Fixture**: `setup(ws)` writes the starting workspace (code, data, docs).
   It must be deterministic and offline.
2. **Prompt(s)**: one or more `Step`s, in English. Use `fresh_session`,
   `hide` and `compact_before` for multi-session tasks (see `core.py`).
3. **Reference solution**: `reference(ws)` applies a correct solution to the
   workspace and returns the final answer text(s) a correct agent would give.
4. **Checks**: `check(ws, answers)` returns a `CheckResult`. Gold is
   deterministic: executed hidden tests, exact numbers, file state or regex.
   Mark gates (for example "the page rendered") as `mandatory`.
5. **Metadata**: a stable `id`, `category`, `suites` (`fast`, `full`),
   `provenance`, `summary`, `weight` (2 only for HARD/long-horizon tasks) and
   `par_s` (par time in seconds, with its source in `docs/TASKS.md`).

### Gold self-test rule

Every task must have a self-test in `tests/` proving both directions:

- the reference solution **passes** the checks, and
- the untouched workspace **fails** them.

Tests are hermetic: no network, no model calls. A task without a passing
gold self-test is not merged. Regenerate `docs/TASKS.md` in the same PR with
`uv run mengine-bench tasks-doc --write` (a test fails when it drifts).

### Content rules

No personal data, company names, secrets, tokens or absolute local paths in
tasks or fixtures. Use neutral fictional names (Alice, Bruno, Carla...) and
public topics.

## How contributions land

`main` is the only branch and nobody pushes to it directly, the maintainer
included: every change, results or code, is a pull request that the
maintainer reviews and merges with a merge commit. There is no CI and no bot.
Questions and bug reports go in issues.

Results: see "Submitting results" in the [README](README.md). One PR adds one
`results/<suite>/<bundle>/` directory and nothing else.

## Maintainer: merging a result PR

```
gh pr checkout <n>
git diff --stat main...HEAD          # only new files in one results/<suite>/<bundle>/
uv run mengine-bench leaderboard     # rewrites LEADERBOARD.md
git commit -m "leaderboard: rank <bundle>" -- LEADERBOARD.md
git push                             # lands on the contributor's PR branch
gh pr merge <n> --merge
```

Before merging, the bundle is public once merged:

- `summary.md` says `Preflight: clean` (otherwise the run stays unranked, so
  ask why);
- skim the transcripts for personal data the redaction cannot know (names,
  companies, private projects) and for an agent reading outside its
  workspace or looking up this repo's gold; reject or ask for a rerun.

 `git push` to the contributor's branch works when the PR
allows edits by maintainers (the default for forks owned by a user); if it
does not, merge first and land the LEADERBOARD.md commit in a PR of your own.
