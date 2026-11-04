"""Computer use on a local webmail replica, graded by server-signed state (#153).

Quillmail (`mengine_bench.sites.quillmail`) is fictional and served from the workspace like a real web app: a
minified client, a session cookie and an anti-CSRF token. The job is an everyday chore: file a vendor's invoice
and tell the vendor the total (#155 dropped the archive step). Any route counts (a browser, the page's own API, a script); the
route of each write is recorded as a note, never a grade.
"""

from __future__ import annotations

import hashlib
import http.cookiejar
import json
import re
import shutil
import urllib.request
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, number, read, saw
from mengine_bench.sites import quillmail
from mengine_bench.sites.quillmail import ATTACHMENT_FILES, BILLING, SEED, SELF, TARGET_THREAD, apply_quillmail
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE, SERVED_DIR, SERVER_FILE, SiteEvent, verify

APP_DIR = Path(quillmail.__file__).resolve().parent / "quillmail_app"
INVOICE_FILE = "LP-2026-0418.pdf"
INVOICE_SHA = hashlib.sha256(ATTACHMENT_FILES[INVOICE_FILE]).hexdigest()
INVOICE_TOTAL = 1205.77
WEBMAIL_INTEGRITY_GATE = "mailbox state and journal written only by the mail server"
WEBMAIL_UNTOUCHED_GATE = "every other conversation left as it was"
# Labels that only record reading or sending, which any route may change in passing.
WEBMAIL_PASSING_LABELS = {"UNREAD", "SENT"}

WEBMAIL_PROMPT = """You are signed in to Quillmail at {SITE} as Bench Tester (tester@quillmail.test), the studio's
shared mailbox. Larkspur Print Co. has billed us for the October print run. Accounting wants two things before the
end of the day:

- the invoice PDF from that email saved in this folder, exactly as attached;
- a reply to Larkspur in that same conversation confirming the invoice total, so they know we have it.

Leave the rest of the mailbox as it is."""


# ----------------------------------------------------------------- fixture ----


def minify_js(source: str) -> str:
    """One line, as the real kind of site ships it; the source keeps every statement `;`-terminated."""
    return "".join(line.strip() for line in source.splitlines() if line.strip())


def minify_css(source: str) -> str:
    return re.sub(r"\s*([{};:,>])\s*", r"\1", re.sub(r"\s+", " ", source)).strip()


def _webmail_setup(ws: Path) -> None:
    site = ws / SERVED_DIR
    (site / "assets").mkdir(parents=True)
    js = minify_js((APP_DIR / "app.js").read_text(encoding="utf-8")).encode("utf-8")
    css = minify_css((APP_DIR / "style.css").read_text(encoding="utf-8")).encode("utf-8")
    names = {"__JS__": f"app.{hashlib.sha256(js).hexdigest()[:10]}.js",
             "__CSS__": f"app.{hashlib.sha256(css).hexdigest()[:10]}.css"}
    (site / "assets" / names["__JS__"]).write_bytes(js)
    (site / "assets" / names["__CSS__"]).write_bytes(css)
    page = (APP_DIR / "index.html").read_text(encoding="utf-8")
    for placeholder, name in names.items():
        page = page.replace(placeholder, name)
    (site / "index.html").write_text(page, encoding="utf-8", newline="\n")


# --------------------------------------------------------------- reference ----


class QuillmailClient:
    """The page's own API from a script: the cookie from the app page, the token from its meta tag."""

    def __init__(self, ws: Path) -> None:
        self.url = json.loads((ws / DATA_DIR / SERVER_FILE).read_text(encoding="utf-8"))["url"]
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        page = self.opener.open(self.url + "/", timeout=10).read().decode("utf-8")
        self.token = re.search(r'name="qm-at" content="([0-9a-f]+)"', page).group(1)  # type: ignore[union-attr]

    def get(self, path: str) -> bytes:
        return self.opener.open(self.url + path, timeout=10).read()

    def post(self, path: str, body: dict[str, object]) -> dict[str, object]:
        request = urllib.request.Request(self.url + path, data=json.dumps(body).encode("utf-8"), method="POST",
                                         headers={"Content-Type": "application/json", "X-Qm-At": self.token})
        return json.loads(self.opener.open(request, timeout=10).read())


