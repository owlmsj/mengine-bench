"""Word universe (#99): collect a saved dictionary site, then sum it up in one searchable view.

From a challenge once used to evaluate engineers. The site is generated from THEMES with a fixed seed, so the gold
is the site itself, and the reference reads it from the pages alone. The page's look is the judge's part; Correct
only asks whether the data is right and whether search and ?word= work.
"""

from __future__ import annotations

import json
import random
import re
import unicodedata
from collections import Counter
from collections.abc import Sequence
from html import unescape
from pathlib import Path
from urllib.parse import quote, unquote

from mengine_bench.core import CheckResult, EvalTask, Step, WROTE_RESULT, checkpoints, has, near, read_json, result_json, saw, write
from mengine_bench.tasks.visual import LOOK, OPENED, _plain, _rendered_source
from mengine_bench.visual import RENDERED, dump_page_dom

SITE = "site"
PAGE = "universe/index.html"
WORDS_FILE = "words.json"
SITE_SEED = 9917

# Neighbours in a list read as near-synonyms: the site lists them as such.
THEMES = {
    "sentimentos": "saudade nostalgia melancolia tristeza mágoa dor angústia aflição ansiedade medo pavor susto espanto "
                   "surpresa alegria felicidade contentamento prazer paixão amor afeto carinho ternura compaixão esperança",
    "família": "família parentesco pais mãe pai filho filha irmão irmã avô avó neto neta tio tia primo prima sobrinho "
               "cunhado sogra genro nora padrinho madrinha herança",
    "natureza": "natureza floresta mata selva árvore raiz folha flor pétala semente fruto jardim campo prado montanha "
                "serra vale rio riacho cachoeira lago mar onda praia areia",
    "tempo": "tempo hora minuto segundo instante momento época era século ano mês semana dia manhã tarde noite madrugada "
             "aurora crepúsculo ontem hoje amanhã eternidade passado futuro",
    "corpo": "corpo cabeça rosto olho boca língua dente pescoço ombro braço mão dedo unha peito coração pulmão estômago "
             "fígado pele osso sangue perna joelho pé alma",
    "lugares": "país nação pátria estado cidade capital vila aldeia bairro rua avenida praça esquina ponte porto estação "
               "mercado igreja escola casa lar quarto cozinha janela porta",
    "comida": "comida refeição almoço jantar pão farinha trigo arroz feijão milho mandioca carne peixe ovo queijo leite "
              "manteiga açúcar mel sal pimenta café chá vinho água",
    "ofícios": "trabalho ofício profissão emprego salário patrão operário pedreiro carpinteiro ferreiro sapateiro alfaiate "
               "padeiro açougueiro pescador lavrador pastor médico enfermeira professor advogado juiz soldado marinheiro engenheiro",
    "artes": "arte música canção melodia ritmo samba violão piano tambor dança teatro cena ator poesia verso rima romance "
             "conto livro pintura tela desenho escultura cinema fotografia",
    "linguagem": "palavra idioma linguagem frase sentido significado dicionário sinônimo gíria sotaque voz fala conversa "
                 "silêncio grito sussurro nome apelido letra sílaba acento pergunta resposta história memória",
}
WORD_THEMES = {word: theme for theme, words in THEMES.items() for word in words.split()}
WORDS = list(WORD_THEMES)
# Every relation link to these goes through a redirect page: the variant is the same word.
VARIANTS = {"saudade": "saudades", "coração": "corações", "paixão": "paixões"}
# Links to pages that were never saved; the site's own leftovers, not words.
BROKEN = ("rascunho-3", "pagina-removida", "link-antigo", "xpto-2", "em-construção")
FOOTER_WORDS = ("amor", "casa", "mar", "café")
# Two words tie for the most connected by construction: a tie must not cost anyone a point.
HUBS = ("palavra", "tempo")
HUB_LINKS = 14
NON_WORD_PAGES = {"sobre.html": "Sobre", "contato.html": "Contato"}


def _file_names() -> dict[str, str]:
    """Accents and capitals vary, as on a site saved over the years; only an accent tells pais from país."""
    folded = Counter(_plain(word) for word in WORDS)
    names = {}
    for index, word in enumerate(WORDS):
        plain = _plain(word)
        keeps_accent = folded[plain] > 1 and word != plain
        names[word] = word if keeps_accent or index % 5 == 0 else plain.capitalize() if index % 5 == 1 else plain
    return {word: f"{name}.html" for word, name in names.items()}


FILES = _file_names()


