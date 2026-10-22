# -*- coding: utf-8 -*-
"""Сборка ролика: кадры собираем в PIL, склеиваем ffmpeg (libx264, crf 17).

Звук берём из записи HeyGen без изменений.
"""
import subprocess
import numpy as np
from PIL import Image
import style

W, H, FPS = 1080, 1920, 25


def ease(p):
    """Плавное начало и конец движения камеры."""
    p = min(max(p, 0.0), 1.0)
    return p * p * (3 - 2 * p)


class VideoFrames(object):
    """Последовательное чтение кадров видео с нужного момента."""

    def __init__(self, path, start=0.0, fps=FPS):
        self.proc = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-ss", "%.3f" % start, "-i", path,
             "-vf", "fps=%d,scale=%d:%d" % (fps, W, H),
             "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            bufsize=W * H * 3 * 4)
        self.n = W * H * 3
        self.last = None

    def next(self):
        buf = self.proc.stdout.read(self.n)
        if buf is None or len(buf) < self.n:
            if self.last is None:
                raise RuntimeError("пустой источник кадров")
            return self.last          # кончился клип - держим последний кадр
        self.last = Image.frombytes("RGB", (W, H), buf)
        return self.last

    def close(self):
        try:
            self.proc.stdout.close()
            self.proc.kill()
        except Exception:
            pass


class Shot(object):
    """Кусок монтажа: источник плюс движение камеры."""

    def __init__(self, t0, t1, kind, path, src_start=0.0,
                 zoom=(1.0, 1.0), anchor=(0.5, 0.5), pan=(0.0, 0.0),
                 zoom_at=None):
        self.t0, self.t1 = t0, t1
        self.kind, self.path = kind, path
        self.src_start = src_start
        self.zoom, self.anchor, self.pan = zoom, anchor, pan
        self.zoom_at = zoom_at or []   # [(время, z), ...] - ломаная по зуму
        self.src = None
        self.still = None

    def open(self):
        if self.kind == "image":
            self.still = Image.open(self.path).convert("RGB")
            if self.still.size != (W, H):
                self.still = self.still.resize((W, H), Image.LANCZOS)
        else:
            self.src = VideoFrames(self.path, self.src_start)

    def close(self):
        if self.src:
            self.src.close()

    def _z(self, t):
        if self.zoom_at:
            pts = self.zoom_at
            if t <= pts[0][0]:
                return pts[0][1]
            for (ta, za), (tb, zb) in zip(pts, pts[1:]):
                if ta <= t <= tb:
                    return za + (zb - za) * ease((t - ta) / max(tb - ta, 1e-6))
            return pts[-1][1]
        p = ease((t - self.t0) / max(self.t1 - self.t0, 1e-6))
        return self.zoom[0] + (self.zoom[1] - self.zoom[0]) * p

    def frame(self, t):
        img = self.still if self.kind == "image" else self.src.next()
        z = self._z(t)
        p = ease((t - self.t0) / max(self.t1 - self.t0, 1e-6))
        ax = self.anchor[0] + self.pan[0] * p
        ay = self.anchor[1] + self.pan[1] * p
        if abs(z - 1.0) < 1e-4:
            return img
        cw, ch = W / z, H / z
        left = ax * W - cw * ax
        top = ay * H - ch * ay
        left = min(max(left, 0.0), W - cw)
        top = min(max(top, 0.0), H - ch)
        return img.crop((int(left), int(top), int(left + cw), int(top + ch))) \
                  .resize((W, H), Image.LANCZOS)


class Text(object):
    """Надпись с мягким появлением и уходом."""

    def __init__(self, t0, t1, fade=0.22, **kw):
        self.t0, self.t1, self.fade = t0, t1, fade
        self.ov = style.make(**kw)

    def alpha(self, t):
        if t < self.t0 or t >= self.t1:
            return 0.0
        a = min((t - self.t0) / self.fade, (self.t1 - t) / self.fade, 1.0)
        return max(a, 0.0)


def render(out_path, shots, texts, audio, duration, dim=None, crf=17):
    """Собрать ролик. dim - [(t0, t1, сила)] общего затемнения кадра."""
    total = int(round(duration * FPS))
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
         "-r", str(FPS), "-i", "-",
         "-i", audio,
         "-filter_complex", "[1:a]apad[a]",
         "-map", "0:v", "-map", "[a]", "-t", "%.3f" % duration,
         "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    cur = -1
    try:
        for i in range(total):
            t = i / float(FPS)
            while cur + 1 < len(shots) and t >= shots[cur + 1].t0 - 1e-9:
                if cur >= 0:
                    shots[cur].close()
                cur += 1
                shots[cur].open()
            img = shots[cur].frame(t)
            if dim:
                for d0, d1, s in dim:
                    if d0 <= t < d1:
                        k = min((t - d0) / 0.4, 1.0) * s
                        a = np.asarray(img, dtype=np.float32) * (1.0 - k)
                        img = Image.fromarray(a.astype(np.uint8))
            items = [(x.ov, x.alpha(t)) for x in texts]
            img = style.apply(img, items)
            enc.stdin.write(img.tobytes())
        if cur >= 0:
            shots[cur].close()
    finally:
        enc.stdin.close()
        enc.wait()
    return out_path
