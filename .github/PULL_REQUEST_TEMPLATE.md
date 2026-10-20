## What this PR does

<!-- One of: adds a result / adds or changes a task / other. -->

## Result checklist

Skip this section if the PR does not add a result. `mengine-bench submit` fills the PR body with the scores.

- [ ] Adds exactly one `results/<run>/` folder written by `mengine-bench run`, not edited by hand, and nothing else
- [ ] The run ended with `privacy check: clean`
- [ ] I read `summary.md` and skimmed the transcripts: no secrets, tokens or personal data
- [ ] My setup is described with `--config key=value` (provider, server hardware, quantization, MCP, skills...) where it matters

## Task checklist

Skip this section if the PR does not add or change tasks. See CONTRIBUTING.md.

- [ ] Fixture, English prompt(s), reference solution and deterministic checks; integrity rules are mandatory gates
- [ ] Gold self-test: the reference passes and the untouched folder fails
- [ ] `uv run mengine-bench tasks-doc --write`, `tasks-doc --readme` and `uv run pytest -q` pass
- [ ] No personal data, company names, secrets or absolute local paths
