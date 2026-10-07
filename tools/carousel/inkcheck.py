# Проверка по пикселям: размер 1080×1350, поля и зазоры между блоками (счётчик / текст / рисунок / подвал).
# Фон строки берётся с правого края слайда, поэтому на фото и градиентах зазоры приблизительные.
# usage: python3 inkcheck.py <папка карусели>
import glob
import os
import sys

from PIL import Image

d = sys.argv[1]
for f in sorted(glob.glob(os.path.join(d, "slide_*.png"))):
    im = Image.open(f).convert("RGB")
    assert im.size == (1080, 1350), (f, im.size)
    px = im.load()
    W, H = im.size
    rows = []
    for y in range(H):
        bg = px[W - 1, y]  # правый край всегда фон (поля 80 px)
        ink = [x for x in range(0, W, 2) if sum(abs(a - b) for a, b in zip(px[x, y], bg)) > 60]
        rows.append((min(ink), max(ink)) if ink else None)
    # склеиваем строки с «чернилами» в блоки (разрыв > 24 px — новый блок)
    blocks, cur = [], None
    for y, r in enumerate(rows):
        if r:
            if cur and y - cur[1] <= 24:
                cur = [cur[0], y, min(cur[2], r[0]), max(cur[3], r[1])]
            else:
                if cur:
                    blocks.append(cur)
                cur = [y, y, r[0], r[1]]
    blocks.append(cur)
    lefts = min(b[2] for b in blocks)
    rights = max(b[3] for b in blocks)
    desc = ", ".join(f"y{b[0]}–{b[1]}" for b in blocks)
    gaps = [blocks[k + 1][0] - blocks[k][1] for k in range(len(blocks) - 1)]
    print(f"{os.path.basename(f)}: x {lefts}–{rights} | блоки: {desc} | зазоры: {gaps}")