def _listed() -> dict[str, tuple[list[str], list[str]]]:
    """What each word's page lists: (synonyms, analogous). An analogous link may show on one of its two pages only."""
    rng = random.Random(SITE_SEED)
    synonyms: dict[str, list[str]] = {}
    analogous: dict[str, list[str]] = {word: [] for word in WORDS}

    def link(word: str, other: str) -> None:
        analogous[word].append(other)
        if rng.random() < 0.7:
            analogous[other].append(word)

    plain_words = [word for word in WORDS if word not in HUBS]
    for words in map(str.split, THEMES.values()):
        for index, word in enumerate(words):
            synonyms[word] = [words[index - 1], words[(index + 1) % len(words)]]
        for word in words:
            if word in HUBS:
                continue
            same_theme = [other for other in words if other != word and other not in HUBS]
            for other in (rng.choice(same_theme), rng.choice(plain_words)):
                if other != word:
                    link(word, other)
    for hub in HUBS:
        theme = next(words.split() for words in THEMES.values() if hub in words.split())
        for other in rng.sample([word for word in plain_words if word not in theme], HUB_LINKS):
            link(hub, other)
    return {word: (synonyms[word], list(dict.fromkeys(analogous[word]))) for word in WORDS}


def _relations() -> dict[str, set[str]]:
    links: dict[str, set[str]] = {word: set() for word in WORDS}
    for word, lists in _listed().items():
        for other in (*lists[0], *lists[1]):
            links[word].add(other)
            links[other].add(word)
    return links


def _pairs(links: dict[str, set[str]]) -> set[frozenset[str]]:
    return {frozenset((word, other)) for word, others in links.items() for other in others}


def _day_words(word: str) -> list[str]:
    return random.Random(f"{SITE_SEED}:{word}").sample(WORDS, 4)


def _noise_pairs() -> set[frozenset[str]]:
    """Pairs that only share a page through its sidebar or footer."""
    pairs = {frozenset((word, other)) for word in WORDS for other in (*_day_words(word), *FOOTER_WORDS) if other != word}
    return pairs - _pairs(_relations())


def _plain_anchor(word: str) -> str:
    return f'<a href="{quote(FILES[word])}">{word}</a>'


def _relation_anchor(word: str, rng: random.Random) -> str:
    variant = VARIANTS.get(word)
    if variant:
        return f'<a href="{_plain(variant)}.html">{variant}</a>'
    return f'<a href="{quote(FILES[word])}">{rng.choice((word, word.capitalize(), word.upper(), _plain(word)))}</a>'


def _items(anchors: Sequence[str]) -> str:
    return "<ul>" + "".join(f"<li>{anchor}</li>" for anchor in anchors) + "</ul>"


def _site_page(title: str, main: str, day_words: Sequence[str]) -> str:
    footer = " ".join(map(_plain_anchor, FOOTER_WORDS))
    others = " ".join(f'<a href="{name}">{label}</a>' for name, label in NON_WORD_PAGES.items())
    return (f'<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8"><title>{title} | Dicionário Criativo</title></head><body>\n'
            f'<header><a href="index.html">Dicionário Criativo</a></header>\n'
            f'<aside><h2>Palavras do dia</h2>{_items([_plain_anchor(word) for word in day_words])}</aside>\n'
            f"<main>{main}</main>\n"
            f"<footer><p>Mais buscadas: {footer}</p><p>{others}</p></footer>\n</body></html>\n")


def _word_page(word: str, theme: str, lists: tuple[list[str], list[str]], extra: str, rng: random.Random) -> str:
    synonyms = _items([_relation_anchor(other, rng) for other in lists[0]])
    analogous = _items([*(_relation_anchor(other, rng) for other in lists[1]), *([extra] if extra else [])])
    return _site_page(word, f'<h1>{word}</h1><p class="tema">Tema: {theme}</p>\n'
                            f'<section id="sinonimos"><h2>Sinônimos</h2>{synonyms}</section>\n'
                            f'<section id="analogas"><h2>Palavras análogas</h2>{analogous}</section>', _day_words(word))


def _redirect_page(variant: str, word: str) -> str:
    return (f'<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8"><title>{variant}</title>'
            f'<meta http-equiv="refresh" content="0; url={quote(FILES[word])}"></head>\n'
            f"<body><p>Redirecionando para {_plain_anchor(word)}.</p></body></html>\n")


