"""Key actions of a run, found in the raw tool events: where a run went right or wrong (#98).

Diagnosis only. They never change a grade and the judge never sees them: scoring them would reward one route
over another, and the briefs leave the route open on purpose.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from mengine_bench.core import Checkpoint
from mengine_bench.runner.trace import fetch_actions, tool_trace


def reached_checkpoints(declared: Sequence[Checkpoint], streams: Sequence[str]) -> list[dict[str, object]]:
    """Each checkpoint with the number of the tool call that first reached it, or None."""
    calls = tool_trace(streams)
    actions = fetch_actions(calls)
    events = [str((call.name, call.inputs)) for call in calls]
    rows: list[dict[str, object]] = []
    for mark in declared:
        pattern = re.compile(mark.pattern, re.IGNORECASE | re.DOTALL)
        candidates = [" ".join(urls) for urls in actions] if mark.fetch_only else events
        call = next((index for index, event in enumerate(candidates, start=1) if pattern.search(event)), None)
        rows.append({"name": mark.name, "call": call})
    return rows
