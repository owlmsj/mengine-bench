"""Fake agents for runner tests: tiny Python scripts driven through the `cmd` adapter."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

FakeAgent = Callable[[str, str], str]


@pytest.fixture(autouse=True)
def isolated_preflight(monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory) -> None:
    """The real preflight reads this machine's home and temp dir; runner tests
    must not depend on them (tests/test_preflight.py covers it with fakes)."""
    from mengine_bench import cli
    from mengine_bench.runner import task_run
    monkeypatch.setattr(cli, "personal_instructions", lambda *args, **kwargs: [])
    monkeypatch.setattr(cli, "blocking_problems", lambda *args, **kwargs: [])
    monkeypatch.setenv("MENGINE_BENCH_SCRATCH", str(tmp_path_factory.mktemp("scratch")))
    # Grading runs a page in a real browser (#82); tests/test_page_checks.py covers it with fakes.
    monkeypatch.setattr(task_run, "add_page_checks", lambda result, html: None)


@pytest.fixture
def fake_agent(tmp_path: Path) -> FakeAgent:
    """Write `body` as a script; return a JSON argv template for CmdAgent.

    The script receives argv[1] = workspace and argv[2] = prompt file.
    """

    def build(name: str, body: str) -> str:
        script = tmp_path / "fakes" / f"{name}.py"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text(body, encoding="utf-8")
        return json.dumps([sys.executable, "-I", str(script), "{workspace}", "{prompt_file}"])

    return build
