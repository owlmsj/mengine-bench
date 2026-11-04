"""Build the two-run audit page from run bundles and auditor rows (#165).

Usage: uv run python -I .claude/skills/bench-audit/build.py <audit.json> <out dir>

audit.json:
  {"id": "...", "title": "...", "subtitle": "...", "footer": "...", "verdict": ["...", ...],
   "runs": [{"key": "a", "label": "Run A", "bundle": "<path>"}, {"key": "b", "label": "Run B", "bundle": "<path>"}],
   "rows": ["<auditor json>", ...], "media_text": {"<task id>": "what to look for"}}
Each auditor file is a JSON array of rows: {"task", "brief", "<key a>": {...}, "<key b>": {...}, "grader_issue",
"better": "<key a>|<key b>|tie", "note"}; a side holds grader_c, really_correct (yes|partial|no), evidence, solution,
judge, my_judge, judge_verdict (fair|too_high|too_low), why.
Writes <out>/index.html, copies pages and media under <out>/assets/, and lists them in <out>/files.json
({published path: absolute source}) for the Artifact `files` parameter.
"""
from __future__ import annotations

import json
import shutil
import sys
from collections import Counter
from pathlib import Path

from mengine_bench.leaderboard import run_cost_text
from mengine_bench.prices import estimated_usd, price_text

HERE = Path(__file__).resolve().parent
ANSWER_CHARS = 4000
AUDIO = {".wav", ".mp3", ".ogg", ".m4a"}
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
SIDE_KEYS = ("grader_c", "really_correct", "judge", "my_judge")


def fail(message: str) -> None:
    raise SystemExit(f"bench-audit build: {message}")


def mmss(seconds: object) -> str:
    if not isinstance(seconds, (int, float)):
        return "-"
    if seconds < 60:
        return f"{seconds:.1f} s"
    whole = round(seconds)
    return f"{whole // 60} min {whole % 60:02d} s"


def task_cost(result: dict, task: dict) -> str:
    """#178 (rule #162): the task's exact harness cost, else its list-price estimate, like the leaderboard."""
    usd = task.get("cost_usd")
    if isinstance(usd, (int, float)):
        return f"${usd:.2f}"
    per_task = {**result, "totals": {"tokens": task.get("tokens") or {}, "stats": task.get("stats") or {}}}
    if price_text(per_task) == "$0.00 (local)":
        return "$0.00 (local)"
    estimate = estimated_usd(per_task)
    return "n/a" if estimate is None else f"~${estimate:.2f}"


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    runs = config.get("runs")
    if not isinstance(runs, list) or len(runs) != 2:
        fail(f"received runs={runs!r}; expected two objects with key, label and bundle")
    for run in runs:
        bundle = Path(run.get("bundle", ""))
        if not (bundle / "result.json").is_file():
            fail(f"received bundle {str(bundle)!r}; expected a folder with result.json")
    return config


def load_rows(config: dict, base: Path, keys: tuple[str, str]) -> list[dict]:
    rows: list[dict] = []
    for name in config.get("rows", []):
        loaded = json.loads((base / name).read_text(encoding="utf-8"))
        rows += loaded if isinstance(loaded, list) else [loaded]
    for row in rows:
        missing = [key for key in keys if not isinstance(row.get(key), dict)]
        missing += [f"{key}.{field}" for key in keys if isinstance(row.get(key), dict) for field in SIDE_KEYS
                    if field not in row[key]]
        if missing or "task" not in row:
            fail(f"received auditor row {str(row.get('task'))!r} missing {missing or ['task']}; expected the schema in this file's docstring")
    return rows


def copy(source: Path, out: Path, published: str, files: dict[str, str]) -> str:
    target = out / published
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    files[published] = str(target.resolve())
    return published


