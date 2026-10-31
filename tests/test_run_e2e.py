"""End-to-end `mengine-bench run` with a fake `cmd` agent, plus multi-step semantics."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import cli
from mengine_bench.core import CheckResult, EvalTask, Step, read
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.task_run import run_task

# Applies the task's own reference solution, like a perfect agent would.
REFERENCE_AGENT = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = next(t for t in catalog.all_tasks() if t.id == "ds-ab-playtest")
answers = task.reference(Path(sys.argv[1]))
sys.stdout.buffer.write(answers[-1].encode("utf-8"))
"""


def test_run_with_reference_agent_scores_full_marks(fake_agent: FakeAgent, tmp_path: Path,
                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    template = json.loads(fake_agent("reference", REFERENCE_AGENT))
    # -I would hide the installed package from the fake agent; drop it.
    template.remove("-I")
    out = tmp_path / "results"
    code = cli.main(["run", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref",
                     "--tasks", "ds-ab-playtest", "--out", str(out), "--work", str(tmp_path / "work")])
    assert code == 0
    [result_file] = out.glob("*/result.json")
    assert "_cmd_fake-ref_none_" in result_file.parent.name
    assert (result_file.parent / "summary.md").is_file()
    result = json.loads(result_file.read_text(encoding="utf-8"))
    [task] = result["tasks"]
    assert task["status"] == "ok" and task["solved"] and task["c"] == 1.0
    assert result["totals"]["correct"] == 100.0 and result["totals"]["score"] is None
    assert result["totals"]["solved"] == 1
    assert "suite" not in result
    assert result["agent"] == {"name": "cmd", "model": "fake/ref", "effort": None, "version": None}
    assert {"os", "cpu", "cpu_count", "python"} <= set(result["environment"])
    assert str(tmp_path) not in result_file.read_text(encoding="utf-8"), "results must not leak local paths"


ECHO_AGENT = """
import sys
from pathlib import Path
ws = Path(sys.argv[1])
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
(ws / "seen.txt").write_text(",".join(sorted(p.name for p in ws.iterdir())), encoding="utf-8")
print(prompt.splitlines()[0])
"""


def _two_step_task(second: Step) -> EvalTask:
    def setup(ws: Path) -> None:
        (ws / "secret.md").write_text("42", encoding="utf-8")

    def check(ws: Path, answers: list[str]) -> CheckResult:
        result = CheckResult()
        result.add("secret hidden in step 2", "secret.md" not in (read(ws, "seen.txt") or ""))
        result.add("answers per step", answers == ["first", "second"])
        return result

    return EvalTask(id="two-step", category="test", provenance="t", summary="t",
                    setup=setup, steps=(Step("first\nread {WS}/secret.md"), second), check=check,
                    reference=lambda ws: [])


def test_fresh_session_hides_files_and_collects_answers(fake_agent: FakeAgent, tmp_path: Path) -> None:
    task = _two_step_task(Step("second", fresh_session=True, hide=("secret.md",)))
    agent = CmdAgent(template=fake_agent("echo", ECHO_AGENT), model="m", effort=None)
    record = run_task(task, agent, tmp_path / "run")
    assert record.status == "ok", record.error
    assert record.answers == ["first", "second"]
    assert record.check is not None and record.check.passed
    assert [step.index for step in record.steps] == [0, 1]
    assert record.agent_s == pytest.approx(sum(step.wall_s for step in record.steps))
    assert (tmp_path / "run" / "transcripts" / "step-1.stdout.txt").is_file()


def test_a_later_step_must_start_a_fresh_session() -> None:
    # #23: resume support is gone; a step that would continue a session is a task definition error.
    with pytest.raises(ValueError, match="fresh_session"):
        _two_step_task(Step("second", hide=("secret.md",)))
    assert not hasattr(Step("x"), "compact_before")


def test_crashing_agent_is_reported(fake_agent: FakeAgent, tmp_path: Path) -> None:
    task = _two_step_task(Step("second", fresh_session=True))
    agent = CmdAgent(template=fake_agent("crash", "import sys; sys.exit(7)"), model="m", effort=None)
    record = run_task(task, agent, tmp_path / "run")
    assert record.status == "crash" and "7" in (record.error or "")


# R19 (release review): a fresh session must start from the declared carry-over
# files only, in a workspace whose ancestors do not hold the earlier steps.
LISTING_AGENT = """
import json, os, sys
from pathlib import Path
ws = Path(sys.argv[1]).resolve()
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
files = sorted(p.relative_to(ws).as_posix() for p in ws.rglob("*") if p.is_file())
siblings = sorted(os.listdir(ws.parent))
(ws / "notes").mkdir(exist_ok=True)
(ws / "notes" / "summary.md").write_text("kept", encoding="utf-8")
(ws / "notes" / "scratch.md").write_text("not carried", encoding="utf-8")
(ws / f"seen-{prompt.splitlines()[0]}.json").write_text(
    json.dumps({"cwd": str(ws), "files": files, "siblings": siblings}), encoding="utf-8")
print(prompt.splitlines()[0])
"""


def _carry_task() -> EvalTask:
    def setup(ws: Path) -> None:
        (ws / "source.md").write_text("original", encoding="utf-8")
        (ws / "copy-of-source.md").write_text("original", encoding="utf-8")

    def check(ws: Path, answers: list[str]) -> CheckResult:
        result = CheckResult()
        result.add("summary carried", read(ws, "notes/summary.md") == "kept")
        return result

    return EvalTask(id="carry", category="test", provenance="t", summary="t",
                    setup=setup, steps=(Step("first"), Step("second", fresh_session=True, hide=("source.md",),
                                                              carry=("notes/summary.md",))),
                    check=check, reference=lambda ws: [])


def test_fresh_session_sees_only_carried_files_in_an_isolated_root(fake_agent: FakeAgent, tmp_path: Path) -> None:
    agent = CmdAgent(template=fake_agent("listing", LISTING_AGENT), model="m", effort=None)
    root = tmp_path / "run"
    record = run_task(_carry_task(), agent, root)
    assert record.status == "ok", record.error
    assert record.workspace is not None and record.check is not None and record.check.passed
    second = json.loads(read(record.workspace, "seen-second.json") or "{}")
    assert second["files"] == ["AGENTS.md", "notes/summary.md"]
    cwd = Path(second["cwd"])
    assert not cwd.is_relative_to(root.resolve()), "fresh workspace must not live under the run root"
    assert not any(name.startswith("step-") for name in second["siblings"])
    # Graded and bundled from the run root once the task is over.
    assert record.workspace.resolve().is_relative_to(root.resolve())
    assert not cwd.exists()


def test_fresh_session_without_carry_starts_empty(fake_agent: FakeAgent, tmp_path: Path) -> None:
    task = _two_step_task(Step("second", fresh_session=True))
    agent = CmdAgent(template=fake_agent("listing", LISTING_AGENT), model="m", effort=None)
    record = run_task(task, agent, tmp_path / "run")
    assert record.workspace is not None
    assert json.loads(read(record.workspace, "seen-second.json") or "{}")["files"] == ["AGENTS.md"]


@pytest.mark.parametrize("exit_code,timed_out,status", [(0, False, "ok"), (7, False, "crash"),
                                                       (None, True, "timeout")])
def test_step_usage_only_recorded_on_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, exit_code: int | None, timed_out: bool, status: str,
) -> None:
    from mengine_bench.runner import process
    from mengine_bench.runner.agents import ClaudeAgent, Usage

    stdout = json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "first",
                         "total_cost_usd": 0.1, "usage": {"input_tokens": 2, "cache_creation_input_tokens": 3,
                         "cache_read_input_tokens": 4, "output_tokens": 5,
                         "output_tokens_details": {"thinking_tokens": 1}}})
    result = process.ProcessResult(stdout, "", exit_code, timed_out, 0.5)
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: result)
    task = _two_step_task(Step("second", fresh_session=True))
    record = run_task(task, ClaudeAgent("m", None), tmp_path / "run", fresh_root=tmp_path)
    assert record.status == status
    expected = Usage(9, 4, 5, 1, 0.1, "harness") if status == "ok" else None
    assert record.steps[0].usage == expected
    assert record.usage == (Usage(18, 8, 10, 2, 0.2, "harness") if status == "ok" else None)


