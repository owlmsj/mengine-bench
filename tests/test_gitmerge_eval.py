"""#124: git-merge-conflict passes any real merge that keeps both features and fails one that drops either."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import run_workspace_tests, write
from mengine_bench.tasks import gitmerge
from mengine_bench.tasks.gitmerge import (GM_BRANCH, GM_EVENT_LOOT, GM_MAIN_LOOT, GM_MERGED_LOOT, GM_REPO,
                                          GM_TEST_PITY, _gm_check, _gm_git, _gm_setup)

MERGE = "main is a merge commit of the old main and the branch"
MARKERS = "no conflict markers in tracked files"
PITY = "hidden pity timer tests pass"
EVENT = "hidden event multiplier tests pass"
BOTH = "hidden test with both together passes"

# Same behavior, another shape: the pity guard first, its own branch.
OTHER_SHAPE = '''"""Loot drops for the dungeon crawler."""

RARE_CHANCE = 0.05
PITY_LIMIT = 10


class LootTable:
    def __init__(self, event_multiplier: float = 1.0) -> None:
        self.event_multiplier = event_multiplier
        self.misses = 0

    def _rare(self) -> str:
        self.misses = 0
        return "rare"

    def drop(self, roll: float) -> str:
        if self.misses >= PITY_LIMIT:
            return self._rare()
        if roll < min(1.0, RARE_CHANCE * self.event_multiplier):
            return self._rare()
        self.misses += 1
        return "common"
'''

# Only a base-chance rare resets the pity count, against the docstring.
EVENT_RARE_KEEPS_COUNT = GM_MERGED_LOOT.replace('''        if self.misses >= PITY_LIMIT or roll < chance:
            self.misses = 0
            return "rare"''', '''        if self.misses >= PITY_LIMIT or roll < RARE_CHANCE:
            self.misses = 0
            return "rare"
        if roll < chance:
            return "rare"''')


def _task() -> gitmerge.EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == "git-merge-conflict")


def _repo(tmp_path: Path) -> Path:
    _gm_setup(tmp_path)
    return tmp_path / GM_REPO


def _merge_conflicted(repo: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([shutil.which("git") or "git", "merge", *extra, GM_BRANCH], cwd=repo, env=gitmerge._gm_env(),
                          capture_output=True, text=True, timeout=60, check=False)


def _resolve(repo: Path, loot: str, *merge_flags: str) -> None:
    _merge_conflicted(repo, *merge_flags)
    write(repo, "loot.py", loot)
    _gm_git(repo, "add", "-A")
    _gm_git(repo, "commit", "-q", "-m", "Merge weekend-event")


def test_the_fixture_is_main_clean_unmerged_and_conflicts(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert _gm_git(repo, "branch", "--show-current") == "main"
    assert _gm_git(repo, "status", "--porcelain") == ""
    assert _gm_git(repo, "rev-parse", "main") == gitmerge._gm_tips()[0]
    assert _gm_git(repo, "rev-parse", GM_BRANCH) == gitmerge._gm_tips()[1]
    assert run_workspace_tests(repo, ["tests.test_loot", "tests.test_pity"])
    merged = _merge_conflicted(repo, "--no-edit")
    assert merged.returncode != 0 and "CONFLICT" in merged.stdout, merged.stdout


def test_the_reference_passes_and_the_untouched_repo_fails(tmp_path: Path) -> None:
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task = _task()
    task.setup(tmp_path / "bare")
    bare = task.check(tmp_path / "bare", [""])
    assert not bare.passed and {MERGE, EVENT, BOTH} <= set(bare.failed())
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)
    assert run_workspace_tests(tmp_path / "solved" / GM_REPO, ["tests.test_loot", "tests.test_pity", "tests.test_event"])


def test_another_resolution_shape_passes(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _resolve(repo, OTHER_SHAPE)
    result = _gm_check(tmp_path, [""])
    assert result.passed, (result.failed(), result.details)


def test_a_merge_built_by_hand_with_plumbing_passes(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    old_main, branch_tip = gitmerge._gm_tips()
    _gm_git(repo, "checkout", "-q", GM_BRANCH, "--", "tests/test_event.py")
    write(repo, "loot.py", GM_MERGED_LOOT)
    _gm_git(repo, "add", "-A")
    tree = _gm_git(repo, "write-tree")
    commit = _gm_git(repo, "commit-tree", tree, "-p", old_main, "-p", branch_tip, "-m", "Merge weekend-event")
    _gm_git(repo, "update-ref", "refs/heads/main", commit)
    result = _gm_check(tmp_path, [""])
    assert result.passed, (result.failed(), result.details)


def test_a_squash_loses_only_the_merge_commit(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _resolve(repo, GM_MERGED_LOOT, "--squash")
    assert _gm_check(tmp_path, [""]).failed() == [MERGE]


def test_an_uncommitted_resolution_is_not_a_merge(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _merge_conflicted(repo)
    write(repo, "loot.py", GM_MERGED_LOOT)
    assert MERGE in _gm_check(tmp_path, [""]).failed()


@pytest.mark.parametrize(("loot", "lost"), [
    (GM_MAIN_LOOT, [EVENT, BOTH]),
    (GM_EVENT_LOOT, [PITY, BOTH]),
    (EVENT_RARE_KEEPS_COUNT, [BOTH]),
])
def test_a_resolution_that_drops_behavior_fails_its_checks(tmp_path: Path, loot: str, lost: list[str]) -> None:
    repo = _repo(tmp_path)
    _resolve(repo, loot)
    assert _gm_check(tmp_path, [""]).failed() == lost


def test_committed_conflict_markers_fail(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _merge_conflicted(repo)
    _gm_git(repo, "add", "-A")
    _gm_git(repo, "commit", "-q", "-m", "Merge weekend-event")
    failed = _gm_check(tmp_path, [""]).failed()
    assert MARKERS in failed and MERGE not in failed


def test_editing_a_visible_test_fails_the_gate(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _resolve(repo, GM_MERGED_LOOT)
    write(repo, "tests/test_pity.py", GM_TEST_PITY.replace("PITY_LIMIT + 1", "PITY_LIMIT + 2"))
    result = _gm_check(tmp_path, [""])
    assert not result.mandatory_ok and result.score == 0.0


def test_the_brief_does_not_hand_over_the_cause() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("conflict", "pity", "multiplier", "rebase", "git merge", "loot.py", "rare"):
        assert word not in prompt, word


def test_a_correct_answer_in_the_chat_alone_earns_nothing(tmp_path: Path) -> None:
    _repo(tmp_path)
    assert not _gm_check(tmp_path, ["Merged weekend-event into main and kept the pity timer"]).passed


def test_deleting_the_incoming_test_fails_the_gate(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _merge_conflicted(repo)
    write(repo, "loot.py", GM_MERGED_LOOT)
    (repo / "tests/test_event.py").unlink()
    _gm_git(repo, "add", "-A")
    _gm_git(repo, "commit", "-q", "-m", "Merge without incoming test")
    result = _gm_check(tmp_path, [""])
    assert not result.mandatory_ok and result.score == 0.0


def test_a_local_implementation_package_passes(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    write(repo, "loot_rules/__init__.py", "from .drops import LootTable\n")
    write(repo, "loot_rules/drops.py", GM_MERGED_LOOT)
    _resolve(repo, "from loot_rules import LootTable\nfrom loot_rules.drops import PITY_LIMIT, RARE_CHANCE\n")
    assert run_workspace_tests(repo, ["tests.test_loot", "tests.test_pity", "tests.test_event"])
    result = _gm_check(tmp_path, [""])
    assert result.passed, (result.failed(), result.details)


def test_a_documentation_commit_after_the_merge_passes(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _resolve(repo, GM_MERGED_LOOT)
    write(repo, "NOTES.md", "The weekend event and pity timer work together.\n")
    _gm_git(repo, "add", "NOTES.md")
    _gm_git(repo, "commit", "-q", "-m", "Document merged behavior")
    result = _gm_check(tmp_path, [""])
    assert result.passed, (result.failed(), result.details)


def test_a_missing_repo_scores_zero(tmp_path: Path) -> None:
    result = _gm_check(tmp_path, [""])
    assert result.score == 0.0
