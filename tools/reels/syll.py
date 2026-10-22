# -*- coding: utf-8 -*-
"""Счёт слоговых вершин в записи: проверка привязки фраз без распознавания."""
import subprocess
import wave
import numpy as np

VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")


def vowels(text):
    return sum(1 for ch in text if ch in VOWELS)


def envelope(media, sr=16000, hop=0.01, win=0.03):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", media, "-ac", "1", "-ar", str(sr),
         "-f", "wav", "-"], capture_output=True).stdout
    import io
    with wave.open(io.BytesIO(raw)) as w:
        n = w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    h, wn = int(sr * hop), int(sr * win)
    frames = (len(a) - wn) // h
    e = np.empty(frames)
    for i in range(frames):
        seg = a[i * h:i * h + wn]
        e[i] = np.sqrt(np.mean(seg * seg) + 1e-12)
    db = 20 * np.log10(e + 1e-12)
    # сглаживание по 50 мс
    k = np.ones(5) / 5.0
    db = np.convolve(db, k, mode="same")
    return db, hop


def peaks(db, hop, floor=None, prom=2.5, min_gap=0.09):
    if floor is None:
        floor = np.percentile(db, 60) - 6
    out = []
    gap = int(min_gap / hop)
    i = 1
    while i < len(db) - 1:
        if db[i] >= db[i - 1] and db[i] > db[i + 1] and db[i] > floor:
            lo = db[max(0, i - 25):i].min()
            hi = db[i + 1:i + 26].min() if i + 1 < len(db) else db[i]
            if db[i] - max(lo, hi) >= prom:
                if not out or i - out[-1] >= gap:
                    out.append(i)
                elif db[i] > db[out[-1]]:
                    out[-1] = i
        i += 1
    return [p * hop for p in out]
