# mengine-bench

mengine-bench is the coding-agent benchmark of Milton Stiilpen Jr's AI
workstation (mengine), public for contribution and comparison. Run it against
your own agent and model, add tasks, and compare results on a shared
leaderboard.

## What it measures

An *agent* here is a harness plus a model (for example Claude Code with a
given model, Codex CLI, opencode, or your own command). Each task is a real,
multi-step job in a fresh workspace, with a deterministic reference ("gold")
check. Categories:

- coding and debugging (including long-horizon, multi-file repos)
- data and business analysis with exact numbers
- information retrieval (local files and the web, with cited sources)
- long-context and context-compaction survival across sessions
- visual output (web pages checked by rendering) and image understanding

Every task ships a reference solution, and the test suite proves without any
model that the reference passes and the untouched workspace fails.

## Suites

| Suite | Tasks | Measured run |
| --- | --- | --- |
| FAST | 14 | FAST has no measured run yet |
| FULL | 20 | 20 min 10 s wall (510 s agent time), baseline below |

FAST already contains all six weight-2 tasks. FULL adds six weight-1 tasks.

The 2026-10-17 FULL baseline used Codex gpt-6.1-sol at low effort and a
3-vote judge (Claude `claude-opus-5-5`, xhigh effort). It took 20 min 10 s wall
(510 s agent time); judging and grading are excluded from agent time.
Both visual tasks reported "no browser" and used deterministic checks only.
This is one measured configuration, not a duration estimate for other agents.

A run declares its suite. Results are only compared within the same suite,
scoring version, judge and visual grading profile.

## Scores in short

- **Objective** (0-100): accuracy plus speed. Each task scores
  `100 * correctness * (0.8 + 0.2 * speed)`, where speed compares the agent's
  time with the task's published par time and only counts for solved tasks.
  HARD tasks weigh 2. It is deterministic except for the two visual tasks,
  whose checklist is voted by the vision judge: the judge does affect their
  objective correctness.
- **Subjective** (0-100, optional): an LLM judge grades each solution with a
  fixed rubric (correctness 40, engineering quality 30, polish 20, process
  efficiency 10), median of 3 votes. Recommended judge: Claude Opus 5.5 at
  xhigh effort.

Full definitions and a worked example: [docs/SCORING.md](docs/SCORING.md).
Task list: [docs/TASKS.md](docs/TASKS.md).

## Quick start

Requires Python >= 3.11 and [uv](https://docs.astral.sh/uv/).

```
git clone https://github.com/owlmsj/mengine-bench.git
cd mengine-bench
uv sync
uv run pytest -q                      # gold self-tests, no model calls
uv run mengine-bench list --suite fast
uv run mengine-bench selftest              # every task's gold, no agent
uv run mengine-bench run --suite fast --agent claude --model <model-id> --dry-run
```

Run a suite against an agent (the agent CLI must be installed and logged in):

```
uv run mengine-bench run --suite fast --agent claude   --model <model-id> --effort high
uv run mengine-bench run --suite fast --agent codex    --model <model-id> --effort high
uv run mengine-bench run --suite fast --agent opencode --model <provider/model>
uv run mengine-bench run --suite fast --agent cmd --model <label> --cmd "my-agent --task {prompt_file} --cwd {workspace}"
```

Add `--judge claude --judge-model claude-opus-5-5 --judge-effort xhigh` for the
subjective score and the visual checklists (`--judge-votes`, default 3).
`--tasks a,b` runs a subset. Each run writes one result bundle to
`results/<suite>/<date>_<agent>_<model>_<effort>_<run id>/` (scores, redacted
transcripts, final workspaces, a sha256 manifest); check it with
`uv run mengine-bench verify <bundle>`.

Agents run with permission prompts bypassed (Claude `bypassPermissions`,
Codex `--dangerously-bypass-approvals-and-sandbox`, opencode `--auto`), in
fresh workspaces under the system temp dir (`--work` to change it). Use a
disposable machine or account. Each step has the task's timeout; on timeout
the whole agent process tree is killed.

Multi-step tasks: a `fresh_session` step starts a new agent process; any
other step resumes the session (claude `--resume`, codex `exec resume`,
opencode `--session`). The `cmd` adapter cannot resume, so such tasks are
reported "unsupported" (scored 0). A fresh-session step starts in a new
workspace holding only the files the task carries over; `hide` moves files
out of the workspace before a step; `compact_before` compacts the session
first (Claude Code only). Visual tasks need a Chromium-family browser
(`MENGINE_BENCH_BROWSER`, PATH, or the standard Edge/Chrome install
locations) and a judge. Without both the run's grading profile is
"unrendered": visual tasks are never solved there (correctness capped at 0.5)
and the leaderboard ranks such runs in their own table.

## Results and leaderboard

[LEADERBOARD.md](LEADERBOARD.md) ranks every submitted run that passes
`mengine-bench verify`, one table per suite, scoring version, judge and
visual grading profile. To add
yours, open a pull request with exactly one bundle directory; the steps are in
[docs/SUBMITTING.md](docs/SUBMITTING.md).

The audit model, plainly:

- **Re-verified**: each task's deterministic checks are re-run from the saved
  final workspace and must match the recorded results; OBJECTIVE, ACCURACY,
  SUBJECTIVE and COMPOSITE are recomputed from the raw per-task data; the
  manifest hashes, the JSON schema, the 25 MB size cap and the absence of
  unredacted secrets are checked. CI does this on every results PR.
- **Self-reported**: timings, judge votes and vision checklist votes cannot be
  re-derived without rerunning the models. They are checked for internal
  consistency (step times sum to the task time, medians and majorities follow
  from the recorded votes) and sealed by the manifest, but they are trusted.
  Questions or disputes about a result: open a "Result question" issue.
- **Partial runs**: a bundle whose tasks are not exactly its declared suite
  (for example a `--tasks` subset) verifies but is listed apart, never ranked.

## Known limitations

- Timings, agent and model identity, and judge votes are self-reported. Verify
  checks them for internal consistency only.
- The manifest is a consistency check, not an attestation: a submitter can
  regenerate it after editing a bundle, so it proves the files agree with each
  other, not that the run happened as described.
- Hidden tests run the submitted workspace code without a hardened sandbox.
  Run `mengine-bench verify` on other people's submissions only in a
  disposable environment (a throwaway VM or container).
- Some gold checks are lenient: they accept a few wrong answers that look
  right.
- Maintainers review each submission pull request by hand before it is
  merged.

## License

MIT, see [LICENSE](LICENSE).
