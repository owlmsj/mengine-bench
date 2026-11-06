"""What the judge reads of a run: one tool log, the same for every harness (#70).

Raw stream tails carried the model id and each harness's event shapes, so the
judge was not blind. Each call becomes one line with a kind, its input, whether
it worked and a slice of its output; nothing else of the stream reaches the judge.
"""

from __future__ import annotations

import gzip
import json
import re
from collections.abc import Iterator, Mapping
from pathlib import Path
from urllib.parse import urlsplit

from mengine_bench.runner.agents import agy_tool_result, pi_tool_results, split_jsonl
from mengine_bench.runner.trace import codex_opened_urls

# A harness may write its scripts inside shell commands; most of those fit here (#70).
INPUT_CHARS = 1_500
OUTPUT_CHARS = 400
# A search shows its count and first results, else the judge reads it as empty (#176).
SEARCH_RESULTS = 5
RESULT_TITLE_CHARS = 80
SEARCH_OUTPUT_CHARS = 700
SEARCH_NOT_RECORDED = "(results not in the harness stream)"
FIRST_CALLS = 20
LAST_CALLS = 40
NO_CALLS = "(no tool calls)"
HARNESS_FILE_MARK = "<harness file>"
# A hidden folder in the home names its harness: .gemini/antigravity-cli, .local/share/opencode (#72).
_HARNESS_FILE = re.compile(r"(?:file:///)?<HOME>[\\/]+\.[^\s\"'`]+")
_KINDS = {"bash": "shell", "shell": "shell", "powershell": "shell", "run_command": "shell", "read": "read",
          "read_file": "read", "view_file": "read", "write": "write", "write_file": "write", "write_to_file": "write",
          "edit": "edit", "edit_file": "edit", "replace_file_content": "edit", "multi_replace_file_content": "edit",
          "sed_file": "edit", "notebook_edit": "edit", "multiedit": "edit", "notebookedit": "edit", "apply_patch": "edit",
          "patch": "edit", "grep": "search", "glob": "search", "grep_search": "search", "find_by_name": "search",
          "list_dir": "search", "websearch": "web_search", "search_web": "web_search", "webfetch": "fetch"}
_OPENCODE = {"step_start", "step_finish", "tool_use"}
_CODEX = {"turn.started", "turn.completed", "item.completed"}
_CLAUDE = {"assistant", "user"}
_PI = {"tool_execution_start", "agent_start", "turn_start"}


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + f"[... {len(text) - limit} chars cut by the benchmark]"


def _kind(name: str) -> str:
    low = name.lower()
    if "browser" in low or "computer" in low or "chrome" in low:
        return "browser"
    if low.startswith("mcp__"):
        return "mcp_tool_call"
    return _KINDS.get(low, "other")


def _input_text(kind: str, payload: object) -> str:
    """The command or the path: a written file's body is shown once, among the deliverables or the changes."""
    fields = _mapping(payload)
    if kind == "shell" and (fields.get("command") or fields.get("CommandLine")):
        return str(fields.get("command") or fields["CommandLine"])
    if kind in ("read", "write", "edit"):
        path = fields.get("path") or fields.get("file_path") or fields.get("notebook_path") or fields.get("Path")
        if path:
            return str(path)
    return payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _line(step: int, kind: str, payload: object, ok: bool, output: object, limit: int = OUTPUT_CHARS) -> str:
    text = output if isinstance(output, str) else "" if output is None else json.dumps(output, ensure_ascii=False)
    shown = _clip(_HARNESS_FILE.sub(HARNESS_FILE_MARK, _input_text(kind, payload)), INPUT_CHARS)
    result = _clip(_HARNESS_FILE.sub(HARNESS_FILE_MARK, text).strip(), limit)
    return (f"[step {step}] {kind} {json.dumps(shown, ensure_ascii=False)} {'ok' if ok else 'failed'} -> "
            f"{json.dumps(result, ensure_ascii=False)}")


def _search_results(rows: list[Mapping[str, object]]) -> str:
    """`N results: title (domain); ...` for the first few rows (#176)."""
    labels = []
    for row in rows[:SEARCH_RESULTS]:
        url = str(row.get("url") or "")
        domain = str(row.get("domain") or urlsplit(url).hostname or "")
        title = _clip(" ".join(str(row.get("title") or "").split()), RESULT_TITLE_CHARS)
        labels.append(f"{title} ({domain})" if title and domain and title != domain else title or url or domain)
    count = f"{len(rows)} result{'' if len(rows) == 1 else 's'}"
    return f"{count}: " + "; ".join(labels) if labels else count


def _search_line(step: int, kind: str, payload: object, ok: bool, rows: object, fallback: object) -> str:
    """A search with its result list; the harness text when the stream has no list, never a bare empty output."""
    if isinstance(rows, list):
        return _line(step, kind, payload, ok, _search_results([_mapping(row) for row in rows]), SEARCH_OUTPUT_CHARS)
    return _line(step, kind, payload, ok, fallback or SEARCH_NOT_RECORDED)


