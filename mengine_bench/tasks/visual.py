"""One-shot visual artifact tasks: a researched landing page and a 3D scene.

One user request, no second turn: the agent must research, design and ship a
complete single-file artifact. Grading = deterministic checks (file, facts,
palette, three.js usage, non-blank render) as gates + a vision checklist
answered by a judge; aesthetics pass at 70% (mengine_bench.visual).
Ported from the private suite; the landing subject was replaced with a public
art-history topic that keeps the Mondrian visual brief.
"""

from __future__ import annotations

import html as html_lib
import re
import unicodedata
from collections.abc import Sequence
from pathlib import Path

from mengine_bench import visual
from mengine_bench.core import CheckResult, EvalTask, Step, has, read, write

ONE_SHOT = ("This is your ONLY request: there will be no second turn and no answers to questions. "
            "Deliver the complete, working final file. Work only inside {WS}.")
MIN_PNG_BYTES = 10_000


def _plain(text: str) -> str:
    # Agents write accents and HTML entities (&eacute;); fold both before matching.
    text = html_lib.unescape(text)
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()


def _hex_colors(html: str) -> list[tuple[int, int, int]]:
    colors = []
    for match in re.finditer(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", html):
        h = match.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        colors.append((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    return colors


def _mondrian_palette(html: str) -> bool:
    colors = _hex_colors(html)
    names = _plain(html)
    red = any(r > 170 and g < 90 and b < 90 for r, g, b in colors) or re.search(r"\bred\b", names)
    blue = any(b > 110 and r < 90 and g < 140 for r, g, b in colors) or re.search(r"\bblue\b", names)
    yellow = any(r > 200 and g > 160 and b < 110 for r, g, b in colors) or re.search(r"\byellow\b", names)
    black = any(max(c) < 45 for c in colors) or re.search(r"\bblack\b", names)
    return bool(red and blue and yellow and black)


# Broken renders and missing required content cannot be outvoted by style.
MANDATORY_VISUAL = frozenset({
    "No text overlapping, clipped or overflowing its block",
    "A visible button or call to action exists",
    "The page looks finished: no lorem ipsum, placeholders or broken empty areas",
    "Finished look, no glitches, black screen or broken geometry",
})

# ------------------------------------------------------ web-mondrian-landing --

LANDING = "landing/index.html"
LANDING_CHECKLIST = (
    "Piet Mondrian style composition: rectangular blocks separated by thick black lines",
    "Palette dominated by red, blue, yellow, white and black",
    "Hero at the top with a large, legible title",
    "Clear typographic hierarchy (title, subtitles and body are distinguishable)",
    "No text overlapping, clipped or overflowing its block",
    "A visible button or call to action exists",
    "Asymmetric grid (blocks of different sizes, not a uniform grid)",
    "The page looks finished: no lorem ipsum, placeholders or broken empty areas",
)


def _landing_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = read(ws, LANDING) or ""
    plain = _plain(html)
    deterministic = [
        ("index.html exists with content", len(html) > 1500),
        ("has a page title and an h1", has(html, r"<title>[^<]{3,}</title>") and has(html, r"<h1\b")),
        ("names the painting (Composition with Red, Blue and Yellow)",
         has(plain, r"composition\s+(ii\s+)?with\s+red,?\s+blue,?\s+and\s+yellow")),
        ("names the painter (Piet Mondrian)", "piet mondrian" in plain),
        ("states the year 1930", "1930" in plain),
        ("names the De Stijl movement", "de stijl" in plain),
        ("links to an external source", has(html, r'href="https?://')),
        ("CSS with the Mondrian palette (red, blue, yellow, black)", _mondrian_palette(html)),
        ("has a call-to-action element",
         has(html, r"<button\b|<a\b[^>]*(class|role)=\"[^\"]*(cta|btn|button)")),
    ]
    return visual.grade(ws, LANDING, deterministic, LANDING_CHECKLIST, MANDATORY_VISUAL, MIN_PNG_BYTES)


LANDING_REFERENCE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Composition with Red, Blue and Yellow</title>
<style>
:root{--r:#d40920;--b:#1356a2;--y:#f7d842;--k:#111111;--w:#f8f5ee}
*{box-sizing:border-box}body{margin:0;background:var(--k);font-family:Helvetica,Arial,sans-serif;color:var(--k)}
.grid{display:grid;grid-template-columns:2fr 1fr 1.3fr;grid-template-rows:auto auto auto;gap:14px;padding:14px;min-height:100vh}
.c{background:var(--w);padding:28px}.r{background:var(--r);color:var(--w)}.b{background:var(--b);color:var(--w)}.y{background:var(--y)}
.hero{grid-column:1/3;grid-row:1;padding:48px}.hero h1{font-size:64px;line-height:1;margin:0 0 16px;letter-spacing:-2px}
.hero p{font-size:20px;max-width:640px}h2{font-size:26px;margin:0 0 10px}p{font-size:16px;line-height:1.5}
.cta{display:inline-block;margin-top:18px;background:var(--k);color:var(--w);padding:14px 22px;text-decoration:none;font-weight:700}
.tall{grid-column:3;grid-row:1/3}.wide{grid-column:2/4}
</style></head><body><main class="grid">
<section class="c hero"><h1>Composition with Red, Blue and Yellow</h1>
<p>In 1930 Piet Mondrian reduced painting to a white field, thick black lines and three primary colours.</p>
<a class="cta" href="https://en.wikipedia.org/wiki/Composition_with_Red,_Blue_and_Yellow">Read about the painting</a></section>
<section class="c r tall"><h2>The painter</h2><p>Piet Mondrian (1872-1944) was a Dutch painter who moved from landscapes to pure abstraction.</p></section>
<section class="c y"><h2>De Stijl</h2><p>De Stijl, founded in the Netherlands in 1917, sought a universal visual language of straight lines and primary colours.</p></section>
<section class="c b"><h2>Neoplasticism</h2><p>Only horizontal and vertical lines, the three primaries, and white, grey and black.</p></section>
<section class="c wide"><h2>Why it matters</h2><p>The asymmetric balance of a large red square and small blue and yellow blocks shaped modern graphic design and architecture.
Source: <a href="https://en.wikipedia.org/wiki/De_Stijl">De Stijl on Wikipedia</a>.</p></section>
</main></body></html>
"""


# -------------------------------------------------------- 3d-voxel-landscape --

SCENE = "scene/index.html"
SCENE_CHECKLIST = (
    "Large, recognisable conical mountain with a snowy peak (Mount Fuji)",
    "Multi-tier pagoda in a red tone",
    "Pink trees or canopies (cherry blossoms)",
    "Sky with atmosphere (gradient, sunset, haze or clouds)",
    "Evident low poly or voxel style (flat facets or cubes)",
    "Layered composition: foreground, middle ground and background",
    "The scene fills the frame (not a small object in a void)",
    "Finished look, no glitches, black screen or broken geometry",
)


def _scene_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = read(ws, SCENE) or ""
    deterministic = [
        ("index.html exists with content", len(html) > 2000),
        ("imports three.js from a CDN", has(html, r"(cdn\.jsdelivr\.net|unpkg\.com|cdnjs\.cloudflare\.com)[^\"']*three")),
        ("creates a WebGLRenderer", "WebGLRenderer" in html),
        ("animation loop", has(html, r"requestAnimationFrame|setAnimationLoop")),
        ("low poly or voxel geometry in the code", has(html, r"BoxGeometry|InstancedMesh|flatShading")),
        ("no external models or textures", not has(html, r"\.(glb|gltf|obj|fbx|jpe?g|png|hdr)['\"]")),
    ]
    return visual.grade(ws, SCENE, deterministic, SCENE_CHECKLIST, MANDATORY_VISUAL, MIN_PNG_BYTES)


SCENE_REFERENCE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Fuji voxel</title>
<style>html,body{margin:0;height:100%;overflow:hidden;background:#f6c9a8}</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"}}</script>
</head><body><script type="module">
import * as THREE from "three";
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf4b183);
scene.fog = new THREE.Fog(0xf6c9a8, 140, 320);
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 500);
camera.position.set(0, 16, 58); camera.lookAt(0, 12, -20);
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(innerWidth, innerHeight); document.body.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xffe7d0, 0x6b8f71, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 1.4); sun.position.set(-30, 50, 20); scene.add(sun);
const mat = c => new THREE.MeshLambertMaterial({color: c, flatShading: true});
const box = new THREE.BoxGeometry(1, 1, 1);
function voxel(x, y, z, c, s = 1) { const m = new THREE.Mesh(box, mat(c)); m.position.set(x, y, z); m.scale.setScalar(s); scene.add(m); return m; }
// Fuji: stacked voxel rings, snow on top
for (let y = 0; y < 26; y++) {
  const r = 34 - y * 1.25;
  for (let a = 0; a < 360; a += 360 / Math.max(10, r * 3)) {
    const t = a * Math.PI / 180;
    voxel(Math.cos(t) * r, y * 1.2, -70 + Math.sin(t) * r * 0.5, y > 19 ? 0xffffff : (y > 16 ? 0xdfe6ee : 0x4d6b8a), 2.2);
  }
}
// ground and lake
const ground = new THREE.Mesh(new THREE.BoxGeometry(220, 1, 160), mat(0x5f8f4e)); ground.position.set(0, -0.5, -20); scene.add(ground);
const lake = new THREE.Mesh(new THREE.BoxGeometry(80, 0.2, 18), mat(0x4f7fb8)); lake.position.set(0, 0.2, -32); scene.add(lake);
// Chureito pagoda, five red tiers
for (let i = 0; i < 5; i++) {
  const w = 7 - i * 1.1;
  const body = voxel(-14, 6 + i * 3.1, 10, 0xc1272d); body.scale.set(w * 0.7, 2.2, w * 0.7);
  const roof = voxel(-14, 7.4 + i * 3.1, 10, 0x2b2b2b); roof.scale.set(w, 0.5, w);
}
voxel(-14, 23, 10, 0xd4a017).scale.set(0.4, 4, 0.4);
// cherry trees in the foreground
const trees = [];
for (let i = 0; i < 26; i++) {
  const x = -40 + (i * 37) % 80, z = 18 + (i * 13) % 20;
  voxel(x, 1.5, z, 0x6b4226).scale.set(0.8, 3, 0.8);
  const crown = voxel(x, 4.5, z, i % 3 ? 0xf7a8c4 : 0xf3c6d7, 4); trees.push(crown);
}
renderer.setAnimationLoop(t => {
  trees.forEach((c, i) => c.rotation.y = Math.sin(t / 1500 + i) * 0.08);
  camera.position.x = Math.sin(t / 9000) * 4;
  camera.lookAt(0, 12, -20);
  renderer.render(scene, camera);
});
addEventListener("resize", () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });
</script></body></html>
"""


def _ship(ws: Path, rel: str, html: str) -> list[str]:
    write(ws, rel, html)
    return ["done"]


TASKS = [
    EvalTask(
        id="web-mondrian-landing", category="web-design", needs=frozenset({"web"}),
        provenance="One-shot research + front-end: Piet Mondrian's Composition with Red, Blue and Yellow (1930)",
        summary="ONE-SHOT: research the painting and ship a Mondrian-style landing page; checks + vision checklist",
        setup=lambda ws: None, check=_landing_check,
        reference=lambda ws: _ship(ws, LANDING, LANDING_REFERENCE),
        timeout_s=900,
        steps=(Step("Research on the web Piet Mondrian's painting \"Composition with Red, Blue and Yellow\" (1930) and "
                    "the De Stijl movement. Create {WS}/landing/index.html: a single-file landing page (HTML + inline "
                    "CSS; Google Fonts allowed; no frameworks) telling its story, with art direction inspired by Piet "
                    "Mondrian (asymmetric grid of rectangles, thick black lines, red, blue, yellow and white). Include "
                    "a page title, a hero, sections with the key facts (the painter, the year, the movement and its "
                    "principles, why the work matters), a call-to-action button and a link to the source. "
                    + ONE_SHOT),),
    ),
    EvalTask(
        id="3d-voxel-landscape", category="3d",
        provenance="One-shot procedural 3D (Design Arena style): Mt. Fuji + Chureito pagoda + sakura in low poly/voxel",
        summary="ONE-SHOT: three.js voxel/low poly scene of Fuji with pagoda and cherry trees; checks + vision checklist",
        setup=lambda ws: None, check=_scene_check,
        reference=lambda ws: _ship(ws, SCENE, SCENE_REFERENCE),
        timeout_s=900,
        steps=(Step("Create {WS}/scene/index.html: a single-file 3D scene with three.js loaded from a CDN "
                    "(cdn.jsdelivr.net or unpkg.com), in low poly or voxel style, showing the classic view of Mount "
                    "Fuji with the Chureito pagoda (red, five tiers) and cherry trees in bloom in the foreground, with "
                    "an atmospheric sky (dusk or haze). All geometry must be procedural (no external models or "
                    "textures). The camera must frame the composition on load; include a subtle animation. "
                    + ONE_SHOT),),
    ),
]
