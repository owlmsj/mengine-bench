"""Task contract ported from the private suite."""

from pathlib import Path

import pytest

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    answer_json,
    close,
    has,
    read,
    read_json,
    run_hidden_tests,
    write,
)


def make_task(**overrides: object) -> EvalTask:
    base: dict[str, object] = dict(
        id="demo", category="coding", provenance="test",
        summary="demo", setup=lambda ws: None, steps=(Step("do it"),),
        check=lambda ws, answers: CheckResult(), reference=lambda ws: [],
    )
    base.update(overrides)
    return EvalTask(**base)  # type: ignore[arg-type]


def test_task_has_no_suite_weight_or_par_and_no_deliverables_by_default() -> None:
    task = make_task()
    assert task.deliverables == ()
    for removed in ("suites", "weight", "par_s"):
        assert not hasattr(task, removed)
    with pytest.raises(TypeError):
        make_task(weight=2)


def test_task_keeps_declared_deliverables() -> None:
    assert make_task(deliverables=("site/index.html",)).deliverables == ("site/index.html",)


def test_task_requires_steps() -> None:
    with pytest.raises(ValueError, match="no steps"):
        make_task(steps=())


def test_failed_mandatory_gate_zeroes_the_score() -> None:
    # #23: a failed gate used to keep up to 0.5; now the task scores 0.
    result = CheckResult(mandatory=[("render", False)])
    result.add("a", True)
    assert result.score == 0.0 and not result.passed and not result.mandatory_ok
    assert result.failed() == ["render"]


def test_check_result_passes_only_with_every_check() -> None:
    result = CheckResult(mandatory=[("gate", True)])
    result.add("a", True)
    result.add("b", False)
    assert result.score == 0.5 and not result.passed
    assert not hasattr(result, "pass_ratio")


def test_file_helpers(tmp_path: Path) -> None:
    write(tmp_path, "a/b.json", '{"x": 1}')
    assert read(tmp_path, "a/b.json") == '{"x": 1}'
    assert read_json(tmp_path, "a/b.json") == {"x": 1}
    assert read(tmp_path, "missing") is None
    write(tmp_path, "bad.json", "{")
    assert read_json(tmp_path, "bad.json") is None


def test_close_and_has() -> None:
    assert close("3,14", 3.14) and not close("x", 1.0) and not close("nan", 1.0)
    assert has("Hello\nWorld", "hello.world") and not has(None, "x")


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig"])
@pytest.mark.parametrize("text,expected", [('{"x": 1}', {"x": 1}), ("{", None)])
def test_file_helpers_accept_bom_without_accepting_invalid_json(
    tmp_path: Path, encoding: str, text: str, expected: object,
) -> None:
    (tmp_path / "answer.json").write_text(text, encoding=encoding)
    assert read(tmp_path, "answer.json") == text
    assert read_json(tmp_path, "answer.json") == expected
    (tmp_path / "answer.csv").write_text("name,count\nplayer,1\n", encoding=encoding)
    assert read(tmp_path, "answer.csv") == "name,count\nplayer,1\n"


def test_answer_json_takes_last_top_level_object() -> None:
    text = 'first {"a": 1} then ```{"b": {"c": 2}}```'
    assert answer_json([text]) == {"b": {"c": 2}}
    assert answer_json([]) == {}


def test_run_hidden_tests(tmp_path: Path) -> None:
    write(tmp_path, "mod.py", "def f():\n    return 2\n")
    gold = (
        "import unittest, mod\n"
        "class T(unittest.TestCase):\n"
        "    def test(self):\n"
        "        self.assertEqual(mod.f(), {})\n"
    )
    ok, _ = run_hidden_tests(tmp_path, gold.format(2))
    bad, _ = run_hidden_tests(tmp_path, gold.format(3))
    assert ok and not bad
