"""What the review of the 14 tasks found before bench 1.3 (#59): each case failed on 1.2.1."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import CheckResult, EvalTask, Step, write
from mengine_bench.judge import JUDGE_SYSTEM_PROMPT, build_judge_prompt, JudgeContext, workspace_diff
from mengine_bench.redact import PathScope, redact_paths
from mengine_bench.run_command import _outcome
from mengine_bench.runner import process
from mengine_bench.runner.agents import OpencodeAgent, partial_answer
from mengine_bench.runner.task_run import _step_env, run_task, snapshot
from mengine_bench.tasks import business, compaction, context, gamedev, ir, longrepo, visual


def _by_id(task_id: str) -> EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == task_id)


def _stopped(stdout: str = "") -> process.ProcessResult:
    return process.ProcessResult(stdout, "", None, True, 120.0)


def _edit_json(path: Path, **fields: object) -> None:
    got = json.loads(path.read_text(encoding="utf-8"))
    got.update(fields)
    path.write_text(json.dumps(got), encoding="utf-8")


# ------------------------------------------------------------------ the runner --


def test_the_workspace_has_nothing_next_to_it(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Prompts, transcripts and the hidden document sat in `..`, and a folder named step-0 under the task id
    # looked like a place to write out of: three runs delivered to `../` and lost the task.
    seen: list[Path] = []

    def fake_run(argv: object, cwd: Path, *args: object, **kwargs: object) -> process.ProcessResult:
        seen.append(Path(cwd))
        assert [item.name for item in Path(cwd).parent.iterdir()] == ["workspace"]
        return _stopped()

    monkeypatch.setattr(process, "run_process", fake_run)
    record = run_task(_by_id("lc-changelog"), OpencodeAgent("m", None), tmp_path / "run")
    assert seen and not seen[0].is_relative_to(tmp_path)
    assert record.workspace is not None and record.workspace.is_relative_to(tmp_path)
    assert not seen[0].parent.exists(), "the temp root is gone once the workspace is back in the run"


@pytest.mark.parametrize("event", [
    {"type": "text", "part": {"text": "ANSWER"}},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "ANSWER"}]}},
    {"type": "item.completed", "item": {"type": "agent_message", "text": "ANSWER"}},
])
def test_the_last_reply_is_read_from_every_stream(event: dict[str, object]) -> None:
    assert partial_answer(json.dumps(event)) == "ANSWER"


def test_a_stream_with_no_reply_gives_nothing_and_plain_output_gives_itself() -> None:
    assert partial_answer(json.dumps({"type": "step_start"})) == ""
    assert partial_answer('{"top_gpu": "H200"}') == '{"top_gpu": "H200"}'


def test_a_reply_given_before_the_limit_is_graded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # An answer-only task lost everything at the limit, even with the right reply already in the stream.
    task = _by_id("lc-changelog")
    answer = context._changelog_reference(tmp_path)[0]
    stream = json.dumps({"type": "text", "part": {"text": answer}})
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: _stopped(stream))
    record = run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    assert record.status == "timeout" and record.answers == [answer]
    assert _outcome(task, record).correctness == 1.0


def test_the_note_names_the_reply_too(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: _stopped())
    task = EvalTask(id="limit", category="test", provenance="test", summary="test", setup=lambda ws: None,
                    check=lambda ws, answers: CheckResult(), reference=lambda ws: [""], steps=(Step("go"),))
    run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    [prompt] = (tmp_path / "run").rglob("step-0.md")
    assert "your reply" in prompt.read_text(encoding="utf-8")


def test_bytecode_and_the_rules_file_stay_out_of_the_judge_diff(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # In one run __pycache__ took 16,463 of the 19,198 characters the judge saw, and the judge took points for it.
    write(tmp_path, "a.py", "x = 1\n")
    write(tmp_path, "__pycache__/a.cpython-313.pyc", "bytes")
    assert list(snapshot(tmp_path)) == ["a.py"]
    assert _step_env(tmp_path, None)["PYTHONDONTWRITEBYTECODE"] == "1"
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: _stopped())
    record = run_task(_by_id("lc-changelog"), OpencodeAgent("m", None), tmp_path / "run")
    assert record.workspace is not None
    assert "AGENTS.md" not in workspace_diff(record.initial_files, snapshot(record.workspace))


def test_the_temporary_workspace_path_is_redacted() -> None:
    line = r'{"workdir":"C:\\Users\\someone\\AppData\\Local\\Temp\\mengine-bench-fresh-abc123\\workspace\\a.py"}'
    cleaned = redact_paths(line, PathScope())
    assert "mengine-bench-fresh" not in cleaned and "someone" not in cleaned and "a.py" in cleaned


def test_a_task_that_only_wants_a_reply_is_not_marked_down_for_its_format() -> None:
    # #70: the rule moved to the system prompt; the message names the criterion that applies it.
    context_ = JudgeContext(task_id="lc-changelog", prompts=("do it",), answers=("{}",), diff="", transcript_tail="", checks=())
    assert "unless the prompt fixed a format" in JUDGE_SYSTEM_PROMPT
    assert "Third criterion: answer_discipline" in build_judge_prompt(context_, screenshot=False)


# ---------------------------------------------------------------- hidden tests --


@pytest.mark.parametrize("task_id", ["gd-astar-doors", "gd-ecs-collision-bug", "gd-integration-repo"])
def test_a_fake_unittest_module_earns_nothing(tmp_path: Path, task_id: str) -> None:
    # A workspace unittest.py replaced the standard module and exited 0, so the untouched code scored 1.0.
    task = _by_id(task_id)
    (tmp_path / "clean").mkdir()
    (tmp_path / "faked").mkdir()
    task.setup(tmp_path / "clean")
    task.setup(tmp_path / "faked")
    write(tmp_path / "faked", "unittest.py", "import sys\nsys.exit(0)\n")
    faked = task.check(tmp_path / "faked", [""]).score
    assert faked == task.check(tmp_path / "clean", [""]).score and faked < 1.0


def test_a_correct_refactor_of_the_collision_helper_passes(tmp_path: Path) -> None:
    # The hidden test imported `overlaps` by name: renaming it zeroed a correct fix with the visible suite green.
    gamedev._ecs_setup(tmp_path)
    gamedev._ecs_reference(tmp_path)
    path = tmp_path / "arena_ecs/systems/collision.py"
    path.write_text(path.read_text(encoding="utf-8").replace("overlaps", "_boxes_overlap"), encoding="utf-8")
    assert gamedev._ecs_check(tmp_path, [""]).passed


def test_collision_pairs_compare_in_any_order(tmp_path: Path) -> None:
    gamedev._ecs_setup(tmp_path)
    gamedev._ecs_reference(tmp_path)
    path = tmp_path / "arena_ecs/systems/collision.py"
    path.write_text(path.read_text(encoding="utf-8").replace("hits.append((ea, eb))", "hits.append((eb, ea))"), encoding="utf-8")
    assert gamedev._ecs_check(tmp_path, [""]).passed


def test_a_broken_suite_does_not_pass_the_integration_task(tmp_path: Path) -> None:
    # The prompt asks for a green suite, and six hidden checks passed with a module of it broken.
    longrepo._setup(tmp_path)
    longrepo._reference(tmp_path)
    assert longrepo._check(tmp_path, [""]).passed
    write(tmp_path, "arena_server/chat/registry.py", "raise RuntimeError('broken')\n")
    checks = dict(longrepo._check(tmp_path, [""]).checks)
    assert checks["existing test suite passes"] is False


# ------------------------------------------------------------------ data tasks --


@pytest.mark.parametrize("value,ok", [(0.0002, True), (0.000198, True), (0.0001, False), (0.0011, False), (0, False)])
def test_the_p_value_must_be_right_to_the_digits_asked(tmp_path: Path, value: float, ok: bool) -> None:
    business._ab_setup(tmp_path)
    answers = business._ab_reference(tmp_path)
    _edit_json(tmp_path / "ab_result.json", p_value=value)
    assert business._ab_check(tmp_path, answers).passed is ok


# ----------------------------------------------------------- retrieval and logs --


@pytest.mark.parametrize("field,value,ok", [
    ("approver", "Alice Sato, producer", True),
    ("approver", "Alice Sato, Bruno Costa", False),
    ("flag", "`matchmaking.max_ping_ms`", True),
    ("build", "Build: 0.14.3", True),
    ("build", "0.14.3-rc1", False),
    ("neoplastic_ranked_max", "10 or 12", False),
    ("restored_value", "120 or 250", False),
])
def test_wiki_answer_forms(tmp_path: Path, field: str, value: str, ok: bool) -> None:
    ir._wiki_setup(tmp_path)
    answers = ir._wiki_reference(tmp_path)
    _edit_json(tmp_path / "answers.json", **{field: value})
    assert ir._wiki_check(tmp_path, answers).passed is ok


@pytest.mark.parametrize("cause,ok", [
    ("A full /data disk prevented the server from saving.", True),
    ("A full disk on /data broke SaveGame.", True),
    ("Not enough free space on /data, so saves failed.", True),
    ("Out-of-memory kill (exit 137); disk had plenty of space.", False),
    ("Not caused by disk space: the RCON auth failure crashed the server.", False),
    ("The server was OOM-killed; the /data disk had free space left.", False),
])
def test_root_cause_names_a_full_disk(cause: str, ok: bool) -> None:
    assert ir._names_disk_full(cause) is ok


def test_minutes_down_keeps_the_digits_asked(tmp_path: Path) -> None:
    ir._logs_setup(tmp_path)
    answers = ir._logs_reference(tmp_path)
    _edit_json(tmp_path / "incident.json", minutes_down=35.77)
    assert not ir._logs_check(tmp_path, answers).passed


def test_every_log_day_is_in_time_order(tmp_path: Path) -> None:
    ir._logs_setup(tmp_path)
    for log in (tmp_path / "logs").glob("*.log"):
        stamps = [line[:19] for line in log.read_text(encoding="utf-8").splitlines() if line[:4] == "2026"]
        assert stamps == sorted(stamps), log.name


@pytest.mark.parametrize("field,value", [
    ("build_change", {"build": "0.9.214"}), ("build_change", "build v0.9.214"), ("builds_between", "162 builds"),
])
def test_changelog_answer_forms(tmp_path: Path, field: str, value: object) -> None:
    got = json.loads(context._changelog_reference(tmp_path)[0])
    got[field] = value
    assert context._changelog_check(tmp_path, [json.dumps(got)]).passed


def test_changelog_wants_one_build(tmp_path: Path) -> None:
    got = json.loads(context._changelog_reference(tmp_path)[0])
    got["build_change"] = "0.9.180 or 0.9.214"
    assert not context._changelog_check(tmp_path, [json.dumps(got)]).passed


# ---------------------------------------------------------------------- vision --


CHART_RIGHT = {"top_gpu": "H200", "top_tps": 180, "bottom_gpu": "4090", "ratio": 6.0}


@pytest.mark.parametrize("change,ok", [
    ({}, True),
    ({"top_tps": "175 TPS"}, True),
    ({"ratio": "5.8x"}, True),
    ({"top_gpu": "Nvidia Tesla H200"}, True),
    # The other series: the 8k bars.
    ({"top_gpu": "B200", "top_tps": 210}, False),
    ({"bottom_gpu": "A100", "ratio": 3.0}, False),
])
def test_chart_reads_the_asked_series(tmp_path: Path, change: dict[str, object], ok: bool) -> None:
    assert context._chart_check(tmp_path, [json.dumps({**CHART_RIGHT, **change})]).passed is ok


def test_chart_prompt_names_the_series() -> None:
    assert "256k" in _by_id("vis-chart").steps[0].prompt


# ------------------------------------------------------------------- compaction --


@pytest.mark.parametrize("field,value,ok", [
    ("final_vram_mib", "7,697 MiB", True),
    ("final_vram_mib", "Q5 at 7697 MiB", True),
    ("final_decode", "38.0t/s", True),
    ("pending", "evals README is stale", True),
    ("file_line", "scripts/start_server.ps1 (local9 block, line 165)", True),
    ("discarded_quant", "Q6K", True),
    ("measure_command", "pwsh -File scripts/measure_decode.ps1 -Ctx 1024 -NPredict 131072", False),
    ("pending", "Update the root README with benchmark results", False),
    ("final_decode", "37.8, later 38.0", False),
])
def test_handoff_answer_forms(tmp_path: Path, field: str, value: str, ok: bool) -> None:
    answers = compaction._handoff_reference(tmp_path)
    got = json.loads(answers[1])
    got[field] = value
    assert compaction._handoff_check(tmp_path, ["ok", json.dumps(got)]).passed is ok


def test_the_handoff_must_keep_the_second_flag_and_fit_a_tighter_limit(tmp_path: Path) -> None:
    answers = compaction._handoff_reference(tmp_path)
    assert compaction._handoff_check(tmp_path, answers).passed
    handoff = tmp_path / "HANDOFF.md"
    good = handoff.read_text(encoding="utf-8")
    handoff.write_text(good.replace(" + `-ub 512`", ""), encoding="utf-8")
    assert not compaction._handoff_check(tmp_path, answers).passed
    handoff.write_text(good + "x" * 1000, encoding="utf-8")
    assert not compaction._handoff_check(tmp_path, answers).passed


# ---------------------------------------------------------------------- visuals --


def test_palette_reads_functional_colors() -> None:
    page = ("<style>.a{background:rgb(212,9,32)}.b{background:rgb(19 86 162)}.c{background:hsl(50,92%,62%)}"
            ".d{color:rgba(0,0,0,1)}</style>")
    assert visual._mondrian_palette(page)


def test_palette_ignores_color_words_in_font_names() -> None:
    assert not visual._mondrian_palette('<style>body{font-family:"Red Hat","Blue Note","Yellow Tail","Black Ops"}</style>')


def test_procedural_geometry_counts_and_a_fetched_model_does_not(tmp_path: Path) -> None:
    filler = "x" * 2100
    page = (f'<script src="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"></script>WebGLRenderer '
            f"requestAnimationFrame new THREE.LatheGeometry(p) {filler}")
    write(tmp_path, visual.SCENE, page)
    assert visual._scene_check(tmp_path, [""]).passed
    write(tmp_path, visual.SCENE, page + ' fetch("https://example.com/fuji.glb")')
    assert not visual._scene_check(tmp_path, [""]).passed


def test_redacting_a_long_line_stays_linear() -> None:
    # A live 1.3 run spent about 7 min writing its bundle: the path pattern backtracked over base64 screenshots.
    import time

    path = r"C:\\Users\\someone\\AppData\\Local\\Temp\\mengine-bench-fresh-abc123\\workspace\\a.py"
    line = "A" * 100_000 + f' "{path}" ' + "B" * 100_000
    started = time.perf_counter()
    cleaned = redact_paths(line, PathScope())
    assert time.perf_counter() - started < 2.0
    assert "mengine-bench-fresh" not in cleaned and "someone" not in cleaned and "a.py" in cleaned
