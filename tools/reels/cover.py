# -*- coding: utf-8 -*-
"""Обложка 1080x1920: затемнённый кадр, красный свет, гранж-мазки, две строки."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import style

W, H = 1080, 1920


def darken(img, k=0.46):
    a = np.asarray(img, dtype=np.float32) * (1.0 - k)
    return Image.fromarray(a.astype(np.uint8))


def red_light(img, centre=(0.78, 0.22), radius=0.75, power=0.5):
    """Мягкий красный свет из угла кадра."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (x / W - centre[0])
    dy = (y / H - centre[1]) * (H / float(W))
    d = np.sqrt(dx * dx + dy * dy) / radius
    g = np.clip(1.0 - d, 0.0, 1.0) ** 2 * power
    a = np.asarray(img, dtype=np.float32)
    a[:, :, 0] = np.clip(a[:, :, 0] + g * 150, 0, 255)
    a[:, :, 1] = np.clip(a[:, :, 1] + g * 22, 0, 255)
    a[:, :, 2] = np.clip(a[:, :, 2] + g * 12, 0, 255)
    return Image.fromarray(a.astype(np.uint8))


def grunge(img, boxes, seed=7, alpha=0.86):
    """Рваные чёрные мазки под строками текста: края съедены шумом."""
    rng = np.random.default_rng(seed)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for x0, y0, x1, y1 in boxes:
        l = x0 - int(rng.integers(20, 50))
        r = x1 + int(rng.integers(20, 50))
        d.rectangle([l, y0 - int(rng.integers(4, 14)),
                     r, y1 + int(rng.integers(2, 12))], fill=255)
    # широкая мягкая кромка, чтобы шуму было что выгрызать
    m = np.asarray(mask.filter(ImageFilter.GaussianBlur(24)),
                   dtype=np.float32) / 255.0

    def noise(cell, blur):
        a = rng.random((max(2, H // cell), max(2, W // cell))).astype(np.float32)
        return np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                          .resize((W, H), Image.BICUBIC)
                          .filter(ImageFilter.GaussianBlur(blur)),
                          dtype=np.float32) / 255.0

    edge = noise(34, 6) * 0.62 + noise(11, 2) * 0.38
    torn = np.clip((m - edge * 0.78 - 0.10) * 3.4, 0.0, 1.0)
    # сухая кисть: часть строк пропускает краску
    streak = rng.random((H, 1)).astype(np.float32)
    streak = np.asarray(Image.fromarray((streak * 255).astype(np.uint8))
                        .resize((W, H), Image.BICUBIC)
                        .filter(ImageFilter.GaussianBlur(3)),
                        dtype=np.float32) / 255.0
    torn *= (0.80 + 0.20 * streak)
    torn = np.asarray(Image.fromarray((torn * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(1.6)),
                      dtype=np.float32) / 255.0
    a = np.asarray(img, dtype=np.float32)
    a *= (1.0 - torn * alpha)[:, :, None]
    return Image.fromarray(a.astype(np.uint8))


def build(bg, text, out, size=118, y_center=1120,
          light=(0.78, 0.22), dark=0.46, seed=7, max_w=960):
    img = Image.open(bg).convert("RGB") if isinstance(bg, str) else bg
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    img = red_light(darken(img, dark), centre=light)
    ov = style.make(text=text, size=size,
                    y_center=y_center, max_lines=4, max_w=max_w,
                    darken=0.0, shadow=0.85)
    # мазки только под строками
    x0, y0, x1, y1 = ov.box
    n = max(1, round((y1 - y0) / (size * 1.22)))
    step = (y1 - y0) / float(n)
    boxes = [(x0, int(y0 + i * step) + 6, x1, int(y0 + (i + 1) * step) - 2)
             for i in range(n)]
    img = grunge(img, boxes, seed=seed)
    img = style.apply(img, [(ov, 1.0)])
    img.save(out, quality=94, subsampling=0)
    return out
