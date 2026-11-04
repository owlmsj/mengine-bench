"""Bundle naming."""

from __future__ import annotations

from pathlib import Path

from mengine_bench.bundle import bundle_dir_name


def test_bundle_dir_name_slugs_every_part() -> None:
    name = bundle_dir_name("2026-10-17", "opencode", "deepseek/v4.1:flash", None, "a1b2c3d4")
    assert name == "2026-10-17_opencode_deepseek-v4.1-flash_none_a1b2c3d4"
    assert bundle_dir_name("2026-10-17", "claude", "claude-opus-5-5", "x high", "ff").endswith("_x-high_ff")


def test_summary_shows_infra_status_and_note(tmp_path: Path) -> None:
    import json
    from test_bundle_leaderboard import _write_result
    from mengine_bench.report import render_summary

    bundle = _write_result(tmp_path, "infra", 50.0, task_ids=["cu-social-cycle"])
    result = json.loads((bundle / "result.json").read_text())
    signature = "only files this session is allowed to read can be uploaded"
    result["tasks"][0].update(status="infra", c=0.5, checks=[], judge=None, agent_s=1.0,
        flags=[f"infra fault: {signature}; rerun that task"])
    summary = render_summary(result)
    assert "| cu-social-cycle | infra" in summary
    assert f"infra fault: {signature}; rerun that task" in summary
