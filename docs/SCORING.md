# Scoring (bench 1.3)

A run of an agent (harness + model + configuration) gets three numbers folded into
the Score, and a Cost kept apart.

| Total | What it is |
| --- | --- |
| **Correct %** | `100 x mean(c_i)` over every task. Deterministic: anyone reproduces it with `run` and `selftest`. |
| **Judge** | Mean of one rubric vote per task, 0-100. Set by the maintainer with `mengine-bench judge`. |
| **Speed** | 100 at 5 min of Time or less, 0 at 30 min or more, linear in between: `100 x (1800 - Time) / 1500`. |
| **Score** | `0.6 x Correct % + 0.25 x Judge + 0.15 x Speed`, one decimal, from the published values. Only once judged. |
| **Time** | Total agent wall seconds. Grading and judging are excluded; a timeout counts its full time. |
| **Cost** | USD estimate of inference, with its basis. A separate column: no points per dollar. |

The formulas live in `mengine_bench/scoring.py`. Runs compare when they ran the
same bench major.minor (1.3.x); a patch release changes no task, prompt or score. A run is one sample:
runs within 1 point of each other at the top get a repeat before anyone calls a winner. Rankings of older
versions stay in LEADERBOARD.md as history, with the Scores of their own formula.

## Checks: c_i

Each task has deterministic checks (executed hidden tests, exact numbers, file
state, regex) and may have mandatory gates (for example "existing tests
untouched", or the page file exists).

- `c_i` = share of the task's scored checks that passed.
- Any failed gate gives `c_i = 0`. A crash gives `c_i = 0`.
- A timeout stops the agent and grades the workspace as the limit found it. A gate on
  the page's size does not apply there, so a page cut short earns the checks it passes, up to
  half of the task; a gate that guards the tests still does. The task shows as `timeout`, counts its full time and
  is never Solved. A reply already given when the limit hits counts as the reply. With nothing written or
  said, there is nothing for the checks to credit.
- Each prompt states the limit, 2 to 8 min per step, and that the folder and the reply are graded as they
  stand when time runs out. Load a local model before the run: a cold load counts against the first task.
- **Solved** = the agent finished, and every gate and every check passed.

Visual tasks (`web-mondrian-landing`, `3d-voxel-landscape`) are graded the same
way at run time: content gates only, no browser and no vision model. The page
is a declared deliverable that the bundle keeps verbatim for the judge.

## Judge

`mengine-bench judge results/<run>` (maintainer only) runs one judge, Claude
`claude-opus-5-5` at effort `xhigh`, exactly once per task. A call that fails or
returns invalid JSON is retried; if a task still has no vote, nothing is written.
Rubric 2.3 grades what the checks cannot see. The check results are shown to
the judge as context with the instruction not to re-score correctness.

| Criterion | Points |
| --- | --- |
| Approach and code/solution quality | 40 |
| Deliverable and instruction following | 30 |
| Self-verification (visual tasks: rendered look) | 30 |

For a visual task the maintainer's machine renders the stored page with headless
Chromium (Edge, Chrome or Chromium; `MENGINE_BENCH_BROWSER` overrides it) and the
judge sees the screenshot. A render that fails is tried up to 3 times. A blank or failed render gives that task a judge of 0, unless the
run was stopped at its limit: then the judge votes on what exists, with no screenshot.
The judge never changes the checks.

The judge also sees the task's status and its run statistics (see below), except
time and speed, which only the Score counts: they depend on the hardware, and the judge grades without knowing
the model or the machine.

## Run statistics

Read from the harness's event stream, per task and in total, including a task
stopped at its limit. They are never folded into Score; they are kept so the
formula can be refined later from many runs.

| Field | What it is |
| --- | --- |
| `model_turns`, `tool_calls`, `tool_errors` | Model calls (Codex reports one per step, so this does not compare across harnesses), tool calls, tool calls that failed |
| `shell_commands`, `shell_failures` | Shell tool calls, and those with a non-zero exit |
| `file_writes` | Write and edit tool calls |
| `repeated_tool_calls` | Calls identical to an earlier one in the same step |
| `outside_path_uses` | Tool paths and shell commands that hold `../` or `..\\`; a hint, since a subfolder can name its parent |
| `input_tokens`, `cached_input_tokens` | Prompt tokens, and the part read from cache |
| `generated_tokens`, `reasoning_tokens` | Everything generated, reasoning included, and the reasoning part; on Claude, a run stopped before its result gives a lower bound |
| `largest_turn_tokens` | The largest single turn; Claude does not report it |
| `first_tool_s`, `first_write_s`, `last_event_s` | Seconds from the first event; opencode only |
| `tool_s`, `wait_s` | Time in tools, and between turns (prefill, queue); opencode only |
| `turn_tps_median` | Median generated tokens per second, turns of 500 tokens or more; opencode only |

A value a harness does not report is `null`, never 0.

Isolation: each call is a new judge process in a new empty temp directory
(holding only `screenshot.png` for visual tasks) with tools off where the CLI
allows it. Agent-written evidence sits in `<<<EVIDENCE <marker> <name>>>>`
blocks; the marker is a hash of the evidence, so the agent cannot forge the
closing line.

## Cost

Cost uses one basis per run, recorded next to the number:

- `harness`: every measured step reported USD (Claude Code `total_cost_usd`,
  opencode step cost).
- `price`: the harness reported no USD, so the submitter declared prices with
  `run --price input=X,cached=Y,output=Z` (USD per million tokens), applied to
  each step's tokens and recorded per task and in total:
  `((input - cached) x X + cached x Y + output x Z) / 1,000,000`. Reasoning
  tokens are already inside output. `--price 0` declares free or local
  inference.
- `n/a`: unknown. Never shown as 0.

A step without usage (crash, timeout) makes the total a lower bound, shown as
`>= $x`. Tokens are always recorded, per step, per task and in total; the
leaderboard's Tokens column is input (cache reads and writes included) plus output.

## Worked example

Three tasks, Claude Code (harness USD):

| Task | Checks | c | Judge | Time (s) | Cost (USD) |
| --- | --- | --- | --- | --- | --- |
| A | 4/4, gates pass | 1.00 | 80 | 120 | 0.40 |
| B | 3/5, gates pass | 0.60 | 60 | 300 | 0.90 |
| C | timeout | 0.00 | 30 | 900 | no usage |

- Correct % = 100 x (1.00 + 0.60 + 0.00) / 3 = 53.3; Solved 1/3
- Judge = (80 + 60 + 30) / 3 = 56.7
- Time = 120 + 300 + 900 = 1320 s (22 min 00 s)
- Speed = 100 x (1800 - 1320) / 1500 = 32.0
- Score = 0.6 x 53.3 + 0.25 x 56.7 + 0.15 x 32.0 = 51.0
- Cost = 0.40 + 0.90 = >= $1.30 (harness), a lower bound because C has no usage

With `--price input=1.25,cached=0.125,output=10`, a Codex step of 2,000,000
input tokens (1,500,000 cached) and 100,000 output tokens costs
(500,000 x 1.25 + 1,500,000 x 0.125 + 100,000 x 10) / 1,000,000 = $1.81.

`tests/test_scoring.py` locks these numbers.
