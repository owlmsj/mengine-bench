"""Basic file editing: a feed photo and a flattened PDF form (#153).

Two everyday edits any route can do (an image tool, a PDF tool, a script): crop a landscape photo to a 1080x1350
portrait JPEG without losing or squashing its subject, and fill a park permit's form fields and flatten them. The
photo and the form are drawn here, offline; Pillow and pypdf read the results back (grader dependencies, #153).
"""

from __future__ import annotations

import hashlib
import io
import re
import zlib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, saw, write

MEDIA_PHOTO = "launch.jpg"
MEDIA_FORM = "permit-form.pdf"
MEDIA_DETAILS = "event-details.txt"
MEDIA_PHOTO_OUT = "out/feed-photo.jpg"
MEDIA_FORM_OUT = "out/permit-filled.pdf"
MEDIA_FEED_SIZE = (1080, 1350)
MEDIA_PHOTO_SIZE = (3000, 2000)
# The subject: a magenta balloon right of centre, so a centre crop loses it.
MEDIA_BALLOON_CENTER = (2550, 700)
MEDIA_BALLOON_RADIUS = 200
MEDIA_BALLOON_RGB = (225, 30, 190)
MEDIA_ORIGINALS_GATE = "the original photo and form left as they were"
MEDIA_MIN_BALLOON_PX = 40
MEDIA_ROUND_RATIO = (0.85, 1.18)  # bbox width / height of a disc that kept its shape
MEDIA_DISC_FILL = (0.66, 0.90)  # pixels / bbox area; a full disc is pi/4


@dataclass(frozen=True)
class MediaField:
    name: str
    label: str
    value: str
    rect: tuple[float, float, float, float]  # x1, y1, x2, y2 in PDF points


MEDIA_FIELDS: tuple[MediaField, ...] = (
    MediaField("organizer", "Organizer", "Tidewater Studio", (200, 640, 520, 664)),
    MediaField("event_date", "Event date (YYYY-MM-DD)", "2026-12-05", (200, 600, 520, 624)),
    MediaField("location", "Location in the park", "North Cove Lawn", (200, 560, 520, 584)),
    MediaField("attendees", "Expected attendees", "40", (200, 520, 520, 544)),
)

MEDIA_DETAILS_TEXT = """From: Ines Varga
Subject: balloon launch permit

Details for the park permit:

Organizer: Tidewater Studio
Date: Saturday 5 December 2026
Where: North Cove Lawn
People: about 40
"""

MEDIA_PROMPT = f"""Tidewater Studio is announcing its balloon launch. Two small jobs before the post goes out:

1. `{MEDIA_PHOTO}` becomes the feed picture: a 1080x1350 JPEG at `{MEDIA_PHOTO_OUT}`. The magenta balloon is the
   subject, so it has to be fully in the picture and still look like itself.
2. The park's permit form `{MEDIA_FORM}` filled in with the details Ines sent in `{MEDIA_DETAILS}`, saved at
   `{MEDIA_FORM_OUT}` and flattened, so the answers can no longer be edited.

Keep the originals as they are."""


# ----------------------------------------------------------------- fixture ----


