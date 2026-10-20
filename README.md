# mengine-bench

mengine-bench is the coding-agent benchmark of Milton Stiilpen Jr's AI
workstation (mengine), public for contribution and comparison. Run it against
your own agent and model, add tasks, and compare results on a shared
leaderboard.

## Compete: one command

Needs [uv](https://docs.astral.sh/uv/), [gh](https://cli.github.com) logged in
(`gh auth login`), the agent CLI you want to measure, installed and logged
in, and a Chromium-family browser (Edge, Chrome, Chromium) so the two visual
tasks get screenshotted. No judge needed: the maintainer judges every run on
review (see [Judging](#judging)).

```
git clone https://github.com/owlmsj/mengine-bench.git
cd mengine-bench
uv sync
uv run mengine-bench run --agent codex --model gpt-6.1-sol --effort low --dry-run   # plan + preflight, runs nothing
uv run mengine-bench run --agent codex --model gpt-6.1-sol --effort low --submit    # ~30 min, then opens the PR
```

`--agent` is `claude`, `codex`, `opencode` or `cmd` (any command, see Quick
start); `--model` is the id that CLI accepts (opencode: `provider/model`).
The dry run must print `"preflight": "clean"`; fix every `preflight:` line
first ([Run hygiene](#run-hygiene)). With `--submit`, a clean run that ends
with `privacy check: clean` is pushed (only its bundle, authored as your
GitHub noreply address) to a branch of your fork, or of this repo if you can
push to it, and the pull request opens with the scores filled in. To read the
bundle before publishing, leave out `--submit` and run
`uv run mengine-bench submit results/full/<bundle>` afterwards.

## Or let your agent do it: copy this prompt

Paste this into a **new session** of the agent you want to measure (Claude
Code, Codex CLI, opencode, ...), started in a folder of your choice. Give that
session permission to run long commands and use the network.

````text
Benchmark yourself with mengine-bench (https://github.com/owlmsj/mengine-bench)
and submit the result. The agent under test is the harness you are running in
plus the model you are running on. Report only values copied from command
output; if something fails or is unclear, stop and show me instead of
guessing. Never print or commit credentials, environment variables or my
personal data.

1. Find your harness (claude, codex or opencode), the exact model id that CLI
   accepts (opencode: provider/model) and your effort, if any.
2. If the current folder is not a clone of mengine-bench, run
   `git clone https://github.com/owlmsj/mengine-bench.git` and cd into it.
   Then `uv sync`.
3. Run `uv run mengine-bench run --agent <harness> --model <model> [--effort
   <effort>] --dry-run` and show me the output. If it prints `preflight:`
   lines, wait until I fix them (README, "Run hygiene", has the commands) and
   say "go"; never delete, move or edit those files yourself, and never use
   --allow-unclean.
4. Run the same command without `--dry-run`. It takes 20 to 40 minutes: run it
   in the background or without a timeout and wait for it to finish. Do not
   help the agent under test or touch its files. It must end with
   `privacy check: clean`.
5. Skim results/full/<bundle>/summary.md and the transcripts for anything
   private the check cannot know (my name, company, clients, private
   projects). If you find any, stop and tell me. Otherwise run
   `uv run mengine-bench submit results/full/<bundle>` and reply with the
   scores and the pull request URL.
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
only say where output files go and what the answer must contain.

Every task ships a reference solution, and the test suite proves without any
model that the reference passes and the untouched workspace fails.

## Suites

| Suite | Tasks |
| --- | --- |
| FAST | 14 |
| FULL | 20 |

FAST already contains all six weight-2 tasks. FULL adds six weight-1 tasks.
Measured runs, with their agent times, are on [LEADERBOARD.md](LEADERBOARD.md).

A run declares its suite. Results are only compared within the same suite,
scoring version, judge and visual grading profile, and only runs of the
current bench are ranked. The two bench 0.1.0 runs (Codex gpt-6.1-sol low and
opencode DeepSeek V4 Flash low, FULL) were retired with 0.2.0: their prompts
limited tools and they started without the preflight. They stay in git
history (`git show fde6c16:LEADERBOARD.md`).

## Tasks

One entry per task: suites, weight (2 = HARD), par time, what it measures and the scenario it is
modeled on. Generated from the catalog; par time provenance and multi-step rules are in
[docs/TASKS.md](docs/TASKS.md).

<!-- task-summaries:begin (generated by `mengine-bench tasks-doc --readme`) -->
| id | category | TL;DR |
| --- | --- | --- |
| `ds-ab-playtest` | data-science | Compare two game tutorials using player data and decide which one to release. |
| `bo-pnl-runway` | backoffice | Calculate monthly profit, cash burn and how long the business can keep running from its ledger. |
| `bo-reconcile` | backoffice | Match invoices to bank payments and report missing, duplicate or incorrect payments. |
| `cmp-handoff` | compaction | Summarize a debugging session, then answer questions using only that summary. |
| `lc-changelog` | long-context | Find when a setting changed and was restored in a long changelog, including who approved the change. |
| `vis-chart` | vision | Read a bar chart to identify the fastest and slowest GPUs and compare their speeds. |
| `ds-sql-funnel` | data-science | Count players at each ordered funnel step in SQLite, excluding test accounts and duplicates, by platform. |
| `gd-astar-doors` | gamedev | Implement the cheapest route across a game map where doors cost more to cross. |
| `gd-ecs-collision-bug` | gamedev | Fix movement and box collision bugs in a small game codebase without changing its tests. |
| `ir-studio-wiki` | retrieval | Find release and game details across a studio wiki and cite the files that support each answer. |
| `ir-server-logs` | retrieval | Read game server logs to explain an outage and calculate downtime and monthly availability. |
| `gd-integration-repo` | gamedev | Fix configuration priority and saved player credits in a game server without changing existing tests. |
| `web-mondrian-landing` | web-design | Build a Mondrian-style landing page about one painting from a local fact sheet, in one request |
| `3d-voxel-landscape` | 3d | Build a three.js low poly or voxel scene of Mount Fuji with a pagoda and cherry trees, in one request |
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

## Judging

Runs are judged by the maintainer, not by the competitor, so every ranked run
has the same judge (Claude `claude-opus-5-5` at `xhigh`, 3 votes) and you need
no judge of your own. A run without a judge (the default) stores the judge's
evidence in its bundle, redacted like the rest: `judge/<task>.json` (task
prompts, answers, workspace diff, transcript tail, check results) and, for
the visual tasks, the screenshot `judge/<task>.png`. Its `summary.md` says
"judge pending", and the leaderboard lists it apart until judged.

While reviewing the pull request, the maintainer runs:

```
uv run mengine-bench judge results/full/<bundle>
```

It runs the subjective rubric on every task and the vision checklist on the
stored screenshots (which finishes the visual tasks' objective grade, exactly
as a judge during the run would), recomputes every score, and rewrites
`result.json` and `summary.md` with `"deferred": true` on the judge. Until
then, visual tasks count as unrendered. `run --judge claude` still judges
during the run if you prefer, with your own Claude account.

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

`--suite` defaults to `full`. `--tasks a,b` runs a subset. Each run writes one result bundle to
`results/<suite>/<date>_<agent>_<model>_<effort>_<run id>/`:

| file | content |
| --- | --- |
| `result.json` | scores, every check with its result, answers, step timings, judge votes with rationales, vision ballots, environment (OS, CPU, RAM, GPU, agent CLI and version, model, effort, judge), bench version and commit, submitter, start and finish time (UTC) |
| `summary.md` | human summary |
| `transcripts/<task>.jsonl.gz` | the raw agent output of every step |

Agents run with permission prompts bypassed (Claude `bypassPermissions`,
Codex `--dangerously-bypass-approvals-and-sandbox`, opencode `--auto`), in
fresh workspaces under the system temp dir. Each step has the task's timeout;
on timeout the whole agent process tree is killed.

## Run hygiene

A run must start clean and publish nothing private. The bench enforces what
it can; the rest is on you.

**Clean start (enforced).** Before launching anything, `run` (and
`run --dry-run`) prints a `preflight:` line for each of these and refuses to
start:

- your harness's personal instructions: `~/.claude/CLAUDE.md` (Claude Code,
  and opencode reads it too), `~/.codex/AGENTS.md` and `AGENTS.override.md`
  (Codex, or under `CODEX_HOME`), `~/.config/opencode/AGENTS.md`. They would
  steer the agent and leak into the transcripts. Move them aside for the run;
- a `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` or `AGENTS.override.md` in the
  temp dir or any folder above it, or a git checkout around it: harnesses load
  those too;
- earlier runs on disk (`<temp>/mengine-bench/runs/*`,
  `<temp>/mengine-bench-fresh-*`): an agent could read other solutions.
  Delete them.

To move the personal instruction files aside before a run, and back after it
(default locations; with `CODEX_HOME` or `CLAUDE_CONFIG_DIR` set, use the path
the `preflight:` line prints):

```powershell
# PowerShell, before the run
$bak = "$HOME/mengine-bench-preflight-backup"
$files = ".claude/CLAUDE.md", ".codex/AGENTS.md", ".codex/AGENTS.override.md", ".config/opencode/AGENTS.md"
foreach ($f in $files) { if (Test-Path "$HOME/$f") { New-Item -ItemType Directory -Force (Split-Path "$bak/$f") | Out-Null; Move-Item "$HOME/$f" "$bak/$f" } }
# after the run (same $bak and $files)
foreach ($f in $files) { if (Test-Path "$bak/$f") { Move-Item "$bak/$f" "$HOME/$f" } }
```

```bash
# bash or zsh, before the run
bak=~/mengine-bench-preflight-backup
files=".claude/CLAUDE.md .codex/AGENTS.md .codex/AGENTS.override.md .config/opencode/AGENTS.md"
for f in $files; do [ -f ~/"$f" ] && mkdir -p "$bak/$(dirname "$f")" && mv ~/"$f" "$bak/$f"; done
# after the run (same bak and files)
for f in $files; do [ -f "$bak/$f" ] && mv "$bak/$f" ~/"$f"; done
```

`--allow-unclean` starts anyway, records the findings in `result.json` and
`summary.md`, and the leaderboard never ranks that run. Each agent also gets an
`AGENTS.md` in its workspace: use any tool, read and write local files only
inside the workspace, print no credentials or personal data. Tools are not
restricted (see "What it measures"), but tools that read your private data
(mail, drive, chat, password managers) can pull it into the transcripts:
disconnect them for the run.

**Nothing private is published (enforced, then checked).** Transcripts,
`summary.md` and `result.json` are redacted before they are written:

- secret-looking values become `[REDACTED:<kind>]`, and so does the exact
  value of every environment variable whose name marks a secret (`*_API_KEY`,
  `*_TOKEN`, `*_SECRET`, `*PASSWORD*`, `*_AUTH`, ...), wherever it appears;
- e-mail addresses are dropped (placeholders and GitHub noreply stay);
- home directories, the run directories, this machine's account and host
  names and your git author name become `<HOME>`, `<WORKSPACE>`,
  `<WORKDIR>`, `<USER>`, `<HOST>` and `<NAME>`; the `--submitter` credit is
  kept because you chose to publish it;
- base64 images become a hash.

The raw run directory (unredacted) is deleted once the bundle is written,
unless you passed `--work`. Then `run` scans the bundle again and ends with
`privacy check: clean`, or names each file and leak kind (never the leaked
text) and exits non-zero: do not publish that bundle. Redaction cannot know
your company, clients or private projects, so still use throwaway API keys
and skim the transcripts before you open the pull request.

Multi-step tasks: a `fresh_session` step starts a new agent process; any
other step resumes the session (claude `--resume`, codex `exec resume`,
opencode `--session`). The `cmd` adapter cannot resume, so such tasks are
reported "unsupported" (scored 0). A fresh-session step starts in a new
workspace holding only the files the task carries over; `hide` moves files
out of the workspace before a step; `compact_before` compacts the session
first (Claude Code only). Visual tasks need a Chromium-family browser
(`MENGINE_BENCH_BROWSER`, PATH, or the standard Edge/Chrome install
locations) during the run and a vision judge (during the run or later, see
[Judging](#judging)). A run with no browser stays "unrendered": visual tasks
are never solved there (correctness capped at 0.5) and the leaderboard ranks
such runs in their own table.

## Submitting results

`run --submit` or `submit <bundle>` (see [Compete](#compete-one-command)) is
the whole flow. It refuses a bundle from another bench version, one whose run
did not start clean, or one that fails the privacy check. The commit holds
the bundle and nothing else, on top of this repo's `main`, built with a
temporary index (your checkout, branch and index are untouched). By hand
works too: a pull request that adds only your `results/<suite>/<bundle>/`
directory. Do not edit LEADERBOARD.md.

There is no CI and no bot. The maintainer reviews every pull request by hand,
may edit it, regenerates [LEADERBOARD.md](LEADERBOARD.md) with
`uv run mengine-bench leaderboard` and merges. Questions about a result: open
an issue naming the bundle directory.

## Known limitations

- Scores, timings, agent and model identity, and judge votes are
  self-reported. The bundle records every check, answer and vote, and the
  transcripts let anyone sanity-check a run, but nothing re-runs it.
- Runs are only compared within the same suite, scoring version, judge and
  visual grading profile; a run of an older bench, a run that is not exactly
  its suite's task set (a `--tasks` subset), one that started unclean or one
  that waits for the judge is listed apart and never ranked.
- The workspace boundary is an instruction, not a sandbox: an agent with
  bypassed permissions can still read the rest of the disk, or find this
  public repo on the web. The transcripts show it if it does, and the
  maintainer rejects such runs.
- Some gold checks are lenient: they accept a few wrong answers that look
  right.

## License

MIT, see [LICENSE](LICENSE).
