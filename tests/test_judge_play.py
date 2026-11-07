"""#213: the judge plays an interactive page before it votes: driver, reply contract, loop and bundle files."""

from __future__ import annotations

import contextlib
import io
import dataclasses
import json
import socket
import struct
import threading
import time
from collections.abc import Iterator
from pathlib import Path

import pytest

from conftest import FakeAgent
from mengine_bench import bundle_judge, catalog, judge, play, visual
from test_bundle_judge import VISUAL_AGENT, _judge, _render_except, _run, _template

PLAY_REPLY = {"notes": "a page", "actions": [{"do": "click", "x": 10, "y": 20, "shot": True}, {"do": "wait", "ms": 5}],
              "done": False}


# ------------------------------------------------------------- websocket ---


def _server_frame(opcode: int, payload: bytes, fin: bool = True) -> bytes:
    size = len(payload)
    if size < 126:
        head = bytes([size])
    elif size < 1 << 16:
        head = bytes([126]) + struct.pack(">H", size)
    else:
        head = bytes([127]) + struct.pack(">Q", size)
    return bytes([(0x80 if fin else 0) | opcode]) + head + payload


def _read_client_frame(conn: socket.socket) -> tuple[int, bytes]:
    def take(size: int) -> bytes:
        data = b""
        while len(data) < size:
            data += conn.recv(size - len(data))
        return data

    first, second = take(2)
    size = second & 0x7F
    if size == 126:
        size = struct.unpack(">H", take(2))[0]
    elif size == 127:
        size = struct.unpack(">Q", take(8))[0]
    assert second & 0x80, "a client frame must be masked (RFC 6455 5.3)"
    mask = take(4)
    return first & 0x0F, bytes(b ^ mask[i % 4] for i, b in enumerate(take(size)))


