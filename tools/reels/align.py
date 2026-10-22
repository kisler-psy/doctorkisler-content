# -*- coding: utf-8 -*-
"""Привязка фраз к речи без распознавания.

Длительности фраз оцениваем через espeak-ng (ru, скорость 160), границы
между фразами ищем среди пауз, найденных ffmpeg silencedetect, а выбор
границ делает динамическое программирование (dp.py).
"""
import re
import subprocess
import tempfile
import os
import wave


def espeak_duration(text, voice="ru", speed=160):
    """Длительность фразы в секундах по синтезу espeak-ng."""
    clean = re.sub(r"[«»„“”…]", " ", text)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        path = f.name
    try:
        subprocess.run(
            ["espeak-ng", "-v", voice, "-s", str(speed), "-w", path, clean],
            check=True, capture_output=True)
        with wave.open(path) as w:
            return w.getnframes() / float(w.getframerate())
    finally:
        os.unlink(path)


def silences(media, noise="-32dB", d=0.16):
    """Список пауз [(начало, конец), ...] по ffmpeg silencedetect."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", media,
         "-af", "silencedetect=noise=%s:d=%s" % (noise, d), "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))


def duration(media):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", media],
        capture_output=True, text=True).stdout
    return float(out.strip())
