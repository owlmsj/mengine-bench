# Scoring (bench 1.4)

A run of an agent (harness + model + configuration) gets three numbers folded into
the Score, and a Cost kept apart.

| Total | What it is |
| --- | --- |
| **Correct %** | `100 x mean(c_i)` over every task. Deterministic: anyone reproduces it with `run` and `selftest`. |
| **Judge** | Mean of one rubric vote per task, 0-100. Set by the maintainer with `mengine-bench judge`. |
| **Speed** | 100 at 5 min of Time or less, 0 at 30 min or more, linear in between: `100 x (1800 - Time) / 1500`. |
| **Score** | `0.6 x Correct % + 0.25 x Judge + 0.15 x Speed x Correct % / 100`, one decimal, from the published values. Speed pays only for work that is right. Only once judged. |
| **Time** | Total agent wall seconds. Grading and judging are excluded; a timeout counts its full time. |
| **Cost** | USD estimate of inference, with its basis. A separate column: no points per dollar. |
| **Est. price** | The run's tokens at public API list prices, so subscription and API runs compare. No points either. |

The formulas live in `mengine_bench/scoring.py`. Runs compare when they ran the
same bench major.minor (1.4.x). A patch release changes no task or prompt. When it changes how a run is judged or
scored, every ranked run is judged again from its bundle (`mengine-bench judge --again`), so none has to run again. Rankings of older versions stay in LEADERBOARD.md as history, with the Scores of their own formula.

A run is one sample and runs are not repeated, so ties come from the published tasks: draw the 14 tasks again with
replacement, 2000 times, seeded, and count how often the higher run stays ahead. Under 80% the two neighbours read as
a tie. This shows how much the order rests on this set of tasks; it says nothing about the noise between two runs of one agent.
`mengine-bench analyze` prints the shares, the points each part of the Score moves and the tasks that separate runs. No agent runs.

## Checks: c_i

