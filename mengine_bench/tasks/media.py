"""Basic media creation: a short spoken announcement as a WAV file (#153).

Any route counts: the OS speech engine (Windows SAPI, macOS `say`, espeak-ng), a TTS tool or anything else. The
check reads the WAV itself and transcribes it with whisper tiny (`mengine_bench.speech`), fetched before the run.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from mengine_bench import speech
from mengine_bench.core import CheckResult, EvalTask, Step, checkpoints, saw, write

WAV = "announcement.wav"
SENTENCE = "Welcome aboard the evening ferry, please keep your bags clear of the doors."
MIN_S, MAX_S = 4.0, 8.0
# Measured 2026-11-03 (#153), whisper tiny on Windows SAPI speech of this 13-word sentence and a 14-word one: WER
# 0.077 and 0.071, one homophone each ("fairy", "harbour"); a near-miss sentence in the same frame scored 0.357.
# 0.2 lets 2 of the 13 words slip (0.154) and fails 3 (0.231).
MAX_WER = 0.2
CREATE_NO_WINDOW = 0x08000000

PROMPT = f"""The ferry company's boarding screens play a short recorded announcement. The next one is this sentence:

"{SENTENCE}"

Deliver it as spoken audio in `./{WAV}`, a WAV file of {MIN_S:g} to {MAX_S:g} seconds that a passenger can understand."""


def _setup(ws: Path) -> None:
    write(ws, "README.md", "Boarding screen announcements for the ferry line. Audio files go in this folder.\n")


def speak(sentence: str, target: Path) -> None:
    """The OS speech engine, no window: the reference route, and one an agent may take."""
    if sys.platform == "win32":
        text = sentence.replace("'", "''")
        script = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                  f"$s.SetOutputToWaveFile('{target}'); $s.Speak('{text}'); $s.Dispose()")
        argv = ["powershell", "-NoProfile", "-NonInteractive", "-Command", script]
    elif shutil.which("say"):
        argv = ["say", "-o", str(target), "--data-format=LEI16@22050", sentence]
    elif shutil.which("espeak-ng") or shutil.which("espeak"):
        argv = [shutil.which("espeak-ng") or "espeak", "-w", str(target), sentence]
    else:
        raise RuntimeError("received no speech engine (SAPI, say or espeak-ng); expected one for the reference")
    flags = CREATE_NO_WINDOW if sys.platform == "win32" else 0
    subprocess.run(argv, check=True, capture_output=True, timeout=60, creationflags=flags)


def _reference(ws: Path) -> list[str]:
    speak(SENTENCE, ws / WAV)
    return [f"Wrote {WAV} with the system speech engine."]


def _check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    path = ws / WAV
    try:
        audio = speech.read_wav(path) if path.is_file() else None
        problem = "" if audio else "no file"
    except ValueError as error:
        audio, problem = None, str(error)
    result.add("announcement.wav is a valid WAV", audio is not None, saw(problem, "a RIFF/WAVE file with audio"))
    seconds = audio.seconds if audio else 0.0
    result.add(f"lasts {MIN_S:g} to {MAX_S:g} s", MIN_S <= seconds <= MAX_S, saw(round(seconds, 2), (MIN_S, MAX_S)))
    try:
        heard = speech.transcribe(audio) if audio and seconds <= 60 else ""
    except Exception as error:  # noqa: BLE001 - a missing model must fail this check, not crash the grading
        heard = ""
        result.notes.append(f"whisper tiny could not run: {type(error).__name__}: {error}"[:300])
    rate = speech.word_error_rate(SENTENCE, heard)
    result.add("whisper tiny hears the sentence", rate <= MAX_WER,
               saw(f"{heard!r} (WER {rate:.2f})", f"WER <= {MAX_WER}"))
    return result


TASKS: list[EvalTask] = [EvalTask(
    id="media-voice",
    category="media",
    provenance="new for bench#153 (computer use: basic media creation)",
    summary="Record a ferry boarding announcement as a short spoken WAV file.",
    setup=_setup,
    steps=(Step(PROMPT),),
    check=_check,
    reference=_reference,
    needs=frozenset({"speech-model"}),
    checkpoints=checkpoints(("used a speech engine", r"System\.Speech|SpeechSynthesizer|\bsay\b|espeak|tts"),
                            ("wrote the audio", r"announcement\.wav")),
    timeout_s=60,
)]
