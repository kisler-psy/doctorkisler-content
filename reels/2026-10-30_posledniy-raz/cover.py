# -*- coding: utf-8 -*-
"""Обложка ролика 7: фишки, красный свет, «ПОСЛЕДНИЙ РАЗ / САМАЯ ДОРОГАЯ СТАВКА»."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _rel in (("..", "..", "common"), ("..", "..", "tools", "reels")):
    _p = os.path.join(HERE, *_rel)
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
import cover
from PIL import Image

OUT = os.path.join(HERE, "..", "posledniy-raz-oblozhka.jpg")

if __name__ == "__main__":
    # кадрируем так, чтобы лицо игрока ушло выше текста
    img = Image.open(os.path.join(HERE, "p2-fishki.png")).convert("RGB")
    img = img.crop((40, 150, 1040, 1928 - 150)).resize((1080, 1920), Image.LANCZOS)
    cover.build(img, "ПОСЛЕДНИЙ РАЗ|*САМАЯ ДОРОГАЯ*|*СТАВКА*", OUT,
                size=112, y_center=1160, light=(0.72, 0.18), dark=0.5, seed=11)
    print(OUT)
