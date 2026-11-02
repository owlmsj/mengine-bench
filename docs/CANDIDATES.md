# Candidates outside the catalog (#127)

These tasks are not ranked. Promotion and an Opus probe belong to the owner.

## cmp-meeting-decisions

Adds business decisions, owners, deadlines and conditional hiring to the
technical handoff tested by `cmp-handoff`, its closest catalog task.
Expected agent time: not measured; timeout 180 seconds per step.
Saturation risk: high for strong readers; the final decisions are explicit.
Diagnose by comparing `result.json` and `DECISIONS.md` with the decision turns
in `meetings/2026-06-30-ops.md`; distinguish the proposed price from the adopted
price and check the currency magnitude and the designer's quarter and threshold.

## cmp-agent-trajectory

Adds chronological tool-event reconstruction to `cmp-handoff`, its closest
catalog task: the last file read is not the last file edited, and the last
test supersedes earlier passes. Expected agent time: not measured; timeout
180 seconds per step. Saturation risk: medium to high; a short event stream
with explicit final markers may be easy for strong agents.
Diagnose by reading steps 96, 150 and 157-159 in `agent/trajectory.jsonl`, then
compare `STATE.md` and the five fields in `result.json`.