def test_run_price_is_validated_before_the_run_and_recorded(fake_agent: FakeAgent, tmp_path: Path) -> None:
    template = json.loads(fake_agent("reference", REFERENCE_AGENT))
    template.remove("-I")
    argv = ["run", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref", "--tasks",
            "ds-ab-playtest", "--out", str(tmp_path / "results")]
    with pytest.raises(SystemExit, match="input=X,cached=Y,output=Z"):
        cli.main([*argv, "--price", "input=1"])
    assert not (tmp_path / "results").exists()
    assert cli.main([*argv, "--price", "input=3,cached=0.3,output=15"]) == 0
    [result_file] = (tmp_path / "results").glob("*/result.json")
    result = json.loads(result_file.read_text(encoding="utf-8"))
    assert result["price_per_mtok"] == {"input": 3.0, "cached": 0.3, "output": 15.0}
    # The cmd adapter reports no tokens: the cost stays unknown, never 0.
    assert (result["totals"]["cost_usd"], result["totals"]["cost_basis"]) == (None, "n/a")


def test_judge_evidence_lists_the_shell_commands_of_every_harness() -> None:
    # The judge grades self-verification; a raw 4k stream tail rarely shows it (#23 review).
    from mengine_bench.run_command import agent_commands
    stream = "\n".join(json.dumps(event) for event in [
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash",
                                                       "input": {"command": "python -m unittest"}}]}},
        {"type": "item.started", "item": {"type": "command_execution", "command": "pytest -q"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "pytest -q"}},
        {"type": "tool_use", "part": {"tool": "bash", "state": {"input": {"command": "ls"}}}},
        {"type": "text", "part": {"text": "no command here"}},
    ])
    assert agent_commands("banner\n" + stream) == ["python -m unittest", "pytest -q", "ls"]


