"""#164: actual sibling writes fail every task, independently of command syntax."""

from collections.abc import Sequence
from pathlib import Path

import pytest

from mengine_bench.core import CheckResult, EvalTask, Step
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.process import ProcessResult
from mengine_bench.runner import task_run


@pytest.mark.parametrize("outside", [False, True])
def test_workspace_gate_scores_sibling_writes_zero(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, outside: bool) -> None:
    def invoke(argv: Sequence[str], cwd: Path, timeout_s: int, **kwargs: object) -> ProcessResult:
        (cwd / "result.json").write_text("{}")
        if outside:
            (cwd.parent / "scratch").mkdir()
            (cwd.parent / "js.js").write_text("downloaded")
        return ProcessResult("done", "", 0, False, 0.01)

    monkeypatch.setattr(task_run.process, "run_process", invoke)
    task = EvalTask("fixture", "test", "#164", "fixture", lambda ws: None, (Step("finish"),),
                    lambda ws, answers: CheckResult(checks=[("correct", True)]), lambda ws: [])
    record = task_run.run_task(task, CmdAgent('["unused", "{prompt_file}"]', "fake", None), tmp_path / "run", fresh_root=tmp_path)
    assert record.check is not None
    assert record.check.score == (0.0 if outside else 1.0)
    assert ("no writes outside the task workspace", not outside) in record.check.mandatory
    if outside:
        assert "received" in record.check.details["no writes outside the task workspace"]
        assert "outside the workspace, in the task's parent and run directories" in record.check.details["no writes outside the task workspace"]


@pytest.mark.parametrize("action", ["read", "modify", "delete", "run-write", "timeout", "crash", "first-step"])
def test_outside_evidence_survives_lifecycle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, action: str) -> None:
    invoked = 0

    def setup(ws: Path) -> None:
        (ws.parent / "existing.txt").write_text("original")

    def invoke(argv: Sequence[str], cwd: Path, timeout_s: int, **kwargs: object) -> ProcessResult:
        nonlocal invoked
        invoked += 1
        target = cwd.parent / "existing.txt"
        if action == "read":
            assert target.read_text() == "original"
        elif action == "delete":
            target.unlink()
        elif action == "run-write":
            (tmp_path / "run" / "extra.txt").write_text("outside")
        elif action == "modify":
            target.write_text("changed contents")
        elif invoked == 1:
            (cwd.parent / "scratch").mkdir()
        return ProcessResult("done", "", 7 if action == "crash" else 0, action == "timeout", 0.01)

    monkeypatch.setattr(task_run.process, "run_process", invoke)
    steps = (Step("first"), Step("second", fresh_session=True)) if action == "first-step" else (Step("finish"),)
    task = EvalTask("fixture", "test", "#164", "fixture", setup, steps,
                    lambda ws, answers: CheckResult(checks=[("correct", True)]), lambda ws: [])
    record = task_run.run_task(task, CmdAgent('["unused", "{prompt_file}"]', "fake", None), tmp_path / "run", fresh_root=tmp_path)
    assert record.check is not None
    assert record.check.score == (1.0 if action == "read" else 0.0)
    assert record.check.partial_score == record.check.score
    if action in {"timeout", "crash"}:
        assert record.status == action
    if action == "first-step":
        assert invoked == 2



@pytest.mark.parametrize("when", ["before", "after"])
def test_a_snapshot_the_runner_cannot_take_leaves_the_gate_unmeasured(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                                     when: str) -> None:
    # #164: a filesystem snapshot that fails is an infra fault; it must never score the agent's task 0.
    calls = 0
    real = task_run.outside_snapshot

    def flaky(workspace: Path, root: Path) -> dict[str, tuple[int, int, int]]:
        nonlocal calls
        calls += 1
        if (when == "before" and calls == 1) or (when == "after" and calls == 2):
            raise PermissionError(13, f"denied at {workspace}", str(workspace.parent / "blocked"))
        return real(workspace, root)

    def invoke(argv: Sequence[str], cwd: Path, timeout_s: int, **kwargs: object) -> ProcessResult:
        (cwd / "result.json").write_text("{}")
        return ProcessResult("done", "", 0, False, 0.01)

    monkeypatch.setattr(task_run, "outside_snapshot", flaky)
    monkeypatch.setattr(task_run.process, "run_process", invoke)
    task = EvalTask("fixture", "test", "#164", "fixture", lambda ws: None, (Step("finish"),),
                    lambda ws, answers: CheckResult(checks=[("correct", True)]), lambda ws: [])
    record = task_run.run_task(task, CmdAgent('["unused", "{prompt_file}"]', "fake", None), tmp_path / "run", fresh_root=tmp_path)
    assert record.check is not None and record.check.score == 1.0
    assert all(name != "no writes outside the task workspace" for name, _ in record.check.mandatory)
    assert any("not measured" in note for note in record.check.notes), record.check.notes
    assert record.outside_unmeasured == "filesystem snapshot unavailable: PermissionError at ../blocked"
    assert str(tmp_path) not in str(record.check.notes)
