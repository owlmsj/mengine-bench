"""What the judge reads of a run: one tool log, the same for every harness (#70).

Raw stream tails carried the model id and each harness's event shapes, so the
judge was not blind. Each call becomes one line with a kind, its input, whether
it worked and a slice of its output; nothing else of the stream reaches the judge.
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterator, Mapping
from pathlib import Path

from mengine_bench.runner.agents import split_jsonl

# A harness may write its scripts inside shell commands; most of those fit here (#70).
INPUT_CHARS = 1_500
OUTPUT_CHARS = 400
FIRST_CALLS = 20
LAST_CALLS = 40
NO_CALLS = "(no tool calls)"
_KINDS = {"bash": "shell", "shell": "shell", "powershell": "shell", "read": "read", "write": "write", "edit": "edit",
          "multiedit": "edit", "notebookedit": "edit", "apply_patch": "edit", "patch": "edit", "grep": "search",
          "glob": "search"}
_OPENCODE = {"step_start", "step_finish", "tool_use"}
_CODEX = {"turn.started", "turn.completed", "item.completed"}
_CLAUDE = {"assistant", "user"}


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + f"[... {len(text) - limit} chars cut by the benchmark]"


def _kind(name: str) -> str:
    low = name.lower()
    if "browser" in low or "computer" in low:
        return "browser"
    return _KINDS.get(low, "other")


def _input_text(kind: str, payload: object) -> str:
    """The command or the path: a written file's body is shown once, among the deliverables or the changes."""
    fields = _mapping(payload)
    if kind == "shell" and fields.get("command"):
        return str(fields["command"])
    if kind in ("read", "write", "edit"):
        path = fields.get("path") or fields.get("file_path") or fields.get("notebook_path")
        if path:
            return str(path)
    return payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _line(step: int, kind: str, payload: object, ok: bool, output: object) -> str:
    text = output if isinstance(output, str) else "" if output is None else json.dumps(output, ensure_ascii=False)
    shown = _clip(_input_text(kind, payload), INPUT_CHARS)
    return (f"[step {step}] {kind} {json.dumps(shown, ensure_ascii=False)} {'ok' if ok else 'failed'} -> "
            f"{json.dumps(_clip(text.strip(), OUTPUT_CHARS), ensure_ascii=False)}")


def _opencode_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    for event in events:
        if event.get("type") != "tool_use":
            continue
        part = _mapping(event.get("part"))
        state = _mapping(part.get("state"))
        exit_code = _mapping(_mapping(state.get("metadata")).get("metadata")).get("exit")
        ok = state.get("status") != "error" and exit_code in (None, 0)
        yield _line(step, _kind(str(part.get("tool") or "")), state.get("input"), ok, state.get("output"))


def _codex_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    for event in events:
        if event.get("type") != "item.completed":
            continue
        item = _mapping(event.get("item"))
        kind = item.get("type")
        ok = item.get("status") != "failed" and item.get("exit_code") in (None, 0)
        if kind == "command_execution":
            yield _line(step, "shell", {"command": item.get("command")}, ok, item.get("aggregated_output"))
        elif kind == "file_change":
            changes = item.get("changes")
            paths = [_mapping(change).get("path") for change in changes] if isinstance(changes, list) else []
            yield _line(step, "edit", ", ".join(str(path) for path in paths), ok, "")
        elif kind in ("mcp_tool_call", "web_search"):
            name = f"{item.get('server', '')}_{item.get('tool', kind)}"
            # The text only: a result's `_meta` names the harness.
            result = _mapping(item.get("result"))
            yield _line(step, _kind(name), item.get("arguments") or item.get("query"), ok, _blocks_text(result.get("content")))


def _blocks_text(content: object) -> str:
    if isinstance(content, str):
        return content
    blocks = content if isinstance(content, list) else []
    return " ".join(str(_mapping(block).get("text") or "") for block in blocks)


def _claude_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    results: dict[str, Mapping[str, object]] = {}
    for event in events:
        content = _mapping(event.get("message")).get("content")
        if event.get("type") == "user" and isinstance(content, list):
            results.update({str(_mapping(block).get("tool_use_id")): _mapping(block) for block in content
                            if _mapping(block).get("type") == "tool_result"})
    for event in events:
        content = _mapping(event.get("message")).get("content")
        if event.get("type") != "assistant" or not isinstance(content, list):
            continue
        for block in map(_mapping, content):
            if block.get("type") != "tool_use":
                continue
            result = results.get(str(block.get("id")), {})
            yield _line(step, _kind(str(block.get("name") or "")), block.get("input"), not result.get("is_error"),
                        _blocks_text(result.get("content")))


def stream_calls(step: int, stdout: str) -> list[str] | None:
    """One line per tool call, or None when the stream is no known harness's."""
    events = split_jsonl(stdout)
    kinds = {event.get("type") for event in events}
    if kinds & _OPENCODE:
        return list(_opencode_calls(step, events))
    if kinds & _CODEX:
        return list(_codex_calls(step, events))
    if kinds & _CLAUDE:
        return list(_claude_calls(step, events))
    return None


def tool_log(streams: list[str]) -> str:
    """Every step's calls, in order; empty when no stream is a known harness's (a `cmd` agent)."""
    parts = [stream_calls(index, stdout) for index, stdout in enumerate(streams, start=1)]
    if all(part is None for part in parts):
        return ""
    calls = [line for part in parts for line in part or []]
    if len(calls) > FIRST_CALLS + LAST_CALLS:
        cut = len(calls) - FIRST_CALLS - LAST_CALLS
        calls = [*calls[:FIRST_CALLS], f"[... {cut} calls cut by the benchmark]", *calls[-LAST_CALLS:]]
    return "\n".join(calls) or NO_CALLS


def transcript_streams(path: Path) -> list[str]:
    """The stdout of each step from a bundle's transcripts/<task>.jsonl.gz."""
    if not path.is_file():
        return []
    streams: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as stored:
        for line in stored:
            if not line.strip().startswith("{"):
                continue
            record = json.loads(line)
            if record.get("stream") == "stdout":
                streams[str(record.get("step"))] = str(record.get("text") or "")
    return [streams[step] for step in sorted(streams, key=lambda name: (len(name), name))]