def _opencode_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    for event in events:
        if event.get("type") != "tool_use":
            continue
        part = _mapping(event.get("part"))
        state = _mapping(part.get("state"))
        exit_code = _mapping(_mapping(state.get("metadata")).get("metadata")).get("exit")
        ok = state.get("status") != "error" and exit_code in (None, 0)
        kind = _kind(str(part.get("tool") or ""))
        if kind == "web_search":
            yield _search_line(step, kind, state.get("input"), ok, None, state.get("output"))
            continue
        yield _line(step, kind, state.get("input"), ok, state.get("output"))


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
        elif kind == "web_search":
            action = dict(_mapping(item.get("action")))
            if item.get("query") and not (action.get("query") or action.get("queries")):
                action["query"] = item["query"]
            opened = codex_opened_urls(item)
            if opened:
                action["opened_urls"] = opened
            web_kind = "fetch" if action.get("type") in {"open_page", "open"} else "web_search"
            yield _search_line(step, web_kind, action, ok, item.get("results"), "")
        elif kind == "mcp_tool_call":
            name = f"{item.get('server', '')}.{item.get('tool', '')}"
            # The text only: a result's `_meta` names the harness.
            result = _mapping(item.get("result"))
            yield _line(step, "browser" if _kind(name) == "browser" else "mcp_tool_call",
                        {"tool": name, "arguments": item.get("arguments")}, ok, _blocks_text(result.get("content")))


def _blocks_text(content: object) -> str:
    if isinstance(content, str):
        return content
    blocks = content if isinstance(content, list) else []
    return " ".join(str(_mapping(block).get("text") or "") for block in blocks)


def _claude_links(event: Mapping[str, object]) -> list[object] | None:
    """WebSearch links from `tool_use_result.results[].content`; the model's text holds them as a JSON dump (#176)."""
    found = _mapping(event.get("tool_use_result")).get("results")
    if not isinstance(found, list):
        return None
    blocks = [_mapping(entry).get("content") for entry in found]
    return [link for block in blocks if isinstance(block, list) for link in block]


def _claude_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    results: dict[str, Mapping[str, object]] = {}
    links: dict[str, list[object] | None] = {}
    for event in events:
        content = _mapping(event.get("message")).get("content")
        if event.get("type") != "user" or not isinstance(content, list):
            continue
        blocks = [_mapping(block) for block in content if _mapping(block).get("type") == "tool_result"]
        results.update({str(block.get("tool_use_id")): block for block in blocks})
        # `tool_use_result` belongs to the event, so it names a call only when the event holds one result.
        if len(blocks) == 1:
            links[str(blocks[0].get("tool_use_id"))] = _claude_links(event)
    for event in events:
        content = _mapping(event.get("message")).get("content")
        if event.get("type") != "assistant" or not isinstance(content, list):
            continue
        for block in map(_mapping, content):
            if block.get("type") != "tool_use":
                continue
            result = results.get(str(block.get("id")), {})
            kind = _kind(str(block.get("name") or ""))
            text = _blocks_text(result.get("content"))
            if kind == "web_search":
                yield _search_line(step, kind, block.get("input"), not result.get("is_error"),
                                   links.get(str(block.get("id"))), text)
                continue
            yield _line(step, kind, block.get("input"), not result.get("is_error"), text)


def _agy_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    for event in events:
        update = _mapping(event.get("step_update"))
        if update.get("step_type") != "tool" or update.get("state") == "ACTIVE":
            continue
        info = _mapping(update.get("tool_info"))
        exit_code, output = agy_tool_result(info)
        ok = update.get("state") == "DONE" and exit_code in (None, 0)
        kind = _kind(str(update.get("tool_name") or ""))
        if kind == "web_search":
            yield _search_line(step, kind, info.get("parameters"), ok, None, output)
            continue
        yield _line(step, kind, info.get("parameters"), ok, output)


def _pi_calls(step: int, events: list[dict[str, object]]) -> Iterator[str]:
    """One line per finished call: the start holds the arguments, the end the result (pi docs/json.md:105-107)."""
    ends = pi_tool_results(events)
    for event in events:
        end = ends.get(str(event.get("toolCallId")))
        if event.get("type") != "tool_execution_start" or end is None:
            continue
        result = _mapping(end.get("result"))
        exit_code = _mapping(result.get("structuredContent")).get("exit_code")
        ok = end.get("isError") is not True and exit_code in (None, 0)
        kind = _kind(str(event.get("toolName") or ""))
        text = _blocks_text(result.get("content"))
        if kind == "web_search":
            yield _search_line(step, kind, event.get("args"), ok, None, text)
            continue
        yield _line(step, kind, event.get("args"), ok, text)


def stream_calls(step: int, stdout: str) -> list[str] | None:
    """One line per tool call, or None when the stream is no known harness's."""
    events = split_jsonl(stdout)
    kinds = {event.get("type") for event in events}
    if any(event.get("event") == "step_update" for event in events):
        return list(_agy_calls(step, events))
    if kinds & _PI:
        return list(_pi_calls(step, events))
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


def _tool_output_texts(events: list[dict[str, object]]) -> Iterator[str]:
    """The whole output of each tool call, per harness shape, never the model's own text (#185)."""
    for event in events:
        update = _mapping(event.get("step_update"))
        if update.get("step_type") == "tool":
            yield agy_tool_result(_mapping(update.get("tool_info")))[1]
        if event.get("type") == "tool_execution_end":
            yield _blocks_text(_mapping(event.get("result")).get("content"))
        part = _mapping(event.get("part"))
        if event.get("type") == "tool_use":
            yield str(_mapping(part.get("state")).get("output") or "")
        item = _mapping(event.get("item"))
        if event.get("type") == "item.completed" and item.get("type") in ("command_execution", "mcp_tool_call"):
            yield str(item.get("aggregated_output") or "") + _blocks_text(_mapping(item.get("result")).get("content"))
        content = _mapping(event.get("message")).get("content")
        if event.get("type") == "user" and isinstance(content, list):
            yield from (_blocks_text(_mapping(block).get("content")) for block in content
                        if _mapping(block).get("type") == "tool_result")


def tool_outputs(streams: list[str]) -> list[str]:
    """Every tool call's full output across the steps (no OUTPUT_CHARS clip), for host-refusal detection."""
    return [text for stdout in streams for text in _tool_output_texts(split_jsonl(stdout)) if text]
