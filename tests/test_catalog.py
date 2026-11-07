"""Registry discovery."""

import types
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import CheckResult, EvalTask, Step


def task(task_id: str) -> EvalTask:
    return EvalTask(
        id=task_id, category="coding", provenance="test", summary="t",
        setup=lambda ws: None, steps=(Step("x"),), check=lambda ws, a: CheckResult(),
        reference=lambda ws: [],
    )


def test_discovery_runs_on_empty_package() -> None:
    assert isinstance(catalog.all_tasks(), list)


def test_collect_keeps_module_order() -> None:
    mod = types.ModuleType("fake")
    mod.TASKS = [task("a"), task("b")]  # type: ignore[attr-defined]
    assert [t.id for t in catalog.collect([mod])] == ["a", "b"]


def test_catalog_has_no_suites() -> None:
    assert not hasattr(catalog, "select") and not hasattr(catalog, "tasks")


def test_module_without_task_list_is_rejected() -> None:
    mod = types.ModuleType("broken")
    mod.TASKS = "nope"  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="broken"):
        catalog.collect([mod])


def test_duplicate_ids_are_rejected() -> None:
    one, two = types.ModuleType("one"), types.ModuleType("two")
    one.TASKS = [task("dup")]  # type: ignore[attr-defined]
    two.TASKS = [task("dup")]  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="'dup'"):
        catalog.collect([one, two])


def test_limits_fit_the_measured_times_and_pin_the_worst_case() -> None:
    # #98: from 7 to 10 runs. The slowest short eval took 50 s, Mondrian 194 s and 3D 288 s. The worst case applies only
    # when an agent hits every limit; the prompt also asks it to stop polishing once the work is right.
    # #137, bench 2.1: each limit is the slowest finished time in the eight 2.0 runs plus 25%, rounded up to 30 s,
    # at least 60 s, never above 2.0 and never below a limit a 2.0 run hit (rs-lock-bug, Mondrian, word universe).
    # #151, bench 2.2: the three Terminal-Bench ports take the same rule from one Opus 5.5 xhigh probe (31.6 to 46.2 s).
    # #153, bench 2.3: the same rule on the slowest finished probe (Opus 5.5 xhigh, Sonnet 5.5 low): cu-social-cycle
    # 114.0 s, media-voice 28.9 s, cu-webmail 53.7 s, web-fact-search 25.1 s, file-media-edit 51.6 s.
    # #155, bench 2.3.1: the two site tasks take the rule from Sonnet 5.5 low browser-route probes (Claude in Chrome):
    # cu-social-cycle 127.6 and 118.2 s, cu-webmail 128.0 and 126.3 s, so 180 s each and a 62 min worst case.
    # #218, bench 2.8: web-archery-game takes the rule from its Opus 5.5 xhigh probe, 232.7 s -> 300 s; 67 min worst.
    tasks = catalog.all_tasks()
    worst = sum(task.timeout_s * len(task.steps) for task in tasks)
    assert worst == 4020, worst
    assert {task.id: task.timeout_s for task in tasks} == {
        "ds-ab-playtest": 180, "bo-pnl-runway": 150, "bo-reconcile": 90, "cmp-handoff": 90, "cfg-source-drift": 60,
        "doc-lab-pdf": 60, "ds-sql-funnel": 90, "ue-packaged-bug": 90, "git-merge-conflict": 90, "infra-gpu-fit": 60,
        "ir-server-logs": 60, "gd-integration-repo": 150, "rs-lock-bug": 180, "sec-leak-fix": 90,
        "hw-stutter-tuning": 90, "ts-plugin-bug": 60, "web-mondrian-landing": 300, "3d-print-homage": 420,
        "web-plan-ranking": 210, "web-word-universe": 360,
        "txt-regex-log": 60, "ds-sqlite-recover": 60, "py-async-cancel": 60,
        "cu-social-cycle": 180, "media-voice": 60, "cu-webmail": 180, "web-fact-search": 60, "file-media-edit": 90,
        "web-archery-game": 300}


def test_a_run_folder_with_read_only_git_objects_is_removed(tmp_path: Path) -> None:
    # #124: git-merge-conflict leaves .git objects read-only on Windows; rmtree(ignore_errors) kept the run folder.
    import os
    import stat

    from mengine_bench.core import remove_tree

    target = tmp_path / "run" / "dropgame" / ".git" / "objects" / "ab"
    target.mkdir(parents=True)
    (target / "cdef").write_bytes(b"x")
    os.chmod(target / "cdef", stat.S_IREAD)
    remove_tree(tmp_path / "run")
    assert not (tmp_path / "run").exists()
