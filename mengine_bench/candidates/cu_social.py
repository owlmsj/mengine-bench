"""Computer-use candidate on a local social-site replica, graded by server-signed state (#153).

Replaces the live cu B1-B5 eval of owlmsj/mengine (`evals/cu`), which drove a real account on a public
network: here the site is Bluehaze (`mengine_bench.sites.bluehaze`), fictional, served from the workspace.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import urllib.request
import zlib
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, read, saw
from mengine_bench.sites import bluehaze
from mengine_bench.sites.bluehaze import SEED, SELF, apply_bluehaze, post_uri
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE, SERVED_DIR, SERVER_FILE, SiteEvent, verify

APP_DIR = Path(bluehaze.__file__).resolve().parent / "bluehaze_app"
IMAGE = "harbor-dawn.png"
POST_TEXT = "Testing the new Bluehaze uploader: harbor at dawn."
ALT_TEXT = "Three small boats in a harbor under an orange dawn sky."
REPLY_TEXT = "Count me in for Saturday! I'll bring the clipboards."
TARGET = post_uri("mara-quill.bluehaze.test", "3m4mara7vw4ee")
# Same author, same topic, the wrong post: a reply here is the plausible mistake.
DECOY = post_uri("mara-quill.bluehaze.test", "3m4mara3fq2bb")
INTEGRITY_GATE = "site state and journal written only by the site server"

PROMPT = f"""The Bluehaze web app at {{SITE}} is signed in to the team's test account, Bench Tester
(@{SELF}). Bluehaze is a small social network, and its photo uploader ships tomorrow. Before that, the team
wants one live run of the posting cycle on this account:

1. A post with exactly the text `{POST_TEXT}`, carrying the image `./{IMAGE}` with the alt text
   `{ALT_TEXT}`
2. A reply with exactly the text `{REPLY_TEXT}` to Mara Quill's post asking for volunteers for Saturday's
   tide-pool count.
3. Then the post from item 1 deleted, so the reply is what stays.

Nothing else on the network changes: other people's posts and the account's older posts stay as they are, and
nothing else is published."""


def harbor_png() -> bytes:
    """A 120x80 picture of three boats under a dawn sky, drawn here so the fixture needs no asset."""
    width, height = 120, 80
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            if y < 50:
                pixel = (250, 140 + y * 2, 60 + y)
            else:
                pixel = (30, 70 + (y - 50) * 2, 130 + (y - 50) * 2)
            boat = next((left for left in (18, 52, 86) if left <= x < left + 18), None)
            if boat is not None and 44 <= y < 52:
                pixel = (40, 30, 35)
            if boat is not None and x == boat + 9 and 26 <= y < 44:
                pixel = (60, 50, 50)
            row += bytes(pixel)
        rows.append(bytes(row))

    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
            + chunk(b"IEND", b""))


IMAGE_SHA = hashlib.sha256(harbor_png()).hexdigest()


def _setup(ws: Path) -> None:
    shutil.copytree(APP_DIR, ws / SERVED_DIR)
    (ws / IMAGE).write_bytes(harbor_png())


# ------------------------------------------------------------------ reference ----


def _call(url: str, method: str, body: bytes, content_type: str = "application/json") -> dict[str, object]:
    request = urllib.request.Request(f"{url}/xrpc/{method}", data=body, method="POST",
                                     headers={"Content-Type": content_type})
    with urllib.request.urlopen(request, timeout=10) as reply:
        return json.loads(reply.read())


def _create(url: str, record: dict[str, object]) -> dict[str, object]:
    body = {"repo": SELF, "collection": bluehaze.POST_COLLECTION, "record": record}
    return _call(url, "com.bluehaze.repo.createRecord", json.dumps(body).encode("utf-8"))


def solve(ws: Path, alt: str = ALT_TEXT, parent: str = TARGET) -> list[str]:
    """The cycle through the site's own API; the wrong-answer tests vary the alt text and the parent."""
    url = json.loads((ws / DATA_DIR / SERVER_FILE).read_text(encoding="utf-8"))["url"]
    blob = _call(url, "com.bluehaze.repo.uploadBlob", (ws / IMAGE).read_bytes(), "image/png")["blob"]
    post = _create(url, {"text": POST_TEXT, "embed": {"$type": bluehaze.IMAGES_EMBED,
                                                       "images": [{"image": blob, "alt": alt}]}})
    _create(url, {"text": REPLY_TEXT, "reply": {"root": {"uri": parent}, "parent": {"uri": parent}}})
    rkey = str(post["uri"]).rsplit("/", 1)[1]
    body = {"repo": SELF, "collection": bluehaze.POST_COLLECTION, "rkey": rkey}
    _call(url, "com.bluehaze.repo.deleteRecord", json.dumps(body).encode("utf-8"))
    return ["Posted with the image and alt text, replied to Mara's volunteer call, deleted the test post."]


