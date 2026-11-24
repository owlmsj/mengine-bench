"""Regression tests for OpenCode 2.3.2 `background_wait` handling (#314)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from mengine_bench.runner.agents import OpencodeAgent
from mengine_bench.runner.process import run_process

TEXT_EVENT = json.dumps({"type": "text", "sessionID": "ses_1", "part": {"text": "done"}})
STEP_FINISH_STOP = json.dumps({"type": "step_finish", "sessionID": "ses_1", "part": {"reason": "stop"}})
BACKGROUND_WAIT = json.dumps({
    "type": "background_wait",
    "timestamp": 1795553194332,
    "sessionID": "ses_1",
    "jobs": [{"id": "sh_1", "kind": "shell", "title": 'cd "<WORKSPACE>" && python bench.py'}],
})
STEP_START = json.dumps({"type": "step_start", "sessionID": "ses_1", "part": {}})


def _script(body: str) -> list[str]:
    return [sys.executable, "-c", body]


def test_opencode_background_wait_stops_after_grace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MENGINE_BENCH_BACKGROUND_GRACE_S", "1")
    call = OpencodeAgent("m", None).invocation("prompt", tmp_path / "p.md", tmp_path, ())
    argv = _script(
        f"import time\n"
        f"for line in ({TEXT_EVENT!r}, {STEP_FINISH_STOP!r}, {BACKGROUND_WAIT!r}):\n"
        f"    print(line, flush=True)\n"
        f"time.sleep(60)\n"
    )
    result = run_process(argv, tmp_path, timeout_s=5, final_event=call.final_event)
    assert result.timed_out is False
    assert result.stopped_after_final is True
    assert result.exit_code == 0
    assert result.wall_s < 4


def test_opencode_background_wait_resets_when_agent_resumes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MENGINE_BENCH_BACKGROUND_GRACE_S", "1")
    call = OpencodeAgent("m", None).invocation("prompt", tmp_path / "p.md", tmp_path, ())
    argv = _script(
        f"import time\n"
        f"print({BACKGROUND_WAIT!r}, flush=True)\n"
        f"time.sleep(0.3)\n"
        f"for line in ({STEP_START!r}, {TEXT_EVENT!r}, {STEP_FINISH_STOP!r}):\n"
        f"    print(line, flush=True)\n"
        f"time.sleep(1.3)\n"
    )
    result = run_process(argv, tmp_path, timeout_s=10, final_event=call.final_event)
    assert result.timed_out is False
    assert result.stopped_after_final is False
    assert result.exit_code == 0
    assert result.wall_s >= 1.5
