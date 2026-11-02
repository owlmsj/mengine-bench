"""One-shot visual artifact tasks: a landing page from a local fact sheet and a 3D homage to a print.

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

import colorsys
import html as html_lib
import json
import re
import unicodedata
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import (RESULT_FILE, WROTE_RESULT, CheckResult, EvalTask, Step, checkpoints, has, near, read,
                                result_json, saw, write)




def _plain(text: str) -> str:
    # Agents write accents and HTML entities (&eacute;); fold both before matching.
    # #28: inline markup inside a fact ("Piet <em>Mondrian</em>") is still the fact.
    text = html_lib.unescape(re.sub(r"<[^>]*>", "", text))
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()


def _hex_colors(html: str) -> list[tuple[int, int, int]]:
    colors = []
    for match in re.finditer(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", html):
        h = match.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        colors.append((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    # #59: rgb() and hsl() are colors too.
    for match in re.finditer(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})", html, flags=re.I):
        colors.append((int(match.group(1)), int(match.group(2)), int(match.group(3))))
    for match in re.finditer(r"hsla?\(\s*([\d.]+)(?:deg)?[\s,]+([\d.]+)%[\s,]+([\d.]+)%", html, flags=re.I):
        hue, saturation, lightness = (float(part) for part in match.groups())
        red, green, blue = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
        colors.append((round(red * 255), round(green * 255), round(blue * 255)))
    return colors


def _style_text(html: str) -> str:
    # #28: color words count only where they style something, not in prose like the painting's title.
    blocks = re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I)
    attributes = re.findall(r"\bstyle\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", html, flags=re.I)
    styles = " ".join([*blocks, *(double or single for double, single in attributes)]).lower()
    # #59: "Red Hat" and "Black Ops" are fonts.
    return re.sub(r"font(-family)?\s*:[^;}]*", "", styles)


def _mondrian_palette(html: str) -> bool:
    colors = _hex_colors(html)
    names = _style_text(html)
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
# Agents may percent-encode the comma of the source URL; #28: a trailing slash or query is the same page.
SOURCE_LINK = r"href\s*=\s*[\"']https?://en\.wikipedia\.org/wiki/Composition_with_Red(,|%2C)_Blue_and_Yellow[\"'#/?]"
# #28: single or double quotes around the class/role value.
# #28: a compact but complete page passes; the gate only rejects an empty or stub page.
LANDING_MIN_VISIBLE_CHARS = 300


def _rendered_source(ws: Path, rel: str) -> str:
    """The page without HTML and CSS/JS block comments: commented-out content never renders (#23 review)."""
    text = read(ws, rel) or ""
    return re.sub(r"/\*.*?\*/", "", re.sub(r"<!--.*?-->", "", text, flags=re.S), flags=re.S)


def _visible_chars(html: str) -> int:
    # Padding with whitespace does not make a page.
    return len("".join(html.split()))


PAGE_GATE = "index.html exists with content"


def _cut_short_page(html: str) -> tuple[str, ...]:
    # With no page at all, a check like "no external assets" would pass on nothing (#41).
    return (PAGE_GATE,) if html.strip() else ()


def _landing_setup(ws: Path) -> None:
    write(ws, FACTSHEET, FACTSHEET_TEXT)


def _landing_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = _rendered_source(ws, LANDING)
    plain = _plain(html)
    result = CheckResult(mandatory=[(PAGE_GATE, _visible_chars(html) > LANDING_MIN_VISIBLE_CHARS)],
                         waived_at_limit=_cut_short_page(html))
    result.add("has a page title and an h1", has(html, r"<title>[^<]{3,}</title>") and has(html, r"<h1\b"))
    result.add("names the painting (Composition with Red, Blue and Yellow)",
               has(plain, r"composition\s+(ii\s+)?(with|in)\s+red,?\s+blue,?\s+and\s+yellow"))
    result.add("names the painter (Piet Mondrian)", "piet mondrian" in plain)
    result.add("states the year 1930", "1930" in plain)
    result.add("names the De Stijl movement", "de stijl" in plain)
    result.add("links to the fact sheet's source", has(html, SOURCE_LINK))
    result.add("CSS with the Mondrian palette (red, blue, yellow, black)", _mondrian_palette(html))
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


# ---------------------------------------------------------- 3d-print-homage --

SCENE = "scene/index.html"
PRINT = "print.jpg"
# #124: Hokusai, The Great Wave off Kanagawa (c. 1831), public domain, from Wikimedia Commons
# (File:Tsunami_by_hokusai_19th_century.jpg, 1280 px, Metropolitan Museum of Art scan). A public-domain work so
# "copy this print" is a legitimate request: a refusal or a watered-down scene is the agent's, not the brief's.
PRINT_ASSET = Path(__file__).resolve().parents[1] / "assets" / "prints" / "great-wave.jpg"
PRINT_BOATS = 3
# #23: one pinned three.js build, so a run does not depend on what "latest" is that day.
THREE_PACKAGE_URL = "https://cdn.jsdelivr.net/npm/three@0.170.0/"
THREE_URL = THREE_PACKAGE_URL + "build/three.module.js"


def _print_setup(ws: Path) -> None:
    (ws / PRINT).write_bytes(PRINT_ASSET.read_bytes())


def _print_palette(html: str) -> tuple[bool, bool]:
    """The print's two signature colours: its deep Prussian blue and the cream of its paper (#124)."""
    # three.js code writes colours as 0x1f3a6b as often as "#1f3a6b".
    hex_literals = re.findall(r"\b0x([0-9a-fA-F]{6})\b", html)
    colors = _hex_colors(html) + [(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)) for h in hex_literals]
    deep_blue = any(b >= 90 and r <= 70 and g <= 120 and b - r >= 50 for r, g, b in colors)
    cream = any(r >= 200 and g >= 180 and b >= 130 and r - b >= 15 for r, g, b in colors)
    return deep_blue, cream


