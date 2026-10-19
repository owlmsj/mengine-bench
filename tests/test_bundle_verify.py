"""Result bundles from a fake run, and `mengine-bench verify` catching tampering."""

from __future__ import annotations

import gzip
import io
import json
import shutil
import tarfile
import uuid
from pathlib import Path

import pytest

from conftest import FakeAgent
from fakes import MARKER, fake_secret
from mengine_bench import cli, leaderboard
from mengine_bench.bundle import MANIFEST_NAME, write_manifest
from mengine_bench.redact import LocalNames
from mengine_bench.verify import verify_bundle

TASK = "ds-ab-playtest"

# Applies the reference solution like a perfect agent, and leaks a planted
# secret on stderr so the transcript must be redacted before publishing.
REFERENCE_AGENT = """
import sys
from pathlib import Path
from mengine_bench import catalog
task = next(t for t in catalog.all_tasks() if t.id == "ds-ab-playtest")
answers = task.reference(Path(sys.argv[1]))
sys.stderr.write("debug: " + sys.argv[3] + "\\n")
sys.stdout.buffer.write(answers[-1].encode("utf-8"))
"""

WRONG_AGENT = """
import sys
from pathlib import Path
(Path(sys.argv[1]) / "ab_result.json").write_text('{"sessions_a": 1}', encoding="utf-8")
print("done")
"""


def run_bundle(fake_agent: FakeAgent, tmp_path: Path, name: str, body: str, model: str) -> Path:
    template = json.loads(fake_agent(name, body))
    # -I would hide the installed package from the fake agent; drop it.
    template.remove("-I")
    template.append(fake_secret("openai"))
    out = tmp_path / "results"
    before = set(out.glob("*/*")) if out.exists() else set()
    code = cli.main(["run", "--suite", "fast", "--agent", "cmd", "--cmd", json.dumps(template), "--model", model,
                     "--tasks", TASK, "--out", str(out), "--work", str(tmp_path / f"work-{name}"),
                     "--submitter", "Alice Example"])
    assert code == 0
    [bundle] = set(out.glob("*/*")) - before
    return bundle


@pytest.fixture
def bundle(fake_agent: FakeAgent, tmp_path: Path) -> Path:
    return run_bundle(fake_agent, tmp_path, "reference", REFERENCE_AGENT, "fake/ref")


def board_as_complete(results: Path, link_base: Path) -> str:
    """Leaderboard with every verified bundle treated as a full-suite run.

    Test bundles hold one task, so they are partial (review R04) and never
    ranked; grouping and ordering tests rank them through the report mode.
    """
    report = leaderboard.verification_report(results, link_base)
    for entry in report["bundles"]:  # type: ignore[union-attr]
        entry["partial"] = False  # type: ignore[index]
    return leaderboard.build_leaderboard_from_report(results, link_base, report).markdown


def failed_items(bundle_dir: Path) -> list[str]:
    report = verify_bundle(bundle_dir)
    return [item.name for item in report.items if item.status == "FAIL"]


def test_bundle_has_every_file_and_a_valid_manifest(bundle: Path, tmp_path: Path) -> None:
    assert bundle.parent.name == "fast"
    assert bundle.name.split("_")[1:4] == ["cmd", "fake-ref", "none"]
    files = sorted(p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file())
    assert files == sorted([MANIFEST_NAME, "result.json", "summary.md", f"transcripts/{TASK}.jsonl.gz",
                            f"workspaces/{TASK}.tar.gz"])
    listed = [line.split("  ", 1)[1] for line in (bundle / MANIFEST_NAME).read_text(encoding="utf-8").splitlines()]
    assert sorted(listed) == sorted(set(files) - {MANIFEST_NAME})
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    assert result["submitter"] == "Alice Example"
    assert result["started_at"].endswith("Z") and result["finished_at"] >= result["started_at"]
    assert set(result["bench_commit"]) == {"sha", "dirty"}
    assert {"agent_cli", "model", "effort", "judge", "ram_gb"} <= set(result["environment"])
    [task] = result["tasks"]
    assert task["passed"] and task["answers"] == ["done"]
    assert all({"name", "ok", "mandatory"} <= set(check) for check in task["checks"])
    transcript = gzip.decompress((bundle / f"transcripts/{TASK}.jsonl.gz").read_bytes()).decode("utf-8")
    assert MARKER not in transcript and "[REDACTED:" in transcript
    assert str(tmp_path) not in transcript and str(tmp_path) not in json.dumps(result)
    with tarfile.open(bundle / f"workspaces/{TASK}.tar.gz") as archive:
        assert "ab_result.json" in archive.getnames()


