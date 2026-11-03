"""Quillmail: an invented look-alike of a big webmail app, for `cu-webmail` (#153).

Same shapes as the real kind of site: a signed-in session cookie set by the app page, an anti-CSRF token the page
carries and every write must echo in a header, a client-rendered inbox over a JSON API, threads with labels
(archive = drop INBOX), attachments served for download and replies sent into the thread. Every person, company,
address and amount is fictional, under the reserved `.test` domain. Stdlib only; run with
`python -m mengine_bench.sites.quillmail`.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
import threading
import time
import zlib
from urllib.parse import parse_qs, quote, urlsplit

from mengine_bench.sites.server_base import SiteHandler, serve
from mengine_bench.sites.signed_store import SERVED_DIR, SiteEvent, SiteState

SELF = {"name": "Bench Tester", "email": "tester@quillmail.test"}
SESSION_COOKIE = "QMSID"
CSRF_HEADER = "X-Qm-At"
CSRF_META = "qm-at"
LABELS = ("INBOX", "UNREAD", "STARRED", "IMPORTANT", "TRASH", "SENT")
MAX_BODY_CHARS = 20_000
EMAIL_PATTERN = re.compile(r"^[^@\s<>]+@[^@\s<>]+\.[a-z]+$", re.IGNORECASE)


# ------------------------------------------------------------------ fixture PDFs ----


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def quillmail_pdf(title: str, lines: list[tuple[str, str]]) -> bytes:
    """A one-page A4 PDF of label/amount rows in Helvetica, Flate-compressed like a real invoice tool writes it."""
    ops = ["BT", "/F2 18 Tf", "56 780 Td", f"({_pdf_escape(title)}) Tj", "ET"]
    y = 740
    for left, right in lines:
        font = "/F2 11 Tf" if left.startswith(("Total", "TOTAL")) else "/F1 11 Tf"
        ops += ["BT", font, f"56 {y} Td", f"({_pdf_escape(left)}) Tj", "ET"]
        if right:
            ops += ["BT", font, f"420 {y} Td", f"({_pdf_escape(right)}) Tj", "ET"]
        y -= 18 if left else 10
    stream = zlib.compress("\n".join(ops).encode("latin-1"), 9)
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> "
        b"/Contents 6 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
        b"<< /Length " + str(len(stream)).encode() + b" /Filter /FlateDecode >>\nstream\n" + stream + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets)
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


INVOICE_TOTAL = "1,205.77"
ATTACHMENT_FILES: dict[str, bytes] = {
    "LP-2026-0418.pdf": quillmail_pdf("Larkspur Print Co. - Invoice LP-2026-0418", [
        ("Invoice date: 2026-10-28", ""), ("Bill to: Tidewater Studio", ""), ("Payment terms: 30 days", ""), ("", ""),
        ("A5 brochure, 2,000 copies", "EUR 812.00"), ("Folding and trimming", "EUR 146.50"),
        ("Delivery", "EUR 38.00"), ("", ""), ("Subtotal", "EUR 996.50"), ("VAT 21%", "EUR 209.27"),
        ("Total due", f"EUR {INVOICE_TOTAL}")]),
    # Same vendor, a quote rather than an invoice: the plausible wrong attachment.
    "Q-2026-311.pdf": quillmail_pdf("Larkspur Print Co. - Quote Q-2026-311", [
        ("Quote date: 2026-10-30", ""), ("Valid for 30 days", ""), ("", ""),
        ("Winter catalogue, 48 pages, 1,500 copies", "EUR 1,934.71"), ("", ""),
        ("Subtotal", "EUR 1,934.71"), ("VAT 21%", "EUR 406.29"), ("Total", "EUR 2,341.00")]),
    "FH-88213.pdf": quillmail_pdf("Fernbrook Hosting - Invoice FH-88213", [
        ("Invoice date: 2026-10-31", ""), ("Plan: Studio VPS, October", "EUR 53.64"), ("", ""),
        ("Subtotal", "EUR 53.64"), ("VAT 21%", "EUR 11.26"), ("Total due", "EUR 64.90")]),
}


def _attachment(att_id: str, filename: str) -> dict[str, object]:
    body = ATTACHMENT_FILES[filename]
    return {"id": att_id, "filename": filename, "mimeType": "application/pdf", "size": len(body),
            "sha256": hashlib.sha256(body).hexdigest()}


def _person(name: str, email: str) -> dict[str, str]:
    return {"name": name, "email": email}


def _thread(thread_id: str, subject: str, labels: list[str], sender: dict[str, str], date: str, body: str,
            attachments: list[dict[str, object]] | None = None) -> dict[str, object]:
    message = {"id": f"m{thread_id}", "from": sender, "to": [SELF], "date": date, "subject": subject,
               "body": body, "attachments": attachments or []}
    return {"id": thread_id, "subject": subject, "labels": labels, "messages": [message]}


WREN = _person("Wren Halloway", "wren@larkspur-print.test")
BILLING = _person("Larkspur Print Co. Billing", "billing@larkspur-print.test")
TARGET_THREAD = "19a2f4c81e7b30d5"
QUOTE_THREAD = "19a37be20c4d91aa"
SEED: SiteState = {"next_message": 1, "threads": [
    _thread("19a4108d2b6ce7f0", "Lunch on Thursday?", ["INBOX", "UNREAD"], _person("Ines Varga", "ines@tidewater.test"),
            "2026-11-03T08:12:00Z", "Shall we try the new noodle place on Thursday at 12:30? Teo is in too."),
    _thread("19a3fe617ad0c2b8", "Your invoice FH-88213", ["INBOX", "UNREAD"],
            _person("Fernbrook Hosting", "billing@fernbrook-hosting.test"), "2026-11-02T22:40:00Z",
            "Hello,\n\nYour invoice FH-88213 for October is attached. It will be charged to the card on file on "
            "November 7.\n\nFernbrook Hosting", [_attachment("fh1", "FH-88213.pdf")]),
    _thread(QUOTE_THREAD, "Quote for the winter catalogue", ["INBOX", "UNREAD"], WREN, "2026-11-02T16:05:00Z",
            "Hi,\n\nAs promised, here is our quote Q-2026-311 for the winter catalogue. Happy to adjust the paper "
            "stock if you need a lower price.\n\nBest,\nWren Halloway\nLarkspur Print Co.",
            [_attachment("q1", "Q-2026-311.pdf")]),
    _thread("19a3c09f55e1b647", "Autumn paper samples are here", ["INBOX"],
            _person("Larkspur Print Co.", "news@larkspur-print.test"), "2026-11-01T09:00:00Z",
            "New this season: recycled linen stock and three matte finishes. Orders over EUR 500.00 ship free until "
            "the end of November. Ask your account manager for a sample pack."),
    _thread("19a39d1ab08e4c32", "Your parcel is on its way", ["INBOX"],
            _person("Parcelfox", "updates@parcelfox.test"), "2026-10-31T14:22:00Z",
            "Parcel PF-5521-0087 left our depot and arrives tomorrow between 10:00 and 14:00."),
    _thread(TARGET_THREAD, "Invoice LP-2026-0418 for the October print run", ["INBOX", "UNREAD"], BILLING,
            "2026-10-29T10:31:00Z",
            "Dear Tidewater Studio,\n\nPlease find attached our invoice LP-2026-0418 for the October brochure print "
            "run. Payment terms are 30 days from the invoice date.\n\nKind regards,\nLarkspur Print Co. Billing",
            [_attachment("lp1", "LP-2026-0418.pdf")]),
    _thread("19a2d771c3f09e18", "Agenda for the studio meeting", ["INBOX", "STARRED"],
            _person("Teo Marsh", "teo@tidewater.test"), "2026-10-28T17:45:00Z",
            "1. Print run review\n2. Winter catalogue timeline\n3. Holiday rota\n\nAdd anything by Friday."),
    _thread("19a28ab4e6170fd3", "Re: Brochure proofs", ["INBOX"], WREN, "2026-10-27T11:10:00Z",
            "Proofs approved on our side too. The run starts Monday; delivery should reach you by the 28th."),
    _thread("19a24f0e9d3b2c71", "Weekly digest: 5 new comments", ["INBOX"],
            _person("Boardly", "digest@boardly.test"), "2026-10-26T07:00:00Z",
            "Ines Varga and 2 others commented on the 'Winter catalogue' board this week."),
    _thread("19a1e2c35f8a6b04", "Studio Wi-Fi password change", ["INBOX", "IMPORTANT"],
            _person("Ines Varga", "ines@tidewater.test"), "2026-10-24T15:30:00Z",
            "The guest network password changes on Monday. The new one is on the whiteboard, not in email."),
    _thread("19a19b0d27c4e8f6", "Invitation: Print run review", ["INBOX"],
            _person("Teo Marsh", "teo@tidewater.test"), "2026-10-22T09:15:00Z",
            "Teo Marsh invited you to Print run review, Thursday 30 October, 15:00 to 15:30."),
    _thread("19a15c6e0b9d3a27", "Welcome to Quillmail", [],
            _person("Quillmail Team", "team@quillmail.test"), "2026-10-01T08:00:00Z",
            "Your mailbox is ready. Archived mail lives in All Mail; nothing is ever deleted unless you empty Trash."),
]}


# --------------------------------------------------------------------- state ----


def _find_thread(threads: list[dict[str, object]], thread_id: object) -> dict[str, object]:
    found = next((thread for thread in threads if thread["id"] == thread_id), None)
    if found is None:
        raise ValueError(f"received thread id {thread_id!r}; expected one of the mailbox's threads")
    return found


def apply_quillmail(state: SiteState, event: SiteEvent) -> SiteState:
    """The one state transition, shared by the server and the grader's replay; `route` is an observation only."""
    threads = json.loads(json.dumps(state["threads"]))
    next_message = int(state["next_message"])  # type: ignore[call-overload]
    kind = event.get("type")
    if kind == "modify":
        thread = _find_thread(threads, event["thread"])
        labels = [label for label in thread["labels"] if label not in event["remove"]]  # type: ignore[union-attr]
        thread["labels"] = labels + [label for label in event["add"] if label not in labels]  # type: ignore[union-attr]
    elif kind == "send":
        message = event["message"]
        if event.get("thread"):
            thread = _find_thread(threads, event["thread"])
            thread["messages"].append(message)  # type: ignore[union-attr]
            thread["labels"] += [] if "SENT" in thread["labels"] else ["SENT"]  # type: ignore[operator]
        else:
            threads.insert(0, {"id": f"sent{next_message:04d}", "subject": message["subject"],  # type: ignore[index]
                               "labels": ["SENT"], "messages": [message]})
        next_message += 1
    else:
        raise ValueError(f"received event type {kind!r}; expected modify or send")
    return {"next_message": next_message, "threads": threads}


