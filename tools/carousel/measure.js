// Ширина строк в пикселях, чтобы подобрать переносы.
// usage: node measure.js [--inter] [--size=N] "строка" ...
// По умолчанию Oswald Bold 100 px заглавными, как заголовки; --inter: Inter Regular, без заглавных.
// Поле текста на слайде — 920 px; пояснения на признаках — до 840 px.
const { FONT_CSS, loadPlaywright } = require('./common.js');

const args = process.argv.slice(2);
const inter = args.includes('--inter');
const sizeArg = args.find((a) => a.startsWith('--size='));
const size = sizeArg ? Number(sizeArg.split('=')[1]) : (inter ? 42 : 100);
const strings = args.filter((a) => !a.startsWith('--'));
const css = inter
  ? `font-family:'InterFS';font-weight:400;font-size:${size}px;`
  : `font-family:'OswaldFS';font-weight:700;font-size:${size}px;text-transform:uppercase;`;
const font = inter ? `400 ${size}px InterFS` : `700 ${size}px OswaldFS`;

(async () => {
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(`<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>${FONT_CSS}</style></head><body></body></html>`);
  const widths = await page.evaluate(async ({ strings, css, font }) => {
    const out = [];
    for (const s of strings) {
      await document.fonts.load(font, s.toUpperCase() + s); // догружаем нужные наборы символов
      const el = document.createElement('span');
      el.style.cssText = `${css}white-space:nowrap;position:absolute;left:0;top:0`;
      el.textContent = s;
      document.body.appendChild(el);
      out.push([s, Math.round(el.getBoundingClientRect().width)]);
      el.remove();
    }
    return out;
  }, { strings, css, font });
  for (const [s, w] of widths) console.log(`${w} px  ${s}`);
  await browser.close();
})();
