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
from mengine_bench.runner.agents import CodexAgent, OpencodeAgent, partial_answer
from mengine_bench.runner.task_run import _step_env, run_task, snapshot
from mengine_bench.tasks import business, compaction, context, ir, longrepo, visual


def _by_id(task_id: str) -> EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == task_id)


def _stopped(stdout: str = "") -> process.ProcessResult:
    return process.ProcessResult(stdout, "", None, True, 120.0)


def _edit_result(ws: Path, **fields: object) -> None:
    path = ws / "result.json"
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


def test_a_result_written_before_the_limit_is_graded_and_the_reply_is_kept(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # An answer-only task lost everything at the limit. #98: the facts live in result.json, so that file is what counts.
    task = _by_id("lc-changelog")
    stream = json.dumps({"type": "text", "part": {"text": "almost there"}})

    def fake_run(argv: object, cwd: Path, *args: object, **kwargs: object) -> process.ProcessResult:
        context._changelog_reference(Path(cwd))
        return _stopped(stream)

    monkeypatch.setattr(process, "run_process", fake_run)
    record = run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    assert record.status == "timeout" and record.answers == ["almost there"]
    assert _outcome(task, record).correctness == 1.0


def test_the_right_facts_in_a_reply_alone_earn_nothing_at_the_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    task = _by_id("lc-changelog")
    answer = json.dumps(context._changelog()[1])
    stream = json.dumps({"type": "text", "part": {"text": answer}})
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: _stopped(stream))
    record = run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    assert record.status == "timeout" and record.answers == [answer]
    assert _outcome(task, record).correctness == 0.0


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


def test_the_format_of_a_reply_is_never_marked_down() -> None:
    # #70: the rule moved to the system prompt; the message names the criterion that applies it.
    # #98, rubric 2.5: no prompt fixes a format any more, so the exception is gone with it.
    context_ = JudgeContext(task_id="lc-changelog", prompts=("do it",), answers=("{}",), diff="", transcript_tail="", checks=())
    assert "code fences, bullet shapes and brevity conventions in a reply are never defects" in JUDGE_SYSTEM_PROMPT
    assert "unless the prompt fixed a format" not in JUDGE_SYSTEM_PROMPT
    assert "Third criterion: answer_discipline" in build_judge_prompt(context_, screenshot=False)


@pytest.mark.parametrize("task_id", ["lc-changelog", "vis-chart", "cmp-handoff"])
@pytest.mark.parametrize("reply", ["", "not json at all", '{"top_gpu": "wrong", "build_change": "wrong"}'])
def test_a_right_result_file_passes_whatever_the_reply_says(tmp_path: Path, task_id: str, reply: str) -> None:
    # #98, #92: the tasks that used to be graded on their reply now deliver the same facts in result.json.
    task = _by_id(task_id)
    task.setup(tmp_path)
    task.reference(tmp_path)
    assert task.check(tmp_path, [reply] * len(task.steps)).passed


# ---------------------------------------------------------------- hidden tests --


@pytest.mark.parametrize("task_id", ["gd-integration-repo"])
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


def test_a_broken_suite_does_not_pass_the_integration_task(tmp_path: Path) -> None:
    # The prompt asks for a green suite, and six hidden checks passed with a module of it broken.
    longrepo._setup(tmp_path)
    longrepo._reference(tmp_path)
    assert longrepo._check(tmp_path, [""]).passed
    write(tmp_path, "arena_server/chat/registry.py", "raise RuntimeError('broken')\n")
    checks = dict(longrepo._check(tmp_path, [""]).checks)
    assert checks["existing test suite passes"] is False


# ------------------------------------------------------------------ data tasks --


@pytest.mark.parametrize("value,ok", [
    # #98: which valid test is the agent's call, so any p under the 5% in the release rule stands, rounding included.
    (0.0002, True), (0.000198, True), (0.0001, True), (0.0011, True), (0, True), ("<0.001", True),
    (0.05, False), (0.2, False), (-0.01, False), ("significant", False), (None, False),
])
def test_the_p_value_must_be_a_number_under_the_release_threshold(tmp_path: Path, value: object, ok: bool) -> None:
    business._ab_setup(tmp_path)
    answers = business._ab_reference(tmp_path)
    _edit_result(tmp_path, p_value=value)
    result = business._ab_check(tmp_path, answers)
    assert dict(result.checks)["the gain is significant"] is ok and result.passed is ok


def test_a_right_p_value_does_not_save_a_wrong_ship_decision(tmp_path: Path) -> None:
    business._ab_setup(tmp_path)
    answers = business._ab_reference(tmp_path)
    _edit_result(tmp_path, ship_b=False)
    assert business._ab_check(tmp_path, answers).failed() == ["ship decision"]


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
    _edit_result(tmp_path, **{field: value})
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


