## What this PR does

<!-- One of: adds a result bundle / adds or changes a task / other. -->

## Result checklist

Skip this section if the PR does not add results.

- [ ] Adds exactly one bundle directory under `results/<suite>/`, written by `mengine-bench run` and not edited by hand
- [ ] Touches nothing else (no code, docs or LEADERBOARD.md)
- [ ] The run started clean (`summary.md`: `Preflight: clean`) and ended with `privacy check: clean`
- [ ] I read summary.md and the transcripts: no secrets, tokens or personal data

| field | value |
| --- | --- |
| suite | |
| agent CLI and version | |
| model id | |
| effort | |
| judge model, effort and votes (or "none") | |
| OBJECTIVE / ACCURACY / solved | |
| bench version and commit | |

## Task checklist

Skip this section if the PR does not add or change tasks. See CONTRIBUTING.md.

- [ ] Fixture, English prompt(s), reference solution and deterministic checks
- [ ] Gold self-test: the reference passes and the untouched workspace fails
- [ ] `uv run mengine-bench tasks-doc --write` and `uv run pytest -q` pass
- [ ] No personal data, company names, secrets or absolute local paths
