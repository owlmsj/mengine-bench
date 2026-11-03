"""Gold tests for media-voice (#153): WAV reading, WER, and the check with speech and transcription stubbed.

The one real end-to-end test (SAPI speech, whisper tiny) runs only where both are available offline.
"""

from __future__ import annotations

import math
import struct
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

from mengine_bench import catalog, speech
from mengine_bench.tasks import media
from mengine_bench.tasks.media import MAX_WER, SENTENCE, TASKS, WAV

TASK = TASKS[0]


def tone(path: Path, seconds: float, rate: int = 22_050) -> None:
    frames = b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * 440 * i / rate))) for i in range(int(seconds * rate)))
    with wave.open(str(path), "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(rate)
        writer.writeframes(frames)


@pytest.fixture
def heard(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """What the stubbed whisper hears; the reference's speech engine is stubbed with a 5.5 s tone."""
    said = [SENTENCE]
    monkeypatch.setattr(speech, "transcribe", lambda audio: said[0])
    monkeypatch.setattr(media, "speak", lambda sentence, target: tone(target, 5.5))
    return said


def test_reference_passes_and_untouched_fails(tmp_path: Path, heard: list[str]) -> None:
    (tmp_path / "empty").mkdir()
    TASK.setup(tmp_path / "empty")
    assert not TASK.check(tmp_path / "empty", [""]).passed
    (tmp_path / "solved").mkdir()
    TASK.setup(tmp_path / "solved")
    result = TASK.check(tmp_path / "solved", TASK.reference(tmp_path / "solved"))
    assert result.passed, result.details


@pytest.mark.parametrize("seconds", [2.0, 9.5])
def test_a_wav_outside_the_duration_range_fails(tmp_path: Path, heard: list[str], seconds: float) -> None:
    tone(tmp_path / WAV, seconds)
    assert TASK.check(tmp_path, [""]).failed() == ["lasts 4 to 8 s"]


def test_another_sentence_fails(tmp_path: Path, heard: list[str]) -> None:
    heard[0] = "Welcome aboard the morning train, please keep your coats clear of the windows."
    tone(tmp_path / WAV, 5.5)
    assert TASK.check(tmp_path, [""]).failed() == ["whisper tiny hears the sentence"]


def test_a_renamed_mp3_is_not_a_wav(tmp_path: Path, heard: list[str]) -> None:
    (tmp_path / WAV).write_bytes(b"ID3\x04\x00" + bytes(4000))
    assert "announcement.wav is a valid WAV" in TASK.check(tmp_path, [""]).failed()


def test_float_and_24_bit_wavs_read_like_16_bit(tmp_path: Path) -> None:
    rate, samples = 16_000, np.sin(np.linspace(0, 200, 16_000)) * 0.5
    for tag, bits, data in ((3, 32, samples.astype("<f4").tobytes()),
                            (1, 24, b"".join(int(v * (1 << 23)).to_bytes(3, "little", signed=True) for v in samples))):
        fmt = struct.pack("<HHIIHH", tag, 1, rate, rate * bits // 8, bits // 8, bits)
        body = b"WAVE" + b"fmt " + struct.pack("<I", len(fmt)) + fmt + b"data" + struct.pack("<I", len(data)) + data
        path = tmp_path / f"{bits}.wav"
        path.write_bytes(b"RIFF" + struct.pack("<I", len(body)) + body)
        audio = speech.read_wav(path)
        assert audio.seconds == 1.0 and np.allclose(audio.samples, samples, atol=1e-3)


def test_word_error_rate_ignores_case_and_punctuation() -> None:
    assert speech.word_error_rate(SENTENCE, SENTENCE.upper().replace(",", "")) == 0
    assert speech.word_error_rate(SENTENCE, SENTENCE.replace("ferry", "fairy")) == pytest.approx(1 / 13)
    assert speech.word_error_rate(SENTENCE, "") == 1.0


def test_the_task_is_in_the_catalog_and_asks_for_the_model_before_the_run() -> None:
    assert TASK.id in {task.id for task in catalog.all_tasks()}
    assert "speech-model" in TASK.needs and MAX_WER == 0.2


def _speech_ready() -> bool:
    if sys.platform != "win32":
        return False
    try:
        from huggingface_hub import try_to_load_from_cache
    except ImportError:
        return False
    return isinstance(try_to_load_from_cache("Systran/faster-whisper-tiny", "model.bin"), str)


@pytest.mark.skipif(not _speech_ready(), reason="needs Windows SAPI and whisper tiny in the local cache")
def test_real_speech_passes_end_to_end(tmp_path: Path) -> None:
    TASK.setup(tmp_path)
    result = TASK.check(tmp_path, TASK.reference(tmp_path))
    assert result.passed, result.details