def _word_setup(ws: Path) -> None:
    rng = random.Random(SITE_SEED + 1)
    listed = _listed()
    for index, word in enumerate(WORDS):
        leftover = BROKEN[index // 40 % len(BROKEN)]
        extra = f'<a href="{_plain(leftover)}.html">{leftover}</a>' if index % 40 == 0 else ""
        write(ws, f"{SITE}/{FILES[word]}", _word_page(word, WORD_THEMES[word], listed[word], extra, rng))
    for word, variant in VARIANTS.items():
        write(ws, f"{SITE}/{_plain(variant)}.html", _redirect_page(variant, word))
    for name, label in NON_WORD_PAGES.items():
        write(ws, f"{SITE}/{name}", _site_page(label, f"<h1>{label}</h1><p>Um dicionário criativo feito por quem gosta de palavras.</p>", WORDS[:4]))
    # The home page shows a part; the rest is only reached by following the links.
    highlights = [word for words in THEMES.values() for word in words.split()[:3]]
    home = "<h1>Dicionário Criativo</h1><h2>Destaques</h2>" + _items([_relation_anchor(word, rng) for word in highlights])
    write(ws, f"{SITE}/index.html", _site_page("Início", home, WORDS[4:8]))


# ------------------------------------------------------------------ checks ----

# The brief fixes the facts, not the shape: an entry may be a list, {"synonyms": [...], "analogous": [...]},
# rows with a name, or {other word: kind}.
NAME_KEYS = ("word", "name", "to", "target", "id")
# Notes an agent may keep beside the links, such as the variants it merged: not relations.
NOT_RELATIONS = r"alias|variant|redirect|source|url|theme|tema|tag"
RELATION_SAMPLE = ("saudade", "nostalgia", "coração", "pais", "país", "avó", "avô", "tempo")
# Two words and, for each, a word far from it that a broken view would show. país must not get the relations of pais.
QUERY_DECOYS = {"saudade": "alfaiate", "país": "mãe"}
QUERY_READ = r"URLSearchParams|location\b|document\.URL"
QUERY_CHECK = "opening the page with ?word= shows that word's relations"


def _word_key(text: object) -> str:
    return " ".join(unicodedata.normalize("NFC", str(text)).casefold().split())


def _row_name(row: dict[str, object]) -> str:
    return next((_word_key(row[key]) for key in NAME_KEYS if isinstance(row.get(key), str)), "")


def _linked_words(value: object) -> set[str]:
    if isinstance(value, str):
        return {_word_key(value)}
    if isinstance(value, list):
        return {word for item in value for word in _linked_words(item)}
    if not isinstance(value, dict):
        return set()
    nested = [item for key, item in value.items() if isinstance(item, (list, dict)) and not re.search(NOT_RELATIONS, str(key), re.I)]
    if nested:
        return _linked_words(nested)
    name = _row_name(value)
    return {name} if name else set(map(_word_key, value))


def _delivered_links(got: object) -> dict[str, set[str]]:
    """Every word and its links, both ways: a link written on one side still links both words."""
    if isinstance(got, dict) and isinstance(got.get("words"), (dict, list)):
        got = got["words"]
    if isinstance(got, list):
        got = {_row_name(row): row for row in got if isinstance(row, dict)}
    if not isinstance(got, dict):
        return {}
    links: dict[str, set[str]] = {}
    for name, value in got.items():
        word = _word_key(name)
        if not word:
            continue
        links.setdefault(word, set())
        for other in _linked_words(value) - {word}:
            links[word].add(other)
            links.setdefault(other, set()).add(word)
    return links


def _few(words: set[str]) -> str:
    return ", ".join(sorted(words)[:5]) or "none"


def _set_detail(got: set[str], want: set[str]) -> str:
    return f"missing {len(want - got)} ({_few(want - got)}), extra {len(got - want)} ({_few(got - want)})"


def _most_connected_ok(value: object, tied: set[str]) -> bool:
    rows = value if isinstance(value, list) else [value]
    names = {_word_key(row) if isinstance(row, str) else _row_name(row) if isinstance(row, dict) else "" for row in rows}
    return bool(names) and names <= tied


def _visible_markup(dom: str) -> str:
    return re.sub(r"<(script|style)\b.*?</\1>", " ", dom, flags=re.S | re.I)


def _shown_words(dom: str) -> set[str]:
    """The words a reader gets from the DOM: its text, and the names a canvas or a chart gives through attributes."""
    markup = _visible_markup(dom)
    exposed = re.findall(r"\b(?:aria-label|title|alt)=\"([^\"]*)\"", markup)
    text = re.sub(r"<[^>]+>", " ", markup)
    return set(re.findall(r"\w+", _word_key(unescape(" ".join((text, *exposed))))))


def _query_problem(doms: dict[str, str], links: dict[str, set[str]]) -> str:
    """Why ?word= failed, or "" if it works. Fair to any view, so a page is only compared with itself:

    - What shows under both words is the page itself (a legend, a full list, every node of a chart), so only what the
      query put on screen can be a wrong relation.
    - All the relations in the DOM count once the DOM changes with the word: a panel, or a chart that highlights.
    - A canvas has no text to read. It passes when the page reads the query and no relation reached the DOM text; a
      text panel that shows only some of them is not this case. The judge looks at the screen.
    """
    (first, first_dom), (second, second_dom) = doms.items()
    shown = {first: _shown_words(first_dom), second: _shown_words(second_dom)}
    reacted = _visible_markup(first_dom) != _visible_markup(second_dom)
    for word, other in ((first, second), (second, first)):
        own = shown[word] - shown[other]
        if QUERY_DECOYS[word] in own:
            return f"?word={word} shows {QUERY_DECOYS[word]}, which has no link with it"
        missing = links[word] - shown[word]
        if not missing and reacted:
            continue
        if "<canvas" in doms[word].lower() and re.search(QUERY_READ, doms[word]) and not own & links[word]:
            continue
        if not missing:
            return "the page is the same for any ?word="
        return f"?word={word} does not show its {len(links[word])} relations, missing {_few(missing)}"
    return ""


def _add_query_check(result: CheckResult, page: Path, links: dict[str, set[str]]) -> None:
    if not page.is_file():
        result.add(QUERY_CHECK, False, f"no {PAGE}")
        return
    doms = {}
    for word in QUERY_DECOYS:
        status, doms[word] = dump_page_dom(page, f"word={quote(word)}")
        if status != RENDERED:
            result.notes.append(f"?word= not run: {status}")
            return
    problem = _query_problem(doms, links)
    result.add(QUERY_CHECK, not problem, problem)


def _universe_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    want = _relations()
    got = _delivered_links(read_json(ws, WORDS_FILE))
    result.add("collected exactly the site's words", set(got) == set(want), _set_detail(set(got), set(want)))
    wrong = [word for word in RELATION_SAMPLE if got.get(word) != want[word]]
    result.add("relations of a sample of words", not wrong,
               f"{wrong[0]}: {_set_detail(got.get(wrong[0], set()), want[wrong[0]])}" if wrong else "")
    false_pairs = _pairs(got) & _noise_pairs()
    examples = [" - ".join(sorted(pair)) for pair in sorted(false_pairs, key=sorted)[:3]]
    result.add("no relation from a sidebar or a footer", bool(got) and not false_pairs,
               f"{len(false_pairs)} false pairs, such as {examples}" if got else f"no {WORDS_FILE}")
    summary = result_json(ws)
    degree = max(map(len, want.values()))
    tied = {word for word, others in want.items() if len(others) == degree}
    expected = {"words": len(want), "relations": len(_pairs(want)), "most_connected": sorted(tied)}
    result.add("result.json has the right words, relations and most_connected",
               near(summary.get("words"), len(want), 0) and near(summary.get("relations"), len(_pairs(want)), 0)
               and _most_connected_ok(summary.get("most_connected"), tied), saw(summary, expected))
    html = _rendered_source(ws, PAGE)
    result.add("the page has a search field", has(html, r"<input\b|<textarea\b|contenteditable|role\s*=\s*[\"']?searchbox|createElement\(\s*[\"'`]input"),
               f"no input, contenteditable or searchbox in {PAGE}")
    _add_query_check(result, ws / PAGE, want)
    return result


# --------------------------------------------------------------- reference ----


def _open_site_page(site: Path, href: str) -> tuple[str, str] | None:
    """The page a link ends at, after any redirect: (file, html), or None for a broken link."""
    path = site / unquote(href)
    if not path.is_file():
        return None
    html = path.read_text(encoding="utf-8")
    moved = re.search(r'url=([^"]+)"', html)
    return _open_site_page(site, moved.group(1)) if moved else (path.name, html)


def _crawl(site: Path) -> dict[str, list[str]]:
    def main_links(html: str) -> list[str]:
        return re.findall(r'href="([^"]+)"', html.split("<main>")[1].split("</main>")[0])

    pages: dict[str, tuple[str, list[str]]] = {}
    todo = main_links((site / "index.html").read_text(encoding="utf-8"))
    while todo:
        opened = _open_site_page(site, todo.pop())
        if opened is None or opened[0] in pages:
            continue
        hrefs = main_links(opened[1])
        pages[opened[0]] = (re.search(r"<h1>(.*?)</h1>", opened[1]).group(1), hrefs)
        todo += hrefs
    links: dict[str, set[str]] = {word: set() for word, _ in pages.values()}
    for word, hrefs in pages.values():
        targets = [_open_site_page(site, href) for href in hrefs]
        for other in (pages[target[0]][0] for target in targets if target):
            links[word].add(other)
            links[other].add(word)
    return {word: sorted(others) for word, others in links.items()}


REFERENCE_PAGE = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Universo de palavras</title>
<style>
body{margin:0;display:flex;gap:24px;font:16px system-ui,sans-serif;background:#10141c;color:#e8e6df}
aside{padding:24px;width:340px}input{width:100%;padding:8px;font-size:16px;box-sizing:border-box}a{color:#ffc857}
</style></head><body>
<canvas id="map" width="860" height="860" role="img" aria-label="Todas as palavras num anel, ligadas por linhas"></canvas>
<aside><h1>Universo de palavras</h1><p id="total"></p>
<input id="search" type="search" placeholder="Procure uma palavra" aria-label="Procure uma palavra">
<h2 id="focus"></h2><ul id="related"></ul></aside>
<script>
const LINKS = __LINKS__;
const WORDS = Object.keys(LINKS);
const at = {};
WORDS.forEach((word, i) => { const a = 2 * Math.PI * i / WORDS.length; at[word] = [430 + 400 * Math.cos(a), 430 + 400 * Math.sin(a)]; });
const pen = document.getElementById("map").getContext("2d");
function line(from, to, color) {
  pen.strokeStyle = color; pen.beginPath(); pen.moveTo(...at[from]); pen.lineTo(...at[to]); pen.stroke();
}
function show(word) {
  pen.clearRect(0, 0, 860, 860);
  WORDS.forEach(from => LINKS[from].forEach(to => line(from, to, "#5b6b8c55")));
  const related = LINKS[word] || [];
  related.forEach(to => line(word, to, "#ffc857"));
  pen.fillStyle = "#e8e6df";
  [word, ...related].filter(name => at[name]).forEach(name => pen.fillText(name, ...at[name]));
  document.getElementById("focus").textContent = LINKS[word] ? word : "";
  document.getElementById("related").innerHTML = related.map(to => `<li><a href="?word=${encodeURIComponent(to)}">${to}</a></li>`).join("");
}
document.getElementById("total").textContent = `${WORDS.length} palavras`;
document.getElementById("search").addEventListener("input", event => show(event.target.value.trim().toLowerCase()));
show(new URLSearchParams(location.search).get("word") || "");
</script></body></html>
"""


def _word_reference(ws: Path) -> list[str]:
    links = _crawl(ws / SITE)
    degree = max(map(len, links.values()))
    write(ws, WORDS_FILE, json.dumps(links, ensure_ascii=False))
    write(ws, "result.json", json.dumps({"words": len(links), "relations": sum(map(len, links.values())) // 2,
                                         "most_connected": next(word for word, others in links.items() if len(others) == degree)},
                                        ensure_ascii=False))
    write(ws, PAGE, REFERENCE_PAGE.replace("__LINKS__", json.dumps(links, ensure_ascii=False)))
    return ["done"]


TASKS = [
    EvalTask(
        id="web-word-universe", category="data-viz",
        provenance="Challenge once used to evaluate engineers: explore a universe of words and sum it up in one "
                   "searchable view, from a saved Portuguese creative dictionary",
        summary="Collect a saved Portuguese dictionary site and build one view that shows how its words relate.",
        setup=_word_setup, check=_universe_check, reference=_word_reference,
        timeout_s=360, deliverables=(PAGE,),
        checkpoints=checkpoints(("walked the site", r"\bsite[/\\]|[/\\]site\b"), ("wrote words.json", r"words\.json"),
                                ("wrote the page", r"universe.{1,4}index\.html"), OPENED, WROTE_RESULT),
        steps=(Step("Words are tied to each other, and nobody here can see how. {WS}/site is a saved copy of a Portuguese "
                    "creative dictionary. Explore this universe of words: collect what the site knows and build "
                    "{WS}/universe/index.html, a single file that sums the universe up in one view and lets someone search "
                    "for a word and find how it relates to others. The best way to show it is your call, and that view is "
                    "what we care about most. So people can share a word, opening the page with ?word=saudade must show "
                    "that word and its relations. Save the data as {WS}/words.json, mapping each word to the words it is "
                    "linked to, and record in {WS}/result.json: words (how many), relations (how many distinct pairs) and "
                    "most_connected. " + LOOK),),
    ),
]
