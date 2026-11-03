"""Computer use on a local social-site replica, graded by server-signed state (#153).

Replaces the live cu B1-B5 eval of owlmsj/mengine (`evals/cu`), which drove a real account on a public network.
Bluehaze (`mengine_bench.sites.bluehaze`) is fictional and served from the workspace as a real site ships:
a minified bundle, a session cookie and an anti-CSRF header the page derives per load. Any route counts; the
one a run took (browser or scripted HTTP) is recorded as a note, never a grade.
"""

from __future__ import annotations

import hashlib
import http.cookiejar
import json
import re
import struct
import urllib.request
import zlib
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, read, saw, write
from mengine_bench.sites import bluehaze
from mengine_bench.sites.bluehaze import BOOT_META, SEED, SELF, TOKEN_HEADER, apply_bluehaze, write_token
from mengine_bench.sites.minify import bundle_name, minify
from mengine_bench.sites.signed_store import DATA_DIR, KEY_FILE, SERVED_DIR, SERVER_FILE, SiteEvent, verify

APP_DIR = Path(bluehaze.__file__).resolve().parent / "bluehaze_app"
IMAGE = "cover.png"
WIDTH, HEIGHT = 1200, 675
TITLE = "Harbor Day 2026"
POST_TEXT = "Testing the new Bluehaze uploader: Harbor Day is on."
ALT_TEXT = "Poster with the title Harbor Day 2026."
INTEGRITY_GATE = "site state and journal written only by the site server"

PROMPT = f"""The Bluehaze web app at {{SITE}} is signed in to the team's test account, Bench Tester
(@{SELF}). Bluehaze is a small social network, and its photo uploader ships tomorrow. Before that, the team
wants one live run of the posting cycle on this account:

1. A post with exactly the text `{POST_TEXT}`, carrying an image you make, `./{IMAGE}`: a {WIDTH}x{HEIGHT} PNG
   with the title `{TITLE}` legible on it, with the alt text `{ALT_TEXT}`
2. Then that post deleted, and only that post.

Nothing else on the network changes: other people's posts and the account's older posts stay as they are, and
nothing else is published."""


def _setup(ws: Path) -> None:
    code = minify((APP_DIR / "app.src.js").read_text(encoding="utf-8"))
    name = bundle_name(code)
    write(ws, f"{SERVED_DIR}/static/js/{name}", code)
    write(ws, f"{SERVED_DIR}/static/css/main.css", (APP_DIR / "style.css").read_text(encoding="utf-8"))
    page = (APP_DIR / "index.html").read_text(encoding="utf-8").replace("__BUNDLE__", name)
    write(ws, f"{SERVED_DIR}/index.html", page)


# ------------------------------------------------------------------ reference ----

# A 5x7 bitmap of the title's glyphs, so the reference draws legible text without an imaging library.
GLYPHS = {
    "H": "10001 10001 10001 11111 10001 10001 10001", "A": "01110 10001 10001 11111 10001 10001 10001",
    "R": "11110 10001 10001 11110 10100 10010 10001", "B": "11110 10001 10001 11110 10001 10001 11110",
    "O": "01110 10001 10001 10001 10001 10001 01110", "D": "11110 10001 10001 10001 10001 10001 11110",
    "Y": "10001 10001 01010 00100 00100 00100 00100", "2": "01110 10001 00001 00010 00100 01000 11111",
    "0": "01110 10011 10101 10101 11001 10001 01110", "6": "00110 01000 10000 11110 10001 10001 01110",
    " ": "00000 00000 00000 00000 00000 00000 00000",
}


def png_bytes(width: int, height: int, pixel: object) -> bytes:
    """An RGB PNG from `pixel(x, y) -> (r, g, b)`, stdlib only."""
    rows = b"".join(b"\x00" + b"".join(bytes(pixel(x, y)) for x in range(width)) for y in range(height))  # type: ignore[operator]

    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows, 6)) + chunk(b"IEND", b"")


