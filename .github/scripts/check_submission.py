"""Results-only policy for result PRs.

Input: the PR's changed files as TSV `status<TAB>filename[<TAB>previous_filename]`
(GitHub pulls/files API). Passes only when every path, including the old side
of a rename, lies inside exactly one newly added `results/<suite>/<bundle>/`.
Stdlib only: the workflow runs it from the base-branch checkout before `uv sync`.
On success prints the bundle dir; on failure prints the reasons and exits 1.
"""

from __future__ import annotations

import sys
from pathlib import Path

LEADERBOARD = "LEADERBOARD.md"


def _bundle_of(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) < 4 or parts[0] != "results" or "" in parts or ".." in parts:
        return None
    return "/".join(parts[:3])


def check_submission(changed_tsv: Path) -> tuple[int, str]:
    problems: list[str] = []
    bundles: set[str] = set()
    for row in changed_tsv.read_text(encoding="utf-8").split("\n"):
        if not row.strip():
            continue
        status, *paths = row.split("\t")
        for path in filter(None, paths):
            if path == LEADERBOARD:
                problems.append(f"{LEADERBOARD} is generated on main; do not edit it in a pull request")
                continue
            bundle = _bundle_of(path)
            if bundle is None:
                problems.append(f"{path}: outside results/<suite>/<bundle>/; code, docs and workflow "
                                "changes go in a separate PR reviewed by the maintainers")
                continue
            if status != "added":
                problems.append(f"{path}: bundles are immutable; received status {status!r}, expected 'added'")
            bundles.add(bundle)
    if len(bundles) != 1:
        problems.append(f"expected exactly one new bundle directory, found {len(bundles)}: {sorted(bundles)}")
    if problems:
        return 1, "\n".join(problems)
    return 0, bundles.pop()


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(f"usage: check_submission.py CHANGED_TSV; received {argv!r}", file=sys.stderr)
        return 2
    code, message = check_submission(Path(argv[0]))
    print(message, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
