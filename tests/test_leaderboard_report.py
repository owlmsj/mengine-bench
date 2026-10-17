"""LEADERBOARD.md from a verification report: the publish job never runs task checks."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import cli, leaderboard
from mengine_bench.bundle import RESULT_NAME
from test_bundle_verify import REFERENCE_AGENT, run_bundle

REPO = Path(__file__).resolve().parents[1]
SHIPPED = sorted((REPO / "results").glob(f"*/*/{RESULT_NAME}"))


def _shipped_results(tmp_path: Path) -> tuple[Path, Path]:
    # result.json alone is enough for the report mode: it never opens workspaces.
    assert SHIPPED, "expected at least one shipped bundle under results/<suite>/<bundle>/"
    source = SHIPPED[0]
    bundle = tmp_path / "results" / source.parent.parent.name / source.parent.name
    bundle.mkdir(parents=True)
    shutil.copyfile(source, bundle / RESULT_NAME)
    return tmp_path / "results", bundle


def _report_for(bundle: Path, base: Path, ok: bool = True) -> dict[str, object]:
    digest = hashlib.sha256((bundle / RESULT_NAME).read_bytes()).hexdigest()
    entry = {"bundle": bundle.relative_to(base).as_posix(), "ok": ok, "partial": False,
             "failed": [] if ok else ["checks"], "result_sha256": digest}
    return {"report_version": leaderboard.REPORT_VERSION, "bundles": [entry]}


def test_from_report_ranks_without_running_verify(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    results, bundle = _shipped_results(tmp_path)
    import mengine_bench.verify as verify_module

    def _forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("the report mode must not verify (it would execute submission code)")

    monkeypatch.setattr(verify_module, "verify_bundle", _forbidden)
    report = tmp_path / "report.json"
    report.write_text(json.dumps(_report_for(bundle, tmp_path)), encoding="utf-8")
    target = tmp_path / "LEADERBOARD.md"
    assert cli.main(["leaderboard", "--results", str(results), "--output", str(target),
                     "--from-report", str(report)]) == 0
    board = target.read_text(encoding="utf-8")
    assert "| 1 | " in board and bundle.name in board and "## Skipped" not in board


def test_report_mode_imports_no_task_code(tmp_path: Path) -> None:
    results, bundle = _shipped_results(tmp_path)
    report = _report_for(bundle, tmp_path)
    script = (
        "import json, sys\nfrom pathlib import Path\n"
        "from mengine_bench import leaderboard\n"
        "board = leaderboard.build_leaderboard_from_report(Path(sys.argv[1]), Path(sys.argv[2]), "
        "json.loads(sys.argv[3]))\n"
        "assert board.ranked == 1, board.skipped\n"
        "bad = sorted(m for m in sys.modules if m.split('.')[:2] in "
        "(['mengine_bench', 'verify'], ['mengine_bench', 'tasks'], ['mengine_bench', 'catalog']))\n"
        "assert not bad, bad\n"
    )
    done = subprocess.run([sys.executable, "-c", script, str(results), str(tmp_path), json.dumps(report)],
                          capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr


def test_from_report_skips_unreported_failed_and_changed_bundles(tmp_path: Path) -> None:
    results, bundle = _shipped_results(tmp_path)
    failed = bundle.parent / "failed"
    changed = bundle.parent / "changed"
    unreported = bundle.parent / "unreported"
    for extra in (failed, changed, unreported):
        shutil.copytree(bundle, extra)
    report = _report_for(bundle, tmp_path)
    entries = report["bundles"]
    assert isinstance(entries, list)
    entries.append(_report_for(failed, tmp_path, ok=False)["bundles"][0])  # type: ignore[index]
    entries.append(_report_for(changed, tmp_path)["bundles"][0])  # type: ignore[index]
    (changed / RESULT_NAME).write_bytes((changed / RESULT_NAME).read_bytes() + b"\n")
    board = leaderboard.build_leaderboard_from_report(results, tmp_path, report)
    reasons = dict(board.skipped)
    assert board.ranked == 1
    assert reasons[failed.relative_to(tmp_path).as_posix()] == "verify failed: checks"
    assert "result.json changed" in reasons[changed.relative_to(tmp_path).as_posix()]
    assert "not in the verification report" in reasons[unreported.relative_to(tmp_path).as_posix()]


def test_report_with_wrong_shape_is_rejected(tmp_path: Path) -> None:
    results, _bundle = _shipped_results(tmp_path)
    with pytest.raises(ValueError, match="report_version"):
        leaderboard.build_leaderboard_from_report(results, tmp_path, {"report_version": 99, "bundles": []})
    with pytest.raises(ValueError, match="bundles"):
        leaderboard.build_leaderboard_from_report(
            results, tmp_path, {"report_version": leaderboard.REPORT_VERSION, "bundles": "x"})


def test_write_report_round_trip_matches_direct_build(fake_agent: FakeAgent, tmp_path: Path) -> None:
    good = run_bundle(fake_agent, tmp_path, "reference", REFERENCE_AGENT, "fake/ref")
    tampered = good.parent / "tampered"
    shutil.copytree(good, tampered)
    (tampered / "summary.md").write_text("# edited\n", encoding="utf-8")
    results, report_file = tmp_path / "results", tmp_path / "verification.json"
    assert cli.main(["leaderboard", "--results", str(results), "--output", str(tmp_path / "unused.md"),
                     "--write-report", str(report_file)]) == 0
    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert {entry["ok"] for entry in report["bundles"]} == {True, False}
    target = tmp_path / "LEADERBOARD.md"
    assert cli.main(["leaderboard", "--results", str(results), "--output", str(target),
                     "--from-report", str(report_file)]) == 0
    direct = leaderboard.build_leaderboard(results, tmp_path)
    assert target.read_text(encoding="utf-8") == direct.markdown