Each task has deterministic checks (executed hidden tests, exact numbers, file
state, regex) and may have mandatory gates (for example "existing tests
untouched", or the page file exists).

- `c_i` = share of the task's scored checks that passed.
- Any failed gate gives `c_i = 0`.
- A timeout or a crash grades the workspace as the stop found it. A gate on
  the page's size does not apply there, so a page cut short earns the checks it passes, up to
  half of the task; a gate that guards the tests still does. The task shows its status, counts its full time and
  is never Solved. A reply already given when the limit hits counts as the reply. With nothing written or
  said, there is nothing for the checks to credit.
- Each prompt states the limit, 2 to 8 min per step, and that the folder and the reply are graded as they
  stand when time runs out. Load a local model before the run: a cold load counts against the first task.
- **Solved** = the agent finished, and every gate and every check passed.

A failed check says why in `result.json` and in the summary's "Failed checks": what it expected and what it received.
The judge does not see that text.

Visual tasks (`web-mondrian-landing`, `3d-voxel-landscape`) add two checks at grading, in a headless
Chromium-family browser: the page runs without an uncaught script error, and its screenshot is not blank. That takes
about 2 s per page, 54 s at most over 46 published pages, and grading is not in Time. A machine with no browser, a render that fails or the
three.js CDN out of reach leaves the two checks out, with a note on the task, and costs no point. The page
is a declared deliverable that the bundle keeps verbatim for the judge.

## Judge

`mengine-bench judge results/<run>` (maintainer only) runs one judge, Claude
`claude-opus-5-5` at effort `xhigh`, exactly once per task. A call that fails or
returns invalid JSON is retried; if a task still has no vote, nothing is written.
Rubric 2.4 grades what the checks cannot see. The check results are shown to
the judge as context with the instruction not to re-score correctness. Its rules and
anchors travel in a system prompt, and every vote comes with its three subscores, which
must add up to the score.

| Criterion | Points |
| --- | --- |
| Approach and code/solution quality | 40 |
| Deliverable and instruction following | 30 |
| Self-verification; on the reply-only `lc-changelog` and `vis-chart`, answer discipline; on pages, the rendered look | 30 |

For a visual task the maintainer's machine renders the stored page with headless
Chromium (Edge, Chrome or Chromium; `MENGINE_BENCH_BROWSER` overrides it) and the
judge sees the screenshot. A render that fails is tried up to 3 times; if it keeps failing, the judge votes without a
screenshot and the bundle records it. With no browser at all, nothing is judged.

The judge reads the task prompt, the check results, the final answers, each page whole, the agent's other changes
and one tool log with the same shape for every harness. It does not read the raw stream, which carries the model id.

Measured in 1.3.3: two votes on the same message differed by 1.35 points on average and 6 at most (23 pairs), so one
task's vote is noisy and a run's mean of 14 is much less so.
The judge never changes the checks.

After a change to the rubric or the judge model, `mengine-bench judge-anchors` votes the reference solution and the untouched
workspace of two tasks: four votes, no agent run, nothing written. The gap must be at least 30 points in each.

The judge also sees the task's status and the tool-level run statistics (see below), not tokens, turns,
time or speed: they depend on the harness or the hardware, and the judge grades without knowing the model or the machine.

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
| `tool_s`, `wait_s` | Time in tools, and between turns (prefill, queue); opencode only, plus `tool_s` on AGY |
| `turn_tps_median` | Median generated tokens per second, turns of 500 tokens or more; opencode and AGY |

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

## Est. price

Cost is `n/a` for most subscription runs, so the leaderboard also prices every run the same way:
`((input - cached) x X + cached x Y + generated x Z) / 1,000,000`. It is an estimate, shown as `~$x`, and a
subscription does not bill this amount. `generated` holds reasoning on every harness. A model with no price below
shows `n/a`, and local inference declared free shows `$0.00 (local)`.

USD per million tokens, read on 2026-10-31:

| Model | Input | Cached | Output | Source |
| --- | --- | --- | --- | --- |
| `claude-opus-5-5` | 8.00 | 0.20 | 20.00 | [Anthropic](https://platform.claude.com/docs/en/about-claude/pricing) |
| `claude-sonnet-5-5` | 4.00 | 0.10 | 10.00 | Anthropic |
| `gpt-6-astra` | 10.00 | 1.00 | 50.00 | [OpenAI](https://developers.openai.com/api/docs/pricing) |
| `gpt-6-astra`, fast | 20.00 | 2.00 | 100.00 | OpenAI |
| `gpt-6.1-sol` | 2.00 | 0.10 | 10.00 | OpenAI |
| `gpt-6.1-sol`, fast | 4.00 | 0.20 | 20.00 | OpenAI |
| `zai/glm-5.3-flash` | 0.15 | 0.03 | 0.50 | [Z.ai](https://docs.z.ai/guides/overview/pricing) |
| `deepseek/deepseek-flash` | 0.15 | 0.003 | 0.60 | [DeepSeek](https://api-docs.deepseek.com/quick_start/pricing) |
| `gemini-4-argon` | 2.00 | 0.10 | 10.00 | [Google](https://ai.google.dev/gemini-api/docs/pricing) |

- Claude's input is its 1 h cache write price (base input is 4.00 and 2.00), because Claude Code caches nearly all its
  uncached input. On the published Opus low and Sonnet medium runs the estimate lands within 1 cent of `total_cost_usd`.
- The fast rows apply when the run's config says `service_tier=fast`.
- DeepSeek's is the off-peak rate, and peak hours cost twice that.
- Gemini's rise to 4.00, 0.20 and 20.00 on 2026-12-01 is not applied.

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
- Score = 0.6 x 53.3 + 0.25 x 56.7 + 0.15 x 32.0 x 53.3 / 100 = 48.7
- Cost = 0.40 + 0.90 = >= $1.30 (harness), a lower bound because C has no usage

With `--price input=1.25,cached=0.125,output=10`, a Codex step of 2,000,000
input tokens (1,500,000 cached) and 100,000 output tokens costs
(500,000 x 1.25 + 1,500,000 x 0.125 + 100,000 x 10) / 1,000,000 = $1.81.

`tests/test_scoring.py` locks these numbers.
