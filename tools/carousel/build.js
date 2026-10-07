// Генератор слайдов карусели Instagram (1080×1350 PNG) и превью-сетки preview.png.
// usage: node build.js <папка карусели>   (или: npm run build -- <папка карусели>)
// В папке карусели нужен source/slides.js с текстами. Необязательно: source/cover.jpg — фото
// обложки 1080×1350 (без него обложка с градиентом), source/avatar.jpg — круглое фото у призыва.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { FONT_CSS, loadPlaywright } = require('./common.js');
const ILL = require('./illustrations.js');

const arg = process.argv[2];
if (!arg) {
  console.error('Укажите папку карусели: npm run build -- carousels/<папка>');
  process.exit(2);
}
// путь считаем от папки, из которой запущен npm (INIT_CWD), а не от tools/carousel
const DIR = path.resolve(process.env.INIT_CWD || process.cwd(), arg);
const SRC = path.join(DIR, 'source');
const slides = require(path.join(SRC, 'slides.js'));
const N = slides.length;
const optional = (f) => (fs.existsSync(path.join(SRC, f)) ? path.join(SRC, f) : null);
const COVER_IMG = optional('cover.jpg');
const AVATAR_IMG = optional('avatar.jpg');

const W = 1080;
const H = 1350;
const C = {
  cream: '#E9DACA',
  ink: '#1C1A18',
  brown: '#3A2A1C',
  accent: '#B08A5A',
};
// цвета плашки из образца
const PLATE = '#4B3520';
const PLATE_TEXT = '#F8EEE2';
// тёплый светлый фон внутренних слайдов: свет слева сверху, как на образце и обложке
const BG_SOFT = 'radial-gradient(120% 95% at 10% 4%, #F3E7DB 0%, #EEDDCB 52%, #E6D0BB 100%)';

