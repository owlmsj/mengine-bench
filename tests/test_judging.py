"""What the advisors' review changed in how a run is graded (#70)."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from mengine_bench import catalog, leaderboard
from mengine_bench.bundle_judge import _agent_diff, read_packet
from mengine_bench.judge import (
    JUDGE_SYSTEM_PROMPT,
    REPLY_ONLY_TASKS,
    JudgeContext,
    build_judge_prompt,
    parse_judge_reply,
    third_criterion,
)
from mengine_bench.judge_view import tool_log, transcript_streams
from mengine_bench.run_command import _correctness, _crash_packet
from mengine_bench.runner.agents import ClaudeAgent, CodexAgent, partial_answer
from mengine_bench.runner.task_run import TaskRunRecord
from mengine_bench.core import CheckResult
from mengine_bench.scoring import TaskOutcome, combined_score, score_run, speed_points


def _jsonl(events: list[dict[str, object]]) -> str:
    return "\n".join(json.dumps(event) for event in events)


OPENCODE = _jsonl([
    {"type": "step_start", "sessionID": "ses_x"},
    {"type": "tool_use", "part": {"tool": "shell", "state": {"status": "completed", "input": {"command": "python x.py"},
                                                             "output": "ok\n", "metadata": {"metadata": {"exit": 0}}}}},
    {"type": "tool_use", "part": {"tool": "shell", "state": {"status": "completed", "input": {"command": "pytest"},
                                                             "output": "1 failed", "metadata": {"metadata": {"exit": 1}}}}},
    {"type": "tool_use", "part": {"tool": "read", "state": {"status": "completed", "input": {"path": "a.txt"}, "output": "body"}}},
])
CODEX = _jsonl([
    {"type": "thread.started", "thread_id": "t"},
    {"type": "turn.started"},
    {"type": "item.completed", "item": {"type": "command_execution", "command": "python x.py", "aggregated_output": "ok\n",
                                        "exit_code": 0, "status": "completed"}},
    {"type": "item.completed", "item": {"type": "command_execution", "command": "pytest", "aggregated_output": "1 failed",
                                        "exit_code": 1, "status": "failed"}},
    {"type": "turn.completed", "usage": {"input_tokens": 1}},
])
CLAUDE = _jsonl([
    {"type": "system", "subtype": "init", "model": "claude-opus-5-5"},
    {"type": "assistant", "message": {"model": "claude-opus-5-5", "content": [
        {"type": "tool_use", "id": "a", "name": "Bash", "input": {"command": "python x.py"}}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "a", "content": "ok\n"}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "b", "name": "Bash", "input": {"command": "pytest"}}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "b", "is_error": True,
                                              "content": [{"type": "text", "text": "1 failed"}]}]}},
])
SHELL_LINES = ('[step 1] shell "python x.py" ok -> "ok"\n[step 1] shell "pytest" failed -> "1 failed"')


def test_the_tool_log_is_the_same_for_every_harness() -> None:
    assert tool_log([CODEX]) == SHELL_LINES
    assert tool_log([CLAUDE]) == SHELL_LINES
    assert tool_log([OPENCODE]) == SHELL_LINES + '\n[step 1] read "a.txt" ok -> "body"'
    for text in (tool_log([CODEX]), tool_log([CLAUDE]), tool_log([OPENCODE])):
        for leak in ("claude-opus", "sessionID", "item.completed", "thread"):
            assert leak not in text


def test_a_tool_result_does_not_name_the_harness() -> None:
    # The Astra 3D run: an MCP result's `_meta` said codex/nodeReplExecutionDurationMs.
    call = {"type": "item.completed", "item": {"type": "mcp_tool_call", "server": "node_repl", "tool": "js", "status": "completed",
                                                "arguments": {"code": "1 + 1"},
                                                "result": {"content": [{"type": "text", "text": "2"}],
                                                           "_meta": {"codex/nodeReplExecutionDurationMs": 2}}}}
    log = tool_log([_jsonl([{"type": "turn.started"}, call])])
    assert "codex" not in log and log.endswith('ok -> "2"')


def test_a_script_run_inline_is_shown_like_a_file_written_first() -> None:
    # The Astra run wrote its scripts inside shell commands: 19 inputs cut at 300 chars, against 6 and 4.
    script = "x = 1; " * 150
    assert script in tool_log([_jsonl([
        {"type": "turn.started"},
        {"type": "item.completed", "item": {"type": "command_execution", "command": script, "exit_code": 0}},
    ])])


def test_a_crash_packet_tells_the_judge_it_crashed() -> None:
    task = next(item for item in catalog.all_tasks() if item.id == "lc-changelog")
    packet = _crash_packet(task, TaskRunRecord(task_id=task.id, status="crash", error="boom"))
    assert packet["status"] == "crash"


def test_a_long_log_keeps_both_ends_and_says_what_it_cut() -> None:
    calls = [{"type": "tool_use", "part": {"tool": "shell", "state": {"input": {"command": f"c{i}"}}}} for i in range(100)]
    log = tool_log([_jsonl(calls)])
    assert '"c0"' in log and '"c99"' in log and "[... 40 calls cut by the benchmark]" in log and '"c50"' not in log


def test_a_stream_from_no_known_harness_has_no_log() -> None:
    assert tool_log(["plain output\n"]) == ""
    assert tool_log([_jsonl([{"type": "step_start"}])]) == "(no tool calls)"


def test_every_step_is_read_from_a_bundle_transcript(tmp_path: Path) -> None:
    path = tmp_path / "t.jsonl.gz"
    lines = [{"step": "0", "stream": "stdout", "text": "first"}, {"step": "0", "stream": "stderr", "text": "noise"},
             {"step": "1", "stream": "stdout", "text": "second"}]
    path.write_bytes(gzip.compress("\n".join(json.dumps(line) for line in lines).encode("utf-8")))
    assert transcript_streams(path) == ["first", "second"]


def test_the_judge_reads_a_whole_page_and_no_raw_stream() -> None:
    page = "x" * 12_000
    context = JudgeContext(task_id="web-mondrian-landing", prompts=("p",), answers=("a",), diff="A landing/index.html\n",
                           transcript_tail='{"model":"claude-opus-5-5"}', checks=(), tool_log="[step 1] write",
                           deliverables=(("landing/index.html", page),))
    prompt = build_judge_prompt(context, screenshot=True)
    assert page in prompt and "cut by the benchmark" not in prompt
    assert "claude-opus" not in prompt and "[step 1] write" in prompt


def test_files_the_bench_moved_and_shown_deliverables_leave_the_diff() -> None:
    by_id = {task.id: task for task in catalog.all_tasks()}
    assert _agent_diff("D _inline/changelog.md\nA notes.txt\n\n--- notes.txt ---\nhi", by_id["lc-changelog"]) == \
        "A notes.txt\n\n--- notes.txt ---\nhi"
    diff = "A landing/index.html\nA a.py\n\n--- landing/index.html ---\n<html>\n\n--- a.py ---\nx = 1"
    assert _agent_diff(diff, by_id["web-mondrian-landing"]) == "A landing/index.html\nA a.py\n\n--- a.py ---\nx = 1"


def test_the_judge_sees_tool_counts_but_not_tokens_or_turns() -> None:
    stats = {"model_turns": 15, "generated_tokens": 3400, "reasoning_tokens": 17, "largest_turn_tokens": 9,
             "tool_calls": 5, "shell_failures": 1}
    context = JudgeContext(task_id="t", prompts=("p",), answers=("a",), diff="", transcript_tail="", checks=(), stats=stats)
    prompt = build_judge_prompt(context, screenshot=False)
    assert "tool_calls: 5" in prompt and "shell_failures: 1" in prompt
    for hidden in ("model_turns", "generated_tokens", "reasoning_tokens", "largest_turn_tokens"):
        assert hidden not in prompt


@pytest.mark.parametrize("task_id,screenshot,third", [
    ("lc-changelog", False, "answer_discipline"), ("vis-chart", False, "answer_discipline"),
    ("ds-ab-playtest", False, "verification"), ("web-mondrian-landing", True, "rendered"),
    ("web-mondrian-landing", False, "verification"),
])
def test_the_third_criterion_follows_the_task(task_id: str, screenshot: bool, third: str) -> None:
    assert third_criterion(task_id, screenshot) == third
    context = JudgeContext(task_id=task_id, prompts=("p",), answers=("a",), diff="", transcript_tail="", checks=())
    assert f"Third criterion: {third}" in build_judge_prompt(context, screenshot=screenshot)


def test_the_reply_only_tasks_are_catalog_tasks_that_deliver_no_file() -> None:
    by_id = {task.id: task for task in catalog.all_tasks()}
    for task_id in REPLY_ONLY_TASKS:
        assert not by_id[task_id].deliverables and not by_id[task_id].render_target


def test_the_reply_needs_subscores_that_sum() -> None:
    reply = {"approach": 30, "deliverable": 25, "verification": 20, "score": 75, "rationale": "fine"}
    verdict = parse_judge_reply(json.dumps(reply), "verification")
    assert verdict.score == 75 and verdict.parts == {"approach": 30, "deliverable": 25, "verification": 20}
    for broken in ({**reply, "score": 76}, {**reply, "approach": 41, "score": 86}, {**reply, "approach": True},
                   {key: value for key, value in reply.items() if key != "verification"}):
        with pytest.raises(ValueError, match="expected"):
            parse_judge_reply(json.dumps(broken), "verification")
    with pytest.raises(ValueError, match="expected"):
        parse_judge_reply(json.dumps(reply), "rendered")


def test_the_system_prompt_travels_apart_from_the_evidence(tmp_path: Path) -> None:
    call = ClaudeAgent("m", "xhigh").judge_invocation("the message", tmp_path, (), system_prompt="the rules")
    assert call.argv[call.argv.index("--system-prompt") + 1] == "the rules"
    assert call.stdin_text == "the message"
    # A judge without that flag gets the rules in the message.
    other = CodexAgent("m", None).judge_invocation("the message", tmp_path, (), system_prompt="the rules")
    assert other.stdin_text == "the rules\n\nthe message"


def test_the_system_prompt_fits_a_command_line_and_names_the_rubric() -> None:
    assert len(JUDGE_SYSTEM_PROMPT) < 8000 and "rubric 2.4" in JUDGE_SYSTEM_PROMPT
    for rule in ("answer_discipline", "do not infer the harness", "cut by the benchmark", "exact sum"):
        assert rule in JUDGE_SYSTEM_PROMPT, rule


def test_speed_only_pays_for_work_that_is_right() -> None:
    # An empty run that ends at once earned 15 points from Speed alone.
    assert combined_score(0.0, 0.0, speed_points(1.0)) == 0.0
    # With every check passing the formula is the same as before, so ranked runs at Correct 100 keep their Score.
    assert combined_score(100.0, 84.2, speed_points(337.0)) == 95.7
    assert combined_score(50.0, 80.0, 100.0) == 57.5


def test_a_crash_is_graded_like_a_timeout_but_is_never_solved() -> None:
    run = score_run([TaskOutcome("a", "crash", 0.8, True, 900.0, (None,))])
    assert (run.correct, run.solved) == (80.0, 0)
    cut = CheckResult(mandatory=[("page", False)], checks=[("a", True), ("b", False)], waived_at_limit=("page",))
    assert _correctness(TaskRunRecord(task_id="t", status="crash", check=cut)) == 0.5
    assert _correctness(TaskRunRecord(task_id="t", status="crash", check=None)) == 0.0


def test_a_reply_before_a_crash_is_kept(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from mengine_bench.runner import process
    from mengine_bench.runner.agents import OpencodeAgent
    from mengine_bench.runner.task_run import run_task

    task = next(item for item in catalog.all_tasks() if item.id == "lc-changelog")
    from mengine_bench.tasks import context
    answer = context._changelog_reference(tmp_path)[0]
    stream = json.dumps({"type": "text", "part": {"text": answer}})
    assert partial_answer(stream) == answer
    monkeypatch.setattr(process, "run_process", lambda *args, **kwargs: process.ProcessResult(stream, "", 1, False, 5.0))
    record = run_task(task, OpencodeAgent("m", None), tmp_path / "run")
    assert record.status == "crash" and record.answers == [answer] and _correctness(record) == 1.0


def _ranked(results: Path, name: str, score: float) -> None:
    from test_bundle_leaderboard import _write_result
    _write_result(results, name, score)


def test_the_board_says_when_the_top_is_too_close_to_call(tmp_path: Path) -> None:
    results = tmp_path / "results"
    _ranked(results, "a", 95.7)
    _ranked(results, "b", 95.1)
    _ranked(results, "c", 85.2)
    board = leaderboard.build_leaderboard(results, tmp_path).markdown
    assert "The top 2 runs are within 1 point: read them as a tie." in board and "repeat" not in board
    far = tmp_path / "far"
    _ranked(far, "a", 95.7)
    _ranked(far, "c", 85.2)
    assert "within 1 point" not in leaderboard.build_leaderboard(far, tmp_path).markdown


def test_a_bundle_without_a_log_for_its_calls_is_refused(tmp_path: Path) -> None:
    task = next(item for item in catalog.all_tasks() if item.id == "ds-ab-playtest")
    judge_dir = tmp_path / "judge"
    judge_dir.mkdir()
    record = JudgeContext(task_id=task.id, prompts=("p",), answers=("a",), diff="", transcript_tail="", checks=(),
                          stats={"tool_calls": 3}).record()
    (judge_dir / f"{task.id}.json").write_text(json.dumps(record), encoding="utf-8")
    transcripts = tmp_path / "transcripts"
    transcripts.mkdir()
    line = json.dumps({"step": "0", "stream": "stdout", "text": _jsonl([{"type": "step_start"}])})
    (transcripts / f"{task.id}.jsonl.gz").write_bytes(gzip.compress(line.encode("utf-8")))
    with pytest.raises(ValueError, match="tool_calls"):
        read_packet(tmp_path, task.id)
