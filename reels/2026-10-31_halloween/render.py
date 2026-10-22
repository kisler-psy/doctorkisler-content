# -*- coding: utf-8 -*-
"""Ролик 8 «Хеллоуин», 31 октября."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _rel in (("..", "..", "common"), ("..", "..", "tools", "reels")):
    _p = os.path.join(HERE, *_rel)
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
import core

OUT = os.path.join(HERE, "..", "halloween-reels.mp4")
HEYGEN = os.path.join(HERE, "heygen-rolik8.mp4")
H1 = os.path.join(HERE, "h1-tykva-skelet.png")
H2 = os.path.join(HERE, "h2-klip-ruka-telefon.mp4")
H3 = os.path.join(HERE, "h3-poet-v-telefon.png")
H4 = os.path.join(HERE, "h4-glaza-dveri.png")
H5 = os.path.join(HERE, "h5-klip-privedenie.mp4")

VOICE = 35.48
DUR = VOICE + 3.0          # три секунды карточки после голоса
CARD = VOICE

FACE = (0.519, 0.292)      # центр лица старика

SUBS = json.load(open(os.path.join(HERE, "timings.json")))

# красным выделяем то, на чём держится шутка
RED = {
    5: "*Три раза.*",
    7: "*С песней.*",
    8: "А в чат нашего дома написал: *«Соседи, я вас всех люблю!»*",
}


def shots():
    return [
        core.Shot(0.00, 2.73, "video", HEYGEN, src_start=0.0,
                  anchor=FACE, zoom=(1.10, 1.13)),
        # Х1 тыква и скелет
        core.Shot(2.73, 6.43, "image", H1,
                  zoom=(1.05, 1.15), anchor=(0.47, 0.42)),
        # Х2 рука тянется к телефону утром
        core.Shot(6.43, 10.65, "video", H2, src_start=0.3,
                  zoom=(1.03, 1.11), anchor=(0.55, 0.60)),
        # старик, на «Три раза» резкое приближение
        core.Shot(10.65, 15.66, "video", HEYGEN, src_start=10.65,
                  anchor=FACE,
                  zoom_at=[(10.65, 1.10), (14.55, 1.10), (14.82, 1.32),
                           (15.66, 1.34)]),
        # Х3 поёт в телефон
        core.Shot(15.66, 19.87, "image", H3,
                  zoom=(1.04, 1.14), anchor=(0.45, 0.38)),
        core.Shot(19.87, 24.40, "video", HEYGEN, src_start=19.87,
                  anchor=FACE, zoom=(1.10, 1.17)),
        # Х4 соседи в щелях дверей
        core.Shot(24.40, 27.35, "image", H4,
                  zoom=(1.03, 1.13), anchor=(0.50, 0.32)),
        core.Shot(27.35, 31.87, "video", HEYGEN, src_start=27.35,
                  anchor=FACE, zoom=(1.10, 1.17)),
        # Х5 привидение в тапочках, держим до конца карточки
        core.Shot(31.87, DUR, "video", H5, src_start=0.0, zoom=(1.0, 1.0)),
    ]


def texts():
    out = []
    for i, p in enumerate(SUBS):
        if i == 0:                      # первую фразу закрывает крупный зачин
            continue
        out.append(core.Text(p["t0"], p["t1"], fade=0.14,
                             text=RED.get(i, p["text"]), size=56,
                             y_center=1420, max_lines=2, max_w=900,
                             darken=0.5, pad=110))
    out += [
        core.Text(0.00, 2.73, fade=0.18,
                  text="САМОЕ СТРАШНОЕ|*В ХЕЛЛОУИН*", size=104,
                  y_top=1020, max_lines=2, max_w=960),
        core.Text(CARD, DUR, fade=0.3,
                  text="САМОЕ СТРАШНОЕ|В ХЕЛЛОУИН —|*УТРОМ ОТКРЫТЬ*|*СВОИ СООБЩЕНИЯ*",
                  size=80, y_center=1040, max_lines=4, max_w=960,
                  sub="ТЕСТ AUDIT — В ОПИСАНИИ ПРОФИЛЯ", sub_size=44),
    ]
    return out


if __name__ == "__main__":
    core.render(OUT, shots(), texts(), HEYGEN, DUR, dim=[(CARD, DUR, 0.5)])
    print(OUT)
