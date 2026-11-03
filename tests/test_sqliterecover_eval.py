"""#151: ds-sqlite-recover passes any reader that gets the rows back and fails one that misses a storage form."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import EvalTask, write
from mengine_bench.tasks.sqliterecover import SR_DB_FILE, SR_OUT_FILE, SR_ROWS, _sr_check, _sr_setup, sr_build_page

SHAPE = f"{SR_OUT_FILE} is a list of item and price rows"
WHOLE = "rows stored as whole numbers recovered"
FRACTION = "rows with fractional prices recovered"
CONSTANT = "rows stored as the constants 0 and 1 recovered"
REAL_ONLY = "no row that is not in the table"


def _task() -> EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == "ds-sqlite-recover")


def _deliver(tmp_path: Path, rows: object) -> list[str]:
    _sr_setup(tmp_path)
    write(tmp_path, SR_OUT_FILE, json.dumps(rows))
    return _sr_check(tmp_path, [""]).failed()


def _all() -> list[dict[str, object]]:
    return [{"item": item, "price": price} for item, price in SR_ROWS]


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    task = _task()
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task.setup(tmp_path / "bare")
    bare = task.check(tmp_path / "bare", [""])
    assert not bare.passed and set(bare.failed()) == {SHAPE, WHOLE, FRACTION, CONSTANT, REAL_ONLY}
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)


def test_the_file_is_the_leaf_page_alone_and_sqlite_cannot_open_it(tmp_path: Path) -> None:
    _sr_setup(tmp_path)
    data = (tmp_path / SR_DB_FILE).read_bytes()
    assert data == sr_build_page() and data[0] == 0x0D and not data.startswith(b"SQLite format 3")
    con = sqlite3.connect(tmp_path / SR_DB_FILE)
    try:
        with pytest.raises(sqlite3.DatabaseError):
            con.execute("SELECT name FROM sqlite_master").fetchall()
    finally:
        con.close()


def test_the_page_holds_every_storage_form_the_checks_name() -> None:
    # Serial types 8 and 9 (0 and 1, no value bytes), 1 (int8), 2 (int16) and 7 (double), next to the item names.
    data = sr_build_page()
    for item, serial in (("trail map", 8), ("matchbox", 9), ("lantern", 1), ("camp stove", 2), ("compass", 7)):
        name = item.encode()
        at = data.index(name)
        assert data[at - 1] == serial, (item, data[at - 3:at])


def test_any_key_order_strings_and_duplicates_still_pass(tmp_path: Path) -> None:
    rows = [{"price": str(price), "item": item} for item, price in reversed(SR_ROWS)]
    assert _deliver(tmp_path, rows + rows[:2]) == []


@pytest.mark.parametrize(("rows", "lost"), [
    # A carver that only decodes 8-byte doubles.
    ([row for row in _all() if row["price"] != int(row["price"])], [WHOLE, CONSTANT]),
    # One that reads a value byte after every name, so 0 and 1 come out as the next cell's first byte.
    ([*(row for row in _all() if row["item"] not in {"trail map", "matchbox"}),
      {"item": "trail map", "price": 14}, {"item": "matchbox", "price": 13}], [CONSTANT, REAL_ONLY]),
    # One that skips the constant rows.
    ([row for row in _all() if row["item"] not in {"trail map", "matchbox"}], [CONSTANT]),
    # All the rows plus carved garbage.
    ([*_all(), {"item": "\u0003!\u0001", "price": 7}], [REAL_ONLY]),
    ({"rows": _all()}, [SHAPE, WHOLE, FRACTION, CONSTANT, REAL_ONLY]),
])
def test_a_recovery_that_misses_a_storage_form_fails_that_check(tmp_path: Path, rows: object, lost: list[str]) -> None:
    assert _deliver(tmp_path, rows) == lost


def test_the_rows_are_not_upstream() -> None:
    assert not any("testword" in item for item, _ in SR_ROWS)


def test_the_brief_does_not_hand_over_the_method() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("header", "page", "varint", "serial", "cell", "b-tree", "hex"):
        assert word not in prompt, word
