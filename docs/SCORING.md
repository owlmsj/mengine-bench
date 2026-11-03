# Scoring (bench 2.1)

A run of an agent (harness + model + configuration) gets three numbers folded into
the Score, and a Cost kept apart.

| Total | What it is |
| --- | --- |
| **Correct %** | `100 x mean(c_i)` over every task. Deterministic: anyone reproduces it with `run` and `selftest`. |
| **Judge** | Mean of one rubric vote per task, 0-100. Set by the maintainer with `mengine-bench judge`. |
| **Speed** | 100 at 5 min of Time or less, 0 at 30 min or more, linear in between: `100 x (1800 - Time) / 1500`. |
| **Score** | `0.6 x Correct % + 0.15 x Judge + 0.25 x Speed x Correct % / 100`, one decimal, from the published values. Speed pays only for work that is right. Only once judged. |
| **Time** | Total agent wall seconds. Grading and judging are excluded; a timeout counts its full time. On Codex the clock stops at the final event (`turn.completed`); a process still alive 5 s later is ended and flagged, not counted as a timeout. |
| **Cost** | One column (#162): `$x` exact when the harness reports it, else `~$x`, the run's tokens at public API list prices (below), so subscription and API runs compare; `$0.00 (local)` for local inference, `>=` a lower bound, `n/a` neither. No points per dollar. |
| **Thinking, Tools, Tool s** | Reasoning tokens, tool calls, and the median seconds per tool call where the harness times each call (opencode, AGY, Claude Code event stamps; `-` on Codex, never estimated). Statistics only, no points (#162). |

The formulas live in `mengine_bench/scoring.py`. Runs compare when they ran the
same bench major.minor (2.0.x). A patch release changes no task or brief; a workspace safety rule may change. When it changes how a run is judged or
scored, every ranked run is judged again from its bundle (`mengine-bench judge --again`), so none has to run again. Rankings of older versions stay in LEADERBOARD.md as history, with the Scores of their own formula.
Bench 1.8 changed only the weights (#122): Speed 0.25 and Judge 0.15, from 0.15 and 0.25 in 1.7; tasks and briefs are those of 1.7.
Bench 2.0 keeps the 1.8 weights and changes the tasks (#124): 20 instead of 15.
Bench 2.1 changes only the time limits (#137): each is the slowest finished time in the eight published 2.0
runs plus 25%, rounded up to 30 s, at least 60 s, never above the 2.0 limit and never below a limit a published run
hit. A run's worst case drops from 76 to 49.5 min, so a setup that cannot keep up fails sooner.
The eight 2.0 runs stay in the 2.1 ranking, each marked 2.0 (#139): they ran with the longer limits.
Bench 2.1.1 (#144): a task whose model never replied before its limit (no turn, tool call, write, token or reply)
runs once more from scratch and keeps the second attempt, flagged on the task; a slow agent is never retried.
Bench 2.2 adds three tasks adapted from Terminal-Bench 2.1 (#151): `txt-regex-log`, `ds-sqlite-recover` and
`py-async-cancel`, 60 s each by the 2.1 rule, so the worst case is 52.5 min. They add about 2 min to a good run: the
Opus 5.5 xhigh probe took 46.2 + 31.6 + 44.7 s. The 2.0 and 2.1 runs stay in the ranking, each row marked with
its version (#151): their 20 tasks against 23 for a 2.2 row.
Bench 2.3 adds computer use, web search, files and basic media (#153): `cu-social-cycle` (a post with an image the
agent makes, a reply and a delete on a local social-site replica, graded from state the site's server signs),
`cu-webmail` (an invoice found, downloaded, answered and archived on a local webmail replica), `web-fact-search`
(three stable facts from the real web, each with the URL that proves it), `file-media-edit` (an exact crop of a photo
and a filled, flattened PDF form) and `media-voice` (a spoken WAV, transcribed offline by whisper tiny). Their limits
follow the 2.1 rule from the slowest finished probe (+25%, rounded up to 30 s): 150, 90, 60, 90 and 60 s, so the worst
case is 60 min. Opus 5.5 xhigh took 98.0 + 47.5 + 25.1 + 51.6 + 28.9 s, about 4 min more for a good run (owner
budget: a best run of about 15 min). The 2.0, 2.1 and 2.2 runs stay in the ranking, each row marked
with its version.
2.3.1 (#155): cu-social-cycle drops the reply, cu-webmail drops the archive, after the first 2.3.0 run timed out on
both through the browser (~4 s per browser action). No 2.3.0 run was published, so 2.3.1 keeps the same minor.
Their limits follow the 2.1 rule from Sonnet 5.5 low browser-route probes (Claude in Chrome): cu-social-cycle
127.6 and 118.2 s, cu-webmail 128.0 and 126.3 s, so 180 s each (from 150 and 90) and a worst case of 62 min.
Bench 2.4 (#161): every prompt asks the agent to close the browser tabs, windows and apps it opened. cu-social-cycle and
cu-webmail gain the scored check "closed the tabs and apps it opened": no site page still sends its heartbeat 5 s after
the agent is done, and nothing the task started is left running. On every task the runner then kills what the task
left running (a process born during the task whose parent links lead back to the runner; never one that existed
before the task or was born from one) and records it as `left_running`, with `left_open_tabs` on the site tasks; a
page told the task is over blanks itself. The 2.0 to 2.3 runs stay in the ranking, each row marked with its version.

A run is one sample and runs are not repeated, so ties come from the published tasks: draw the tasks again with
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
- Each prompt states the limit, 1 to 7 min per step, and that the folder and the reply are graded as they
  stand when time runs out. Load a local model before the run: a cold load counts against the first task.
- **Solved** = the agent finished, and every gate and every check passed.

A failed check says why in `result.json` and in the summary's "Failed checks": what it expected and what it received.
The judge does not see that text.

Visual tasks (`web-mondrian-landing`, `3d-print-homage`, `web-word-universe`) add two checks at grading, in a headless
Chromium-family browser: the page runs without an uncaught script error, and its screenshot is not blank. That takes
about 2 s per page, 54 s at most over 46 published pages, and grading is not in Time. A machine with no browser, a render that fails or the
three.js CDN out of reach leaves the two checks out, with a note on the task, and costs no point. The page
is a declared deliverable that the bundle keeps verbatim for the judge.

## Open briefs

Since 1.6 every eval is an open brief: the context, the problem and the outcome wanted. The method, the tools and the
traps are left to the agent. Business definitions live in documents in the workspace, as they would at a company. The
prompt keeps the question and a small `result.json` contract, because a person has to be able to check the answer.

Correct reads delivered files, never the chat. It accepts rounding, percent or fraction and common number formats, and
rejects a wrong answer, not a different route. Two experts should reach the same verdict on any result.

Limits are 3 min per eval, 5 min for `gd-integration-repo`, `web-mondrian-landing` and `web-plan-ranking`, 6 min for
`web-word-universe` and 7 min for `3d-print-homage`, from measured times: the slowest short eval took 50 s. The eight
evals new in 2.0 (#124) start at those limits until a pilot run measures them. Each prompt states its limit and
asks the agent to finish once the work is right, with at most 2 rounds of revision. At the limit the agent stops, and what it delivered is graded.

Each eval also declares checkpoints, key actions matched against the tool calls, published per task in the bundle and
`summary.md`. They exist to diagnose a run. They change no grade and the judge never sees them, because scoring them
would reward one route over another. "Not seen" can simply be a different route.

## Judge

`mengine-bench judge results/<run>` (maintainer only) runs one judge, Claude
`claude-opus-5-5` at effort `xhigh`, exactly once per task. A call that fails or
returns invalid JSON is retried; if a task still has no vote, nothing is written.
Rubric 2.5 grades what the checks cannot see. The check results are shown to
the judge as context with the instruction not to re-score correctness. Its rules and
anchors travel in a system prompt, and every vote comes with its three subscores, which
must add up to the score.

| Criterion | Points |
| --- | --- |
| Reasoning and execution: understood the problem, chose a sound strategy of its own, carried it out simply and reproducibly. Any valid route can earn full marks. | 40 |
| Deliverable and presentation: the problem is solved, nothing invented, and the final message says what was found, the assumptions and any limit left open. Format is never a defect. | 30 |
| Quality assurance: an independent check of its own result; on a task that only asks for a few facts, answer discipline (none in 2.0); on pages, the rendered look | 30 |

The plan is judged from the actions: a written plan earns nothing by itself.

For a visual task the maintainer's machine renders the stored page with headless
Chromium (Edge, Chrome or Chromium; `MENGINE_BENCH_BROWSER` overrides it) and the
judge sees three frames, each from a fresh load after about 1, 4 and 8 seconds of page time, next to
a reference page, made by Opus 5.5 xhigh for the same brief, which sets the bar and stays fixed so a grade does not move when a new run comes out. A frame that fails is
tried up to 3 times; if it keeps failing, the judge votes on the other frames, or without images when none rendered, and
the bundle records it. With no browser at all, nothing is judged.

The judge reads the task prompt, the check results, the final answers, each page whole, the agent's other changes
and one tool log with the same shape for every harness. It does not read the raw stream, which carries the model id.

Measured in 1.3.3: two votes on the same message differed by 1.35 points on average and 6 at most (23 pairs), so one
task's vote is noisy and a run's mean of 20 is much less so.
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
(holding only the frames and references for visual tasks) with tools off where the CLI
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

## Estimated cost

A harness reports cost only on some runs, so the leaderboard's Cost falls back to pricing the run the same way for all:
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
- Score = 0.6 x 53.3 + 0.15 x 56.7 + 0.25 x 32.0 x 53.3 / 100 = 44.7
- Cost = 0.40 + 0.90 = >= $1.30 (harness), a lower bound because C has no usage

With `--price input=1.25,cached=0.125,output=10`, a Codex step of 2,000,000
input tokens (1,500,000 cached) and 100,000 output tokens costs
(500,000 x 1.25 + 1,500,000 x 0.125 + 100,000 x 10) / 1,000,000 = $1.81.

`tests/test_scoring.py` locks these numbers.
