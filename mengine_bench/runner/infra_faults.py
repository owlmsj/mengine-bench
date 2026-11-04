"""Known host refusals from published #181 transcripts and the #164 snapshot note."""

from collections.abc import Iterable

INFRA_SIGNATURES = (
    "only files this session is allowed to read can be uploaded",
    "fileChooser.setFiles failed",
    "filesystem snapshot unavailable",
)


def infra_fault(stdout_of_steps: Iterable[str]) -> str | None:
    """Return the first exact host refusal, without changing any grade."""
    for stream in stdout_of_steps:
        for signature in INFRA_SIGNATURES:
            if signature in stream:
                return signature
    return None