def _scene_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    html = _rendered_source(ws, SCENE)
    result = CheckResult(mandatory=[(PAGE_GATE, _visible_chars(html) > 2000)], waived_at_limit=_cut_short_page(html))
    # #28: only jsDelivr; the judge render resolves no other CDN, so unpkg would check but render blank.
    result.add("imports three.js 0.170.0 from the CDN", has(html, r"cdn\.jsdelivr\.net/npm/three@0\.170\.0/"))
    result.add("creates a WebGLRenderer", "WebGLRenderer" in html)
    result.add("animation loop", has(html, r"requestAnimationFrame|setAnimationLoop"))
    # #124: the print is a reference; loading it as a texture would be a photo of the print, not a homage.
    loaded = _loaded_external_assets(html)
    result.add("no external models or textures", not loaded, saw(loaded, []))
    deep_blue, cream = _print_palette(html)
    result.add("keeps the print's deep blue", deep_blue, saw(deep_blue, "a colour near #1f3a6b"))
    result.add("keeps the print's cream paper", cream, saw(cream, "a colour near #efe3c6"))
    got = result_json(ws)
    result.add("counted the boats in the print", near(got.get("boats"), PRINT_BOATS, 0), saw(got.get("boats"), PRINT_BOATS))
    result.add("named the mountain", has(str(got.get("mountain") or ""), r"fuji"), saw(got.get("mountain"), "Mount Fuji"))
    return result


# #28: a resource the page loads, not any string that ends in .png (a "fuji.png" download link is fine).
LOADED_RESOURCE = r"(?:\.load(?:Async)?\s*\(\s*|\bfetch\s*\(\s*|\bsrc\s*=\s*|\burl\(\s*)[\"'`]?([^\"'`)\s>]+)"
ASSET_FILE = r"\.(glb|gltf|obj|fbx|jpe?g|png|webp|hdr|exr|ktx2)([?#].*)?$"


# #28 review: the judge render resolves Google Fonts as well as the pinned three.js package.
ALLOWED_FONT_URLS = ("https://fonts.googleapis.com/", "https://fonts.gstatic.com/")


def _loaded_external_assets(html: str) -> list[str]:
    targets = re.findall(LOADED_RESOURCE, html, flags=re.I)
    remote = [t for t in targets if re.match(r"(https?:)?//", t, flags=re.I)
              and not t.startswith((THREE_PACKAGE_URL, *ALLOWED_FONT_URLS))]
    return remote + [t for t in targets if re.search(ASSET_FILE, t, flags=re.I)]


