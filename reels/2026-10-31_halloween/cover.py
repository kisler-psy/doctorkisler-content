# -*- coding: utf-8 -*-
"""Обложка ролика 8: привидение в тапочках, «САМОЕ СТРАШНОЕ / УТРОМ ОТКРЫТЬ ТЕЛЕФОН»."""
import os
import subprocess
import sys
import io

HERE = os.path.dirname(os.path.abspath(__file__))
for _rel in (("..", "..", "common"), ("..", "..", "tools", "reels")):
    _p = os.path.join(HERE, *_rel)
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
import cover
from PIL import Image

OUT = os.path.join(HERE, "..", "halloween-oblozhka.jpg")


def frame(path, t):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
         "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGB")


if __name__ == "__main__":
    img = frame(os.path.join(HERE, "h5-klip-privedenie.mp4"), 2.4)
    cover.build(img, "САМОЕ СТРАШНОЕ|*УТРОМ ОТКРЫТЬ*|*ТЕЛЕФОН*", OUT,
                size=112, y_center=1070, light=(0.2, 0.3), dark=0.44, seed=5)
    print(OUT)
