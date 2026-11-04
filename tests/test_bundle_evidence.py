"""Human evidence is preserved without becoming judge input (#165)."""

from __future__ import annotations

import json
import os
import subprocess
import tarfile
from dataclasses import replace
from pathlib import Path

import pytest

from conftest import FakeAgent
from fakes import fake_secret
from mengine_bench import bundle_judge, catalog, cli
from mengine_bench.bundle import bundle_leaks, write_bundle
from mengine_bench.core import CheckResult, EvalTask, Step
from mengine_bench.redact import LocalNames, PathScope

WAV_BYTES = b"RIFF\xff\x00WAVE human audio evidence"
PDF_BYTES = b"%PDF-1.7\nHuman-only form contents\n%%EOF"


def test_workspace_archive_preserves_files_and_scans_members(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    (ws / ".git").mkdir(parents=True)
    (ws / ".git/HEAD").write_bytes(b"ref: refs/heads/main\n")
    (ws / "target").mkdir()
    (ws / "target/ignored").write_bytes(b"build")
    raw = fake_secret("github").encode()
    (ws / "output.bin").write_bytes(raw)
    results = {"date": "2026-01-01", "agent": {"name": "fake", "model": "fake"},
               "run_id": "workspace", "tasks": [{"id": "test", "flags": []}]}
    from unittest.mock import patch
    with patch("mengine_bench.bundle.render_summary", return_value="summary"):
        bundle = write_bundle(results, tmp_path / "bundles", {}, PathScope(workspaces=(ws,)),
                              workspaces={"test": ws})
    with tarfile.open(bundle / "workspace/test.tar.gz") as archive:
        assert set(archive.getnames()) == {".git/HEAD", "output.bin"}
        assert archive.extractfile("output.bin").read() == raw
    assert "workspace/test.tar.gz/output.bin" in bundle_leaks(bundle, LocalNames())


def _evidence_task() -> EvalTask:
    return EvalTask(id="human-evidence", category="media", provenance="test", summary="test",
                    setup=lambda ws: None, steps=(Step("Create media files."),),
                    check=lambda ws, answers: CheckResult(checks=[("created", True)]),
                    reference=lambda ws: [], evidence=("out/audio.wav", "out/form.pdf"))


@pytest.mark.parametrize("native_paths", [False, True])
def test_fake_run_preserves_bytes_and_keeps_evidence_out_of_judge(
        fake_agent: FakeAgent, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, native_paths: bool) -> None:
    task = _evidence_task()
    if native_paths:
        task = replace(task, evidence=tuple(relative.replace("/", os.sep) for relative in task.evidence))
    monkeypatch.setattr(catalog, "all_tasks", lambda: [task])
    monkeypatch.setattr(catalog, "task_by_id", lambda task_id: task)
    body = f"""
import sys
from pathlib import Path
ws = Path(sys.argv[1])
(ws / 'out').mkdir()
(ws / 'out/audio.wav').write_bytes({WAV_BYTES!r})
(ws / 'out/form.pdf').write_bytes({PDF_BYTES!r})
print('done')
"""
    assert cli.main(["run", "--agent", "cmd", "--cmd", fake_agent("evidence", body),
                     "--model", "fake", "--tasks", task.id, "--out", str(tmp_path / "results")]) == 0
    [bundle] = (tmp_path / "results").iterdir()
    for relative, raw in zip(task.evidence, (WAV_BYTES, PDF_BYTES)):
        assert (bundle / "evidence" / task.id / relative).read_bytes() == raw
        assert not (bundle / "judge" / task.id / relative).exists()
    packet = bundle_judge.read_packet(bundle, task.id)
    assert packet.context.deliverables == () and packet.images == {} and packet.render is None
    context = json.dumps(packet.context.record())
    assert "human audio evidence" not in context
    assert "Human-only form contents" not in context


def _write_evidence_bundle(tmp_path: Path, files: dict[str, Path]) -> Path:
    results: dict[str, object] = {
        "date": "2026-01-01", "agent": {"name": "fake", "model": "fake"}, "run_id": "evidence",
        "tasks": [{"id": "human-evidence", "flags": []}],
    }
    # Summary rendering is exercised by the fake run; this isolates binary storage.
    from unittest.mock import patch
    with patch("mengine_bench.bundle.render_summary", return_value="summary"):
        return write_bundle(results, tmp_path / "results", {},
                            PathScope(workspaces=(tmp_path / "workspace",), names=LocalNames()),
                            evidence={"human-evidence": files})


def test_evidence_size_cap_and_nonregular_files_have_skip_notes(tmp_path: Path) -> None:
    from mengine_bench.bundle import EVIDENCE_FILE_BYTES
    ws = tmp_path / "workspace"
    ws.mkdir()
    (ws / "large.wav").write_bytes(b"x" * (EVIDENCE_FILE_BYTES + 1))
    (ws / "directory").mkdir()
    (tmp_path / "outside.pdf").write_bytes(PDF_BYTES)
    bundle = _write_evidence_bundle(tmp_path, {
        "large.wav": ws / "large.wav", "directory": ws / "directory",
        "outside.pdf": tmp_path / "outside.pdf",
    })
    assert not list((bundle / "evidence").rglob("*"))
    [task] = json.loads((bundle / "result.json").read_text(encoding="utf-8"))["tasks"]
    assert len(task["flags"]) == 3
    assert all("evidence" in note and "skipped" in note and "expected" in note and "received" in note
               for note in task["flags"])
    assert any("large.wav" in note and str(EVIDENCE_FILE_BYTES) in note for note in task["flags"])


@pytest.mark.parametrize("directory", [False, True])
def test_evidence_symlinks_are_skipped_with_notes(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, directory: bool) -> None:
    ws = tmp_path / "workspace"
    ws.mkdir()
    (ws / "real.pdf").write_bytes(PDF_BYTES)
    link = ws / "link"
    try:
        link.symlink_to(ws if directory else ws / "real.pdf", target_is_directory=directory)
    except OSError as error:
        if getattr(error, "winerror", None) != 1314:
            raise
        # Windows without symlink privilege: model the link bit, exercising the same rejection path (#165).
        if directory:
            link.mkdir()
            (link / "real.pdf").write_bytes(PDF_BYTES)
        else:
            link.write_bytes(PDF_BYTES)
        original = Path.is_symlink
        monkeypatch.setattr(Path, "is_symlink", lambda path: path == link or original(path))
    relative = "link/real.pdf" if directory else "link"
    bundle = _write_evidence_bundle(tmp_path, {relative: ws / relative})
    assert not (bundle / "evidence" / "human-evidence" / relative).exists()
    [task] = json.loads((bundle / "result.json").read_text(encoding="utf-8"))["tasks"]
    assert any(relative in note and "symlink" in note for note in task["flags"])


@pytest.mark.parametrize("relative", ["form.pdf", "opaque.gz"])
def test_secret_in_evidence_blocks_privacy_check(
        tmp_path: Path, capsys: pytest.CaptureFixture[str], relative: str) -> None:
    ws = tmp_path / "workspace"
    ws.mkdir()
    raw = PDF_BYTES + b"\n" + fake_secret("github").encode()
    (ws / relative).write_bytes(raw)
    bundle = _write_evidence_bundle(tmp_path, {relative: ws / relative})
    assert (bundle / "evidence/human-evidence" / relative).read_bytes() == raw
    assert f"evidence/human-evidence/{relative}" in bundle_leaks(bundle, LocalNames())
    assert cli._privacy_check(bundle, LocalNames()) == 1
    printed = capsys.readouterr().out
    assert "privacy check: FAILED; do not publish this bundle" in printed
    assert fake_secret("github") not in printed


def test_evidence_directory_links_are_rejected_on_disk(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    (ws / "real").mkdir(parents=True)
    (ws / "real/form.pdf").write_bytes(PDF_BYTES)
    link = ws / "linked"
    if os.name == "nt":
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(ws / "real")],
                                capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stdout + result.stderr
    else:
        link.symlink_to(ws / "real", target_is_directory=True)
    bundle = _write_evidence_bundle(tmp_path, {"linked/form.pdf": link / "form.pdf"})
    assert not (bundle / "evidence/human-evidence/linked/form.pdf").exists()
    [task] = json.loads((bundle / "result.json").read_text(encoding="utf-8"))["tasks"]
    assert any("symlink or junction" in note for note in task["flags"])


def test_evidence_at_the_size_cap_is_preserved(tmp_path: Path) -> None:
    from mengine_bench.bundle import EVIDENCE_FILE_BYTES
    ws = tmp_path / "workspace"
    ws.mkdir()
    raw = b"\xff" * EVIDENCE_FILE_BYTES
    (ws / "audio.wav").write_bytes(raw)
    bundle = _write_evidence_bundle(tmp_path, {"audio.wav": ws / "audio.wav"})
    assert (bundle / "evidence/human-evidence/audio.wav").read_bytes() == raw
    [task] = json.loads((bundle / "result.json").read_text(encoding="utf-8"))["tasks"]
    assert task["flags"] == []


def test_media_tasks_declare_owner_evidence() -> None:
    from mengine_bench.tasks import media, mediaedit
    assert media.TASKS[0].evidence == (media.WAV,)
    assert mediaedit.TASKS[0].evidence == (mediaedit.MEDIA_PHOTO_OUT, mediaedit.MEDIA_FORM_OUT)
