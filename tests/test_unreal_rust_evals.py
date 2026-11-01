"""#103: the Unreal and Rust evals fail wrong work and accept every valid fix."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import write
from mengine_bench.tasks import gamedev, rust
from mengine_bench.tasks.gamedev import GAME_INI, HEADER, SOURCE, UE_FILES

TRACKER = "	UArenaScoreTracker* ScoreTracker = nullptr;"
PACKAGING_LINE = '+DirectoriesToAlwaysCook=(Path="/Game/Data/Effects")'


def _ue_solved(tmp_path: Path) -> Path:
    gamedev._ue_setup(tmp_path)
    gamedev._ue_reference(tmp_path)
    return tmp_path


def _fixed(ws: Path, rel: str, old: str, new: str) -> None:
    text = (ws / rel).read_text(encoding="utf-8")
    assert old in text, old
    write(ws, rel, text.replace(old, new))


def test_both_evals_are_in_the_catalog_and_the_old_ones_left() -> None:
    ids = {task.id for task in catalog.all_tasks()}
    assert {"ue-packaged-bug", "rs-lock-bug"} <= ids
    assert not {"gd-astar-doors", "gd-ecs-collision-bug"} & ids
    assert len(ids) == 15


@pytest.mark.parametrize("task_id", ["ue-packaged-bug", "rs-lock-bug"])
def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path, task_id: str) -> None:
    task = next(task for task in catalog.all_tasks() if task.id == task_id)
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task.setup(tmp_path / "bare")
    assert not task.check(tmp_path / "bare", [""]).passed
    task.setup(tmp_path / "solved")
    answers = task.reference(tmp_path / "solved")
    result = task.check(tmp_path / "solved", answers)
    assert result.passed, result.failed()


@pytest.mark.parametrize("task_id", ["ue-packaged-bug", "rs-lock-bug"])
def test_the_brief_does_not_hand_over_the_causes(task_id: str) -> None:
    prompt = next(task for task in catalog.all_tasks() if task.id == task_id).steps[0].prompt.lower()
    for word in ("uproperty", "garbage", "alwayscook", "deadlock", "lock order", "lost update"):
        assert word not in prompt, word


# ----------------------------------------------------------------- Unreal --

@pytest.mark.parametrize("fix", [
    "	UPROPERTY()\n	UArenaScoreTracker* ScoreTracker = nullptr;",
    "	UPROPERTY(Transient)\n	TObjectPtr<UArenaScoreTracker> ScoreTracker;",
    "	UPROPERTY(VisibleAnywhere, Category = \"Arena\")\n	TObjectPtr<class UArenaScoreTracker> ScoreTracker = nullptr;",
    "	TStrongObjectPtr<UArenaScoreTracker> ScoreTracker;",
])
def test_every_valid_way_to_keep_the_tracker_alive_passes(tmp_path: Path, fix: str) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, HEADER, UE_FILES[HEADER].replace(TRACKER, fix))
    assert "crash fixed: the score tracker survives garbage collection" not in gamedev._ue_check(ws, [""]).failed()


def test_the_root_set_also_keeps_it_alive(tmp_path: Path) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, HEADER, UE_FILES[HEADER])
    _fixed(ws, SOURCE, "	Stats = new FArenaStats();", "	ScoreTracker->AddToRoot();\n	Stats = new FArenaStats();")
    assert gamedev._ue_check(ws, [""]).passed


@pytest.mark.parametrize("wrong", [
    TRACKER,
    "	// UPROPERTY()\n" + TRACKER,
    "	TWeakObjectPtr<UArenaScoreTracker> ScoreTracker;",
])
def test_wrong_ways_to_keep_the_tracker_fail(tmp_path: Path, wrong: str) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, HEADER, UE_FILES[HEADER].replace(TRACKER, wrong))
    assert "crash fixed: the score tracker survives garbage collection" in gamedev._ue_check(ws, [""]).failed()


def test_reflecting_the_plain_pointer_fails(tmp_path: Path) -> None:
    ws = _ue_solved(tmp_path)
    _fixed(ws, HEADER, "	FArenaStats* Stats = nullptr;", "	UPROPERTY()\n	FArenaStats* Stats = nullptr;")
    assert "the plain C++ pointer stays out of reflection" in gamedev._ue_check(ws, [""]).failed()


@pytest.mark.parametrize("line", [
    '+DirectoriesToAlwaysCook=(Path="/Game/Data/Palettes")',
    '+DirectoriesToAlwaysCook=(Path="/Game/Data/Palettes/")',
    '+DirectoriesToAlwaysCook=(Path="Data/Palettes")',
    '+DirectoriesToAlwaysCook=(Path=/Game/Data/Palettes)',
    '+DirectoriesToAlwaysCook=(Path="/Game/Data")',
])
def test_every_valid_cook_path_passes(tmp_path: Path, line: str) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, GAME_INI, UE_FILES[GAME_INI].replace(PACKAGING_LINE, PACKAGING_LINE + "\n" + line))
    assert "colors fixed: the palette reaches the cook" not in gamedev._ue_check(ws, [""]).failed()


def test_a_hard_reference_from_the_class_also_cooks_it(tmp_path: Path) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, GAME_INI, UE_FILES[GAME_INI])
    _fixed(ws, SOURCE, "void AArenaGameMode::BeginPlay()",
           'AArenaGameMode::AArenaGameMode()\n{\n	static ConstructorHelpers::FObjectFinder<UArenaPalette> Found(TEXT("/Game/Data/Palettes/DA_Primary"));\n}\n\nvoid AArenaGameMode::BeginPlay()')
    assert gamedev._ue_check(ws, [""]).passed


@pytest.mark.parametrize("ini", [
    UE_FILES[GAME_INI],
    UE_FILES[GAME_INI].replace(PACKAGING_LINE, PACKAGING_LINE + '\n+DirectoriesToNeverCook=(Path="/Game/Data/Palettes")'),
    UE_FILES[GAME_INI] + '\n[/Script/EngineSettings.GeneralProjectSettings]\n+DirectoriesToAlwaysCook=(Path="/Game/Data/Palettes")\n',
    UE_FILES[GAME_INI].replace(PACKAGING_LINE, PACKAGING_LINE + '\n;+DirectoriesToAlwaysCook=(Path="/Game/Data/Palettes")'),
])
def test_a_cook_line_in_the_wrong_place_fails(tmp_path: Path, ini: str) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, GAME_INI, ini)
    assert "colors fixed: the palette reaches the cook" in gamedev._ue_check(ws, [""]).failed()


def test_correct_never_reads_the_chat(tmp_path: Path) -> None:
    ws = _ue_solved(tmp_path)
    (ws / "result.json").unlink()
    failed = gamedev._ue_check(ws, ["ScoreTracker has no UPROPERTY and the palette is not cooked"]).failed()
    assert "the report names the crash cause" in failed and "the report names the color cause" in failed


def test_the_report_accepts_other_words(tmp_path: Path) -> None:
    ws = _ue_solved(tmp_path)
    write(ws, "result.json", json.dumps({"crash_cause": "The GC frees the tracker", "no_colors_cause": "DA_Primary never gets packaged"}))
    assert gamedev._ue_check(ws, [""]).passed


# ------------------------------------------------------------------- Rust --

ONE_LOCK = """use std::collections::HashMap;
use std::sync::{Arc, Mutex};