def test_verify_passes_on_untouched_bundle(bundle: Path, capsys: pytest.CaptureFixture[str]) -> None:
    report = verify_bundle(bundle)
    assert report.ok, [(i.name, i.detail) for i in report.items if i.status == "FAIL"]
    names = {item.name for item in report.items}
    assert {"manifest", "schema", f"checks:{TASK}", "scores", "secrets", "size"} <= names
    assert cli.main(["verify", str(bundle)]) == 0
    assert "PASS manifest" in capsys.readouterr().out


def _rewrite_workspace(bundle_dir: Path, rel: str, content: bytes) -> None:
    archive_path = bundle_dir / f"workspaces/{TASK}.tar.gz"
    with tarfile.open(archive_path) as old:
        members = [(m, old.extractfile(m).read() if m.isfile() else None) for m in old.getmembers()]
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as new:
        for member, body in members:
            if member.name == rel:
                body = content
                member.size = len(content)
            new.addfile(member, io.BytesIO(body) if body is not None else None)
    archive_path.write_bytes(buffer.getvalue())


def test_verify_fails_when_workspace_altered(bundle: Path) -> None:
    _rewrite_workspace(bundle, "ab_result.json", b'{"sessions_a": 0}')
    write_manifest(bundle)
    assert failed_items(bundle) == [f"checks:{TASK}"]


def test_verify_fails_when_scores_edited(bundle: Path) -> None:
    path = bundle / "result.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    result["totals"]["objective"] = round(result["totals"]["objective"] - 7.0, 1)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_manifest(bundle)
    assert failed_items(bundle) == ["scores"]


def test_verify_fails_on_manifest_mismatch(bundle: Path) -> None:
    (bundle / "summary.md").write_text("# edited after sealing\n", encoding="utf-8")
    assert "manifest" in failed_items(bundle)
    assert cli.main(["verify", str(bundle)]) == 1


def test_verify_fails_on_unredacted_transcript_secret(bundle: Path) -> None:
    path = bundle / f"transcripts/{TASK}.jsonl.gz"
    line = json.dumps({"step": "0", "stream": "stdout", "text": "key " + fake_secret("openai")})
    path.write_bytes(gzip.compress(gzip.decompress(path.read_bytes()) + line.encode("utf-8") + b"\n"))
    write_manifest(bundle)
    assert failed_items(bundle) == ["secrets"]


def test_leaderboard_ranks_verified_bundles_and_skips_failing(fake_agent: FakeAgent, tmp_path: Path) -> None:
    good = run_bundle(fake_agent, tmp_path, "reference", REFERENCE_AGENT, "fake/ref")
    run_bundle(fake_agent, tmp_path, "wrong", WRONG_AGENT, "fake/wrong")
    # Short name: the pytest tmp path is already near the Windows MAX_PATH.
    tampered = good.parent / "tampered"
    shutil.copytree(good, tampered)
    (tampered / "summary.md").write_text("# edited\n", encoding="utf-8")
    target = tmp_path / "LEADERBOARD.md"
    assert cli.main(["leaderboard", "--results", str(tmp_path / "results"), "--output", str(target)]) == 0
    listed = target.read_text(encoding="utf-8")
    assert "| 1 | " not in listed and good.name in listed[listed.index("## Partial runs"):listed.index("## Skipped")]
    board = board_as_complete(tmp_path / "results", tmp_path)
    section = board[board.index("## FAST, no judge"):board.index("## Skipped")]
    assert section.index("| 1 | cmd") < section.index("fake/ref |") < section.index("| 2 | cmd")
    assert section.index("fake/wrong |") > section.index("| 2 | cmd")
    assert f"[summary](results/fast/{good.name}/summary.md)" in section
    assert "verified" in section and tampered.name not in section
    assert tampered.name in board[board.index("## Skipped"):]


def test_vision_ballots_must_match_recorded_majority() -> None:
    from mengine_bench.verify import _vision_problems
    task = {"checks": [{"name": "vision: red block", "ok": True, "mandatory": False}],
            "vision": {"checklist": ["red block"], "votes": 3, "ballots": [[True], [True], [False]], "errors": []}}
    assert _vision_problems(task) == []
    task["vision"]["ballots"] = [[True], [False], [False]]
    assert _vision_problems(task) == ["item 'red block': ballots give False, recorded True"]


def test_workspace_archive_with_parent_path_is_rejected(tmp_path: Path) -> None:
    from mengine_bench.verify import _safe_extract
    archive = tmp_path / "evil.tar.gz"
    with tarfile.open(archive, mode="w:gz") as tar:
        info = tarfile.TarInfo("../escape.txt")
        info.size = 2
        tar.addfile(info, io.BytesIO(b"hi"))
    (tmp_path / "out").mkdir()
    with pytest.raises(ValueError, match="escape.txt"):
        _safe_extract(archive, tmp_path / "out")
    assert not (tmp_path / "escape.txt").exists()