// ---------- типографика ----------
const NB = ' ';
function ru(s, keep = []) {
  for (const k of keep) s = s.replace(k, k.replace(/ /g, NB));
  return s
    .replace(/(\d+\.?) /g, `$1${NB}`) // «1. Телефон», «7 признаков»
    .replace(/(?<=^|[\s«( ])([а-яёА-ЯЁ]{1,2}) /g, `$1${NB}`); // короткие слова не висят в конце строки
}
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const t = (s, keep) => esc(ru(s, keep));
// в пояснениях цитата «…» целиком остаётся на одной строке
const tb = (s, keep) => t(s.replace(/«[^»]*»/g, (q) => q.replace(/ /g, NB)), keep);

// ---------- оформление ----------
// Обложка без фото: кремовый держится в верхней трети, к низу плавно уходит в коричневый.
function coverGradient() {
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const a = hex(C.cream);
  const b = hex(C.brown);
  const from = 42;
  const stops = [`${C.cream} 0%`, `${C.cream} ${from}%`];
  for (let i = 1; i <= 16; i++) {
    const x = i / 16;
    const e = x * x * (3 - 2 * x); // smoothstep
    const c = a.map((v, k) => Math.round(v + (b[k] - v) * e));
    stops.push(`rgb(${c.join(',')}) ${(from + (100 - from) * x).toFixed(2)}%`);
  }
  return `linear-gradient(180deg, ${stops.join(', ')})`;
}
// Фото обложки уже обработано (photo/cover_photo.py): светлый верх под заголовок есть в самом фото.
const coverBg = COVER_IMG
  ? `url(data:image/jpeg;base64,${fs.readFileSync(COVER_IMG).toString('base64')}) center/cover no-repeat`
  : coverGradient();

const CSS = `
${FONT_CSS}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{width:${W}px;height:${H}px;overflow:hidden;background:${C.cream};color:${C.ink};
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;font-family:'InterFS'}
.slide{position:relative;width:${W}px;height:${H}px;overflow:hidden}
.counter{position:absolute;left:80px;top:80px;height:56px;padding:0 22px;border:2px solid ${C.ink};border-radius:16px;
  display:flex;align-items:center;font:400 26px/1 'InterFS';letter-spacing:.06em;color:${C.ink};font-variant-numeric:tabular-nums}
.footer{position:absolute;left:80px;right:80px;bottom:80px;height:76px;display:flex;align-items:center;gap:28px}
.note{flex:1;font:400 24px/1.3 'InterFS';color:${C.brown}}
.handle{font:400 24px/1 'InterFS';color:${C.brown};letter-spacing:.01em}
.arrow{flex:none;width:76px;height:76px;border:2px solid ${C.ink};border-radius:50%;display:flex;align-items:center;justify-content:center}
.arrow svg{display:block}
h1{margin:0;font-family:'OswaldFS';font-weight:700;text-transform:uppercase;color:${C.ink};text-wrap:balance}
.rule{width:120px;height:3px;background:${C.accent}}
.body{margin:0;font:400 42px/1.42 'InterFS';color:${C.brown};text-wrap:balance}
.nowrap{white-space:nowrap}

/* обложка */
.cover{background:${coverBg}}
.cover .head{position:absolute;left:80px;right:80px;top:176px}
.cover h1{font-size:96px;line-height:1.24;white-space:nowrap}
.cover .rule{margin:36px 0 28px}
.cover .sub{font:400 69px/1.2 'InterFS';color:${C.accent}}
.cover .note,.cover .handle{color:${COVER_IMG ? PLATE_TEXT : C.cream}}
.cover .arrow{border-color:${COVER_IMG ? PLATE_TEXT : C.cream}}
/* с фото: подписи и стрелка на тёмной плашке, как на образце */
.photo .footer{left:56px;right:56px;bottom:56px;height:124px;padding:0 24px 0 36px;background:${PLATE};border-radius:26px}
.photo .note{display:flex;align-items:center;gap:14px;font-size:26px}
.photo .note svg{flex:none;display:block}

/* слайды-признаки: текст сверху, рисунок справа внизу */
.sign,.final{background:${BG_SOFT}}
.sign .text{position:absolute;left:80px;right:80px}
.sign h1{font-size:96px;line-height:1.2}
.sign .rule{margin:40px 0 36px}
.sign .body{max-width:840px}
.sign .ill{position:absolute}
.sign .ill svg{display:block}
.sign .text{top:176px}
.sign .ill{right:80px;bottom:206px}

/* финал */
.final .content{position:absolute;left:80px;right:80px;top:170px;bottom:190px;display:flex;flex-direction:column;justify-content:center}
.final h1{font-size:96px;line-height:1.2}
.final .rule{margin:40px 0 36px}
.final .body{max-width:880px}
/* призыв на тёмной плашке, как на обложке и образце, с фото автора */
.final .cta{margin-top:56px;display:flex;align-items:center;gap:32px;background:${PLATE};border-radius:28px;
  padding:30px 40px 30px 30px;font:400 38px/1.36 'InterFS';color:${PLATE_TEXT};text-wrap:balance}
.final .cta img{flex:none;display:block;width:150px;height:150px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px ${PLATE_TEXT}}
.final .kw{font-family:'OswaldFS';font-weight:700;font-size:42px;letter-spacing:.02em;color:#E3B583}
`;

const arrowSvg = (color) =>
  `<svg width="30" height="30" viewBox="0 0 30 30" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">` +
  `<path d="M4 15H26"/><path d="M18 7L26 15L18 23"/></svg>`;

function footer(i, s) {
  const last = i === N - 1;
  const onDark = s.type === 'cover';
  const note = s.note
    ? `<div class="note">${t(s.note).replace('DSM-5', '<span class="nowrap">DSM-5</span>')}</div>`
    : '<div class="note"></div>';
  const light = COVER_IMG ? PLATE_TEXT : C.cream;
  const arrow = last ? '' : `<div class="arrow">${arrowSvg(onDark ? light : C.ink)}</div>`;
  if (onDark && COVER_IMG) {
    const mark = `<svg width="22" height="28" viewBox="0 0 22 28" fill="none" stroke="${light}" stroke-width="2" stroke-linejoin="round"><path d="M2 2H20V26L11 19.5L2 26Z"/></svg>`;
    return `<div class="footer"><div class="note">${mark}<span>${t(s.note)}</span></div><div class="handle">@doctorkisler</div>${arrow}</div>`;
  }
  return `<div class="footer">${note}<div class="handle">@doctorkisler</div>${arrow}</div>`;
}

function slideHtml(i) {
  const s = slides[i];
  const counter = `<div class="counter">${i + 1}/${N}</div>`;
  let inner = '';
  if (s.type === 'cover') {
    const k = s.title.indexOf(s.titleBreakAfter) + s.titleBreakAfter.length;
    const title = `${t(s.title.slice(0, k))}<br>${t(s.title.slice(k).trim())}`;
    inner = `<div class="head"><h1>${title}</h1><div class="rule"></div><div class="sub">${t(s.subtitle)}</div></div>`;
  } else if (s.type === 'sign') {
    if (s.ill && !ILL[s.ill]) throw new Error(`Нет рисунка «${s.ill}» в illustrations.js`);
    const ill = s.ill ? `<div class="ill">${ILL[s.ill]().replace(/width="400" height="400"/, 'width="440" height="440"')}</div>` : '';
    // breakAfter: строки рвутся только после указанных слов, остальные пробелы неразрывные
    const body = s.breakAfter
      ? s.breakAfter.reduce((acc, w) => acc.replace(`${w} `, `${w}\n`), s.text).split('\n').map((seg) => esc(seg.replace(/ /g, NB))).join('<br>')
      : tb(s.text, s.keep);
    inner = `${ill}<div class="text"><h1>${t(s.title)}</h1><div class="rule"></div><p class="body">${body}</p></div>`;
  } else {
    const cta = t(s.cta).replace(s.keyword, `<span class="kw">${s.keyword}</span>`);
    const avatar = AVATAR_IMG ? `<img src="data:image/jpeg;base64,${fs.readFileSync(AVATAR_IMG).toString('base64')}" alt="">` : '';
    inner = `<div class="content"><h1>${t(s.title)}</h1><div class="rule"></div><p class="body">${tb(s.text)}</p><div class="cta">${avatar}<span>${cta}</span></div></div>`;
  }
  return `<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>${CSS}</style></head>` +
    `<body><div class="slide ${s.type}${s.type === 'cover' && COVER_IMG ? ' photo' : ''}">${counter}${inner}${footer(i, s)}</div></body></html>`;
}

// ---------- проверка шрифтов через DevTools: какими шрифтами реально отрисован каждый текстовый узел ----------
async function fontReport(page) {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
  const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: '.slide, .slide *' });
  const used = {};
  for (const nodeId of nodeIds) {
    const { fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId });
    for (const f of fonts) {
      const key = `${f.familyName}${f.isCustomFont ? ' (web font)' : ' (СИСТЕМНЫЙ)'}`;
      used[key] = (used[key] || 0) + f.glyphCount;
    }
  }
  await cdp.detach();
  return used;
}

