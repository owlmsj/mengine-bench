"""Run statistics from each harness's stream, outside the Score (#39)."""

from __future__ import annotations

import json

from mengine_bench.judge import JudgeContext, build_judge_prompt
from mengine_bench.report import stats_summary
from mengine_bench.runner.stats import RunStats, merge_stats, stats_record, stream_stats


def _jsonl(events: list[dict[str, object]]) -> str:
    return "\n".join(json.dumps(event) for event in events)


def _tool(stamp: int, tool: str, payload: dict[str, object], *, status: str = "completed", exit_code: int | None = None,
          spent_ms: int = 1000) -> dict[str, object]:
    metadata = {"metadata": {} if exit_code is None else {"exit": exit_code}}
    return {"type": "tool_use", "timestamp": stamp, "part": {"tool": tool, "state": {
        "status": status, "input": payload, "metadata": metadata, "time": {"start": stamp - spent_ms, "end": stamp}}}}


def _finish(stamp: int, *, output: int, reasoning: int = 0, read: int = 0, fresh: int = 10) -> dict[str, object]:
    return {"type": "step_finish", "timestamp": stamp, "part": {"tokens": {
        "input": fresh, "output": output, "reasoning": reasoning, "cache": {"read": read, "write": 0}}}}


OPENCODE_STREAM = _jsonl([
    {"type": "step_start", "timestamp": 10_000},
    _tool(12_000, "read", {"path": "a.txt"}),
    _tool(13_000, "read", {"path": "a.txt"}),
    _finish(14_000, output=100, read=90),
    {"type": "step_start", "timestamp": 19_000},
    _tool(21_000, "shell", {"command": "python x.py"}, exit_code=1, spent_ms=2000),
    _tool(25_000, "write", {"path": "../outside.json", "content": "{}"}),
    _tool(26_000, "write", {"path": "out.json"}, status="error"),
    _finish(29_000, output=600, reasoning=400, read=100),
    # The stop at the limit: this turn has no step_finish, and it still counts in the clock.
    {"type": "step_start", "timestamp": 30_000},
])


def test_opencode_stream_gives_counts_tokens_and_times() -> None:
    record = stats_record(stream_stats(OPENCODE_STREAM))
    assert record == {
        # Three starts: the turn stopped at the limit counts, and its tokens are unknown.
        "model_turns": 3, "tool_calls": 5, "tool_errors": 1, "shell_commands": 1, "shell_failures": 1,
        "file_writes": 2, "repeated_tool_calls": 1, "outside_path_uses": 1,
        "input_tokens": 210, "cached_input_tokens": 190, "generated_tokens": 1100, "reasoning_tokens": 400,
        "largest_turn_tokens": 1000, "first_tool_s": 2.0, "first_write_s": 15.0, "last_event_s": 20.0,
        "tool_s": 6.0, "wait_s": 6.0, "turn_tps_median": 100.0,
    }


def test_opencode_turn_without_step_finish_still_counts() -> None:
    # Seen on lc-changelog: one answered turn, no step_finish, so usage is unknown but the turn happened.
    stdout = _jsonl([{"type": "step_start", "timestamp": 1000},
                     {"type": "text", "timestamp": 2000, "part": {"text": "answer"}}])
    record = stats_record(stream_stats(stdout))
    assert record["model_turns"] == 1 and record["generated_tokens"] is None


def test_codex_stream_counts_tools_and_leaves_times_unmeasured() -> None:
    stdout = _jsonl([
        {"type": "turn.started"},
        {"type": "item.completed", "item": {"type": "agent_message", "text": "hi"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "pytest", "exit_code": 2,
                                            "status": "failed"}},
        {"type": "item.completed", "item": {"type": "file_change", "changes": [{"path": "a.py"}], "status": "completed"}},
        {"type": "turn.completed", "usage": {"input_tokens": 70, "cached_input_tokens": 60, "output_tokens": 50,
                                             "reasoning_output_tokens": 20}},
    ])
    record = stats_record(stream_stats(stdout))
    assert (record["model_turns"], record["tool_calls"], record["tool_errors"]) == (1, 2, 1)
    assert (record["shell_commands"], record["shell_failures"], record["file_writes"]) == (1, 1, 1)
    assert (record["input_tokens"], record["generated_tokens"], record["reasoning_tokens"]) == (70, 50, 20)
    assert record["first_write_s"] is None and record["last_event_s"] is None and record["turn_tps_median"] is None


