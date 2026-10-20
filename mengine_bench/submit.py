"""Submit a result bundle as a pull request to the public repo, in one command.

The commit holds the bundle and nothing else, on top of the upstream main. It
is built with a temporary git index, so the local checkout (branch, index,
working tree) is untouched, and it is authored as the logged-in gh user's
GitHub noreply identity, so no personal e-mail lands in public git history.
Accounts with push access push the branch upstream; everyone else pushes to
their fork, which `gh repo fork` creates when missing.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path

from mengine_bench import __version__
from mengine_bench.bundle import RESULT_NAME, bundle_leaks
from mengine_bench.redact import local_names
from mengine_bench.report import cost_text, time_text

UPSTREAM = "owlmsj/mengine-bench"
UPSTREAM_BRANCH = "main"
PUSH_HINT = "if git asked for credentials, run `gh auth setup-git` once and retry `mengine-bench submit <bundle>`"


class SubmitError(RuntimeError):
    """The bundle cannot be submitted, or a git/gh step failed."""


def _call(argv: list[str], cwd: Path | None = None, env: Mapping[str, str] | None = None) -> str:
    executable = shutil.which(argv[0])
    if executable is None:
        raise SubmitError(f"received no {argv[0]!r} on PATH; expected git and gh (https://cli.github.com), logged in")
    done = subprocess.run([executable, *argv[1:]], cwd=cwd, env=None if env is None else {**os.environ, **env},
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
                          check=False)
    if done.returncode:
        raise SubmitError(f"`{' '.join(argv[:3])}` exited {done.returncode}: {done.stderr.strip()[-600:]}")
    return done.stdout.strip()


def gh_login() -> str:
    """The logged-in GitHub account; fails early, before a 30-minute run."""
    return _call(["gh", "api", "user", "--jq", ".login"])


def submission_problems(bundle: Path, result: Mapping[str, object]) -> list[str]:
    """Why this bundle must not be published (empty when it can be)."""
    problems = []
    if result.get("bench_version") != __version__:
        problems.append(f"received bench {result.get('bench_version')}; expected {__version__}: run with this bench")
    if result.get("preflight") != []:
        problems.append("the run did not start clean (result.json `preflight`); fix it and run again")
    submitter = result.get("submitter")
    names = local_names().allowing(submitter if isinstance(submitter, str) else None)
    problems += [f"privacy check: {name}: {', '.join(sorted(kinds))}" for name, kinds in
                 bundle_leaks(bundle, names).items()]
    return problems


def pr_title(result: Mapping[str, object]) -> str:
    agent = result["agent"]
    assert isinstance(agent, dict)
    return (f"results: {agent['name']} {agent['model']} "
            f"{agent.get('effort') or 'default effort'}")


def pr_body(result: Mapping[str, object]) -> str:
    agent, totals, environment = result["agent"], result["totals"], result["environment"]
    judge, commit = result.get("judge"), result.get("bench_commit")
    assert isinstance(agent, dict) and isinstance(totals, dict) and isinstance(environment, dict)
    judge_text = "pending: the maintainer runs `mengine-bench judge` on review"
    if isinstance(judge, dict):
        judge_text = f"{judge.get('model')}@{judge.get('effort')}, rubric {judge.get('rubric')}"
    commit_text = (f"{commit.get('sha')} (dirty: {commit.get('dirty')})" if isinstance(commit, dict) else "unknown")
    rows = [
        ("agent CLI and version", f"{agent['name']} {agent.get('version') or 'unknown'}"),
        ("model id", agent["model"]),
        ("effort", agent.get("effort") or "default"),
        ("judge", judge_text),
        ("Correct % / solved", f"{totals['correct']} / {totals['solved']}/{totals['total']}"),
        ("Judge / Score", f"{totals.get('judge')} / {totals.get('score')} (set by the maintainer's judge)"),
        ("Time", time_text(totals.get("time_s"))),
        ("Cost", cost_text(totals)),
        ("wall time", f"{result.get('started_at')} to {result.get('finished_at')}"),
        ("bench version and commit", f"{result['bench_version']} at {commit_text}"),
        ("machine", f"{environment.get('os')}, {environment.get('cpu')}, {environment.get('ram_gb')} GB RAM, "
                    f"GPU {environment.get('gpu') or 'none'}"),
        ("preflight / privacy check", "clean / clean"),
    ]
    table = "\n".join(f"| {name} | {value} |" for name, value in rows)
    return ("Adds one result bundle, written by `mengine-bench run` and submitted with `mengine-bench submit`; "
            "nothing else changes.\n\n| field | value |\n| --- | --- |\n" + table + "\n")


def commit_bundle(repo: Path, bundle: Path, base: str, message: str, author: tuple[str, str]) -> str:
    """A commit of `base` plus the bundle dir, via a temporary index; returns its sha."""
    relative = bundle.resolve().relative_to(repo.resolve()).as_posix()
    name, email = author
    with tempfile.TemporaryDirectory(prefix="mengine-bench-submit-") as tmp:
        env = {"GIT_INDEX_FILE": str(Path(tmp) / "index"), "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email,
               "GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": email}
        _call(["git", "read-tree", base], cwd=repo, env=env)
        _call(["git", "add", "--force", "--", relative], cwd=repo, env=env)
        tree = _call(["git", "write-tree"], cwd=repo, env=env)
        return _call(["git", "commit-tree", tree, "-p", base, "-m", message], cwd=repo, env=env)


def submit(bundle: Path) -> str:
    """Push the bundle on its own branch and open the pull request; returns the PR URL."""
    bundle = bundle.resolve()
    result = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    problems = submission_problems(bundle, result)
    if problems:
        raise SubmitError("received a bundle that cannot be published:\n- " + "\n- ".join(problems))
    repo = Path(_call(["git", "rev-parse", "--show-toplevel"], cwd=bundle)).resolve()
    parts = bundle.relative_to(repo).parts
    if len(parts) != 2 or parts[0] != "results":
        raise SubmitError(f"received bundle {bundle}; expected <bench clone>/results/<bundle>")
    user = json.loads(_call(["gh", "api", "user"]))
    login = str(user["login"])
    author = (login, f"{user['id']}+{login}@users.noreply.github.com")
    can_push = _call(["gh", "api", f"repos/{UPSTREAM}", "--jq", ".permissions.push"]) == "true"
    target = UPSTREAM if can_push else f"{login}/{UPSTREAM.split('/')[1]}"
    if not can_push:
        _call(["gh", "repo", "fork", UPSTREAM, "--clone=false", "--remote=false"])
    _call(["git", "fetch", "--quiet", f"https://github.com/{UPSTREAM}.git", UPSTREAM_BRANCH], cwd=repo)
    base = _call(["git", "rev-parse", "FETCH_HEAD"], cwd=repo)
    sha = commit_bundle(repo, bundle, base, pr_title(result), author)
    branch = f"results/{bundle.name}"
    try:
        _call(["git", "push", "--quiet", f"https://github.com/{target}.git", f"{sha}:refs/heads/{branch}"], cwd=repo)
    except SubmitError as error:
        raise SubmitError(f"{error}\n{PUSH_HINT}") from error
    return _call(["gh", "pr", "create", "--repo", UPSTREAM, "--base", UPSTREAM_BRANCH,
                  "--head", f"{target.split('/')[0]}:{branch}", "--title", pr_title(result),
                  "--body", pr_body(result)])
