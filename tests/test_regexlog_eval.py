"""#151: txt-regex-log passes a right regex written any way and fails one that takes a shortcut on any trap."""

from __future__ import annotations

from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import EvalTask, write
from mengine_bench.tasks.regexlog import _RL_ADDRESS, RL_GROUPS, RL_PATTERN_FILE, RL_REFERENCE_REGEX, _rl_check, _rl_setup

LAST = "the last date on each line with an address"
NO_ADDRESS = "lines without a valid address match nothing"
BAD_DATE = "impossible dates match nothing"
GLUED = "dates glued to letters or digits match nothing"

# The upstream solution's regex: its edge class [^0-9A-Za-z] also takes a newline, so a line with no address borrows
# the address that starts the next line.
UPSTREAM_SHAPE = (r"(?=.*(?:^|[^0-9A-Za-z])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)"
                  r"(?=$|[^0-9A-Za-z])).*(?:^|[^0-9A-Za-z])(\d{4}-(?:(?:01|03|05|07|08|10|12)-(?:0[1-9]|[12]\d|3[01])"
                  r"|(?:04|06|09|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|1\d|2[0-9])))(?=$|[^0-9A-Za-z])")
# The same construction kept to one line, with upstream's octet 1?\d?\d (it takes 01) made strict: another valid route.
PER_LINE_SHAPE = "^" + UPSTREAM_SHAPE.replace("[^0-9A-Za-z]", r"[^0-9A-Za-z\n]").replace(r"1?\d?\d", r"1\d\d|[1-9]?\d")
FIRST_DATE = RL_REFERENCE_REGEX.replace(r")[^\n]*(?<!", r")[^\n]*?(?<!", 1)
ANY_DATE = RL_REFERENCE_REGEX.replace(r"(\d{4}-(?:", r"(\d{4}-(?:\d\d-\d\d|", 1)
LOOSE_ADDRESS = RL_REFERENCE_REGEX.replace(_RL_ADDRESS, r"\d+\.\d+\.\d+\.\d+")
# #164: the reference with octets that take a leading zero; the brief rules 01.2.3.4 out.
LEADING_ZERO = RL_REFERENCE_REGEX.replace(r"1\d\d|[1-9]?\d)", r"1\d\d|[01]?\d?\d)")
WORD_EDGES = r"^(?=[^\n]*\b(?:\d{1,3}\.){3}\d{1,3}\b)[^\n]*\b(\d{4}-\d\d-\d\d)\b"


def _task() -> EvalTask:
    return next(task for task in catalog.all_tasks() if task.id == "txt-regex-log")


def _with(tmp_path: Path, pattern: str) -> list[str]:
    _rl_setup(tmp_path)
    write(tmp_path, RL_PATTERN_FILE, pattern + "\n")
    return _rl_check(tmp_path, [""]).failed()


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    task = _task()
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    task.setup(tmp_path / "bare")
    bare = task.check(tmp_path / "bare", [""])
    assert not bare.passed and set(bare.failed()) == {LAST, NO_ADDRESS, BAD_DATE, GLUED}
    task.setup(tmp_path / "solved")
    result = task.check(tmp_path / "solved", task.reference(tmp_path / "solved"))
    assert result.passed, (result.failed(), result.details)


def test_every_group_holds_lines_that_match_and_lines_that_do_not() -> None:
    # A regex that matches nothing must fail every check.
    for label, rows in RL_GROUPS:
        dates = [date for _, date in rows]
        assert any(dates) and None in dates, label


def test_another_construction_passes(tmp_path: Path) -> None:
    assert _with(tmp_path, PER_LINE_SHAPE) == []


def test_the_upstream_regex_leaks_into_the_next_line(tmp_path: Path) -> None:
    assert _with(tmp_path, UPSTREAM_SHAPE) == [NO_ADDRESS]


@pytest.mark.parametrize(("pattern", "lost"), [
    (FIRST_DATE, [LAST]),
    (ANY_DATE, [BAD_DATE]),
    (LOOSE_ADDRESS, [NO_ADDRESS]),
    (LEADING_ZERO, [NO_ADDRESS]),
    (WORD_EDGES, [NO_ADDRESS, BAD_DATE]),
    (r"(?!)", [LAST, NO_ADDRESS, BAD_DATE, GLUED]),
    (r"(\d{4}-\d\d-\d\d", [LAST, NO_ADDRESS, BAD_DATE, GLUED]),
])
def test_a_regex_that_skips_a_trap_fails_that_check(tmp_path: Path, pattern: str, lost: list[str]) -> None:
    assert _with(tmp_path, pattern) == lost


def test_the_hidden_lines_are_not_the_sample_or_upstream() -> None:
    hidden = {line for _, rows in RL_GROUPS for line, _ in rows}
    assert not any("192.168.0.1" in line or "testword" in line for line in hidden)


def test_the_brief_does_not_hand_over_the_method() -> None:
    prompt = _task().steps[0].prompt.lower()
    for word in ("lookahead", "lookbehind", "greedy", "(?=", "\\b"):
        assert word not in prompt, word
