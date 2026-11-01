"""Rust: a shared board that hangs under load and loses points (#103).

The agent edits a real crate and runs cargo. The gold builds a copy of the crate with hidden tests it never saw,
so any lock design that keeps the public API passes: one lock for all, ordered locks or atomics.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, read, scratch_root, write

CARGO_TOML = """[package]
name = "arena_scores"
version = "0.1.0"
edition = "2021"

[dependencies]
"""

LIB = """//! Player scores shared between the match threads of the Pixel Arena server.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

pub type PlayerId = u32;

/// Clones share the same scores, so each match thread keeps its own handle.
#[derive(Clone, Default)]
pub struct Board {
    players: Arc<Mutex<HashMap<PlayerId, Arc<Mutex<i64>>>>>,
    total: Arc<Mutex<i64>>,
}

impl Board {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn join(&self, id: PlayerId, score: i64) {
        self.players.lock().unwrap().insert(id, Arc::new(Mutex::new(score)));
        *self.total.lock().unwrap() += score;
    }

    fn slot(&self, id: PlayerId) -> Arc<Mutex<i64>> {
        self.players.lock().unwrap()[&id].clone()
    }

    /// Adds points to a player and to the board total.
    pub fn award(&self, id: PlayerId, points: i64) {
        let slot = self.slot(id);
        let score = *slot.lock().unwrap();
        *slot.lock().unwrap() = score + points;
        let total = *self.total.lock().unwrap();
        *self.total.lock().unwrap() = total + points;
    }

    /// Moves points between two players. The board total does not change.
    /// Moving points from a player to the same player changes nothing.
    pub fn transfer(&self, from: PlayerId, to: PlayerId, points: i64) {
        let from_slot = self.slot(from);
        let to_slot = self.slot(to);
        let mut from_score = from_slot.lock().unwrap();
        let mut to_score = to_slot.lock().unwrap();
        *from_score -= points;
        *to_score += points;
    }

    pub fn score(&self, id: PlayerId) -> i64 {
        *self.slot(id).lock().unwrap()
    }

    pub fn total(&self) -> i64 {
        *self.total.lock().unwrap()
    }
}
"""

VISIBLE = """use arena_scores::Board;

#[test]
fn one_thread_keeps_the_scores() {
    let board = Board::new();
    board.join(1, 10);
    board.join(2, 0);
    board.award(1, 5);
    board.transfer(1, 2, 3);
    assert_eq!((board.score(1), board.score(2), board.total()), (12, 3, 15));
}
"""

HIDDEN = """use arena_scores::Board;
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

/// A deadlock must fail its test, not hang the whole run.
fn within_limit(work: impl FnOnce() + Send + 'static) -> bool {
    let (done, finished) = mpsc::channel();
    thread::spawn(move || {
        work();
        let _ = done.send(());
    });
    finished.recv_timeout(Duration::from_secs(20)).is_ok()
}

#[test]
fn awards_from_many_threads_all_count() {
    let board = Board::new();
    board.join(1, 0);
    let check = board.clone();
    assert!(within_limit(move || {
        let workers: Vec<_> = (0..8)
            .map(|_| {
                let board = board.clone();
                thread::spawn(move || (0..20_000).for_each(|_| board.award(1, 1)))
            })
            .collect();
        workers.into_iter().for_each(|worker| worker.join().unwrap());
    }));
    assert_eq!((check.score(1), check.total()), (160_000, 160_000));
}

#[test]
fn opposite_transfers_do_not_hang() {
    let board = Board::new();
    board.join(1, 1_000);
    board.join(2, 1_000);
    let check = board.clone();
    assert!(within_limit(move || {
        let workers: Vec<_> = [(1, 2), (2, 1), (1, 2), (2, 1)]
            .into_iter()
            .map(|(from, to)| {
                let board = board.clone();
                thread::spawn(move || (0..20_000).for_each(|_| board.transfer(from, to, 1)))
            })
            .collect();
        workers.into_iter().for_each(|worker| worker.join().unwrap());
    }));
    assert_eq!((check.score(1), check.score(2), check.total()), (1_000, 1_000, 2_000));
}

#[test]
fn a_transfer_to_the_same_player_changes_nothing() {
    let board = Board::new();
    board.join(7, 40);
    let check = board.clone();
    assert!(within_limit(move || board.transfer(7, 7, 5)));
    assert_eq!((check.score(7), check.total()), (40, 40));
}

