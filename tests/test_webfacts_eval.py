"""#153: web-fact-search grades three pinned facts offline: exact value, primary-source domain, any writing."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import CheckResult, ToolCall, write
from mengine_bench.tasks.webfacts import WEB_FACTS
from mengine_bench.runner.trace import url_key

TASK = next(task for task in catalog.all_tasks() if task.id == "web-fact-search")


def _check(ws: Path, answers: list[str]) -> CheckResult:
    entries = json.loads((ws / "result.json").read_text(encoding="utf-8")) if (ws / "result.json").exists() else {}
    trace = [ToolCall("WebFetch", {"url": entry.get("url")}) for entry in entries.values()]
    return TASK.check(ws, answers, trace)


def _solved(ws: Path) -> Path:
    ws.mkdir(parents=True, exist_ok=True)
    TASK.setup(ws)
    TASK.reference(ws)
    return ws


def _set(ws: Path, key: str, field: str, value: object) -> None:
    got = json.loads((ws / "result.json").read_text(encoding="utf-8"))
    got[key][field] = value
    write(ws, "result.json", json.dumps(got))


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    ws = _solved(tmp_path / "solved")
    assert _check(ws, ["done"]).passed
    assert TASK.check(ws, TASK.reference(ws)).passed
    (tmp_path / "bare").mkdir()
    TASK.setup(tmp_path / "bare")
    bare = _check(tmp_path / "bare", [""])
    assert bare.score == 0.0 and len(bare.checks) == 2 * len(WEB_FACTS) + 1


@pytest.mark.parametrize(("key", "value", "url"), [
    ("sqlite_3_40_0_release_date", "November 16, 2022", "https://sqlite.org/releaselog/3_40_0.html"),
    ("sqlite_3_40_0_release_date", "16/11/2022", "http://www.sqlite.org/changes.html#version_3_40_0"),
    ("postgresql_15_0_release_date", "2022-10-13T00:00:00Z", "https://www.postgresql.org/about/news/postgresql-15-released-2526/"),
    ("unicode_15_0_characters_added", "4,489", "https://unicode.org/versions/Unicode15.0.0/"),
    ("unicode_15_0_characters_added", "4489 characters", "https://www.unicode.org/L2/L2022/"),
])
def test_other_writings_and_other_pages_of_the_same_site_pass(tmp_path: Path, key: str, value: str, url: str) -> None:
    ws = _solved(tmp_path)
    _set(ws, key, "value", value)
    _set(ws, key, "url", url)
    assert _check(ws, [""]).passed


@pytest.mark.parametrize(("key", "field", "bad", "check"), [
    # 3.40.1, the patch release a careless search lands on.
    ("sqlite_3_40_0_release_date", "value", "2022-12-28", "sqlite_3_40_0_release_date value"),
    # The beta 1 announcement date.
    ("postgresql_15_0_release_date", "value", "2022-05-19", "postgresql_15_0_release_date value"),
    # The total in Unicode 15.0, not the characters it added.
    ("unicode_15_0_characters_added", "value", 149186, "unicode_15_0_characters_added value"),
    ("unicode_15_0_characters_added", "value", "4489 or 4193", "unicode_15_0_characters_added value"),
    ("sqlite_3_40_0_release_date", "url", "https://en.wikipedia.org/wiki/SQLite", "sqlite_3_40_0_release_date primary source"),
    ("postgresql_15_0_release_date", "url", "https://postgresql.org.example.com/15", "postgresql_15_0_release_date primary source"),
    ("unicode_15_0_characters_added", "url", "unicode.org", "unicode_15_0_characters_added primary source"),
])
def test_each_wrong_fact_or_source_fails_only_its_check(tmp_path: Path, key: str, field: str, bad: object, check: str) -> None:
    ws = _solved(tmp_path)
    _set(ws, key, field, bad)
    result = _check(ws, [""])
    expected = [check] + (["cited primary sources were fetched"] if field == "url" and not url_key(bad) else [])
    assert result.failed() == expected and check in result.details


def test_the_brief_asks_for_the_web_and_hands_over_no_answer() -> None:
    prompt = TASK.steps[0].prompt
    assert "open web" in prompt and "web" in TASK.needs
    for fact in WEB_FACTS:
        assert fact.key in prompt
        assert str(fact.answer) not in prompt and fact.source not in prompt


def test_a_correct_answer_in_the_chat_alone_earns_nothing(tmp_path: Path) -> None:
    ws = _solved(tmp_path / "ref")
    answer = (ws / "result.json").read_text(encoding="utf-8")
    (tmp_path / "chat").mkdir()
    assert _check(tmp_path / "chat", [answer]).score == 0.0


def test_memory_only_result_no_longer_passes(tmp_path: Path) -> None:
    # #164: Opus wrote the right facts and primary URLs with only a heredoc, no fetch.
    result = TASK.check(_solved(tmp_path), ["done"])
    assert not result.passed
    assert "cited primary sources were fetched" in result.failed()


def test_fetching_a_different_page_on_the_same_host_is_sufficient(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    trace = [ToolCall("WebFetch", {"url": fact.source}) for fact in WEB_FACTS]
    trace[0] = ToolCall("WebFetch", {"url": "https://sqlite.org/index.html"})
    assert TASK.check(ws, [], trace).passed


def test_runner_recovers_codex_python_fetch_script(tmp_path: Path) -> None:
    from mengine_bench.runner import task_run

    ws = _solved(tmp_path)
    script = "import urllib.request\n" + "\n".join(f"urllib.request.urlopen({fact.source!r})" for fact in WEB_FACTS)
    (ws / "lookup.py").write_text(script, encoding="utf-8")
    events = [
        {"type": "item.completed", "item": {"type": "file_change", "status": "completed", "changes": [{"path": "lookup.py", "kind": "add"}]}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python ./lookup.py", "exit_code": 0, "status": "completed"}},
    ]
    record = task_run.TaskRunRecord(TASK.id, workspace=ws, answers=["done"], streams=["\n".join(map(json.dumps, events))])
    task_run._grade(TASK, record)
    assert record.check is not None and record.check.passed, record.check