def media_photo_jpeg() -> bytes:
    """A launch field at dawn: sky, hills, a tent and the magenta balloon with its basket."""
    from PIL import Image, ImageDraw

    width, height = MEDIA_PHOTO_SIZE
    image = Image.new("RGB", MEDIA_PHOTO_SIZE)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / height
        draw.line([(0, y), (width, y)], fill=(int(120 + 100 * t), int(170 + 50 * t), int(235 - 20 * t)))
    draw.polygon([(0, 1400), (700, 1150), (1500, 1350), (2300, 1100), (3000, 1300), (3000, 2000), (0, 2000)], fill=(86, 140, 70))
    draw.polygon([(0, 1650), (1200, 1500), (3000, 1700), (3000, 2000), (0, 2000)], fill=(64, 112, 52))
    draw.polygon([(600, 1550), (800, 1350), (1000, 1550)], fill=(240, 236, 220))
    draw.ellipse([(1300, 300), (1500, 360)], fill=(245, 245, 250))
    cx, cy = MEDIA_BALLOON_CENTER
    r = MEDIA_BALLOON_RADIUS
    for dx in (-60, 60):
        draw.line([(cx + dx, cy + r - 40), (cx + dx // 2, cy + r + 110)], fill=(90, 70, 60), width=4)
    draw.rectangle([(cx - 40, cy + r + 110), (cx + 40, cy + r + 170)], fill=(120, 80, 45))
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=MEDIA_BALLOON_RGB)
    out = io.BytesIO()
    image.save(out, "JPEG", quality=90)
    return out.getvalue()


def _media_pdf_text(x: float, y: float, size: int, text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return f"BT /Helv {size} Tf {x} {y} Td ({escaped}) Tj ET"


def media_form_pdf() -> bytes:
    """A one-page AcroForm with four empty text fields, like a council's fillable PDF."""
    page_ops = [_media_pdf_text(56, 760, 18, "Port Wrenfield Parks - Event Permit Application"),
                _media_pdf_text(56, 735, 10, "Fill in every field. Applications are reviewed within 10 working days.")]
    for field in MEDIA_FIELDS:
        page_ops.append(_media_pdf_text(56, field.rect[1] + 7, 11, field.label))
    page_ops.append(_media_pdf_text(56, 480, 9, "Port Wrenfield Parks Department, 2 Harbour Row. Form EP-3."))
    content = zlib.compress("\n".join(page_ops).encode("latin-1"))
    font = 4
    objects: dict[int, bytes] = {
        1: b"<< /Type /Catalog /Pages 2 0 R /AcroForm 5 0 R >>",
        2: b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        font: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        6: b"<< /Length " + str(len(content)).encode() + b" /Filter /FlateDecode >>\nstream\n" + content + b"\nendstream",
    }
    widgets = []
    for index, field in enumerate(MEDIA_FIELDS):
        widget, appearance = 7 + 2 * index, 8 + 2 * index
        x1, y1, x2, y2 = field.rect
        box = f"0.95 0.95 1 rg 0 0 {x2 - x1} {y2 - y1} re f".encode()
        objects[appearance] = (b"<< /Type /XObject /Subtype /Form /BBox [0 0 " + f"{x2 - x1} {y2 - y1}".encode()
                               + b"] /Length " + str(len(box)).encode() + b" >>\nstream\n" + box + b"\nendstream")
        objects[widget] = (f"<< /Type /Annot /Subtype /Widget /FT /Tx /T ({field.name}) /TU ({field.label}) "
                           f"/Rect [{x1} {y1} {x2} {y2}] /F 4 /P 3 0 R /DA (/Helv 11 Tf 0 g) "
                           f"/MK << /BC [0.5 0.5 0.6] /BG [0.95 0.95 1] >> /AP << /N {appearance} 0 R >> >>").encode()
        widgets.append(f"{widget} 0 R")
    refs = " ".join(widgets).encode()
    objects[3] = (b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /Helv 4 0 R >> >> "
                  b"/Contents 6 0 R /Annots [" + refs + b"] >>")
    objects[5] = b"<< /Fields [" + refs + b"] /DR << /Font << /Helv 4 0 R >> >> /DA (/Helv 11 Tf 0 g) >>"
    out = bytearray(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    for number in sorted(objects):
        offsets[number] = len(out)
        out += f"{number} 0 obj\n".encode() + objects[number] + b"\nendobj\n"
    size = max(objects) + 1
    xref = len(out)
    out += f"xref\n0 {size}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{offsets[number]:010d} 00000 n \n".encode() for number in range(1, size))
    out += f"trailer\n<< /Size {size} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def _media_setup(ws: Path) -> None:
    (ws / MEDIA_PHOTO).write_bytes(media_photo_jpeg())
    (ws / MEDIA_FORM).write_bytes(media_form_pdf())
    write(ws, MEDIA_DETAILS, MEDIA_DETAILS_TEXT)


# --------------------------------------------------------------- reference ----


def media_crop_box(left: int) -> tuple[int, int, int, int]:
    """The full-height 4:5 window of the photo starting at `left`."""
    width = MEDIA_PHOTO_SIZE[1] * MEDIA_FEED_SIZE[0] // MEDIA_FEED_SIZE[1]
    return (left, 0, left + width, MEDIA_PHOTO_SIZE[1])


def media_write_photo(ws: Path, box: tuple[int, int, int, int] | None = None, size: tuple[int, int] = MEDIA_FEED_SIZE,
                      fmt: str = "JPEG") -> None:
    from PIL import Image

    image = Image.open(ws / MEDIA_PHOTO)
    if box is not None:
        image = image.crop(box)
    (ws / MEDIA_PHOTO_OUT).parent.mkdir(parents=True, exist_ok=True)
    image.resize(size, Image.Resampling.LANCZOS).save(ws / MEDIA_PHOTO_OUT, fmt)


def media_write_form(ws: Path, values: dict[str, str] | None = None, flatten: bool = True) -> None:
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter(clone_from=PdfReader(ws / MEDIA_FORM))
    filled = values if values is not None else {field.name: field.value for field in MEDIA_FIELDS}
    writer.update_page_form_field_values(writer.pages[0], filled, auto_regenerate=False, flatten=flatten)
    if flatten:
        writer.remove_annotations(subtypes="/Widget")
        del writer.root_object["/AcroForm"]
    (ws / MEDIA_FORM_OUT).parent.mkdir(parents=True, exist_ok=True)
    with open(ws / MEDIA_FORM_OUT, "wb") as out:
        writer.write(out)


def _media_reference(ws: Path) -> list[str]:
    media_write_photo(ws, media_crop_box(MEDIA_PHOTO_SIZE[0] - media_crop_box(0)[2]))
    media_write_form(ws)
    return ["Cropped the photo around the balloon and filled and flattened the permit."]


# ------------------------------------------------------------------- check ----


def _media_photo_checks(ws: Path, result: CheckResult) -> None:
    from PIL import Image, UnidentifiedImageError

    path = ws / MEDIA_PHOTO_OUT
    try:
        image = Image.open(path)
        image.load()
    except (OSError, UnidentifiedImageError) as error:
        for name in ("photo is a JPEG", "photo is exactly 1080x1350", "balloon fully in frame and undistorted"):
            result.add(name, False, saw(f"{type(error).__name__} reading {MEDIA_PHOTO_OUT}", "a readable JPEG"))
        return
    result.add("photo is a JPEG", image.format == "JPEG", saw(image.format, "JPEG"))
    result.add("photo is exactly 1080x1350", image.size == MEDIA_FEED_SIZE, saw(image.size, MEDIA_FEED_SIZE))
    ok, why = media_balloon_whole(image)
    result.add("balloon fully in frame and undistorted", ok, why)


def media_balloon_whole(image: object) -> tuple[bool, str]:
    """The magenta disc: present, clear of every edge, round and filled like a whole disc."""
    rgb = image.convert("RGB")  # type: ignore[attr-defined]
    width, height = rgb.size
    pixels = rgb.load()
    xs, ys = [], []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r > 170 and b > 130 and g < 100:
                xs.append(x)
                ys.append(y)
    if len(xs) < MEDIA_MIN_BALLOON_PX ** 2 // 2:
        return False, saw(f"{len(xs)} magenta pixels", "the balloon in the picture")
    left, right, top, bottom = min(xs), max(xs), min(ys), max(ys)
    box_w, box_h = right - left + 1, bottom - top + 1
    found = {"bbox": (left, top, right, bottom), "size": (width, height)}
    if left <= 1 or top <= 1 or right >= width - 2 or bottom >= height - 2:
        return False, saw(found, "the balloon clear of every edge")
    ratio, fill = box_w / box_h, len(xs) / (box_w * box_h)
    if not MEDIA_ROUND_RATIO[0] <= ratio <= MEDIA_ROUND_RATIO[1] or not MEDIA_DISC_FILL[0] <= fill <= MEDIA_DISC_FILL[1]:
        return False, saw({**found, "width/height": round(ratio, 2), "fill": round(fill, 2)}, "a round, whole balloon")
    return True, ""


def _media_apply(matrix: Sequence[float], x: float, y: float) -> tuple[float, float]:
    return matrix[0] * x + matrix[2] * y + matrix[4], matrix[1] * x + matrix[3] * y + matrix[5]


def media_field_texts(path: Path) -> tuple[dict[str, str], bool, str]:
    """Text drawn inside each field's box, whether the form is flattened, and why reading failed."""
    from pypdf import PdfReader
    from pypdf.errors import PyPdfError

    try:
        reader = PdfReader(path)
        page = reader.pages[0]
        pieces: list[tuple[float, float, str]] = []
        # pypdf restarts cm at identity inside a form XObject, which is where flattening tools put the values:
        # each Do pushes the placement it ran under, popped by the Q that closes it at the outer level.
        frames: list[list[object]] = []

        def before(operator: bytes, args: object, cm: Sequence[float], tm: Sequence[float]) -> None:
            if operator == b"Do":
                frames.append([list(cm), 0])
            elif frames and operator == b"q":
                frames[-1][1] += 1  # type: ignore[operator]
            elif frames and operator == b"Q":
                frames[-1][1] -= 1  # type: ignore[operator]
                if frames[-1][1] < 0:  # type: ignore[operator]
                    frames.pop()

        def visit(text: str, cm: Sequence[float], tm: Sequence[float], *_: object) -> None:
            if not text.strip():
                return
            x, y = _media_apply(cm, tm[4], tm[5])
            for outer, _depth in reversed(frames):
                x, y = _media_apply(outer, x, y)  # type: ignore[arg-type]
            pieces.append((x, y, text))

        page.extract_text(visitor_operand_before=before, visitor_text=visit)
        annots = [annot.get_object() for annot in page.get("/Annots") or []]
        widgets = [annot for annot in annots if annot.get("/Subtype") == "/Widget"]
        fields = reader.get_fields() or {}
        flattened = not widgets and not fields
    except (PyPdfError, OSError, ValueError, KeyError, IndexError) as error:
        return {}, False, f"{type(error).__name__}: {error}"
    texts = {}
    for field in MEDIA_FIELDS:
        x1, y1, x2, y2 = field.rect
        inside = [text for x, y, text in pieces if x1 - 8 <= x <= x2 + 8 and y1 - 8 <= y <= y2 + 8]
        # Still a live form: the value is in the field, which "flattened" fails on its own.
        live = str((fields.get(field.name) or {}).get("/V") or "")
        texts[field.name] = " ".join((" ".join(inside) or live).split())
    return texts, flattened, ""


def media_value_ok(got: str, field: MediaField) -> bool:
    """Exact text, except a count, which may read "40" or "about 40" (the details say "about 40")."""
    if field.name == "attendees":
        return re.findall(r"\d+", got) == [field.value]
    return got.strip().casefold() == field.value.casefold()


def _media_form_checks(ws: Path, result: CheckResult) -> None:
    path = ws / MEDIA_FORM_OUT
    texts, flattened, error = media_field_texts(path) if path.is_file() else ({}, False, f"no {MEDIA_FORM_OUT}")
    for field in MEDIA_FIELDS:
        got = texts.get(field.name, "")
        result.add(f"permit {field.name} filled", media_value_ok(got, field),
                   saw(error or got, f"{field.value!r} shown in the {field.label} box"))
    result.add("permit flattened", path.is_file() and not error and flattened,
               saw(error or "fields still editable", "no form fields or widgets left"))


def _media_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    originals = {MEDIA_PHOTO: media_photo_jpeg(), MEDIA_FORM: media_form_pdf()}
    changed = [name for name, body in originals.items()
               if not (ws / name).is_file() or hashlib.sha256((ws / name).read_bytes()).digest() != hashlib.sha256(body).digest()]
    result.mandatory.append((MEDIA_ORIGINALS_GATE, not changed))
    if changed:
        result.details[MEDIA_ORIGINALS_GATE] = saw(changed, "both originals byte for byte")
    _media_photo_checks(ws, result)
    _media_form_checks(ws, result)
    return result


TASKS: list[EvalTask] = [EvalTask(
    id="file-media-edit",
    category="documents",
    provenance="new for bench#153: crop a photo for a social feed and fill and flatten a PDF form",
    summary="Crop a photo to a 1080x1350 feed picture keeping its subject, and fill and flatten a PDF form.",
    setup=_media_setup,
    steps=(Step(MEDIA_PROMPT),),
    check=_media_check,
    reference=_media_reference,
    timeout_s=90,
    checkpoints=checkpoints(("read the details", r"event-details"), ("made the feed photo", r"feed-photo"),
                            ("filled the permit", r"permit-filled")),
)]
