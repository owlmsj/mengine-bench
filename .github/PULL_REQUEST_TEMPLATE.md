## What this PR does

<!-- One of: adds a result bundle / adds or changes a task / other. -->

## Result submission checklist

Skip this section if the PR does not add results. See docs/SUBMITTING.md.

- [ ] Adds exactly one bundle directory under `results/<suite>/`, written by `mengine-bench run` and not edited by hand
- [ ] Touches no other bundle, no code and no docs
- [ ] Does not edit LEADERBOARD.md (it is regenerated on main)
- [ ] `uv run mengine-bench verify <bundle>` passes locally (paste the last line below)
- [ ] I read the transcripts and they contain no secrets, tokens or personal data
- [ ] Run from a clean checkout of a released bench version (`bench_commit.dirty` is false)

| field | value |
| --- | --- |
| suite | |
| agent CLI and version | |
| model id | |
| effort | |
| judge model, effort and votes (or "none") | |
| verify result | |

## Task checklist

Skip this section if the PR does not add or change tasks. See CONTRIBUTING.md.

- [ ] Fixture, English prompt(s), reference solution and deterministic checks
- [ ] Gold self-test: the reference passes and the untouched workspace fails
- [ ] `uv run mengine-bench tasks-doc --write` and `uv run pytest -q` pass
- [ ] No personal data, company names, secrets or absolute local paths
