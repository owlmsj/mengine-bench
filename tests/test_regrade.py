"""Regrade the delivered workspace without invoking an agent (#185)."""

import json
import io
import gzip
import tarfile
from dataclasses import replace
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import catalog, cli
from mengine_bench.core import CheckResult


@pytest.fixture
def fresh_bundle(fake_agent: FakeAgent, tmp_path: Path) -> Path:
    template = json.loads(fake_agent("reference", '''
import sys
from pathlib import Path
from mengine_bench import catalog
task_id = Path(sys.argv[2]).parent.parent.name
answers = catalog.task_by_id(task_id).reference(Path(sys.argv[1]))
print(answers[-1])
'''))
    template.remove("-I")
    assert cli.main(["run", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake",
                     "--tasks", "ds-ab-playtest,bo-pnl-runway", "--out", str(tmp_path / "bundles")]) == 0
    [bundle] = (tmp_path / "bundles").iterdir()
    return bundle


def read_result(bundle: Path) -> dict[str, object]:
    return json.loads((bundle / "result.json").read_text(encoding="utf-8"))


def test_regrade_reproduces_fresh_bundle(fresh_bundle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    before = read_result(fresh_bundle)
    monkeypatch.setattr(cli, "make_agent", lambda *args: pytest.fail("regrade invoked an agent"))
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    after = read_result(fresh_bundle)
    for original, updated in zip(before["tasks"], after["tasks"]):
        assert original["c"] == updated["c"] == 1
        assert original["checks"] == updated["checks"]
    assert before["totals"] == after["totals"]
    assert after["totals"]["score"] is None


@pytest.mark.parametrize("status", ["timeout", "infra"])
def test_regrade_preserves_timeout_partial_credit_and_runtime(
        fresh_bundle: Path, monkeypatch: pytest.MonkeyPatch, status: str) -> None:
    from mengine_bench.regrade import _regrade_task
    from mengine_bench.run_command import _detail
    from mengine_bench.runner.task_run import TaskRunRecord, _grade
    result = read_result(fresh_bundle)
    row = result["tasks"][0]
    row.update(status=status, c=0.5, solved=False,
               steps=[{"index": 0, "wall_s": 12.5, "exit_code": None, "status": "timeout"}])
    lookup = catalog.task_by_id
    monkeypatch.setattr(catalog, "task_by_id", lambda task_id: replace(
        lookup(task_id), check=lambda ws, answers: CheckResult(checks=[("first", True)],
            mandatory=[("finished", False)], waived_at_limit=("finished",))))
    task = catalog.task_by_id(row["id"])
    baseline = TaskRunRecord(task_id=task.id, status=status, workspace=fresh_bundle)
    _grade(task, baseline)
    row["checks"] = _detail(task, baseline)["checks"]
    original = json.dumps(row, sort_keys=True).encode()
    _regrade_task(fresh_bundle, row, result["bench_version"])
    assert row["c"] == 0.5
    row.pop("graded_with")
    row.pop("grading_version")
    assert json.dumps(row, sort_keys=True).encode() == original


def test_regrade_uses_current_check_and_records_history(fresh_bundle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    before = read_result(fresh_bundle)
    original_lookup = catalog.task_by_id
    monkeypatch.setattr(catalog, "task_by_id", lambda task_id: replace(
        original_lookup(task_id), check=lambda ws, answers: CheckResult(checks=[("changed", False)])))
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    after = read_result(fresh_bundle)
    for original, updated in zip(before["tasks"], after["tasks"]):
        assert updated["c"] == 0
        assert updated["graded_with"] == [{"bench_version": before["bench_version"],
                                           "correct": original["c"], "checks": original["checks"]}]
    assert after["totals"]["correct"] == 0
    assert after["totals"]["score"] is None


def test_missing_workspace_keeps_grade(fresh_bundle: Path) -> None:
    before = read_result(fresh_bundle)
    row = before["tasks"][0]
    archive = fresh_bundle / "workspace" / f"{row['id']}.tar.gz"
    archive.rename(archive.with_suffix(".missing"))
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    updated = read_result(fresh_bundle)["tasks"][0]
    assert updated["c"] == row["c"] and updated["checks"] == row["checks"]
    assert "graded_with" not in updated
    assert "regrade skipped: workspace not kept" in updated["flags"]


def test_two_step_bundle_regrades_last_workspace(fake_agent: FakeAgent, tmp_path: Path,
                                               monkeypatch: pytest.MonkeyPatch) -> None:
    from test_run_e2e import ECHO_AGENT, _two_step_task
    from mengine_bench.core import Step
    task = _two_step_task(Step("second", fresh_session=True, hide=("secret.md",)))
    monkeypatch.setattr(catalog, "all_tasks", lambda: [task])
    monkeypatch.setattr(catalog, "task_by_id", lambda task_id: task)
    assert cli.main(["run", "--agent", "cmd", "--cmd", fake_agent("two", ECHO_AGENT),
                     "--model", "fake", "--tasks", task.id, "--out", str(tmp_path / "bundles")]) == 0
    [bundle] = (tmp_path / "bundles").iterdir()
    before = read_result(bundle)
    assert cli.main(["regrade", str(bundle)]) == 0
    after = read_result(bundle)
    assert after["tasks"][0]["c"] == before["tasks"][0]["c"] == 1
    assert after["tasks"][0]["checks"] == before["tasks"][0]["checks"]


def test_trace_and_runtime_gate_observations_are_replayed(fresh_bundle: Path,
                                                       monkeypatch: pytest.MonkeyPatch) -> None:
    from mengine_bench.core import TraceCheck
    from mengine_bench.runner.workspace_gate import WORKSPACE_WRITE_GATE
    result = read_result(fresh_bundle)
    row = result["tasks"][0]
    row["outside_writes"] = ["../scratch/file"]
    event = {"type": "item.completed", "item": {"type": "command_execution", "command": "echo replay"}}
    with gzip.open(fresh_bundle / row["transcript"], "wt", encoding="utf-8") as stream:
        stream.write(json.dumps({"step": "0", "stream": "stdout", "text": json.dumps(event)}) + "\n")
    (fresh_bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    original_lookup = catalog.task_by_id
    task_id = row["id"]
    def evaluate(ws, answers, trace):
        return CheckResult(checks=[("trace replayed", len(trace) == 1 and trace[0].name == "shell")])
    monkeypatch.setattr(catalog, "task_by_id", lambda received: replace(
        original_lookup(received), check=TraceCheck(evaluate)) if received == task_id else original_lookup(received))
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    updated = read_result(fresh_bundle)["tasks"][0]
    assert updated["c"] == 0
    assert next(check for check in updated["checks"] if check["name"] == "trace replayed")["ok"]
    assert not next(check for check in updated["checks"] if check["name"] == WORKSPACE_WRITE_GATE)["ok"]


def test_judged_score_changes_and_history_appends(fresh_bundle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    result = read_result(fresh_bundle)
    result["judge"] = {"model": "fake"}
    for row in result["tasks"]:
        row["judge"] = 80
    result["totals"].update(judge=80, score=95)
    (fresh_bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    original_lookup = catalog.task_by_id
    monkeypatch.setattr(catalog, "task_by_id", lambda task_id: replace(
        original_lookup(task_id), check=lambda ws, answers: CheckResult(checks=[("changed", False)])))
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    after = read_result(fresh_bundle)
    assert after["totals"]["score"] == 20
    assert after["totals"]["judge"] == 80
    assert all(len(row["graded_with"]) == 2 for row in after["tasks"])


@pytest.mark.parametrize("name,kind", [("../escape", tarfile.REGTYPE), ("link", tarfile.SYMTYPE)])
def test_unsafe_archive_is_rejected_without_rewriting(tmp_path: Path, name: str, kind: bytes) -> None:
    from mengine_bench.regrade import _extract
    archive_path = tmp_path / "unsafe.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        member = tarfile.TarInfo(name)
        member.type = kind
        member.linkname = "../outside"
        archive.addfile(member, io.BytesIO())
    with pytest.raises(ValueError, match="expected a regular file inside workspace"):
        _extract(archive_path, tmp_path / "workspace")
    assert not (tmp_path / "escape").exists()

def test_regrade_refreshes_judge_packet_and_preserves_original(
        fresh_bundle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from mengine_bench import bundle_judge
    result = read_result(fresh_bundle)
    row = result["tasks"][0]
    packet_path = fresh_bundle / "judge" / f"{row['id']}.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    packet.update(checks=[["false failure", False]], status="crash")
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    assert cli.main(["regrade", str(fresh_bundle)]) == 0
    updated = read_result(fresh_bundle)["tasks"][0]
    refreshed = json.loads(packet_path.read_text(encoding="utf-8"))
    expected = [(check["name"], check["ok"]) for check in updated["checks"]]
    context = bundle_judge.read_packet(fresh_bundle, row["id"]).context
    assert list(context.checks) == expected
    assert context.status == row["status"]
    assert refreshed["checks_graded_with"] == [{"checks": packet["checks"], "status": "crash"}]
    for key in packet.keys() - {"checks", "status"}:
        assert refreshed[key] == packet[key]

