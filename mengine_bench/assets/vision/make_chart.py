"""Source of chart.png: `uv run --no-project --with matplotlib python make_chart.py` from this folder (#59).

Two series, no printed values and no sorted bars, so the numbers have to be read from the axis.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

GPUS = ["H100", "A100", "B200", "4090", "H200"]
CONTEXT_8K = [160, 70, 210, 90, 190]
CONTEXT_256K = [110, 60, 170, 30, 180]

figure, axes = plt.subplots(figsize=(8, 4.5), dpi=120)
positions = range(len(GPUS))
width = 0.38
axes.bar([p - width / 2 for p in positions], CONTEXT_8K, width, label="8k context", color="#4c78a8")
axes.bar([p + width / 2 for p in positions], CONTEXT_256K, width, label="256k context", color="#f58518")
axes.set_xticks(list(positions), GPUS)
axes.set_ylabel("Decode speed (TPS)")
axes.set_yticks(range(0, 251, 50))
axes.set_ylim(0, 250)
axes.grid(axis="y", linewidth=0.6, alpha=0.6)
axes.set_axisbelow(True)
axes.legend(loc="upper right")
axes.set_title("Decode speed by GPU and context size")
figure.tight_layout()
figure.savefig(Path(__file__).with_name("chart.png"))
