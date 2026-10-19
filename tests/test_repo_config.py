"""Workflow hardening and git config for result bundles.

Line-based checks on purpose: the workflows are small, and a YAML parser is not
a dependency of the bench.
"""

from __future__ import annotations

import fnmatch
import re
import runpy
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((REPO / ".github" / "workflows").glob("*.yml"))
SUBMISSION_CHECK = REPO / ".github" / "scripts" / "check_submission.py"
GIT = shutil.which("git")


def _jobs(text: str) -> dict[str, str]:
    """Job name -> its block, from the two-space-indented keys under `jobs:`."""
    body = text[text.index("\njobs:\n") + len("\njobs:\n"):]
    parts = re.split(r"(?m)^  ([A-Za-z0-9_-]+):\n", body)
    return dict(zip(parts[1::2], parts[2::2]))


def _run_scripts(text: str) -> list[str]:
    scripts: list[str] = []
    lines = text.split("\n")
    for index, line in enumerate(lines):
        found = re.match(r"^(\s*)(?:- )?run: ?(.*)$", line)
        if not found:
            continue
        indent, rest = len(found.group(1)), found.group(2)
        if rest not in ("|", ">"):
            scripts.append(rest)
            continue
        block = [follow for follow in lines[index + 1:]]
        kept = []
        for follow in block:
            if follow.strip() and len(follow) - len(follow.lstrip()) <= indent:
                break
            kept.append(follow)
        scripts.append("\n".join(kept))
    return scripts


def test_workflows_exist_and_are_valid_yaml_shaped() -> None:
    assert {path.name for path in WORKFLOWS} == {"ci.yml", "results.yml"}
    for path in WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        assert "\t" not in text, f"{path.name}: tabs are invalid YAML indentation"
        assert text.startswith("name: ") and "\njobs:\n" in text


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda p: p.name)
def test_actions_are_pinned_by_full_sha_with_version_comment(path: Path) -> None:
    uses = re.findall(r"uses: (\S+)(.*)", path.read_text(encoding="utf-8"))
    assert uses
    for action, comment in uses:
        assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", action), f"{path.name}: {action} is not SHA-pinned"
        assert re.fullmatch(r" # v\d+\.\d+\.\d+", comment), f"{path.name}: {action} lacks a '# vX.Y.Z' comment"


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda p: p.name)
def test_read_only_default_locked_install_and_no_persisted_credentials(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    head = text[:text.index("\njobs:\n")]
    assert re.search(r"(?m)^permissions:\n  contents: read$", head), f"{path.name}: top-level contents: read"
    checkouts = text.count("uses: actions/checkout@")
    assert checkouts and text.count("persist-credentials: false") == checkouts
    syncs = re.findall(r"uv sync.*", text)
    assert syncs and all(sync == "uv sync --locked" for sync in syncs), syncs


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda p: p.name)
def test_no_expression_interpolation_inside_run_scripts(path: Path) -> None:
    # ${{ }} in run: is template injection; values go through env: instead.
    for script in _run_scripts(path.read_text(encoding="utf-8")):
        assert "${{" not in script, f"{path.name}: expression inside run: {script[:80]!r}"


def test_publish_job_never_executes_submission_code() -> None:
    jobs = _jobs((REPO / ".github" / "workflows" / "results.yml").read_text(encoding="utf-8"))
    writers = [name for name, block in jobs.items() if "contents: write" in block]
    assert writers == ["publish"]
    publish = jobs["publish"]
    assert "needs: verify-main" in publish
    assert "--from-report" in publish and "actions/download-artifact@" in publish
    for forbidden in ("mengine-bench verify", "--write-report", "selftest", "mengine-bench run"):
        assert forbidden not in publish
    for name, block in jobs.items():
        if name == "publish":
            continue
        assert "contents: read" in block and "secrets." not in block, name
    verify_main = jobs["verify-main"]
    assert "--write-report" in verify_main and "actions/upload-artifact@" in verify_main


def test_publish_opens_a_reviewable_pull_request_without_a_bypass() -> None:
    # main accepts pull requests only, and a personal repository cannot add
    # the GitHub Actions app to a ruleset bypass list, so publish must not
    # push to main. It updates a long-lived branch and opens a PR the owner
    # merges; no secret or extra credential is involved.
    path = REPO / ".github" / "workflows" / "results.yml"
    text = path.read_text(encoding="utf-8")
    publish = _jobs(text)["publish"]
    assert "ref: main" in publish
    assert "gh pr create" in publish
    assert "git push --force origin" in publish
    assert "HEAD:main" not in publish
    assert "pull-requests: write" in publish
    assert "secrets." not in text


def test_codeowners_guard_workflows_and_bench_code() -> None:
    rules = [line.split() for line in (REPO / ".github" / "CODEOWNERS").read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.startswith("#")]
    owned = {rule[0] for rule in rules if len(rule) >= 2}
    assert {"/.github/", "/mengine_bench/"} <= owned


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


def _submission(rows: list[tuple[str, ...]], tmp_path: Path) -> tuple[int, str]:
    changed = tmp_path / "changed.tsv"
    changed.write_text("".join("\t".join(row) + "\n" for row in rows), encoding="utf-8")
    module = runpy.run_path(str(SUBMISSION_CHECK))
    return module["check_submission"](changed)


GOOD = [("added", "results/full/run-a/result.json"), ("added", "results/full/run-a/workspaces/t.tar.gz")]


@pytest.mark.parametrize(("rows", "reason"), [
    (GOOD + [("modified", "mengine_bench/verify.py")], "outside results/<suite>/<bundle>/"),
    (GOOD + [("added", ".github/workflows/results.yml")], "outside results/<suite>/<bundle>/"),
    (GOOD + [("modified", "LEADERBOARD.md")], "LEADERBOARD.md"),
    (GOOD + [("added", "results/full/run-b/result.json")], "exactly one"),
    (GOOD + [("modified", "results/full/old/result.json")], "immutable"),
    ([("added", "results/full/result.json")], "outside results/<suite>/<bundle>/"),
    ([("renamed", "results/full/run-a/x.py", "mengine_bench/x.py")], "outside results/<suite>/<bundle>/"),
    ([], "exactly one"),
])
def test_submission_check_rejects(rows: list[tuple[str, ...]], reason: str, tmp_path: Path) -> None:
    code, message = _submission(rows, tmp_path)
    assert code == 1 and reason in message, message


def test_submission_check_accepts_one_new_bundle(tmp_path: Path) -> None:
    assert _submission(GOOD, tmp_path) == (0, "results/full/run-a")
