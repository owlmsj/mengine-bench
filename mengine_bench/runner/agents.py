"""Agent adapters: one interface over Claude Code, Codex CLI, opencode and any command.

Flags were read from each CLI's `--help` (claude 2.1, codex-cli 0.162,
opencode 2.0). Adapters only build argv lists (never shell strings) and parse
output; `process.run_process` launches them. Long prompts go through stdin
because inlined long-context documents exceed the Windows command-line limit.

A step succeeds only with exit 0 AND the adapter's terminal completion event
(claude `result` success, codex `turn.completed`, opencode `step_finish`
reason `stop`); a success-looking prefix of a truncated stream is a crash
(release review R16).

`judge_invocation` is the judge's argv (release review R17): judges read
agent-written evidence, so they run with tools, approvals and session
persistence off wherever the CLI allows it (flags read from claude 2.1.302,
codex-cli 0.162.1 and opencode 2.0.29 `--help`).
"""

from __future__ import annotations

import base64
import json
import mimetypes
import math
import shlex
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

AGENT_NAMES = ("claude", "codex", "opencode", "cmd")
# Stay well under the 32767-char Windows command line with flags and paths.
ARGV_PROMPT_LIMIT = 24_000
VERSION_TIMEOUT_S = 20


class AgentError(RuntimeError):
    """The agent ran but its output is not a successful final answer."""


@dataclass(frozen=True)
class Invocation:
    argv: list[str]
    stdin_text: str | None
    # Extra environment on top of the caller's; None keeps it unchanged.
    env: Mapping[str, str] | None = None


@dataclass(frozen=True)
class Usage:
    """Token counts share one meaning across harnesses (#23): input_tokens is
    every prompt token including cache reads and writes, as Codex reports it;
    cached_input_tokens is the part read from cache."""

    input_tokens: int | None
    cached_input_tokens: int | None
    output_tokens: int | None
    reasoning_tokens: int | None
    cost_usd: float | None
    cost_source: Literal["harness", "none", "partial"]


def _known_sum(values: Sequence[int | None]) -> int | None:
    if not values or any(value is None for value in values):
        return None
    return sum(value for value in values if value is not None)


def sum_usage(usages: Sequence[Usage]) -> Usage | None:
    if not usages:
        return None
    costs = [usage.cost_usd for usage in usages]
    cost = None if any(value is None for value in costs) else sum(value for value in costs if value is not None)
    source: Literal["harness", "none", "partial"] = "harness" if cost is not None else "none"
    if any(usage.cost_source == "partial" for usage in usages):
        source = "partial"
    return Usage(
        _known_sum([usage.input_tokens for usage in usages]),
        _known_sum([usage.cached_input_tokens for usage in usages]),
        _known_sum([usage.output_tokens for usage in usages]),
        _known_sum([usage.reasoning_tokens for usage in usages]), cost, source,
    )


def _usage_mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, dict) else {}


def _token_count(value: object) -> int | None:
    return value if type(value) is int and value >= 0 else None


def _usd_cost(value: object) -> float | None:
    if type(value) not in (int, float):
        return None
    try:
        cost = float(value)
    except OverflowError:
        return None
    return cost if math.isfinite(cost) and cost >= 0 else None


def _claude_usage(final: Mapping[str, object]) -> Usage:
    usage = _usage_mapping(final.get("usage"))
    details = _usage_mapping(usage.get("output_tokens_details"))
    cost = _usd_cost(final.get("total_cost_usd"))
    return Usage(
        _known_sum([_token_count(usage.get("input_tokens")), _token_count(usage.get("cache_creation_input_tokens")),
                    _token_count(usage.get("cache_read_input_tokens"))]),
        _token_count(usage.get("cache_read_input_tokens")), _token_count(usage.get("output_tokens")),
        _token_count(details.get("thinking_tokens")), cost, "harness" if cost is not None else "none",
    )


def _codex_usage(event: Mapping[str, object]) -> Usage:
    usage = _usage_mapping(event.get("usage"))
    return Usage(_token_count(usage.get("input_tokens")), _token_count(usage.get("cached_input_tokens")),
                 _token_count(usage.get("output_tokens")), _token_count(usage.get("reasoning_output_tokens")),
                 None, "none")


