"""Filesystem evidence in the task's isolated parent and run directory (#164)."""

from __future__ import annotations

import os
import stat
from pathlib import Path

WORKSPACE_WRITE_GATE = "no writes outside the task workspace"
FileStamp = tuple[int, int, int]


def _snapshot_error(error: OSError) -> None:
    raise error


def outside_snapshot(workspace: Path, root: Path) -> dict[str, FileStamp]:
    """Do not follow links or read contents; tool installations may be read freely.

    This detects surviving changes in task-owned directories, not writes anywhere
    on the host or files created and removed between snapshots (#164).
    """
    stamps: dict[str, FileStamp] = {}
    for label, parent in (("parent", workspace.parent), ("run", root)):
        for directory, dirs, files in os.walk(parent, followlinks=False, onerror=_snapshot_error):
            base = Path(directory)
            dirs[:] = [name for name in dirs if base / name != workspace]
            for name in [*dirs, *files]:
                path = base / name
                info = path.lstat()
                # Directory timestamps include workspace changes, so only their existence/type counts.
                stamp = (info.st_mode, 0, 0) if stat.S_ISDIR(info.st_mode) else (info.st_mode, info.st_size, info.st_mtime_ns)
                stamps[f"{label}/{path.relative_to(parent).as_posix()}"] = stamp
    return stamps


def outside_changes(before: dict[str, FileStamp], after: dict[str, FileStamp]) -> list[str]:
    return sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