@lru_cache(maxsize=2)
def poster_png(title: str = TITLE.upper(), width: int = WIDTH, height: int = HEIGHT) -> bytes:
    scale = 12
    text_w, text_h = len(title) * 6 * scale, 7 * scale
    left, top = (width - text_w) // 2, (height - text_h) // 2

    def pixel(x: int, y: int) -> tuple[int, int, int]:
        column, row = (x - left) // scale, (y - top) // scale
        glyph = column // 6
        if 0 <= row < 7 and 0 <= glyph < len(title) and column % 6 < 5 and x >= left:
            if GLYPHS[title[glyph]].split()[row][column % 6] == "1":
                return (255, 255, 255)
        return (20, 60 + y * 80 // height, 120 + y * 60 // height)

    return png_bytes(width, height, pixel)


class SiteClient:
    """The site's own write path from a script: load the page, keep its cookie, send the token it derives."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        with self.opener.open(url + "/", timeout=10) as reply:
            page = reply.read().decode("utf-8")
        found = re.search(rf'<meta name="{BOOT_META}" content="([0-9a-f]+)">', page)
        if found is None:
            raise ValueError(f"received a page without the {BOOT_META} meta; expected the site's page")
        self.token = write_token(found.group(1))

    def call(self, method: str, body: bytes, content_type: str = "application/json") -> dict[str, object]:
        request = urllib.request.Request(f"{self.url}/xrpc/{method}", data=body, method="POST",
                                         headers={"Content-Type": content_type, TOKEN_HEADER: self.token})
        with self.opener.open(request, timeout=10) as reply:
            return json.loads(reply.read())

    def create(self, record: dict[str, object]) -> dict[str, object]:
        body = {"repo": SELF, "collection": bluehaze.POST_COLLECTION, "record": record}
        return self.call("com.bluehaze.repo.createRecord", json.dumps(body).encode("utf-8"))


def solve(ws: Path, alt: str = ALT_TEXT, image: bytes | None = None, delete: bool = True) -> list[str]:
    """The cycle through the site's API; the wrong-answer tests vary the alt text, the image and the delete."""
    (ws / IMAGE).write_bytes(poster_png() if image is None else image)
    client = SiteClient(json.loads((ws / DATA_DIR / SERVER_FILE).read_text(encoding="utf-8"))["url"])
    blob = client.call("com.bluehaze.repo.uploadBlob", (ws / IMAGE).read_bytes(), "image/png")["blob"]
    post = client.create({"text": POST_TEXT, "embed": {"$type": bluehaze.IMAGES_EMBED,
                                                         "images": [{"image": blob, "alt": alt}]}})
    if not delete:
        return ["Made cover.png and posted it with the alt text."]
    body = {"repo": SELF, "collection": bluehaze.POST_COLLECTION, "rkey": str(post["uri"]).rsplit("/", 1)[1]}
    client.call("com.bluehaze.repo.deleteRecord", json.dumps(body).encode("utf-8"))
    return ["Made cover.png, posted it with the alt text, then deleted the test post."]


def _reference(ws: Path) -> list[str]:
    return solve(ws)


# ---------------------------------------------------------------------- check ----


def png_size(data: bytes) -> tuple[int, int] | None:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


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


def route_note(events: list[SiteEvent]) -> str | None:
    """#153: how the writes arrived, for the record. A browser sends Sec-Fetch-*; a script usually does not."""
    writes = [event.get("client") or {} for event in events if event.get("type") in ("upload", "create", "delete")]
    if not writes:
        return None
    browser = sum(1 for client in writes if client.get("sec_fetch_mode"))  # type: ignore[union-attr]
    route = "browser" if browser == len(writes) else "scripted HTTP" if not browser else "mixed"
    agents = sorted({str(client.get("ua") or "none") for client in writes})  # type: ignore[union-attr]
    return f"route observed: {route} ({browser} of {len(writes)} writes with Sec-Fetch-*; user agents {agents})"


def _check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    final, events = _signed_history(ws, result)
    note = route_note(events)
    if note:
        result.notes.append(note)
    image = (ws / IMAGE).read_bytes() if (ws / IMAGE).is_file() else b""
    result.add(f"{IMAGE} is a {WIDTH}x{HEIGHT} PNG", png_size(image) == (WIDTH, HEIGHT),
               saw(png_size(image), (WIDTH, HEIGHT)))
    created = [(index, event["post"]) for index, event in enumerate(events) if event["type"] == "create"]
    deleted = {event["uri"]: index for index, event in enumerate(events) if event["type"] == "delete"}
    top_level = [(index, post) for index, post in created if not _parent(post)]
    matching = [(index, post) for index, post in top_level if post["record"].get("text", "").strip() == POST_TEXT]
    test_at, test_post = (matching or top_level or [(-1, {"uri": None, "record": {}})])[-1]
    record = test_post["record"]
    result.add("test post published with the exact text", bool(matching),
               saw([post["record"].get("text") for _, post in top_level], POST_TEXT))
    images = (record.get("embed") or {}).get("images") or []
    shas = [((entry.get("image") or {}).get("ref") or {}).get("$link") for entry in images]
    want = [hashlib.sha256(image).hexdigest()] if image else ["sha256 of ./cover.png"]
    result.add(f"test post carries {IMAGE}", shas == want, saw(shas, want))
    alts = [str(entry.get("alt", "")).strip() for entry in images]
    result.add("image has the given alt text", alts == [ALT_TEXT], saw(alts, [ALT_TEXT]))
    final_uris = {post["uri"] for post in final}
    result.add("test post deleted", test_post["uri"] in deleted and test_post["uri"] not in final_uris,
               saw("still there" if test_post["uri"] in final_uris else "never posted", "deleted"))
    seed = {post["uri"]: post for post in SEED["posts"]}  # type: ignore[union-attr]
    kept = {post["uri"]: post for post in final if post["uri"] in seed}
    result.add("other people's posts and older posts untouched", kept == seed,
               saw(sorted(set(seed) - set(kept)), "no seed post missing or changed"))
    extra = [post["record"].get("text") for post in final if post["uri"] not in seed]
    result.add("nothing else published", not extra, saw(extra, []))
    in_order = 0 <= test_at < deleted.get(test_post["uri"], -1)
    result.add("post, then delete", in_order, saw([test_at, deleted.get(test_post["uri"])],
                                                  "post < delete in the journal"))
    return result


TASKS: list[EvalTask] = [EvalTask(
    id="cu-social-cycle",
    category="computer-use",
    provenance="new for bench#153; replaces the live cu B1-B5 of owlmsj/mengine evals/cu with a local replica",
    summary="Make a poster image, post it with alt text on a social site, then delete that test post.",
    setup=_setup,
    steps=(Step(PROMPT),),
    check=_check,
    reference=_reference,
    timeout_s=180,
    deliverables=(IMAGE,),
    checkpoints=checkpoints(("made the image", r"cover\.png"), ("opened the site", r"127\.0\.0\.1|navigate"),
                            ("deleted the test post", r"deleteRecord|Delete post|confirmBtn")),
    site="mengine_bench.sites.bluehaze",
)]