def run_media(bundle: Path, key: str, task: str, judge: object, out: Path, files: dict[str, str]) -> list[dict]:
    """Pages and screenshots the judge saw (judge/), and human-only evidence (evidence/, #165)."""
    items: list[dict] = []
    shot = bundle / "judge" / f"{task}.png"
    shot_path = copy(shot, out, f"assets/{key}/{task}/screenshot.png", files) if shot.is_file() else None
    task_dir = bundle / "judge" / task
    pages = sorted(task_dir.rglob("*.html")) if task_dir.is_dir() else []
    if pages:
        page = copy(pages[0], out, f"assets/{key}/{task}/page.html", files)
        items.append({"kind": "page", "src": page, "shot": shot_path, "judge": judge})
    elif shot_path:
        items.append({"kind": "image", "src": shot_path, "judge": judge, "caption": "screenshot do judge"})
    sources = [path for folder in (task_dir, bundle / "evidence" / task) if folder.is_dir()
               for path in sorted(folder.rglob("*")) if path.is_file() and path.suffix.lower() != ".html"]
    for source in sources:
        root = task_dir if task_dir in source.parents else bundle / "evidence" / task
        rel = source.relative_to(root).as_posix()
        published = copy(source, out, f"assets/{key}/{task}/files/{rel}", files)
        suffix = source.suffix.lower()
        kind = "audio" if suffix in AUDIO else "image" if suffix in IMAGES else "file"
        items.append({"kind": kind, "src": published, "judge": judge, "caption": rel})
    return items


def build(config_path: Path, out: Path) -> dict[str, str]:
    config = load_config(config_path)
    runs = config["runs"]
    keys = (runs[0]["key"], runs[1]["key"])
    rows = load_rows(config, config_path.parent, keys)
    results = {run["key"]: json.loads((Path(run["bundle"]) / "result.json").read_text(encoding="utf-8")) for run in runs}
    by_task = {key: {task["id"]: task for task in results[key]["tasks"]} for key in keys}
    order = [task["id"] for task in results[keys[0]]["tasks"]]
    rows.sort(key=lambda row: order.index(row["task"]) if row["task"] in order else len(order))
    files: dict[str, str] = {}
    out.mkdir(parents=True, exist_ok=True)
    for row in rows:
        for key in keys:
            task = by_task[key].get(row["task"], {})
            answer = "\n\n".join(text for text in task.get("answers") or [] if text)
            row[key].update(time=mmss(task.get("agent_s")), cost=task_cost(results[key], task),
                            answer=answer if len(answer) <= ANSWER_CHARS else answer[:ANSWER_CHARS] + " [...]",
                            rationale=task.get("judge_rationale") or "", parts=task.get("judge_parts") or {})
    for run in runs:
        totals = results[run["key"]]["totals"]
        run["totals"] = {"score": f"{totals.get('score') or 0:.1f}", "solved": totals.get("solved"),
                         "time": mmss(totals.get("time_s")), "cost": run_cost_text(results[run["key"]]),
                         "judge": f"{totals.get('judge') or 0:.1f}",
                         "real": sum(row[run["key"]]["really_correct"] == "yes" for row in rows),
                         "audit": f"{sum(float(row[run['key']]['my_judge']) for row in rows) / max(len(rows), 1):.1f}"}
        run.pop("bundle_path", None)
    media = []
    for task_id in order:
        items = {run["key"]: run_media(Path(run["bundle"]), run["key"], task_id, by_task[run["key"]].get(task_id, {}).get("judge"),
                                       out, files) for run in runs}
        if any(items.values()):
            media.append({"task": task_id, "text": config.get("media_text", {}).get(task_id, ""), "items": items})
    data = {"id": config.get("id", config_path.stem), "title": config.get("title", "Auditoria de runs"),
            "subtitle": config.get("subtitle", ""), "footer": config.get("footer", ""), "verdict": config.get("verdict", []),
            "runs": [{"key": run["key"], "label": run["label"], "totals": run["totals"]} for run in runs],
            "rows": rows, "gaps": [{"task": row["task"], "text": row["grader_issue"]} for row in rows if row.get("grader_issue")],
            "better": dict(Counter(row.get("better", "tie") for row in rows)), "media": media}
    template = (HERE / "template.html").read_text(encoding="utf-8")
    html = template.replace("__TITLE__", data["title"].replace("<", "&lt;")).replace(
        "__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    (out / "index.html").write_text(html, encoding="utf-8", newline="\n")
    (out / "files.json").write_text(json.dumps(files, indent=1), encoding="utf-8", newline="\n")
    return files


if __name__ == "__main__":
    if len(sys.argv) != 3:
        fail(f"received {sys.argv[1:]!r}; expected <audit.json> <out dir>")
    published = build(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"wrote {Path(sys.argv[2]) / 'index.html'} and {len(published)} asset(s); files.json lists them")
