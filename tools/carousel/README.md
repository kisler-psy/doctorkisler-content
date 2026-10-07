# Генератор каруселей @doctorkisler

Рисует слайды Instagram-карусели (PNG 1080×1350) и сетку-превью `preview.png`. Тексты и фото каждой карусели лежат в её папке, движок общий.

## Что установить

- Node.js 18+ и npm, Python 3.10+.
- Зависимости (из корня репозитория):

```
npm --prefix tools/carousel ci
python3 -m pip install -r tools/carousel/requirements.txt
```

- Браузер для Playwright, если его ещё нет на машине: `npx --prefix tools/carousel playwright install chromium`.

## Сборка

Из корня репозитория:

```
npm --prefix tools/carousel run build -- carousels/2026-10-16_priznaki_igry
```

Команда рисует `slide_01.png … slide_NN.png` и `preview.png` в папке карусели и печатает проверку по каждому слайду: какими шрифтами отрисован текст и не вылез ли он за поля. Если есть замечания, они помечены «ПРОБЛЕМЫ», и команда завершается с ошибкой.

## Новая карусель

1. Создайте папку `carousels/<дата>_<тема>/source/`.
2. Скопируйте туда `slides.js` из прошлой карусели и замените тексты.
3. Положите в `source/` фото: `cover.jpg` (обложка 1080×1350, см. ниже) и `avatar.jpg` (квадрат для круглого фото у призыва). Без `cover.jpg` обложка будет с градиентом, без `avatar.jpg` призыв будет без фото.
4. Запустите сборку с новой папкой.

Поля слайдов в `slides.js`:

- `cover` — обложка: `title`, `titleBreakAfter` (слово, после которого перенос заголовка), `subtitle`, `note` (мелко внизу).
- `sign` — признак: `title`, `text`, `ill` (рисунок). Необязательно: `breakAfter` — список слов, после которых только и можно переносить пояснение; `keep` — сочетания, которые не разрывать.
- `final` — финал: `title`, `text`, `cta` (призыв), `keyword` (слово из призыва, выделяется), `note` (мелко внизу).

Рисунки — функции в `illustrations.js`: `phoneDown`, `moneyAway`, `calendarDebt`, `sleeplessClock`, `scoreboard`, `chaseLoop`, `stakesGrow`. Новый рисунок добавляется туда же (SVG 400×400).

Ширину строки, чтобы подобрать переносы: `node tools/carousel/measure.js "строка"` (заголовок Oswald 100 px) или `node tools/carousel/measure.js --inter "строка"` (пояснение Inter 42 px). Поле текста — 920 px, пояснение на признаках — до 840 px.

## Фото для обложки

Нужно отдельное окружение Python с rembg (первый запуск скачает модель ~180 МБ):

```
python3 -m venv tools/carousel/.venv
tools/carousel/.venv/bin/pip install -r tools/carousel/requirements-photo.txt
```

Дальше три шага (пути к фото подставьте свои):

```
cd tools/carousel
.venv/bin/python -I photo/run_seg.py фото.jpg маска.png
.venv/bin/python -I photo/cover_photo.py фото.jpg маска.png cover.jpg x0=90 y0=150 cw=800 top_solid=0.30 top_clear=0.52 top_alpha=0.55 wall_hue=22 wall_sat=0.19 wall_lift=0.52 exclude=300:480:290:470,920:1170:0:150
python3 photo/avatar.py cover.jpg avatar.jpg 514 846 560
```

1. `run_seg.py` делает маску человека.
2. `cover_photo.py` оставляет человека резким, а фон размывает, тонирует в тёплые тона и высветляет под заголовок. Параметры выше — для текущей обложки. Для нового снимка подберите кадр: `x0`, `y0` — левый верхний угол, `cw` — ширина (px исходника, кадр 4:5). Голова должна оказаться ниже заголовка. `exclude` — участки фона `y0:y1:x0:x1`, которые нужно убрать (картина, принтер).
3. `avatar.py` вырезает квадрат вокруг лица: центр лица и сторона квадрата в пикселях обложки.

Готовые `cover.jpg` и `avatar.jpg` положите в `source/` карусели. Исходные снимки в репозиторий не кладите: он публичный.

## Проверки

```
python3 tools/carousel/cmapcheck.py carousels/<папка>
python3 tools/carousel/inkcheck.py carousels/<папка>
```

- `cmapcheck.py` — все символы текстов есть в шрифтах Oswald и Inter, «квадратиков» не будет.
- `inkcheck.py` — размер 1080×1350 и зазоры между блоками на каждом слайде (на фото и градиентах приблизительно).
- Проверку шрифтов и полей печатает и сама сборка.