# -------------------------------------------------------------------- server ----


class QuillmailHandler(SiteHandler):
    sessions: set[str] = set()
    sessions_lock = threading.Lock()
    csrf_secret = secrets.token_bytes(32)

    # -------------------------------------------------------- session --
    def _cookie_session(self) -> str | None:
        for part in (self.headers.get("Cookie") or "").split(";"):
            name, _, value = part.strip().partition("=")
            if name == SESSION_COOKIE and value in self.sessions:
                return value
        return None

    def _csrf_for(self, session: str) -> str:
        return hmac.new(self.csrf_secret, session.encode("ascii"), hashlib.sha256).hexdigest()[:40]

    def _send_app(self) -> None:
        """The app page: signs the browser in (the account's saved session) and carries the write token."""
        session = self._cookie_session()
        fresh = session is None
        if session is None:
            session = secrets.token_urlsafe(24)
            with self.sessions_lock:
                self.sessions.add(session)
        page = (self.workspace / SERVED_DIR / "index.html").read_text(encoding="utf-8")
        page = page.replace("__QM_AT__", self._csrf_for(session))
        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if fresh:
            self.send_header("Set-Cookie", f"{SESSION_COOKIE}={session}; Path=/; HttpOnly; SameSite=Lax")
        self.end_headers()
        self.wfile.write(body)

    def _signed_in(self) -> str | None:
        session = self._cookie_session()
        if session is None:
            self.send_json(401, {"error": "unauthenticated", "message": "Not signed in: open the app page first."})
        return session

    def _route(self) -> dict[str, str]:
        """How the write arrived, for the record only: never a grade (#153)."""
        names = ("User-Agent", "Origin", "Sec-Fetch-Site", "Sec-Fetch-Mode", "Sec-Fetch-Dest")
        return {name.lower(): (self.headers.get(name) or "")[:120] for name in names if self.headers.get(name)}

    # ---------------------------------------------------------- routes --
    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's name
        parts = urlsplit(self.path)
        query = {name: values[-1] for name, values in parse_qs(parts.query).items()}
        if parts.path.startswith("/assets/") or parts.path == "/favicon.ico":
            self.serve_static()
            return
        if not parts.path.startswith("/mail/api/") and parts.path != "/mail/u/0/attachment":
            self._send_app()
            return
        if self._signed_in() is None:
            return
        if parts.path == "/mail/u/0/attachment":
            self._send_attachment(query)
        elif parts.path == "/mail/api/threads":
            self.send_json(200, self._list(query))
        elif parts.path.startswith("/mail/api/thread/"):
            self._send_thread(parts.path.removeprefix("/mail/api/thread/"))
        elif parts.path == "/mail/api/me":
            self.send_json(200, {**SELF, "labels": self._counts()})
        else:
            self.send_json(404, {"error": "not_found", "message": f"no API at {parts.path}"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        session = self._signed_in()
        if session is None:
            return
        if not hmac.compare_digest(self.headers.get(CSRF_HEADER) or "", self._csrf_for(session)):
            self.send_json(403, {"error": "csrf", "message": f"Missing or stale {CSRF_HEADER} header; reload the app."})
            return
        try:
            body = json.loads(self.read_body() or b"{}")
            if not isinstance(body, dict):
                raise ValueError(f"received body {body!r:.80}; expected a JSON object")
            if path.startswith("/mail/api/thread/") and path.endswith("/modify"):
                self.send_json(200, self._modify(path.split("/")[4], body))
            elif path == "/mail/api/send":
                self.send_json(200, self._send(body))
            else:
                self.send_json(404, {"error": "not_found", "message": f"no API at {path}"})
        except (ValueError, KeyError, TypeError) as error:
            self.send_json(400, {"error": "invalid", "message": str(error)})

    # ----------------------------------------------------------- reads --
    def _threads(self) -> list[dict[str, object]]:
        return self.store.state["threads"]  # type: ignore[return-value]

    def _counts(self) -> dict[str, int]:
        threads = self._threads()
        return {"INBOX": sum("INBOX" in t["labels"] and "UNREAD" in t["labels"] for t in threads),  # type: ignore[operator]
                "TRASH": sum("TRASH" in t["labels"] for t in threads)}  # type: ignore[operator]

    def _summary(self, thread: dict[str, object]) -> dict[str, object]:
        messages = thread["messages"]
        last = messages[-1]  # type: ignore[index]
        return {"id": thread["id"], "subject": thread["subject"], "labels": thread["labels"],
                "from": [m["from"] for m in messages], "date": last["date"],  # type: ignore[union-attr]
                "snippet": " ".join(str(last["body"]).split())[:110],
                "hasAttachment": any(m["attachments"] for m in messages), "count": len(messages)}  # type: ignore[union-attr]

    def _list(self, query: dict[str, str]) -> dict[str, object]:
        label, needle = query.get("label", "INBOX").upper(), query.get("q", "").strip().lower()
        found = []
        for thread in sorted(self._threads(), key=lambda t: str(t["messages"][-1]["date"]), reverse=True):  # type: ignore[index]
            labels = thread["labels"]
            in_label = label == "ALL" and "TRASH" not in labels or label in labels  # type: ignore[operator]
            text = json.dumps(thread["messages"], ensure_ascii=False).lower() + str(thread["subject"]).lower()
            if in_label and (not needle or all(word in text for word in needle.split())):
                found.append(self._summary(thread))
        return {"threads": found, "label": label}

    def _send_thread(self, thread_id: str) -> None:
        thread = next((t for t in self._threads() if t["id"] == thread_id), None)
        if thread is None:
            self.send_json(404, {"error": "not_found", "message": f"no thread {thread_id!r}"})
            return
        self.send_json(200, thread)

    def _send_attachment(self, query: dict[str, str]) -> None:
        thread = next((t for t in self._threads() if t["id"] == query.get("th")), None)
        attachments = [a for m in (thread or {}).get("messages", []) for a in m["attachments"]]  # type: ignore[union-attr]
        found = next((a for a in attachments if a["id"] == query.get("att")), None)
        if found is None:
            self.send_json(404, {"error": "not_found", "message": f"no attachment {query.get('att')!r} in {query.get('th')!r}"})
            return
        body = ATTACHMENT_FILES[str(found["filename"])]
        disposition = "inline" if query.get("disp") == "inline" else "attachment"
        self.send_response(200)
        self.send_header("Content-Type", str(found["mimeType"]))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Content-Disposition", f"{disposition}; filename=\"{found['filename']}\"; "
                                                f"filename*=UTF-8''{quote(str(found['filename']))}")
        self.send_header("Cache-Control", "private, no-store")
        self.end_headers()
        self.wfile.write(body)

    # ---------------------------------------------------------- writes --
    def _modify(self, thread_id: str, body: dict[str, object]) -> dict[str, object]:
        _find_thread(self._threads(), thread_id)
        add, remove = body.get("addLabels", []), body.get("removeLabels", [])
        if not isinstance(add, list) or not isinstance(remove, list) or not set(add) | set(remove) <= set(LABELS) - {"SENT"}:
            raise ValueError(f"received addLabels {add!r} and removeLabels {remove!r}; expected lists of "
                             f"{', '.join(label for label in LABELS if label != 'SENT')}")
        state = self.store.record({"type": "modify", "thread": thread_id, "add": add, "remove": remove,
                                   "route": self._route()})
        return self._summary(_find_thread(state["threads"], thread_id))  # type: ignore[arg-type]

    def _send(self, body: dict[str, object]) -> dict[str, object]:
        to = body.get("to")
        recipients = [to] if isinstance(to, str) else to
        if not isinstance(recipients, list) or not recipients or not all(
                isinstance(item, str) and EMAIL_PATTERN.match(item.strip()) for item in recipients):
            raise ValueError(f"received to {to!r}; expected one or more email addresses")
        text, subject = body.get("body"), body.get("subject", "")
        if not isinstance(text, str) or not text.strip() or len(text) > MAX_BODY_CHARS or not isinstance(subject, str):
            raise ValueError(f"received body {text!r:.60} and subject {subject!r:.60}; expected non-empty text")
        thread_id = body.get("threadId") or None
        if thread_id is not None:
            thread = _find_thread(self._threads(), thread_id)
            subject = subject or f"Re: {thread['subject']}"
        number = int(self.store.state["next_message"])  # type: ignore[call-overload]
        message = {"id": f"s{number:04d}", "from": SELF, "to": [{"name": "", "email": item.strip()} for item in recipients],
                   "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "subject": subject, "body": text,
                   "attachments": [], "inReplyTo": body.get("inReplyTo") or None}
        self.store.record({"type": "send", "thread": thread_id, "message": message, "route": self._route()})
        return {"id": message["id"], "threadId": thread_id or f"sent{number:04d}"}


if __name__ == "__main__":
    serve(QuillmailHandler, apply_quillmail, SEED)