def _opencode_usage(part: object) -> Usage:
    finish = _usage_mapping(part)
    tokens = _usage_mapping(finish.get("tokens"))
    cache = _usage_mapping(tokens.get("cache"))
    cost = _usd_cost(finish.get("cost"))
    return Usage(
        _known_sum([_token_count(tokens.get("input")), _token_count(cache.get("write")),
                    _token_count(cache.get("read"))]),
        _token_count(cache.get("read")), _token_count(tokens.get("output")),
        _token_count(tokens.get("reasoning")), cost, "harness" if cost is not None else "none",
    )


@dataclass(frozen=True)
class Parsed:
    answer: str
    session_id: str | None
    usage: Usage | None = None


class Agent(Protocol):
    name: str
    model: str
    effort: str | None

    def invocation(self, prompt: str, prompt_file: Path, workspace: Path,
                   attachments: Sequence[str]) -> Invocation: ...

    def judge_invocation(self, prompt: str, workdir: Path, attachments: Sequence[str],
                         prompt_file: Path | None = None, system_prompt: str | None = None) -> Invocation: ...

    def parse(self, stdout: str, exit_code: int) -> Parsed: ...

    def version(self) -> str | None: ...


def _with_rules(prompt: str, system_prompt: str | None) -> str:
    """For a judge CLI with no system prompt flag."""
    return f"{system_prompt}\n\n{prompt}" if system_prompt else prompt


def split_jsonl(stdout: str) -> list[dict[str, object]]:
    """Parse JSONL on "\\n" only: str.splitlines would also split on U+2028
    inside JSON strings and corrupt the events."""
    events: list[dict[str, object]] = []
    for line in stdout.split("\n"):
        line = line.removesuffix("\r").strip()
        if not line.startswith("{"):
            continue  # CLIs interleave banners and warnings with the events.
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def _require_exit_zero(exit_code: int) -> None:
    if exit_code != 0:
        raise AgentError(f"received exit={exit_code}; expected exit=0")


def partial_answer(stdout: str) -> str:
    """The last reply in a stream stopped at its limit; plain output is its own reply."""
    events = split_jsonl(stdout)
    replies: list[object] = []
    known = False
    for event in events:
        kind = event.get("type")
        known = known or kind in ("text", "step_start", "step_finish", "tool_use", "assistant", "user", "turn.started",
                                  "turn.completed", "item.completed", "thread.started", "system")
        part, message, item = event.get("part"), event.get("message"), event.get("item")
        if kind == "text" and isinstance(part, dict):
            replies.append(part.get("text"))
        if kind == "assistant" and isinstance(message, dict) and isinstance(message.get("content"), list):
            replies += [block.get("text") for block in message["content"]
                        if isinstance(block, dict) and block.get("type") == "text"]
        if kind == "item.completed" and isinstance(item, dict) and item.get("type") == "agent_message":
            replies.append(item.get("text"))
    texts = [reply for reply in replies if isinstance(reply, str) and reply.strip()]
    if texts:
        return texts[-1]
    return "" if known else stdout


def parse_claude_stream(stdout: str, exit_code: int) -> Parsed:
    _require_exit_zero(exit_code)
    events = split_jsonl(stdout)
    results = [event for event in events if event.get("type") == "result"]
    if not results:
        raise AgentError(f"received no result event in {len(events)} events (exit={exit_code}); "
                         "expected a stream-json result")
    final = results[-1]
    if final.get("is_error") is not False or final.get("subtype") != "success":
        raise AgentError(f"received result subtype={final.get('subtype')!r} is_error={final.get('is_error')!r}; "
                         "expected subtype=success, is_error=false")
    answer = final.get("result")
    if not isinstance(answer, str) or not answer.strip():
        raise AgentError(f"received result={answer!r}; expected non-empty answer text")
    session = final.get("session_id")
    return Parsed(answer=answer, session_id=session if isinstance(session, str) else None, usage=_claude_usage(final))


