"""Machine facts for result.json and the declared `--config` (#23).

Results are public: they name the hardware (CPU model, GPU model and VRAM)
but never a local path, user or host name. `--config key=value` is free-form
metadata the submitter declares (provider, quantization, context, MCP...);
the bench records it and never applies it to the harness.
"""

from __future__ import annotations

import platform
import re
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

import psutil

NOT_DETECTED = "not detected"
PROBE_TIMEOUT_S = 10
CONFIG_KEY = re.compile(r"^[A-Za-z0-9_.-]+$")
# Filled by the bench itself from the preflight (#23); a submitter cannot declare it.
RESERVED_CONFIG_KEYS = frozenset({"personal_instructions"})


def cpu_from_cpuinfo(text: str) -> str | None:
    for line in text.splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "model name" and value.strip():
            return value.strip()
    return None


def _windows_cpu() -> str | None:
    try:
        import winreg
    except ImportError:
        return None
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            value, _ = winreg.QueryValueEx(key, "ProcessorNameString")
    except OSError:
        return None
    return str(value)


def _linux_cpu() -> str | None:
    try:
        return cpu_from_cpuinfo(Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return None


def _mac_cpu() -> str | None:
    try:
        proc = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True,
                              timeout=PROBE_TIMEOUT_S, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def cpu_name(system: str | None = None) -> str:
    """The CPU model name; platform.processor() is only a fallback (on Windows it is a family string)."""
    system = system or platform.system()
    source = {"Windows": _windows_cpu, "Linux": _linux_cpu, "Darwin": _mac_cpu}.get(system)
    found = source() if source is not None else None
    if found and found.strip():
        return " ".join(found.split())
    return platform.processor() or platform.machine() or NOT_DETECTED


def _gpu_entry(line: str) -> str | None:
    name, _, memory = line.rpartition(",")
    mib = re.match(r"\s*(\d+)\s*MiB", memory)
    if not name.strip() or mib is None:
        return line.strip() or None
    return f"{name.strip()} ({round(int(mib.group(1)) / 1024)} GB)"


def gpu_names() -> str:
    """NVIDIA GPUs with VRAM from nvidia-smi, else "not detected"."""
    smi = shutil.which("nvidia-smi")
    if smi is None:
        return NOT_DETECTED
    try:
        proc = subprocess.run([smi, "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True,
                              text=True, timeout=PROBE_TIMEOUT_S, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return NOT_DETECTED
    entries = [entry for entry in (_gpu_entry(line) for line in proc.stdout.splitlines()) if entry]
    return ", ".join(entries) if proc.returncode == 0 and entries else NOT_DETECTED


def collect_environment() -> dict[str, object]:
    return {
        "os": f"{platform.system()} {platform.release()}",
        "cpu": cpu_name(),
        "cpu_count": psutil.cpu_count(logical=True),
        "ram_gb": round(psutil.virtual_memory().total / 2**30, 1),
        "gpu": gpu_names(),
        "python": platform.python_version(),
    }


def parse_config(pairs: Sequence[str]) -> dict[str, str]:
    """Repeated `--config key=value` into an ordered mapping; a later key replaces an earlier one."""
    config: dict[str, str] = {}
    for pair in pairs:
        key, sep, value = pair.partition("=")
        if not sep or not CONFIG_KEY.match(key) or key in RESERVED_CONFIG_KEYS:
            raise ValueError(f"received --config {pair!r}; expected key=value with a key of letters, digits, "
                             f"'_', '.' or '-' (not {sorted(RESERVED_CONFIG_KEYS)})")
        config[key] = value.strip()
    return config
