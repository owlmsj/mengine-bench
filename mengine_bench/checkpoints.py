"""Key actions of a run, found in the raw tool events: where a run went right or wrong (#98).

Diagnosis only. They never change a grade and the judge never sees them: scoring them would reward one route
over another, and the briefs leave the route open on purpose.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from mengine_bench.core import Checkpoint

# One event per call: "item.started" would count a Codex command twice, and an active AGY step is not done yet.
_TOOL_EVENT = re.compile(r'"tool_use"|"item\.completed".*"(command_execution|file_change|mcp_tool_call)"|"step_update"')
_NOT_DONE = re.compile(r'"state"\s*:\s*"ACTIVE"')


def _tool_events(streams: Sequence[str]) -> list[str]:
    lines = [line for stream in streams for line in stream.split("\n")]
    return [line for line in lines if _TOOL_EVENT.search(line) and not _NOT_DONE.search(line)]


def reached_checkpoints(declared: Sequence[Checkpoint], streams: Sequence[str]) -> list[dict[str, object]]:
    """Each checkpoint with the number of the tool call that first reached it, or None."""
    events = _tool_events(streams)
    rows: list[dict[str, object]] = []
    for mark in declared:
        pattern = re.compile(mark.pattern, re.IGNORECASE | re.DOTALL)
        call = next((index for index, event in enumerate(events, start=1) if pattern.search(event)), None)
        rows.append({"name": mark.name, "call": call})
    return rows
