"""Shared inflation budget for submitted archives and gzip transcripts.

Bundles come from strangers: a 25 MiB bundle must not inflate into gigabytes
or millions of tar members on a verify runner or in privacy-scan (review R09).
One budget spans a whole bundle and the first overrun raises, so callers
stop instead of reading on.
"""

from __future__ import annotations

import gzip
import io
import tarfile
from collections.abc import Iterator
from typing import BinaryIO

UNPACK_BYTES_CAP = 200 * 10**6
UNPACK_MEMBERS_CAP = 5000
_CHUNK = 2**20


class UnpackBudgetExceeded(ValueError):
    pass


class UnpackBudget:
    """Caps read at construction so a test can lower the module constants."""

    def __init__(self) -> None:
        self.bytes_cap, self.members_cap = UNPACK_BYTES_CAP, UNPACK_MEMBERS_CAP
        self.bytes_used = self.members_used = 0

    def charge_bytes(self, count: int, label: str) -> None:
        self.bytes_used += count
        if self.bytes_used > self.bytes_cap:
            raise UnpackBudgetExceeded(f"{label}: received {self.bytes_used} uncompressed bytes so far; "
                                       f"expected at most {self.bytes_cap} per bundle")

    def charge_member(self, label: str) -> None:
        self.members_used += 1
        if self.members_used > self.members_cap:
            raise UnpackBudgetExceeded(f"{label}: received {self.members_used} archive members so far; "
                                       f"expected at most {self.members_cap} per bundle")


def read_gzip_bounded(source: BinaryIO, budget: UnpackBudget, label: str) -> bytes:
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=source, mode="rb") as stream:
        while chunk := stream.read(_CHUNK):
            budget.charge_bytes(len(chunk), label)
            out.write(chunk)
    return out.getvalue()


def iter_tar_bounded(source: BinaryIO, budget: UnpackBudget,
                     label: str) -> Iterator[tuple[tarfile.TarInfo, bytes | None]]:
    """(member, body or None for non-files); lazy iteration, never getmembers()."""
    with tarfile.open(fileobj=source, mode="r:gz") as archive:
        for member in archive:
            budget.charge_member(label)
            if not member.isfile():
                yield member, None
                continue
            # Charge the declared size before reading so a huge member is never buffered.
            budget.charge_bytes(member.size, label)
            stream = archive.extractfile(member)
            yield member, stream.read() if stream is not None else b""
