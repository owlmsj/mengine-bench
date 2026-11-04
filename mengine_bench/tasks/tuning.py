"""Performance task: find why a gaming rig's 1% lows collapse, from captures alone (#124).

Mirrors tuning a Windows gaming rig for 1% lows with PresentMon and a sensor log. The rig
is described in files; nothing touches the host. The planted cause is a power-saving state
on the GPU's link whose transitions line up with the frame spikes; a malware scan and disk
bursts happen at other seconds. The owner's constraints forbid the tempting wrong fix.
"""

from __future__ import annotations

import json
import math
import random
import re
from collections.abc import Mapping, Sequence
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    WROTE_RESULT,
    checkpoints,
    near,
    number,
    result_json,
    saw,
    write,
)

STUTTER_SECONDS = 60
# Spike starts: every 4 s from 2.4 s, so the link sensor shows the power state at seconds 2, 6, ..., 58.
STUTTER_EVENTS = tuple(2.4 + 4 * k for k in range(15))
STUTTER_EVENT_S = 0.26
STUTTER_SCAN_SECONDS = (43, 44, 45)  # a malware scan: busy disk and CPU, smooth frames
STUTTER_DISK_SECONDS = (13, 27, 52)  # disk bursts: smooth frames
STUTTER_CAUSE_PATTERN = (r"aspm|active[ -]state power|link[ -]state power|"
                         r"\bL1\b.{0,80}(root|port|pcie|link)|(root|port|pcie|link).{0,80}\bL1\b")
STUTTER_ASPM_SETTING = r"aspm.{0,40}(rp1|gpu|root.?port.?1)|(rp1|gpu|root.?port.?1).{0,40}aspm"
STUTTER_OFF_VALUE = r"^\s*(off|disabled?|none|0|false|no|l0)\s*$"
STUTTER_LINK_SETTING = r"link.?(speed|gen|width)|pcie.?gen|gpu_link"
STUTTER_OVERCLOCK_SETTING = r"xmp|expo|pbo|precision.?boost|core.?ratio|vcore|overclock"

STUTTER_SETTINGS: tuple[tuple[str, object, str], ...] = (
    ("power_plan", "Balanced", "Windows"),
    ("hardware_accelerated_gpu_scheduling", "on", "Windows"),
    ("game_mode", "on", "Windows"),
    ("defender_realtime_protection", "on", "Windows"),
    ("defender_exclusions", [], "Windows"),
    ("defender_scheduled_scan", "daily 21:00, quick", "Windows"),
    ("core_parking_min_cores_pct", 100, "Windows"),
    ("processor_min_state_pct", 5, "Windows"),
    ("memory_integrity_hvci", "off", "Windows"),
    ("game_dvr_background_recording", "off", "Windows"),
    ("usb_selective_suspend", "enabled", "Windows"),
    ("fullscreen_optimizations", "enabled", "Windows"),
    ("pcie_aspm_rp0_nvme", "L1", "BIOS"),
    ("pcie_aspm_rp1_gpu", "L1", "BIOS"),
    ("pcie_aspm_rp2_chipset", "disabled", "BIOS"),
    ("gpu_link_speed", "Gen5", "BIOS"),
    ("gpu_link_width", "x4", "BIOS"),
    ("resizable_bar", "on", "BIOS"),
    ("xmp_profile", "XMP I (DDR5-6000)", "BIOS"),
    ("cpu_pbo", "enabled", "BIOS"),
    ("cpu_core_ratio", "auto", "BIOS"),
    ("gpu_low_latency_mode", "on", "Driver"),
    ("vsync", "off", "Game"),
    ("frame_rate_limit", "none", "Game"),
)

STUTTER_NOTES_MD = """# Owner notes - rig "arena-01"

The game hitches every few seconds even though the average frame rate looks fine.
Capture: PresentMon on Arena.exe for one minute in the same replay, plus a 1 s sensor log
taken at the same time (same clock: second 0 of both files is the same instant).
settings.json is a dump of the rig's current settings.

How we measure:
- Average FPS = frames presented divided by the capture's seconds (1000 / mean MsBetweenPresents).
- 1% low = the FPS at the 99th percentile frame time (1000 / p99 of MsBetweenPresents).

Fixed constraints:
- The GPU stays at its current PCIe link speed (Gen5 x4): the slot is shared with the
  AI workload and that link speed is validated for it.
- No BIOS overclock changes (XMP, PBO, core ratio stay as they are).
"""


