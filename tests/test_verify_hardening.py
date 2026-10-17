"""verify.py hardening from the public-release review (R02, R04, R05, R06, R09).

Each test is the regression for one finding; tampered bundles are re-sealed
with write_manifest so only the probed rule can fail.
"""

from __future__ import annotations

import gzip
import io
import json
import tarfile
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import catalog, leaderboard
from mengine_bench import verify as verify_module
from mengine_bench.bundle import RESULT_NAME, write_manifest
from mengine_bench.privacy import scan_repo
from mengine_bench.scoring import score_suite
from mengine_bench.verify import _outcome, _safe_extract, verify_bundle
from test_bundle_verify import REFERENCE_AGENT, TASK, run_bundle

Result = dict[str, object]


@pytest.fixture
def bundle(fake_agent: FakeAgent, tmp_path: Path) -> Path:
    return run_bundle(fake_agent, tmp_path, "reference", REFERENCE_AGENT, "fake/ref")


def _read(bundle_dir: Path) -> Result:
    return json.loads((bundle_dir / RESULT_NAME).read_text(encoding="utf-8"))


def _seal(bundle_dir: Path, result: Result) -> None:
    (bundle_dir / RESULT_NAME).write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_manifest(bundle_dir)


def _failed(bundle_dir: Path) -> list[str]:
    return [item.name for item in verify_bundle(bundle_dir).items if item.status == "FAIL"]


def _first_task(result: Result) -> dict[str, object]:
    tasks = result["tasks"]
    assert isinstance(tasks, list)
    return tasks[0]


# R02: evidence ---------------------------------------------------------------

def test_r02_scored_task_without_checks_or_workspace_fails(bundle: Path) -> None:
    result = _read(bundle)
    task = _first_task(result)
    (bundle / str(task["workspace"]["archive"])).unlink()  # type: ignore[index]
    task["workspace"], task["checks"] = None, []
    _seal(bundle, result)
    assert f"checks:{TASK}" in _failed(bundle)


def test_r02_fabricated_all_100_full_suite_without_evidence_fails(bundle: Path) -> None:
    result = _read(bundle)
    template = _first_task(result)
    (bundle / str(template["workspace"]["archive"])).unlink()  # type: ignore[index]
    tasks = []
    for spec in catalog.tasks("full"):
        tasks.append({**template, "id": spec.id, "category": spec.category, "weight": spec.weight,
                      "par_s": spec.par_s, "checks": [], "workspace": None, "transcript": None,
                      "check_score": 1.0, "mandatory_ok": True, "passed": True, "pass_ratio": 1.0,
                      "steps": [{**template["steps"][0], "wall_s": 1.0}], "agent_s": 1.0})  # type: ignore[index]
    suite = score_suite("full", [_outcome(task) for task in tasks])
    for task, score in zip(tasks, suite.tasks):
        task.update(c=score.correctness, s=score.speed, o=score.objective)
    totals = result["totals"]
    assert isinstance(totals, dict)
    totals.update(objective=suite.objective, accuracy=suite.accuracy, solved=suite.solved, total=suite.total,
                  total_agent_s=suite.total_agent_s)
    result.update(suite="full", tasks=tasks)
    _seal(bundle, result)
    assert suite.objective == 100.0
    failed = _failed(bundle)
    assert [f"checks:{spec.id}" for spec in catalog.tasks("full")] == [n for n in failed if n.startswith("checks:")]


# R04: suite membership -------------------------------------------------------

def test_r04_subset_run_is_partial_not_failed(bundle: Path) -> None:
    report = verify_bundle(bundle)
    assert report.ok and report.partial
    [item] = [item for item in report.items if item.name == "suite"]
    assert item.status == verify_module.PARTIAL


def test_r04_exact_suite_is_complete() -> None:
    ids = [task.id for task in catalog.tasks("fast")]
    assert verify_module.suite_membership("fast", list(reversed(ids))) == ([], False)
    assert verify_module.suite_membership("fast", ids[:-1])[1] is True


def test_r04_duplicate_task_ids_fail(bundle: Path) -> None:
    result = _read(bundle)
    tasks = result["tasks"]
    assert isinstance(tasks, list)
    tasks.append(dict(tasks[0]))
    _seal(bundle, result)
    assert "suite" in _failed(bundle)


def test_r04_partial_bundle_is_listed_but_not_ranked(bundle: Path, tmp_path: Path) -> None:
    results = bundle.parent.parent
    report = leaderboard.verification_report(results, tmp_path)
    [entry] = report["bundles"]  # type: ignore[misc]
    assert entry["partial"] is True
    board = leaderboard.build_leaderboard_from_report(results, tmp_path, report)
    assert board.ranked == 0 and board.partial == [entry["bundle"]]
    assert "| 1 | " not in board.markdown
    assert bundle.name in board.markdown[board.markdown.index("## Partial runs (not ranked)"):]