def test_the_websocket_client_speaks_the_frames_devtools_sends() -> None:
    big = "x" * 70_000  # a screenshot is far over the 16-bit length
    got: dict[str, object] = {}
    listener = socket.create_server(("127.0.0.1", 0))

    def serve() -> None:
        conn, _ = listener.accept()
        with conn:
            request = b""
            while b"\r\n\r\n" not in request:
                request += conn.recv(4096)
            got["request"] = request.decode("ascii")
            conn.sendall(b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n")
            got["sent"] = _read_client_frame(conn)
            conn.sendall(_server_frame(0x9, b"hi") + _server_frame(0x1, b"he", fin=False) + _server_frame(0x0, b"llo"))
            got["pong"] = _read_client_frame(conn)
            conn.sendall(_server_frame(0x1, big.encode()))

    thread = threading.Thread(target=serve)
    thread.start()
    client = play.CdpSocket(f"ws://127.0.0.1:{listener.getsockname()[1]}/devtools/page/1", timeout_s=5)
    client.send_text('{"id": 1}')
    assert client.recv_text() == "hello"
    assert client.recv_text() == big
    client.close()
    thread.join(5)
    listener.close()
    assert str(got["request"]).startswith("GET /devtools/page/1 HTTP/1.1\r\n")
    assert got["sent"] == (0x1, b'{"id": 1}')
    assert got["pong"] == (0xA, b"hi")


def test_a_refused_handshake_names_what_it_got() -> None:
    listener = socket.create_server(("127.0.0.1", 0))

    def serve() -> None:
        conn, _ = listener.accept()
        with conn:
            conn.recv(4096)
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

    thread = threading.Thread(target=serve)
    thread.start()
    with pytest.raises(play.CdpError, match="received handshake .*404.*expected HTTP 101"):
        play.CdpSocket(f"ws://127.0.0.1:{listener.getsockname()[1]}/x", timeout_s=5)
    thread.join(5)
    listener.close()


# ---------------------------------------------------------------- replies ---


def test_a_play_reply_becomes_bounded_actions() -> None:
    plan = play.parse_play_reply("Sure.\n" + json.dumps({"notes": "start", "done": True, "actions": [
        {"do": "down", "x": 100, "y": 500}, {"do": "move", "x": 40, "y": 560, "ms": 600, "shot": True},
        {"do": "up"}, {"do": "key", "key": "Space", "ms": 50}, {"do": "wait", "ms": 1500}]}))
    assert plan.done and plan.notes == "start"
    assert [action.text() for action in plan.actions] == [
        "down 100,500", "move 40,560 600ms +shot", "up", "key Space 50ms", "wait 1500ms"]


@pytest.mark.parametrize("reply,expected", [
    ({"actions": [{"do": "click", "x": 1280, "y": 1}], "done": False}, "x=1280; expected an integer 0..1279"),
    ({"actions": [{"do": "wait", "ms": 60_000}], "done": False}, "ms=60000; expected an integer 0..4000"),
    ({"actions": [{"do": "key", "key": "F5"}], "done": False}, "key 'F5'"),
    ({"actions": [{"do": "jump"}], "done": False}, "expected an object whose do is one of"),
    ({"actions": [{"do": "up", "shot": True}, {"do": "up", "shot": True}], "done": False}, "2 shots"),
    ({"actions": [{"do": "up"}] * 13, "done": False}, "at most 12"),
    ({"actions": []}, "done=None"),
])
def test_a_play_reply_out_of_bounds_is_refused_with_what_it_received(reply: dict[str, object], expected: str) -> None:
    with pytest.raises(ValueError, match=expected.replace("(", r"\(").replace(")", r"\)")):
        play.parse_play_reply(json.dumps(reply))


# ------------------------------------------------------------------- loop ---


class FakeDriver:
    def __init__(self, fail_after: int | None = None) -> None:
        self.done: list[str] = []
        self.shots = 0
        self.fail_after = fail_after

    def act(self, action: play.PlayAction) -> None:
        self.done.append(action.text())

    def score(self) -> int | None:
        return None

    def hold(self) -> None:
        self.done.append("hold")

    def release(self) -> None:
        self.done.append("release")

    def frame(self) -> bytes:
        if self.fail_after is not None and self.shots >= self.fail_after:
            raise play.CdpError("received EOF from DevTools; expected more frames")
        self.shots += 1
        return f"frame {self.shots}".encode()

    def drain(self) -> tuple[list[dict[str, object]], list[str]]:
        return [{"t": 1200, "kind": "oscillator", "wave": "sine", "hz": 440, "state": "running"}], ["Error: boom"]


def _opener(driver: FakeDriver) -> play.PlayOpener:
    @contextlib.contextmanager
    def open_driver(html: Path) -> Iterator[play.PlayDriver]:
        yield driver

    return open_driver


def _replies(monkeypatch: pytest.MonkeyPatch, replies: list[str]) -> list[tuple[str, tuple[str, ...], str]]:
    asked: list[tuple[str, tuple[str, ...], str]] = []
    pending = iter(replies)

    def fake_ask(agent: object, prompt: str, audit: Path, timeout_s: float, files: dict[str, Path] | None = None,
                 system_prompt: str = "") -> str:
        asked.append((prompt, tuple(files or {}), system_prompt))
        return next(pending)

    monkeypatch.setattr(judge, "_ask", fake_ask)
    return asked


def test_the_judge_plays_turn_by_turn_on_the_frames_of_the_last_turn(tmp_path: Path,
                                                                      monkeypatch: pytest.MonkeyPatch) -> None:
    asked = _replies(monkeypatch, [json.dumps(PLAY_REPLY), json.dumps({**PLAY_REPLY, "done": True})])
    driver = FakeDriver()
    record = play.play_page(object(), tmp_path / "page.html", "build a game", "start it", tmp_path, 9,  # type: ignore[arg-type]
                            opener=_opener(driver))
    assert [prompt.count("turn 1 of 5") for prompt, _, _ in asked] == [1, 0]
    assert [files for _, files, _ in asked] == [("play-00.png",), ("play-01.png", "play-02.png")]
    assert all(rules == play.PLAY_SYSTEM_PROMPT for _, _, rules in asked)
    assert "build a game" in asked[0][0] and "start it" in asked[0][0]
    # The page clock stops before each frame the judge reads and runs again only for its actions.
    assert driver.done == ["hold", *["release", "click 10,20 +shot", "wait 5ms", "hold"] * 2]
    assert list(record.frames) == [f"play-0{n}.png" for n in range(5)]
    assert (tmp_path / "play" / "play-04.png").read_bytes() == b"frame 5"
    log = play.play_log_text(record)
    assert "turn 1: frames play-01.png, play-02.png" in log and "judge notes: a page" in log
    assert "1.2s oscillator wave=sine hz=440 state=running" in log and "page errors: Error: boom" in log


def test_a_judge_that_cannot_reply_ends_the_play_and_keeps_what_it_saw(tmp_path: Path,
                                                                       monkeypatch: pytest.MonkeyPatch) -> None:
    asked = _replies(monkeypatch, [json.dumps(PLAY_REPLY), "no json", '{"actions": "x"}'])
    record = play.play_page(object(), tmp_path / "page.html", "b", "g", tmp_path, 9,  # type: ignore[arg-type]
                            opener=_opener(FakeDriver()))
    assert len(asked) == 3, "one retry per turn, then the play stops"
    assert len(record.turns) == 2 and list(record.frames) == ["play-00.png", "play-01.png", "play-02.png"]
    assert record.problems and record.problems[0].startswith("turn 2: no valid play reply in 2 attempts")


def test_a_browser_that_dies_mid_play_keeps_the_frames_before_it(tmp_path: Path,
                                                                  monkeypatch: pytest.MonkeyPatch) -> None:
    _replies(monkeypatch, [json.dumps(PLAY_REPLY)])
    record = play.play_page(object(), tmp_path / "page.html", "b", "g", tmp_path, 9,  # type: ignore[arg-type]
                            opener=_opener(FakeDriver(fail_after=2)))
    assert list(record.frames) == ["play-00.png", "play-01.png"]
    assert record.problems == ["browser: received EOF from DevTools; expected more frames"]


# --------------------------------------------------------------- bundle ---

PLAYING_JUDGE = r"""
import json, os, sys
from pathlib import Path
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
log = Path(__file__).with_suffix(".calls")
attached = next((line for line in prompt.split("\n") if "Attached images" in line), "")
log.write_text((log.read_text() if log.exists() else "") + json.dumps(
    {"play": prompt.startswith("You are playtesting"), "attached": attached, "files": sorted(os.listdir(".")),
     "has_log": "## Judge play (recorded by the benchmark)" in prompt}) + "\n")
if prompt.startswith("You are playtesting"):
    print(json.dumps({"notes": "pressed", "actions": [{"do": "click", "x": 5, "y": 5}], "done": True}))
else:
    print(json.dumps({"score": 80, "approach": 30, "deliverable": 25, "rendered": 25, "rationale": "solid"}))
"""


def test_a_task_with_judge_play_is_played_then_voted_and_the_bundle_keeps_the_play(
        fake_agent: FakeAgent, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    landing = catalog.task_by_id("web-mondrian-landing")
    assert landing is not None
    playing = dataclasses.replace(landing, judge_play="Click anywhere.")
    monkeypatch.setattr(bundle_judge.catalog, "task_by_id", lambda task_id: playing)
    bundle = _run(fake_agent, tmp_path / "results", "web-mondrian-landing", VISUAL_AGENT)
    monkeypatch.setattr(bundle_judge, "render_headless", _render_except(None, []))
    stale = bundle / "judge" / "web-mondrian-landing-play-07.png"
    stale.write_bytes(b"an older vote")
    monkeypatch.setattr(play, "open_play_driver", _opener(FakeDriver()))
    assert _judge(fake_agent, bundle, PLAYING_JUDGE) == 0
    calls = [json.loads(line) for line in (tmp_path / "fakes" / "judge.calls").read_text(encoding="utf-8").splitlines()]
    assert [call["play"] for call in calls] == [True, False]
    assert calls[0]["files"] == ["play-00.png"]
    assert calls[1]["attached"] == ("Attached images, in this order: frame-1s.png, frame-4s.png, screenshot.png, "
                                    "play-00.png, play-01.png, reference.png.")
    assert calls[1]["has_log"]
    stored = bundle / "judge"
    assert (stored / "web-mondrian-landing-play-01.png").read_bytes() == b"frame 2"
    assert not stale.exists(), "--again and a new vote must not keep another vote's play frame"
    kept = json.loads((stored / "web-mondrian-landing-play.json").read_text(encoding="utf-8"))
    assert [turn["actions"] for turn in kept["turns"]] == [[], ["click 5,5"]]


def test_judge_play_needs_a_page_and_three_lines_at_most() -> None:
    landing = catalog.task_by_id("web-mondrian-landing")
    plain = catalog.task_by_id("rs-lock-bug")
    assert landing is not None and plain is not None
    with pytest.raises(ValueError, match="expected an HTML deliverable to play"):
        dataclasses.replace(plain, judge_play="Click.")
    with pytest.raises(ValueError, match="4 lines of judge_play"):
        dataclasses.replace(landing, judge_play="a\nb\nc\nd")


# ------------------------------------------------------------------ live ---

LIVE_PAGE = """<!doctype html><body style="margin:0"><canvas id="c" width="1440" height="900"></canvas><script>
const g = document.getElementById('c').getContext('2d'); let score = 0, ctx = null;
const draw = () => { g.fillStyle = '#fff'; g.fillRect(0, 0, 1440, 900); g.fillStyle = '#000';
  g.font = '64px sans-serif'; g.fillText('Score ' + score, 40, 100); };
addEventListener('pointerdown', () => { score += 1; ctx = ctx || new AudioContext(); const o = ctx.createOscillator();
  o.frequency.value = 660; o.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.05); draw(); });
addEventListener('keydown', (e) => { if (e.code !== 'Space') return; score += 10; draw();
  const o = ctx.createOscillator(); o.frequency.setValueAtTime(300, ctx.currentTime);
  o.frequency.exponentialRampToValueAtTime(600, ctx.currentTime + 0.05); o.connect(ctx.destination); o.start();
  throw new Error('space'); });
draw();</script>"""


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
def test_the_driver_plays_a_real_page_and_hears_what_it_starts(tmp_path: Path) -> None:
    page = tmp_path / "page.html"
    page.write_text(LIVE_PAGE, encoding="utf-8")
    with play.open_play_driver(page) as driver:
        before = driver.frame()
        driver.act(play.PlayAction("click", 300, 300))
        driver.act(play.PlayAction("key", key="Space"))
        after = driver.frame()
        sounds, errors = driver.drain()
    assert before[:8] == after[:8] == b"\x89PNG\r\n\x1a\n" and before != after
    # A pitch set by automation shows where it starts and ends, not the node's default 440.
    assert [(s["kind"], s["hz"], s["state"]) for s in sounds] == [("oscillator", 660, "running"),
                                                               ("oscillator", "300->600", "running")]
    assert errors and "space" in errors[0]


HELD_PAGE = """<!doctype html><body style="margin:0"><canvas id="c" width="1440" height="900"></canvas><script>
const g = document.getElementById('c').getContext('2d'); let x = 0, last = performance.now(), biggest = 0;
const tick = (now) => { const dt = now - last; last = now; biggest = Math.max(biggest, dt); x = (x + dt / 4) % 1400;
  g.fillStyle = '#fff'; g.fillRect(0, 0, 1440, 900); g.fillStyle = '#c00'; g.fillRect(x, 400, 40, 40);
  requestAnimationFrame(tick); };
requestAnimationFrame(tick); setInterval(() => { window.ticks = (window.ticks || 0) + 1; }, 100);</script>"""


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
def test_a_held_page_waits_for_the_judge_and_resumes_without_a_jump(tmp_path: Path) -> None:
    # #213: in the first live play balloons escaped while the judge thought, and it blamed the game for it.
    page = tmp_path / "page.html"
    page.write_text(HELD_PAGE, encoding="utf-8")
    evaluate = "[performance.now(), window.ticks || 0, biggest]"
    with play.open_play_driver(page) as driver:
        assert isinstance(driver, play.ChromiumPlayDriver)
        driver.hold()
        before = driver.frame()
        clock = driver.session.call("Runtime.evaluate", expression=evaluate, returnByValue=True)["result"]["value"]
        time.sleep(1.5)
        assert driver.frame() == before
        held = driver.session.call("Runtime.evaluate", expression=evaluate, returnByValue=True)["result"]["value"]
        driver.session.call("Runtime.evaluate", expression="biggest = 0")
        driver.release()
        driver.act(play.PlayAction("wait", ms=300))
        after = driver.session.call("Runtime.evaluate", expression=evaluate, returnByValue=True)["result"]["value"]
    assert held[0] - clock[0] < 50 and held[1] == clock[1], "no page time and no interval tick while held"
    assert after[2] < 500, "the first frame after the release sees a normal step, not the 1.5 s the judge took"


# A canvas sized in device pixels with no CSS size: right at ratio 1, cropped on any scaled screen (#213, the Opus probe).
SCALED_PAGE = """<!doctype html><style>html,body{margin:0;overflow:hidden}canvas{display:block}__CSS__</style>
<canvas id="c"></canvas><script>
const c = document.getElementById('c'), g = c.getContext('2d'), r = devicePixelRatio;
c.width = innerWidth * r; c.height = innerHeight * r; g.scale(r, r);
g.fillStyle = '#fff'; g.fillRect(0, 0, innerWidth, innerHeight);
g.fillStyle = '#c00'; g.fillRect(innerWidth - 60, innerHeight - 60, 60, 60);</script>"""


@pytest.mark.skipif(visual.find_browser() is None, reason="no Chromium-family browser on PATH")
@pytest.mark.parametrize("css,corner_seen", [("", False), ("canvas{width:100vw;height:100vh}", True)])
def test_the_judge_plays_on_a_scaled_laptop_screen(tmp_path: Path, css: str, corner_seen: bool) -> None:
    # The owner opened the 91-point Opus game on a 150% screen and it was cropped; at ratio 1 the judge never saw it.
    from PIL import Image

    page = tmp_path / "page.html"
    page.write_text(SCALED_PAGE.replace("__CSS__", css), encoding="utf-8")
    with play.open_play_driver(page) as driver:
        frame = Image.open(io.BytesIO(driver.frame())).convert("RGB")
    assert frame.size == (play.VIEW_W, play.VIEW_H), "frames stay on the CSS grid the actions use"
    red, green, blue = frame.getpixel((play.VIEW_W - 20, play.VIEW_H - 20))
    assert (red > 150 and green < 80 and blue < 80) is corner_seen
