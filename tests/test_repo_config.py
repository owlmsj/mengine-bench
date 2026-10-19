"""Repository shape: contributions are pull requests the owner reviews by hand."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_repo_runs_no_github_automation() -> None:
    # Workflows on pull_request run fork code, and the old required checks
    # blocked results-only PRs, so the repo ships none.
    github = REPO / ".github"
    automation = [path.relative_to(REPO).as_posix() for pattern in ("workflows/*", "CODEOWNERS", "dependabot.yml")
                  for path in github.glob(pattern)]
    assert automation == [], f"received GitHub automation {automation}; expected none"