SCENE_REFERENCE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Great Wave homage</title>
<style>html,body{margin:0;height:100%;overflow:hidden;background:#efe3c6}</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"}}</script>
</head><body><script type="module">
import * as THREE from "three";
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xefe3c6);
scene.fog = new THREE.Fog(0xefe3c6, 90, 220);
const camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.1, 400);
camera.position.set(0, 9, 60); camera.lookAt(0, 8, 0);
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(innerWidth, innerHeight); document.body.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xfff6e0, 0x1f3a6b, 1.2));
const sun = new THREE.DirectionalLight(0xffffff, 1.2); sun.position.set(-20, 40, 30); scene.add(sun);
const mat = c => new THREE.MeshLambertMaterial({color: c, flatShading: true});
// Mount Fuji, small and far, between the waves
const fuji = new THREE.Mesh(new THREE.ConeGeometry(9, 7, 7), mat(0x2b4c7e)); fuji.position.set(6, 3.5, -40); scene.add(fuji);
const snow = new THREE.Mesh(new THREE.ConeGeometry(3.6, 2.8, 7), mat(0xffffff)); snow.position.set(6, 5.6, -40); scene.add(snow);
// The great wave: a curling crest of tilted cones, deep blue with white foam claws
const crest = new THREE.Group(); scene.add(crest);
for (let i = 0; i < 40; i++) {
  const t = i / 39, angle = t * Math.PI * 1.15;
  const seg = new THREE.Mesh(new THREE.ConeGeometry(3.4 - t * 2.2, 6, 6), mat(i % 3 ? 0x1f3a6b : 0x3f6e9e));
  seg.position.set(-24 + Math.sin(angle) * 14, 2 + (1 - Math.cos(angle)) * 11, -6);
  seg.rotation.z = -angle; crest.add(seg);
  const foam = new THREE.Mesh(new THREE.IcosahedronGeometry(0.9 + (i % 4) * 0.2, 0), mat(0xf7f3ea));
  foam.position.copy(seg.position).add(new THREE.Vector3(1.6, 2.2, 0.8)); crest.add(foam);
}
// Rolling swells in front
const swells = [];
for (let i = 0; i < 9; i++) {
  const swell = new THREE.Mesh(new THREE.ConeGeometry(7, 7 + (i % 3) * 2, 6), mat(i % 2 ? 0x1f3a6b : 0x6f9cc4));
  swell.position.set(-34 + i * 9, 1, 10 + (i % 2) * 6); scene.add(swell); swells.push(swell);
}
// Three long boats with their rowers
const boats = [];
for (const [x, z, r] of [[-12, 4, 0.3], [14, -8, -0.25], [4, 18, 0.15]]) {
  const boat = new THREE.Group();
  const hull = new THREE.Mesh(new THREE.BoxGeometry(16, 0.8, 2.2), mat(0xe8c9a0)); boat.add(hull);
  for (let k = 0; k < 7; k++) {
    const rower = new THREE.Mesh(new THREE.SphereGeometry(0.45, 6, 4), mat(0x2a2a3a)); rower.position.set(-5 + k * 1.7, 0.8, 0); boat.add(rower);
  }
  boat.position.set(x, 2.5, z); boat.rotation.z = r; scene.add(boat); boats.push(boat);
}
renderer.setAnimationLoop(t => {
  swells.forEach((s, i) => s.position.y = 1 + Math.sin(t / 900 + i) * 0.6);
  boats.forEach((b, i) => b.position.y = 2.5 + Math.sin(t / 700 + i * 2) * 0.8);
  crest.rotation.z = Math.sin(t / 2500) * 0.03;
  renderer.render(scene, camera);
});
addEventListener("resize", () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });
</script></body></html>
"""


def _scene_reference(ws: Path) -> list[str]:
    write(ws, RESULT_FILE, json.dumps({"boats": PRINT_BOATS, "mountain": "Mount Fuji"}))
    return _ship(ws, SCENE, SCENE_REFERENCE)


def _ship(ws: Path, rel: str, html: str) -> list[str]:
    write(ws, rel, html)
    return ["done"]


# The judge's sandbox reaches these and nothing else, so saying it is a fact about the world, not a method (#28, #98).
LOOK = ("It is reviewed by opening the file, with no build step, in a browser that reaches only Google Fonts and "
        f"{THREE_URL}.")
OPENED = ("looked at it in a browser", r"browser|screenshot|headless|playwright|cua\.|chrome|msedge")

TASKS = [
    EvalTask(
        id="web-mondrian-landing", category="web-design",
        provenance="One-shot front-end from a local fact sheet: Piet Mondrian's Composition with Red, Blue and "
                   "Yellow (1930)",
        summary="Build a landing page that tells the story of one Mondrian painting from a fact sheet.",
        setup=_landing_setup, check=_landing_check,
        reference=lambda ws: _ship(ws, LANDING, LANDING_REFERENCE),
        timeout_s=300, deliverables=(LANDING,),
        checkpoints=checkpoints(("read the fact sheet", r"FACTSHEET"), ("wrote the page", r"landing.{1,4}index\.html"), OPENED),
        steps=(Step("We need a landing page, {WS}/landing/index.html in a single file, for the story of Piet Mondrian's "
                    "\"Composition with Red, Blue and Yellow\" (1930). The facts are in {WS}/FACTSHEET.md, and nothing beyond "
                    "them should be claimed. A visitor should leave knowing the painter, the year, the movement and why the "
                    "work matters, and be invited to read more at the source the fact sheet gives. The page itself should "
                    "speak Mondrian's visual language. " + LOOK),),
    ),
    EvalTask(
        id="3d-print-homage", category="3d", needs=frozenset({"vision"}),
        provenance="One-shot procedural 3D from a reference image (#124): a homage to Hokusai's Great Wave, public domain",
        summary="Turn a famous public-domain woodblock print into a 3D wallpaper that anyone who knows the print recognizes.",
        setup=_print_setup, check=_scene_check, reference=_scene_reference,
        timeout_s=420, deliverables=(SCENE,),
        checkpoints=checkpoints(("wrote the scene", r"scene.{1,4}index\.html"), OPENED, WROTE_RESULT),
        steps=(Step("A client loves the woodblock print attached, also in {WS}/print.jpg; it is in the public domain. They "
                    "want a 3D wallpaper that copies it: its composition, its palette and its subjects, so anyone who knows "
                    "the print recognizes it at a glance, rebuilt as our own low poly scene with some gentle motion. Deliver "
                    "{WS}/scene/index.html, a single file with everything built in code: the print is the reference, not a "
                    "texture. Record in {WS}/result.json what you took from it: boats (how many the print shows) and mountain "
                    "(its name). " + LOOK, attach=(PRINT,)),),
    ),
]
