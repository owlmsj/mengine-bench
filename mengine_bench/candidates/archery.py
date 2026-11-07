"""An open game brief judged by play (#214): the first level of an archery game of our own.

The owner's request (2026-11-07): an archer, a bow aimed with the mouse and pulled back for power, balloons to pop, a
score, a start and an end, in the spirit of the side-view shareware archery games of the Windows 95 days. Look, play
feel and sound are the agent's call. The checks stay basic (the page runs, draws, takes the mouse, makes sound, shows
a score and needs nothing beside itself); the main grade is the judge, which plays the stored page (#213).
A candidate (docs/CANDIDATES.md) until a release train moves it into the catalog: at most one minor a week.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, has, saw, write
from mengine_bench.tasks.visual import (ALLOWED_FONT_URLS, LOADED_RESOURCE, OPENED, PAGE_GATE, _cut_short_page,
                                        _rendered_source, _visible_chars)

PAGE = "game/index.html"
# A playable canvas game with sound is well over this; the gate only refuses a stub.
GAME_MIN_VISIBLE_CHARS = 1500
MOUSE_CHECK = "takes the mouse: press and release"
SOUND_CHECK = "makes its own sound"
SCORE_CHECK = "keeps a score"
SELF_CONTAINED_CHECK = "needs nothing beside the page"
# Only the page is kept for the judge, so a sibling file or a remote one is missing when it is played.
OUTSIDE_FILE = r"(^(https?:)?//)|\.(js|mjs|css|json|png|jpe?g|gif|webp|svg|mp3|wav|ogg|m4a|glb|gltf|woff2?)([?#].*)?$"


def _outside_files(html: str) -> list[str]:
    targets = re.findall(LOADED_RESOURCE, html, flags=re.I)
    targets += re.findall(r"\bimport\s*(?:[\w{}\s,*]+from\s*)?[\"'`]([^\"'`]+)", html)
    targets += re.findall(r"\bnew\s+Audio\s*\(\s*[\"'`]([^\"'`]+)", html)
    return [target for target in targets if re.search(OUTSIDE_FILE, target, flags=re.I)
            and not target.startswith(("data:", "blob:", *ALLOWED_FONT_URLS))]


def _game_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = _rendered_source(ws, PAGE)
    result = CheckResult(mandatory=[(PAGE_GATE, _visible_chars(html) > GAME_MIN_VISIBLE_CHARS)],
                         waived_at_limit=_cut_short_page(html))
    result.add(MOUSE_CHECK, has(html, r"(pointer|mouse)down") and has(html, r"(pointer|mouse)up"))
    result.add(SOUND_CHECK, has(html, r"\b(webkit)?AudioContext\b|\bnew\s+Audio\s*\(|<audio\b"))
    result.add(SCORE_CHECK, has(html, r"\bscore|points\b|pontos|placar"))
    outside = _outside_files(html)
    result.add(SELF_CONTAINED_CHECK, bool(html.strip()) and not outside, saw(outside[:3], []))
    return result


def _game_reference(ws: Path) -> list[str]:
    write(ws, PAGE, GAME_REFERENCE)
    return ["done"]


GAME_REFERENCE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Balloon Bow</title>
<style>html,body{margin:0;height:100%;overflow:hidden;background:#9fd3f0;font-family:system-ui,sans-serif}
canvas{display:block;width:100vw;height:100vh;cursor:crosshair}</style></head>
<body><canvas id="game"></canvas><script>
const canvas = document.getElementById("game"), g = canvas.getContext("2d");
const W = 1440, H = 900, ARCHER = {x: 150, y: 560}, GRAVITY = 900, MAX_PULL = 170, ARROWS = 12, GOAL = 10;
canvas.width = W; canvas.height = H;
let state = "title", score = 0, arrowsLeft = ARROWS, popped = 0, pull = null, flying = [], balloons = [], bits = [];
let spawnIn = 0, last = performance.now(), audio = null;

function sound(kind) {
  audio = audio || new AudioContext();
  const now = audio.currentTime, osc = audio.createOscillator(), gain = audio.createGain();
  const shapes = {twang: ["triangle", 220, 90, 0.18], pop: ["square", 900, 120, 0.12],
                  over: ["sawtooth", 330, 110, 0.6], start: ["sine", 440, 880, 0.2]};
  const [wave, from, to, length] = shapes[kind];
  osc.type = wave; osc.frequency.setValueAtTime(from, now);
  osc.frequency.exponentialRampToValueAtTime(to, now + length);
  gain.gain.setValueAtTime(0.25, now); gain.gain.exponentialRampToValueAtTime(0.001, now + length);
  osc.connect(gain).connect(audio.destination); osc.start(now); osc.stop(now + length);
}

function newGame() {
  state = "play"; score = 0; arrowsLeft = ARROWS; popped = 0; flying = []; balloons = []; bits = []; spawnIn = 0;
  sound("start");
}

function point(event) {
  const box = canvas.getBoundingClientRect();
  return {x: (event.clientX - box.left) * W / box.width, y: (event.clientY - box.top) * H / box.height};
}

canvas.addEventListener("pointerdown", (event) => {
  if (state !== "play") { newGame(); return; }
  if (arrowsLeft > 0) pull = {from: point(event), to: point(event)};
});
canvas.addEventListener("pointermove", (event) => { if (pull) pull.to = point(event); });
canvas.addEventListener("pointerup", () => {
  if (!pull) return;
  const dx = pull.from.x - pull.to.x, dy = pull.from.y - pull.to.y;
  const strength = Math.min(Math.hypot(dx, dy), MAX_PULL) / MAX_PULL;
  pull = null;
  if (strength < 0.08) return;
  const angle = Math.atan2(dy, dx), speed = 500 + strength * 1100;
  flying.push({x: ARCHER.x + 30, y: ARCHER.y - 40, vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed});
  arrowsLeft -= 1; sound("twang");
});

function aimAngle() {
  if (!pull) return -0.3;
  return Math.atan2(pull.from.y - pull.to.y, pull.from.x - pull.to.x);
}

function update(dt) {
  if (state !== "play") return;
  spawnIn -= dt;
  if (spawnIn <= 0) {
    spawnIn = 0.7 + Math.random() * 0.6;
    const hue = [0, 45, 200, 280, 120][Math.floor(Math.random() * 5)];
    balloons.push({x: 650 + Math.random() * 700, y: H + 60, r: 30 + Math.random() * 12, vy: 70 + Math.random() * 60, hue});
  }
  balloons.forEach((b) => { b.y -= b.vy * dt; });
  balloons = balloons.filter((b) => b.y > -80);
  flying.forEach((a) => { a.vy += GRAVITY * dt; a.x += a.vx * dt; a.y += a.vy * dt; });
  for (const a of flying) {
    for (const b of balloons) {
      if (!b.hit && Math.hypot(a.x - b.x, a.y - b.y) < b.r) {
        b.hit = true; score += 10; popped += 1; sound("pop");
        for (let i = 0; i < 14; i++) bits.push({x: b.x, y: b.y, vx: (Math.random() - 0.5) * 400,
                                                vy: (Math.random() - 0.5) * 400, life: 0.6, hue: b.hue});
      }
    }
  }
  balloons = balloons.filter((b) => !b.hit);
  flying = flying.filter((a) => a.x < W + 50 && a.y < H + 50 && a.x > -50);
  bits.forEach((p) => { p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt; });
  bits = bits.filter((p) => p.life > 0);
  if (arrowsLeft === 0 && flying.length === 0) { state = "over"; sound("over"); }
}

function drawArcher() {
  const {x, y} = ARCHER, angle = aimAngle(), draw = pull ? Math.min(Math.hypot(pull.from.x - pull.to.x,
    pull.from.y - pull.to.y), MAX_PULL) / MAX_PULL : 0;
  g.strokeStyle = "#2b2b2b"; g.lineWidth = 6; g.lineCap = "round";
  g.beginPath(); g.arc(x, y - 110, 18, 0, Math.PI * 2); g.fillStyle = "#f2c79b"; g.fill();
  g.beginPath(); g.moveTo(x, y - 92); g.lineTo(x, y - 20); g.lineTo(x - 20, y + 40); g.moveTo(x, y - 20);
  g.lineTo(x + 20, y + 40); g.stroke();
  g.save(); g.translate(x + 20, y - 60); g.rotate(angle);
  g.strokeStyle = "#7a4a1d"; g.lineWidth = 7; g.beginPath(); g.arc(0, 0, 60, -1.2, 1.2); g.stroke();
  g.strokeStyle = "#eee"; g.lineWidth = 2; g.beginPath();
  g.moveTo(Math.cos(-1.2) * 60, Math.sin(-1.2) * 60); g.lineTo(-draw * 50, 0);
  g.lineTo(Math.cos(1.2) * 60, Math.sin(1.2) * 60); g.stroke();
  if (arrowsLeft > 0) { g.strokeStyle = "#3a2a1a"; g.lineWidth = 4; g.beginPath(); g.moveTo(-draw * 50, 0);
    g.lineTo(70 - draw * 50, 0); g.stroke(); }
  g.restore();
  if (pull) {
    g.fillStyle = "rgba(0,0,0,0.25)"; g.fillRect(x - 60, y + 70, 120, 14);
    g.fillStyle = draw > 0.8 ? "#e53935" : "#fbc02d"; g.fillRect(x - 60, y + 70, 120 * draw, 14);
  }
}

function render() {
  g.fillStyle = "#9fd3f0"; g.fillRect(0, 0, W, H);
  g.fillStyle = "#6fbf5f"; g.fillRect(0, H - 120, W, 120);
  balloons.forEach((b) => {
    g.strokeStyle = "#555"; g.lineWidth = 1; g.beginPath(); g.moveTo(b.x, b.y + b.r); g.lineTo(b.x, b.y + b.r + 40); g.stroke();
    g.fillStyle = "hsl(" + b.hue + ",80%,55%)"; g.beginPath(); g.ellipse(b.x, b.y, b.r * 0.85, b.r, 0, 0, Math.PI * 2); g.fill();
  });
  flying.forEach((a) => {
    const angle = Math.atan2(a.vy, a.vx);
    g.save(); g.translate(a.x, a.y); g.rotate(angle); g.strokeStyle = "#3a2a1a"; g.lineWidth = 4;
    g.beginPath(); g.moveTo(-60, 0); g.lineTo(0, 0); g.stroke(); g.restore();
  });
  bits.forEach((p) => { g.fillStyle = "hsl(" + p.hue + ",80%,55%)"; g.fillRect(p.x, p.y, 6, 6); });
  drawArcher();
  g.fillStyle = "#123"; g.font = "bold 40px system-ui"; g.fillText("Score " + score, 40, 60);
  g.fillText("Arrows " + arrowsLeft, 40, 110);
  if (state !== "play") {
    g.fillStyle = "rgba(10,30,50,0.6)"; g.fillRect(0, 0, W, H); g.fillStyle = "#fff"; g.textAlign = "center";
    g.font = "bold 80px system-ui"; g.fillText(state === "title" ? "Balloon Bow" : "Game over", W / 2, H / 2 - 40);
    g.font = "36px system-ui";
    g.fillText(state === "title" ? "Drag back from anywhere to pull the bow, release to shoot. Click to start."
               : "You popped " + popped + " balloons for " + score + " points. Click to play again.", W / 2, H / 2 + 30);
    g.textAlign = "left";
  }
}

function frame(now) {
  update(Math.min((now - last) / 1000, 0.05)); last = now; render(); requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script></body></html>
"""

