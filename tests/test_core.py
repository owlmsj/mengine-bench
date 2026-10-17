"""Task contract ported from the private suite."""

from pathlib import Path

import pytest

from mengine_bench.core import (
    FAST,
    FULL,
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
        id="demo", category="coding", suites=frozenset({FAST, FULL}), provenance="test",
        summary="demo", setup=lambda ws: None, steps=(Step("do it"),),
        check=lambda ws, answers: CheckResult(), reference=lambda ws: [], par_s=60.0,
    )
    base.update(overrides)
    return EvalTask(**base)  # type: ignore[arg-type]


def test_task_defaults_weight_one() -> None:
    task = make_task()
    assert task.weight == 1 and task.par_s == 60.0


def test_task_rejects_unknown_suite() -> None:
    with pytest.raises(ValueError, match="agentic"):
        make_task(suites=frozenset({"agentic"}))


def test_task_rejects_bad_weight_and_par() -> None:
    with pytest.raises(ValueError, match="weight 3"):
        make_task(weight=3)
    with pytest.raises(ValueError, match="par_s 0"):
        make_task(par_s=0)


def test_task_requires_steps() -> None:
    with pytest.raises(ValueError, match="no steps"):
        make_task(steps=())


def test_check_result_mandatory_gates_pass() -> None:
    result = CheckResult(mandatory=[("render", False)])
    result.add("a", True)
    assert result.score == 1.0 and not result.passed and not result.mandatory_ok
    assert result.failed() == ["render"]


def test_check_result_pass_ratio() -> None:
    result = CheckResult(pass_ratio=0.5)
    result.add("a", True)
    result.add("b", False)
    assert result.passed


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
