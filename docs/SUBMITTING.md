# Submitting results

Anyone can add a run of their agent (harness + model) to the leaderboard. A
submission is one **result bundle**: a directory written by
`mengine-bench run` that holds everything needed to audit the run.

## 1. Run

```
uv sync
uv run mengine-bench run --suite fast --agent claude --model <model-id> --effort high \
    --judge claude --judge-model claude-opus-5-5 --judge-effort xhigh \
    --submitter "your name or handle (optional, public)"
```

Run from a clean checkout of a released bench version: the bundle records the
bench commit and whether the tree was dirty. The judge is optional; without
it the run has an OBJECTIVE score only.

The bundle lands in `results/<suite>/<YYYY-MM-DD>_<agent>_<model>_<effort>_<run id>/`:

| file | content |
| --- | --- |
| `result.json` | scores, raw per-task data (step timings, every check with name and result, c/s/o, answers, judge votes with rationales, vision ballots, flags such as "no browser", "unsupported", "timeout"), environment (OS, CPU, RAM, GPU if detectable, agent CLI and version, model id, effort, judge model, effort and votes), bench version and commit, scoring version, submitter, start and finish time (UTC) |
| `summary.md` | human summary |
| `transcripts/<task>.jsonl.gz` | the raw agent output of every step, one JSON line per step and stream |
| `workspaces/<task>.tar.gz` | the final workspace of every task |
| `MANIFEST.sha256` | sha256 of every other file |

The schema of `result.json` is [result.schema.json](result.schema.json).

### What the bundle leaves out

- **Secrets.** Transcripts and `result.json` are redacted before writing:
  env-var-looking assignments (`*_KEY=`, `*TOKEN=`, `*SECRET=`,
  `*PASSWORD=`), OpenAI/Anthropic-style `sk-` keys, GitHub, Slack, AWS and
  Google key patterns, bearer tokens and private key blocks become
  `[REDACTED:<kind>]`. A workspace file that contains such a pattern is
  dropped from the archive (workspaces must stay byte-exact to be re-graded),
  and listed as excluded in `result.json`. Still: run with throwaway
  credentials and read your transcripts before publishing.
- **Images.** Base64 image blobs in transcripts become
  `[image sha256=<hex> bytes=<n>]`.
- **Local paths and names.** Transcripts, `summary.md` and `result.json`
  are scrubbed of: each task's step workspace (`<WORKSPACE>`), the run
  directory (`<WORKDIR>`), any home directory (`Users\<name>` under any
  Windows drive letter, with backslashes or slashes, in any JSON-escaped form;
  `/home/<name>`; `/Users/<name>`) as `<HOME>`, and your account and machine
  names as whole tokens (`<USER>`, `<HOST>`). Recorded answers and check
  names are scrubbed of paths only, because `verify` re-grades them
  verbatim. Workspace archives are left byte-exact.
- **Caches and big files.** Workspace archives skip `.git`, `node_modules`,
  `.venv`, `venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`,
  `.ruff_cache`, `.cache`, browser profiles, and any file over **1 MiB**
  (listed as excluded).

**Size limit:** a bundle may be at most **25 MiB** (26,214,400 bytes) in
total. `verify` and the results workflow reject anything bigger.

## 2. Verify locally

```
uv run mengine-bench verify results/fast/<your bundle>
```

It prints one line per item and exits non-zero on any FAIL:

