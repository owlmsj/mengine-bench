"""`mengine-bench verify`: audit a result bundle with the bench code at hand.

Re-derived (PASS/FAIL): manifest hashes, JSON schema, size cap, every task's
deterministic checks re-run on its saved workspace, all scores recomputed with
scoring.py, and a secret scan. Not re-derivable without models (marked
SELF-REPORTED when internally consistent, FAIL otherwise): timings, judge
votes and vision checklist ballots. See docs/SUBMITTING.md.
"""

from __future__ import annotations

import json
import re
import statistics
import tarfile
import tempfile
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import lru_cache
from importlib import resources
from pathlib import Path, PurePosixPath

import jsonschema

from mengine_bench import __version__, catalog, visual
from mengine_bench.bundle import (
    BUNDLE_SIZE_CAP, MANIFEST_NAME, RESULT_NAME, SUMMARY_NAME, WORKSPACE_FILE_CAP, manifest_lines, without_graded,
)
from mengine_bench.core import CheckResult, EvalTask, scratch_root
from mengine_bench.redact import LocalNames, find_path_leaks, find_secrets, local_names
from mengine_bench.scoring import TaskOutcome, score_suite
from mengine_bench.unpack_budget import UnpackBudget, iter_tar_bounded, read_gzip_bounded

PASS, FAIL, SELF_REPORTED, SKIP = "PASS", "FAIL", "SELF-REPORTED", "SKIP"
# Verified but not ranked: the task set is not exactly the declared suite (R04).
PARTIAL = "PARTIAL"
TOLERANCE = 0.05
# Windows reads these as rooted or as stream names even though POSIX does not (R06).
_UNSAFE_MEMBER_NAME = re.compile(r"[\\:]")
VISION_PREFIX = "vision: "
# Visual checks that need a browser or a judge; verify re-grades without both.
_SELF_REPORTED_CHECKS = (visual.SCREENSHOT_CHECK, visual.PROFILE_CHECK)

Task = dict[str, object]


@dataclass(frozen=True)
class VerifyItem:
    name: str
    status: str
    detail: str = ""


@dataclass
class VerifyReport:
    bundle: Path
    items: list[VerifyItem] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(item.status != FAIL for item in self.items)

    @property
    def partial(self) -> bool:
        return any(item.status == PARTIAL for item in self.items)

    def add(self, name: str, problems: Sequence[str], passed: str = "", status: str = PASS) -> None:
        if problems:
            self.items.append(VerifyItem(name, FAIL, "; ".join(problems)))
            return
        self.items.append(VerifyItem(name, status, passed))

    def render(self) -> str:
        lines = [f"{item.status} {item.name}" + (f": {item.detail}" if item.detail else "") for item in self.items]
        failed = sum(item.status == FAIL for item in self.items)
        verdict = f"VERIFIED {self.bundle.name}" + (" (partial: not ranked)" if self.partial else "")
        lines.append(verdict if self.ok else f"FAILED {self.bundle.name}: {failed} item(s)")
        return "\n".join(lines) + "\n"


@lru_cache(maxsize=1)
def _schema_text() -> str:
    return resources.files("mengine_bench").joinpath("schemas/result.schema.json").read_text(encoding="utf-8")


def load_schema() -> dict[str, object]:
    return json.loads(_schema_text())


def _manifest_problems(bundle: Path) -> list[str]:
    path = bundle / MANIFEST_NAME
    if not path.is_file():
        return [f"received no {MANIFEST_NAME}; expected one listing every other file"]
    recorded = sorted(line for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    actual = manifest_lines(bundle)
    recorded_set, actual_set = set(recorded), set(actual)
    problems = [f"mismatch or missing: {line.split('  ', 1)[-1]}" for line in sorted(recorded_set - actual_set)]
    problems += [f"unlisted or changed: {line.split('  ', 1)[-1]}" for line in sorted(actual_set - recorded_set)]
    return problems


def _size_problems(bundle: Path) -> tuple[list[str], int]:
    total = sum(path.stat().st_size for path in bundle.rglob("*") if path.is_file())
    if total > BUNDLE_SIZE_CAP:
        return [f"received {total} bytes; expected at most {BUNDLE_SIZE_CAP}"], total
    return [], total


def _schema_problems(result: object) -> list[str]:
    validator = jsonschema.Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(result), key=lambda error: list(error.absolute_path))
    return [f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message[:160]}" for error in errors[:5]]