def _stutter_frames() -> list[float]:
    rng = random.Random(124_301)
    frames: list[float] = []
    clock = 0.0
    while clock < STUTTER_SECONDS:
        in_spike = any(start <= clock < start + STUTTER_EVENT_S for start in STUTTER_EVENTS)
        ms = rng.gauss(22.0, 0.5) if in_spike else max(5.6, rng.gauss(6.95, 0.3))
        frames.append(round(ms, 3))
        clock += ms / 1000
    return frames


def _stutter_expected() -> dict[str, float]:
    frames = _stutter_frames()
    ordered = sorted(frames)
    count = len(ordered)
    nearest = ordered[math.ceil(0.99 * count) - 1]
    position = (count - 1) * 0.99
    lower = math.floor(position)
    interpolated = ordered[lower] + (ordered[min(lower + 1, count - 1)] - ordered[lower]) * (position - lower)
    return {"avg_fps": 1000 / (sum(frames) / count), "low_nearest": 1000 / nearest, "low_interpolated": 1000 / interpolated}


def _stutter_presentmon() -> str:
    lines = ["Application,ProcessID,SwapChainAddress,Runtime,SyncInterval,PresentFlags,Dropped,TimeInSeconds,"
             "MsBetweenPresents,MsBetweenDisplayChange,MsInPresentAPI,MsUntilRenderComplete,MsUntilDisplayed\n"]
    rng = random.Random(124_302)
    clock = 0.0
    for ms in _stutter_frames():
        lines.append(f"Arena.exe,7316,0x000001F2A8C40000,DXGI,0,512,0,{clock:.6f},{ms:.3f},"
                     f"{ms + rng.uniform(-0.05, 0.05):.3f},{rng.uniform(0.15, 0.4):.3f},"
                     f"{rng.uniform(4.0, 5.5):.3f},{rng.uniform(5.0, 6.5):.3f}\n")
        clock += ms / 1000
    return "".join(lines)


def _stutter_sensors() -> str:
    rng = random.Random(124_303)
    spike_seconds = {int(start) for start in STUTTER_EVENTS}
    lines = ["time_s,cpu_clock_mhz,cpu_util_pct,gpu_clock_mhz,gpu_pcie_link_state,gpu_pcie_link_speed,"
             "dpc_latency_us,disk_active_pct,top_cpu_process\n"]
    for second in range(STUTTER_SECONDS):
        scan = second in STUTTER_SCAN_SECONDS
        disk = rng.uniform(80, 97) if scan or second in STUTTER_DISK_SECONDS else rng.uniform(0, 6)
        lines.append(f"{second},{rng.randint(5150, 5450)},{rng.uniform(55, 68) if scan else rng.uniform(31, 42):.0f},"
                     f"{rng.randint(2710, 2760)},{'L1' if second in spike_seconds else 'L0'},Gen5 x4,"
                     f"{rng.randint(380, 520) if scan else rng.randint(40, 95)},{disk:.0f},"
                     f"{'MsMpEng.exe' if scan else 'Arena.exe'}\n")
    return "".join(lines)


def _stutter_setup(ws: Path) -> None:
    write(ws, "capture/presentmon.csv", _stutter_presentmon())
    write(ws, "capture/sensors.csv", _stutter_sensors())
    write(ws, "settings.json", json.dumps({"rig": "arena-01", "settings": [
        {"setting": name, "value": value, "where": where} for name, value, where in STUTTER_SETTINGS]}, indent=2) + "\n")
    write(ws, "NOTES.md", STUTTER_NOTES_MD)


def _stutter_changes(got: Mapping[str, object]) -> list[tuple[str, str]]:
    """(setting, to) pairs from the `changes` list; anything else is dropped."""
    changes = got.get("changes")
    if not isinstance(changes, list):
        return []
    pairs = []
    for change in changes:
        if not isinstance(change, dict):
            continue
        setting = change.get("setting", change.get("name"))
        pairs.append((str(setting or ""), str(change.get("to", change.get("value", "")))))
    return pairs


