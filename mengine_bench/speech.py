"""WAV reading and an offline whisper-tiny transcript for audio tasks (#153).

The owner approved whisper tiny as a grader dependency. faster-whisper runs it on the CPU in int8; the model is
fetched once by `ensure_speech_model` before a run that needs it, so grading never downloads. The WAV is decoded
here, not by faster-whisper's PyAV path: a PyAV release changed `av.open` and broke that path (measured
2026-11-03 with faster-whisper 1.x), and a WAV needs no codec.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np

WHISPER_MODEL = "tiny"
WHISPER_RATE = 16_000
PCM, IEEE_FLOAT, EXTENSIBLE = 1, 3, 0xFFFE


@dataclass(frozen=True)
class WavAudio:
    rate: int
    channels: int
    seconds: float
    # Mono float32 in [-1, 1].
    samples: np.ndarray


def read_wav(path: Path) -> WavAudio:
    """A RIFF/WAVE file with PCM 8/16/24/32-bit or float32/64 data, or ValueError naming what was found."""
    raw = path.read_bytes()
    if len(raw) < 12 or raw[:4] != b"RIFF" or raw[8:12] != b"WAVE":
        raise ValueError(f"received header {raw[:12]!r}; expected RIFF....WAVE")
    chunks: dict[bytes, bytes] = {}
    offset = 12
    while offset + 8 <= len(raw):
        kind, size = raw[offset:offset + 4], struct.unpack("<I", raw[offset + 4:offset + 8])[0]
        chunks.setdefault(kind, raw[offset + 8:offset + 8 + size])
        offset += 8 + size + (size & 1)
    fmt, data = chunks.get(b"fmt "), chunks.get(b"data")
    if fmt is None or len(fmt) < 16 or not data:
        raise ValueError(f"received chunks {sorted(chunks)}; expected a fmt chunk and non-empty data")
    tag, channels, rate, _, align, bits = struct.unpack("<HHIIHH", fmt[:16])
    if tag == EXTENSIBLE and len(fmt) >= 26:
        tag = struct.unpack("<H", fmt[24:26])[0]
    if channels < 1 or rate < 1000 or align != channels * bits // 8:
        raise ValueError(f"received {channels} channels at {rate} Hz, {bits} bits; expected a playable PCM layout")
    frames = len(data) // align
    samples = _decode(data[:frames * align], tag, bits).reshape(frames, channels).mean(axis=1)
    return WavAudio(rate=rate, channels=channels, seconds=frames / rate, samples=samples.astype(np.float32))


def _decode(data: bytes, tag: int, bits: int) -> np.ndarray:
    if tag == IEEE_FLOAT and bits in (32, 64):
        return np.frombuffer(data, dtype="<f4" if bits == 32 else "<f8").astype(np.float64)
    if tag != PCM or bits not in (8, 16, 24, 32):
        raise ValueError(f"received format tag {tag} with {bits} bits; expected PCM 8/16/24/32 or float 32/64")
    if bits == 8:
        return (np.frombuffer(data, dtype=np.uint8).astype(np.float64) - 128) / 128
    if bits == 24:
        triples = np.frombuffer(data, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        values = triples[:, 0] | (triples[:, 1] << 8) | (triples[:, 2] << 16)
        return np.where(values >= 1 << 23, values - (1 << 24), values) / float(1 << 23)
    kind = "<i2" if bits == 16 else "<i4"
    return np.frombuffer(data, dtype=kind).astype(np.float64) / float(1 << (bits - 1))


def resample(samples: np.ndarray, rate: int, target: int = WHISPER_RATE) -> np.ndarray:
    """Linear resampling: enough for speech recognition, and no new dependency."""
    if rate == target or not len(samples):
        return samples.astype(np.float32)
    count = int(round(len(samples) * target / rate))
    positions = np.linspace(0, len(samples) - 1, count)
    return np.interp(positions, np.arange(len(samples)), samples).astype(np.float32)


def ensure_speech_model() -> str:
    """Fetch whisper tiny into the Hugging Face cache now, so grading never downloads; returns its folder."""
    from faster_whisper import download_model

    return str(download_model(WHISPER_MODEL))


def transcribe(audio: WavAudio) -> str:
    """English transcript of the audio by whisper tiny, from the local cache only."""
    from faster_whisper import WhisperModel

    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8", local_files_only=True)
    segments, _ = model.transcribe(resample(audio.samples, audio.rate), language="en", beam_size=5)
    return " ".join(segment.text for segment in segments).strip()


def words(text: str) -> list[str]:
    return re.sub(r"[^a-z0-9' ]+", " ", text.lower().replace("’", "'")).split()


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Word-level edit distance over the reference length, after lowercasing and dropping punctuation."""
    ref, hyp = words(reference), words(hypothesis)
    row = list(range(len(hyp) + 1))
    for i, word in enumerate(ref, 1):
        previous, row[0] = row[0], i
        for j, other in enumerate(hyp, 1):
            previous, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, previous + (word != other))
    return row[-1] / max(len(ref), 1)
