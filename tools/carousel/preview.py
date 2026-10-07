# Превью: все слайды карусели в одной сетке по 3 в ряд.
# usage: python3 preview.py <папка карусели>   (build.js запускает его сам)
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

d = sys.argv[1]
files = sorted(glob.glob(os.path.join(d, "slide_*.png")))
SCALE = 0.4
TW, TH = int(1080 * SCALE), int(1350 * SCALE)  # 432×540
GAP, PAD, COLS = 24, 48, 3
rows = math.ceil(len(files) / COLS)
W = PAD * 2 + TW * COLS + GAP * (COLS - 1)
H = PAD * 2 + TH * rows + GAP * (rows - 1)
sheet = Image.new("RGB", (W, H), "#FFFFFF")
draw = ImageDraw.Draw(sheet)
for k, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((TW, TH), Image.LANCZOS)
    r, c = divmod(k, COLS)
    x, y = PAD + c * (TW + GAP), PAD + r * (TH + GAP)
    sheet.paste(im, (x, y))
    draw.rectangle([x - 1, y - 1, x + TW, y + TH], outline="#D8CCBF", width=1)
sheet.save(os.path.join(d, "preview.png"), optimize=True)
print(f"preview.png {W}×{H}, слайдов: {len(files)}")