def test_a_step_stopped_at_its_limit_still_grades_and_measures(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """#39: the deliverable counts as the limit found it, and the partial stream still gives statistics."""
    from mengine_bench.runner import process
    from mengine_bench.runner.agents import OpencodeAgent
    from mengine_bench.run_command import _outcome
    from mengine_bench.scoring import score_run

    def setup(ws: Path) -> None:
        (ws / "page.html").write_text("delivered", encoding="utf-8")

    def check(ws: Path, answers: list[str]) -> CheckResult:
        result = CheckResult()
        result.add("page delivered", read(ws, "page.html") == "delivered")
        return result

    task = EvalTask(id="limit", category="test", provenance="test", summary="test", setup=setup, check=check,
                    reference=lambda ws: [""], steps=(Step("go"),))
    stream = "\n".join(json.dumps(event) for event in (
        {"type": "step_start", "timestamp": 1000},
        {"type": "tool_use", "timestamp": 2000, "part": {"tool": "write", "state": {"status": "completed",
                                                                                     "input": {"path": "page.html"}}}},
        {"type": "step_finish", "timestamp": 3000, "part": {"tokens": {"input": 5, "output": 7, "reasoning": 3}}},
    ))
    result = process.ProcessResult(stream, "", None, True, 900.0)
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: result)
    record = run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    assert record.status == "timeout" and record.usage is None
    assert (record.stats.tool_calls, record.stats.file_writes, record.stats.generated_tokens) == (1, 1, 10)
    assert record.stats.first_write_s == 1.0
    run = score_run([_outcome(task, record)])
    assert (run.correct, run.solved, run.time_s) == (100.0, 0, 900.0)


def test_a_thin_page_at_the_limit_gets_partial_credit(tmp_path: Path) -> None:
    """#41: a timeout never zeroes what was delivered; with nothing delivered there is nothing to credit."""
    from mengine_bench import catalog
    from mengine_bench.core import write
    from mengine_bench.run_command import _outcome
    from mengine_bench.runner.task_run import TaskRunRecord
    from mengine_bench.tasks import visual

    empty = visual._scene_check(tmp_path, [""])
    assert empty.partial_score == 0.0
    write(tmp_path, visual.SCENE, '<script src="https://cdn.jsdelivr.net/npm/three@0.170.0/x.js"></script>WebGLRenderer')
    thin = visual._scene_check(tmp_path, [""])
    # This stub passes 2 of 5 checks and the live one passed 4; either way it earns at most half.
    assert thin.score == 0.0 and 0.0 < thin.partial_score <= 0.5
    stub = CheckResult(mandatory=[("page", False)], checks=[("a", True), ("b", True), ("c", True), ("d", False)],
                       waived_at_limit=("page",))
    assert stub.partial_score == 0.5
    whole = CheckResult(mandatory=[("page", True)], checks=[("a", True), ("b", True), ("c", True), ("d", False)])
    assert whole.partial_score == 0.75
    task = next(item for item in catalog.all_tasks() if item.id == "3d-voxel-landscape")
    stopped = TaskRunRecord(task_id=task.id, status="timeout", check=thin)
    finished = TaskRunRecord(task_id=task.id, status="ok", check=thin)
    assert _outcome(task, stopped).correctness == thin.partial_score
    assert _outcome(task, finished).correctness == 0.0


def test_a_timeout_never_waives_a_gate_that_guards_the_tests() -> None:
    tampered = CheckResult(mandatory=[("existing tests untouched", False)], checks=[("hidden tests", True)])
    assert tampered.partial_score == 0.0


def test_the_agent_is_told_the_limit_and_how_it_is_graded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from mengine_bench.runner import process
    from mengine_bench.runner.agents import OpencodeAgent

    task = EvalTask(id="limit", category="test", provenance="test", summary="test", setup=lambda ws: None,
                    check=lambda ws, answers: CheckResult(), reference=lambda ws: [""], steps=(Step("go"),), timeout_s=120)
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: process.ProcessResult("", "", None, True, 120.0))
    run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    [prompt] = (tmp_path / "run").rglob("step-0.md")
    text = prompt.read_text(encoding="utf-8")
    assert text.startswith("go") and "2 min" in text and "as it stands" in text
