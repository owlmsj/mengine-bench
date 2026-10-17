"""Fake agents for runner tests: tiny Python scripts driven through the `cmd` adapter."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

FakeAgent = Callable[[str, str], str]


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
