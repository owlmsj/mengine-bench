"""#164: significance alone does not make a reported p-value correct."""

import json
import math
from pathlib import Path

import pytest

from mengine_bench.tasks import business


def test_reference_passes_and_untouched_fails(tmp_path: Path) -> None:
    business._ab_setup(tmp_path)
    assert not business._ab_check(tmp_path, [""]).passed
    assert business._ab_check(tmp_path, business._ab_reference(tmp_path)).passed


@pytest.mark.parametrize("p_value,valid", [
    (0.0002, True),  # #164: Opus's rounded pooled two-sided z-test.
    (0.000198, True),  # #164: Sonnet's pooled two-sided z-test.
    (0.0003, True),  # #98: existing equivalent-test route.
    ("<0.001", True), ("p < 0.001", True),
    ("<0.01", False), ("<0.0001", False),
    (0.01, False),  # #164: invented significant value that the old check accepted.
    (0, False), (0.049, False), (-0.0001, False), (None, False),
])
def test_ab_p_value_tracks_gold(tmp_path: Path, p_value: object, valid: bool) -> None:
    business._ab_reference(tmp_path)
    _replace_p_value(tmp_path, p_value)
    result = business._ab_check(tmp_path, [])
    assert dict(result.checks)["the gain is significant"] is valid
    assert result.passed is valid


def _replace_p_value(ws: Path, p_value: object) -> None:
    output = ws / "result.json"
    got = json.loads(output.read_text(encoding="utf-8"))
    got["p_value"] = p_value
    output.write_text(json.dumps(got), encoding="utf-8")


def test_ab_accepts_continuity_correction_and_two_sided_fisher(tmp_path: Path) -> None:
    # #164: independent fixed contingency table from the deduplicated fixture.
    # Pearson chi-square equals the pooled z-test squared for this 2x2 table.
    pooled = 762 / 1800
    z = (420 / 900 - 342 / 900) / math.sqrt(pooled * (1 - pooled) * 2 / 900)
    continuity_z = ((420 - 342 - 1) / 900) / math.sqrt(pooled * (1 - pooled) * 2 / 900)
    fisher = 2 * sum(math.comb(762, k) * math.comb(1038, 900 - k) / math.comb(1800, 900)
                     for k in range(343))
    business._ab_reference(tmp_path)
    for p_value in (math.erfc(z / math.sqrt(2)), math.erfc(continuity_z / math.sqrt(2)), fisher):
        _replace_p_value(tmp_path, p_value)
        assert business._ab_check(tmp_path, []).passed, p_value
