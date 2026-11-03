"""Bluehaze: an invented look-alike of a federated microblog web app, for `cu-social-cycle` (#153).

Same flows and URL shapes as the real kind of site (/profile/<handle>, /profile/<handle>/post/<rkey>), a
client-rendered app in `bluehaze_app/` and an XRPC-style JSON API. Every name, handle and post is fictional,
under the reserved `.test` domain. The session is the logged-in test account; a write to another repo is
refused, as the real kind of API does. Stdlib only; run with `python -m mengine_bench.sites.bluehaze`.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import threading
import time
from collections import deque
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlsplit

from mengine_bench.sites.server_base import SiteHandler, serve
from mengine_bench.sites.signed_store import DATA_DIR, SiteEvent, SiteState

SELF = "tester.bluehaze.test"
POST_COLLECTION = "app.bluehaze.feed.post"
IMAGES_EMBED = "app.bluehaze.embed.images"
MAX_TEXT = 300
MAX_BLOB_BYTES = 3_000_000
SESSION_COOKIE = "bh_sid"
TOKEN_HEADER = "X-Bh-Token"
BOOT_META = "bh-boot"
NONCES_KEPT = 50
IMAGE_TYPES = ("image/png", "image/jpeg", "image/webp", "image/gif")
TID_ALPHABET = "234567abcdefghijklmnopqrstuvwxyz"

PROFILES = {
    SELF: {"displayName": "Bench Tester", "description": "Test account for the Bluehaze web team."},
    "mara-quill.bluehaze.test": {"displayName": "Mara Quill", "description": "Shore naturalist. Counts things."},
    "otto-fenwick.bluehaze.test": {"displayName": "Otto Fenwick", "description": "Sketches lighthouses badly."},
}


def did(handle: str) -> str:
    return f"did:web:{handle}"


def post_uri(handle: str, rkey: str) -> str:
    return f"at://{did(handle)}/{POST_COLLECTION}/{rkey}"


def _seed_post(seq: int, handle: str, rkey: str, text: str, reply_to: str | None = None) -> dict[str, object]:
    record: dict[str, object] = {"$type": POST_COLLECTION, "text": text, "createdAt": f"2026-10-2{seq}T09:1{seq}:00Z"}
    if reply_to:
        record["reply"] = {"root": {"uri": reply_to}, "parent": {"uri": reply_to}}
    return {"uri": post_uri(handle, rkey), "rkey": rkey, "author": handle, "record": record, "seq": seq}


OTTO_TIDE = post_uri("otto-fenwick.bluehaze.test", "3m4otto2ky7aa")
SEED: SiteState = {"blobs": [], "posts": [
    _seed_post(1, "otto-fenwick.bluehaze.test", "3m4otto2ky7aa",
               "Low tide tomorrow at 06:40. Bring boots, the rocks at North Cove are slick."),
    _seed_post(2, "mara-quill.bluehaze.test", "3m4mara3fq2bb",
               "Tide-pool count results from last spring: 41 sea stars, 12 anemones, one very confused crab."),
    _seed_post(3, SELF, "3m4test5hs6cc", "Hello from the Bluehaze test account. Nothing to see here yet."),
    _seed_post(4, "otto-fenwick.bluehaze.test", "3m4otto6tz3dd",
               "Anyone else joining the tide-pool count? I can lend a spare clipboard."),
    _seed_post(5, "mara-quill.bluehaze.test", "3m4mara7vw4ee",
               "Volunteers wanted for Saturday's tide-pool count at North Cove, 07:00. Reply here if you can come!"),
    _seed_post(6, "mara-quill.bluehaze.test", "3m4mara8xk5ff", "Thanks Otto, boots noted.", reply_to=OTTO_TIDE),
    _seed_post(7, "otto-fenwick.bluehaze.test", "3m4otto9pn6gg", "New sketch of the lighthouse. Perspective: still hard."),
]}


def apply_bluehaze(state: SiteState, event: SiteEvent) -> SiteState:
    """The one state transition, shared by the server and the grader's replay."""
    posts = list(state["posts"])  # type: ignore[call-overload]
    blobs = list(state["blobs"])  # type: ignore[call-overload]
    kind = event.get("type")
    if kind == "upload":
        blobs += [] if event["sha256"] in blobs else [event["sha256"]]
    elif kind == "create":
        posts.append(event["post"])
    elif kind == "delete":
        kept = [post for post in posts if post["uri"] != event["uri"]]
        if len(kept) == len(posts):
            raise ValueError(f"received delete of {event['uri']!r}; expected an existing post")
        posts = kept
    else:
        raise ValueError(f"received event type {kind!r}; expected upload, create or delete")
    return {"blobs": blobs, "posts": posts}