@pytest.mark.parametrize("value,ok", [
    # #98: the true value is 35.8167 and the exact window has its own checks, so a whole minute is rounding.
    (35.82, True), ("35.8", True), (36, True), (35.4, True), (35.3, False), (36.4, False), (35.0, False), ("35 or 36", False)
])
def test_minutes_down_takes_rounding_and_no_more(tmp_path: Path, value: object, ok: bool) -> None:
    ir._logs_setup(tmp_path)
    answers = ir._logs_reference(tmp_path)
    _edit_result(tmp_path, minutes_down=value)
    result = ir._logs_check(tmp_path, answers)
    assert dict(result.checks)["minutes down"] is ok and result.passed is ok


@pytest.mark.parametrize("value,ok", [
    # The true value is 99.91709 and the tolerance 0.002.
    (99.917, True), ("99.917%", True), (99.916, True), (99.91, False), (99.93, False), (99.9, False),
])
def test_availability_takes_a_small_tolerance_and_no_more(tmp_path: Path, value: object, ok: bool) -> None:
    ir._logs_setup(tmp_path)
    answers = ir._logs_reference(tmp_path)
    _edit_result(tmp_path, availability_june_pct=value)
    result = ir._logs_check(tmp_path, answers)
    assert dict(result.checks)["June availability"] is ok and result.passed is ok


def test_every_log_day_is_in_time_order(tmp_path: Path) -> None:
    ir._logs_setup(tmp_path)
    for log in (tmp_path / "logs").glob("*.log"):
        stamps = [line[:19] for line in log.read_text(encoding="utf-8").splitlines() if line[:4] == "2026"]
        assert stamps == sorted(stamps), log.name


@pytest.mark.parametrize("field,value", [
    ("build_change", {"build": "0.9.214"}), ("build_change", "build v0.9.214"), ("builds_between", "162 builds"),
])
def test_changelog_answer_forms(tmp_path: Path, field: str, value: object) -> None:
    answers = context._changelog_reference(tmp_path)
    _edit_result(tmp_path, **{field: value})
    assert context._changelog_check(tmp_path, answers).passed


def test_changelog_wants_one_build(tmp_path: Path) -> None:
    answers = context._changelog_reference(tmp_path)
    _edit_result(tmp_path, build_change="0.9.180 or 0.9.214")
    result = context._changelog_check(tmp_path, answers)
    assert result.failed() == ["build that changed recoil_multiplier (not _ads)"]


# ---------------------------------------------------------------------- vision --


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
    answers = context._chart_reference(tmp_path)
    _edit_result(tmp_path, **change)
    assert context._chart_check(tmp_path, answers).passed is ok


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
    _edit_result(tmp_path, **{field: value})
    assert compaction._handoff_check(tmp_path, answers).passed is ok


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


def test_every_step_prompt_offers_every_skill_tool_and_mcp_server(monkeypatch: pytest.MonkeyPatch,
                                                                  tmp_path: Path) -> None:
    # #85: AGENTS.md alone misses an agent that does not load it, so the prompt of each step says it too.
    prompts: list[str] = []

    def fake_run(argv: object, cwd: Path, *args: object, **kwargs: object) -> process.ProcessResult:
        prompts.append(str(kwargs.get("stdin_text") or ""))
        rules = (Path(cwd) / "AGENTS.md").read_text(encoding="utf-8")
        assert "any skill, tool or MCP server" in rules
        return process.ProcessResult(stdout="", stderr="", exit_code=0, timed_out=False, wall_s=0.1)

    monkeypatch.setattr(process, "run_process", fake_run)
    task = _by_id("cmp-handoff")
    assert len(task.steps) > 1
    run_task(task, CodexAgent("m", None), tmp_path / "run")
    assert prompts
    for prompt in prompts:
        assert "any skill, tool or MCP server available to you" in prompt
        assert "smarter, more correct or faster" in prompt


def test_step_env_drops_parent_session_and_keeps_credentials(monkeypatch, tmp_path: Path) -> None:
    session_keys = (
        "CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID", "CLAUDE_PID",
        "CLAUDE_EFFORT", "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_BRIDGE_SESSION_ID",
        "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_EXECPATH",
        "CLAUDE_CODE_MESSAGING_TOKEN",
    )
    for key in session_keys:
        monkeypatch.setenv(key, "parent-session")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-test-credential")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "test-config")
    env = _step_env(tmp_path, {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"})
    assert not set(session_keys) & env.keys()
    assert env["ANTHROPIC_API_KEY"] == "fake-test-credential"
    assert env["CLAUDE_CONFIG_DIR"] == "test-config"
    assert env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] == "1"
    assert env["PWD"] == str(tmp_path.resolve())
