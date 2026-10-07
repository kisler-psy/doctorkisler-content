# Проверка «квадратиков»: каждый символ текстов карусели есть в файлах шрифтов @fontsource.
# Тексты берутся из <папка карусели>/source/slides.js и надписей в illustrations.js.
# usage: python3 cmapcheck.py <папка карусели>
import json
import re
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FS = HERE / "node_modules" / "@fontsource"
slides_js = Path(sys.argv[1]).resolve() / "source" / "slides.js"
slides = json.loads(subprocess.check_output(
    ["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(slides_js)]))


def cmap(*files):
    out = set()
    for f in files:
        out |= set(TTFont(FS / f).getBestCmap())
    return out


osw = cmap("oswald/files/oswald-cyrillic-700-normal.woff2", "oswald/files/oswald-latin-700-normal.woff2")
inter = cmap("inter/files/inter-cyrillic-400-normal.woff2", "inter/files/inter-latin-400-normal.woff2")
NB = " "
n = len(slides)
# Oswald: заголовки (на слайдах заглавными), ключевое слово призыва, надписи в рисунках
labels = "".join(re.findall(r">([^<>]+)</text>", (HERE / "illustrations.js").read_text(encoding="utf-8")))
osw_text = "".join(s["title"].upper() + s.get("keyword", "") for s in slides) + labels + NB
# Inter: подзаголовки, пояснения, призыв, подписи внизу, ник и счётчики
inter_text = "".join(s.get(k, "") for s in slides for k in ("subtitle", "text", "cta", "note"))
inter_text += "@doctorkisler" + "".join(f"{i}/{n}" for i in range(1, n + 1)) + NB

ok = True
for name, text, codes in (("Oswald Bold", osw_text, osw), ("Inter Regular", inter_text, inter)):
    chars = set(text)
    missing = sorted(c for c in chars if ord(c) not in codes)
    ok &= not missing
    print(f"{name}: проверено {len(chars)} уникальных символов, без глифа: {''.join(missing) or 'нет'}")
sys.exit(0 if ok else 1)
