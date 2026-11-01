"""Timeouts kill the whole agent process tree, grandchildren included."""

from __future__ import annotations

import gzip
import json
import sys
import time
from pathlib import Path

import psutil
import pytest

from conftest import FakeAgent
from mengine_bench.runner.agents import AgyAgent, ClaudeAgent, CmdAgent
from mengine_bench.runner.process import run_process

SPAWNER = """
import subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
Path(sys.argv[1], "grandchild.pid").write_text(str(child.pid))
time.sleep(120)
"""


def test_timeout_kills_child_and_grandchild(fake_agent: FakeAgent, tmp_path: Path) -> None:
    agent = CmdAgent(template=fake_agent("spawner", SPAWNER), model="m", effort=None)
    ws = tmp_path / "ws"
    ws.mkdir()
    call = agent.invocation("p", tmp_path / "p.md", ws, ())
    started = time.monotonic()
    result = run_process(call.argv, ws, timeout_s=3, stdin_text=call.stdin_text)
    assert result.timed_out and time.monotonic() - started < 30
    pid_file = ws / "grandchild.pid"
    assert pid_file.is_file(), "fake agent never spawned its grandchild"
    grandchild = int(pid_file.read_text())
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and _alive(grandchild):
        time.sleep(0.1)
    assert not _alive(grandchild), "grandchild survived the timeout"


def test_completed_process_captures_output_and_exit(tmp_path: Path) -> None:
    # Agents speak UTF-8 on both pipes regardless of the host code page.
    code = ("import sys; data = sys.stdin.buffer.read().decode('utf-8'); "
            "sys.stdout.buffer.write(data.upper().encode('utf-8')); sys.stderr.write('warn'); sys.exit(3)")
    result = run_process([sys.executable, "-c", code], tmp_path, timeout_s=30, stdin_text="héllo")
    assert (result.stdout.strip(), result.stderr, result.exit_code, result.timed_out) == ("HÉLLO", "warn", 3, False)
    assert result.wall_s > 0


FINAL_EVENT = '{"type":"turn.completed"'


def _speaker(*lines: str, then: str) -> list[str]:
    printed = "".join(f"print({line!r}, flush=True); " for line in lines)
    return [sys.executable, "-c", f"import sys, time; {printed}{then}"]


def test_agent_stuck_after_its_final_event_is_stopped_and_counts_as_finished(tmp_path: Path) -> None:
    # #85: `codex exec` gave its final reply at 128 s and was still alive at the 480 s limit.
    argv = _speaker('{"type":"item.completed"}', FINAL_EVENT + ',"usage":{}}', then="time.sleep(60)")
    result = run_process(argv, tmp_path, timeout_s=40, final_event=FINAL_EVENT)
    assert (result.timed_out, result.exit_code, result.stopped_after_final) == (False, 0, True)
    assert FINAL_EVENT in result.stdout
    assert result.wall_s < 5


def test_the_clock_stops_at_the_final_event_when_the_agent_exits_slowly(tmp_path: Path) -> None:
    # #85: `codex exec` takes 1 to 3 s to exit after its final event on every session.
    argv = _speaker(FINAL_EVENT + "}", then="time.sleep(2)")
    result = run_process(argv, tmp_path, timeout_s=40, final_event=FINAL_EVENT)
    assert (result.exit_code, result.stopped_after_final) == (0, False)
    assert result.wall_s < 1.5


def test_a_failing_exit_after_the_final_event_stays_a_failure(tmp_path: Path) -> None:
    argv = _speaker(FINAL_EVENT + "}", then="time.sleep(1); sys.exit(3)")
    result = run_process(argv, tmp_path, timeout_s=40, final_event=FINAL_EVENT)
    assert (result.exit_code, result.stopped_after_final) == (3, False)


def test_the_final_event_quoted_inside_a_message_changes_nothing(tmp_path: Path) -> None:
    quoted = '{"type":"item","text":"\\n' + FINAL_EVENT + '"}'
    argv = _speaker(quoted, then="time.sleep(1)")
    result = run_process(argv, tmp_path, timeout_s=40, final_event=FINAL_EVENT)
    assert (result.exit_code, result.stopped_after_final) == (0, False)
    assert result.wall_s >= 1


def test_without_a_final_event_the_limit_still_applies(tmp_path: Path) -> None:
    result = run_process(_speaker(FINAL_EVENT + "}", then="time.sleep(60)"), tmp_path, timeout_s=2)
    assert result.timed_out and not result.stopped_after_final


def _alive(pid: int) -> bool:
    try:
        return psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


@pytest.mark.parametrize("agent", [ClaudeAgent("m", None), AgyAgent("m", None)])
def test_adapter_clock_stops_at_recorded_result(agent: ClaudeAgent | AgyAgent, tmp_path: Path) -> None:
    run = ("2026-10-31_claude_claude-opus-5-5_low_3b43a44b" if agent.name == "claude"
           else "2026-10-31_agy_gemini-4-argon_high_cd4f5698")
    task = "3d-voxel-landscape" if agent.name == "claude" else "bo-pnl-runway"
    transcript = Path(__file__).parents[1] / "results" / run / "transcripts" / f"{task}.jsonl.gz"
    with gzip.open(transcript, "rt", encoding="utf-8") as source:
        lines = [line for wrapper in map(json.loads, source) if wrapper["stream"] == "stdout"
                 for line in wrapper["text"].split("\n") if line.startswith("{")]
    final = next(line for line in lines
                 if json.loads(line).get("type", json.loads(line).get("event")) == "result")
    call = agent.invocation("prompt", tmp_path / "prompt.md", tmp_path, ())
    result = run_process(_speaker(final, then="time.sleep(2)"), tmp_path, timeout_s=10,
                         final_event=call.final_event)
    assert result.exit_code == 0
    assert result.wall_s < 1.5
