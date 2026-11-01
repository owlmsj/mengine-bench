"""`mengine-bench judge-anchors`: does the judge still tell finished work from nothing? (#82)

Run it after a rubric or judge model change. Two tasks are voted twice, on their reference solution and on the
untouched workspace, and the gap must hold. Four votes, no agent run, and nothing is written to any bundle.
"""

from __future__ import annotations

import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from mengine_bench import catalog
from mengine_bench.core import EvalTask
from mengine_bench.judge import JudgeContext, TaskVerdict, workspace_diff
from mengine_bench.runner.task_run import snapshot

# One task with code and one with data, neither needing a browser.
ANCHOR_TASKS = ("gd-astar-doors", "bo-reconcile")
# A reference has no tool log, so it earns little on self-verification. Measured on rubric 2.4: references 55 and 53,
# untouched workspaces 0 and 0.
MIN_GAP = 30


class Voter(Protocol):
    def grade(self, context: JudgeContext, workdir: Path) -> TaskVerdict: ...


@dataclass(frozen=True)
class AnchorRow:
    task_id: str
    reference: int | None
    untouched: int | None

    @property
    def gap(self) -> int | None:
        return None if self.reference is None or self.untouched is None else self.reference - self.untouched


@dataclass(frozen=True)
class AnchorReport:
    rows: Sequence[AnchorRow]

    @property
    def ok(self) -> bool:
        return all(row.gap is not None and row.gap >= MIN_GAP for row in self.rows)


def _context(task: EvalTask, ws: Path, solved: bool) -> JudgeContext:
    ws.mkdir(parents=True)
    task.setup(ws)
    before = snapshot(ws)
    answers = task.reference(ws) if solved else [""] * len(task.steps)
    check = task.check(ws, answers)
    return JudgeContext(task_id=task.id, prompts=tuple(step.prompt for step in task.steps), answers=tuple(answers),
                        diff=workspace_diff(before, snapshot(ws)), transcript_tail="",
                        checks=(*check.mandatory, *check.checks))


def vote_anchors(judge: Voter, root: Path) -> AnchorReport:
    rows = []
    for task_id in ANCHOR_TASKS:
        task = next(item for item in catalog.all_tasks() if item.id == task_id)
        reference = judge.grade(_context(task, root / task_id / "reference", True), root / task_id / "judge-reference")
        untouched = judge.grade(_context(task, root / task_id / "untouched", False), root / task_id / "judge-untouched")
        rows.append(AnchorRow(task_id, reference.score, untouched.score))
    return AnchorReport(rows)


def run_anchors(judge: Voter) -> AnchorReport:
    with tempfile.TemporaryDirectory(prefix="mengine-bench-anchors-") as tmp:
        return vote_anchors(judge, Path(tmp))
