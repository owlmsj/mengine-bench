"""`mengine-bench redo <bundle>` reruns only the crashed tasks of a bundle with its own agent (#205)."""

from __future__ import annotations

import json
import tarfile
from pathlib import Path

import psutil
import pytest

from conftest import FakeAgent
from mengine_bench import __version__, cli, run_command

# Solves ds-ab-playtest with its reference; any other task gets a wrong answer, never a crash.
REFERENCE_OR_GUESS = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = catalog.task_by_id("ds-ab-playtest")
try:
    answer = task.reference(Path(sys.argv[1]))[-1]
except Exception:
    answer = "no idea"
sys.stdout.buffer.write(answer.encode("utf-8"))
"""
CRASHED = "ds-ab-playtest"
KEPT = "bo-reconcile"


def _template(fake_agent: FakeAgent) -> str:
    template = json.loads(fake_agent("reference-or-guess", REFERENCE_OR_GUESS))
    template.remove("-I")  # -I would hide the installed package from the fake agent
    return json.dumps(template)


def _crashed_bundle(template: str, out: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    real_run_task = run_command.run_task

    def vanishing(task: object, *args: object, **kwargs: object) -> object:
        if getattr(task, "id") == CRASHED:
            raise psutil.NoSuchProcess(2592)
        return real_run_task(task, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(run_command, "run_task", vanishing)
        assert cli.main(["run", "--agent", "cmd", "--cmd", template, "--model", "fake/ref",
                         "--tasks", f"{CRASHED},{KEPT}", "--out", str(out)]) == 0
    [bundle] = [path.parent for path in out.glob("*/result.json")]
    return bundle


def _judged_with_a_profile(bundle: Path) -> dict[str, object]:
    """Make the bundle look like the #205 one: judged, and an archive written before fix 2."""
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    for row in result["tasks"]:
        row.update(judge=70, judge_rationale="fine", judge_parts={"correctness": 70})
    result["judge"] = {"agent": "claude", "model": "judge-model"}
    result["totals"]["judge"] = 70.0
    (bundle / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (bundle / "judge" / f"{CRASHED}.png").write_bytes(b"old frame")
    profile = bundle.parent / "profile"
    (profile / "Default").mkdir(parents=True)
    (profile / "Local State").write_text("{}", encoding="utf-8")
    (profile / "Default" / "History").write_text("history", encoding="utf-8")
    archive_path = bundle / "workspace" / f"{KEPT}.tar.gz"
    with tarfile.open(archive_path) as archive:
        kept = {member.name: archive.extractfile(member).read() for member in archive.getmembers() if member.isfile()}
    with tarfile.open(archive_path, "w:gz") as archive:
        for name, raw in kept.items():
            info = tarfile.TarInfo(name)
            info.size = len(raw)
            archive.addfile(info, __import__("io").BytesIO(raw))
        archive.add(profile / "Local State", arcname="tmp/edgeprofile/Local State")
        archive.add(profile / "Default" / "History", arcname="tmp/edgeprofile/Default/History")
    return result


def test_redo_reruns_the_crashed_task_and_keeps_the_rest(fake_agent: FakeAgent, tmp_path: Path,
                                                         monkeypatch: pytest.MonkeyPatch,
                                                         capsys: pytest.CaptureFixture[str]) -> None:
    template = _template(fake_agent)
    bundle = _crashed_bundle(template, tmp_path / "results", monkeypatch)
    before = _judged_with_a_profile(bundle)
    rows_before = {row["id"]: row for row in before["tasks"]}
    assert rows_before[CRASHED]["status"] == "crash" and rows_before[KEPT]["status"] != "crash"
    capsys.readouterr()

    assert cli.main(["redo", str(bundle), "--cmd", template]) == 0

    printed = capsys.readouterr().out
    assert printed.rstrip().endswith("privacy check: clean"), printed
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in result["tasks"]}
    assert [row["id"] for row in result["tasks"]] == [row["id"] for row in before["tasks"]]
    assert rows[CRASHED]["status"] == "ok" and rows[CRASHED]["c"] == 1.0, rows[CRASHED]
    assert any("redo" in flag and "#205" in flag for flag in rows[CRASHED]["flags"])
    assert rows[CRASHED]["judge"] is None and rows[CRASHED]["transcript"] == f"transcripts/{CRASHED}.jsonl.gz"
    assert (bundle / rows[CRASHED]["transcript"]).is_file() and (bundle / "judge" / f"{CRASHED}.json").is_file()
    assert not (bundle / "judge" / f"{CRASHED}.png").exists(), "the old vote's frame must go with the vote"
    assert rows[KEPT]["c"] == rows_before[KEPT]["c"] and rows[KEPT]["checks"] == rows_before[KEPT]["checks"]
    assert result["run_id"] == before["run_id"] and result["date"] == before["date"]
    assert result["agent"] == before["agent"] and result["config"] == before["config"]
    assert result["totals"]["correct"] == round(100 * (1.0 + rows[KEPT]["c"]) / 2, 1)
    assert result["judge"] is None and result["totals"]["judge"] is None and result["totals"]["score"] is None
    [redo] = result["redo"]
    assert redo["tasks"] == [CRASHED] and redo["bench_version"] == __version__
    assert redo["previous"][CRASHED]["status"] == "crash"
    assert "NoSuchProcess" in redo["previous"][CRASHED]["error"]
    assert redo["judge_cleared"] == {"agent": "claude", "model": "judge-model"}
    with tarfile.open(bundle / "workspace" / f"{KEPT}.tar.gz") as archive:
        assert not any(name.startswith("tmp/edgeprofile") for name in archive.getnames())
    assert any("tmp/edgeprofile" in flag for flag in rows[KEPT]["flags"])
    assert "redo" in (bundle / "summary.md").read_text(encoding="utf-8").lower()


def _bundle_with(tmp_path: Path, **changes: object) -> Path:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    result = {"bench_version": __version__, "run_id": "r", "date": "2026-11-06", "config": {},
              "agent": {"name": "cmd", "model": "fake/ref", "effort": None, "version": None},
              "price_per_mtok": None, "submitter": None, "judge": None,
              "tasks": [{"id": CRASHED, "status": "ok"}], **changes}
    (bundle / "result.json").write_text(json.dumps(result), encoding="utf-8")
    return bundle


@pytest.mark.parametrize(("changes", "argv", "expected"), [
    ({"bench_version": "2.5.2"}, [], "received bundle of bench 2.5.2; expected bench " + ".".join(__version__.split(".")[:2])),
    ({}, [], "received no task with status crash"),
    ({}, ["--tasks", "no-such-task"], "received --tasks ['no-such-task']"),
    ({}, ["--tasks", CRASHED], "received --agent cmd without --cmd"),
])
def test_redo_refuses_with_the_received_value(changes: dict[str, object], argv: list[str], expected: str,
                                               tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    bundle = _bundle_with(tmp_path, **changes)
    before = (bundle / "result.json").read_bytes()
    assert cli.main(["redo", str(bundle), *argv]) == 1
    assert expected in capsys.readouterr().out
    assert (bundle / "result.json").read_bytes() == before
