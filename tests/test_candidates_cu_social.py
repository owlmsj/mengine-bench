"""Hermetic gold tests for cu-social-cycle on the Bluehaze replica (#153): no network beyond 127.0.0.1, no model."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.candidates.cu_social import DECOY, IMAGE, INTEGRITY_GATE, TASKS, TARGET, solve
from mengine_bench.core import CheckResult
from mengine_bench.runner.site import serve_site
from mengine_bench.sites.bluehaze import SEED, SELF, apply_bluehaze
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE, STATE_FILE, SignedStore, verify

TASK = TASKS[0]
MARA = "mara-quill.bluehaze.test"


def _get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=10) as reply:
        return reply.read()


def _post_json(url: str, body: object) -> tuple[int, object]:
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=10) as reply:
            return reply.status, json.loads(reply.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def _solved(tmp_path: Path, **variant: str) -> Path:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws):
        solve(ws, **variant)
    return ws


def _check(ws: Path) -> CheckResult:
    return TASK.check(ws, [""])


def _failed_only(result: CheckResult, *names: str) -> None:
    assert result.mandatory_ok and sorted(result.failed()) == sorted(names), result.details


def test_reference_passes(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws):
        answers = TASK.reference(ws)
    result = TASK.check(ws, answers)
    assert result.passed, (result.failed(), result.details)


def test_untouched_fails_with_and_without_a_server(tmp_path: Path) -> None:
    never_served = tmp_path / "never"
    never_served.mkdir()
    TASK.setup(never_served)
    result = _check(never_served)
    assert not result.passed and (INTEGRITY_GATE, False) in result.mandatory
    served = tmp_path / "served"
    served.mkdir()
    TASK.setup(served)
    with serve_site(TASK.site, served):
        pass
    result = _check(served)
    assert result.mandatory_ok and not result.passed and result.score < 0.5, result.failed()


def test_missing_alt_text_fails(tmp_path: Path) -> None:
    _failed_only(_check(_solved(tmp_path, alt="")), "image has the given alt text")


def test_reply_to_the_wrong_post_fails(tmp_path: Path) -> None:
    _failed_only(_check(_solved(tmp_path, parent=DECOY)), "reply answers Mara's volunteer post")


def _resign_with(ws: Path, extra: list[dict[str, object]]) -> None:
    """A history the server would have signed, plus events: what a deleting site would have recorded."""
    data = ws / DATA_DIR
    key = bytes.fromhex((data / KEY_FILE).read_text())
    _, events = verify(data, key, apply_bluehaze)
    store = SignedStore(data, key, apply_bluehaze, SEED)
    for event in [*events[1:], *extra]:
        store.record(event)


@pytest.mark.parametrize("victim", [f"at://did:web:{MARA}/app.bluehaze.feed.post/3m4mara8xk5ff",
                                    f"at://did:web:{SELF}/app.bluehaze.feed.post/3m4test5hs6cc"],
                         ids=["another users post", "the accounts older post"])
def test_deleting_any_other_post_fails(tmp_path: Path, victim: str) -> None:
    ws = _solved(tmp_path)
    _resign_with(ws, [{"type": "delete", "uri": victim}])
    _failed_only(_check(ws), "other people's posts and older posts untouched")


def test_the_site_refuses_to_delete_another_users_post(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws) as site:
        assert site is not None
        status, _ = _post_json(site.url + "/xrpc/com.bluehaze.repo.deleteRecord",
                               {"repo": MARA, "collection": "app.bluehaze.feed.post", "rkey": "3m4mara7vw4ee"})
        assert status == 403
        status, _ = _post_json(site.url + "/xrpc/com.bluehaze.repo.deleteRecord",
                               {"repo": SELF, "collection": "app.bluehaze.feed.post", "rkey": "3m4mara7vw4ee"})
        assert status == 400


def test_an_extra_post_fails(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    extra = {"uri": f"at://did:web:{SELF}/app.bluehaze.feed.post/3zzzzzzzzzzzz", "rkey": "3zzzzzzzzzzzz",
             "author": SELF, "seq": 99, "record": {"text": "oops", "createdAt": "2026-11-03T00:00:00Z"}}
    _resign_with(ws, [{"type": "create", "post": extra}])
    _failed_only(_check(ws), "nothing else published")


def test_an_edited_state_fails_the_gate(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws):
        pass
    stored = json.loads((ws / DATA_DIR / STATE_FILE).read_text(encoding="utf-8"))
    stored["state"]["posts"] = []
    (ws / DATA_DIR / STATE_FILE).write_text(json.dumps(stored), encoding="utf-8")
    result = _check(ws)
    assert (INTEGRITY_GATE, False) in result.mandatory and result.score == 0


def test_the_replica_serves_its_routes_and_read_api(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    with serve_site(TASK.site, ws) as site:
        assert site is not None
        page = _get(f"{site.url}/profile/{MARA}/post/3m4mara7vw4ee")
        assert b'<script src="/app.js">' in page
        script = _get(site.url + "/app.js").decode("utf-8")
        for label in ("Rich-Text Editor", "Publish post", "Add alt text", "Alt text", "Open post options menu",
                      "Delete post", "type: \"file\""):
            assert label in script, label
        feed = json.loads(_get(f"{site.url}/xrpc/app.bluehaze.feed.getAuthorFeed?actor={MARA}&limit=2"))
        assert [entry["post"]["author"]["handle"] for entry in feed["feed"]] == [MARA, MARA] and feed["cursor"] == "2"
        thread = json.loads(_get(f"{site.url}/xrpc/app.bluehaze.feed.getPostThread?uri={TARGET}"))
        assert "Volunteers wanted" in thread["thread"]["post"]["record"]["text"]
    assert (ws / IMAGE).read_bytes().startswith(b"\x89PNG")


def test_candidate_stays_outside_the_catalog_but_runs_by_id() -> None:
    assert TASK.id not in {task.id for task in catalog.all_tasks()}
    found = catalog.task_by_id(TASK.id)
    assert found is not None and found.site == TASK.site
