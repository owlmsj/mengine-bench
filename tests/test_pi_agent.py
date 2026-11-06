"""pi reads like any other harness: argv, reply, usage, statistics and the judge's tool log (#198).

The stream is pi 1.5.0's (`pi -p --mode json --no-session --model deepseek/deepseek-flash --thinking low`),
trimmed from a live run: the system message and most text deltas are cut, the home path is `<HOME>`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench.judge_view import tool_log, tool_outputs
from mengine_bench.preflight import global_instruction_files
from mengine_bench.runner.agents import AgentError, PiAgent, Usage, make_agent, partial_answer
from mengine_bench.runner.stats import stream_stats
from mengine_bench.runner.trace import shell_commands, tool_trace

STREAM = (Path(__file__).parent / "fixtures" / "pi" / "stream.jsonl").read_text(encoding="utf-8")
ANSWER = "Created `hello.txt` with the word KIWI.\n\n`cat hello.txt` printed:\n\n```\nKIWI\n```"


def _events() -> list[dict[str, object]]:
    return [json.loads(line) for line in STREAM.split("\n") if line]


def _stream(events: list[dict[str, object]]) -> str:
    return "\n".join(json.dumps(event) for event in events) + "\n"


def _with_last_stop(reason: str, error: str | None = None) -> str:
    events = _events()
    final = next(event for event in reversed(events) if event["type"] == "message_end")
    final["message"]["stopReason"] = reason
    if error:
        final["message"]["errorMessage"] = error
    return _stream(events)


def test_the_argv_is_print_json_without_a_session_and_the_prompt_goes_through_stdin(tmp_path: Path) -> None:
    agent = make_agent("pi", "home/qwen38-flash-next-exl3-605-256k", "low", None)
    call = agent.invocation("x" * 50_000, tmp_path / "p.md", tmp_path, ("ref.png",))
    assert isinstance(agent, PiAgent)
    assert call.argv[1:] == ["-p", "--mode", "json", "--no-session", "--model", "home/qwen38-flash-next-exl3-605-256k",
                             "--thinking", "low", "@ref.png"]
    assert call.stdin_text == "x" * 50_000
    assert call.final_event == '{"type":"agent_settled"'


def test_no_effort_leaves_thinking_to_pi(tmp_path: Path) -> None:
    call = PiAgent(model="deepseek/deepseek-flash", effort=None).invocation("hi", tmp_path / "p.md", tmp_path, ())
    assert "--thinking" not in call.argv
    assert call.argv[-1] == "deepseek/deepseek-flash"


def test_the_judge_runs_without_tools_or_context_and_reads_the_rules_from_stdin(tmp_path: Path) -> None:
    call = PiAgent(model="m", effort="low").judge_invocation("grade", tmp_path, ("shot.png",), system_prompt="rules")
    assert call.argv[1:] == ["-p", "--mode", "json", "--no-session", "--model", "m", "--thinking", "low",
                             "--no-tools", "--no-extensions", "--no-mcp", "--no-skills", "--no-prompt-templates",
                             "--no-context-files", "--no-approve", "@shot.png"]
    assert call.stdin_text == "rules\n\ngrade"


def test_the_reply_is_the_last_assistant_message_and_usage_adds_every_turn() -> None:
    parsed = PiAgent(model="m", effort=None).parse(STREAM, 0)
    assert parsed.answer == ANSWER
    assert parsed.session_id == "01a1b0d6-bf6f-7195-a90a-ae58abfe8a32"
    # Turns: input 1607 + 211 uncached, cacheRead 0 + 1536; output 111 + 24; cost 0.0006153 + 0.000101316.
    assert parsed.usage is not None
    assert parsed.usage.cost_usd == pytest.approx(0.0006153 + 0.000101316)
    assert parsed.usage == Usage(1607 + 211 + 1536, 1536, 135, 0, parsed.usage.cost_usd, "harness")


@pytest.mark.parametrize("reason", ["error", "aborted", "length", "toolUse"])
def test_a_last_message_that_did_not_stop_is_a_crash_with_its_text_kept(reason: str) -> None:
    stream = _with_last_stop(reason, "boom")
    with pytest.raises(AgentError, match=f"stopReason='{reason}'.*'boom'"):
        PiAgent(model="m", effort=None).parse(stream, 0)
    assert partial_answer(stream) == ANSWER


def test_a_nonzero_exit_is_a_crash() -> None:
    with pytest.raises(AgentError, match="exit=1"):
        PiAgent(model="m", effort=None).parse(STREAM, 1)


def test_a_stream_cut_before_any_assistant_message_has_no_reply() -> None:
    events = _events()
    cut = _stream(events[:events.index(next(event for event in events if event["type"] == "message_start"))])
    with pytest.raises(AgentError, match="no assistant message_end"):
        PiAgent(model="m", effort=None).parse(cut, 0)
    assert partial_answer(cut) == ""


def test_partial_answer_takes_the_last_assistant_text_of_a_stream_stopped_mid_turn() -> None:
    events = _events()
    final = max(index for index, event in enumerate(events) if event["type"] == "message_start")
    assert partial_answer(_stream(events[:final + 2])) == "I'll create the file and read it back."


def _failed_shell(command: str, exit_code: int) -> list[dict[str, object]]:
    call = {"toolCallId": "call_x", "toolName": "bash", "args": {"command": command}}
    result = {"content": [{"type": "text", "text": "1 failed"}], "structuredContent": {"exit_code": exit_code}}
    return [{"type": "tool_execution_start", **call},
            {"type": "tool_execution_end", "toolCallId": "call_x", "toolName": "bash", "result": result,
             "isError": True, "durationMs": 500}]


def test_the_statistics_count_turns_calls_tokens_and_tool_time() -> None:
    events = _events()
    stats = stream_stats(_stream([*events[:-4], *_failed_shell("pytest", 1), *events[-4:]]))
    assert stats.model_turns == 2
    assert (stats.tool_calls, stats.tool_errors, stats.shell_commands, stats.shell_failures) == (3, 1, 2, 1)
    assert (stats.file_writes, stats.repeated_tool_calls, stats.outside_path_uses) == (1, 0, 0)
    # pi's output already holds reasoning (docs/message-types.md:90): generated is output, as on Claude and Codex.
    assert (stats.input_tokens, stats.cached_input_tokens, stats.generated_tokens, stats.reasoning_tokens) == (
        1607 + 211 + 1536, 1536, 135, 0)
    assert stats.largest_turn_tokens == 111
    assert stats.tool_call_s == [0.013, 0.125, 0.5] and stats.tool_s == pytest.approx(0.638)


def test_the_judge_reads_the_same_log_as_for_any_harness() -> None:
    events = _events()
    log = tool_log([_stream([*events[:-4], *_failed_shell("pytest", 1), *events[-4:]])])
    assert log.split("\n") == ['[step 1] write "hello.txt" ok -> "Successfully wrote to hello.txt"',
                               '[step 1] shell "cat hello.txt" ok -> "KIWI"',
                               '[step 1] shell "pytest" failed -> "1 failed"']
    assert "deepseek" not in log
    assert tool_outputs([STREAM]) == ["Successfully wrote to hello.txt", "KIWI\n"]


def test_the_checks_see_each_call_once_with_its_inputs() -> None:
    trace = tool_trace([_stream([*_events(), *_failed_shell("pytest", 1)])])
    assert [(call.name, call.failed) for call in trace] == [("write", False), ("bash", False), ("bash", True)]
    assert shell_commands(trace) == ["cat hello.txt", "pytest"]


def test_its_personal_instructions_count_as_configuration(tmp_path: Path) -> None:
    home_rules = tmp_path / ".pi" / "agent" / "AGENTS.md"
    home_rules.parent.mkdir(parents=True)
    home_rules.write_text("rules", encoding="utf-8")
    assert global_instruction_files("pi", tmp_path, {}) == [home_rules]
    moved = tmp_path / "pi-home"
    moved.mkdir()
    (moved / "APPEND_SYSTEM.md").write_text("more", encoding="utf-8")
    assert global_instruction_files("pi", tmp_path, {"PI_CODING_AGENT_DIR": str(moved)}) == [moved / "APPEND_SYSTEM.md"]
