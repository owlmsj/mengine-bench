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


def test_readme_records_clone_steps_score_and_judge() -> None:
    text = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    for expected in ("git clone https://github.com/owlmsj/mengine-bench.git cd mengine-bench uv sync",
                     "Everything its harness gives it", "Claude Opus 5.5, xhigh",
                     "Score = 0.6 x Correct % + 0.25 x Judge + 0.15 x Speed x Correct % / 100", "## The 14 tasks", "--config key=value",
                     "--price input=X,cached=Y,output=Z", "privacy check: clean"):
        assert expected in text, expected
    assert f"## The {len(catalog.all_tasks())} tasks" in text


def test_readme_names_every_personal_instruction_file(tmp_path: Path) -> None:
    from mengine_bench.preflight import INSTRUCTION_FILES, global_instruction_files
    for folder in (".claude", ".codex", ".config/opencode"):
        (tmp_path / folder).mkdir(parents=True, exist_ok=True)
        for name in INSTRUCTION_FILES:
            (tmp_path / folder / name).write_text("x", encoding="utf-8")
    names = {path.relative_to(tmp_path).as_posix() for agent in ("claude", "codex", "opencode")
             for path in global_instruction_files(agent, tmp_path, {})}
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    # AGENTS.override.md is Codex's rarely used twin of AGENTS.md; the warning names it when present.
    assert names and {name for name in names if f"~/{name}" not in text} <= {".codex/AGENTS.override.md"}