def _safe_member_name(member: tarfile.TarInfo) -> PurePosixPath:
    name = PurePosixPath(member.name)
    unsafe = (_UNSAFE_MEMBER_NAME.search(member.name) or name.is_absolute() or ".." in name.parts
              or not (member.isfile() or member.isdir()))
    if unsafe:
        raise ValueError(f"received archive member {member.name!r} (type {member.type!r}); "
                         "expected a relative regular file")
    return name


def _archive_members(archive: Path, budget: UnpackBudget | None = None) -> Iterator[tuple[PurePosixPath, bytes]]:
    """Regular files only, relative paths, bounded sizes: bundles come from strangers."""
    with archive.open("rb") as source:
        for member, body in iter_tar_bounded(source, budget or UnpackBudget(), archive.name):
            name = _safe_member_name(member)
            if body is None:
                continue
            if member.size > WORKSPACE_FILE_CAP:
                raise ValueError(f"received member {member.name!r} of {member.size} bytes; "
                                 f"expected <= {WORKSPACE_FILE_CAP}")
            yield name, body


def _safe_extract(archive: Path, target: Path) -> None:
    root = target.resolve()
    for name, body in _archive_members(archive):
        dest = target.joinpath(*name.parts)
        # Containment proof on top of the name rules: a resolved path outside root is never written.
        if not dest.resolve().is_relative_to(root):
            raise ValueError(f"received archive member {str(name)!r} resolving outside the workspace; "
                             "expected a relative regular file")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)


def _read_gzip(path: Path, budget: UnpackBudget | None = None) -> bytes:
    with path.open("rb") as source:
        return read_gzip_bounded(source, budget or UnpackBudget(), path.name)


def _unpack_problems(bundle: Path) -> list[str]:
    """One budget for every archive and transcript in the bundle; first violation ends the walk (R09)."""
    budget = UnpackBudget()
    try:
        for path in sorted(bundle.rglob("*")):
            if path.name.endswith(".tar.gz") and path.is_file():
                for _ in _archive_members(path, budget):
                    pass
            elif path.name.endswith(".gz") and path.is_file():
                _read_gzip(path, budget)
    except (OSError, EOFError, ValueError, tarfile.TarError) as error:
        return [f"{path.relative_to(bundle).as_posix()}: {error}"]
    return []


@contextmanager
def _offline_visual() -> Iterator[None]:
    # Without a browser, visual.grade mirrors the deterministic gates as
    # checks; vision items and the screenshot gate are compared elsewhere.
    previous_render, previous_judge = visual.RENDER, visual.JUDGE
    visual.RENDER = lambda html, png: visual.NO_BROWSER
    visual.JUDGE = visual.unavailable_judge
    try:
        yield
    finally:
        visual.RENDER, visual.JUDGE = previous_render, previous_judge


def _rederivable(name: str) -> bool:
    return not name.startswith(VISION_PREFIX) and name not in _SELF_REPORTED_CHECKS


def _recorded_checks(task: Task) -> list[dict[str, object]]:
    checks = task.get("checks")
    return checks if isinstance(checks, list) else []


def regrade(task: EvalTask, recorded: Task, bundle: Path) -> CheckResult | None:
    workspace = recorded.get("workspace")
    if not isinstance(workspace, dict):
        return None
    answers = [str(answer) for answer in recorded.get("answers") or []]
    answers += [""] * (len(task.steps) - len(answers))
    with tempfile.TemporaryDirectory(prefix="verify-", dir=scratch_root()) as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        _safe_extract(bundle / str(workspace["archive"]), ws)
        with _offline_visual():
            return task.check(ws, answers)


