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
    ("lc-contract", "_inline/contract.md", "Arena Tools"),
    ("gd-astar-doors", "pathfind.py", "Pixel Arena"),
    ("gd-ecs-collision-bug", "arena_ecs/components.py", "class Position"),
    ("gd-integration-repo", "README.md", "arena-server"),
    ("gd-integration-repo", "docs/CONFIG.md", "ARENA_<KEY>"),
])
def test_fixture_uses_public_vocabulary(task_id: str, fixture: str, expected: str, tmp_path: Path) -> None:
    task = next(task for task in catalog.all_tasks() if task.id == task_id)
    task.setup(tmp_path)
    assert expected in (tmp_path / fixture).read_text(encoding="utf-8")


@pytest.mark.parametrize("document", ["README.md", "docs/TASKS.md"])
def test_docs_explain_weight_two_membership(document: str) -> None:
    full = catalog.tasks("full")
    fast_ids = {task.id for task in catalog.tasks("fast")}
    heavy_ids = {task.id for task in full if task.weight == 2}
    assert len(heavy_ids) == 6 and heavy_ids <= fast_ids
    text = " ".join((ROOT / document).read_text(encoding="utf-8").split())
    assert "FAST already contains all six weight-2 tasks" in text
    assert "FULL adds six weight-1 tasks" in text


def test_readme_records_measured_baseline_and_clone_steps() -> None:
    text = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    for expected in ("git clone https://github.com/owlmsj/mengine-bench.git cd mengine-bench uv sync",
                     "20 min 10 s wall", "510 s agent time", "Codex gpt-6.1-sol",
                     "low effort", "judge with 1 vote, as its bundle records", "claude-opus-5-5", "xhigh",
                     "Both visual tasks were rendered in a browser and graded by the vision judge",
                     "FAST has no measured run yet", "every tool its harness gives it"):
        assert expected in text
    # The 2026-10-17 bundle records grading.visual "rendered" and a screenshot per visual task.
    assert 'reported "no browser"' not in text


def test_docs_distinguish_all_six_derived_par_times() -> None:
    text = (ROOT / "docs/TASKS.md").read_text(encoding="utf-8").split("## Multi-step tasks")[0]
    derived = {
        "bo-reconcile": ("bo-pnl-runway", "27.5", "55"),
        "lc-contract": ("lc-changelog", "3.6", "8"),
        "cmp-meeting-decisions": ("cmp-handoff", "19.6", "40"),
        "cmp-agent-trajectory": ("cmp-handoff", "19.6", "40"),
        "ir-server-logs": ("ir-studio-wiki", "14.6", "29.2"),
        "ir-web-facts": ("ir-studio-wiki", "14.6", "29.2"),
    }
    for task_id, (source, measured, published) in derived.items():
        assert f"| `{task_id}` | `{source}` | {measured} | {published} |" in text
    for expected in ("14 measured", "six derived", "2026-09-23", "2026-09-24", "rounded up"):
        assert expected in text
    scoring = (ROOT / "docs/SCORING.md").read_text(encoding="utf-8")
    assert "14 measured" in scoring and "six derived" in scoring
