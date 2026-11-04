"""Known host refusals from published #181 transcripts and the #164 snapshot note."""

from collections.abc import Iterable, Sequence

# #181: what a browser tool answered when the host refused the upload; only a tool's output carries it (#185).
TOOL_SIGNATURES = (
    "only files this session is allowed to read can be uploaded",
    "fileChooser.setFiles failed",
)
# #164: written by the runner into TaskRunRecord.outside_unmeasured, never by the agent's stream.
SNAPSHOT_SIGNATURE = "filesystem snapshot unavailable"
INFRA_SIGNATURES = (*TOOL_SIGNATURES, SNAPSHOT_SIGNATURE)


def infra_fault(texts: Iterable[str]) -> str | None:
    """The first known signature in runner-written texts (published flags), without changing any grade."""
    for text in texts:
        for signature in INFRA_SIGNATURES:
            if signature in text:
                return signature
    return None


def task_infra_fault(streams: Sequence[str], snapshot_note: str | None) -> str | None:
    """A host refusal in a tool call's output, else the runner's snapshot note; the model's prose never counts (#185)."""
    from mengine_bench.judge_view import tool_outputs

    for output in tool_outputs(list(streams)):
        for signature in TOOL_SIGNATURES:
            if signature in output:
                return signature
    if snapshot_note is not None and SNAPSHOT_SIGNATURE in snapshot_note:
        return SNAPSHOT_SIGNATURE
    return None
