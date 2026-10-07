# Квадрат для круглого фото на финальном слайде: вырезаем из готовой обложки область вокруг лица.
# usage: python3 avatar.py <cover.jpg> <avatar.jpg> <cx> <cy> <d>
#   cx, cy — центр лица на обложке, d — сторона квадрата (px обложки 1080×1350)
import sys

from PIL import Image

src, out = sys.argv[1], sys.argv[2]
cx, cy, d = map(int, sys.argv[3:6])
im = Image.open(src).convert("RGB")
im.crop((cx - d // 2, cy - d // 2, cx + d // 2, cy + d // 2)).resize((320, 320), Image.LANCZOS).save(out, quality=94)
print(out, "320×320")
