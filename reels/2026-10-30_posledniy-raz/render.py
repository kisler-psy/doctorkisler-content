# -*- coding: utf-8 -*-
"""Ролик 7 «Последний раз - самая дорогая ставка», 30 октября."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _rel in (("..", "..", "common"), ("..", "..", "tools", "reels")):
    _p = os.path.join(HERE, *_rel)
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
import core
import style

OUT = os.path.join(HERE, "..", "posledniy-raz-reels.mp4")
HEYGEN = os.path.join(HERE, "heygen-rolik7.mp4")
P1 = os.path.join(HERE, "p1-klip-telefon-noch.mp4")
P2 = os.path.join(HERE, "p2-fishki.png")
P3 = os.path.join(HERE, "p3-utro-kofe.png")
DUR = 48.663

# центр лица аватара, доли кадра: зум идёт в эту точку, голова не уезжает
FACE = (0.496, 0.309)

T = {p["text"]: (p["t0"], p["t1"]) for p in
     json.load(open(os.path.join(HERE, "timings.json")))}
SUBS = json.load(open(os.path.join(HERE, "timings.json")))

# переносы, которые нельзя отдавать автомату: кавычки и связки
SUB_FIX = {
    2: "Кажется, что так|вы решаете остановиться.",
    3: "На самом деле|вы разрешаете себе сыграть ещё.",
    5: "Стоит сказать «последний раз»,|и оно сразу отпускает.",
    6: "Мозг запоминает:|эти слова помогают.",
}

CARD = DUR - 3.0          # последние 3 с - крупная карточка
SUB_END = CARD            # субтитры под карточку не лезут


def shots():
    return [
        # П1: лицо в свете телефона, первые 0,5 с клипа обрезаны
        core.Shot(0.00, 2.05, "video", P1, src_start=0.5,
                  zoom=(1.04, 1.11), anchor=(0.30, 0.45)),
        # аватар: базовый зум 1.15, на «сразу отпускает» ближе
        core.Shot(2.05, 24.27, "video", HEYGEN, src_start=2.05,
                  anchor=FACE,
                  zoom_at=[(2.05, 1.15), (17.2, 1.15), (18.2, 1.27),
                           (24.27, 1.27)]),
        # П2: фишки, медленное приближение
        core.Shot(24.27, 29.77, "image", P2,
                  zoom=(1.10, 1.22), anchor=(0.52, 0.56), pan=(0.0, 0.03)),
        # П3: утро, кофе и телефон
        core.Shot(29.77, 36.23, "image", P3,
                  zoom=(1.06, 1.17), anchor=(0.42, 0.55), pan=(0.03, 0.0)),
        # аватар до конца
        core.Shot(36.23, DUR, "video", HEYGEN, src_start=36.23,
                  anchor=FACE, zoom_at=[(36.23, 1.15), (DUR, 1.22)]),
    ]


def texts():
    out = []
    # субтитры по фразам: первую фразу закрывает крупный зачин,
    # последнюю - финальная карточка
    for i, p in enumerate(SUBS):
        if i == 0:
            continue
        t0, t1 = p["t0"], min(p["t1"], SUB_END)
        if t1 - t0 < 0.3:
            continue
        out.append(core.Text(t0, t1, fade=0.14,
                             text=SUB_FIX.get(i, p["text"]), size=56,
                             y_center=1420, max_lines=2, max_w=900,
                             darken=0.5, pad=110))
    # крупные заголовки
    out += [
        core.Text(0.00, 2.05, fade=0.18,
                  text="ПОСЛЕДНИЙ РАЗ|*— И ВСЁ*", size=112,
                  y_center=1300, max_lines=2, max_w=960),
        core.Text(7.04, 10.93, text="НЕ РЕШЕНИЕ,|*А РАЗРЕШЕНИЕ*", size=90,
                  y_top=1020, max_lines=2, max_w=940),
        core.Text(14.60, 18.49, text="НАПРЯЖЕНИЕ|*ОТПУСКАЕТ*", size=90,
                  y_top=1020, max_lines=2, max_w=940),
        core.Text(18.70, 21.48, text="МОЗГ *ЗАПОМИНАЕТ*", size=90,
                  y_top=1020, max_lines=2, max_w=940),
        core.Text(24.50, 29.60, text="ПОСЛЕДНЯЯ =|*САМАЯ КРУПНАЯ*", size=90,
                  y_top=1000, max_lines=2, max_w=940),
        core.Text(30.00, 36.10, text="РЕШАТЬ *УТРОМ*", size=104,
                  y_top=210, max_lines=1, max_w=940),
        core.Text(36.60, 43.12, text="УДАЛИТЬ ПРИЛОЖЕНИЕ|*ПОСТАВИТЬ ЛИМИТ*",
                  size=84, y_top=1020, max_lines=2, max_w=940),
        core.Text(CARD, DUR, fade=0.3,
                  text="ТЕСТ|*В ОПИСАНИИ ПРОФИЛЯ*", size=94,
                  y_center=1150, max_lines=2, max_w=980,
                  sub="анонимно, результат сразу", sub_size=48),
    ]
    return out


if __name__ == "__main__":
    core.render(OUT, shots(), texts(), HEYGEN, DUR,
                dim=[(CARD, DUR, 0.5)])
    print(OUT)
