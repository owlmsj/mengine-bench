"""Adapter argv construction and transcript parsing; never launches a real agent CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from mengine_bench.runner.agents import (
    AgentError, ClaudeAgent, CmdAgent, CodexAgent, OpencodeAgent, make_agent, parse_claude_stream,
    parse_codex_jsonl, parse_opencode_jsonl, split_jsonl,
)

WS = Path("ws")
PROMPT_FILE = Path("prompts") / "step-0.md"


def tail(argv: list[str]) -> list[str]:
    # argv[0] is resolved through PATH and differs per host.
    return argv[1:]


def test_claude_new_session_reads_prompt_from_stdin() -> None:
    agent = ClaudeAgent(model="claude-opus-5-5", effort="xhigh")
    call = agent.invocation("do it", PROMPT_FILE, WS, session_id=None, attachments=())
    assert tail(call.argv) == ["-p", "--output-format", "stream-json", "--verbose", "--model", "claude-opus-5-5",
                               "--effort", "xhigh", "--permission-mode", "bypassPermissions"]
    assert call.stdin_text == "do it"
    assert Path(call.argv[0]).stem.lower() == "claude"


def test_claude_resume_and_compact() -> None:
    agent = ClaudeAgent(model="m", effort=None)
    call = agent.invocation("next", PROMPT_FILE, WS, session_id="abc", attachments=())
    assert tail(call.argv)[-2:] == ["--resume", "abc"]
    assert "--effort" not in call.argv
    assert agent.supports_resume and agent.supports_compact
    assert agent.compact_prompt == "/compact"


def test_codex_new_and_resume() -> None:
    agent = CodexAgent(model="gpt-6", effort="high")
    first = agent.invocation("p", PROMPT_FILE, WS, session_id=None, attachments=("images/a.png",))
    assert tail(first.argv) == ["exec", "--json", "--skip-git-repo-check", "-m", "gpt-6",
                                "-c", 'model_reasoning_effort="high"',
                                "--dangerously-bypass-approvals-and-sandbox", "-i", "images/a.png", "-"]
    assert first.stdin_text == "p"
    resumed = agent.invocation("p2", PROMPT_FILE, WS, session_id="t-1", attachments=())
    assert tail(resumed.argv)[:2] == ["exec", "resume"]
    assert tail(resumed.argv)[-2:] == ["t-1", "-"]
    assert agent.supports_resume and not agent.supports_compact


def test_opencode_short_prompt_in_argv_long_prompt_on_stdin() -> None:
    agent = OpencodeAgent(model="deepseek/flash", effort="high")
    short = agent.invocation("hi", PROMPT_FILE, WS, session_id="ses_1", attachments=("a.png",))
    assert tail(short.argv) == ["run", "--standalone", "--auto", "--format", "json", "-m", "deepseek/flash#high",
                                "--session", "ses_1", "--file", "a.png", "hi"]
    assert short.stdin_text is None
    long = agent.invocation("x" * 40_000, PROMPT_FILE, WS, session_id=None, attachments=())
    assert long.argv[-1] == "deepseek/flash#high"
    assert long.stdin_text == "x" * 40_000


def test_cmd_template_substitutes_placeholders_per_argument() -> None:
    template = json.dumps(["python", "my agent.py", "--ws={workspace}", "{prompt_file}", "{model}"])
    agent = CmdAgent(template=template, model="m1", effort=None)
    call = agent.invocation("p", Path("dir with space") / "p.md", Path("w s"), session_id=None, attachments=())
    assert call.argv == ["python", "my agent.py", f"--ws={Path('w s')}", str(Path("dir with space") / "p.md"), "m1"]
    assert call.stdin_text is None
    assert not agent.supports_resume


def test_cmd_template_plain_string_is_split_without_a_shell() -> None:
    agent = CmdAgent(template="my-agent --run {prompt_file}", model="m", effort=None)
    assert agent.invocation("p", Path("p.md"), WS, None, ()).argv == ["my-agent", "--run", "p.md"]
    with pytest.raises(ValueError, match="prompt_file"):
        CmdAgent(template="my-agent --run", model="m", effort=None)


def test_make_agent_rejects_unknown_names() -> None:
    assert isinstance(make_agent("codex", "m", None, None), CodexAgent)
    with pytest.raises(ValueError, match="'gemini'"):
        make_agent("gemini", "m", None, None)
    with pytest.raises(ValueError, match="--cmd"):
        make_agent("cmd", "m", None, None)


def test_jsonl_splits_on_newline_only() -> None:
    line = json.dumps({"type": "text", "part": {"text": "a b"}}, ensure_ascii=False)
    assert split_jsonl(line + "\r\n" + line + "\n") == [{"type": "text", "part": {"text": "a b"}}] * 2


def test_parse_claude_stream() -> None:
    events = [{"type": "system", "subtype": "init", "session_id": "s1"},
              {"type": "assistant", "message": {"content": [{"type": "text", "text": "x"}]}},
              {"type": "result", "subtype": "success", "is_error": False, "result": "final answer",
               "session_id": "s1"}]
    stdout = "\n".join(json.dumps(e, ensure_ascii=False) for e in events)
    parsed = parse_claude_stream(stdout, 0)
    assert (parsed.answer, parsed.session_id) == ("final answer", "s1")
    failed = stdout.replace('"is_error": false', '"is_error": true')
    with pytest.raises(AgentError, match="is_error"):
        parse_claude_stream(failed, 0)
    with pytest.raises(AgentError, match="no result"):
        parse_claude_stream(json.dumps(events[0]), 0)


def test_parse_codex_jsonl() -> None:
    events = [{"type": "thread.started", "thread_id": "t-9"},
              {"type": "item.completed", "item": {"type": "agent_message", "text": "first"}},
              {"type": "item.completed", "item": {"type": "agent_message", "text": "last"}},
              {"type": "turn.completed"}]
    parsed = parse_codex_jsonl("\n".join(json.dumps(e) for e in events), 0)
    assert (parsed.answer, parsed.session_id) == ("last", "t-9")
    with pytest.raises(AgentError, match="turn.failed"):
        parse_codex_jsonl(json.dumps({"type": "turn.failed", "error": {"message": "x"}}), 0)


def test_parse_opencode_jsonl() -> None:
    events = [{"type": "step_start", "sessionID": "ses_7", "part": {}},
              {"type": "text", "sessionID": "ses_7", "part": {"text": "he"}},
              {"type": "text", "sessionID": "ses_7", "part": {"text": "llo"}},
              {"type": "step_finish", "sessionID": "ses_7", "part": {"reason": "stop"}}]
    parsed = parse_opencode_jsonl("\n".join(json.dumps(e) for e in events), 0)
    assert (parsed.answer, parsed.session_id) == ("hello", "ses_7")
    truncated = [*events[:-1], {"type": "step_finish", "part": {"reason": "length"}}]
    with pytest.raises(AgentError, match="length"):
        parse_opencode_jsonl("\n".join(json.dumps(e) for e in truncated), 0)
    with pytest.raises(AgentError, match="exit"):
        parse_opencode_jsonl("", 2)


# R16 (release review): a success-looking stream is not enough; the exit code
# and the adapter's terminal completion event must both say the run finished.
CLAUDE_OK = [{"type": "system", "subtype": "init", "session_id": "s1"},
             {"type": "result", "subtype": "success", "is_error": False, "result": "done", "session_id": "s1"}]


def _jsonl(events: list[dict[str, object]]) -> str:
    return "\n".join(json.dumps(e) for e in events)


def test_claude_success_event_with_failing_exit_is_a_crash() -> None:
    with pytest.raises(AgentError, match="exit=7"):
        parse_claude_stream(_jsonl(CLAUDE_OK), 7)


def test_codex_message_without_turn_completed_is_a_crash() -> None:
    truncated = [{"type": "thread.started", "thread_id": "t-1"}, {"type": "turn.started"},
                 {"type": "item.completed", "item": {"type": "agent_message", "text": "partial"}}]
    with pytest.raises(AgentError, match="turn.completed"):
        parse_codex_jsonl(_jsonl(truncated), 0)
    # A later turn that started and never completed is truncated too.
    restarted = [*truncated, {"type": "turn.completed"}, {"type": "turn.started"},
                 {"type": "item.completed", "item": {"type": "agent_message", "text": "half"}}]
    with pytest.raises(AgentError, match="turn.completed"):
        parse_codex_jsonl(_jsonl(restarted), 0)


def test_opencode_text_without_terminal_stop_is_a_crash() -> None:
    text_only = [{"type": "step_start", "sessionID": "ses_1", "part": {}},
                 {"type": "text", "sessionID": "ses_1", "part": {"text": "partial"}}]
    mid_tool = [*text_only, {"type": "step_finish", "sessionID": "ses_1", "part": {"reason": "tool-calls"}}]
    with pytest.raises(AgentError, match="tool-calls"):
        parse_opencode_jsonl(_jsonl(mid_tool), 0)
    # A last step that never produced text is still not an answer.
    silent = [*mid_tool, {"type": "step_start", "sessionID": "ses_1", "part": {}}]
    with pytest.raises(AgentError, match="step_finish"):
        parse_opencode_jsonl(_jsonl(silent), 0)


# opencode 2.0.29 `run --format json` returns on session.execution.succeeded and can
# drop the last step's step_finish (cli/src/run/noninteractive.ts); failures and
# interruptions emit an error event and exit 1. Real FULL transcript: 18 step_start,
# 17 step_finish, last finish "tool-calls", final answer text after the 18th start.
def test_opencode_final_answer_step_without_step_finish_is_complete() -> None:
    events = [{"type": "step_start", "sessionID": "ses_2", "part": {}},
              {"type": "tool_use", "sessionID": "ses_2", "part": {"tool": "read"}},
              {"type": "step_finish", "sessionID": "ses_2", "part": {"reason": "tool-calls"}},
              {"type": "step_start", "sessionID": "ses_2", "part": {}},
              {"type": "text", "sessionID": "ses_2", "part": {"text": "final answer"}}]
    parsed = parse_opencode_jsonl(_jsonl(events), 0)
    assert (parsed.answer, parsed.session_id) == ("final answer", "ses_2")
    with pytest.raises(AgentError, match="exit"):
        parse_opencode_jsonl(_jsonl(events), 1)


# R17: judges read untrusted answers, diffs and screenshots, so their argv
# must not grant tools, approvals or a repo-shaped cwd.
def _pair(argv: list[str], flag: str) -> str:
    return argv[argv.index(flag) + 1]


def test_claude_judge_invocation_has_no_tools(tmp_path: Path) -> None:
    call = ClaudeAgent(model="claude-opus-5-5", effort="xhigh").judge_invocation("grade", tmp_path, ())
    argv = tail(call.argv)
    assert _pair(argv, "--tools") == ""
    assert _pair(argv, "--permission-mode") == "dontAsk"
    assert {"--restricted", "--strict-mcp-config", "--no-session-persistence"} <= set(argv)
    assert "bypassPermissions" not in argv and "--resume" not in argv
    assert call.stdin_text == "grade"


def test_claude_judge_sends_images_inline_without_a_read_tool(tmp_path: Path) -> None:
    (tmp_path / "screenshot.png").write_bytes(b"\x89PNG demo")
    call = ClaudeAgent(model="m", effort=None).judge_invocation("look", tmp_path, ("screenshot.png",))
    assert _pair(tail(call.argv), "--input-format") == "stream-json"
    assert _pair(tail(call.argv), "--tools") == ""
    assert call.stdin_text is not None and call.stdin_text.endswith("\n")
    message = json.loads(call.stdin_text)
    assert message["type"] == "user"
    blocks = message["message"]["content"]
    assert blocks[0] == {"type": "text", "text": "look"}
    assert blocks[1]["type"] == "image"
    assert blocks[1]["source"] == {"type": "base64", "media_type": "image/png", "data": "iVBORyBkZW1v"}


def test_codex_judge_invocation_is_read_only_and_ephemeral(tmp_path: Path) -> None:
    call = CodexAgent(model="gpt-6", effort="high").judge_invocation("grade", tmp_path, ("screenshot.png",))
    argv = tail(call.argv)
    assert _pair(argv, "--sandbox") == "read-only"
    assert "--dangerously-bypass-approvals-and-sandbox" not in argv
    assert {"--ephemeral", "--ignore-user-config", "--ignore-rules"} <= set(argv)
    disabled = {argv[i + 1] for i, arg in enumerate(argv) if arg == "--disable"}
    assert {"shell_tool", "unified_exec", "apps", "browser_use", "computer_use"} <= disabled
    assert _pair(argv, "-i") == "screenshot.png" and argv[-1] == "-"
    assert "--search" not in argv


def test_opencode_judge_invocation_denies_tools(tmp_path: Path) -> None:
    call = OpencodeAgent(model="p/m", effort=None).judge_invocation("grade", tmp_path, ())
    assert "--auto" not in call.argv
    assert call.env is not None
    config = json.loads(call.env["OPENCODE_CONFIG_CONTENT"])
    assert {config["permission"][tool] for tool in ("edit", "bash", "webfetch", "external_directory")} == {"deny"}


# opencode 2.0.29 resolves its root as process.env.PWD ?? process.cwd() (cli/src/run/run.ts:73).
# Popen(cwd=workspace) kept the caller's PWD, so a FULL run worked in the bench checkout and
# wrote task files there instead of the workspace.
def test_agent_step_runs_with_pwd_set_to_the_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace

    from mengine_bench.runner import task_run

    seen: dict[str, object] = {}

    def fake_run(argv, cwd, timeout_s, stdin_text=None, env=None):
        seen.update(cwd=cwd, env=env)
        raise OSError("stop after capture")

    monkeypatch.setattr(task_run.process, "run_process", fake_run)
    monkeypatch.setenv("PWD", "/somewhere/else")
    workspace = tmp_path / "ws"
    workspace.mkdir()
    agent = CmdAgent(template="my-agent {prompt_file}", model="m", effort=None)
    record = SimpleNamespace(steps=[])
    with pytest.raises(Exception, match="could not start agent"):
        task_run._invoke(agent, SimpleNamespace(timeout_s=5), workspace, tmp_path, "0", "do it",
                         None, record, (), 0)
    env = seen["env"]
    assert isinstance(env, dict)
    assert env["PWD"] == str(workspace.resolve())
    assert env.get("PATH") == os.environ.get("PATH")


def test_claude_real_usage() -> None:
    parsed = parse_claude_stream(_jsonl([{
        "type": "result", "subtype": "success", "is_error": False, "result": "done",
        "total_cost_usd": 0.00369365,
        "usage": {"input_tokens": 2, "cache_creation_input_tokens": 17537,
                  "cache_read_input_tokens": 16405, "output_tokens": 44,
                  "output_tokens_details": {"thinking_tokens": 40}}, "num_turns": 1,
    }]), 0)
    from mengine_bench.runner.agents import Usage
    assert parsed.usage == Usage(33944, 16405, 44, 40, 0.00369365, "harness")


@pytest.mark.parametrize("answer", ["", "   ", "\n\t"])
def test_claude_empty_answer_rejected(answer: str) -> None:
    with pytest.raises(AgentError, match="received result=.*expected non-empty answer text"):
        parse_claude_stream(_jsonl([{**CLAUDE_OK[-1], "result": answer}]), 0)


def test_codex_real_usage_sums_all_turns() -> None:
    from mengine_bench.runner.agents import Usage
    turn = {"type": "turn.completed", "usage": {
        "input_tokens": 22329, "cached_input_tokens": 13312, "cache_write_input_tokens": 0,
        "output_tokens": 5, "reasoning_output_tokens": 0}}
    events = [turn, {"type": "item.completed", "item": {"type": "agent_message", "text": "done"}}, turn]
    assert parse_codex_jsonl(_jsonl(events), 0).usage == Usage(44658, 26624, 10, 0, None, "none")


@pytest.mark.parametrize("partial", [False, True])
def test_opencode_usage_sums_steps(partial: bool) -> None:
    from mengine_bench.runner.agents import Usage
    finish = {"type": "step_finish", "part": {"reason": "stop", "cost": 0.25,
              "tokens": {"input": 10, "output": 5, "reasoning": 2, "cache": {"read": 7, "write": 3}}}}
    events = [finish, finish]
    if partial:
        events.append({"type": "step_start"})
    events.append({"type": "text", "part": {"text": "done"}})
    assert parse_opencode_jsonl(_jsonl(events), 0).usage == Usage(
        40, 14, 10, 4, 0.5, "partial" if partial else "harness")


@pytest.mark.parametrize("bad", [None, "3", True, -1, 1.5, {}, []])
def test_malformed_usage_fields_are_unknown(bad: object) -> None:
    parsed = parse_claude_stream(_jsonl([{**CLAUDE_OK[-1], "total_cost_usd": "bad",
        "usage": {"input_tokens": bad, "cache_creation_input_tokens": 2,
                  "cache_read_input_tokens": bad, "output_tokens": bad,
                  "output_tokens_details": {"thinking_tokens": bad}}}]), 0)
    from mengine_bench.runner.agents import Usage
    assert parsed.usage == Usage(None, None, None, None, None, "none")


def test_opencode_without_finish_has_unknown_partial_usage() -> None:
    from mengine_bench.runner.agents import Usage
    events = [{"type": "step_start"}, {"type": "text", "part": {"text": "done"}}]
    assert parse_opencode_jsonl(_jsonl(events), 0).usage == Usage(None, None, None, None, None, "partial")


def test_task_usage_totals_preserve_unknown_cost() -> None:
    from mengine_bench.runner.agents import Usage
    from mengine_bench.runner.task_run import StepRecord, TaskRunRecord
    record = TaskRunRecord("usage")
    assert record.usage is None
    record.steps.append(StepRecord(0, 1.0, 0, "ok", usage=Usage(10, 2, 3, 1, 0.2, "harness")))
    record.steps.append(StepRecord(1, 1.0, None, "timeout"))
    assert record.usage == Usage(10, 2, 3, 1, 0.2, "harness")
    record.steps.append(StepRecord(2, 1.0, 0, "ok", usage=Usage(5, 1, 2, None, None, "none")))
    assert record.usage == Usage(15, 3, 5, None, None, "none")


def test_codex_malformed_turn_does_not_become_zero() -> None:
    from mengine_bench.runner.agents import Usage
    events = [{"type": "item.completed", "item": {"type": "agent_message", "text": "done"}},
              {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}},
              {"type": "turn.completed", "usage": {"input_tokens": "bad", "output_tokens": 2}}]
    assert parse_codex_jsonl(_jsonl(events), 0).usage == Usage(None, None, 7, None, None, "none")


@pytest.mark.parametrize("cost", [None, "bad", True, -1, float("nan"), float("inf")])
def test_opencode_invalid_cost_and_tokens_are_unknown(cost: object) -> None:
    from mengine_bench.runner.agents import Usage
    events = [{"type": "text", "part": {"text": "done"}},
              {"type": "step_finish", "part": {"reason": "stop", "cost": cost, "tokens": []}}]
    assert parse_opencode_jsonl(_jsonl(events), 0).usage == Usage(None, None, None, None, None, "none")


def test_cmd_usage_is_unmeasured() -> None:
    assert CmdAgent("agent {prompt_file}", "m", None).parse("done", 0).usage is None
