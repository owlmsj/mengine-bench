"""#153: file-media-edit reads back the feed photo and the flattened permit; wrong crops and forms fail."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DecodedStreamObject, NameObject

from mengine_bench import catalog
from mengine_bench.tasks import mediaedit as media
from mengine_bench.tasks.mediaedit import (
    MEDIA_FIELDS,
    MEDIA_FORM,
    MEDIA_FORM_OUT,
    MEDIA_PHOTO,
    MEDIA_PHOTO_OUT,
    MEDIA_PHOTO_SIZE,
    media_crop_box,
    media_write_form,
    media_write_photo,
)

TASK = next(task for task in catalog.all_tasks() if task.id == "file-media-edit")
VALUES = {field.name: field.value for field in MEDIA_FIELDS}


def _ws(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    ws.mkdir(parents=True)
    TASK.setup(ws)
    return ws


def test_the_reference_passes_and_the_untouched_folder_fails(tmp_path: Path) -> None:
    ws = _ws(tmp_path)
    TASK.reference(ws)
    result = TASK.check(ws, [""])
    assert result.passed, result.details
    bare = TASK.check(_ws(tmp_path / "bare"), [""])
    assert bare.score == 0.0 and bare.mandatory_ok


def _letterboxed(ws: Path) -> None:
    """Another valid route: the whole photo scaled into the frame on a white band."""
    photo = Image.open(ws / MEDIA_PHOTO)
    photo.thumbnail(media.MEDIA_FEED_SIZE)
    canvas = Image.new("RGB", media.MEDIA_FEED_SIZE, "white")
    canvas.paste(photo, (0, (media.MEDIA_FEED_SIZE[1] - photo.height) // 2))
    (ws / "out").mkdir(exist_ok=True)
    canvas.save(ws / MEDIA_PHOTO_OUT, "JPEG", quality=80, progressive=True)


def _form_by_hand(ws: Path) -> None:
    """Another valid route: values drawn on the page as text, the form dropped, about 40 written as given."""
    writer = PdfWriter(clone_from=PdfReader(ws / MEDIA_FORM))
    page = writer.pages[0]
    ops = []
    for field in MEDIA_FIELDS:
        value = "about 40" if field.name == "attendees" else field.value
        ops.append(f"BT /Helv 11 Tf {field.rect[0] + 3} {field.rect[1] + 7} Td ({value}) Tj ET")
    extra = DecodedStreamObject()
    extra.set_data("\n".join(ops).encode("latin-1"))
    page[NameObject("/Contents")] = ArrayObject([page.raw_get("/Contents"), writer._add_object(extra)])
    writer.remove_annotations(subtypes="/Widget")
    del writer.root_object["/AcroForm"]
    (ws / "out").mkdir(exist_ok=True)
    with open(ws / MEDIA_FORM_OUT, "wb") as out:
        writer.write(out)


def test_other_valid_routes_pass(tmp_path: Path) -> None:
    ws = _ws(tmp_path)
    _letterboxed(ws)
    _form_by_hand(ws)
    result = TASK.check(ws, [""])
    assert result.passed, result.details


def _photo_and_form(photo: Callable[[Path], None], form: Callable[[Path], None]) -> Callable[[Path], None]:
    def act(ws: Path) -> None:
        photo(ws)
        form(ws)
    return act


RIGHT_CROP = media_crop_box(MEDIA_PHOTO_SIZE[0] - media_crop_box(0)[2])
CENTRE_CROP = media_crop_box((MEDIA_PHOTO_SIZE[0] - media_crop_box(0)[2]) // 2)
# The window that ends inside the balloon: half of it cut off at the right edge.
HALF_CROP = media_crop_box(media.MEDIA_BALLOON_CENTER[0] - media_crop_box(0)[2])


@pytest.mark.parametrize(("act", "failed"), [
    (_photo_and_form(lambda ws: media_write_photo(ws, CENTRE_CROP), media_write_form), ["balloon fully in frame and undistorted"]),
    (_photo_and_form(lambda ws: media_write_photo(ws, HALF_CROP), media_write_form), ["balloon fully in frame and undistorted"]),
    # Squashed: the whole landscape stretched to the portrait size.
    (_photo_and_form(lambda ws: media_write_photo(ws, None), media_write_form), ["balloon fully in frame and undistorted"]),
    (_photo_and_form(lambda ws: media_write_photo(ws, RIGHT_CROP, (864, 1080)), media_write_form), ["photo is exactly 1080x1350"]),
    (_photo_and_form(lambda ws: media_write_photo(ws, RIGHT_CROP, fmt="PNG"), media_write_form), ["photo is a JPEG"]),
    (_photo_and_form(lambda ws: media_write_photo(ws, RIGHT_CROP), lambda ws: media_write_form(ws, flatten=False)), ["permit flattened"]),
    (_photo_and_form(lambda ws: media_write_photo(ws, RIGHT_CROP),
                     lambda ws: media_write_form(ws, {**VALUES, "event_date": "5 December 2026"})), ["permit event_date filled"]),
    (_photo_and_form(lambda ws: media_write_photo(ws, RIGHT_CROP),
                     lambda ws: media_write_form(ws, {**VALUES, "location": VALUES["organizer"], "organizer": VALUES["location"]})),
     ["permit organizer filled", "permit location filled"]),
])
def test_each_plausible_mistake_fails_its_check(tmp_path: Path, act: Callable[[Path], None], failed: list[str]) -> None:
    ws = _ws(tmp_path)
    act(ws)
    result = TASK.check(ws, [""])
    assert result.failed() == failed, result.details


def test_an_edited_original_fails_the_gate(tmp_path: Path) -> None:
    ws = _ws(tmp_path)
    TASK.reference(ws)
    media_write_photo(ws, RIGHT_CROP)
    (ws / MEDIA_PHOTO).write_bytes((ws / MEDIA_PHOTO_OUT).read_bytes())
    result = TASK.check(ws, [""])
    assert media.MEDIA_ORIGINALS_GATE in result.failed() and result.score == 0.0


def test_the_fixture_form_has_four_empty_fields_and_the_photo_its_balloon() -> None:
    import io

    reader = PdfReader(io.BytesIO(media.media_form_pdf()))
    fields = reader.get_fields() or {}
    assert sorted(fields) == sorted(VALUES) and not any(field.get("/V") for field in fields.values())
    photo = Image.open(io.BytesIO(media.media_photo_jpeg()))
    assert photo.size == MEDIA_PHOTO_SIZE and media.media_balloon_whole(photo)[0]


def test_the_brief_hands_over_no_method() -> None:
    prompt = TASK.steps[0].prompt
    for leaked in ("crop", "Pillow", "pypdf", "2026-12-05", "magick", "ffmpeg"):
        assert leaked not in prompt, leaked