CheckRow = tuple[str, bool, bool]


def _evidence_problems(recorded: Task, bundle: Path) -> list[str]:
    """A graded task (status ok) must ship its checks and workspace, else nothing can be re-derived (R02)."""
    if recorded.get("status") != "ok":
        return []
    problems = []
    if not _recorded_checks(recorded):
        problems.append("received a scored task with no checks; expected its recorded check list")
    workspace = recorded.get("workspace")
    archive = workspace.get("archive") if isinstance(workspace, dict) else None
    expected = f"workspaces/{recorded.get('id')}.tar.gz"
    if archive != expected or not (bundle / expected).is_file():
        problems.append(f"received workspace archive {archive!r}; expected {expected} present in the bundle")
    return problems


def _recorded_rows(recorded: Task) -> list[CheckRow]:
    return [(str(c["name"]), bool(c["ok"]), bool(c["mandatory"])) for c in _recorded_checks(recorded)]


def _fresh_rows(fresh: CheckResult, recorded: Task) -> list[CheckRow]:
    rows = [(name, ok, True) for name, ok in fresh.mandatory] + [(name, ok, False) for name, ok in fresh.checks]
    recorded_flags = recorded.get("flags") or []
    assert isinstance(recorded_flags, list)
    # Offline re-grading mirrors the visual gates as scored checks; a rendered
    # run scored vision items there instead, so the mirror is not comparable.
    offline_mirror = isinstance(fresh, visual.VisualCheckResult) and visual.NO_BROWSER in fresh.flags
    if offline_mirror and visual.PROFILE_UNRENDERED not in recorded_flags:
        rows = rows[:len(fresh.mandatory)]
    return [row for row in rows if _rederivable(row[0])]


def _row_problems(got: list[CheckRow], recorded: Task) -> list[str]:
    """Exact ordered (name, ok, mandatory) list, so duplicated or reordered checks cannot inflate a score (R05)."""
    rows = _recorded_rows(recorded)
    # Same name in both roles is legit: offline visual grading mirrors gates as scored checks.
    roles = [(name, mandatory) for name, _ok, mandatory in rows]
    dupes = sorted({role[0] for role in roles if roles.count(role) > 1})
    problems = [f"received duplicated check {name!r}; expected each check once" for name in dupes]
    want = [row for row in rows if _rederivable(row[0])]
    if got == want:
        return problems
    index = next((i for i, (g, w) in enumerate(zip(got, want)) if g != w), min(len(got), len(want)))
    shown_got = got[index] if index < len(got) else None
    shown_want = want[index] if index < len(want) else None
    mismatch = (f"check #{index}: re-graded {shown_got}, recorded {shown_want} "
                f"({len(got)} re-graded, {len(want)} recorded; expected the same ordered list)")
    return [*problems, mismatch]


def _check_problems(task: EvalTask | None, recorded: Task, bundle: Path) -> list[str]:
    if task is None:
        return [f"received unknown task id {recorded.get('id')!r}; expected one from this bench's catalog"]
    problems = []
    if recorded.get("weight") != task.weight or recorded.get("par_s") != task.par_s:
        problems.append(f"received weight/par_s {recorded.get('weight')}/{recorded.get('par_s')}; "
                        f"expected {task.weight}/{task.par_s:g}")
    evidence = _evidence_problems(recorded, bundle)
    problems += evidence
    try:
        fresh = regrade(task, recorded, bundle)
    except (ValueError, RuntimeError, OSError, tarfile.TarError) as error:
        return [*problems, f"re-grading failed: {error}", *_consistency_problems(recorded)]
    if fresh is None and _recorded_checks(recorded) and not evidence:
        problems.append("no saved workspace; expected one to re-grade")
    if fresh is not None:
        problems += _row_problems(_fresh_rows(fresh, recorded), recorded)
        if recorded.get("pass_ratio") != fresh.pass_ratio:
            problems.append(f"received pass_ratio {recorded.get('pass_ratio')}; expected {fresh.pass_ratio}")
    # Always: a task with no evidence must still not claim credit its checks do not give.
    return problems + _consistency_problems(recorded)


