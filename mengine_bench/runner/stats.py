"""Run statistics read from a harness's event stream; never part of the Score (#39).

They come from the stream rather than from `Usage`, so a run stopped at its limit
still has them. None means the harness does not report that value, never zero:
only opencode stamps its events, so the time fields are None for Claude and Codex;
AGY reports each step's duration, so it has tool time and turn rates.
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field

from mengine_bench.runner.agents import agy_tool_result, split_jsonl

SHELL_TOOLS = frozenset({"bash", "shell", "run_command"})
WRITE_TOOLS = frozenset({"write", "edit", "multiedit", "notebookedit", "apply_patch", "patch", "write_file", "edit_file",
                         "write_to_file", "replace_file_content", "multi_replace_file_content", "sed_file", "notebook_edit"})
# Below this a turn's rate says more about fixed latency than about generation.
TURN_RATE_MIN_TOKENS = 500
OUTSIDE_PATH_MARKS = ("../", "..\\")
# Only where a tool is told where to act: a file body can hold relative imports.
OUTSIDE_PATH_FIELDS = ("path", "file_path", "notebook_path", "workdir", "command", "Path", "CommandLine")


@dataclass
class RunStats:
    model_turns: int = 0
    tool_calls: int = 0
    tool_errors: int = 0
    shell_commands: int = 0
    shell_failures: int = 0
    file_writes: int = 0
    repeated_tool_calls: int = 0
    outside_path_uses: int = 0
    input_tokens: int | None = None
    cached_input_tokens: int | None = None
    # Everything the model generated, reasoning included, on every harness.
    generated_tokens: int | None = None
    reasoning_tokens: int | None = None
    largest_turn_tokens: int | None = None
    first_tool_s: float | None = None
    first_write_s: float | None = None
    last_event_s: float | None = None
    # opencode's tool clock can start while the arguments are generated.
    tool_s: float | None = None
    # Between one turn's end and the next one's start: prefill and queue.
    wait_s: float | None = None
    turn_rates: list[float] = field(default_factory=list)


def stats_record(stats: RunStats) -> dict[str, object]:
    """JSON form: the rates as one median, the times rounded."""
    record = asdict(stats)
    rates = record.pop("turn_rates")
    record["turn_tps_median"] = round(statistics.median(rates), 1) if rates else None
    return {key: round(value, 2) if isinstance(value, float) else value for key, value in record.items()}


def _add(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return left if right is None else right
    return left + right


def merge_stats(parts: Iterable[RunStats]) -> RunStats:
    """Several steps or tasks: counts and tokens add up, the firsts keep the earliest part that has one."""
    merged = RunStats()
    for part in parts:
        for name in ("model_turns", "tool_calls", "tool_errors", "shell_commands", "shell_failures", "file_writes",
                     "repeated_tool_calls", "outside_path_uses", "input_tokens", "cached_input_tokens",
                     "generated_tokens", "reasoning_tokens", "last_event_s", "tool_s", "wait_s"):
            setattr(merged, name, _add(getattr(merged, name), getattr(part, name)))
        if part.largest_turn_tokens is not None:
            merged.largest_turn_tokens = max(merged.largest_turn_tokens or 0, part.largest_turn_tokens)
        merged.first_tool_s = part.first_tool_s if merged.first_tool_s is None else merged.first_tool_s
        merged.first_write_s = part.first_write_s if merged.first_write_s is None else merged.first_write_s
        merged.turn_rates.extend(part.turn_rates)
    return merged


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _count(value: object) -> int:
    return value if type(value) is int and value >= 0 else 0


def _names_parent_path(payload: object) -> bool:
    fields = [payload.get(key) for key in OUTSIDE_PATH_FIELDS] if isinstance(payload, dict) else [payload]
    text = json.dumps(fields, ensure_ascii=False).replace("\\\\", "\\")
    return any(mark in text for mark in OUTSIDE_PATH_MARKS)


def _note_tool(stats: RunStats, seen: set[str], name: str, payload: object, *, failed: bool = False,
               exit_code: object = None, at_s: float | None = None) -> None:
    tool = name.lower()
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    stats.tool_calls += 1
    stats.tool_errors += failed
    stats.repeated_tool_calls += f"{tool}:{text}" in seen
    seen.add(f"{tool}:{text}")
    stats.outside_path_uses += _names_parent_path(payload)
    if stats.first_tool_s is None:
        stats.first_tool_s = at_s
    if tool in SHELL_TOOLS:
        stats.shell_commands += 1
        stats.shell_failures += type(exit_code) is int and exit_code != 0
    if tool in WRITE_TOOLS:
        stats.file_writes += 1
        if stats.first_write_s is None:
            stats.first_write_s = at_s


def _note_tokens(stats: RunStats, prompt: int, cached: int, generated: int, reasoning: int) -> None:
    stats.input_tokens = (stats.input_tokens or 0) + prompt
    stats.cached_input_tokens = (stats.cached_input_tokens or 0) + cached
    stats.generated_tokens = (stats.generated_tokens or 0) + generated
    stats.reasoning_tokens = (stats.reasoning_tokens or 0) + reasoning
    stats.largest_turn_tokens = max(stats.largest_turn_tokens or 0, generated)


def _opencode_stats(events: list[dict[str, object]]) -> RunStats:
    stats = RunStats(tool_s=0.0, wait_s=0.0)
    seen: set[str] = set()
    stamps = [event["timestamp"] for event in events if type(event.get("timestamp")) is int]
    origin = stamps[0] if stamps else 0
    stats.last_event_s = (stamps[-1] - origin) / 1000 if stamps else None
    began, ended = None, None
    for event in events:
        kind, stamp, part = event.get("type"), event.get("timestamp"), _mapping(event.get("part"))
        known = type(stamp) is int
        # Counted on start: opencode can drop the last step_finish, and a stopped turn has none.
        stats.model_turns += kind == "step_start"
        if kind == "step_start" and known:
            began = stamp
            stats.wait_s += (stamp - ended) / 1000 if ended is not None else 0.0
        elif kind == "tool_use":
            _opencode_tool(stats, seen, part, (stamp - origin) / 1000 if known else None)
        elif kind == "step_finish":
            ended = stamp if known else ended
            _opencode_turn(stats, part, stamp - began if known and began is not None else None)
    return stats


def _opencode_tool(stats: RunStats, seen: set[str], part: Mapping[str, object], at_s: float | None) -> None:
    state = _mapping(part.get("state"))
    times = _mapping(state.get("time"))
    if type(times.get("start")) is int and type(times.get("end")) is int:
        stats.tool_s += (times["end"] - times["start"]) / 1000
    inner = _mapping(_mapping(state.get("metadata")).get("metadata"))
    _note_tool(stats, seen, str(part.get("tool") or ""), state.get("input"), failed=state.get("status") == "error",
               exit_code=inner.get("exit"), at_s=at_s)


def _opencode_turn(stats: RunStats, part: Mapping[str, object], elapsed_ms: int | None) -> None:
    tokens = _mapping(part.get("tokens"))
    cache = _mapping(tokens.get("cache"))
    reasoning = _count(tokens.get("reasoning"))
    # opencode reports reasoning apart from output; Claude and Codex count it inside.
    generated = _count(tokens.get("output")) + reasoning
    cached = _count(cache.get("read"))
    _note_tokens(stats, _count(tokens.get("input")) + _count(cache.get("write")) + cached, cached, generated, reasoning)
    if elapsed_ms and generated >= TURN_RATE_MIN_TOKENS:
        stats.turn_rates.append(generated / (elapsed_ms / 1000))


def _codex_stats(events: list[dict[str, object]]) -> RunStats:
    stats = RunStats()
    seen: set[str] = set()
    for event in events:
        if event.get("type") == "turn.completed":
            usage = _mapping(event.get("usage"))
            stats.model_turns += 1
            _note_tokens(stats, _count(usage.get("input_tokens")), _count(usage.get("cached_input_tokens")),
                         _count(usage.get("output_tokens")), _count(usage.get("reasoning_output_tokens")))
        if event.get("type") == "item.completed":
            _codex_item(stats, seen, _mapping(event.get("item")))
    return stats


def _codex_item(stats: RunStats, seen: set[str], item: Mapping[str, object]) -> None:
    kind = item.get("type")
    if kind == "command_execution":
        _note_tool(stats, seen, "shell", item.get("command"), failed=item.get("status") == "failed",
                   exit_code=item.get("exit_code"))
    elif kind == "file_change":
        _note_tool(stats, seen, "apply_patch", item.get("changes"), failed=item.get("status") == "failed")
    elif kind in ("mcp_tool_call", "web_search"):
        _note_tool(stats, seen, str(kind), {key: value for key, value in item.items() if key != "id"},
                   failed=item.get("status") == "failed")


def _claude_stats(events: list[dict[str, object]]) -> RunStats:
    stats = RunStats()
    seen: set[str] = set()
    failed = {str(block.get("tool_use_id")) for event in events if event.get("type") == "user"
              for block in _claude_blocks(event) if block.get("type") == "tool_result" and block.get("is_error")}
    usage_by_call: dict[str, Mapping[str, object]] = {}
    for index, event in enumerate(events):
        if event.get("type") != "assistant":
            continue
        message = _mapping(event.get("message"))
        usage = _mapping(message.get("usage"))
        if usage:
            # One model call streams one event per block, all with its id (#53).
            usage_by_call[str(message.get("id") or index)] = usage
        for block in _claude_blocks(event):
            if block.get("type") == "tool_use":
                error = str(block.get("id")) in failed
                # Claude marks a failed shell command only as an errored tool result.
                _note_tool(stats, seen, str(block.get("name") or ""), block.get("input"), failed=error,
                           exit_code=1 if error else 0)
    stats.model_turns = len(usage_by_call)
    # Stream usage holds only early output counts; the result has the totals, so a stopped run is a lower bound.
    results = [event for event in events if event.get("type") == "result" and _mapping(event.get("usage"))]
    for usage in [_mapping(results[-1].get("usage"))] if results else usage_by_call.values():
        _note_claude_usage(stats, usage)
    stats.largest_turn_tokens = None
    return stats


def _note_claude_usage(stats: RunStats, usage: Mapping[str, object]) -> None:
    read = _count(usage.get("cache_read_input_tokens"))
    total = _count(usage.get("input_tokens")) + _count(usage.get("cache_creation_input_tokens")) + read
    thinking = _count(_mapping(usage.get("output_tokens_details")).get("thinking_tokens"))
    _note_tokens(stats, total, read, _count(usage.get("output_tokens")), thinking)


def _claude_blocks(event: Mapping[str, object]) -> list[Mapping[str, object]]:
    content = _mapping(event.get("message")).get("content")
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def _agy_stats(events: list[dict[str, object]]) -> RunStats:
    stats = RunStats(tool_s=0.0)
    seen: set[str] = set()
    for event in events:
        step = _mapping(event.get("step_update"))
        # A step streams while ACTIVE and reports its usage and result when it ends.
        if step.get("state") == "ACTIVE":
            continue
        if step.get("step_type") == "agent_response":
            _agy_turn(stats, step)
        elif step.get("step_type") == "tool":
            info = _mapping(step.get("tool_info"))
            stats.tool_s += step["duration_seconds"] if type(step.get("duration_seconds")) is float else 0.0
            _note_tool(stats, seen, str(step.get("tool_name") or ""), info.get("parameters"),
                       failed=step.get("state") != "DONE", exit_code=agy_tool_result(info)[0])
    return stats


def _agy_turn(stats: RunStats, step: Mapping[str, object]) -> None:
    usage = _mapping(step.get("usage"))
    stats.model_turns += 1
    cached = _count(usage.get("cache_read_tokens"))
    generated = _count(usage.get("output_tokens"))
    _note_tokens(stats, _count(usage.get("input_tokens")) + cached, cached, generated, _count(usage.get("thinking_tokens")))
    seconds = step.get("duration_seconds")
    if type(seconds) is float and seconds > 0 and generated >= TURN_RATE_MIN_TOKENS:
        stats.turn_rates.append(generated / seconds)


def stream_stats(stdout: str) -> RunStats:
    """Statistics of one step's stream; a stream from an unknown harness gives empty ones."""
    events = split_jsonl(stdout)
    kinds = {event.get("type") for event in events}
    if any(event.get("event") == "step_update" for event in events):
        return _agy_stats(events)
    if kinds & {"step_start", "step_finish", "tool_use"}:
        return _opencode_stats(events)
    if kinds & {"turn.started", "turn.completed", "item.completed"}:
        return _codex_stats(events)
    if kinds & {"assistant", "user"}:
        return _claude_stats(events)
    return RunStats()
