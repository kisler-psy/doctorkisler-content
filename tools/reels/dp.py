# -*- coding: utf-8 -*-
"""Выбор границ фраз среди пауз динамическим программированием.

Сравниваем не длину отрезка целиком, а чистое время речи внутри него:
паузы между перечислениями иначе растягивают короткую фразу.
"""
import math

INF = float("inf")


class Speech(object):
    """Чистое время речи от нуля до момента t."""

    def __init__(self, sil):
        self.sil = sorted(sil)

    def upto(self, t):
        quiet = 0.0
        for a, b in self.sil:
            if b <= t:
                quiet += b - a
            elif a < t:
                quiet += t - a
                break
            else:
                break
        return t - quiet

    def between(self, a, b):
        return max(self.upto(b) - self.upto(a), 0.0)


def fit(phrase_secs, sil, t0, t1, min_speech=0.28):
    """Разложить фразы по отрезку [t0, t1], ставя границы в серединах пауз."""
    sp = Speech(sil)
    n = len(phrase_secs)
    total_speech = sp.between(t0, t1)
    total_est = sum(phrase_secs)
    expect = [p / total_est * total_speech for p in phrase_secs]

    pts = [t0]
    for a, b in sorted(sil):
        mid = (a + b) / 2.0
        if t0 < mid < t1:
            pts.append(mid)
    pts.append(t1)
    m = len(pts)

    best = [[INF] * m for _ in range(n + 1)]
    back = [[-1] * m for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(1, n + 1):
        for j in range(i, m):
            if i == n and j != m - 1:
                continue
            for k in range(i - 1, j):
                if best[i - 1][k] == INF:
                    continue
                got = sp.between(pts[k], pts[j])
                if got < min_speech:
                    continue
                cost = best[i - 1][k] + math.log(got / expect[i - 1]) ** 2
                if cost < best[i][j]:
                    best[i][j] = cost
                    back[i][j] = k
    if best[n][m - 1] == INF:
        out, t = [], t0
        step = (t1 - t0) / total_est
        for e in phrase_secs:
            out.append((t, t + e * step))
            t += e * step
        return out
    seq, j = [], m - 1
    for i in range(n, 0, -1):
        k = back[i][j]
        seq.append((pts[k], pts[j]))
        j = k
    return list(reversed(seq))
