"""Machine facts in result.json: real CPU and GPU names, and the declared --config."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from mengine_bench import environment
from mengine_bench.environment import NOT_DETECTED, parse_config


def test_cpu_name_from_proc_cpuinfo() -> None:
    text = "processor\t: 0\nvendor_id\t: AuthenticAMD\nmodel name\t: AMD Ryzen 9 7950X 16-Core Processor\n"
    assert environment.cpu_from_cpuinfo(text) == "AMD Ryzen 9 7950X 16-Core Processor"
    assert environment.cpu_from_cpuinfo("processor\t: 0\n") is None


@pytest.mark.parametrize(("system", "source"), [("Windows", "_windows_cpu"), ("Linux", "_linux_cpu"),
                                                ("Darwin", "_mac_cpu")])
def test_cpu_name_uses_each_os_source(monkeypatch: pytest.MonkeyPatch, system: str, source: str) -> None:
    for name in ("_windows_cpu", "_linux_cpu", "_mac_cpu"):
        monkeypatch.setattr(environment, name, lambda: None)
    monkeypatch.setattr(environment, source, lambda: "  Intel(R) Core(TM) i9-14900K  ")
    assert environment.cpu_name(system) == "Intel(R) Core(TM) i9-14900K"


def test_cpu_name_falls_back_to_the_platform(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(environment, "_linux_cpu", lambda: None)
    monkeypatch.setattr(environment.platform, "processor", lambda: "")
    monkeypatch.setattr(environment.platform, "machine", lambda: "x86_64")
    assert environment.cpu_name("Linux") == "x86_64"


def test_gpu_names_with_vram_from_nvidia_smi(monkeypatch: pytest.MonkeyPatch) -> None:
    out = "NVIDIA GeForce RTX 4090, 24564 MiB\nNVIDIA RTX A6000, 49140 MiB\n"
    monkeypatch.setattr(environment.shutil, "which", lambda name: "/bin/nvidia-smi")
    monkeypatch.setattr(environment.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(a, 0, stdout=out, stderr=""))
    assert environment.gpu_names() == "NVIDIA GeForce RTX 4090 (24 GB), NVIDIA RTX A6000 (48 GB)"


def test_gpu_not_detected_without_nvidia_smi(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(environment.shutil, "which", lambda name: None)
    assert environment.gpu_names() == NOT_DETECTED == "not detected"


def test_collect_environment_has_the_spec_fields() -> None:
    found = environment.collect_environment()
    assert {"os", "cpu", "cpu_count", "ram_gb", "gpu", "python"} <= set(found)
    assert isinstance(found["cpu"], str) and found["cpu"]


def test_parse_config_keeps_declared_pairs_in_order() -> None:
    pairs = ["provider=local", 'server_gpu=RTX 5090', "quant=Q4_K_M", "ctx=256k", "temperature=0.6"]
    assert parse_config(pairs) == {"provider": "local", "server_gpu": "RTX 5090", "quant": "Q4_K_M",
                                   "ctx": "256k", "temperature": "0.6"}
    assert parse_config([]) == {}


@pytest.mark.parametrize("bad", ["novalue", "=x", "bad key=x", "personal_instructions=none"])
def test_parse_config_errors_name_the_value(bad: str) -> None:
    with pytest.raises(ValueError, match="key=value") as error:
        parse_config([bad])
    assert repr(bad) in str(error.value)


def test_run_records_config_and_summary_shows_it(fake_agent: object, tmp_path: Path) -> None:
    from mengine_bench import cli
    from test_run_e2e import REFERENCE_AGENT

    template = json.loads(fake_agent("reference", REFERENCE_AGENT))  # type: ignore[operator]
    template.remove("-I")
    out = tmp_path / "results"
    assert cli.main(["run", "--agent", "cmd", "--cmd", json.dumps(template), "--model", "fake/ref", "--tasks",
                     "ds-ab-playtest", "--out", str(out), "--config", "provider=local", "--config",
                     "quant=Q4_K_M"]) == 0
    [bundle] = out.glob("*")
    result = json.loads((bundle / "result.json").read_text(encoding="utf-8"))
    assert result["config"]["provider"] == "local" and result["config"]["quant"] == "Q4_K_M"
    assert result["environment"]["gpu"]
    [task] = result["tasks"]
    assert set(task["steps"][0]) >= {"usage", "wall_s"} and "tokens" in task and "cost_usd" in task
    summary = (bundle / "summary.md").read_text(encoding="utf-8")
    assert "provider=local" in summary and "quant=Q4_K_M" in summary and "Machine:" in summary
    assert len(summary.splitlines()) < 40, "summary.md stays short"