# R05: ordered checks ---------------------------------------------------------

def test_r05_duplicated_check_fails(bundle: Path) -> None:
    result = _read(bundle)
    task = _first_task(result)
    checks = task["checks"]
    assert isinstance(checks, list)
    scored = [c for c in checks if not c["mandatory"]]
    checks.extend([scored[0]] * 5)
    _seal(bundle, result)
    assert f"checks:{TASK}" in _failed(bundle)


def test_r05_reordered_checks_fail(bundle: Path) -> None:
    result = _read(bundle)
    task = _first_task(result)
    checks = task["checks"]
    assert isinstance(checks, list) and len(checks) > 1
    task["checks"] = list(reversed(checks))
    _seal(bundle, result)
    assert f"checks:{TASK}" in _failed(bundle)


# R06: tar member names -------------------------------------------------------

def _evil_archive(path: Path, info: tarfile.TarInfo, body: bytes = b"") -> Path:
    with tarfile.open(path, mode="w:gz") as tar:
        if info.isfile():
            info.size = len(body)
            tar.addfile(info, io.BytesIO(body))
        else:
            tar.addfile(info)
    return path


def _member(name: str, kind: bytes = tarfile.REGTYPE, link: str = "") -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type, info.linkname = kind, link
    return info


@pytest.mark.parametrize("info", [
    _member("..\\escaped.txt"),
    _member("sub\\file.txt"),
    _member("C:/drive.txt"),
    _member("C:drive-relative.txt"),
    _member("//server/share/unc.txt"),
    _member("/absolute.txt"),
    _member("a/../../dotdot.txt"),
    _member("link", tarfile.SYMTYPE, "../outside"),
    _member("hard", tarfile.LNKTYPE, "other.txt"),
    _member("dev", tarfile.CHRTYPE),
    _member("blk", tarfile.BLKTYPE),
    _member("fifo", tarfile.FIFOTYPE),
], ids=["backslash-dotdot", "backslash", "drive", "drive-relative", "unc", "absolute", "dotdot",
        "symlink", "hardlink", "chardev", "blockdev", "fifo"])
def test_r06_unsafe_member_is_rejected(tmp_path: Path, info: tarfile.TarInfo) -> None:
    archive = _evil_archive(tmp_path / "evil.tar.gz", info, b"hi")
    out = tmp_path / "deep" / "out"
    out.mkdir(parents=True)
    with pytest.raises(ValueError, match="expected a relative regular file"):
        _safe_extract(archive, out)
    assert [p for p in tmp_path.rglob("*") if p.is_file() and p != archive] == []


# R09: unpack budget ----------------------------------------------------------

def test_r09_byte_budget_stops_verify_before_regrading(bundle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mengine_bench.unpack_budget.UNPACK_BYTES_CAP", 64)
    report = verify_bundle(bundle)
    assert [item.name for item in report.items if item.status == "FAIL"] == ["unpack"]
    assert not any(item.name.startswith(("checks:", "secrets")) for item in report.items)


def test_r09_member_budget_stops_verify(bundle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mengine_bench.unpack_budget.UNPACK_MEMBERS_CAP", 1)
    assert _failed(bundle) == ["unpack"]


def _tar_gz(members: int, size: int) -> bytes:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as archive:
        for index in range(members):
            info = tarfile.TarInfo(f"f{index}.txt")
            info.size = size
            archive.addfile(info, io.BytesIO(b"x" * size))
    return gzip.compress(raw.getvalue(), mtime=0)


def test_r09_privacy_scan_stops_on_bundle_budget(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mengine_bench.unpack_budget.UNPACK_BYTES_CAP", 1000)
    run = tmp_path / "results" / "fast" / "run1" / "workspaces"
    run.mkdir(parents=True)
    # Each archive fits alone; together they exceed the per-bundle cap.
    (run / "a.tar.gz").write_bytes(_tar_gz(1, 600))
    (run / "b.tar.gz").write_bytes(_tar_gz(1, 600))
    (run / "c.tar.gz").write_bytes(_tar_gz(1, 600))
    hits = scan_repo(tmp_path)
    assert [(hit.path, hit.kind) for hit in hits] == [("results/fast/run1/workspaces/b.tar.gz", "unpack-budget")]


def test_r09_privacy_scan_member_cap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mengine_bench.unpack_budget.UNPACK_MEMBERS_CAP", 3)
    (tmp_path / "w.tar.gz").write_bytes(_tar_gz(4, 1))
    assert [hit.kind for hit in scan_repo(tmp_path)] == ["unpack-budget"]
