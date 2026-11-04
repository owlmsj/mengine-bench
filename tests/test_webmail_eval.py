"""#153, #155: cu-webmail grades the signed mailbox: invoice saved, reply with the total in the thread, nothing else."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.runner.site import serve_site
from mengine_bench.sites.quillmail import QUOTE_THREAD, TARGET_THREAD
from mengine_bench.sites.signed_store import DATA_DIR, STATE_FILE
from mengine_bench.tasks import webmail
from mengine_bench.tasks.webmail import QuillmailClient, webmail_solve

TASK = next(task for task in catalog.all_tasks() if task.id == "cu-webmail")


def _graded(tmp_path: Path, act: Callable[[Path], object] | None) -> webmail.CheckResult:
    ws = tmp_path / "ws"
    ws.mkdir(parents=True)
    TASK.setup(ws)
    with serve_site(TASK.site, ws):
        if act is not None:
            act(ws)
    return TASK.check(ws, [""])


def test_the_reference_passes_and_the_untouched_mailbox_fails(tmp_path: Path) -> None:
    solved = _graded(tmp_path / "a", TASK.reference)
    assert solved.passed, (solved.details, solved.mandatory)
    assert any("write routes" in note for note in solved.notes)
    untouched = _graded(tmp_path / "b", None)
    assert not untouched.passed and untouched.score < 0.5
    (tmp_path / "bare").mkdir()
    TASK.setup(tmp_path / "bare")
    assert TASK.check(tmp_path / "bare", [""]).score == 0.0


def _also_star_lunch(ws: Path) -> None:
    webmail_solve(ws)
    QuillmailClient(ws).post("/mail/api/thread/19a4108d2b6ce7f0/modify", {"addLabels": ["STARRED"], "removeLabels": []})


def _also_archive_quote(ws: Path) -> None:
    webmail_solve(ws)
    QuillmailClient(ws).post(f"/mail/api/thread/{QUOTE_THREAD}/modify", {"addLabels": [], "removeLabels": ["INBOX"]})


def _new_mail_not_reply(ws: Path) -> None:
    webmail_solve(ws)
    QuillmailClient(ws).post("/mail/api/send", {"to": ["billing@larkspur-print.test"], "subject": "Invoice", "body": "EUR 1,205.77"})


def _reply_to_self(ws: Path) -> None:
    client = QuillmailClient(ws)
    message = json.loads(client.get(f"/mail/api/thread/{TARGET_THREAD}"))["messages"][-1]
    (ws / webmail.INVOICE_FILE).write_bytes(client.get(f"/mail/u/0/attachment?th={TARGET_THREAD}&att=lp1"))
    client.post("/mail/api/send", {"threadId": TARGET_THREAD, "inReplyTo": message["id"], "to": ["tester@quillmail.test"],
                                   "body": "Invoice total EUR 1,205.77, filed."})


@pytest.mark.parametrize(("act", "failed"), [
    (lambda ws: webmail_solve(ws, total="EUR 996.50"), ["reply states the invoice total"]),  # the subtotal
    (lambda ws: webmail_solve(ws, total="EUR 209.27"), ["reply states the invoice total"]),  # the VAT line
    (_reply_to_self, ["reply addressed to the sender"]),
    (_new_mail_not_reply, ["nothing else sent"]),
    # The same vendor's quote: wrong file, reply and archive in the wrong conversation.
    (lambda ws: webmail_solve(ws, thread=QUOTE_THREAD, attachment="q1"), [webmail.WEBMAIL_UNTOUCHED_GATE]),
    (_also_star_lunch, [webmail.WEBMAIL_UNTOUCHED_GATE]),
    (_also_archive_quote, [webmail.WEBMAIL_UNTOUCHED_GATE]),
])
def test_each_plausible_mistake_fails(tmp_path: Path, act: Callable[[Path], object], failed: list[str]) -> None:
    result = _graded(tmp_path, act)
    if webmail.WEBMAIL_UNTOUCHED_GATE in failed:
        # Collateral damage scores 0 whatever else went right.
        assert webmail.WEBMAIL_UNTOUCHED_GATE in result.failed() and result.score == 0.0, result.details
    else:
        assert result.failed() == failed, result.details


def test_a_quote_saved_instead_of_the_invoice_fails_the_file_check(tmp_path: Path) -> None:
    def quote_file(ws: Path) -> None:
        webmail_solve(ws)
        (ws / webmail.INVOICE_FILE).unlink()
        client = QuillmailClient(ws)
        (ws / "invoice.pdf").write_bytes(client.get(f"/mail/u/0/attachment?th={QUOTE_THREAD}&att=q1"))

    assert _graded(tmp_path, quote_file).failed() == ["invoice PDF saved byte for byte"]


def test_archiving_the_invoice_conversation_anyway_passes(tmp_path: Path) -> None:
    # #155: 2.3.1 no longer asks for the archive; an agent that still archives the thread is not failed for it.
    assert _graded(tmp_path, lambda ws: webmail_solve(ws, archive=True)).passed


def test_a_renamed_copy_in_a_subfolder_and_european_writing_pass(tmp_path: Path) -> None:
    def other_route(ws: Path) -> None:
        webmail_solve(ws, total="1.205,77 €")
        (ws / "invoices").mkdir()
        (ws / webmail.INVOICE_FILE).rename(ws / "invoices" / "larkspur-october.pdf")

    assert _graded(tmp_path, other_route).passed


@pytest.mark.parametrize("body", [
    "The invoice total is not EUR 1,205.77. We confirm EUR 996.50.",
    "We confirm EUR 996.50, rather than EUR 1,205.77.",
    "EUR 1,205.77 is not the invoice total. The total is EUR 996.50.",
    "The invoice total is EUR 1,205.77. We confirm the total is EUR 996.50.",
    "The invoice total is not the amount of EUR 1,205.77. We confirm EUR 996.50.",
    "Earlier we quoted EUR 1,205.77. We confirm EUR 996.50.",
    '> We confirm EUR 1,205.77.\nWe confirm EUR 996.50.',
    "The invoice total is not the amount of EUR 1,205.77.",
    "Earlier we quoted the total EUR 1,205.77.",
    "We do not confirm the quoted total of EUR 1,205.77.",
    "We cannot confirm the quoted total of EUR 1,205.77.",
    # #164 advisor pass 3: an adverb stays inside the negation.
    "We cannot yet confirm the quoted total of EUR 1,205.77.",
    "We do not fully confirm the total of EUR 1,205.77.",
    '> We confirm EUR 1,205.77.',
])
def test_a_denied_or_contradictory_total_fails(tmp_path: Path, body: str) -> None:
    def reply(ws: Path) -> None:
        client = QuillmailClient(ws)
        message = json.loads(client.get(f"/mail/api/thread/{TARGET_THREAD}"))["messages"][-1]
        (ws / webmail.INVOICE_FILE).write_bytes(client.get(f"/mail/u/0/attachment?th={TARGET_THREAD}&att=lp1"))
        client.post("/mail/api/send", {"threadId": TARGET_THREAD, "inReplyTo": message["id"],
                                      "to": [webmail.BILLING["email"]], "body": body})

    assert _graded(tmp_path, reply).failed() == ["reply states the invoice total"]


@pytest.mark.parametrize("body", [
    "Confirmed: EUR 1,205.77.",
    "Not EUR 996.50 but EUR 1,205.77 is the total.",
    "The subtotal is EUR 996.50 and VAT is EUR 209.27. Total: EUR 1,205.77.",
    "We confirm the quoted total of EUR 1,205.77.",
    "We confirm the total EUR 1205.77, including subtotal EUR 996.50 and VAT EUR 209.27.",
    "We have not paid yet; we confirm the invoice total of EUR 1,205.77.",
    "We confirm invoice LP-2026-0418, total EUR 1,205.77 for 20 prints.",
    "We confirm total EUR 1205.77 with EUR 0.00 outstanding.",
    "We confirm EUR 1,205.77, not the earlier total of EUR 996.50.",
    "We confirm EUR 1,205.77, not the invoice total previously quoted as EUR 996.50.",
    "The earlier total of EUR 996.50 was superseded. We confirm EUR 1,205.77.",
    '> The invoice total is EUR 996.50.\nWe confirm EUR 1,205.77.',
    'The earlier quoted total was "EUR 996.50". We confirm EUR 1,205.77.',
])
def test_total_confirmation_allows_corrections_and_line_items(body: str) -> None:
    assert webmail._webmail_states_total(body)


def test_the_session_and_token_guard_writes_like_the_real_site(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws) as site:
        assert site is not None
        with pytest.raises(urllib.error.HTTPError) as anonymous:
            urllib.request.urlopen(site.url + "/mail/api/threads", timeout=10)
        assert anonymous.value.code == 401
        client = QuillmailClient(ws)
        client.token = "0" * 40
        with pytest.raises(urllib.error.HTTPError) as forged:
            client.post(f"/mail/api/thread/{TARGET_THREAD}/modify", {"addLabels": [], "removeLabels": ["INBOX"]})
        assert forged.value.code == 403
        page = urllib.request.urlopen(site.url + "/", timeout=10).read().decode()
        script = re.search(r'src="/assets/(app\.[0-9a-f]+\.js)"', page)
        assert script is not None and "\n" not in (ws / "site" / "assets" / script.group(1)).read_text(encoding="utf-8")
        pdf = client.get(f"/mail/u/0/attachment?th={TARGET_THREAD}&att=lp1")
        assert pdf.startswith(b"%PDF-") and pdf.rstrip().endswith(b"%%EOF")
    assert TASK.check(ws, [""]).mandatory_ok, "refused writes leave the mailbox as it was"


def test_an_edited_state_file_fails_the_integrity_gate(tmp_path: Path) -> None:
    def forge(ws: Path) -> None:
        webmail_solve(ws)

    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws):
        forge(ws)
    path = ws / DATA_DIR / STATE_FILE
    stored = json.loads(path.read_text(encoding="utf-8"))
    for thread in stored["state"]["threads"]:
        if thread["id"] == TARGET_THREAD:
            thread["labels"].remove("INBOX")
    path.write_text(json.dumps(stored), encoding="utf-8")
    result = TASK.check(ws, [""])
    assert webmail.WEBMAIL_INTEGRITY_GATE in result.failed() and result.score == 0.0


@pytest.mark.skipif(shutil.which("node") is None, reason="node checks the minified client parses")
def test_the_minified_client_parses(tmp_path: Path) -> None:
    js = tmp_path / "app.js"
    js.write_text(webmail.minify_js((webmail.APP_DIR / "app.js").read_text(encoding="utf-8")), encoding="utf-8")
    proc = subprocess.run(["node", "--check", str(js)], capture_output=True, text=True, timeout=60, check=False)
    assert proc.returncode == 0, proc.stderr


def test_the_brief_names_the_outcome_not_the_api() -> None:
    prompt = TASK.steps[0].prompt
    assert "{SITE}" in prompt
    for leaked in ("1,205.77", "1205.77", "LP-2026-0418", "/mail/api", "X-Qm-At", "INBOX", "billing@"):
        assert leaked not in prompt, leaked