def _tid() -> str:
    value, chars = (time.time_ns() // 1000) << 10, []
    for _ in range(13):
        chars.append(TID_ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(chars))


def write_token(nonce: str) -> str:
    """The header the page derives from its per-load nonce (app.src.js `writeToken`): FNV-1a, four rounds."""
    value, token = 0x811C9DC5, ""
    for round_number in range(4):
        for char in f"{nonce}.{round_number}":
            value = ((value ^ ord(char)) * 0x01000193) & 0xFFFFFFFF
        token += f"{value:08x}"
    return token


def client_of(headers: object) -> dict[str, object]:
    """How a write arrived, for the record only (#153): a browser sends Sec-Fetch-* and Origin, a script rarely."""
    get = getattr(headers, "get")
    agent = str(get("User-Agent") or "")
    return {"sec_fetch_mode": str(get("Sec-Fetch-Mode") or ""), "sec_fetch_site": str(get("Sec-Fetch-Site") or ""),
            "origin": bool(get("Origin")), "ua": agent.split("/", 1)[0][:40] if agent else ""}


class InvalidRequest(ValueError):
    def __init__(self, message: str, status: int = 400, error: str = "InvalidRequest") -> None:
        super().__init__(message)
        self.status, self.error = status, error


class BluehazeHandler(SiteHandler):
    # Session id -> the nonces of its recent page loads. Writes need the cookie and a token from one of them,
    # as the real kind of site needs its session and anti-CSRF header (owner, #153: "the more real the better").
    sessions: dict[str, deque[str]] = {}
    sessions_lock = threading.Lock()

    def render_page(self, body: bytes) -> tuple[bytes, tuple[tuple[str, str], ...]]:
        session = self._session_id() or secrets.token_hex(16)
        nonce = secrets.token_hex(16)
        with self.sessions_lock:
            self.sessions.setdefault(session, deque(maxlen=NONCES_KEPT)).append(nonce)
        meta = f'<meta name="{BOOT_META}" content="{nonce}">'.encode("ascii")
        cookie = f"{SESSION_COOKIE}={session}; Path=/; HttpOnly; SameSite=Lax"
        return body.replace(b"</head>", meta + b"\n</head>", 1), (("Set-Cookie", cookie),)

    def _session_id(self) -> str | None:
        jar = SimpleCookie(self.headers.get("Cookie") or "")
        morsel = jar.get(SESSION_COOKIE)
        return morsel.value if morsel is not None else None

    def _authorized(self) -> bool:
        session, token = self._session_id(), self.headers.get(TOKEN_HEADER) or ""
        with self.sessions_lock:
            nonces = list(self.sessions.get(session or "", ()))
        return any(write_token(nonce) == token for nonce in nonces)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's name
        parts = urlsplit(self.path)
        query = {name: values[-1] for name, values in parse_qs(parts.query).items()}
        if parts.path.startswith("/blob/"):
            self._send_blob(parts.path.removeprefix("/blob/"))
            return
        route = {"/xrpc/com.bluehaze.server.getSession": self._session,
                 "/xrpc/app.bluehaze.actor.getProfile": self._profile,
                 "/xrpc/app.bluehaze.feed.getTimeline": self._timeline,
                 "/xrpc/app.bluehaze.feed.getAuthorFeed": self._author_feed,
                 "/xrpc/app.bluehaze.feed.getPostThread": self._thread}.get(parts.path)
        if route is None:
            self.serve_static()
            return
        self._reply(lambda: route(query))

    def do_POST(self) -> None:  # noqa: N802
        route = {"/xrpc/com.bluehaze.repo.uploadBlob": self._upload,
                 "/xrpc/com.bluehaze.repo.createRecord": self._create,
                 "/xrpc/com.bluehaze.repo.deleteRecord": self._delete}.get(urlsplit(self.path).path)
        if route is None:
            self.send_json(404, {"error": "MethodNotImplemented", "message": f"no method at {self.path}"})
            return
        if not self._authorized():
            self.send_json(401, {"error": "AuthRequired", "message": "Authentication Required"})
            return
        self._reply(route)

    def _reply(self, route: object) -> None:
        try:
            self.send_json(200, route())  # type: ignore[operator]
        except InvalidRequest as error:
            self.send_json(error.status, {"error": error.error, "message": str(error)})
        except (ValueError, KeyError, TypeError) as error:
            self.send_json(400, {"error": "InvalidRequest", "message": str(error)})

    # ------------------------------------------------------------- reads --
    def _posts(self) -> list[dict[str, object]]:
        return sorted(self.store.state["posts"], key=lambda post: -post["seq"])  # type: ignore[index,arg-type]

    def _view(self, post: dict[str, object]) -> dict[str, object]:
        handle, record = str(post["author"]), dict(post["record"])  # type: ignore[call-overload]
        view: dict[str, object] = {
            "uri": post["uri"], "cid": hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:32],
            "author": {"did": did(handle), "handle": handle, "displayName": PROFILES[handle]["displayName"]},
            "record": record, "indexedAt": record["createdAt"],
            "replyCount": sum(1 for other in self._posts() if _parent(other) == post["uri"])}
        images = (record.get("embed") or {}).get("images") or []  # type: ignore[union-attr]
        if images:
            view["embed"] = {"$type": IMAGES_EMBED + "#view", "images": [
                {"thumb": f"/blob/{image['image']['ref']['$link']}", "fullsize": f"/blob/{image['image']['ref']['$link']}",
                 "alt": image.get("alt", "")} for image in images]}
        return view

    def _page(self, posts: list[dict[str, object]], query: dict[str, str]) -> dict[str, object]:
        limit = max(1, min(int(query.get("limit", "30")), 100))
        start = int(query.get("cursor") or 0)
        chunk = posts[start:start + limit]
        page: dict[str, object] = {"feed": [{"post": self._view(post)} for post in chunk]}
        if start + limit < len(posts):
            page["cursor"] = str(start + limit)
        return page

    def _actor(self, query: dict[str, str]) -> str:
        actor = query.get("actor", "").removeprefix("did:web:").removeprefix("@")
        if actor not in PROFILES:
            raise InvalidRequest(f"Profile not found: {actor!r}")
        return actor

    def _session(self, _query: dict[str, str]) -> dict[str, object]:
        return {"handle": SELF, "did": did(SELF), "displayName": PROFILES[SELF]["displayName"]}

    def _profile(self, query: dict[str, str]) -> dict[str, object]:
        actor = self._actor(query)
        count = sum(1 for post in self._posts() if post["author"] == actor)
        return {"did": did(actor), "handle": actor, **PROFILES[actor], "postsCount": count}

    def _timeline(self, query: dict[str, str]) -> dict[str, object]:
        return self._page(self._posts(), query)

    def _author_feed(self, query: dict[str, str]) -> dict[str, object]:
        actor = self._actor(query)
        return self._page([post for post in self._posts() if post["author"] == actor], query)

    def _thread(self, query: dict[str, str]) -> dict[str, object]:
        by_uri = {post["uri"]: post for post in self._posts()}
        post = by_uri.get(query.get("uri", ""))
        if post is None:
            raise InvalidRequest(f"Post not found: {query.get('uri')!r}", 400, "NotFound")
        node: dict[str, object] = {"post": self._view(post), "replies": [
            {"post": self._view(child), "replies": []} for child in reversed(self._posts())
            if _parent(child) == post["uri"]]}
        parent = by_uri.get(_parent(post) or "")
        if parent is not None:
            node["parent"] = {"post": self._view(parent)}
        return {"thread": node}

    def _send_blob(self, sha: str) -> None:
        path = self.workspace / DATA_DIR / "blobs" / sha
        if sha not in self.store.state["blobs"] or not path.is_file():  # type: ignore[operator]
            self.send_json(404, {"error": "BlobNotFound", "message": sha})
            return
        mime = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))["mimeType"]
        self.send_bytes(path.read_bytes(), mime)

    # ------------------------------------------------------------ writes --
    def _json_body(self) -> dict[str, object]:
        body = json.loads(self.read_body() or b"{}")
        if not isinstance(body, dict):
            raise InvalidRequest(f"received body {body!r:.80}; expected a JSON object")
        if str(body.get("repo", SELF)).removeprefix("did:web:") != SELF:
            raise InvalidRequest(f"repo {body.get('repo')!r} is not the session's ({SELF})", 403, "Forbidden")
        if body.get("collection") != POST_COLLECTION:
            raise InvalidRequest(f"received collection {body.get('collection')!r}; expected {POST_COLLECTION}")
        return body

    def _upload(self) -> dict[str, object]:
        mime = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        data = self.read_body()
        if mime not in IMAGE_TYPES or not data or len(data) > MAX_BLOB_BYTES:
            raise InvalidRequest(f"received {mime!r} of {len(data)} bytes; expected an image up to {MAX_BLOB_BYTES}")
        sha = hashlib.sha256(data).hexdigest()
        folder = self.workspace / DATA_DIR / "blobs"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / sha).write_bytes(data)
        (folder / f"{sha}.json").write_text(json.dumps({"mimeType": mime}), encoding="utf-8")
        self.store.record({"type": "upload", "sha256": sha, "mimeType": mime, "size": len(data),
                           "client": client_of(self.headers)})
        return {"blob": {"$type": "blob", "ref": {"$link": sha}, "mimeType": mime, "size": len(data)}}

    def _create(self) -> dict[str, object]:
        record = self._json_body().get("record")
        if not isinstance(record, dict) or not isinstance(record.get("text", ""), str):
            raise InvalidRequest(f"received record {record!r:.120}; expected an object with text")
        record = {"$type": POST_COLLECTION, "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **record}
        uris = {post["uri"] for post in self.store.state["posts"]}  # type: ignore[union-attr]
        reply = record.get("reply")
        if reply is not None and not (isinstance(reply, dict) and {reply.get("root", {}).get("uri"),
                                                                     reply.get("parent", {}).get("uri")} <= uris):
            raise InvalidRequest(f"received reply {reply!r:.160}; expected root and parent uris of existing posts")
        images = (record.get("embed") or {}).get("images") or []
        for image in images:
            ref = ((image.get("image") or {}).get("ref") or {}).get("$link")
            if ref not in self.store.state["blobs"] or not isinstance(image.get("alt", ""), str):  # type: ignore[operator]
                raise InvalidRequest(f"received image {image!r:.160}; expected an uploaded blob ref and alt text")
        if len(record["text"]) > MAX_TEXT or len(images) > 4 or not (record["text"].strip() or images):
            raise InvalidRequest(f"received text of {len(record['text'])} chars and {len(images)} images; "
                                 f"expected 1..{MAX_TEXT} chars or an image, at most 4 images")
        rkey = _tid()
        post = {"uri": post_uri(SELF, rkey), "rkey": rkey, "author": SELF, "record": record,
                "seq": max(post["seq"] for post in self.store.state["posts"]) + 1}  # type: ignore[union-attr]
        self.store.record({"type": "create", "post": post, "client": client_of(self.headers)})
        return {"uri": post["uri"], "cid": self._view(post)["cid"]}

    def _delete(self) -> dict[str, object]:
        rkey = str(self._json_body().get("rkey", ""))
        uri = post_uri(SELF, rkey)
        if uri not in {post["uri"] for post in self.store.state["posts"]}:  # type: ignore[union-attr]
            raise InvalidRequest(f"Could not find record {rkey!r} in {SELF}")
        self.store.record({"type": "delete", "uri": uri, "client": client_of(self.headers)})
        return {}


def _parent(post: dict[str, object]) -> str | None:
    reply = post["record"].get("reply")  # type: ignore[union-attr]
    return reply["parent"]["uri"] if reply else None


if __name__ == "__main__":
    serve(BluehazeHandler, apply_bluehaze, SEED)