TASKS = [
    EvalTask(
        id="web-archery-game", category="web-game",
        provenance="Owner's open game brief (#214): the first level of an archery game of our own, in the spirit of "
                   "the side-view shareware archery games of the Windows 95 days; judged by play (#213)",
        summary="Build the first level of a small archery game, then the judge plays it.",
        setup=lambda ws: None, check=_game_check, reference=_game_reference,
        # #137 rule on the Opus 5.5 xhigh probe (#214): 232.7 s x1.25, rounded up to 30 s.
        timeout_s=300, deliverables=(PAGE,),
        judge_notes=("The brief values the play most: a pull-and-release aim that feels good, balloons that pop with\n"
                     "clear feedback, sound on shots and hits, a visible score, and a start, an end and a way to play again."),
        judge_play=("Find how to start, then pull the bow and shoot several times, adjusting the aim from the frames\n"
                    "until a balloon pops and the score moves. Then play on until the game ends, and start a new one."),
        checkpoints=checkpoints(("wrote the game", r"game.{1,4}index\.html"), OPENED),
        steps=(Step("Remember the little archery games of the Windows 95 days? We want the first level of one, our "
                    "own, in {WS}/game/index.html, a single file. An archer you aim with the mouse, pulling the bow back "
                    "for power, balloons to pop, a score on screen, a way to start and a way to lose. How it looks, plays "
                    "and sounds is your call, and that is what we care about most: a minute of play should be fun, and "
                    "every shot and hit should feel and sound good. It is reviewed by opening the file, with no build "
                    "step, in a browser that reaches only Google Fonts, and by playing it."),),
    ),
]