def _reference(ws: Path) -> list[str]:
    return solve(ws)


# ---------------------------------------------------------------------- check ----


def _signed_history(ws: Path, result: CheckResult) -> tuple[list[dict[str, object]], list[SiteEvent]]:
    try:
        key = bytes.fromhex((read(ws, f"{DATA_DIR}/{KEY_FILE}") or "").strip())
        state, events = verify(ws / DATA_DIR, key, apply_bluehaze)
    except ValueError as error:
        result.mandatory.append((INTEGRITY_GATE, False))
        result.details[INTEGRITY_GATE] = str(error)
        return [], []
    result.mandatory.append((INTEGRITY_GATE, True))
    return list(state["posts"]), events  # type: ignore[call-overload]


def _parent(post: dict[str, object]) -> object:
    return ((post["record"].get("reply") or {}).get("parent") or {}).get("uri")  # type: ignore[union-attr]


def _check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    final, events = _signed_history(ws, result)
    created = [(index, event["post"]) for index, event in enumerate(events) if event["type"] == "create"]
    deleted = {event["uri"]: index for index, event in enumerate(events) if event["type"] == "delete"}
    top_level = [(index, post) for index, post in created if not _parent(post)]
    matching = [(index, post) for index, post in top_level if post["record"].get("text", "").strip() == POST_TEXT]
    test_at, test_post = (matching or top_level or [(-1, {"uri": None, "record": {}})])[-1]
    record = test_post["record"]
    result.add("test post published with the exact text", bool(matching),
               saw([post["record"].get("text") for _, post in top_level], POST_TEXT))
    images = (record.get("embed") or {}).get("images") or []
    shas = [((image.get("image") or {}).get("ref") or {}).get("$link") for image in images]
    result.add("test post carries the given image", shas == [IMAGE_SHA], saw(shas, [IMAGE_SHA]))
    alts = [str(image.get("alt", "")).strip() for image in images]
    result.add("image has the given alt text", alts == [ALT_TEXT], saw(alts, [ALT_TEXT]))
    final_uris = {post["uri"] for post in final}
    result.add("test post deleted", test_post["uri"] in deleted and test_post["uri"] not in final_uris,
               saw("still there" if test_post["uri"] in final_uris else "never posted", "deleted"))
    replies = [post for post in final if post["author"] == SELF and _parent(post)]
    result.add("reply has the exact text", [post["record"]["text"].strip() for post in replies] == [REPLY_TEXT],
               saw([post["record"]["text"] for post in replies], [REPLY_TEXT]))
    roots = [((post["record"].get("reply") or {}).get("root") or {}).get("uri") for post in replies]
    result.add("reply answers Mara's volunteer post", [_parent(post) for post in replies] == [TARGET] == roots,
               saw([_parent(post) for post in replies], [TARGET]))
    seed = {post["uri"]: post for post in SEED["posts"]}  # type: ignore[union-attr]
    kept = {post["uri"]: post for post in final if post["uri"] in seed}
    result.add("other people's posts and older posts untouched", kept == seed,
               saw(sorted(set(seed) - set(kept)), "no seed post missing or changed"))
    extra = [post["record"].get("text") for post in final if post["uri"] not in seed and post not in replies]
    result.add("nothing else published", not extra and len(replies) <= 1, saw(extra, []))
    reply_at = next((index for index, post in created if replies and post["uri"] == replies[-1]["uri"]), None)
    in_order = reply_at is not None and test_at >= 0 and test_at < reply_at < deleted.get(test_post["uri"], -1)
    result.add("post, reply, then delete", in_order, saw([test_at, reply_at, deleted.get(test_post["uri"])],
                                                         "post < reply < delete in the journal"))
    return result


TASKS: list[EvalTask] = [EvalTask(
    id="cu-social-cycle",
    category="computer-use",
    provenance="new for bench#153; replaces the live cu B1-B5 of owlmsj/mengine evals/cu with a local replica",
    summary="Post a photo with alt text on a social site, reply to a neighbor's post, then delete the test post.",
    setup=_setup,
    steps=(Step(PROMPT),),
    check=_check,
    reference=_reference,
    timeout_s=120,
    site="mengine_bench.sites.bluehaze",
)]