def parse_codex_jsonl(stdout: str, exit_code: int) -> Parsed:
    events = split_jsonl(stdout)
    failed = [event for event in events if event.get("type") in ("turn.failed", "error")]
    if failed:
        raise AgentError(f"received {failed[-1].get('type')} event {json.dumps(failed[-1])[:200]}; "
                         "expected a completed turn")
    _require_exit_zero(exit_code)
    turns = [event.get("type") for event in events if event.get("type") in ("turn.started", "turn.completed")]
    if not turns or turns[-1] != "turn.completed":
        raise AgentError(f"received turn events {turns[-3:]} in {len(events)} events; "
                         "expected the stream to end with turn.completed")
    session = next((event.get("thread_id") for event in events if event.get("type") == "thread.started"), None)
    texts = [item.get("text") for event in events if event.get("type") == "item.completed"
             for item in [event.get("item")] if isinstance(item, dict) and item.get("type") == "agent_message"]
    answers = [text for text in texts if isinstance(text, str)]
    if not answers:
        raise AgentError(f"received no agent_message in {len(events)} events; expected a final message")
    usage = sum_usage([_codex_usage(event) for event in events if event.get("type") == "turn.completed"])
    return Parsed(answer=answers[-1], session_id=session if isinstance(session, str) else None, usage=usage)


def parse_opencode_jsonl(stdout: str, exit_code: int) -> Parsed:
    _require_exit_zero(exit_code)
    events = split_jsonl(stdout)
    errors = [event for event in events if event.get("type") == "error"]
    if errors:
        raise AgentError(f"received error event {json.dumps(errors[-1])[:200]}; expected successful JSONL")
    parts = [event.get("part") for event in events]
    finishes = [part for event, part in zip(events, parts) if event.get("type") == "step_finish"]
    if any(isinstance(part, dict) and part.get("reason") == "length" for part in finishes):
        raise AgentError("received step_finish reason=length; expected a complete answer")
    last = finishes[-1].get("reason") if finishes and isinstance(finishes[-1], dict) else None
    if last != "stop" and not _final_step_answered(events):
        raise AgentError(f"received last step_finish reason={last!r} in {len(events)} events; "
                         "expected a terminal step_finish with reason=stop")
    texts = [part.get("text") for event, part in zip(events, parts)
             if event.get("type") == "text" and isinstance(part, dict)]
    answer = "".join(text for text in texts if isinstance(text, str))
    if not answer.strip():
        raise AgentError(f"received no text in {len(events)} events; expected a non-empty answer")
    session = next((event.get("sessionID") for event in events if isinstance(event.get("sessionID"), str)), None)
    usage = sum_usage([_opencode_usage(part) for part in finishes])
    if _final_step_answered(events):
        previous = usage or Usage(None, None, None, None, None, "none")
        usage = Usage(previous.input_tokens, previous.cached_input_tokens, previous.output_tokens,
                      previous.reasoning_tokens, previous.cost_usd, "partial")
    return Parsed(answer=answer, session_id=session, usage=usage)


def _final_step_answered(events: list[dict[str, object]]) -> bool:
    """opencode 2.0.29 can drop the last step_finish: it returns on
    session.execution.succeeded (cli/src/run/noninteractive.ts), while failures and
    interruptions emit an error and exit 1. With exit 0 and no error event, a last
    step that started after every step_finish and produced text is complete."""
    kinds = [event.get("type") for event in events]
    starts = [index for index, kind in enumerate(kinds) if kind == "step_start"]
    finishes = [index for index, kind in enumerate(kinds) if kind == "step_finish"]
    if not starts or (finishes and finishes[-1] > starts[-1]):
        return False
    return any(kind == "text" for kind in kinds[starts[-1]:])


def _image_block(path: Path) -> dict[str, object]:
    media_type = mimetypes.guess_type(path.name)[0]
    if media_type not in ("image/png", "image/jpeg", "image/gif", "image/webp"):
        raise ValueError(f"received attachment {path.name!r} of type {media_type!r}; "
                         "expected a png/jpeg/gif/webp image")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}


def _executable(name: str) -> str:
    # Windows installs agent CLIs as .cmd/.exe shims that Popen cannot find by bare name.
    return shutil.which(name) or name


