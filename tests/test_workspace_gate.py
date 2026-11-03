"""#164: actual sibling writes fail every task, independently of command syntax."""

from pathlib import Path

import pytest

from mengine_bench.core import CheckResult, EvalTask, Step
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.process import ProcessResult
from mengine_bench.runner import task_run


@pytest.mark.parametrize("outside", [False, True])
def test_workspace_gate_scores_sibling_writes_zero(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, outside: bool) -> None:
    def invoke(argv, cwd, timeout_s, **kwargs):
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