def test_claude_stream_ties_errors_to_their_tool_call() -> None:
    usage = {"input_tokens": 5, "cache_creation_input_tokens": 3, "cache_read_input_tokens": 2, "output_tokens": 40,
             "output_tokens_details": {"thinking_tokens": 10}}
    stdout = _jsonl([
        {"type": "assistant", "message": {"usage": usage, "content": [
            {"type": "tool_use", "id": "a", "name": "Bash", "input": {"command": "false"}},
            {"type": "tool_use", "id": "b", "name": "Write", "input": {"file_path": "x"}},
        ]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "a", "is_error": True}]}},
        {"type": "result", "subtype": "success", "is_error": False, "result": "ok"},
    ])
    record = stats_record(stream_stats(stdout))
    assert (record["tool_calls"], record["tool_errors"], record["shell_failures"], record["file_writes"]) == (2, 1, 1, 1)
    assert (record["input_tokens"], record["generated_tokens"], record["reasoning_tokens"]) == (10, 40, 10)


def test_an_unknown_stream_is_unmeasured_not_zero_tokens() -> None:
    record = stats_record(stream_stats("plain text\nno events here"))
    assert record["model_turns"] == 0 and record["generated_tokens"] is None and record["turn_tps_median"] is None


def test_merge_adds_steps_and_keeps_the_earliest_first_write() -> None:
    first = RunStats(tool_calls=1, generated_tokens=10, largest_turn_tokens=10, first_write_s=None, last_event_s=5.0,
                     turn_rates=[100.0])
    second = RunStats(tool_calls=2, generated_tokens=30, largest_turn_tokens=20, first_write_s=7.0, last_event_s=9.0,
                      turn_rates=[200.0, 300.0])
    record = stats_record(merge_stats([first, second]))
    assert (record["tool_calls"], record["generated_tokens"], record["largest_turn_tokens"]) == (3, 40, 20)
    assert (record["first_write_s"], record["last_event_s"], record["turn_tps_median"]) == (7.0, 14.0, 200.0)
    assert stats_record(merge_stats([RunStats()]))["generated_tokens"] is None


def _context(**overrides: object) -> JudgeContext:
    fields: dict[str, object] = {
        "task_id": "t", "prompts": ("do it",), "answers": ("done",), "diff": "", "transcript_tail": "", "checks": (),
        "status": "timeout", "stats": {"model_turns": 12, "generated_tokens": 3400, "tool_errors": 2},
    }
    return JudgeContext(**{**fields, **overrides})  # type: ignore[arg-type]


def test_the_judge_sees_status_and_measurements_as_trusted_context() -> None:
    prompt = build_judge_prompt(_context(), screenshot=False)
    section = prompt.split("## Run measurements", 1)[1].split("## Agent final answer", 1)[0]
    assert "status: timeout" in section
    assert "model_turns: 12" in section and "generated_tokens: 3400" in section
    assert "hardware" in section


def test_the_judge_gets_no_time_or_speed_because_they_reveal_the_hardware() -> None:
    stats = stream_stats(OPENCODE_STREAM)
    packet = stats_summary(stats_record(stats))
    assert packet["generated_tokens"] == 1100 and packet["shell_failures"] == 1 and packet["outside_path_uses"] == 1
    for hidden in ("turn_tps_median", "wait_s", "tool_s", "first_write_s", "first_tool_s", "last_event_s"):
        assert hidden not in packet


def test_an_older_packet_without_measurements_still_loads() -> None:
    record = _context().record()
    del record["status"], record["stats"]
    context = JudgeContext.from_record(record)
    assert context.status == "ok" and dict(context.stats) == {}
    assert "## Run measurements" not in build_judge_prompt(context, screenshot=False)
