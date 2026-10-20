"""Bundle naming."""

from __future__ import annotations

from mengine_bench.bundle import bundle_dir_name


def test_bundle_dir_name_slugs_every_part() -> None:
    name = bundle_dir_name("2026-10-17", "opencode", "deepseek/v4.1:flash", None, "a1b2c3d4")
    assert name == "2026-10-17_opencode_deepseek-v4.1-flash_none_a1b2c3d4"
    assert bundle_dir_name("2026-10-17", "claude", "claude-opus-5-5", "x high", "ff").endswith("_x-high_ff")