def test_scoring_uses_the_recorded_rounded_agent_time() -> None:
    # Regression: scoring on the unrounded time made verify recompute a
    # different total_agent_s whenever rounding crossed a 0.05 boundary.
    from mengine_bench.catalog import all_tasks
    from mengine_bench.runner.task_run import StepRecord, TaskRunRecord
    task = next(t for t in all_tasks() if t.id == TASK)
    record = TaskRunRecord(task_id=TASK, steps=[StepRecord(0, 0.2549, 0, "ok")])
    assert cli._outcome(task, record, ()).agent_s == 0.25


def _fake_home_line(name: str) -> str:
    # Built at runtime: never a real account name in the repo.
    return json.dumps({"step": "0", "stream": "stdout", "text": f"shell C:\\Users\\{name}\\AppData\\pwsh.exe"})


def test_verify_fails_on_unredacted_home_path_without_printing_it(bundle: Path) -> None:
    name = "u" + uuid.uuid4().hex[:8]
    path = bundle / f"transcripts/{TASK}.jsonl.gz"
    path.write_bytes(gzip.compress(gzip.decompress(path.read_bytes()) + _fake_home_line(name).encode("utf-8")
                                   + b"\n"))
    with (bundle / "summary.md").open("a", encoding="utf-8") as summary:
        summary.write(f"\nran in /home/{name}/bench\n")
    write_manifest(bundle)
    report = verify_bundle(bundle)
    [item] = [item for item in report.items if item.status == "FAIL"]
    assert item.name == "paths"
    assert f"transcripts/{TASK}.jsonl.gz: 1 home path" in item.detail and "summary.md: 1 home path" in item.detail
    assert name not in report.render()


def test_verify_fails_on_local_user_token(bundle: Path) -> None:
    names = LocalNames(user="usr" + uuid.uuid4().hex[:8], host=None)
    assert verify_bundle(bundle, names).ok
    with (bundle / "summary.md").open("a", encoding="utf-8") as summary:
        summary.write(f"\nby {names.user}\n")
    write_manifest(bundle)
    report = verify_bundle(bundle, names)
    assert [item.name for item in report.items if item.status == "FAIL"] == ["paths"]
    assert names.user not in report.render()


def test_rebundle_applies_current_redaction_without_rerunning(bundle: Path, tmp_path: Path,
                                                              monkeypatch: pytest.MonkeyPatch) -> None:
    raw = tmp_path / "work-reference"
    assert (raw / "run.json").is_file(), "run must store what rebundle needs"
    name = "u" + uuid.uuid4().hex[:8]
    with (raw / TASK / "transcripts" / "step-0.stdout.txt").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"cwd": f"C:\\Users\\{name}\\x"}) + "\n")

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("rebundle launched an agent")

    monkeypatch.setattr("mengine_bench.runner.process.run_process", forbidden)
    out = tmp_path / "rebundled"
    assert cli.main(["rebundle", str(raw), "--out", str(out)]) == 0
    [new] = list(out.glob("*/*"))
    assert new.name == bundle.name
    report = verify_bundle(new)
    assert report.ok, [(i.name, i.detail) for i in report.items if i.status == "FAIL"]
    transcript = gzip.decompress((new / f"transcripts/{TASK}.jsonl.gz").read_bytes()).decode("utf-8")
    assert name not in transcript and "<HOME>" in transcript
    old = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    fresh = json.loads((new / "result.json").read_text(encoding="utf-8"))
    assert fresh["totals"] == old["totals"] and fresh["tasks"][0]["checks"] == old["tasks"][0]["checks"]


def test_rebundle_names_what_an_old_raw_dir_lacks(bundle: Path, tmp_path: Path) -> None:
    raw = tmp_path / "work-reference"
    (raw / "run.json").unlink()
    with pytest.raises(SystemExit, match="run.json"):
        cli.main(["rebundle", str(raw), "--out", str(tmp_path / "again")])
    # Runs from before run.json existed: take the recorded data from the old bundle.
    assert cli.main(["rebundle", str(raw), "--out", str(tmp_path / "again"),
                     "--result", str(bundle / "result.json")]) == 0
    [new] = list((tmp_path / "again").glob("*/*"))
    assert verify_bundle(new).ok



# An agent that reads a public web page echoes the page's contact address into
# its transcript (2026-10-19 FULL run, web-mondrian-landing); published text
# keeps no third-party email. Placeholder domains and GitHub noreply stay.
def test_redact_text_hides_third_party_emails_only() -> None:
    from mengine_bench.redact import redact_text

    # Assembled at runtime so this file does not trip the repo's own privacy scan.
    third_party = "sammlungonline" + "@" + "kunsthaus.ch"
    text = f"mail {third_party} or dev@example.com or 1+me@users.noreply.github.com"
    out = redact_text(text)
    assert third_party not in out and "[REDACTED:email]" in out
    assert "dev@example.com" in out and "1+me@users.noreply.github.com" in out
