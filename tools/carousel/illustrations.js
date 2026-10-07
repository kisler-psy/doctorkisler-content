// Линейные иллюстрации в стиле карусели: тонкая чёрная линия, кремовая заливка предметов,
// мягкий круг-подложка оттенка #B08A5A. Все рисунки в системе координат 400×400.
const INK = '#1C1A18';
const CREAM = '#E9DACA';
const TINT = '#D6BFA1'; // #B08A5A, разбавленный кремовым
const ACCENT = '#B08A5A';
const SW = 5; // толщина основной линии

const svg = (body, size = 400) =>
  `<svg viewBox="0 0 400 400" width="${size}" height="${size}" fill="none" stroke="${INK}" stroke-width="${SW}" ` +
  `stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
const disc = (cx, cy) => `<circle cx="${cx}" cy="${cy}" r="150" fill="${TINT}" stroke="none"/>`;

// 1. Телефон лежит экраном вниз и вибрирует
function phoneDown() {
  return svg(`
    ${disc(232, 196)}
    <g transform="rotate(-14 200 212)">
      <rect x="116" y="58" width="168" height="308" rx="34" fill="${CREAM}"/>
      <rect x="136" y="80" width="72" height="84" rx="20" fill="${CREAM}" stroke-width="4"/>
      <circle cx="158" cy="104" r="12" fill="${CREAM}" stroke-width="4"/>
      <circle cx="158" cy="140" r="12" fill="${CREAM}" stroke-width="4"/>
      <circle cx="188" cy="122" r="6" fill="${ACCENT}" stroke="none"/>
      <path d="M92 168V214M70 180V202"/>
      <path d="M308 226V272M330 238V260"/>
    </g>`);
}

// 2. Деньги уходят непонятно куда: купюры улетают из кошелька
function banknote(cx, cy, w, h, angle) {
  return `<g transform="rotate(${angle} ${cx} ${cy})">` +
    `<rect x="${cx - w / 2}" y="${cy - h / 2}" width="${w}" height="${h}" rx="8" fill="${CREAM}" stroke-width="4"/>` +
    `<circle cx="${cx}" cy="${cy}" r="${Math.round(h * 0.22)}" stroke-width="4"/>` +
    `<path d="M${cx - w / 2 + 14} ${cy}h10M${cx + w / 2 - 24} ${cy}h10" stroke-width="4"/></g>`;
}
function moneyAway() {
  return svg(`
    ${disc(214, 196)}
    ${banknote(318, 64, 100, 54, -8)}${banknote(246, 120, 120, 64, 12)}${banknote(168, 180, 132, 70, -16)}
    <path d="M292 116l18 8M362 96l16 4M226 54l14 8" stroke-width="4"/>
    <rect x="62" y="206" width="236" height="148" rx="24" fill="${CREAM}"/>
    <path d="M62 246H298" stroke-width="4"/>
    <rect x="232" y="262" width="88" height="54" rx="16" fill="${CREAM}"/>
    <circle cx="262" cy="289" r="8" fill="${ACCENT}" stroke="none"/>
    <text x="70" y="160" font-family="OswaldFS" font-weight="700" font-size="96" fill="${ACCENT}" stroke="none">?</text>`);
}

// 3. Всё чаще просит в долг: календарь с обведённым днём и монета
function calendarDebt() {
  const dots = [];
  for (const y of [184, 230, 276]) for (const x of [112, 162, 212, 262]) dots.push(`<circle cx="${x}" cy="${y}" r="6" fill="${INK}" stroke="none"/>`);
  return svg(`
    ${disc(204, 200)}
    <rect x="74" y="84" width="236" height="236" rx="26" fill="${CREAM}"/>
    <path d="M74 110a26 26 0 0 1 26-26h184a26 26 0 0 1 26 26v34H74Z" fill="${ACCENT}"/>
    <path d="M132 62V104M252 62V104" stroke-width="7"/>
    ${dots.join('')}
    <circle cx="262" cy="230" r="24" stroke="${INK}" stroke-width="4"/>
    <circle cx="306" cy="306" r="54" fill="${CREAM}"/>
    <circle cx="306" cy="306" r="38" stroke-width="3"/>
    <path d="M292 292l14-10v48" stroke-width="5"/>`);
}

// 4. Не спит и срывается: будильник показывает три часа ночи, рядом луна
function sleeplessClock() {
  return svg(`
    ${disc(200, 214)}
    <circle cx="122" cy="128" r="34" fill="${CREAM}"/>
    <circle cx="278" cy="128" r="34" fill="${CREAM}"/>
    <path d="M140 318L118 350M260 318L282 350" stroke-width="6"/>
    <circle cx="200" cy="228" r="108" fill="${CREAM}"/>
    <path d="M200 146v14M282 228h-14M200 310v-14M118 228h14" stroke-width="4"/>
    <path d="M200 228H254" stroke-width="7"/>
    <path d="M200 228V166" stroke-width="5"/>
    <circle cx="200" cy="228" r="9" fill="${ACCENT}" stroke="none"/>
    <path d="M78 94L64 80M70 124H52" stroke-width="4"/>
    <path d="M344.16 26A32 32 0 1 0 374.32 68.24A26 26 0 1 1 344.16 26Z" fill="${ACCENT}" stroke-width="4"/>
    <path d="M296 26v18M287 35h18" stroke-width="3"/>`);
}

// 5. Живёт в счёте матчей: табло со счётом и мяч
function scoreboard() {
  const pent = [-90, -18, 54, 126, 198].map((a) => a * Math.PI / 180);
  const pt = (r, a) => `${(306 + r * Math.cos(a)).toFixed(1)} ${(300 + r * Math.sin(a)).toFixed(1)}`;
  const pentagon = `M${pent.map((a) => pt(17, a)).join('L')}Z`;
  const spokes = pent.map((a) => `M${pt(17, a)}L${pt(50, a)}`).join('');
  return svg(`
    ${disc(200, 200)}
    <path d="M130 262V326M270 262V326" stroke-width="7"/>
    <rect x="54" y="104" width="292" height="164" rx="24" fill="${CREAM}"/>
    <rect x="78" y="128" width="244" height="116" rx="12" fill="${INK}" stroke="none"/>
    <text x="200" y="222" text-anchor="middle" font-family="OswaldFS" font-weight="700" font-size="88" letter-spacing="6" fill="${CREAM}" stroke="none">2:1</text>
    <circle cx="306" cy="300" r="50" fill="${CREAM}"/>
    <path d="${spokes}" stroke-width="4"/>
    <path d="${pentagon}" fill="${INK}" stroke-width="3"/>`);
}

// 6. «Надо отыграться»: замкнутый круг вокруг монеты с минусом
function chaseLoop() {
  return svg(`
    ${disc(200, 200)}
    <circle cx="200" cy="200" r="66" fill="${CREAM}"/>
    <circle cx="200" cy="200" r="48" stroke-width="3"/>
    <path d="M176 200H224" stroke="${ACCENT}" stroke-width="10"/>
    <path d="M89.1 159.6A118 118 0 0 1 302.2 141" stroke-width="6"/>
    <path d="M304.8 111.1L302.2 141L275 128.3" stroke-width="6"/>
    <path d="M310.9 240.4A118 118 0 0 1 97.8 259" stroke-width="6"/>
    <path d="M95.2 288.9L97.8 259L125 271.7" stroke-width="6"/>`);
}

// 7. Ставки растут: стопки монет становятся выше
function coin(cx, y, rx = 34, ry = 11, h = 14) {
  return `<path d="M${cx - rx} ${y}v${h}a${rx} ${ry} 0 0 0 ${2 * rx} 0v-${h}" fill="${CREAM}" stroke-width="4"/>` +
    `<ellipse cx="${cx}" cy="${y}" rx="${rx}" ry="${ry}" fill="${CREAM}" stroke-width="4"/>`;
}
function stack(cx, n, base = 332) {
  let s = '';
  for (let i = 0; i < n; i++) s += coin(cx, base - 14 - i * 14);
  return s;
}
function stakesGrow() {
  return svg(`
    ${disc(214, 200)}
    <path d="M24 346H376" stroke-width="4"/>
    ${stack(66, 1)}${stack(148, 3)}${stack(230, 6)}${stack(312, 10)}
    <path d="M52 250L120 206L196 156L292 60" />
    <path d="M248 60H292V104" />`);
}

module.exports = { phoneDown, moneyAway, calendarDebt, sleeplessClock, scoreboard, chaseLoop, stakesGrow };
