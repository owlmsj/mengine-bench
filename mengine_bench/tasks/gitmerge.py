"""Git merge: a feature branch and main both changed the same function while parallel sessions worked (#124).

Setup builds a real repo: main shipped a pity timer, the weekend-event branch added an event multiplier to the same
drop function, so merging conflicts. The gold reads the commit graph and runs hidden tests on the work tree, so any
merge route passes (git merge and a manual resolution, a merge tool, an editor). A squash or a rebase loses only the
merge-commit check: the features still earn theirs.
"""

from __future__ import annotations

import functools
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, read, run_hidden_tests, saw, scratch_root, write

GM_REPO = "dropgame"
GM_BRANCH = "weekend-event"
GM_GIT_LIMIT_S = 60
GM_TEST_LIMIT_S = 60

GM_README = """# Drop game

Loot drops for the dungeon crawler. `python -m unittest` runs the tests.
"""

GM_BASE_LOOT = '''"""Loot drops for the dungeon crawler."""

RARE_CHANCE = 0.05


class LootTable:
    """Decides what one defeated monster drops."""

    def __init__(self) -> None:
        pass

    def drop(self, roll: float) -> str:
        """Return "rare" or "common" for a roll in [0, 1).

        A roll below the rare chance drops a rare.
        """
        if roll < RARE_CHANCE:
            return "rare"
        return "common"
'''

GM_MAIN_LOOT = '''"""Loot drops for the dungeon crawler."""

RARE_CHANCE = 0.05
PITY_LIMIT = 10


class LootTable:
    """Decides what one defeated monster drops."""

    def __init__(self) -> None:
        self.misses = 0

    def drop(self, roll: float) -> str:
        """Return "rare" or "common" for a roll in [0, 1).

        A roll below the rare chance drops a rare.
        Pity timer: after PITY_LIMIT common drops in a row, the next drop is rare whatever the roll.
        Any rare drop, however it came, resets the count of commons in a row to zero.
        """
        if self.misses >= PITY_LIMIT or roll < RARE_CHANCE:
            self.misses = 0
            return "rare"
        self.misses += 1
        return "common"
'''

GM_EVENT_LOOT = '''"""Loot drops for the dungeon crawler."""

RARE_CHANCE = 0.05


class LootTable:
    """Decides what one defeated monster drops."""

    def __init__(self, event_multiplier: float = 1.0) -> None:
        self.event_multiplier = event_multiplier

    def drop(self, roll: float) -> str:
        """Return "rare" or "common" for a roll in [0, 1).

        A roll below the rare chance drops a rare.
        During an event the rare chance is RARE_CHANCE times event_multiplier, capped at 1.
        A rare that only the event made possible is a rare like any other.
        """
        chance = min(1.0, RARE_CHANCE * self.event_multiplier)
        if roll < chance:
            return "rare"
        return "common"
'''

GM_MERGED_LOOT = '''"""Loot drops for the dungeon crawler."""

RARE_CHANCE = 0.05
PITY_LIMIT = 10


class LootTable:
    """Decides what one defeated monster drops."""

    def __init__(self, event_multiplier: float = 1.0) -> None:
        self.misses = 0
        self.event_multiplier = event_multiplier

    def drop(self, roll: float) -> str:
        """Return "rare" or "common" for a roll in [0, 1).

        A roll below the rare chance drops a rare.
        Pity timer: after PITY_LIMIT common drops in a row, the next drop is rare whatever the roll.
        Any rare drop, however it came, resets the count of commons in a row to zero.
        During an event the rare chance is RARE_CHANCE times event_multiplier, capped at 1.
        A rare that only the event made possible is a rare like any other.
        """
        chance = min(1.0, RARE_CHANCE * self.event_multiplier)
        if self.misses >= PITY_LIMIT or roll < chance:
            self.misses = 0
            return "rare"
        self.misses += 1
        return "common"
'''

GM_TEST_LOOT = '''import unittest

from loot import LootTable


class DropTest(unittest.TestCase):
    def test_a_low_roll_drops_a_rare(self) -> None:
        self.assertEqual(LootTable().drop(0.01), "rare")

    def test_a_high_roll_drops_a_common(self) -> None:
        self.assertEqual(LootTable().drop(0.5), "common")
'''

GM_TEST_PITY = '''import unittest

from loot import PITY_LIMIT, LootTable


class PityTest(unittest.TestCase):
    def test_the_drop_after_the_limit_is_rare(self) -> None:
        table = LootTable()
        drops = [table.drop(0.99) for _ in range(PITY_LIMIT + 1)]
        self.assertEqual(drops, ["common"] * PITY_LIMIT + ["rare"])
'''

