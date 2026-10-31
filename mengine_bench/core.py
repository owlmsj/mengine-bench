"""Task contract: a task = fixture + prompts + deterministic gold.

Every task ships a reference solution so the self-tests prove, without any
model, that the gold passes a correct answer and fails an untouched workspace.
Gold is executed tests, exact numbers, file state or regex; the maintainer's
LLM judge only feeds the separate Judge grade (docs/SCORING.md).
"""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

@dataclass(frozen=True)
class Step:
    """One user turn.

    `fresh_session` starts a new agent process without the chat history, in
    a new workspace that holds only the `carry` files from the previous one.
    `hide` moves workspace paths out of reach before the turn, so the agent
    must rely on what it kept in context. Every step after the first is a
    fresh session (#23: no task resumes one, so adapters have no resume).
    `attach` passes workspace files as attachments (images for vision tasks);
    `inline` pastes their text into the prompt.
    """

    prompt: str
    fresh_session: bool = False
    hide: tuple[str, ...] = ()
    attach: tuple[str, ...] = ()
    inline: tuple[str, ...] = ()
    carry: tuple[str, ...] = ()


@dataclass
class CheckResult:
    checks: list[tuple[str, bool]] = field(default_factory=list)
    # Gates: any failure here means not solved and score 0 (#23: no partial
    # credit for checks that pass because the gate's work was skipped).
    mandatory: list[tuple[str, bool]] = field(default_factory=list)
    # Gates a run stopped at its limit may still miss: a page cut short earns what it holds (#41).
    # A gate that guards the tests is never here, so tampering earns nothing.
    waived_at_limit: tuple[str, ...] = ()

    def add(self, name: str, ok: bool) -> None:
        self.checks.append((name, bool(ok)))

    @property
    def mandatory_ok(self) -> bool:
        return all(ok for _, ok in self.mandatory)

    @property
    def passed(self) -> bool:
        return self.mandatory_ok and bool(self.checks) and all(ok for _, ok in self.checks)

    @property
    def score(self) -> float:
        """Correctness 0..1: the share of scored checks passed, 0 on a failed gate."""
        if not self.checks or not self.mandatory_ok:
            return 0.0
        return sum(ok for _, ok in self.checks) / len(self.checks)

    @property
    def partial_score(self) -> float:
        """Correctness of a run stopped at its limit: the same share, without the waived gates."""
        if not self.checks or not all(ok or name in self.waived_at_limit for name, ok in self.mandatory):
            return 0.0
        return sum(ok for _, ok in self.checks) / len(self.checks)

    def failed(self) -> list[str]:
        return [name for name, ok in [*self.mandatory, *self.checks] if not ok]


Setup = Callable[[Path], None]
Check = Callable[[Path, Sequence[str]], CheckResult]
Reference = Callable[[Path], list[str]]


@dataclass(frozen=True)
class EvalTask:
    id: str
    category: str
    provenance: str
    summary: str
    setup: Setup
    steps: tuple[Step, ...]
    check: Check
    reference: Reference
    needs: frozenset[str] = frozenset()
    timeout_s: int = 120
    # Workspace files stored verbatim in the bundle for the maintainer's judge
    # (visual tasks: the page it renders).
    deliverables: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.steps:
            raise ValueError(f"task {self.id!r} received no steps; expected at least one Step")
        resumed = [index for index, step in enumerate(self.steps) if index and not step.fresh_session]
        if resumed:
            raise ValueError(f"task {self.id!r} received steps {resumed} that continue a session; "
                             f"expected fresh_session=True on every step after the first")
        bad = [rel for rel in self.deliverables if not rel or rel.startswith(("/", "\\")) or ".." in rel.split("/")]
        if bad:
            raise ValueError(f"task {self.id!r} received deliverables {bad}; expected workspace-relative paths")

    @property
    def render_target(self) -> str | None:
        """The HTML deliverable the maintainer's judge renders (visual tasks), or None."""
        return next((rel for rel in self.deliverables if rel.endswith(".html")), None)


# --------------------------------------------------------------- helpers ----


def write(ws: Path, rel: str, text: str) -> Path:
    path = ws / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def read(ws: Path, rel: str) -> str | None:
    path = ws / rel
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8-sig", errors="replace")


def read_json(ws: Path, rel: str) -> object | None:
    text = read(ws, rel)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def close(value: object, expected: float, tol: float = 1e-2) -> bool:
    """Numeric match that tolerates rounding but not a different number."""
    try:
        number = float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and abs(number - expected) <= tol


def has(text: str | None, pattern: str) -> bool:
    return bool(text) and re.search(pattern, text or "", re.IGNORECASE | re.DOTALL) is not None


def run_hidden_tests(ws: Path, test_source: str, timeout_s: int = 60) -> tuple[bool, str]:
    """Run gold unittest code the agent never saw, importing modules from ws."""
    with tempfile.TemporaryDirectory(prefix="bench-hidden-", dir=scratch_root()) as tmp:
        test_file = Path(tmp) / "test_hidden_gold.py"
        test_file.write_text(test_source, encoding="utf-8")
        env = {"PYTHONPATH": str(ws), "PYTHONDONTWRITEBYTECODE": "1"}
        # Windows needs SYSTEMROOT for sockets/random even in a minimal env.
        if "SYSTEMROOT" in os.environ:
            env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "unittest", "-q", test_file.name],
                cwd=tmp,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, f"hidden tests exceeded {timeout_s}s"
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
    return proc.returncode == 0, " | ".join(tail)


def answer_json(answers: Sequence[str], index: int = -1) -> dict[str, object]:
    """Last JSON object in an answer text (models wrap it in prose or fences)."""
    if not answers:
        return {}
    text = answers[index] or ""
    decoder = json.JSONDecoder()
    found: dict[str, object] = {}
    start = text.find("{")
    while start >= 0:
        try:
            value, end = decoder.raw_decode(text, start)
        except json.JSONDecodeError:
            start = text.find("{", start + 1)
            continue
        if isinstance(value, dict):
            found = value
        # Skip the whole object so its nested braces never replace it.
        start = text.find("{", end)
    return found


def scratch_root() -> Path:
    """Parent dir for gold temp dirs; callers own unique TemporaryDirectories.

    MENGINE_BENCH_SCRATCH overrides it (e.g. a fast or excluded-from-AV disk).
    """
    override = os.environ.get("MENGINE_BENCH_SCRATCH")
    root = Path(override) if override else Path(tempfile.gettempdir()) / "mengine-bench"
    root.mkdir(parents=True, exist_ok=True)
    return root