#[test]
fn clones_share_the_scores() {
    let board = Board::new();
    board.join(1, 1);
    board.clone().award(1, 2);
    assert_eq!((board.score(1), board.total()), (3, 3));
}
"""

HIDDEN_CASES = (("awards from many threads all count", "awards_from_many_threads_all_count"),
                ("opposite transfers do not hang", "opposite_transfers_do_not_hang"),
                ("a transfer to the same player changes nothing", "a_transfer_to_the_same_player_changes_nothing"),
                ("clones share the scores", "clones_share_the_scores"))
RS_FILES = {"Cargo.toml": CARGO_TOML, "src/lib.rs": LIB, "tests/board.rs": VISIBLE}
CARGO_LIMIT_S = 180


def _sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _rs_setup(ws: Path) -> None:
    for rel, text in RS_FILES.items():
        write(ws, rel, text)


def run_cargo_hidden(ws: Path) -> tuple[dict[str, bool], str]:
    """Each hidden test's result in a copy of the crate, and why the build failed when it did.

    Only the manifest and the sources are copied: the agent's own tests and any target folder do not count.
    """
    cargo = shutil.which("cargo")
    if cargo is None:
        return {}, "cargo not found; expected the Rust toolchain on PATH"
    with tempfile.TemporaryDirectory(prefix="bench-cargo-", dir=scratch_root(), ignore_cleanup_errors=True) as tmp:
        crate = Path(tmp)
        (crate / "Cargo.toml").write_bytes((ws / "Cargo.toml").read_bytes())
        shutil.copytree(ws / "src", crate / "src")
        write(crate, "tests/hidden_gold.rs", HIDDEN)
        env = {**os.environ, "CARGO_TARGET_DIR": str(crate / "target"), "CARGO_TERM_COLOR": "never"}
        try:
            done = subprocess.run([cargo, "test", "--offline", "--test", "hidden_gold"], cwd=crate, env=env, capture_output=True,
                                  text=True, encoding="utf-8", errors="replace", timeout=CARGO_LIMIT_S, check=False)
        except subprocess.TimeoutExpired:
            return {}, f"cargo test exceeded {CARGO_LIMIT_S}s"
    passed = {name: outcome == "ok" for name, outcome in re.findall(r"^test (\w+) \.\.\. (\w+)", done.stdout, re.MULTILINE)}
    errors = [line for line in done.stderr.splitlines() if line.startswith("error")]
    return passed, " | ".join(errors[:3]) or done.stderr[-200:]


def _rs_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    untouched = _sha(read(ws, "tests/board.rs") or "") == _sha(VISIBLE)
    result.mandatory.append(("visible tests left untouched", untouched))
    manifest = read(ws, "Cargo.toml") or ""
    dependencies = re.search(r"^\[(?:[\w-]*-)?dependencies\][^\[]*", manifest, re.MULTILINE)
    no_new = dependencies is None or not re.sub(r"\[.*?\]", "", dependencies.group(0)).strip()
    result.mandatory.append(("no new dependencies", no_new))
    passed, why = run_cargo_hidden(ws) if (ws / "Cargo.toml").is_file() and (ws / "src").is_dir() else ({}, "the crate is gone")
    for label, test in HIDDEN_CASES:
        result.add(f"hidden {label}", passed.get(test, False), why if not passed else f"{test} failed")
    return result


def _rs_reference(ws: Path) -> list[str]:
    fixed = LIB.replace("""        let slot = self.slot(id);
        let score = *slot.lock().unwrap();
        *slot.lock().unwrap() = score + points;
        let total = *self.total.lock().unwrap();
        *self.total.lock().unwrap() = total + points;
""", """        *self.slot(id).lock().unwrap() += points;
        *self.total.lock().unwrap() += points;
""").replace("""        let from_slot = self.slot(from);
        let to_slot = self.slot(to);
        let mut from_score = from_slot.lock().unwrap();
        let mut to_score = to_slot.lock().unwrap();
        *from_score -= points;
        *to_score += points;
""", """        if from == to {
            return;
        }
        // One order for every thread, so two opposite transfers cannot wait on each other.
        let (first, second, moved) = if from < to { (from, to, -points) } else { (to, from, points) };
        let first_slot = self.slot(first);
        let second_slot = self.slot(second);
        let mut first_score = first_slot.lock().unwrap();
        let mut second_score = second_slot.lock().unwrap();
        *first_score += moved;
        *second_score -= moved;
""")
    write(ws, "src/lib.rs", fixed)
    return ["locks taken in one order, and each update under one lock"]


TASKS = [
    EvalTask(
        id="rs-lock-bug", category="engineering",
        provenance="Real Rust work: lock order and a lost update in shared state; hidden cargo tests, any lock design passes",
        summary="Find out why a Rust game server hangs under load and loses points, and fix it.",
        setup=_rs_setup, check=_rs_check, reference=_rs_reference, timeout_s=180,
        checkpoints=checkpoints(("read the crate", r"lib\.rs"), ("ran the tests", r"cargo\s+(\+\S+\s+)?test")),
        steps=(Step("The match server of our game hangs under load, and the final scores come out low. The score board is the "
                    "crate in {WS}. Find out why and fix it. Its public API stays as it is, the tests in {WS}/tests stay as they "
                    "are, and the crate takes no new dependencies."),),
    ),
]