GM_TEST_EVENT = '''import unittest

from loot import LootTable


class EventTest(unittest.TestCase):
    def test_the_event_raises_the_rare_chance(self) -> None:
        self.assertEqual(LootTable(event_multiplier=2.0).drop(0.08), "rare")
        self.assertEqual(LootTable().drop(0.08), "common")
'''

GM_HIDDEN = '''import unittest

from loot import LootTable


class HiddenPityTest(unittest.TestCase):
    def test_pity_after_ten_commons_and_reset(self) -> None:
        table = LootTable()
        drops = [table.drop(0.99) for _ in range(22)]
        self.assertEqual(drops, (["common"] * 10 + ["rare"]) * 2)

    def test_a_rolled_rare_resets_the_count(self) -> None:
        table = LootTable()
        drops = [table.drop(0.99) for _ in range(6)] + [table.drop(0.01)] + [table.drop(0.99) for _ in range(11)]
        self.assertEqual(drops, ["common"] * 6 + ["rare"] + ["common"] * 10 + ["rare"])


class HiddenEventTest(unittest.TestCase):
    def test_the_multiplier_scales_the_chance(self) -> None:
        self.assertEqual(LootTable(event_multiplier=3.0).drop(0.14), "rare")
        self.assertEqual(LootTable(event_multiplier=3.0).drop(0.16), "common")
        self.assertEqual(LootTable().drop(0.06), "common")


class HiddenBothTest(unittest.TestCase):
    def test_an_event_rare_resets_pity_and_pity_still_holds(self) -> None:
        table = LootTable(event_multiplier=3.0)
        drops = [table.drop(0.9) for _ in range(4)] + [table.drop(0.10)] + [table.drop(0.9) for _ in range(11)]
        self.assertEqual(drops, ["common"] * 4 + ["rare"] + ["common"] * 10 + ["rare"])
'''

GM_HIDDEN_CASES = (("hidden pity timer tests pass", "HiddenPityTest"),
                   ("hidden event multiplier tests pass", "HiddenEventTest"),
                   ("hidden test with both together passes", "HiddenBothTest"))
GM_VISIBLE = {"tests/test_loot.py": GM_TEST_LOOT, "tests/test_pity.py": GM_TEST_PITY, "tests/test_event.py": GM_TEST_EVENT}
GM_CONFLICT_MARKER = re.compile(r"^(<{7}|={7}|>{7})(\s|$)", re.MULTILINE)


def _gm_env() -> dict[str, str]:
    """Git with no user or system config, so a host hook, signing key or autocrlf cannot change the fixture."""
    keep = ("PATH", "SYSTEMROOT", "TEMP", "TMP", "HOME", "USERPROFILE")
    env = {name: os.environ[name] for name in keep if name in os.environ}
    env.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
                "LC_ALL": "C"})
    return env


