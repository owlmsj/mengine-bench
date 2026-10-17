"""Privacy scanner: generic detectors, optional private terms, allowlist, bundles, CLI.

Every sample is assembled at runtime from harmless fragments, so this file
never trips the scanner it tests (the repo-wide scan includes tests/).
"""

from __future__ import annotations

import gzip
import io
import tarfile
from pathlib import Path

import pytest

from fakes import KINDS, fake_secret
from mengine_bench import cli
from mengine_bench.privacy import (
    ALLOWED_LINES, PRIVATE_TERMS_ENV, load_private_terms, scan_repo, scan_text,
)

_AT = "@"
_BS = "\\"
LEAKS: dict[str, list[str]] = {
    "home-path": [
        "C:" + _BS + "Users" + _BS + "zed" + _BS + "repo",
        "C:" + _BS * 4 + "Users" + _BS * 4 + "zed",
        "d:/" + "users/zed/x",
        "/ho" + "me/zed/repo",
        "/Us" + "ers/zed/repo",
        _BS + "/home" + _BS + "/zed",
    ],
    "email": ["mail zed" + _AT + "corp-mail.io now"],
    "private-ip": [".".join(octets) for octets in (("10", "1", "2", "3"), ("172", "20", "0", "5"),
                                                    ("192", "168", "1", "9"), ("100", "100", "4", "2"))],
    "tailnet-host": ["box." + "tail1234" + ".ts" + ".net"],
    "windows-host": ["host DESKTOP-" + "AB12CD3 up"],
}
CLEAN = [
    "8.8.8.8", "100.128.0.1", "172.32.0.1", "Windows 10.0.26200", "v1.10.2.3.4",
    "https://example.com/home/page", "/home/{name}/x", "/home/<name>", "/usr/bin/env",
    "bot" + _AT + "users.noreply.github.com", "alice" + _AT + "example.com", "b" + _AT + "example.org",
    "DESKTOP-ABC", "@pytest.fixture",
]


@pytest.mark.parametrize(("kind", "sample"), [(k, s) for k, samples in LEAKS.items() for s in samples])
def test_generic_detector_catches_synthetic_leak(kind: str, sample: str) -> None:
    assert [hit.kind for hit in scan_text(f"intro\n{sample}\n", "x.txt")] == [kind]


@pytest.mark.parametrize("kind", KINDS)
def test_token_shapes_reuse_redact_detectors(kind: str) -> None:
    hits = scan_text(f"agent saw {fake_secret(kind)}", "x.txt")
    assert hits and all(hit.kind == "token" for hit in hits)


@pytest.mark.parametrize("sample", CLEAN)
def test_benign_text_is_clean(sample: str) -> None:
    assert scan_text(sample, "x.txt") == []


def _terms_file(tmp_path: Path) -> Path:
    path = tmp_path / "terms.txt"
    path.write_text("# comment\nzqxbanned\n\nZqx  Paired\n", encoding="utf-8")
    return path


def test_private_terms_fold_case_and_accents_and_match_words(tmp_path: Path) -> None:
    terms = load_private_terms(_terms_file(tmp_path))
    text = "ok\nApproved by Zqxbánned\nzqx\npaired\nzqxbannedx and zqx alone\n"
    assert [(hit.line, hit.kind) for hit in scan_text(text, "x.md", terms)] == [
        (2, "private-term"), (3, "private-term")]
    assert scan_text(text, "x.md") == []


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_allowlist_keeps_exactly_the_about_and_copyright_lines(tmp_path: Path) -> None:
    assert len(ALLOWED_LINES) == 2
    repo = tmp_path / "repo"
    _write(repo, "README.md", "# t\nmengine-bench is the coding-agent benchmark of Zqxbanned's AI\nby Zqxbanned\n")
    _write(repo, "LICENSE", "MIT\nCopyright (c) 2026 Zqxbanned\nZqxbanned again\n")
    _write(repo, "docs/x.md", "Copyright (c) 2026 Zqxbanned\n")
    hits = scan_repo(repo, load_private_terms(_terms_file(tmp_path)))
    assert sorted((hit.path, hit.line) for hit in hits) == [("LICENSE", 3), ("README.md", 3), ("docs/x.md", 1)]


def _gz(text: str) -> bytes:
    return gzip.compress(text.encode("utf-8"), mtime=0)


def test_bundle_archives_are_decompressed_and_scanned(tmp_path: Path) -> None:
    run = tmp_path / "results" / "fast" / "run1"
    (run / "transcripts").mkdir(parents=True)
    (run / "transcripts" / "t.jsonl.gz").write_bytes(_gz('{"x": "zed' + _AT + 'corp-mail.io"}\n'))
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as archive:
        for name, body in (("ok.txt", "fine"), ("notes.txt", "cwd /ho" + "me/zed/repo")):
            info = tarfile.TarInfo(name)
            info.size = len(body)
            archive.addfile(info, io.BytesIO(body.encode()))
    (run / "workspaces").mkdir()
    (run / "workspaces" / "t.tar.gz").write_bytes(gzip.compress(raw.getvalue(), mtime=0))
    hits = scan_repo(tmp_path)
    assert sorted((hit.path, hit.kind) for hit in hits) == [
        ("results/fast/run1/transcripts/t.jsonl.gz", "email"),
        ("results/fast/run1/workspaces/t.tar.gz!notes.txt", "home-path"),
    ]


def test_cli_prints_file_and_count_never_the_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                   capsys: pytest.CaptureFixture[str]) -> None:
    repo = tmp_path / "repo"
    _write(repo, "a.md", "zqxbanned twice zqxbanned\n")
    _write(repo, "b.md", "clean\n")
    terms = _terms_file(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.delenv(PRIVATE_TERMS_ENV, raising=False)
    assert cli.main(["privacy-scan"]) == 0
    assert cli.main(["privacy-scan", "--private-terms", str(terms)]) == 1
    out = capsys.readouterr().out
    assert "a.md: 2 hit(s)" in out and "b.md" not in out
    assert "zqxbanned" not in out.lower()
    monkeypatch.setenv(PRIVATE_TERMS_ENV, str(terms))
    assert cli.main(["privacy-scan"]) == 1
