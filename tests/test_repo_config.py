"""Repository shape: no GitHub automation, and git config for result bundles."""

from __future__ import annotations

import fnmatch
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
GIT = shutil.which("git")


def test_repo_runs_no_github_automation() -> None:
    # Submissions are pull requests the owner reviews and merges by hand
    # (CONTRIBUTING.md). Workflows on pull_request run fork code, and the old
    # required checks blocked results-only PRs, so the repo ships none.
    github = REPO / ".github"
    automation = [path.relative_to(REPO).as_posix() for pattern in ("workflows/*", "CODEOWNERS", "dependabot.yml")
                  for path in github.glob(pattern)]
    assert automation == [], f"received GitHub automation {automation}; expected none"


@pytest.mark.skipif(GIT is None, reason="git not on PATH")
def test_gitignore_keeps_bundle_workspaces() -> None:
    def ignored(path: str) -> bool:
        done = subprocess.run([GIT, "check-ignore", "-q", "--no-index", path], cwd=REPO, timeout=30)
        assert done.returncode in (0, 1), f"git check-ignore {path}: exit {done.returncode}"
        return done.returncode == 0

    assert not ignored("results/x/y/workspaces/a.tar.gz")
    assert ignored("workspaces/scratch.txt")


def _gitattributes() -> list[tuple[str, list[str]]]:
    rules = []
    for line in (REPO / ".gitattributes").read_text(encoding="utf-8").split("\n"):
        if line.strip() and not line.startswith("#"):
            pattern, *attrs = line.split()
            rules.append((pattern, attrs))
    return rules


def _matches(pattern: str, path: str) -> bool:
    if "/" not in pattern:
        return fnmatch.fnmatchcase(path.rsplit("/", 1)[-1], pattern)
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-2])
    return fnmatch.fnmatchcase(path, pattern)


def _text_attr(path: str) -> str:
    """Last matching rule wins, as in git; 'binary' is the -text -diff macro."""
    state = "unspecified"
    for pattern, attrs in _gitattributes():
        if not _matches(pattern, path):
            continue
        for attr in attrs:
            if attr in ("-text", "binary"):
                state = "unset"
            elif attr == "text=auto":
                state = "auto"
            elif attr == "text":
                state = "set"
    return state


def test_every_manifest_file_is_stored_as_raw_bytes() -> None:
    manifests = sorted((REPO / "results").glob("*/*/MANIFEST.sha256"))
    assert manifests
    paths = ["results/x/y/workspaces/a.tar.gz", "results/x/y/result.json"]
    for manifest in manifests:
        base = manifest.parent.relative_to(REPO).as_posix()
        paths.append(f"{base}/MANIFEST.sha256")
        for line in manifest.read_text(encoding="utf-8").split("\n"):
            if line.strip():
                paths.append(f"{base}/{line.split(None, 1)[1]}")
    for path in paths:
        assert _text_attr(path) == "unset", f"{path}: expected -text, got {_text_attr(path)}"
    assert _text_attr("mengine_bench/cli.py") == "auto"
    assert _text_attr("dist/x.tar.gz") == "unset"


@pytest.mark.skipif(GIT is None, reason="git not on PATH")
def test_git_agrees_bundle_bytes_are_not_converted() -> None:
    done = subprocess.run([GIT, "check-attr", "text", "--", "results/x/y/result.json", "README.md"],
                          cwd=REPO, capture_output=True, text=True, timeout=30)
    assert done.stdout.split("\n")[:2] == ["results/x/y/result.json: text: unset", "README.md: text: auto"]
