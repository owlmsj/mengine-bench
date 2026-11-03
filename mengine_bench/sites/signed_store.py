"""Signed site state: an append-only journal and a state file only the server process can sign (#153).

The server gets a per-run key on stdin, never through argv, the environment or a file, so an agent that
edits `site-data/state.json` or `site-data/journal.jsonl` cannot sign the edit. The runner writes the key
to `site-data/grader.key` only after the server is gone, for the grader. Each journal line is chained to
the previous one, so dropping, reordering or editing a line breaks every later signature, and the state
must equal the journal replayed, so a signed state that disagrees with its journal fails too.

Stdlib only: this module runs inside the site server process.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import threading
from collections.abc import Callable
from pathlib import Path

DATA_DIR = "site-data"
SERVED_DIR = "site"
STATE_FILE = "state.json"
JOURNAL_FILE = "journal.jsonl"
KEY_FILE = "grader.key"
SERVER_FILE = "server.json"

SiteState = dict[str, object]
SiteEvent = dict[str, object]
# A pure function: the server and the grader replay the same events with it.
ApplyEvent = Callable[[SiteState, SiteEvent], SiteState]


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sign(key: bytes, previous: str, payload: object) -> str:
    return hmac.new(key, previous.encode("ascii") + canonical(payload), hashlib.sha256).hexdigest()


def replay(events: list[SiteEvent], apply: ApplyEvent) -> SiteState:
    if not events or events[0].get("type") != "seed":
        raise ValueError(f"received first event {events[:1]!r}; expected a seed event")
    state = json.loads(json.dumps(events[0]["state"]))
    for event in events[1:]:
        state = apply(state, event)
    return state


class SignedStore:
    """The server's writer: every mutation is one signed journal line, then the signed state."""

    def __init__(self, data_dir: Path, key: bytes, apply: ApplyEvent, seed: SiteState) -> None:
        self._dir, self._key, self._apply = data_dir, key, apply
        self._lock = threading.Lock()
        self._seq, self._last = 0, ""
        self._dir.mkdir(parents=True, exist_ok=True)
        # A fresh journal per server start: an earlier one was signed with another run's key.
        (self._dir / JOURNAL_FILE).write_bytes(b"")
        self.state: SiteState = {}
        self.record({"type": "seed", "state": seed})

    def record(self, event: SiteEvent) -> SiteState:
        with self._lock:
            state = replay([event], self._apply) if event.get("type") == "seed" else self._apply(self.state, event)
            entry = {"seq": self._seq, "event": event}
            self._last = sign(self._key, self._last, entry)
            with (self._dir / JOURNAL_FILE).open("ab") as journal:
                journal.write(canonical({**entry, "mac": self._last}) + b"\n")
            self._seq += 1
            self.state = state
            signed = {"state": state, "journal_mac": self._last, "mac": sign(self._key, self._last, state)}
            temporary = self._dir / (STATE_FILE + ".tmp")
            temporary.write_bytes(canonical(signed))
            os.replace(temporary, self._dir / STATE_FILE)
            return state


def verify(data_dir: Path, key: bytes, apply: ApplyEvent) -> tuple[SiteState, list[SiteEvent]]:
    """The replayed state and the events, or ValueError naming the first thing that is not the server's."""
    journal, state_file = data_dir / JOURNAL_FILE, data_dir / STATE_FILE
    if not journal.is_file() or not state_file.is_file():
        raise ValueError(f"received no {DATA_DIR}/{JOURNAL_FILE} or {STATE_FILE}; expected both from the site server")
    events: list[SiteEvent] = []
    last = ""
    for number, line in enumerate(journal.read_bytes().splitlines()):
        try:
            entry = json.loads(line)
        except ValueError as error:
            raise ValueError(f"received unreadable journal line {number}: {line[:80]!r}; expected JSON") from error
        mac = entry.pop("mac", "") if isinstance(entry, dict) else ""
        if entry.get("seq") != number or not hmac.compare_digest(str(mac), sign(key, last, entry)):
            raise ValueError(f"received journal line {number} not signed by the server; expected an intact chain")
        last = str(mac)
        events.append(entry["event"])
    try:
        stored = json.loads(state_file.read_bytes())
    except ValueError as error:
        raise ValueError(f"received unreadable {STATE_FILE}; expected the server's JSON") from error
    if not isinstance(stored, dict) or stored.get("journal_mac") != last or not hmac.compare_digest(
            str(stored.get("mac", "")), sign(key, last, stored.get("state"))):
        raise ValueError(f"received {STATE_FILE} not signed by the server for the last journal line; expected it")
    replayed = replay(events, apply)
    if canonical(replayed) != canonical(stored["state"]):
        raise ValueError(f"received {STATE_FILE} that differs from the journal replayed; expected the same state")
    return replayed, events
