"""One-command submission: what may be published, the bundle-only commit, and where it is pushed."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from mengine_bench import __version__, cli, submit
from mengine_bench.submit import SubmitError

GIT = shutil.which("git")


def _result(**overrides: object) -> dict[str, object]:
    result: dict[str, object] = {
        "bench_version": __version__, "preflight": [], "submitter": "dquill",
        "agent": {"name": "codex", "model": "gpt-x", "effort": "low", "version": "codex-cli 1.0"},
        "judge": None,
        "totals": {"score": 88.5, "correct": 90.0, "solved": 12, "total": 14, "time_s": 500.0, "judge": 85.0,
                   "cost_usd": 3.2, "cost_basis": "price", "cost_lower_bound": True},
        "environment": {"os": "Linux 6", "cpu": "x86_64", "ram_gb": 32.0, "gpu": None},
        "bench_commit": {"sha": "abc", "dirty": False},
        "started_at": "2026-10-19T10:00:00Z", "finished_at": "2026-10-19T10:30:00Z",
    }
    result.update(overrides)
    return result


def _bundle(root: Path, result: dict[str, object], summary: str = "clean\n") -> Path:
    bundle = root / "results" / "2026-10-19_codex_gpt-x_low_ab12cd34"
    (bundle / "transcripts").mkdir(parents=True)
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    (bundle / "summary.md").write_text(summary, encoding="utf-8")
    return bundle


def test_title_and_body_come_from_result_json() -> None:
    result = _result()
    assert submit.pr_title(result) == "results: codex gpt-x low"
    body = submit.pr_body(result)
    for expected in ("| agent CLI and version | codex codex-cli 1.0 |", "| judge | pending: the maintainer runs `mengine-bench judge` on review |",
                     "| Correct % / solved | 90.0 / 12/14 |", "| Cost | >= $3.20 (price) |", "| Time | 8 min 20 s |", "| preflight / privacy check | clean"):
        assert expected in body


@pytest.mark.parametrize(("overrides", "summary", "reason"), [
    ({"bench_version": "0.0.1"}, "clean\n", "received bench 0.0.1"),
    ({"preflight": ["codex global instructions: x"]}, "clean\n", "did not start clean"),
    ({"preflight": None}, "clean\n", "did not start clean"),
    ({}, "cwd " + "C:" + "\\Users\\" + "dana" + "\\x\n", "privacy check: summary.md: home path"),
])
def test_unpublishable_bundles_are_refused(tmp_path: Path, overrides: dict[str, object], summary: str,
                                           reason: str) -> None:
    result = _result(**overrides)
    problems = submit.submission_problems(_bundle(tmp_path, result, summary), result)
    assert any(reason in problem for problem in problems), problems
    assert submit.submission_problems(_bundle(tmp_path / "ok", _result()), _result()) == []


def _git(repo: Path, *args: str) -> str:
    assert GIT is not None
    return subprocess.run([GIT, *args], cwd=repo, capture_output=True, text=True, check=True, timeout=60).stdout.strip()


@pytest.mark.skipif(GIT is None, reason="git not on PATH")
def test_commit_holds_base_plus_bundle_and_leaves_the_checkout_alone(tmp_path: Path) -> None:
    repo = tmp_path / "clone"
    repo.mkdir()
    _git(repo, "init", "--quiet", "--initial-branch=main")
    (repo / "README.md").write_text("bench\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "--quiet", "-m", "base")
    base = _git(repo, "rev-parse", "HEAD")
    bundle = _bundle(repo, _result())
    sha = submit.commit_bundle(repo, bundle, base, "results: x", ("dquill", "7+dquill@users.noreply.github.com"))
    files = _git(repo, "ls-tree", "-r", "--name-only", sha).splitlines()
    assert files == ["README.md", f"{bundle.relative_to(repo).as_posix()}/result.json",
                     f"{bundle.relative_to(repo).as_posix()}/summary.md"]
    assert _git(repo, "log", "-1", "--format=%an <%ae> %P", sha) == f"dquill <7+dquill@users.noreply.github.com> {base}"
    assert _git(repo, "rev-parse", "HEAD") == base, "the local branch must not move"
    assert _git(repo, "status", "--porcelain") == "?? results/", "the local index must not change"


@pytest.mark.skipif(GIT is None, reason="git not on PATH")
def test_own_results_do_not_make_the_next_run_dirty(tmp_path: Path) -> None:
    from mengine_bench.bundle import bench_commit
    repo = tmp_path / "clone"
    repo.mkdir()
    _git(repo, "init", "--quiet", "--initial-branch=main")
    (repo / "README.md").write_text("bench\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "--quiet", "-m", "base")
    _bundle(repo, _result())
    assert bench_commit(repo)["dirty"] is False, "a submitted bundle stays untracked in the clone"
    (repo / "extra_task.py").write_text("x = 1\n", encoding="utf-8")
    assert bench_commit(repo)["dirty"] is True


@pytest.mark.parametrize(("can_push", "push_target", "head"), [
    ("true", "https://github.com/owlmsj/mengine-bench.git", "owlmsj:"),
    ("false", "https://github.com/dquill/mengine-bench.git", "dquill:"),
])
def test_submit_pushes_upstream_with_access_else_to_the_fork(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                             can_push: str, push_target: str, head: str) -> None:
    bundle = _bundle(tmp_path, _result())
    calls: list[list[str]] = []
    replies = {("git", "rev-parse", "--show-toplevel"): str(tmp_path),
               ("gh", "api", "user"): json.dumps({"login": "dquill", "id": 7}),
               ("gh", "api", "repos/owlmsj/mengine-bench"): can_push,
               ("git", "rev-parse", "FETCH_HEAD"): "base0", ("git", "write-tree"): "tree0",
               ("git", "commit-tree", "tree0"): "commit0", ("gh", "pr", "create"): "https://github.com/pr/1"}

    def fake_call(argv: list[str], cwd: Path | None = None, env: object = None) -> str:
        calls.append(argv)
        return next((reply for key, reply in replies.items() if tuple(argv[:len(key)]) == key), "")

    monkeypatch.setattr(submit, "_call", fake_call)
    assert submit.submit(bundle) == "https://github.com/pr/1"
    [push] = [argv for argv in calls if argv[:2] == ["git", "push"]]
    assert push[-2:] == [push_target, f"commit0:refs/heads/results/{bundle.name}"]
    assert (["gh", "repo", "fork", "owlmsj/mengine-bench", "--clone=false", "--remote=false"] in calls) == (
        can_push == "false")
    [create] = [argv for argv in calls if argv[:3] == ["gh", "pr", "create"]]
    assert create[create.index("--head") + 1] == f"{head}results/{bundle.name}"


def test_run_submit_fails_before_running_without_gh(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def no_gh() -> str:
        raise SubmitError("received no 'gh' on PATH")

    monkeypatch.setattr(cli, "gh_login", no_gh)
    with pytest.raises(SystemExit, match="--submit needs gh"):
        cli.main(["run", "--agent", "cmd", "--cmd", "x {prompt_file}", "--model", "m", "--submit",
                  "--out", str(tmp_path / "results")])
    assert not (tmp_path / "results").exists()
    with pytest.raises(SystemExit, match="--allow-unclean"):
        cli.main(["run", "--agent", "cmd", "--cmd", "x {prompt_file}", "--model", "m", "--submit", "--allow-unclean"])
