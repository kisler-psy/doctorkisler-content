# -*- coding: utf-8 -*-
"""Привязка фраз к речи через DTW между синтезом espeak и записью.

Распознавание в облаке недоступно, поэтому синтезируем тот же текст
espeak-ng и тянем его на запись по мел-спектру. Тембры разные, но
структура гласных и пауз совпадает, и этого хватает, чтобы найти
границы фраз.
"""
import io
import re
import subprocess
import wave
import numpy as np

SR = 16000
HOP = 0.02
NMEL = 26


def _wav_bytes_to_array(raw):
    with wave.open(io.BytesIO(raw)) as w:
        n = w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64)
    return a / 32768.0


def read_media(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR),
         "-f", "wav", "-"], capture_output=True).stdout
    return _wav_bytes_to_array(raw)


def synth(text, voice="ru", speed=160):
    clean = re.sub(r"[«»„“”]", " ", text)
    raw = subprocess.run(
        ["espeak-ng", "-v", voice, "-s", str(speed), "--stdout", clean],
        capture_output=True).stdout
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", "pipe:0", "-ac", "1", "-ar", str(SR),
         "-f", "wav", "-"], input=raw, capture_output=True).stdout
    return _wav_bytes_to_array(raw)


def _mel_bank(nfft, sr=SR, nmel=NMEL, fmin=60.0, fmax=7000.0):
    def hz2mel(f):
        return 2595.0 * np.log10(1.0 + f / 700.0)

    def mel2hz(m):
        return 700.0 * (10 ** (m / 2595.0) - 1.0)

    pts = mel2hz(np.linspace(hz2mel(fmin), hz2mel(fmax), nmel + 2))
    bins = np.floor((nfft + 1) * pts / sr).astype(int)
    fb = np.zeros((nmel, nfft // 2 + 1))
    for i in range(nmel):
        l, c, r = bins[i], bins[i + 1], bins[i + 2]
        if c == l:
            c = l + 1
        if r == c:
            r = c + 1
        fb[i, l:c] = (np.arange(l, c) - l) / float(c - l)
        fb[i, c:r] = (r - np.arange(c, r)) / float(r - c)
    return fb


def features(a, sr=SR, hop=HOP, win=0.025):
    h, wn = int(sr * hop), int(sr * win)
    nfft = 1
    while nfft < wn:
        nfft *= 2
    fb = _mel_bank(nfft, sr)
    win_fn = np.hanning(wn)
    nfr = max(1, (len(a) - wn) // h)
    out = np.empty((nfr, NMEL))
    for i in range(nfr):
        seg = a[i * h:i * h + wn] * win_fn
        spec = np.abs(np.fft.rfft(seg, nfft)) ** 2
        out[i] = np.log(fb.dot(spec) + 1e-10)
    # убираем разницу тембров: нормируем каждую полосу
    out -= out.mean(axis=0)
    out /= (out.std(axis=0) + 1e-6)
    # и каждый кадр, чтобы считать косинусное расстояние
    out -= out.mean(axis=1, keepdims=True)
    out /= (np.linalg.norm(out, axis=1, keepdims=True) + 1e-6)
    return out


def path(fx, fy, band=0.18):
    """DTW-путь между синтезом fx и записью fy. Возвращает для каждого
    кадра синтеза индекс кадра записи. Поиск ограничен полосой вокруг
    диагонали: темп речи отличается не в разы."""
    n, m = len(fx), len(fy)
    cost = 1.0 - fx.dot(fy.T)
    w = max(int(band * max(n, m)), 40)
    acc = np.full((n, m), np.inf)
    ptr = np.zeros((n, m), dtype=np.int8)
    acc[0, 0] = cost[0, 0]
    for j in range(1, min(m, w + 1)):
        acc[0, j] = acc[0, j - 1] + cost[0, j]
        ptr[0, j] = 2
    for i in range(1, n):
        prev = acc[i - 1]
        row = acc[i]
        c = cost[i]
        centre = int(i * (m - 1) / float(n - 1)) if n > 1 else 0
        j0, j1 = max(0, centre - w), min(m, centre + w + 1)
        if j0 == 0:
            row[0] = prev[0] + c[0]
            ptr[i, 0] = 1
            j0 = 1
        for j in range(j0, j1):
            d, p = prev[j], 1            # шаг по синтезу
            if prev[j - 1] < d:
                d, p = prev[j - 1], 0    # диагональ
            if row[j - 1] < d:
                d, p = row[j - 1], 2     # шаг по записи
            row[j] = d + c[j]
            ptr[i, j] = p
    # обратный ход
    i, j = n - 1, m - 1
    map_x = np.zeros(n, dtype=int)
    while True:
        map_x[i] = j
        if i == 0 and j == 0:
            break
        p = ptr[i, j]
        if p == 0:
            i, j = i - 1, j - 1
        elif p == 1:
            i -= 1
        else:
            j -= 1
    return map_x
