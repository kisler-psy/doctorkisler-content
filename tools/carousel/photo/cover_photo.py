# Фото для обложки: человек резкий на переднем плане, фон за ним размыт и тонирован в тёплые тона,
# верх фона высветлен под заголовок. Ничего не ложится поверх человека.
# usage: python -I cover_photo.py <фото> <маска.png> <cover.jpg> [ключ=значение ...]
# Маску делает run_seg.py. Результат: JPEG 1080×1350, кладётся в <папка карусели>/source/cover.jpg.
import sys

import numpy as np
from PIL import Image
from pymatting import estimate_foreground_ml
from scipy.ndimage import gaussian_filter

src, mask_path, out = sys.argv[1:4]
P = dict(x0=90, y0=150, cw=800,          # кадр 4:5 в исходнике: левый край, верх, ширина (px исходника)
         blur=9.0,                       # размытие фона, px исходника
         top_solid=0.40, top_clear=0.62, top_alpha=0.92,  # высветление фона сверху (доли высоты кадра)
         light='#F2E4D7',                # цвет высветления (светлый фон образца)
         wall_sat=0.20, wall_lift=0.45, wall_hue=26,  # зелёная стена: насыщенность, светлота и тон после перекраски
         glow=0.55, gx=0.22, gy=0.10, gr=1.05,  # мягкий свет слева сверху (доля, центр, радиус в высотах кадра)
         exclude='')                     # участки фона, которые заменить соседней стеной: y0:y1:x0:x1,… (px исходника)
for kv in sys.argv[4:]:
    k, v = kv.split('=', 1)
    if k not in P:
        sys.exit(f'неизвестный параметр: {k}')
    P[k] = v if isinstance(P[k], str) else float(v)

I = np.asarray(Image.open(src).convert('RGB')).astype(np.float64) / 255
A = np.asarray(Image.open(mask_path).convert('L')).astype(np.float64) / 255
A = np.clip((A - 0.04) / 0.92, 0, 1)    # убираем «пыль» в маске

# 1) чистые цвета человека по краям (без примеси цвета стены в волосах)
F = estimate_foreground_ml(I, A)

# 2) фон без человека: нормированное размытие, дыру за человеком заполняем более крупным размытием
def nblur(img, w, s):
    num = np.stack([gaussian_filter(img[..., c] * w, s) for c in range(3)], -1)
    den = gaussian_filter(w, s)[..., None]
    return num / np.maximum(den, 1e-6), den[..., 0]
wbg = (1 - A) ** 2
# лишние предметы на фоне (картина, принтер) не берём в фон: дыры заполнятся соседней стеной
for zone in filter(None, P['exclude'].split(',')):
    ya, yb, xa, xb = map(int, zone.split(':'))
    wbg[ya:yb, xa:xb] = 0
B1, d1 = nblur(I, wbg, P['blur'])
B2, _ = nblur(I, wbg, P['blur'] * 6)
k = np.clip((d1 - 0.05) / 0.25, 0, 1)[..., None]
B = k * B1 + (1 - k) * B2

# 3) тонировка фона: зелёные обои -> тёплый беж, всё чуть светлее и теплее
def rgb2hsv(x):
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    mx, mn = x.max(-1), x.min(-1); d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    return np.stack([h * 60, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx], -1)
def hsv2rgb(x):
    h, s, v = x[..., 0] / 60, x[..., 1], x[..., 2]
    i = np.floor(h) % 6; f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    sel = [i == n for n in range(6)]
    r = np.select(sel, [v, q, p, p, t, v]); g = np.select(sel, [t, v, v, q, p, p]); b = np.select(sel, [p, p, t, v, v, q])
    return np.stack([r, g, b], -1)
hsv = rgb2hsv(B)
hue = hsv[..., 0]
w_green = np.clip(1 - np.abs(((hue - 100 + 180) % 360) - 180) / 80, 0, 1) ** 0.7  # вес «зелёности»
hsv[..., 0] = (1 - w_green) * hue + w_green * P['wall_hue']
hsv[..., 1] = (1 - w_green) * hsv[..., 1] + w_green * P['wall_sat']
hsv[..., 2] = (1 - w_green) * hsv[..., 2] + w_green * np.clip(P['wall_lift'] + 0.6 * hsv[..., 2], 0, 1)
# розово-красные тона (шторы) -> в золотисто-карамельные, как тёплые тона образца
hue = hsv[..., 0]
w_red = np.clip(1 - np.abs(((hue - 8 + 180) % 360) - 180) / 30, 0, 1)
hsv[..., 0] = (1 - w_red) * hue + w_red * 26
hsv[..., 1] = hsv[..., 1] * (1 + 0.10 * w_red)
B = hsv2rgb(hsv)
B = B * np.array([1.03, 1.0, 0.93])      # тёплый баланс
B = 0.10 + 0.90 * B                       # чуть приподнятые тени, мягче
B = np.clip(B, 0, 1)

# 4) человек: лёгкое тепло, без обесцвечивания
F = np.clip(F * np.array([1.025, 1.0, 0.955]), 0, 1)

# 5) кадр 4:5 и масштаб до 1080×1350
x0, y0, cw = int(P['x0']), int(P['y0']), int(P['cw'])
ch = round(cw * 1350 / 1080)
def crop(img): return img[y0:y0 + ch, x0:x0 + cw]
def to_out(img):
    arr = (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)
    return np.asarray(Image.fromarray(arr).resize((1080, 1350), Image.LANCZOS)).astype(np.float64) / 255
Fo, Bo = to_out(crop(F)), to_out(crop(B))
Ao = np.asarray(Image.fromarray((crop(A) * 255 + 0.5).astype(np.uint8)).resize((1080, 1350), Image.LANCZOS)).astype(np.float64)[..., None] / 255

# 6) мягкий свет слева сверху, как от окна на образце (только фон, человек поверх)
yy, xx = np.mgrid[0:1350, 0:1080] / 1350.0
r = np.sqrt((xx - P['gx'] * 1080 / 1350) ** 2 + (yy - P['gy']) ** 2) / P['gr']
t = np.clip(r, 0, 1)
glow = (P['glow'] * (1 - t * t * (3 - 2 * t)))[..., None]
# плюс ровная подсветка зоны заголовка, затухающая задолго до головы
t2 = np.clip((yy - P['top_solid']) / (P['top_clear'] - P['top_solid']), 0, 1)
top = (P['top_alpha'] * (1 - t2 * t2 * (3 - 2 * t2)))[..., None]
fade = 1 - (1 - glow) * (1 - top)
light = np.array([int(P['light'][i:i + 2], 16) for i in (1, 3, 5)]) / 255
Bo = Bo * (1 - fade) + light * fade

outimg = Fo * Ao + Bo * (1 - Ao)
Image.fromarray((np.clip(outimg, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out, quality=94, subsampling=0)
print(out, f"crop x {x0}-{x0 + cw}, y {y0}-{y0 + ch}")