def webmail_solve(ws: Path, thread: str = TARGET_THREAD, attachment: str = "lp1", total: str = "EUR 1,205.77",
                  archive: bool = False) -> list[str]:
    """The chore through the page's API; the tests vary the thread, the attachment, the total and an extra archive."""
    client = QuillmailClient(ws)
    found = json.loads(client.get(f"/mail/api/thread/{thread}"))
    message = found["messages"][-1]
    name = next(a["filename"] for a in message["attachments"] if a["id"] == attachment)
    (ws / name).write_bytes(client.get(f"/mail/u/0/attachment?th={thread}&att={attachment}"))
    client.post("/mail/api/send", {"threadId": thread, "inReplyTo": message["id"], "to": [message["from"]["email"]],
                                   "body": f"Hello,\n\nThanks, we received invoice LP-2026-0418 for {total} and "
                                           f"have passed it to accounting.\n\nBench Tester"})
    if archive:
        client.post(f"/mail/api/thread/{thread}/modify", {"addLabels": [], "removeLabels": ["INBOX"]})
    return ["Saved the invoice and replied to Larkspur with the total."]


def _webmail_reference(ws: Path) -> list[str]:
    return webmail_solve(ws)


# ------------------------------------------------------------------- check ----


def _webmail_history(ws: Path, result: CheckResult) -> tuple[list[dict[str, object]], list[SiteEvent]]:
    try:
        key = bytes.fromhex((read(ws, f"{DATA_DIR}/{KEY_FILE}") or "").strip())
        state, events = verify(ws / DATA_DIR, key, apply_quillmail)
    except ValueError as error:
        result.mandatory.append((WEBMAIL_INTEGRITY_GATE, False))
        result.details[WEBMAIL_INTEGRITY_GATE] = str(error)
        return [], []
    result.mandatory.append((WEBMAIL_INTEGRITY_GATE, True))
    return list(state["threads"]), events  # type: ignore[call-overload]


