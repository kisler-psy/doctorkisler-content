# Маска человека на фото (rembg). Первый запуск скачивает модель (~180 МБ) в ~/.u2net.
# usage: python -I run_seg.py <фото> <маска.png> [модель]   (модель по умолчанию isnet-general-use)
import sys

from PIL import Image
from rembg import new_session, remove

src, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "isnet-general-use"
im = Image.open(src).convert("RGB")
mask = remove(im, session=new_session(model), only_mask=True)
mask.save(out)
print(out, mask.size, mask.mode)