def _stutter_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    exp = _stutter_expected()
    got = result_json(ws)
    result.add("average FPS", near(got.get("avg_fps"), exp["avg_fps"], exp["avg_fps"] * 0.01),
               saw(got.get("avg_fps"), round(exp["avg_fps"], 1)))
    # #124: nearest-rank and interpolated p99 are both valid readings of the owner's definition.
    low = number(got.get("low_1pct_fps"))
    low_ok = low is not None and any(abs(low - want) <= want * 0.02 for want in (exp["low_nearest"], exp["low_interpolated"]))
    result.add("1% low FPS", low_ok, saw(got.get("low_1pct_fps"), round(exp["low_nearest"], 1)))
    cause = got.get("cause")
    cause_text = cause if isinstance(cause, str) else json.dumps(cause)
    result.add("cause named", isinstance(cause, (str, list, dict)) and re.search(STUTTER_CAUSE_PATTERN, cause_text, re.IGNORECASE) is not None,
               saw(cause, "the GPU link's power-saving state (ASPM L1 on its root port)"))
    pairs = _stutter_changes(got)
    # #164: the plan's final value per setting counts, so a later change back to L1 undoes the fix.
    final_aspm = {setting.strip().lower(): to for setting, to in pairs if re.search(STUTTER_ASPM_SETTING, setting, re.IGNORECASE)}
    fixed = bool(final_aspm) and all(re.search(STUTTER_OFF_VALUE, to, re.IGNORECASE) for to in final_aspm.values())
    result.add("ASPM off on the GPU root port", fixed, saw(pairs, "pcie_aspm_rp1_gpu -> disabled"))
    # #124: an empty change list keeps every constraint but fixes nothing, so it earns neither.
    link = [setting for setting, _ in pairs if re.search(STUTTER_LINK_SETTING, setting, re.IGNORECASE)]
    result.add("GPU link speed kept", bool(pairs) and not link, saw(link or pairs, "changes that leave the link speed alone"))
    overclock = [setting for setting, _ in pairs if re.search(STUTTER_OVERCLOCK_SETTING, setting, re.IGNORECASE)]
    result.add("BIOS overclock kept", bool(pairs) and not overclock, saw(overclock or pairs, "no XMP, PBO or core ratio change"))
    return result


def _stutter_reference(ws: Path) -> list[str]:
    exp = _stutter_expected()
    write(ws, "result.json", json.dumps({
        "avg_fps": round(exp["avg_fps"], 1), "low_1pct_fps": round(exp["low_nearest"], 1),
        "cause": "ASPM L1 on the GPU's PCIe root port: every frame spike starts in a second where the link sits in L1.",
        "changes": [{"setting": "pcie_aspm_rp1_gpu", "from": "L1", "to": "disabled"}]}))
    return ["done"]


TASKS = [
    EvalTask(
        id="hw-stutter-tuning", category="performance",
        provenance="Tuning the owner's Windows gaming rig for 1% lows from a PresentMon capture and a sensor log",
        summary="Find from captured logs why a gaming PC stutters and which settings fix it within the owner's rules.",
        setup=_stutter_setup, check=_stutter_check, reference=_stutter_reference, timeout_s=90,
        checkpoints=checkpoints(("read the frame capture", r"presentmon"), ("read the sensor log", r"sensors"),
                                ("read the settings", r"settings\.json"), ("read the owner notes", r"NOTES"), WROTE_RESULT),
        steps=(Step("The owner's gaming rig hitches every few seconds even though the average frame rate looks fine, "
                    "and the 1% lows are poor. A one-minute frame capture, a sensor log, a dump of the rig's settings and "
                    "the owner's notes are in {WS}. That rig is not this machine: everything about it is in these files, "
                    "and nothing is to be applied to this host. Find what causes the hitches and which setting changes fix "
                    "them within the owner's constraints. Record in {WS}/result.json: avg_fps, low_1pct_fps, cause and "
                    "changes (a list of {setting, from, to})."),),
    ),
]