def _cli_version(name: str) -> str | None:
    try:
        proc = subprocess.run([_executable(name), "--version"], capture_output=True, text=True,
                              timeout=VERSION_TIMEOUT_S, check=False, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return None
    lines = proc.stdout.strip().splitlines()
    return lines[0] if proc.returncode == 0 and lines else None


@dataclass
class ClaudeAgent:
    """Claude Code in print mode; stream-json requires --verbose."""

    model: str
    effort: str | None
    name: str = "claude"

    def invocation(self, prompt: str, prompt_file: Path, workspace: Path,
                   attachments: Sequence[str]) -> Invocation:
        # Attachments are named in the prompt; Claude Code reads images with its Read tool.
        argv = [_executable("claude"), "-p", "--output-format", "stream-json", "--verbose", "--model", self.model]
        if self.effort:
            argv += ["--effort", self.effort]
        argv += ["--permission-mode", "bypassPermissions"]
        return Invocation(argv=argv, stdin_text=prompt)

    def judge_invocation(self, prompt: str, workdir: Path, attachments: Sequence[str],
                         prompt_file: Path | None = None, system_prompt: str | None = None) -> Invocation:
        # --tools "" removes every built-in tool; --restricted also drops user,
        # project and local settings (hooks) and --strict-mcp-config every MCP
        # server. Without a Read tool, images travel inline as stream-json
        # content blocks.
        argv = [_executable("claude"), "-p", "--output-format", "stream-json", "--verbose", "--model", self.model]
        if self.effort:
            argv += ["--effort", self.effort]
        argv += ["--tools", "", "--restricted", "--strict-mcp-config", "--permission-mode", "dontAsk",
                 "--no-session-persistence"]
        if system_prompt:
            # Replaces Claude Code's own prompt, which describes tools a judge does not have (#70).
            argv += ["--system-prompt", system_prompt]
        if not attachments:
            return Invocation(argv=argv, stdin_text=prompt)
        blocks: list[dict[str, object]] = [{"type": "text", "text": prompt}]
        blocks += [_image_block(workdir / attachment) for attachment in attachments]
        message = {"type": "user", "message": {"role": "user", "content": blocks}}
        return Invocation(argv=[*argv, "--input-format", "stream-json"], stdin_text=json.dumps(message) + "\n")

    def parse(self, stdout: str, exit_code: int) -> Parsed:
        return parse_claude_stream(stdout, exit_code)

    def version(self) -> str | None:
        return _cli_version("claude")


CODEX_JUDGE_DISABLED_FEATURES = ("shell_tool", "unified_exec", "apps", "browser_use", "browser_use_external",
                                 "computer_use", "in_app_browser")
# opencode has no tool-off flag; an inline config denies every tool permission
# and `run` without --auto rejects anything that would ask.
OPENCODE_JUDGE_CONFIG = {"permission": {"edit": "deny", "bash": "deny", "webfetch": "deny", "websearch": "deny",
                                        "external_directory": "deny", "task": "deny"}}


@dataclass
class CodexAgent:
    """`codex exec --json`, one fresh session per step."""

    model: str
    effort: str | None
    name: str = "codex"

    def invocation(self, prompt: str, prompt_file: Path, workspace: Path,
                   attachments: Sequence[str]) -> Invocation:
        argv = [_executable("codex"), "exec"]
        argv += ["--json", "--skip-git-repo-check", "-m", self.model]
        if self.effort:
            argv += ["-c", f'model_reasoning_effort="{self.effort}"']
        # Parity with Claude's bypassPermissions: the task workspace is the sandbox.
        argv.append("--dangerously-bypass-approvals-and-sandbox")
        for attachment in attachments:
            argv += ["-i", attachment]
        argv.append("-")
        return Invocation(argv=argv, stdin_text=prompt)

    def judge_invocation(self, prompt: str, workdir: Path, attachments: Sequence[str],
                         prompt_file: Path | None = None, system_prompt: str | None = None) -> Invocation:
        # Codex cannot drop every tool: read-only sandbox (no writes, no
        # network), no user config/MCP/rules, no session files, and the
        # command, app and browser features off.
        argv = [_executable("codex"), "exec", "--json", "--skip-git-repo-check", "--ephemeral",
                "--ignore-user-config", "--ignore-rules", "--sandbox", "read-only"]
        for feature in CODEX_JUDGE_DISABLED_FEATURES:
            argv += ["--disable", feature]
        argv += ["-m", self.model]
        if self.effort:
            argv += ["-c", f'model_reasoning_effort="{self.effort}"']
        for attachment in attachments:
            argv += ["-i", attachment]
        argv.append("-")
        return Invocation(argv=argv, stdin_text=_with_rules(prompt, system_prompt))

    def parse(self, stdout: str, exit_code: int) -> Parsed:
        return parse_codex_jsonl(stdout, exit_code)

    def version(self) -> str | None:
        return _cli_version("codex")


@dataclass
class OpencodeAgent:
    """`opencode run --format json`; effort maps to the model variant (`model#effort`).

    --standalone keeps runs off any shared background server.
    """

    model: str
    effort: str | None
    name: str = "opencode"

    def invocation(self, prompt: str, prompt_file: Path, workspace: Path,
                   attachments: Sequence[str]) -> Invocation:
        model = f"{self.model}#{self.effort}" if self.effort else self.model
        argv = [_executable("opencode"), "run", "--standalone", "--auto", "--format", "json", "-m", model]
        for attachment in attachments:
            argv += ["--file", attachment]
        if len(prompt) > ARGV_PROMPT_LIMIT:
            return Invocation(argv=argv, stdin_text=prompt)
        return Invocation(argv=[*argv, prompt], stdin_text=None)

    def judge_invocation(self, prompt: str, workdir: Path, attachments: Sequence[str],
                         prompt_file: Path | None = None, system_prompt: str | None = None) -> Invocation:
        prompt = _with_rules(prompt, system_prompt)
        model = f"{self.model}#{self.effort}" if self.effort else self.model
        argv = [_executable("opencode"), "run", "--standalone", "--format", "json", "-m", model]
        for attachment in attachments:
            argv += ["--file", attachment]
        env = {"OPENCODE_CONFIG_CONTENT": json.dumps(OPENCODE_JUDGE_CONFIG)}
        if len(prompt) > ARGV_PROMPT_LIMIT:
            return Invocation(argv=argv, stdin_text=prompt, env=env)
        return Invocation(argv=[*argv, prompt], stdin_text=None, env=env)

    def parse(self, stdout: str, exit_code: int) -> Parsed:
        return parse_opencode_jsonl(stdout, exit_code)

    def version(self) -> str | None:
        return _cli_version("opencode")


CMD_PLACEHOLDERS = ("{prompt_file}", "{workspace}", "{model}", "{effort}")


@dataclass
class CmdAgent:
    """Any command: the template is a JSON argv list or a POSIX-quoted string.

    Placeholders are substituted per argument after splitting, so paths with
    spaces stay one argument. The answer is the trimmed stdout.
    """

    template: str
    model: str
    effort: str | None
    name: str = "cmd"

    def __post_init__(self) -> None:
        argv = self._split()
        if not argv or not any("{prompt_file}" in arg for arg in argv):
            raise ValueError(f"received cmd template {self.template!r}; expected an argv containing {{prompt_file}}")

    def _split(self) -> list[str]:
        if self.template.lstrip().startswith("["):
            parsed = json.loads(self.template)
            if not isinstance(parsed, list) or not all(isinstance(arg, str) for arg in parsed):
                raise ValueError(f"received cmd template {self.template!r}; expected a JSON list of strings")
            return parsed
        return shlex.split(self.template)

    def invocation(self, prompt: str, prompt_file: Path, workspace: Path,
                   attachments: Sequence[str]) -> Invocation:
        values = {"{prompt_file}": str(prompt_file), "{workspace}": str(workspace),
                  "{model}": self.model, "{effort}": self.effort or ""}
        argv = []
        for arg in self._split():
            for placeholder, value in values.items():
                arg = arg.replace(placeholder, value)
            argv.append(arg)
        return Invocation(argv=argv, stdin_text=None)

    def judge_invocation(self, prompt: str, workdir: Path, attachments: Sequence[str],
                         prompt_file: Path | None = None, system_prompt: str | None = None) -> Invocation:
        # A user command's tool policy is the user's own; judge.py still runs
        # it in an empty cwd with the prompt file outside that cwd.
        if prompt_file is None:
            raise ValueError("received no prompt_file for a cmd judge; expected the {prompt_file} path")
        return self.invocation(prompt, prompt_file, workdir, attachments)

    def parse(self, stdout: str, exit_code: int) -> Parsed:
        _require_exit_zero(exit_code)
        return Parsed(answer=stdout.strip(), session_id=None)

    def version(self) -> str | None:
        # A user command has no reliable version flag; results record "cmd" only.
        return None


def make_agent(name: str, model: str, effort: str | None, cmd_template: str | None) -> Agent:
    if name == "claude":
        return ClaudeAgent(model=model, effort=effort)
    if name == "codex":
        return CodexAgent(model=model, effort=effort)
    if name == "opencode":
        return OpencodeAgent(model=model, effort=effort)
    if name == "cmd":
        if not cmd_template:
            raise ValueError("received agent 'cmd' without a template; expected --cmd TEMPLATE")
        return CmdAgent(template=cmd_template, model=model, effort=effort)
    raise ValueError(f"received agent {name!r}; expected one of {AGENT_NAMES}")
