"""Public fixture vocabulary and release claims must stay reproducible."""

from pathlib import Path

import pytest

from mengine_bench import catalog

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(("task_id", "fixture", "expected"), [
    ("ds-ab-playtest", "telemetry/README.md", "Pixel Arena tutorial"),
    ("ds-ab-playtest", "telemetry/README.md", "arena-panel"),
    ("bo-reconcile", "backoffice/invoices.csv", "Arena Studio"),
    ("cmp-handoff", "session/transcript.md", "local-9b Q5"),
    ("cmp-handoff", "session/transcript.md", "scripts/measure_decode.ps1"),
    ("cmp-handoff", "session/transcript.md", "scripts/start_server.ps1:165"),
    ("cmp-handoff", "session/transcript.md", "profiles/local/local-9b.json"),
    ("cmp-handoff", "session/transcript.md", "check_vision.ps1"),
    ("lc-changelog", "_inline/changelog.md", "Pixel Arena"),
    ("gd-astar-doors", "pathfind.py", "Pixel Arena"),
    ("gd-ecs-collision-bug", "arena_ecs/components.py", "class Position"),
    ("gd-integration-repo", "README.md", "arena-server"),
    ("gd-integration-repo", "docs/CONFIG.md", "ARENA_<KEY>"),
])
def test_fixture_uses_public_vocabulary(task_id: str, fixture: str, expected: str, tmp_path: Path) -> None:
    task = next(task for task in catalog.all_tasks() if task.id == task_id)
    task.setup(tmp_path)
    assert expected in (tmp_path / fixture).read_text(encoding="utf-8")


def test_readme_records_clone_steps_and_current_runs_only() -> None:
    text = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    for expected in ("git clone https://github.com/owlmsj/mengine-bench.git cd mengine-bench uv sync",
                     "every tool its harness gives it", "claude-opus-5-5", "xhigh",
                     "only runs of the current bench are ranked", "git show fde6c16:LEADERBOARD.md"):
        assert expected in text
    # The 0.1.0 runs left results/: the README must not quote them as current numbers.
    for retired in ("20 min 10 s wall", "baseline below", "Both runs are on"):
        assert retired not in text


def test_committed_results_are_all_of_the_current_bench() -> None:
    import json
    from mengine_bench import __version__
    for result_file in (ROOT / "results").rglob("result.json"):
        assert json.loads(result_file.read_text(encoding="utf-8"))["bench_version"] == __version__, result_file


def test_readme_moves_every_preflight_instruction_file_aside_and_back(tmp_path: Path) -> None:
    from mengine_bench.preflight import INSTRUCTION_FILES, global_instruction_files
    for folder in (".claude", ".codex", ".config/opencode"):
        for name in INSTRUCTION_FILES:
            (tmp_path / folder).mkdir(parents=True, exist_ok=True)
            (tmp_path / folder / name).write_text("x", encoding="utf-8")
    checked = {path.relative_to(tmp_path).as_posix() for agent in ("claude", "codex", "opencode")
               for path in global_instruction_files(agent, tmp_path, {})}
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    hygiene = text[text.index("## Run hygiene"):text.index("## Submitting results")]
    assert checked and {path for path in checked if f'"{path}"' not in hygiene and f" {path}" not in hygiene} == set()
    assert "after the run" in hygiene and "mengine-bench-preflight-backup" in hygiene
