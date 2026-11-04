"""#124: hw-stutter-tuning grades the frame metrics, the cause and a fix inside the owner's constraints."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.tasks import tuning

TASK = next(task for task in catalog.all_tasks() if task.id == "hw-stutter-tuning")
EXP = tuning._stutter_expected()
FIX = {"setting": "pcie_aspm_rp1_gpu", "from": "L1", "to": "disabled"}
GOOD = {"avg_fps": round(EXP["avg_fps"], 1), "low_1pct_fps": round(EXP["low_nearest"], 1),
        "cause": "ASPM L1 on the GPU root port", "changes": [FIX]}


def _deliver(ws: Path, payload: object) -> None:
    (ws / "result.json").write_text(json.dumps(payload), encoding="utf-8")


def _workspace(tmp_path: Path) -> Path:
    TASK.setup(tmp_path)
    return tmp_path


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    (tmp_path / "bare").mkdir()
    (tmp_path / "solved").mkdir()
    TASK.setup(tmp_path / "bare")
    bare = TASK.check(tmp_path / "bare", [""])
    assert not bare.passed and bare.score == 0
    TASK.setup(tmp_path / "solved")
    result = TASK.check(tmp_path / "solved", TASK.reference(tmp_path / "solved"))
    assert result.passed, result.failed()


def test_the_spikes_line_up_with_the_link_state_and_not_with_the_decoys(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    frames = list(csv.DictReader(io.StringIO((ws / "capture/presentmon.csv").read_text(encoding="utf-8"))))
    spike_seconds = {int(float(row["TimeInSeconds"])) for row in frames if float(row["MsBetweenPresents"]) > 15}
    sensors = list(csv.DictReader(io.StringIO((ws / "capture/sensors.csv").read_text(encoding="utf-8"))))
    low_power = {int(row["time_s"]) for row in sensors if row["gpu_pcie_link_state"] == "L1"}
    busy_disk = {int(row["time_s"]) for row in sensors if int(row["disk_active_pct"]) > 50}
    assert spike_seconds == low_power
    assert busy_disk and not busy_disk & spike_seconds
    assert {row["gpu_pcie_link_speed"] for row in sensors} == {"Gen5 x4"}


@pytest.mark.parametrize("payload", [
    GOOD,
    {**GOOD, "low_1pct_fps": f"{EXP['low_interpolated']:.2f} fps", "avg_fps": f"{EXP['avg_fps']:.0f}",
     "cause": "PCIe link state power management puts the GPU link into L1 and every exit stalls a frame",
     "changes": [{"setting": "PCIe ASPM (root port 1, GPU)", "from": "L1", "to": "Off"},
                 {"setting": "power_plan", "from": "Balanced", "to": "High performance"},
                 {"setting": "defender_exclusions", "from": [], "to": ["C:/Games/Arena"]}]},
    {**GOOD, "cause": ["Active State Power Management on rp1"],
     "changes": [{"setting": "pcie_aspm_rp1_gpu", "from": "L1", "to": "L0"},
                 {"setting": "pcie_aspm_rp0_nvme", "from": "L1", "to": "disabled"}]},
    # #164: the final value per setting decides, so a plan that tries L0s first and then disables it still fixes.
    {**GOOD, "changes": [{**FIX, "to": "L0s"}, FIX]},
])
def test_every_valid_answer_passes(tmp_path: Path, payload: dict[str, object]) -> None:
    ws = _workspace(tmp_path)
    _deliver(ws, payload)
    result = TASK.check(ws, [""])
    assert result.passed, (result.failed(), result.details)


@pytest.mark.parametrize(("key", "wrong", "check"), [
    ("avg_fps", 120.0, "average FPS"),
    ("avg_fps", 160.0, "average FPS"),
    ("low_1pct_fps", 120.0, "1% low FPS"),
    ("low_1pct_fps", 30.0, "1% low FPS"),
    ("cause", "Windows Defender scan hitting the disk", "cause named"),
    ("cause", "GPU link speed too high for the slot", "cause named"),
    ("changes", [{**FIX, "setting": "pcie_aspm_rp0_nvme"}, {"setting": "power_plan", "from": "Balanced", "to": "High"}],
     "ASPM off on the GPU root port"),
    ("changes", [{**FIX, "to": "L0s"}, {"setting": "game_mode", "from": "on", "to": "off"}], "ASPM off on the GPU root port"),
    # #164: a later change that turns the same setting back to L1 leaves the cause in place.
    ("changes", [FIX, {"setting": "pcie_aspm_rp1_gpu", "from": "disabled", "to": "L1"}], "ASPM off on the GPU root port"),
    ("changes", [FIX, {"setting": "PCIE_ASPM_RP1_GPU", "from": "disabled", "to": "L0s"}], "ASPM off on the GPU root port"),
    ("changes", [FIX, {"setting": "gpu_link_speed", "from": "Gen5", "to": "Gen4"}], "GPU link speed kept"),
    ("changes", [FIX, {"setting": "xmp_profile", "from": "XMP I", "to": "disabled"}], "BIOS overclock kept"),
])
def test_each_check_fails_on_its_own_wrong_answer(tmp_path: Path, key: str, wrong: object, check: str) -> None:
    ws = _workspace(tmp_path)
    _deliver(ws, {**GOOD, key: wrong})
    result = TASK.check(ws, [""])
    assert result.failed() == [check], result.failed()
    assert check in result.details


def test_the_brief_does_not_hand_over_the_cause() -> None:
    prompt = TASK.steps[0].prompt.lower()
    for word in ("aspm", "l1", "pcie", "link", "root port", "power management", "defender", "presentmon", "percentile"):
        assert word not in prompt, word
    assert "not this machine" in prompt


def test_a_correct_answer_only_in_the_chat_earns_nothing(tmp_path: Path) -> None:
    ws = _workspace(tmp_path)
    result = TASK.check(ws, [json.dumps(GOOD)])
    assert not result.passed and result.score == 0
