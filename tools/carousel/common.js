// Общее для build.js и measure.js: шрифты @fontsource (base64) и загрузка Playwright.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ---------- шрифты: Oswald Bold и Inter Regular, латиница и кириллица ----------
const FS = path.join(__dirname, 'node_modules/@fontsource');
const LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD';
const CYRILLIC = 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116';
function face(family, pkg, file, weight, range) {
  const b64 = fs.readFileSync(path.join(FS, pkg, 'files', file)).toString('base64');
  return `@font-face{font-family:'${family}';font-style:normal;font-weight:${weight};font-display:block;` +
    `src:url(data:font/woff2;base64,${b64}) format('woff2');unicode-range:${range};}`;
}
// Отдельные имена семейств, чтобы не подхватился системный Inter и сбой загрузки был заметен.
const FONT_CSS = [
  face('OswaldFS', 'oswald', 'oswald-cyrillic-700-normal.woff2', 700, CYRILLIC),
  face('OswaldFS', 'oswald', 'oswald-latin-700-normal.woff2', 700, LATIN),
  face('InterFS', 'inter', 'inter-cyrillic-400-normal.woff2', 400, CYRILLIC),
  face('InterFS', 'inter', 'inter-latin-400-normal.woff2', 400, LATIN),
].join('\n');

// ---------- Playwright: сначала локальный из node_modules, иначе глобальный ----------
function loadPlaywright() {
  try {
    return require('playwright');
  } catch {
    const globalRoot = execSync('npm root -g').toString().trim();
    return require(path.join(globalRoot, 'playwright'));
  }
}

module.exports = { FONT_CSS, loadPlaywright };
