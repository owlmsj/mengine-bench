"""#228: `run --tasks-dir` runs an external task pool (mengine#952) and keeps each OpenCode session."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import cli
from mengine_bench.bundle import transcript_jsonl
from mengine_bench.redact import PathScope
from mengine_bench.runner.agents import CmdAgent
from mengine_bench.runner.task_run import run_task

POOL_MODULE = '''
from pathlib import Path
from mengine_bench.core import CheckResult, EvalTask, Step, saw


def setup(ws: Path) -> None:
    (ws / "n.txt").write_text("41", encoding="utf-8")


def check(ws: Path, answers: list[str]) -> CheckResult:
    result = CheckResult()
    got = (ws / "out.txt").read_text(encoding="utf-8").strip() if (ws / "out.txt").is_file() else None
    result.add("incremented", got == "42", saw(got, "42"))
    return result


def reference(ws: Path) -> list[str]:
    (ws / "out.txt").write_text("42", encoding="utf-8")
    return ["42"]


TASKS = [EvalTask(id="pool-228-inc", category="engineering", summary="Increment a number from a file.",
                  steps=(Step("Write n.txt + 1 to {WS}/out.txt and say the result."),), setup=setup, check=check,
                  reference=reference, timeout_s=60, provenance="#228 test pool", site=None)]
'''

SOLVER = """
import json, sys
from pathlib import Path
ws = Path(sys.argv[1])
(ws / "out.txt").write_text(str(int((ws / "n.txt").read_text()) + 1), encoding="utf-8")
print(json.dumps({"type": "text", "sessionID": "ses_fake228", "part": {"type": "text", "text": "42"}}))
"""


def _pool(tmp_path: Path) -> Path:
    pool = tmp_path / "pool"
    pool.mkdir()
    (pool / "q228_inc.py").write_text(POOL_MODULE, encoding="utf-8")
    return pool


def test_tasks_dir_dry_run_lists_only_the_external_pool(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pool = _pool(tmp_path)
    assert cli.main(["run", "--agent", "claude", "--model", "m", "--tasks-dir", str(pool), "--dry-run"]) == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["tasks"] == ["pool-228-inc"]
    assert plan["config"]["tasks_dir"] == "pool"


def test_tasks_dir_refuses_submit(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="--tasks-dir"):
        cli.main(["run", "--agent", "claude", "--model", "m", "--tasks-dir", str(_pool(tmp_path)), "--submit"])


def test_tasks_dir_rejects_a_folder_without_tasks(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(SystemExit, match="empty"):
        cli.main(["run", "--agent", "claude", "--model", "m", "--tasks-dir", str(empty), "--dry-run"])


@dataclass
class SessionAgent:
    """A cmd agent whose harness can export the session it just ran, like OpenCode's `session export`."""

    inner: CmdAgent
    name: str = "cmd"

    def invocation(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        return self.inner.invocation(*args, **kwargs)

    def parse(self, stdout: str, exit_code: int):  # type: ignore[no-untyped-def]
        return self.inner.parse(stdout, exit_code)

    def version(self) -> str | None:
        return None

    def session_export_argv(self, session_id: str) -> list[str]:
        body = "import json,sys; print(json.dumps({'info': {'id': sys.argv[1]}, 'messages': []}))"
        return [sys.executable, "-I", "-c", body, session_id]


def test_session_export_lands_in_the_transcript(fake_agent: FakeAgent, tmp_path: Path) -> None:
    pool = _pool(tmp_path)
    from mengine_bench.catalog import tasks_from_dir

    [task] = tasks_from_dir(pool)
    agent = SessionAgent(CmdAgent(template=fake_agent("solver", SOLVER), model="fake/m", effort=None))
    record = run_task(task, agent, tmp_path / "run")
    assert record.status == "ok" and record.check is not None and record.check.passed, record
    exported = tmp_path / "run" / "transcripts" / "step-0.session.txt"
    assert json.loads(exported.read_text(encoding="utf-8"))["info"]["id"] == "ses_fake228"
    lines = [json.loads(line) for line in transcript_jsonl(exported.parent, PathScope()).decode().splitlines()]
    assert [line["stream"] for line in lines] == ["session", "stderr", "stdout"]
