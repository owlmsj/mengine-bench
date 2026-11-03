"""Gold tests for cu-social-cycle on the Bluehaze replica (#153): no network beyond 127.0.0.1, no model."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from mengine_bench import catalog
from mengine_bench.core import CheckResult
from mengine_bench.runner.site import serve_site
from mengine_bench.sites.bluehaze import SEED, SELF, TOKEN_HEADER, apply_bluehaze, post_uri
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE, STATE_FILE, SignedStore, verify
from mengine_bench.tasks.social import IMAGE, INTEGRITY_GATE, TASKS, SiteClient, png_size, poster_png, solve

TASK = TASKS[0]
MARA = "mara-quill.bluehaze.test"
VOLUNTEERS = post_uri(MARA, "3m4mara7vw4ee")


def _get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=10) as reply:
        return reply.read()


def _status(request: urllib.request.Request, opener: urllib.request.OpenerDirector | None = None) -> int:
    try:
        with (opener or urllib.request.build_opener()).open(request, timeout=10) as reply:
            return reply.status
    except urllib.error.HTTPError as error:
        return error.code


def _fresh(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    ws.mkdir()
    TASK.setup(ws)
    return ws


def _solved(tmp_path: Path, **variant: object) -> Path:
    ws = _fresh(tmp_path)
    with serve_site(TASK.site, ws):
        solve(ws, **variant)  # type: ignore[arg-type]
    return ws


def _check(ws: Path) -> CheckResult:
    return TASK.check(ws, [""])


def _failed_only(result: CheckResult, *names: str) -> None:
    assert result.mandatory_ok and sorted(result.failed()) == sorted(names), result.details


def test_reference_passes_and_its_route_is_noted(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    with serve_site(TASK.site, ws):
        answers = TASK.reference(ws)
    result = TASK.check(ws, answers)
    assert result.passed, (result.failed(), result.details)
    assert png_size((ws / IMAGE).read_bytes()) == (1200, 675)
    assert any(note.startswith("route observed: scripted HTTP") for note in result.notes), result.notes


def test_untouched_fails_with_and_without_a_server(tmp_path: Path) -> None:
    never = tmp_path / "never"
    never.mkdir()
    TASK.setup(never)
    assert (INTEGRITY_GATE, False) in _check(never).mandatory
    served = _fresh(tmp_path)
    with serve_site(TASK.site, served):
        pass
    result = _check(served)
    assert result.mandatory_ok and not result.passed and result.score < 0.5, result.failed()


def test_missing_alt_text_fails(tmp_path: Path) -> None:
    _failed_only(_check(_solved(tmp_path, alt="")), "image has the given alt text")


def test_leaving_the_test_post_up_fails(tmp_path: Path) -> None:
    # #155: the cycle is post then delete; a post left standing fails both the delete and the "nothing else" check.
    _failed_only(_check(_solved(tmp_path, delete=False)), "test post deleted", "nothing else published",
                 "post, then delete")


def test_a_reply_left_behind_fails(tmp_path: Path) -> None:
    # #155: the 2.3.0 reply step is gone, so an agent that still replies publishes something not asked for.
    ws = _solved(tmp_path)
    reply = {"uri": f"at://did:web:{SELF}/app.bluehaze.feed.post/3zzzzzzzzzzzy", "rkey": "3zzzzzzzzzzzy",
             "author": SELF, "seq": 98, "record": {"text": "Count me in!", "createdAt": "2026-11-03T00:00:00Z",
                                                   "reply": {"root": {"uri": VOLUNTEERS}, "parent": {"uri": VOLUNTEERS}}}}
    _resign_with(ws, [{"type": "create", "post": reply}])
    _failed_only(_check(ws), "nothing else published")


def test_an_image_of_the_wrong_size_fails(tmp_path: Path) -> None:
    _failed_only(_check(_solved(tmp_path, image=poster_png(width=1280, height=720))), "cover.png is a 1200x675 PNG")


def test_posting_another_image_than_cover_png_fails(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    (ws / IMAGE).write_bytes(poster_png(title="HARBOR DAY 2006"))
    _failed_only(_check(ws), "test post carries cover.png")


def _resign_with(ws: Path, extra: list[dict[str, object]]) -> None:
    """A history the server would have signed, plus events: what a site that allowed them would record."""
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


def test_an_extra_post_fails(tmp_path: Path) -> None:
    ws = _solved(tmp_path)
    extra = {"uri": f"at://did:web:{SELF}/app.bluehaze.feed.post/3zzzzzzzzzzzz", "rkey": "3zzzzzzzzzzzz",
             "author": SELF, "seq": 99, "record": {"text": "oops", "createdAt": "2026-11-03T00:00:00Z"}}
    _resign_with(ws, [{"type": "create", "post": extra}])
    _failed_only(_check(ws), "nothing else published")


def test_an_edited_state_fails_the_gate(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    with serve_site(TASK.site, ws):
        pass
    stored = json.loads((ws / DATA_DIR / STATE_FILE).read_text(encoding="utf-8"))
    stored["state"]["posts"] = []
    (ws / DATA_DIR / STATE_FILE).write_text(json.dumps(stored), encoding="utf-8")
    result = _check(ws)
    assert (INTEGRITY_GATE, False) in result.mandatory and result.score == 0


def test_writes_need_the_session_cookie_and_the_page_token(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    body = json.dumps({"repo": SELF, "collection": "app.bluehaze.feed.post", "record": {"text": "x"}}).encode()
    with serve_site(TASK.site, ws) as site:
        assert site is not None
        url = site.url + "/xrpc/com.bluehaze.repo.createRecord"
        client = SiteClient(site.url)
        bare = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
        assert _status(bare) == 401, "a write without the cookie and the token"
        no_cookie = urllib.request.Request(url, data=body, method="POST",
                                           headers={"Content-Type": "application/json", TOKEN_HEADER: client.token})
        assert _status(no_cookie) == 401, "the token without the session cookie"
        wrong = urllib.request.Request(url, data=body, method="POST",
                                       headers={"Content-Type": "application/json", TOKEN_HEADER: "0" * 32})
        assert _status(wrong, client.opener) == 401, "the cookie with a wrong token"
        delete = json.dumps({"repo": MARA, "collection": "app.bluehaze.feed.post", "rkey": "3m4mara7vw4ee"}).encode()
        with pytest.raises(urllib.error.HTTPError) as refused:
            client.call("com.bluehaze.repo.deleteRecord", delete)
        assert refused.value.code == 403, "another user's repo"


def test_the_replica_ships_a_minified_bundle_and_the_real_flows(tmp_path: Path) -> None:
    ws = _fresh(tmp_path)
    served = sorted(path.relative_to(ws / "site").as_posix() for path in (ws / "site").rglob("*") if path.is_file())
    assert served[0] == "index.html" and served[1] == "static/css/main.css" and served[2].startswith("static/js/main.")
    bundle = (ws / "site" / served[2]).read_text(encoding="utf-8")
    assert bundle.count("\n") == 0 and "createRecord" not in bundle and "X-Bh-Token" not in bundle
    for label in ("Rich-Text Editor", "Publish post", "Add alt text", "Alt text", "Open post options menu",
                  "Delete post", '"file"'):
        assert label in bundle, label
    with serve_site(TASK.site, ws) as site:
        assert site is not None
        page = _get(f"{site.url}/profile/{MARA}/post/3m4mara7vw4ee")
        assert b'<meta name="bh-boot"' in page and served[2].encode() in page
        feed = json.loads(_get(f"{site.url}/xrpc/app.bluehaze.feed.getAuthorFeed?actor={MARA}&limit=2"))
        assert [entry["post"]["author"]["handle"] for entry in feed["feed"]] == [MARA, MARA] and feed["cursor"] == "2"
        thread = json.loads(_get(f"{site.url}/xrpc/app.bluehaze.feed.getPostThread?uri={VOLUNTEERS}"))
        assert "Volunteers wanted" in thread["thread"]["post"]["record"]["text"]


def test_the_task_is_in_the_catalog_with_its_image_for_the_judge() -> None:
    assert TASK.id in {task.id for task in catalog.all_tasks()}
    assert TASK.deliverables == (IMAGE,) and TASK.render_target is None


def test_the_minifier_renames_a_spread_variable_like_any_other_use() -> None:
    # #153: `...picked` kept its old name while its declaration was renamed, so the composer threw on attach.
    from mengine_bench.sites.minify import minify

    out = minify('const picked = [1];\nfunction show(list) { return [...picked, list.picked, {picked: 2}]; }\n')
    assert "...picked" not in out and ".picked" in out and "{picked:" in out, out
