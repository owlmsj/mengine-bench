"""Compare owner audit scores with fresh official votes, without rewriting bundles (#185)."""

from __future__ import annotations

import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from mengine_bench.bundle_judge import read_packet, vote_packet
from mengine_bench.judge import RUBRIC_VERSION, RubricJudge

_EXPORT = re.compile(r"^([\w-]+): (.+)=(\d+) ([^=]+)=(\d+) \(auditor: .+; judge [^/]+/[^)]+\)$")


@dataclass(frozen=True)
class OwnerVote:
    task_id: str
    pick: str
    a: int
    b: int


def _pick(prefix: str, label_b: str) -> str:
    # build.py takes arbitrary labels from the audit config. An A pick repeats its label (#165).
    words = prefix.split(" ")
    half = len(words) // 2
    if len(words) % 2 == 0 and words[:half] == words[half:]:
        return " ".join(words[:half])
    for pick in (label_b, "empate", "-", "A", "B"):
        if prefix.startswith(f"{pick} "):
            return pick
    raise ValueError(f"received vote prefix {prefix!r}; expected a pick followed by its A label")


def parse_votes(text: str) -> list[OwnerVote]:
    """Read the bench-audit copy button's two scores, ordered A then B, with free text labels."""
    votes: list[OwnerVote] = []
    seen: set[str] = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        match = _EXPORT.fullmatch(line.strip())
        if match is None:
            raise ValueError(f"received vote {line!r}; expected '<task>: <pick> <labelA>=<0..100> "
                             "<labelB>=<0..100> (auditor: ...; judge a/b)'")
        task_id, prefix, score_a, label_b, score_b = match.groups()
        a, b = int(score_a), int(score_b)
        if task_id in seen or not (0 <= a <= 100 and 0 <= b <= 100):
            raise ValueError(f"received vote {line!r}; expected unique tasks and two integer scores in 0..100")
        votes.append(OwnerVote(task_id, _pick(prefix, label_b), a, b))
        seen.add(task_id)
    if not votes:
        raise ValueError(f"received votes {text!r}; expected at least one audit vote with both scores")
    return votes


def calibrate(votes: list[OwnerVote], bundles: tuple[Path, Path], judge: RubricJudge) -> tuple[str, int]:
    """Pre-read every packet, then vote in scratch; only the caller may save the report."""
    packets = {(vote.task_id, side): read_packet(bundle, vote.task_id)
               for vote in votes for side, bundle in enumerate(bundles)}
    rows = ["# Judge calibration", "", f"Bundles: A={bundles[0].name}; B={bundles[1].name}", "",
            "| task | owner pick | bundle | owner vote | new vote | abs diff |",
            "| --- | --- | --- | --- | --- | --- |"]
    diffs: list[int] = []
    scratch = Path("tmp")
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="judge-calibrate-", dir=scratch) as tmp:
        for vote in votes:
            for side, bundle in enumerate(bundles):
                verdict = vote_packet(bundle, vote.task_id, packets[vote.task_id, side], judge,
                                      Path(tmp) / str(side) / vote.task_id)
                if verdict.score is None:
                    raise ValueError(f"received no vote for {vote.task_id} in {bundle.name}: {verdict.errors}; "
                                     "expected a judge vote for each owner score")
                owner = (vote.a, vote.b)[side]
                diff = abs(verdict.score - owner)
                diffs.append(diff)
                rows.append(f"| {vote.task_id} | {vote.pick} | {'AB'[side]} | {owner} | {verdict.score} | {diff} |")
    beyond = sum(diff > 8 for diff in diffs)
    rows.extend(["", f"Mean |diff|: {mean(diffs):.1f}", f"Beyond 8: {beyond}", f"Rubric: {RUBRIC_VERSION}"])
    return "\n".join(rows) + "\n", beyond