| item | how | status |
| --- | --- | --- |
| `manifest` | every file hashed and listed, nothing extra | re-derived |
| `size` | bundle at most 25 MiB | re-derived |
| `unpack` | all archives and transcripts together inflate to at most 200 MB and 5000 tar members; tar members are relative regular files (no backslash, drive, UNC, absolute or `..` names, no links or devices); on a violation verify stops here | re-derived |
| `secrets` | no unredacted secret pattern in transcripts, result, summary or workspaces | re-derived |
| `paths` | no home path (any form above) in transcripts, `summary.md` or `result.json`, and, when run locally (not on CI, where the names are the runner's), none of this machine's account or host name; reports file and count, never the matched text | re-derived |
| `schema` | `result.json` matches the JSON schema | re-derived |
| `bench_version` | the bundle's bench version equals the checkout's | re-derived |
| `suite` | the task ids are unique (duplicates FAIL) and exactly the declared suite's set; any other set is PARTIAL: verified but listed apart and never ranked | re-derived |
| `checks:<task>` | the task's deterministic checks re-run on the extracted saved workspace with the recorded answers; the recorded checks must be the exact ordered list of (name, ok, mandatory) the task produces, each check once; every graded task (status `ok`) must carry its checks and its workspace archive; weight and par time must match the catalog; check score, mandatory gates and pass flag must follow from the checks | re-derived |
| `scores` | OBJECTIVE, ACCURACY, SUBJECTIVE, COMPOSITE, solved, total agent time and every task's c/s/o recomputed with `scoring.py` (tolerance 0.05) | re-derived |
| `timings` | step times sum to each task's agent time | SELF-REPORTED |
| `vision` | ballot counts and sizes, and each checklist result is the majority of the ballots | SELF-REPORTED |
| `judge` | vote counts within the configured votes, one rationale per vote, subjective is the median | SELF-REPORTED |

Visual tasks are re-graded without a browser: their deterministic gates are
re-derived; the screenshot gate and the vision checklist items are covered by
the `vision` item instead.

### Fixing a bundle before submission: `rebundle`

If `verify` fails on `paths` or `secrets` (for example a bundle written by
an older bench that missed a path form), rebuild it from the raw run
directory instead of rerunning:

```
uv run mengine-bench rebundle <raw run dir> --out results/
```

The raw run directory is the `--work` dir that `run` prints ("raw workspaces
in ..."; by default `<temp>/mengine-bench/runs/<timestamp>`). It holds each
task's transcripts and workspaces, and `run.json`: the recorded results
(scores, checks, answers, timings, judge votes and rationales, vision
ballots). `rebundle` applies the current redaction and writes a new bundle
and manifest; it runs no agent and no judge, so every score stays the
recorded one. The bundle directory name is the same as before, so point
`--out` at a fresh directory or delete the old bundle first.

Runs made before `run.json` existed lack the recorded results; `rebundle`
says so. For those, pass the old bundle's result as the source of that data:
`--result <old bundle>/result.json` (the final workspace is then taken from
the highest `step-<n>` directory of each task).

## 3. Open a pull request

- Add **exactly one** bundle directory under `results/<suite>/`, unedited.
  Do not touch other bundles, code or docs in the same PR.
- **Do not edit LEADERBOARD.md.** It is regenerated on `main` after merge.
- Fill the PR checklist (agent CLI version, model id, effort, judge).

CI (`.github/workflows/results.yml`) first enforces the results-only policy
(`.github/scripts/check_submission.py`): every changed path must be a newly
added file inside one `results/<suite>/<bundle>/` directory. A PR that also
changes code, docs, workflows or LEADERBOARD.md, modifies or renames an
existing bundle, or adds more than one bundle fails. It then enforces the size
limit and runs `mengine-bench verify` on the bundle with the bench code of the
**base branch** (not the code in your PR), with a read-only token, no
persisted checkout credentials and no secrets, and posts the verify report as
the job summary. Any FAIL fails the PR.

Note that verification executes the hidden gold tests against the code in
your saved workspaces. That is the point of the audit, and why CI runs it with
read-only permissions and no secrets.

Changes to `.github/` (workflows, this policy script) and to `mengine_bench/`
go in a separate PR and need maintainer review (`.github/CODEOWNERS`, with
"require review from code owners" on `main`). A pull request runs the
workflow file from the PR itself, so that review, not the workflow, is what
keeps a submission from rewriting its own checks.

After merge, `main` regenerates LEADERBOARD.md in two jobs. `verify-main`
re-verifies every bundle (running submission code) with a read-only token
and uploads `verification.json` as an artifact. `publish`, the only job with
`contents: write`, never runs submission code: it downloads that report and
runs `mengine-bench leaderboard --from-report verification.json`, which reads
`result.json` files and the report only (a bundle whose `result.json` hash
differs from the report, or that the report does not list, is skipped), then
commits LEADERBOARD.md. Locally, `mengine-bench leaderboard` does both steps
in one process.

Git stores `results/**` byte for byte (`.gitattributes`: `-text`), because
`MANIFEST.sha256` hashes raw bytes and a CRLF checkout (Windows
`core.autocrlf=true`) would break verification. If you cloned before that
rule existed, re-clone before verifying.

## What is audited and what is trusted

- **Audited** (re-derived from the bundle): deterministic task results and
  every score computed from them.
- **Self-reported** (internally consistent and sealed by the manifest, but
  not re-derivable without rerunning the models): wall times, so the speed
  term; judge votes, so SUBJECTIVE and COMPOSITE; vision checklist ballots.
  The transcripts are there so anyone can sanity-check them.

Disputes or questions about a result: open a
["Result question" issue](../.github/ISSUE_TEMPLATE/result_question.yml)
naming the bundle directory.

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

## Reproducing someone's result

1. Check out the bench commit recorded in their `result.json`
   (`bench_commit.sha`) and run `uv sync`.
2. `uv run mengine-bench verify results/<suite>/<their bundle>` re-derives
   the audited part.
3. To reproduce the run itself, use the same agent CLI version, model id and
   effort from `environment`, and the same judge model, effort and votes:

   ```
   uv run mengine-bench run --suite <suite> --agent <agent> --model <model> --effort <effort> \
       --judge <judge agent> --judge-model <judge model> --judge-effort <judge effort> --judge-votes <n>
   ```

   Model outputs vary between runs, so compare scores with the run-to-run
   spread in mind, not as exact numbers. Timings depend on the host and the
   provider's load.