def suite_membership(suite: str, ids: Sequence[str]) -> tuple[list[str], bool]:
    """(problems, partial): duplicates FAIL; any other set than the declared suite's is partial (R04)."""
    dupes = sorted({task_id for task_id in ids if ids.count(task_id) > 1})
    if dupes:
        return [f"received duplicated task ids {dupes}; expected each task once"], False
    expected = {task.id for task in catalog.tasks(suite)}
    return [], set(ids) != expected


def _consistency_problems(recorded: Task) -> list[str]:
    """check_score, mandatory_ok and passed must follow from the recorded checks."""
    checks = _recorded_checks(recorded)
    scored = [bool(c["ok"]) for c in checks if not c["mandatory"]]
    mandatory_ok = all(bool(c["ok"]) for c in checks if c["mandatory"])
    score = sum(scored) / len(scored) if scored else 0.0
    ratio = float(recorded.get("pass_ratio") or 1.0)  # type: ignore[arg-type]
    passed = mandatory_ok and bool(scored) and score >= ratio - 1e-9
    problems = []
    if abs(float(recorded.get("check_score") or 0.0) - score) > 1e-9:  # type: ignore[arg-type]
        problems.append(f"received check_score {recorded.get('check_score')}; checks give {score}")
    if recorded.get("mandatory_ok") is not mandatory_ok or recorded.get("passed") is not passed:
        problems.append(f"received mandatory_ok/passed {recorded.get('mandatory_ok')}/{recorded.get('passed')}; "
                        f"checks give {mandatory_ok}/{passed}")
    return problems


def _vision_problems(recorded: Task) -> list[str]:
    vision = recorded.get("vision")
    voted = {str(c["name"])[len(VISION_PREFIX):]: bool(c["ok"]) for c in _recorded_checks(recorded)
             if str(c["name"]).startswith(VISION_PREFIX)}
    if not isinstance(vision, dict):
        return ["vision checks recorded without ballots"] if voted else []
    checklist, ballots, votes = vision["checklist"], vision["ballots"], int(vision["votes"])
    assert isinstance(checklist, list) and isinstance(ballots, list)
    if len(ballots) > votes or any(len(ballot) != len(checklist) for ballot in ballots):
        return [f"received {len(ballots)} ballots of sizes {[len(b) for b in ballots]}; "
                f"expected at most {votes} of size {len(checklist)}"]
    # Same rule as judge.VisionChecklistJudge: majority of configured votes.
    needed = votes // 2 + 1
    problems = []
    for index, item in enumerate(checklist):
        majority = sum(bool(ballot[index]) for ballot in ballots) >= needed
        if voted.get(str(item)) is not majority:
            problems.append(f"item {item!r}: ballots give {majority}, recorded {voted.get(str(item))}")
    return problems


def _timing_problems(recorded: Task) -> list[str]:
    steps = recorded.get("steps")
    assert isinstance(steps, list)
    agent_s = recorded.get("agent_s")
    if not steps:
        return [] if agent_s is None else [f"received agent_s {agent_s} without steps; expected null"]
    total = sum(float(step["wall_s"]) for step in steps)
    if agent_s is None or abs(float(agent_s) - total) > TOLERANCE:  # type: ignore[arg-type]
        return [f"received agent_s {agent_s}; steps sum to {total:.2f}"]
    return []


def _judge_problems(result: dict[str, object]) -> list[str]:
    judge = result.get("judge")
    configured = int(judge["votes"]) if isinstance(judge, dict) else 0
    problems = []
    for task in result["tasks"]:  # type: ignore[union-attr]
        votes, rationales = task["judge_votes"], task["judge_rationales"]
        if len(votes) > configured or len(rationales) != len(votes):
            problems.append(f"{task['id']}: {len(votes)} votes, {len(rationales)} rationales, "
                            f"{configured} configured; expected votes <= configured and one rationale each")
        median = float(statistics.median(votes)) if votes else None
        if task["subjective"] != median:
            problems.append(f"{task['id']}: received subjective {task['subjective']}; median of votes is {median}")
    return problems


