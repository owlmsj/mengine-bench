# mengine-bench

mengine-bench is the coding-agent benchmark of Milton Stiilpen Jr's AI
workstation (mengine), public for contribution and comparison. Run it against
your own agent and model, add tasks, and compare results on a shared
leaderboard.

## Benchmark your own agent: copy this prompt

Paste the prompt below into a **new session** of the coding agent you want to
measure (Claude Code, Codex CLI, opencode, ...). The agent runs the FULL suite
against its own harness and model and opens a pull request from your fork.
It spends model tokens (the published FULL runs took 20 to 28 minutes of wall
time) and runs agents with permission prompts bypassed, so use a disposable
machine or account.

````text
You are a coding agent in a fresh session. Benchmark yourself with
mengine-bench (https://github.com/owlmsj/mengine-bench): the agent under test
is the harness you are running in plus the model you are running on. Then
submit the result as a pull request. Report only values copied from command
output or from result.json; write "unknown" for anything you cannot read.
If something fails or is unclear, stop and ask me instead of guessing.

1. Identify the run and confirm it with me before spending tokens:
   - harness: claude, codex or opencode, and its exact `--version`;
   - model: the exact model id that CLI accepts (opencode: provider/model)
     and the effort, if any;
   - my GitHub login: `gh api user --jq .login`;
   - judge: claude-opus-5-5 at xhigh with 3 votes if the Claude Code CLI is
     installed and logged in, otherwise none;
   - whether a Chromium-family browser is installed (visual tasks need it).
   Show me the command you will run and wait for my "go".
2. `gh repo fork owlmsj/mengine-bench --clone`, cd into it, `uv sync`.
3. Run the suite once, exactly as confirmed:
   `uv run mengine-bench run --suite full --agent <agent> --model <model>
   --effort <effort> --judge claude --judge-model claude-opus-5-5
   --judge-effort xhigh --judge-votes 3 --submitter <github login>`
   (`--judge none` without the other judge flags if there is no judge).
   Do not help the agent, edit its workspaces or rerun single tasks.
4. Read summary.md and skim the transcripts for secrets, tokens or personal
   data; if you find any, stop and tell me. Do not edit the bundle.
5. On a new branch `results-<agent>-<model>-<date>`, commit only the new
   `results/full/<bundle>/` directory and open the pull request with
   `gh pr create --repo owlmsj/mengine-bench`, filling the template from
   result.json (agent, model, effort, judge, totals, bench version and
   commit, wall time from started_at to finished_at).
   Reply to me with the PR URL.
````

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

The agent may use every tool its harness gives it: shell, web search and
fetch, browsers, MCP servers, skills, subagents. Nothing is turned off; what
is measured is the harness plus the model as you configured them. Prompts
only say where output files go and what the answer must contain. Bench 0.1.0
prompts told agents to avoid tools on some tasks, so the two 0.1.0 baselines
below are not strictly comparable with 0.2.0 runs.

Every task ships a reference solution, and the test suite proves without any
model that the reference passes and the untouched workspace fails.

## Suites

| Suite | Tasks | Measured run |
| --- | --- | --- |
| FAST | 14 | FAST has no measured run yet |
| FULL | 20 | 20 min 10 s wall (510 s agent time), baseline below |

FAST already contains all six weight-2 tasks. FULL adds six weight-1 tasks.

The 2026-10-17 FULL baseline used Codex gpt-6.1-sol at low effort and a
judge with 1 vote, as its bundle records (Claude `claude-opus-5-5`, xhigh
effort). It took 20 min 10 s wall (510 s agent time); judging and grading are
excluded from agent time.
Both visual tasks were rendered in a browser and graded by the vision judge
(1 vote each).
This is one measured configuration, not a duration estimate for other agents.

The 2026-10-19 FULL baseline used opencode 2.0.29 with DeepSeek V4 Flash
(`deepseek/deepseek-flash`, variant `low`) and the same judge (1 vote). It took
27 min 57 s wall (1,466 s agent time).

| | gpt-6.1-sol low (Codex) | DeepSeek V4 Flash low (opencode) |
| --- | --- | --- |
| OBJECTIVE / ACCURACY | 94.3 / 96.3 | 92.8 / 95.5 |
| solved | 18/20 | 18/20 |
| SUBJECTIVE / COMPOSITE | 88.5 / 92.0 | 86.5 / 90.3 |
| agent time, 18 non-web tasks | 336.9 s | 388.5 s (faster on 10 of 18) |
| agent time, 2 web build tasks | 142.1 s | 1,077.1 s |
| misses | bo-reconcile 0.50, ir-server-logs 0.83, 3d-voxel 0.86 | vis-chart 0.00 (image withheld: the opencode config declared the model text-only; the DeepSeek API reads images), ir-server-logs 0.83 |

Both runs are on [LEADERBOARD.md](LEADERBOARD.md).

A run declares its suite. Results are only compared within the same suite,
scoring version, judge and visual grading profile.

## Tasks

One entry per task: suites, weight (2 = HARD), par time, what it measures and the scenario it is
modeled on. Generated from the catalog; par time provenance and multi-step rules are in
[docs/TASKS.md](docs/TASKS.md).

<!-- task-summaries:begin (generated by `mengine-bench tasks-doc --readme`) -->
**data-science**

- `ds-ab-playtest` (FAST, FULL; weight 1; par 25 s): Deduplicate telemetry, per-variant rates, lift, two-proportion z-test and ship decision. Scenario: Pixel Arena playtest A/B (arena-panel telemetry); two-proportion z-test on a dirty export.
- `ds-sql-funnel` (FAST, FULL; weight 2; par 23 s): HARD: ordered funnel with a 7-day window per step in SQLite, per platform. Scenario: Product funnel in SQL: ordered steps, 7-day window per step, test accounts, dupes, out-of-order events.

**backoffice**

- `bo-pnl-runway` (FAST, FULL; weight 1; par 28 s): Build a monthly P&L (revenue, COGS, margin, opex, EBITDA) from a Brazilian-format ledger and compute burn and runway. Scenario: Startup monthly close: P&L from a Brazilian-format ledger (`;`, 1.234,56) + chart of accounts, burn and runway.
- `bo-reconcile` (FULL; weight 1; par 55 s): Reconcile invoices with a bank statement: unpaid, duplicated and mismatched. Scenario: Accounts receivable reconciliation: invoices vs bank statement with PIX/TED memo variants and noise.
- `bo-safe-conversion` (FAST, FULL; weight 2; par 51 s): HARD: Series A round with pool top-up and conversion of 3 SAFEs (circular computation). Scenario: Series A math: post-money pool top-up in the pre-money plus SAFE conversion (circular, fixed point).

**compaction**

- `cmp-handoff` (FAST, FULL; weight 1; par 20 s): Compact a debugging session into HANDOFF.md <=1500 chars and answer 6 questions from it alone. Scenario: Agent debugging-session handoff on a local LLM server; native retention rules.
- `cmp-meeting-decisions` (FULL; weight 1; par 40 s): Compact a long operations meeting into DECISIONS.md and answer 7 questions from it alone. Scenario: Startup weekly ops meeting: decisions, owners, deadlines, with a debated-then-changed price.
- `cmp-agent-trajectory` (FULL; weight 1; par 40 s): Compact an agent trajectory (160 steps) into STATE.md and answer 5 questions from it alone. Scenario: AMA-Bench style: compact a 160-step agent trajectory (JSONL) and answer from the state only.

**long-context**

- `lc-changelog` (FAST, FULL; weight 1; par 4 s): Find the change and revert of a parameter in a 640-build changelog and cross-reference date/approver. Scenario: AA-LCR style multi-hop over a long build changelog with near-duplicate distractor keys.
- `lc-contract` (FULL; weight 1; par 8 s): Compute the annual cost of 37 seats in a long contract with an amendment and a trap draft. Scenario: Contract review over a long agreement: price amendment supersedes a clause, unsigned draft is a trap.

**vision**

- `vis-chart` (FAST, FULL; weight 1; par 3 s): Read a bar chart: highest/lowest GPU, value and ratio. Scenario: ChartQA style bar chart (golden image chart.png).

**gamedev**

- `gd-astar-doors` (FAST, FULL; weight 1; par 19 s): Implement minimum-cost pathfinding (doors cost 3) on a tile map; hidden tests. Scenario: Terminal-Bench style: implement + hidden tests; A* with weighted doors on a Pixel Arena tile map.
- `gd-ecs-collision-bug` (FAST, FULL; weight 1; par 12 s): Find and fix 2 bugs (movement and AABB collision) in a multi-file ECS without touching the tests. Scenario: SWE-bench style debug: two planted bugs across an ECS package; visible tests must stay untouched.
- `gd-lockstep-desync` (FAST, FULL; weight 2; par 52 s): HARD: make a lockstep simulation deterministic across processes without changing the rules. Scenario: Multiplayer lockstep desync: two nondeterminism sources, one invisible in-process (hash seed).
- `gd-integration-repo` (FAST, FULL; weight 2; par 89 s): ONE-SHOT LONG: ~100-file repo, 3 layered bugs that only the integration test and the spec reveal. Scenario: Long-horizon SWE: ~100-file game backend, 3 layered bugs only visible end to end; spec in docs/.

**retrieval**

- `ir-studio-wiki` (FAST, FULL; weight 1; par 14.6 s): Answer 5 multi-hop facts from a studio wiki with distractors, citing files. Scenario: Internal-wiki QA with multi-hop (bug -> changelog -> approvals) and planted distractors.
- `ir-server-logs` (FULL; weight 1; par 29.2 s): Game server log forensics: incident window, root cause and monthly SLO. Scenario: Game server ops: incident window, root cause and monthly SLO from 3 days of logs.
- `ir-web-facts` (FULL; weight 1; par 29.2 s): Research 4 public facts on the web (llama.cpp, PagedAttention, Linux mascot, Rust 1.0) with sources. Scenario: Stable public web facts (llama.cpp, vLLM paper, Linux mascot, Rust 1.0) with cited sources.

**web-design**

- `web-mondrian-landing` (FAST, FULL; weight 2; par 345 s): ONE-SHOT: research the painting and ship a Mondrian-style landing page; checks + vision checklist. Scenario: One-shot research + front-end: Piet Mondrian's Composition with Red, Blue and Yellow (1930).

**3d**

- `3d-voxel-landscape` (FAST, FULL; weight 2; par 295 s): ONE-SHOT: three.js voxel/low poly scene of Fuji with pagoda and cherry trees; checks + vision checklist. Scenario: One-shot procedural 3D (Design Arena style): Mt. Fuji + Chureito pagoda + sakura in low poly/voxel.
<!-- task-summaries:end -->

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
uv run mengine-bench selftest         # every task's gold, no agent
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
`results/<suite>/<date>_<agent>_<model>_<effort>_<run id>/`:

| file | content |
| --- | --- |
| `result.json` | scores, every check with its result, answers, step timings, judge votes with rationales, vision ballots, environment (OS, CPU, RAM, GPU, agent CLI and version, model, effort, judge), bench version and commit, submitter, start and finish time (UTC) |
| `summary.md` | human summary |
| `transcripts/<task>.jsonl.gz` | the raw agent output of every step |

Before writing, transcripts, `summary.md` and `result.json` are redacted:
secret-looking values become `[REDACTED:<kind>]`, base64 images become a
hash, third-party e-mail addresses are dropped, and home directories, the run
directories and this machine's account and host names become `<HOME>`,
`<WORKSPACE>`, `<WORKDIR>`, `<USER>` and `<HOST>`. Still: run with throwaway
credentials and read your transcripts before publishing.

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

## Submitting results

Use the prompt above, or do it by hand: fork, run a suite, read `summary.md`
and the transcripts, and open a pull request that adds only your
`results/<suite>/<bundle>/` directory. Do not edit LEADERBOARD.md.

There is no CI and no bot. The maintainer reviews every pull request by hand,
may edit it, regenerates [LEADERBOARD.md](LEADERBOARD.md) with
`uv run mengine-bench leaderboard` and merges. Questions about a result: open
an issue naming the bundle directory.

## Known limitations

- Scores, timings, agent and model identity, and judge votes are
  self-reported. The bundle records every check, answer and vote, and the
  transcripts let anyone sanity-check a run, but nothing re-runs it.
- Runs are only compared within the same suite, scoring version, judge and
  visual grading profile; a run that is not exactly its suite's task set (a
  `--tasks` subset) is listed apart and never ranked.
- Some gold checks are lenient: they accept a few wrong answers that look
  right.

## License

MIT, see [LICENSE](LICENSE).
