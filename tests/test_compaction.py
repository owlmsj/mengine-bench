"""#164: the discarded quant field must commit to one quantization."""

import json
from pathlib import Path

import pytest

from mengine_bench.tasks import compaction


def test_reference_passes_and_untouched_fails(tmp_path: Path) -> None:
    compaction._handoff_setup(tmp_path)
    assert not compaction._handoff_check(tmp_path, ["", ""]).passed
    assert compaction._handoff_check(tmp_path, compaction._handoff_reference(tmp_path)).passed


@pytest.mark.parametrize("quant,valid", [
    # #164: verbatim discarded_quant field from Sonnet's delivered result.json.
    ("Q6_K (7.03 GiB, does not fit at 128k). Also discarded: the first Q5 run "
     "(37.8 t/s, 7881 MiB, 1494 MiB spilled to shared memory). Q4_K_M (7305 MiB, "
     "40.4 t/s) is kept only as fallback.", False),
    ("Q6_K or Q5", False), ("Q6_K; Q4_K_M is only fallback", True),
    ("Q6_K was discarded; Q4_K_M remains the fallback", True),
    ("Q6_K discarded; Q5_K_M is retained; Q4_K_M is kept", True),
    ("Q6_K or Q5_K_M", False),
    ("Q6_K or Q5_K_M is kept as fallback", False),
    ("Q6_K or Q6_K_M", False), ("Q6_K or IQ4_XS", False),
    (["Q6_K", "Q5"], False), ("Q6_K or Q8_0", False),
    ("Q6_K", True), ("Q6K", True), ("q6", True),
    ("`q6_k` does not fit at 128k (7.03 GiB)", True),
    ("Q6_K was discarded; Q6_K does not fit", True),
])
def test_handoff_requires_one_discarded_quant(tmp_path: Path, quant: object, valid: bool) -> None:
    compaction._handoff_reference(tmp_path)
    output = tmp_path / "result.json"
    got = json.loads(output.read_text(encoding="utf-8"))
    got["discarded_quant"] = quant
    output.write_text(json.dumps(got), encoding="utf-8")
    result = compaction._handoff_check(tmp_path, [])
    assert dict(result.checks)["answer discarded_quant"] is valid
    assert result.passed is valid