def _gm_git(repo: Path, *args: str, when: str = "") -> str:
    """Run git in repo; `when` pins author and committer dates so the fixture's SHAs are the same on every run."""
    env = _gm_env()
    if when:
        env.update({"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when})
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git-merge-conflict received no git on PATH; expected git installed")
    # core.fsmonitor and hooks off: the check runs git in a repo the agent controlled.
    argv = [git, "-c", "core.fsmonitor=false", "-c", "core.hooksPath=" + os.devnull, *args]
    done = subprocess.run(argv, cwd=repo, env=env, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=GM_GIT_LIMIT_S, check=False)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} exited {done.returncode}: {done.stderr.strip()[:200]}; expected 0")
    return done.stdout.strip()


def _gm_commit(repo: Path, files: dict[str, str], message: str, when: str) -> None:
    for rel, text in files.items():
        write(repo, rel, text)
    _gm_git(repo, "add", "--", *files)
    _gm_git(repo, "commit", "-q", "-m", message, when=when)


def _gm_build(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _gm_git(repo, "init", "-q", "-b", "main")
    for key, value in (("user.name", "Drop Game Dev"), ("user.email", "dev@dropgame.invalid"),
                       ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
        _gm_git(repo, "config", key, value)
    _gm_commit(repo, {"README.md": GM_README, "loot.py": GM_BASE_LOOT, "tests/__init__.py": "",
                      "tests/test_loot.py": GM_TEST_LOOT}, "Add loot drops", "2026-03-02T10:00:00+00:00")
    _gm_git(repo, "checkout", "-q", "-b", GM_BRANCH)
    _gm_commit(repo, {"loot.py": GM_EVENT_LOOT, "tests/test_event.py": GM_TEST_EVENT},
               "Weekend event: multiply the rare chance", "2026-03-03T11:00:00+00:00")
    _gm_git(repo, "checkout", "-q", "main")
    _gm_commit(repo, {"loot.py": GM_MAIN_LOOT, "tests/test_pity.py": GM_TEST_PITY},
               "Pity timer: a rare after 10 misses in a row", "2026-03-04T12:00:00+00:00")


@functools.lru_cache(maxsize=1)
def _gm_tips() -> tuple[str, str]:
    """(main tip, branch tip) of a fresh fixture: the dates are pinned, so these are the workspace's SHAs too."""
    with tempfile.TemporaryDirectory(prefix="bench-gm-", dir=scratch_root(), ignore_cleanup_errors=True) as tmp:
        repo = Path(tmp) / GM_REPO
        _gm_build(repo)
        return _gm_git(repo, "rev-parse", "main"), _gm_git(repo, "rev-parse", GM_BRANCH)


def _gm_sha(text: str | None) -> str:
    return hashlib.sha256((text or "").replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _gm_setup(ws: Path) -> None:
    _gm_build(ws / GM_REPO)


def _gm_merge_problem(repo: Path) -> str:
    """Why main does not contain the committed merge of the old main and the branch, or "" when it does."""
    old_main, branch_tip = _gm_tips()
    try:
        # A follow-up commit does not undo the requested committed merge (#164).
        merges = _gm_git(repo, "rev-list", "--parents", "--merges", "main").splitlines()
        dirty = _gm_git(repo, "status", "--porcelain", "--untracked-files=no")
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        return str(error)
    parents = [line.split()[1:] for line in merges]
    if [old_main, branch_tip] not in parents:
        return saw(parents, f"a merge in main's ancestry with parents {[old_main, branch_tip]}")
    if dirty:
        return saw(f"uncommitted changes: {dirty[:120]}", "the resolution committed")
    return ""


def _gm_tracked(repo: Path) -> list[str]:
    try:
        return _gm_git(repo, "ls-files").splitlines()
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        return [path.relative_to(repo).as_posix() for path in repo.rglob("*.py") if ".git" not in path.parts]


def _gm_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    repo = ws / GM_REPO
    # Incoming tests are protected too, including deletion during resolution (#164).
    changed = [rel for rel, text in GM_VISIBLE.items()
               if not (repo / rel).is_file() or _gm_sha(read(repo, rel)) != _gm_sha(text)]
    result.mandatory.append(("visible tests left untouched", not changed))
    if not (repo / ".git").exists():
        result.add("main is a merge commit of the old main and the branch", False, saw("no repo", f"{GM_REPO}/.git"))
    else:
        problem = _gm_merge_problem(repo)
        result.add("main is a merge commit of the old main and the branch", not problem, problem)
    marked = [rel for rel in _gm_tracked(repo) if GM_CONFLICT_MARKER.search(read(repo, rel) or "")]
    result.add("no conflict markers in tracked files", not marked, saw(marked, []))
    with tempfile.TemporaryDirectory(prefix="bench-gm-tree-", dir=scratch_root(), ignore_cleanup_errors=True) as tmp:
        # Local packages and their resources are valid implementations of loot.py (#164).
        if repo.is_dir():
            shutil.copytree(repo, tmp, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
        for label, case in GM_HIDDEN_CASES:
            source = GM_HIDDEN + f"\n\ndef load_tests(loader, tests, pattern):\n    return loader.loadTestsFromTestCase({case})\n"
            ok, why = run_hidden_tests(Path(tmp), source, timeout_s=GM_TEST_LIMIT_S)
            result.add(label, ok, why)
    return result


def _gm_reference(ws: Path) -> list[str]:
    repo = ws / GM_REPO
    subprocess.run([shutil.which("git") or "git", "merge", "--no-edit", GM_BRANCH], cwd=repo, env=_gm_env(),
                   capture_output=True, timeout=GM_GIT_LIMIT_S, check=False)
    write(repo, "loot.py", GM_MERGED_LOOT)
    _gm_git(repo, "add", "loot.py")
    _gm_git(repo, "commit", "-q", "--no-edit")
    return ["merged weekend-event into main, keeping the pity timer and the event multiplier"]


TASKS = [
    EvalTask(
        id="git-merge-conflict", category="engineering",
        provenance="Parallel sessions merging branches in the owner's repos: two features changed the same function",
        summary="Merge a feature branch into main without losing what main shipped meanwhile.",
        setup=_gm_setup, check=_gm_check, reference=_gm_reference, timeout_s=90,
        checkpoints=checkpoints(("merged the branch", r"git\s+(-c\s+\S+\s+)*merge"), ("ran the tests", r"unittest|pytest"),
                                ("committed", r"git\s+(-c\s+\S+\s+)*commit")),
        steps=(Step(f"Our dungeon game's repo is {{WS}}/{GM_REPO}. The {GM_BRANCH} branch has to go into main before the "
                    "event starts, without losing anything main shipped while the branch was open. Commit the merge. The "
                    "tests in tests/ stay as they are."),),
    ),
]
