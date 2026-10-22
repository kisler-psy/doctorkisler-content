# -*- coding: utf-8 -*-
"""Надписи для рилсов: узкий жирный капс, без плашек, мягкое затемнение.

Разметка текста: кусок в *звёздочках* печатается красным.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/opt/fonts/Oswald-VF.ttf"
WHITE = (248, 248, 248)
RED = (244, 52, 28)
W, H = 1080, 1920

_cache = {}


def font(size, weight=700):
    key = (size, weight)
    if key not in _cache:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_axes([weight])
        _cache[key] = f
    return _cache[key]


def runs(text):
    """Разбор разметки *красное* -> [(кусок, цвет), ...]"""
    out, red = [], False
    for part in text.split("*"):
        if part:
            out.append((part, RED if red else WHITE))
        red = not red
    return out


def _words(text):
    """Слова с пометкой цвета, пробелы сохраняются."""
    out = []
    for chunk, col in runs(text):
        pieces = chunk.split(" ")
        for i, p in enumerate(pieces):
            if p:
                out.append([p, col])
            elif i and out:
                pass
    return out


# предлоги и союзы, которые нельзя оставлять в конце строки
HANGING = set("""а и но или да же бы ли в во на за по до из от к ко с со у о об обо
про для при над под перед между без через что как чем чтобы если когда то не ни""".split())


def wrap(text, fnt, max_w, max_lines=3):
    """Перенос по словам. Вертикальная черта в тексте - жёсткий перенос,
    висячие предлоги уводим на следующую строку.
    Возвращает None, если не помещается: тогда уменьшаем кегль."""
    dummy = Image.new("L", (8, 8))
    d = ImageDraw.Draw(dummy)

    def width(ws):
        return d.textlength(" ".join(w[0] for w in ws), font=fnt)

    forced = [t for t in text.split("|") if t.strip()]
    if len(forced) > 1:
        lines = []
        for part in forced:
            got = wrap(part, fnt, max_w, max_lines)
            if got is None:
                return None
            lines += got
        return lines if len(lines) <= max_lines else None

    words = _words(text)
    if not words:
        return []
    for n in range(1, max_lines + 1):
        lines = _split(words, n, width, max_w, d, fnt)
        if lines is not None:
            return lines
    return None


def _split(words, n, width, max_w, d, fnt):
    """Разложить слова на n строк примерно поровну, не шире max_w."""
    if n == 1:
        return [words] if width(words) <= max_w else None
    total = width(words)
    if total / n > max_w:
        return None
    lines, cur = [], []
    target = total / n
    for i, w in enumerate(words):
        cand = cur + [w]
        rest = len(words) - i - 1
        need = n - len(lines) - 1
        if cur and (width(cand) > max_w or
                    (width(cand) > target * 1.12 and rest >= need and len(lines) < n - 1)):
            lines.append(cur)
            cur = [w]
        else:
            cur = cand
        if len(lines) == n - 1:
            cur = cur + words[i + 1:]
            break
    lines.append(cur)
    if len(lines) != n or any(width(l) > max_w for l in lines):
        return None
    lines = _fix_hanging(lines, width, max_w)
    if any(width(l) > max_w for l in lines):
        return None
    return lines


def _fix_hanging(lines, width, max_w):
    """Висячий предлог в конце строки переносим вниз."""
    for i in range(len(lines) - 1):
        while len(lines[i]) > 1 and lines[i][-1][0].lower().strip("«»,.!?:;—") in HANGING:
            moved = lines[i].pop()
            lines[i + 1].insert(0, moved)
            if width(lines[i + 1]) > max_w:
                lines[i + 1].pop(0)
                lines[i].append(moved)
                break
    return lines


def _radial(box, strength=0.62, pad=130):
    """Мягкое радиальное затемнение под текстом: массив 0..strength."""
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(W, x1 + pad), min(H, y1 + pad)
    if x1 <= x0 or y1 <= y0:
        return np.zeros((H, W), dtype=np.float32)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([x0 - pad // 2, y0, x1 + pad // 2, y1], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(pad * 0.75))
    return np.asarray(mask, dtype=np.float32) / 255.0 * strength


class Overlay(object):
    """Готовый слой надписи: текст с тенью и карта затемнения под ним."""

    def __init__(self, rgba, dark, box):
        self.rgba = rgba
        self.dark = dark
        self.box = box


def make(text, size, y_top=None, y_center=None, max_lines=3, max_w=950,
         gap=0.22, darken=0.62, weight=700, sub=None, sub_size=None,
         shadow=0.78, pad=130):
    """Собрать слой надписи один раз, дальше класть его на кадры."""
    size_now = size
    while True:
        fnt = font(size_now, weight)
        lines = wrap(text, fnt, max_w, max_lines)
        if lines is not None or size_now <= 34:
            break
        size_now -= 4
    if not lines:
        return None
    size = size_now
    lh = int(size * (1.0 + gap))
    ssize = sub_size or int(size * 0.42)
    sub_lines = []
    total_h = lh * len(lines)
    if sub:
        while ssize > 24:
            sfnt = font(ssize, 500)
            sub_lines = wrap(sub, sfnt, max_w, 2)
            if sub_lines is not None:
                break
            ssize -= 3
        sub_lines = sub_lines or []
        total_h += int(size * 0.18) + int(ssize * 1.3) * len(sub_lines)
    y = int(y_center - total_h / 2) if y_center is not None else int(y_top)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0b, x1b = W, 0
    cy = y
    for ln in lines:
        txt = " ".join(w[0] for w in ln)
        tw = d.textlength(txt, font=fnt)
        x = (W - tw) / 2.0
        x0b, x1b = min(x0b, int(x)), max(x1b, int(x + tw))
        for word, col in ln:
            d.text((x, cy), word, font=fnt, fill=col + (255,))
            x += d.textlength(word + " ", font=fnt)
        cy += lh
    if sub_lines:
        sfnt = font(ssize, 500)
        cy += int(size * 0.18)
        for ln in sub_lines:
            txt = " ".join(w[0] for w in ln)
            tw = d.textlength(txt, font=sfnt)
            x = (W - tw) / 2.0
            x0b, x1b = min(x0b, int(x)), max(x1b, int(x + tw))
            for word, col in ln:
                d.text((x, cy), word, font=sfnt, fill=col + (255,))
                x += d.textlength(word + " ", font=sfnt)
            cy += int(ssize * 1.3)

    box = (x0b, y, x1b, cy)
    if shadow:
        sh = layer.split()[3].filter(ImageFilter.GaussianBlur(9))
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        base.putalpha(sh.point(lambda v: int(v * shadow)))
        layer = Image.alpha_composite(base, layer)
    dark = _radial(box, darken, pad) if darken else np.zeros((H, W), dtype=np.float32)
    return Overlay(layer, dark, box)


def apply(img, items):
    """Положить слои (overlay, прозрачность) на кадр."""
    items = [(o, a) for o, a in items if o is not None and a > 0.004]
    if not items:
        return img
    a = np.asarray(img, dtype=np.float32)
    dark = np.zeros((H, W), dtype=np.float32)
    for o, op in items:
        dark = np.maximum(dark, o.dark * op)
    a *= (1.0 - dark)[:, :, None]
    out = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    for o, op in items:
        lay = o.rgba
        if op < 0.999:
            lay = lay.copy()
            lay.putalpha(lay.split()[3].point(lambda v: int(v * op)))
        out = Image.alpha_composite(out, lay)
    return out.convert("RGB")