pub type PlayerId = u32;

#[derive(Default)]
struct State {
    scores: HashMap<PlayerId, i64>,
    total: i64,
}

#[derive(Clone, Default)]
pub struct Board {
    state: Arc<Mutex<State>>,
}

impl Board {
    pub fn new() -> Self {
        Self::default()
    }
    pub fn join(&self, id: PlayerId, score: i64) {
        let mut state = self.state.lock().unwrap();
        state.scores.insert(id, score);
        state.total += score;
    }
    pub fn award(&self, id: PlayerId, points: i64) {
        let mut state = self.state.lock().unwrap();
        *state.scores.get_mut(&id).unwrap() += points;
        state.total += points;
    }
    pub fn transfer(&self, from: PlayerId, to: PlayerId, points: i64) {
        let mut state = self.state.lock().unwrap();
        *state.scores.get_mut(&from).unwrap() -= points;
        *state.scores.get_mut(&to).unwrap() += points;
    }
    pub fn score(&self, id: PlayerId) -> i64 {
        self.state.lock().unwrap().scores[&id]
    }
    pub fn total(&self) -> i64 {
        self.state.lock().unwrap().total
    }
}
"""


def _rs_solved(tmp_path: Path) -> Path:
    rust._rs_setup(tmp_path)
    rust._rs_reference(tmp_path)
    return tmp_path


def test_a_different_valid_design_passes(tmp_path: Path) -> None:
    rust._rs_setup(tmp_path)
    write(tmp_path, "src/lib.rs", ONE_LOCK)
    result = rust._rs_check(tmp_path, [""])
    assert result.passed, (result.failed(), result.details)


def test_ordered_locks_without_the_same_player_case_fail_only_that_case(tmp_path: Path) -> None:
    ws = _rs_solved(tmp_path)
    _fixed(ws, "src/lib.rs", "        if from == to {\n            return;\n        }\n", "")
    failed = rust._rs_check(ws, [""]).failed()
    assert failed == ["hidden a transfer to the same player changes nothing"]


def test_the_lost_update_alone_fails_its_case(tmp_path: Path) -> None:
    ws = _rs_solved(tmp_path)
    _fixed(ws, "src/lib.rs", "        *self.total.lock().unwrap() += points;\n    }\n\n    /// Moves",
           "        let total = *self.total.lock().unwrap();\n        std::thread::yield_now();\n        *self.total.lock().unwrap() = total + points;\n    }\n\n    /// Moves")
    assert "hidden awards from many threads all count" in rust._rs_check(ws, [""]).failed()


def test_the_deadlock_fails_within_the_limit_instead_of_hanging(tmp_path: Path) -> None:
    rust._rs_setup(tmp_path)
    assert "hidden opposite transfers do not hang" in rust._rs_check(tmp_path, [""]).failed()


def test_a_broken_build_earns_nothing_and_says_why(tmp_path: Path) -> None:
    ws = _rs_solved(tmp_path)
    write(ws, "src/lib.rs", "this is not rust\n")
    result = rust._rs_check(ws, [""])
    assert result.score == 0.0
    assert "error" in result.details["hidden clones share the scores"]


def test_editing_the_visible_tests_earns_nothing(tmp_path: Path) -> None:
    ws = _rs_solved(tmp_path)
    write(ws, "tests/board.rs", "")
    result = rust._rs_check(ws, [""])
    assert not result.mandatory_ok and result.score == 0


def test_a_new_dependency_earns_nothing(tmp_path: Path) -> None:
    ws = _rs_solved(tmp_path)
    write(ws, "Cargo.toml", rust.CARGO_TOML + 'parking_lot = "0.12"\n')
    assert not rust._rs_check(ws, [""]).mandatory_ok


def test_a_cargo_target_folder_stays_out_of_the_judge_view(tmp_path: Path) -> None:
    from mengine_bench.runner.task_run import snapshot
    write(tmp_path, "src/lib.rs", "x")
    write(tmp_path, "target/debug/huge.bin", "x")
    assert set(snapshot(tmp_path)) == {"src/lib.rs"}
