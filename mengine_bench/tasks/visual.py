"""One-shot visual artifact tasks: a landing page from a local fact sheet and a 3D scene.

One user request, no second turn: the agent must design and ship a complete
single-file page. The run grades deterministic content gates only (file,
facts, source link, palette, pinned three.js usage), so anyone reproduces the
grade without a browser (#23). The page is a deliverable: the bundle keeps it
verbatim and only the maintainer's `mengine-bench judge` renders it headless
for the rendered-look part of the Judge grade.
Ported from the private suite; the landing subject was replaced with a public
art-history topic that keeps the Mondrian visual brief.
"""

from __future__ import annotations

import html as html_lib
import re
import unicodedata
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, has, read, write

ONE_SHOT = ("This is your ONLY request: there will be no second turn and no answers to questions. "
            "Deliver the complete, working final file. Work only inside {WS}.")


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


# ------------------------------------------------------ web-mondrian-landing --

LANDING = "landing/index.html"
FACTSHEET = "FACTSHEET.md"
FACTSHEET_SOURCE = "https://en.wikipedia.org/wiki/Composition_with_Red,_Blue_and_Yellow"
# #23: a local fact sheet replaces web research, so every harness gets the same facts.
FACTSHEET_TEXT = f"""# Fact sheet: Composition with Red, Blue and Yellow

Source: {FACTSHEET_SOURCE}

- Title: Composition with Red, Blue and Yellow (also listed as Composition II in Red, Blue, and Yellow)
- Painter: Piet Mondrian (1872-1944), Dutch painter
- Year: 1930
- Medium: oil on canvas
- Collection: Kunsthaus Zurich
- Movement: De Stijl, founded in the Netherlands in 1917 by Theo van Doesburg and Piet Mondrian
- Principles (Neoplasticism): only horizontal and vertical lines, the three primary colours red, blue and
  yellow, and the non-colours white, grey and black
- The picture: a large red square at the top right, a small blue square at the bottom left and a small yellow
  rectangle at the bottom right, divided by thick black lines on a white ground
- Why it matters: its asymmetric balance of a few primary-colour blocks became a reference for modern graphic
  design and architecture
"""
# Agents may percent-encode the comma of the source URL.
SOURCE_LINK = r"href\s*=\s*[\"']https?://en\.wikipedia\.org/wiki/Composition_with_Red(,|%2C)_Blue_and_Yellow[\"'#]"


def _rendered_source(ws: Path, rel: str) -> str:
    """The page without HTML and CSS/JS block comments: commented-out content never renders (#23 review)."""
    text = read(ws, rel) or ""
    return re.sub(r"/\*.*?\*/", "", re.sub(r"<!--.*?-->", "", text, flags=re.S), flags=re.S)


def _visible_chars(html: str) -> int:
    # Padding with whitespace does not make a page.
    return len("".join(html.split()))


def _landing_setup(ws: Path) -> None:
    write(ws, FACTSHEET, FACTSHEET_TEXT)


def _landing_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = _rendered_source(ws, LANDING)
    plain = _plain(html)
    result = CheckResult(mandatory=[("index.html exists with content", _visible_chars(html) > 1500)])
    result.add("has a page title and an h1", has(html, r"<title>[^<]{3,}</title>") and has(html, r"<h1\b"))
    result.add("names the painting (Composition with Red, Blue and Yellow)",
               has(plain, r"composition\s+(ii\s+)?(with|in)\s+red,?\s+blue,?\s+and\s+yellow"))
    result.add("names the painter (Piet Mondrian)", "piet mondrian" in plain)
    result.add("states the year 1930", "1930" in plain)
    result.add("names the De Stijl movement", "de stijl" in plain)
    result.add("links to the fact sheet's source", has(html, SOURCE_LINK))
    result.add("CSS with the Mondrian palette (red, blue, yellow, black)", _mondrian_palette(html))
    result.add("has a call-to-action element", has(html, r"<button\b|<a\b[^>]*(class|role)=\"[^\"]*(cta|btn|button)"))
    return result


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
# #23: one pinned three.js build, so a run does not depend on what "latest" is that day.
THREE_URL = "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"


def _scene_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = _rendered_source(ws, SCENE)
    result = CheckResult(mandatory=[("index.html exists with content", _visible_chars(html) > 2000)])
    result.add("imports three.js 0.170.0 from the CDN",
               has(html, r"(cdn\.jsdelivr\.net/npm|unpkg\.com)/three@0\.170\.0/"))
    result.add("creates a WebGLRenderer", "WebGLRenderer" in html)
    result.add("animation loop", has(html, r"requestAnimationFrame|setAnimationLoop"))
    result.add("low poly or voxel geometry in the code", has(html, r"BoxGeometry|InstancedMesh|flatShading"))
    result.add("no external models or textures", not has(html, r"\.(glb|gltf|obj|fbx|jpe?g|png|hdr)['\"]"))
    return result


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
        id="web-mondrian-landing", category="web-design",
        provenance="One-shot front-end from a local fact sheet: Piet Mondrian's Composition with Red, Blue and "
                   "Yellow (1930)",
        summary="Build a Mondrian-style landing page about one painting from a local fact sheet, in one request.",
        setup=_landing_setup, check=_landing_check,
        reference=lambda ws: _ship(ws, LANDING, LANDING_REFERENCE),
        timeout_s=900, deliverables=(LANDING,),
        steps=(Step("Read {WS}/FACTSHEET.md: the facts about Piet Mondrian's painting \"Composition with Red, Blue "
                    "and Yellow\" (1930) and the De Stijl movement. Create {WS}/landing/index.html: a single-file "
                    "landing page (HTML + inline CSS; Google Fonts allowed; no frameworks) telling its story, with "
                    "art direction inspired by Piet Mondrian (asymmetric grid of rectangles, thick black lines, red, "
                    "blue, yellow and white). Include a page title, a hero, sections with the key facts (the "
                    "painter, the year, the movement and its principles, why the work matters), a call-to-action "
                    "button and a link to the source URL given in the fact sheet. " + ONE_SHOT),),
    ),
    EvalTask(
        id="3d-voxel-landscape", category="3d",
        provenance="One-shot procedural 3D (Design Arena style): Mt. Fuji + Chureito pagoda + sakura in low poly/voxel",
        summary="Build a three.js low poly or voxel scene of Mount Fuji with a pagoda and cherry trees, in one request.",
        setup=lambda ws: None, check=_scene_check,
        reference=lambda ws: _ship(ws, SCENE, SCENE_REFERENCE),
        timeout_s=900, deliverables=(SCENE,),
        steps=(Step("Create {WS}/scene/index.html: a single-file 3D scene with three.js 0.170.0 loaded from "
                    f"{THREE_URL} (an import map is fine), in low poly or voxel style, showing the classic view of "
                    "Mount Fuji with the Chureito pagoda (red, five tiers) and cherry trees in bloom in the "
                    "foreground, with an atmospheric sky (dusk or haze). All geometry must be procedural (no "
                    "external models or textures). The camera must frame the composition on load; include a "
                    "subtle animation. " + ONE_SHOT),),
    ),
]
