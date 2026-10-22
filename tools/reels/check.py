# -*- coding: utf-8 -*-
"""Лист кадров с надписями: начало и конец каждой надписи плюс детектор лиц."""
import io
import subprocess
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

CAS = cv2.CascadeClassifier(cv2.data.haarcascades +
                            "haarcascade_frontalface_default.xml")


def frame(video, t):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", video,
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGB")


def faces(img):
    g = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    return [list(map(int, r)) for r in
            CAS.detectMultiScale(g, 1.08, 6, minSize=(110, 110))]


def sheet(video, marks, out, cols=6, tile=250):
    """marks - [(время, подпись)]; рисуем зоны текста и найденные лица."""
    tiles, report = [], []
    for t, label in marks:
        im = frame(video, t)
        fs = faces(im)
        d = ImageDraw.Draw(im)
        for x, y, w, h in fs:
            d.rectangle([x, y, x + w, y + h], outline=(0, 230, 255), width=7)
        d.line([(0, 1500), (1080, 1500)], fill=(255, 70, 70), width=5)
        d.line([(0, 1000), (1080, 1000)], fill=(90, 255, 120), width=3)
        report.append((t, label, fs))
        th = int(tile * 1920 / 1080)
        tiles.append((label, t, im.resize((tile, th))))
    th = int(tile * 1920 / 1080)
    rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (tile * cols, (th + 22) * rows), "black")
    f = ImageFont.load_default(15)
    for i, (label, t, im) in enumerate(tiles):
        x, y = tile * (i % cols), (th + 22) * (i // cols)
        sh.paste(im, (x, y + 22))
        ImageDraw.Draw(sh).text((x + 4, y + 3), "%.1f %s" % (t, label),
                                font=f, fill="white")
    sh.save(out, quality=92)
    return report