def _outcome(task: Task) -> TaskOutcome:
    return TaskOutcome(
        task_id=str(task["id"]), category=str(task["category"]), weight=int(task["weight"]),  # type: ignore[arg-type]
        par_s=float(task["par_s"]), check_score=float(task["check_score"]),  # type: ignore[arg-type]
        mandatory_ok=bool(task["mandatory_ok"]), passed=bool(task["passed"]),
        agent_s=None if task["agent_s"] is None else float(task["agent_s"]),  # type: ignore[arg-type]
        status=str(task["status"]), judge_votes=tuple(int(v) for v in task["judge_votes"]),  # type: ignore[union-attr]
    )


def _close(got: object, want: float | None, tolerance: float = TOLERANCE) -> bool:
    if want is None or got is None:
        return got is None and want is None
    return abs(float(got) - want) <= tolerance  # type: ignore[arg-type]


def _score_problems(result: dict[str, object]) -> list[str]:
    tasks = result["tasks"]
    totals = result["totals"]
    assert isinstance(tasks, list) and isinstance(totals, dict)
    judge = result.get("judge")
    label = str(judge["label"]) if isinstance(judge, dict) else None
    try:
        suite = score_suite(str(result["suite"]), [_outcome(task) for task in tasks], judge=label)
    except ValueError as error:
        return [f"recomputation failed: {error}"]
    problems = []
    expected = {"objective": suite.objective, "accuracy": suite.accuracy, "subjective": suite.subjective,
                "composite": suite.composite, "total_agent_s": suite.total_agent_s}
    for key, want in expected.items():
        if not _close(totals.get(key), want):
            problems.append(f"received {key} {totals.get(key)}; recomputed {want}")
    for key, want in (("solved", suite.solved), ("total", suite.total)):
        if totals.get(key) != want:
            problems.append(f"received {key} {totals.get(key)}; recomputed {want}")
    for task, score in zip(tasks, suite.tasks):
        for key, want in (("c", score.correctness), ("s", score.speed), ("o", score.objective)):
            if not _close(task[key], want, 0.01 if key != "o" else TOLERANCE):
                problems.append(f"{task['id']}: received {key} {task[key]}; recomputed {want:.3f}")
    return problems


