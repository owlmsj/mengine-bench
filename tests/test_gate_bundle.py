"""Published mandatory gate evidence (#164)."""
from pathlib import Path
from mengine_bench.core import CheckResult, EvalTask, Step
from mengine_bench.runner import task_run


def test_written_bundle_explains_workspace_zero(tmp_path: Path) -> None:
    import json
    from mengine_bench.bundle import write_bundle
    from mengine_bench.redact import PathScope
    from mengine_bench.report import RunMeta, build_results
    from mengine_bench.run_command import _detail, _outcome
    from mengine_bench.scoring import score_run

    task = EvalTask("fixture", "test", "#164", "fixture", lambda ws: None, (Step("finish"),),
                    lambda ws, answers: CheckResult(checks=[("correct", True)]), lambda ws: [])
    record = task_run.TaskRunRecord(task.id, workspace=tmp_path, outside_writes=["parent/scratch", "run/extra.txt"])
    task_run._grade(task, record)
    assert record.check is not None
    # #164: mandatory details must take the same redaction route as scored details.
    record.check.mandatory.append(("redaction probe", False))
    record.check.details["redaction probe"] = str(tmp_path / "private.txt")
    meta = RunMeta("2026-01-01", "fake", "fake", None, None, "fixture", "start", "end")
    results = build_results(meta, score_run([_outcome(task, record)]), {task.id: _detail(task, record)}, {}, {})
    bundle = write_bundle(results, tmp_path / "bundles", {}, PathScope(workspaces=(tmp_path,)))
    text = (bundle / "result.json").read_text(encoding="utf-8")
    row = json.loads(text)["tasks"][0]
    assert row["c"] == 0
    gate = next(check for check in row["checks"] if check["name"] == "no writes outside the task workspace")
    assert gate["mandatory"] and not gate["ok"]
    assert "parent/scratch" in gate["detail"] and "run/extra.txt" in gate["detail"]
    assert str(tmp_path) not in text and "<WORKSPACE>" in text
