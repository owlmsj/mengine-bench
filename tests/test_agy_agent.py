"""AGY reads like any other harness: reply, usage, statistics and the judge's tool log (#72).

The stream is agy 1.4.12's, trimmed from a live run of gemini-4-argon-high.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench.judge_view import tool_log
from mengine_bench.preflight import global_instruction_files
from mengine_bench.run_command import agent_commands
from mengine_bench.runner.agents import AgentError, AgyAgent, make_agent, partial_answer
from mengine_bench.runner.stats import stream_stats

CONVERSATION = "ab86ef80"


def _update(index: int, state: str, kind: str, **fields: object) -> dict[str, object]:
    step = {"conversation_id": CONVERSATION, "step_index": index, "state": state, "step_type": kind, **fields}
    return {"event": "step_update", "step_update": step}


def _tool(index: int, state: str, name: str, parameters: dict[str, str], **info: object) -> dict[str, object]:
    return _update(index, state, "tool", tool_name=name, duration_seconds=1.5,
                   tool_info={"name": name, "parameters": parameters, **info})


def _usage(generated: int, thinking: int, prompt: int, cached: int) -> dict[str, int]:
    return {"input_tokens": prompt, "output_tokens": generated, "thinking_tokens": thinking, "cache_read_tokens": cached,
            "total_tokens": prompt + generated}


def _jsonl(events: list[dict[str, object]]) -> str:
    return "\n".join(json.dumps(event) for event in events)


TOOLS = [
    _tool(2, "ACTIVE", "run_command", {"CommandLine": "python x.py"}),
    _tool(2, "DONE", "run_command", {"CommandLine": "python x.py"},
          output="Command exited with code 0.\n\nCommand output:\nok\r\n"),
    _tool(3, "ACTIVE", "run_command", {"CommandLine": "pytest"}),
    _tool(3, "DONE", "run_command", {"CommandLine": "pytest"},
          output="Command exited with code 1.\n\nCommand output:\n1 failed\r\n"),
]
BEGIN = {"event": "init", "conversation_id": CONVERSATION,
         "init": {"model": "gemini-4-argon-high", "cwd": "ws", "tools": ["run_command"], "permission_mode": "always-proceed"}}
FIRST_TURN = _update(1, "DONE", "agent_response", duration_seconds=5.0, usage=_usage(600, 160, 1000, 0))
LAST_TURN = [_update(5, "ACTIVE", "agent_response", text_delta="DO"), _update(5, "ACTIVE", "agent_response", text_delta="NE"),
             _update(5, "DONE", "agent_response", text_delta="\n", duration_seconds=2.0, usage=_usage(19, 14, 200, 800))]
RESULT = {"event": "result", "result": {"conversation_id": CONVERSATION, "status": "SUCCESS", "response": "DONE\n",
                                        "duration_seconds": 26.4, "num_turns": 1, "usage": _usage(619, 174, 1200, 800)}}
STREAM = _jsonl([BEGIN, FIRST_TURN, *TOOLS, *LAST_TURN, RESULT])


def test_the_model_and_effort_make_agys_model_id(tmp_path: Path) -> None:
    agent = make_agent("agy", "gemini-4-argon", "high", None)
    call = agent.invocation("do it", tmp_path / "p.md", tmp_path, ())
    assert call.argv[1:] == ["--model", "gemini-4-argon-high", "--output-format", "stream-json", "--input-format", "stream-json",
                             "--dangerously-skip-permissions", "--print", ""]
    assert AgyAgent("gemini-4-argon-low", None).invocation("p", tmp_path / "p.md", tmp_path, ()).argv[2] == "gemini-4-argon-low"


def test_a_long_prompt_travels_on_stdin_as_one_message(tmp_path: Path) -> None:
    # lc-changelog inlines 87,221 chars; the Windows command line stops at 32,767.
    prompt = 'line "one"\n' + "x" * 90_000
    call = AgyAgent("m", None).invocation(prompt, tmp_path / "p.md", tmp_path, ())
    assert call.stdin_text is not None and call.stdin_text.count("\n") == 1 and call.stdin_text.endswith("\n")
    assert json.loads(call.stdin_text) == {"event": "user", "message": {"role": "user", "content": prompt}}
    assert prompt not in call.argv


def test_agy_does_not_judge(tmp_path: Path) -> None:
    # It has no flag that removes its tools, and a judge reads agent-written evidence.
    with pytest.raises(ValueError, match="expected claude, codex or opencode"):
        AgyAgent("m", None).judge_invocation("p", tmp_path, ())


def test_the_reply_and_usage_come_from_the_result() -> None:
    parsed = AgyAgent("m", None).parse(STREAM, 0)
    assert parsed.answer == "DONE\n" and parsed.session_id == CONVERSATION
    usage = parsed.usage
    assert usage is not None
    # AGY's input_tokens leaves the cache reads out; the bench's includes them (agents.Usage).
    assert (usage.input_tokens, usage.cached_input_tokens, usage.output_tokens, usage.reasoning_tokens) == (2000, 800, 619, 174)
    assert usage.cost_usd is None and usage.cost_source == "none"


@pytest.mark.parametrize("stream,exit_code,reason", [
    (STREAM, 1, "exit=1"),
    (_jsonl([BEGIN, FIRST_TURN]), 0, "no result"),
    (_jsonl([{"event": "result", "result": {"status": "FAILED", "response": "x"}}]), 0, "status='FAILED'"),
    (_jsonl([{"event": "result", "result": {"status": "SUCCESS", "response": "  "}}]), 0, "no text"),
])
def test_anything_but_a_finished_reply_is_a_crash(stream: str, exit_code: int, reason: str) -> None:
    with pytest.raises(AgentError, match=reason):
        AgyAgent("m", None).parse(stream, exit_code)


def test_a_stopped_run_keeps_its_last_reply() -> None:
    assert partial_answer(_jsonl([BEGIN, *TOOLS, *LAST_TURN[:2]])) == "DONE"
    assert partial_answer(_jsonl([BEGIN, *TOOLS])) == "", "the raw stream is not a reply"
    assert partial_answer(STREAM) == "DONE\n"


def test_the_statistics_count_finished_calls_once() -> None:
    edits = [_tool(6, "DONE", "write_file", {"Path": "a.txt"}), _tool(7, "DONE", "edit_file", {"Path": "a.txt"}),
             _tool(8, "ERROR", "read_file", {"Path": "../missing"}, error={"type": "TOOL_ERROR", "message": "file does not exist"}),
             _tool(9, "DONE", "run_command", {"CommandLine": "pytest"})]
    stats = stream_stats(_jsonl([BEGIN, FIRST_TURN, *TOOLS, *edits, *LAST_TURN, RESULT]))
    assert stats.model_turns == 2
    assert (stats.tool_calls, stats.tool_errors, stats.shell_commands, stats.shell_failures) == (6, 1, 3, 1)
    assert (stats.file_writes, stats.repeated_tool_calls, stats.outside_path_uses) == (2, 1, 1)
    assert (stats.input_tokens, stats.cached_input_tokens, stats.generated_tokens, stats.reasoning_tokens) == (2000, 800, 619, 174)
    assert stats.largest_turn_tokens == 600 and stats.turn_rates == [120.0]
    assert stats.tool_s == 9.0


def test_the_judge_reads_the_same_log_as_for_any_harness() -> None:
    log = tool_log([STREAM])
    assert log == '[step 1] shell "python x.py" ok -> "ok"\n[step 1] shell "pytest" failed -> "1 failed"'
    assert "gemini" not in log and CONVERSATION not in log


def test_the_judge_sees_files_by_path_and_why_a_call_failed() -> None:
    calls = [_tool(2, "DONE", "write_file", {"Path": "a.txt"}), _tool(3, "DONE", "edit_file", {"Path": "a.txt"}),
             _tool(4, "ERROR", "read_file", {"Path": "b.txt"}, error={"type": "TOOL_ERROR", "message": "file does not exist"}),
             _tool(5, "DONE", "grep_search", {"Query": "beta"}, output="a.txt:1"),
             _tool(6, "DONE", "capture_browser_screenshot", {"PageId": "1"}, output="saved")]
    assert tool_log([_jsonl([BEGIN, *calls])]).split("\n") == [
        '[step 1] write "a.txt" ok -> ""',
        '[step 1] edit "a.txt" ok -> ""',
        '[step 1] read "b.txt" failed -> "file does not exist"',
        '[step 1] search "{\\"Query\\": \\"beta\\"}" ok -> "a.txt:1"',
        '[step 1] browser "{\\"PageId\\": \\"1\\"}" ok -> "saved"',
    ]


@pytest.mark.parametrize("path", [
    # Seen in the live AGY and opencode runs: skills read, long output spilled to a file.
    r"<HOME>\.gemini\antigravity-cli\skills\guide\SKILL.md",
    "file:///<HOME>/.gemini/antigravity-cli/brain/44f7/.system_generated/steps/2/output.txt",
    r"<HOME>\.local\share\opencode\tool-output\tool_1",
])
def test_a_file_in_a_harness_home_folder_does_not_name_it(path: str) -> None:
    call = _tool(2, "DONE", "read_file", {"Path": path}, output=f"The full output is at {path}. Preview follows")
    assert tool_log([_jsonl([BEGIN, call])]) == (
        '[step 1] read "<harness file>" ok -> "The full output is at <harness file> Preview follows"')


def test_a_project_under_the_home_keeps_its_path() -> None:
    path = r"<HOME>\Code\arena\.venv\a.py"
    assert "Code" in tool_log([_jsonl([BEGIN, _tool(2, "DONE", "read_file", {"Path": path})])])


def test_a_run_with_no_calls_says_so() -> None:
    assert tool_log([_jsonl([BEGIN, FIRST_TURN, *LAST_TURN, RESULT])]) == "(no tool calls)"


def test_its_shell_commands_are_found() -> None:
    assert agent_commands(STREAM) == ["python x.py", "pytest"]


def test_its_personal_instructions_count_as_configuration(tmp_path: Path) -> None:
    rules = tmp_path / ".gemini" / "GEMINI.md"
    rules.parent.mkdir()
    rules.write_text("rules", encoding="utf-8")
    assert global_instruction_files("agy", tmp_path, {}) == [rules]