def _webmail_saved_pdfs(ws: Path) -> dict[str, str]:
    """Every file the agent left outside the app and the server's data, by relative path -> sha256."""
    found = {}
    for path in ws.rglob("*"):
        rel = path.relative_to(ws)
        if path.is_file() and rel.parts[0] not in (SERVED_DIR, DATA_DIR) and path.stat().st_size < 5_000_000:
            found[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return found


def _webmail_states_total(text: str) -> bool:
    """Accept the total in either number convention, excluding denials and competing confirmations."""
    correct = False
    text = re.sub(r"(?m)^\s*>[^\n]*", "", text)
    # #164: a quoted or denied total is not a confirmation. Keep negation local so
    # unrelated statements ("not paid yet") and corrected subtotals stay valid.
    clauses = re.split(r"[;\n!?]|\.(?!\d)|\b(?:but|rather than)\b", text, flags=re.I)
    for clause in clauses:
        for match in re.finditer(r"\d[\d.,]*\d|\d", clause):
            got = number(match.group())
            before, after = clause[:match.start()], clause[match.end():]
            prefix = re.split(r",|\band\b|\bincluding\b", before, flags=re.I)[-1]
            # #164: negation scopes over the amount's noun phrase, not just its currency.
            noun_phrase = r"(?:(?:the|an?|earlier|previous|invoice|total|amount|of|previously|quoted|as)\s+)*"
            denied = re.search(r"\b(?:not|never|isn't|isn\u2019t|wasn't|wasn\u2019t)\s*" + noun_phrase
                               + r"(?:EUR\s*|\u20ac\s*)?$", prefix, re.I)
            denied_after = re.match(r"\s*(?:EUR|\u20ac)?\s*(?:is|was)\s+not\b", after, re.I)
            historical = re.search(r"\b(?:earlier|previous(?:ly)?|quoted|superseded)\b",
                                   re.split(r"\bconfirm(?:ed)?\b", prefix, flags=re.I)[-1], re.I)
            superseded = re.match(r"\s*(?:EUR|\u20ac)?\s*(?:is|was|has been)\s+(?:superseded|replaced|incorrect|wrong)\b", after, re.I)
            if denied or denied_after or historical or superseded:
                continue
            if got is not None and abs(got - INVOICE_TOTAL) < 0.005:
                correct = True
                continue
            line_item = re.search(r"\b(?:subtotal|VAT|tax)\b", prefix, re.I)
            confirms = re.search(r"\b(?:confirm(?:ed)?|total(?:\s+amount)?)\s*(?:is|of|for|:|=)?\s*"
                                 r"(?:EUR\s*|\u20ac\s*)?$", prefix, re.I)
            money = re.search(r"[.,]\d{2}$", match.group()) or re.search(r"(?:EUR|\u20ac)\s*$", before, re.I)
            if got is not None and money and confirms and not line_item:
                return False
    return correct


def _webmail_kept(thread: dict[str, object]) -> dict[str, object]:
    return {"labels": sorted(set(thread["labels"]) - WEBMAIL_PASSING_LABELS), "messages": thread["messages"]}  # type: ignore[arg-type]


def _webmail_route_note(events: list[SiteEvent]) -> str:
    routes = sorted({json.dumps(event.get("route", {}), sort_keys=True) for event in events[1:]})
    return "write routes (observation only): " + ("; ".join(routes) if routes else "none")


def _webmail_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    threads, events = _webmail_history(ws, result)
    seed = {thread["id"]: thread for thread in SEED["threads"]}  # type: ignore[union-attr]
    final = {thread["id"]: thread for thread in threads}
    changed = sorted(thread_id for thread_id, thread in seed.items()
                     if thread_id != TARGET_THREAD and (thread_id not in final or _webmail_kept(final[thread_id]) != _webmail_kept(thread)))
    result.mandatory.append((WEBMAIL_UNTOUCHED_GATE, not changed))
    if changed:
        result.details[WEBMAIL_UNTOUCHED_GATE] = saw({tid: final.get(tid, {}).get("labels") for tid in changed},
                                                     {tid: seed[tid]["labels"] for tid in changed})
    saved = _webmail_saved_pdfs(ws)
    result.add("invoice PDF saved byte for byte", INVOICE_SHA in saved.values(),
               saw(sorted(saved), f"a file with the sha256 of {INVOICE_FILE}"))
    target = final.get(TARGET_THREAD, {"labels": [], "messages": []})
    sent = [m for t in threads for m in t["messages"] if m["from"]["email"] == SELF["email"]]  # type: ignore[index]
    replies = [m for m in target["messages"] if m["from"]["email"] == SELF["email"]]  # type: ignore[union-attr]
    result.add("reply sent in the invoice conversation", len(replies) == 1,
               saw([(m["subject"], m["to"]) for m in sent], f"one reply in thread {TARGET_THREAD}"))
    reply = replies[-1] if replies else {"to": [], "body": ""}
    recipients = sorted({str(p["email"]).lower() for p in reply["to"]})  # type: ignore[union-attr]
    result.add("reply addressed to the sender", recipients == [BILLING["email"]], saw(recipients, [BILLING["email"]]))
    result.add("reply states the invoice total", _webmail_states_total(str(reply["body"])),
               saw(str(reply["body"])[:160], INVOICE_TOTAL))
    result.add("nothing else sent", len(sent) == len(replies), saw([(m["subject"], m["to"]) for m in sent], "only the reply"))
    result.notes.append(_webmail_route_note(events))
    return result


TASKS: list[EvalTask] = [EvalTask(
    id="cu-webmail",
    category="computer-use",
    provenance="new for bench#153: an everyday mailbox chore on a local webmail replica",
    summary="In a webmail app, save a vendor's invoice PDF and reply to the sender with its total.",
    setup=_webmail_setup,
    steps=(Step(WEBMAIL_PROMPT),),
    check=_webmail_check,
    reference=_webmail_reference,
    timeout_s=180,
    site="mengine_bench.sites.quillmail",
    checkpoints=checkpoints(("opened the mail app", r"127\.0\.0\.1"), ("downloaded the invoice", r"attachment|LP-2026-0418"),
                            ("replied", r"/mail/api/send|Reply|Send")),
)]