def _texts(bundle: Path) -> Iterator[tuple[str, str]]:
    for path in sorted(bundle.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(bundle).as_posix()
        if rel.endswith(".jsonl.gz"):
            yield rel, _read_gzip(path).decode("utf-8", errors="replace")
        elif rel.endswith(".tar.gz"):
            for name, body in _archive_members(path):
                yield f"{rel}:{name}", body.decode("utf-8", errors="replace")
        else:
            yield rel, path.read_text(encoding="utf-8", errors="replace")


def _secret_problems(bundle: Path) -> list[str]:
    try:
        return [f"{rel}: unredacted {', '.join(kinds)}" for rel, text in _texts(bundle)
                if (kinds := find_secrets(text))]
    except (OSError, EOFError, ValueError, tarfile.TarError) as error:
        return [f"could not scan: {error}"]


def _published_texts(bundle: Path) -> Iterator[tuple[str, str, str]]:
    """(file, text scanned for home paths, text scanned for local names); workspaces stay byte-exact."""
    for path in sorted((bundle / "transcripts").glob("*.jsonl.gz")):
        text = _read_gzip(path).decode("utf-8", errors="replace")
        yield path.relative_to(bundle).as_posix(), text, text
    summary = bundle / SUMMARY_NAME
    if summary.is_file():
        text = summary.read_text(encoding="utf-8", errors="replace")
        yield SUMMARY_NAME, text, text
    result = bundle / RESULT_NAME
    if result.is_file():
        text = result.read_text(encoding="utf-8", errors="replace")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            yield RESULT_NAME, text, text
            return
        # Graded fields keep task words verbatim (bundle.GRADED_KEYS).
        yield RESULT_NAME, text, json.dumps(without_graded(data) if isinstance(data, dict) else data)


def _path_problems(bundle: Path, names: LocalNames) -> list[str]:
    # Counts only: echoing the match would print the very name being hidden.
    try:
        problems = []
        for rel, text, named in _published_texts(bundle):
            leaks = find_path_leaks(text)
            leaks.update({kind: count for kind, count in find_path_leaks(named, names).items() if kind != "home path"})
            problems += [f"{rel}: {count} {kind}{'s' if count > 1 else ''}" for kind, count in sorted(leaks.items())]
        return problems
    except (OSError, EOFError, ValueError) as error:
        return [f"could not scan: {type(error).__name__}"]


def _load(bundle: Path) -> tuple[dict[str, object] | None, list[str]]:
    try:
        data = json.loads((bundle / RESULT_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, [f"received unreadable {RESULT_NAME} ({error}); expected JSON"]
    if not isinstance(data, dict):
        return None, [f"received {type(data).__name__}; expected a JSON object"]
    return data, _schema_problems(data)


def _per_task(report: VerifyReport, name: str, tasks: list[Task], probe: Callable[[Task], list[str]],
              status: str = PASS) -> None:
    problems = [f"{task['id']}: {problem}" for task in tasks for problem in probe(task)]
    report.add(name, problems, f"{len(tasks)} task(s) consistent", status)


def verify_bundle(bundle: Path, names: LocalNames | None = None) -> VerifyReport:
    """Audit `bundle`; `names` (default: this machine's, none on CI) must not appear in published text."""
    report = VerifyReport(bundle=bundle)
    report.add("manifest", _manifest_problems(bundle), "every file hashed and listed")
    size_problems, size = _size_problems(bundle)
    report.add("size", size_problems, f"{size} bytes <= {BUNDLE_SIZE_CAP}")
    unpack = _unpack_problems(bundle)
    report.add("unpack", unpack, "archives and transcripts within the per-bundle unpack budget")
    if unpack:
        return report
    report.add("secrets", _secret_problems(bundle), "no unredacted secrets")
    report.add("paths", _path_problems(bundle, local_names() if names is None else names),
               "no home paths or local user/host names in transcripts, summary or result")
    result, problems = _load(bundle)
    report.add("schema", problems, "result.json matches the schema")
    if result is None or problems:
        return report
    version = result["bench_version"]
    report.add("bench_version", [] if version == __version__ else
               [f"bundle made with bench {version}; verify with a checkout of that version, this is {__version__}"],
               str(version))
    if version != __version__:
        return report
    known = {task.id: task for task in catalog.all_tasks()}
    tasks = result["tasks"]
    assert isinstance(tasks, list)
    membership, partial = suite_membership(str(result["suite"]), [str(task["id"]) for task in tasks])
    if partial:
        report.items.append(VerifyItem("suite", PARTIAL, f"{len(tasks)} task(s), not the exact "
                                                         f"{result['suite']} suite; listed, not ranked"))
    else:
        report.add("suite", membership, f"exactly the {result['suite']} suite")
    for task in tasks:
        report.add(f"checks:{task['id']}", _check_problems(known.get(str(task["id"])), task, bundle),
                   "re-graded from the saved workspace")
    report.add("scores", _score_problems(result), "objective, accuracy, subjective, composite recomputed")
    _per_task(report, "timings", tasks, _timing_problems, SELF_REPORTED)
    if any(_recorded_vision(task) for task in tasks):
        _per_task(report, "vision", tasks, _vision_problems, SELF_REPORTED)
    if result.get("judge") is None and not any(task["judge_votes"] for task in tasks):
        report.items.append(VerifyItem("judge", SKIP, "no judge"))
    else:
        report.add("judge", _judge_problems(result), "vote counts and medians consistent", SELF_REPORTED)
    return report


def _recorded_vision(task: Task) -> bool:
    return task.get("vision") is not None or any(str(c["name"]).startswith(VISION_PREFIX)
                                                 for c in _recorded_checks(task))

