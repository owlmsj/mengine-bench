# Scoring (version 1.0)

mengine-bench reports two scores for one run of an agent (harness + model)
on one suite:

- **OBJECTIVE** (0-100): did the agent get it right, and how fast compared
  with the published par time. Deterministic for every task except the
  visual ones: their aesthetic checklist is voted by the vision judge, so
  **the judge does affect the objective correctness of visual tasks** (see
  [Visual tasks](#visual-tasks-and-the-grading-profile)).
- **SUBJECTIVE** (0-100, optional): an LLM judge grades the quality of each
  solution with a fixed rubric.

The formulas live in `mengine_bench/scoring.py` (`SCORING_VERSION = "1.0"`).
Every result file records the scoring version and the visual grading profile
(`grading.visual`); results are only compared within the same suite, scoring
version, judge and grading profile.

## Per-task inputs

| Symbol | Meaning |
| --- | --- |
| `w_i` | Task weight: 1 for normal tasks, 2 for HARD/long-horizon tasks (marked in the catalog). |
| `c_i` | Correctness in [0, 1]: share of the task's deterministic checks that passed. |
| `p_i` | Solved: the task's own pass rule (all checks, or a stated share for checklist-graded visual tasks). |
| `t_i` | The agent's wall time for the task in seconds, excluding grading and judging. |
| `ref_s_i` | The task's published par time in seconds (`par_s` in the catalog). |

Special cases:

- **Mandatory checks** (for example "the page rendered") must all pass. If any
  fails, `c_i` is capped at 0.5 and the task is not solved.
- **Timeout or crash**: `c_i = 0`. A step counts as finished only when the
  agent CLI exits 0 AND its stream ends with the adapter's terminal
  completion event (Claude Code: a `result` event with `subtype: success`;
  Codex: `turn.completed` as the last turn event; opencode: a last
  `step_finish` with `reason: stop`). Anything else, including a
  success-looking but truncated stream or a success event with a failing
  exit code, is a crash.
- **Unsupported** (the adapter cannot do what the task needs, e.g. resume a
  session): scored 0 and listed separately in the report.

## Objective score

```
s_i = min(1, ref_s_i / t_i)   if solved, else 0
o_i = 100 * c_i * (0.8 + 0.2 * s_i)

OBJECTIVE = sum(w_i * o_i) / sum(w_i)            (one decimal)
ACCURACY  = sum(w_i * 100 * c_i) / sum(w_i)       (one decimal)
```

Correctness dominates (80%); speed only moves the remaining 20%, and only
for solved tasks, so a fast wrong answer never earns speed credit. Beating
par earns nothing extra: `s_i` is capped at 1.

Each report also lists the solved count, the total agent time and per-category
results.

## Subjective score (optional)

A judge model grades each task's solution 0-100 with this rubric:

| Criterion | Points |
| --- | --- |
| Correctness and completeness | 40 |
| Engineering quality of the solution (approach, code, verification) | 30 |
| Deliverable polish and instruction following | 20 |
| Process efficiency (tool calls, retries, wasted steps) | 10 |

The judge sees the task prompt(s), the agent's final answer, the workspace
diff (file list plus truncated contents), the tail of the transcript and the
deterministic check results. It returns JSON `{"score": int, "rationale": str}`.

By default the judge votes 3 times; the task's judge score is the **median**
of the votes. A task the judge could not grade counts as 0.

```
SUBJECTIVE = sum(w_i * median(votes_i)) / sum(w_i)   (one decimal)
```

Recommended judge: **Claude Opus 5.5 at xhigh effort**. Every report states
the judge model and effort. Scores from different judges are not comparable.

### Judge isolation

Answers, diffs, transcripts and screenshots are written by the agent under
test, so the judge treats them as untrusted:

- Each vote is a new judge process in a new, empty system-temp directory
  (only `screenshot.png` for vision votes), never under the run tree or the
  repo. The prompt is kept next to the run for audit.
- Text evidence sits in `<<<EVIDENCE <marker> <name>>>> ... <<<END EVIDENCE
  <marker> <name>>>>` blocks, preceded by the rule that evidence is data, not
  instructions. The marker is a hash of the evidence, so the agent cannot
  forge the closing line.
- The judge runs with tools off where the CLI allows it. Claude Code:
  `--tools "" --restricted --strict-mcp-config --permission-mode dontAsk
  --no-session-persistence`, images sent inline as stream-json content blocks.
  Codex: `--sandbox read-only` (no writes, no network), `--ephemeral
  --ignore-user-config --ignore-rules`, and the shell, exec, app and browser
  features disabled; Codex keeps a read-only built-in, so Claude is the
  recommended judge. opencode: an inline config denying edit, bash, web and
  external-directory permissions, without `--auto`. A `cmd` judge's tool
  policy is the user's own.

## Visual tasks and the grading profile

Visual tasks (`web-mondrian-landing`, `3d-voxel-landscape`) are graded by
deterministic gates (mandatory), a headless browser screenshot (mandatory:
rendered with content) and the vision judge's checklist (3 votes, majority
per item; listed mandatory items gate, the rest pass at 70%). The browser is
`MENGINE_BENCH_BROWSER`, else Edge/Chrome/Chromium on PATH, else their
standard install locations on Windows, macOS and Linux.

Every run records `grading.visual` in result.json:

- `rendered`: every visual task was screenshotted and judged.
- `unrendered`: at least one visual task had no browser or no vision judge.
  Those tasks are flagged `unrendered` and get the failing mandatory check
  "graded rendered: browser screenshot and vision judge", so they are not
  solved and `c_i` is capped at 0.5, however well the textual gates went.

The leaderboard groups by grading profile, so unrendered runs never rank
next to rendered ones. Gold self-tests grade visual tasks on the
deterministic gates only (no browser, no model).

## Multi-step boundary

A `fresh_session` step starts a new agent process in a new workspace that
holds only the files the step declares in `carry` (for `cmp-*` tasks: the
summary written in step 1) plus AGENTS.md. That workspace lives under its own
system-temp root, so the earlier steps are neither inside nor above it; it
moves back under the run directory for grading once the task ends. `hide`
moves named files out of a continuing workspace before the turn; `inline`
pastes files into the prompt. The runner does not sandbox the agent's file
system: an agent that ignores AGENTS.md could still open an absolute path
elsewhere on the disk.

## Composite (optional)

Reported only when both scores exist:

```
COMPOSITE = 0.6 * OBJECTIVE + 0.4 * SUBJECTIVE
```

computed from the two rounded scores.

## Par times

`par_s` includes 14 measured values from the maintainers' original private v1
runs with DeepSeek V4.1 Flash and six derived values for tasks absent from
those runs. The derived values double a comparable measured task's time,
with the rounding described in [TASKS.md](TASKS.md#par-times). That page lists
the source runs and each derivation. Changing a par time changes scores, so
it requires a scoring version bump.

## Worked example

Five tasks, one judge (3 votes each):

| Task | w | par (s) | time (s) | checks | outcome | c | s | o | votes | judge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1 | 120 | 90 | 10/10 | solved | 1.0 | 1.0 | 100.0 | 80, 85, 90 | 85 |
| B | 2 | 300 | 600 | 10/10 | solved | 1.0 | 0.5 | 90.0 | 70, 60, 75 | 70 |
| C | 1 | 200 | 150 | 6/10 | not solved | 0.6 | 0 | 48.0 | 40, 50, 45 | 45 |
| D | 1 | 200 | 100 | 9/10, a mandatory check failed | not solved | 0.5 | 0 | 40.0 | 30, 35, 20 | 30 |
| E | 2 | 400 | 900 | timeout | not solved | 0 | 0 | 0.0 | 10, 0, 5 | 5 |

- OBJECTIVE = (100 + 2 * 90 + 48 + 40 + 2 * 0) / 7 = 368 / 7 = **52.6**
- ACCURACY = (100 + 2 * 100 + 60 + 50 + 0) / 7 = 410 / 7 = **58.6**
- Solved: **2 / 5**; total agent time: **1840 s**
- SUBJECTIVE = (85 + 2 * 70 + 45 + 30 + 2 * 5) / 7 = 310 / 7 = **44.3**
- COMPOSITE = 0.6 * 52.6 + 0.4 * 44.3 = **49.3**

This table is locked by `tests/test_scoring.py::test_docs_worked_example`.