(async () => {
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const summary = [];
  for (let i = 0; i < N; i++) {
    const html = slideHtml(i);
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const loaded = await page.evaluate(() =>
      [...document.fonts].map((f) => `${f.family} ${f.weight} ${f.status}`));
    const report = await fontReport(page);
    // геометрия: текст не вылезает за поля 80 px и не наезжает на подвал и рисунок
    const geo = await page.evaluate(() => {
      const box = (sel) => {
        const els = [...document.querySelectorAll(sel)];
        if (!els.length) return null;
        const rs = els.flatMap((e) => { const g = document.createRange(); g.selectNodeContents(e); return [...g.getClientRects(), e.getBoundingClientRect()]; });
        return {
          top: Math.round(Math.min(...rs.map((r) => r.top))), bottom: Math.round(Math.max(...rs.map((r) => r.bottom))),
          left: Math.round(Math.min(...rs.map((r) => r.left))), right: Math.round(Math.max(...rs.map((r) => r.right))),
        };
      };
      const lines = (sel) => {
        const e = document.querySelector(sel); if (!e) return 0;
        const g = document.createRange(); g.selectNodeContents(e);
        return new Set([...g.getClientRects()].map((r) => Math.round(r.bottom))).size;
      };
      return {
        content: box('h1, .rule, .body, .sub, .cta'), footer: box('.footer'),
        ill: (() => { const e = document.querySelector('.ill svg'); if (!e) return null; const r = e.getBoundingClientRect(); return { top: r.top, bottom: r.bottom, left: r.left, right: r.right }; })(),
        textRects: [...document.querySelectorAll('h1, .body')].flatMap((e) => { const g = document.createRange(); g.selectNodeContents(e); return [...g.getClientRects()].map((r) => ({ top: r.top, bottom: r.bottom, left: r.left, right: r.right })); }),
        h1Lines: lines('h1'), bodyLines: lines('.body'),
      };
    });
    const problems = [];
    if (geo.content.left < 80 || geo.content.right > W - 80) problems.push('текст выходит за поля');
    if (geo.content.bottom > geo.footer.top - 40) problems.push('текст близко к подвалу');
    if (geo.ill) {
      const hit = geo.textRects.some((r) => r.left < geo.ill.right && r.right > geo.ill.left && r.top < geo.ill.bottom && r.bottom > geo.ill.top);
      if (hit) problems.push('текст наезжает на рисунок');
      if (geo.ill.bottom > geo.footer.top - 30) problems.push('рисунок близко к подвалу');
    }
    if (Object.keys(report).some((k) => k.includes('СИСТЕМНЫЙ'))) problems.push('часть текста нарисована системным шрифтом');
    const file = path.join(DIR, `slide_${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: file, clip: { x: 0, y: 0, width: W, height: H } });
    summary.push({ file: path.basename(file), fonts: report, faces: loaded, geo, problems });
  }
  await browser.close();
  for (const s of summary) {
    const g = s.geo;
    console.log(`${s.file}: шрифты ${JSON.stringify(s.fonts)} | faces ${s.faces.filter((f) => f.endsWith('loaded')).length}/${s.faces.length} loaded` +
      ` | заголовок ${g.h1Lines} стр., текст ${g.bodyLines} стр. | контент y ${g.content.top}–${g.content.bottom}, x ${g.content.left}–${g.content.right}` +
      ` | ${s.problems.length ? 'ПРОБЛЕМЫ: ' + s.problems.join('; ') : 'ок'}`);
  }
  // превью-сетка из готовых слайдов
  execFileSync(process.env.PYTHON || 'python3', [path.join(__dirname, 'preview.py'), DIR], { stdio: 'inherit' });
  if (summary.some((s) => s.problems.length)) {
    console.error('Есть замечания к вёрстке, смотрите строки «ПРОБЛЕМЫ» выше.');
    process.exitCode = 1;
  }
})();
