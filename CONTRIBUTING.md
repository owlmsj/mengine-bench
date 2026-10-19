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

`uv run mengine-bench privacy-scan` checks every tracked file (and the
decompressed contents of result bundles) for home paths, e-mail addresses,
private and tailnet addresses, default Windows host names and token shapes.
It prints file and hit count only and exits non-zero on any hit;
`uv run pytest -q` runs it too (`tests/test_no_personal_data.py`). Build test samples of these shapes at runtime from fragments so
the test sources stay clean.

### Maintainer pre-release step

Names worth protecting cannot be recognized by shape, and a list of them in
a public repo (even hashed) reveals what it protects. Keep them in a local
file, one term per line (a word or a word pair; case and accents are
ignored), outside git. The conventional name `private-terms.txt` is in
`.gitignore`. Before each release run:

```
uv run mengine-bench privacy-scan --private-terms private-terms.txt
```

or set `MENGINE_BENCH_PRIVATE_TERMS` to the file path, which `privacy-scan`
and `uv run pytest` both honor. Private-term hits are waived only on the
README "about" line and the LICENSE copyright line.

## How contributions land

`main` is the only branch and nobody pushes to it directly, the maintainer
included: every change, results or code, is a pull request from a fork (or a
maintainer branch) that the maintainer reviews and merges with a merge
commit. There is no CI, no bot and no GitHub Actions workflow; the checks
below run on the maintainer's machine. Questions and bug reports go in
issues.

## Submitting results

See [docs/SUBMITTING.md](docs/SUBMITTING.md): run a suite, verify the bundle
locally with `uv run mengine-bench verify <bundle>`, and open a PR that adds
exactly one directory under `results/<suite>/`, unedited. Do not edit
LEADERBOARD.md; the maintainer regenerates it.

## Maintainer: reviewing a result PR

Verification executes the submitted workspace code, so run it in a
disposable environment (a throwaway VM or container), never on a machine
with credentials:

```
gh pr checkout <n>
git diff --stat main...HEAD                 # only new files in one results/<suite>/<bundle>/
uv sync --locked
uv run mengine-bench verify results/<suite>/<bundle>
uv run pytest -q                            # includes the privacy scan of the new bundle
uv run mengine-bench leaderboard            # rewrites LEADERBOARD.md
git commit -m "leaderboard: rank <bundle>" -- LEADERBOARD.md
git push                                    # lands on the contributor's PR branch
gh pr merge <n> --merge
```

`git push` to the contributor's branch works when the PR allows edits by
maintainers (the default for forks owned by a user). If it does not, merge
the PR first and land the LEADERBOARD.md commit in a pull request of your
own. Reject a result PR that touches anything outside its bundle directory,
edits an existing bundle, or adds more than one.
