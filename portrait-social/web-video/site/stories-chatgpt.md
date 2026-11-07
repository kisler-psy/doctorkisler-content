# Сайт Portrait: два коротких ролика «Мама» и «Папа»

Вопросы не задавай. Сделай всё по пунктам ниже, остальной сайт не меняй. Никаких заголовков, подписей и кнопок к роликам не добавляй: кнопка бесплатной пробы на сайте уже есть.

## 1. Файлы

Из прикреплённого архива `portrait-stories-site.zip` положи 12 файлов в папку сайта `assets/media/stories/` (имена не меняй):

- `mama-de.mp4`, `mama-cs.mp4`, `mama-ru.mp4`, `papa-de.mp4`, `papa-cs.mp4`, `papa-ru.mp4`
- обложки: `mama-de-poster.webp`, `mama-cs-poster.webp`, `mama-ru-poster.webp`, `papa-de-poster.webp`, `papa-cs-poster.webp`, `papa-ru-poster.webp`

Из того же архива положи в корень сайта (рядом с `media.js`) `stories-video.js` и `stories-video.css`. Их полный текст есть ниже, в пунктах 5 и 6.

## 2. Ролик «Мама»: сразу после первого экрана

В `index.html` найди `<section class="occasions wrap" aria-labelledby="occasions-title">`. Прямо ПЕРЕД ним вставь:

```html
<section class="story-video wrap" id="story-mama">
  <video class="story-video-player" data-story="mama" controls playsinline preload="none" width="720" height="900" poster="assets/media/stories/mama-de-poster.webp">
    <source src="assets/media/stories/mama-de.mp4" type="video/mp4">
  </video>
</section>
```

## 3. Ролик «Папа»: после образца подарка

В `index.html` найди `<section class="before-after-section">` (сразу после блока `id="example"`). Прямо ПЕРЕД ним вставь:

```html
<section class="story-video wrap" id="story-papa">
  <video class="story-video-player" data-story="papa" controls playsinline preload="none" width="720" height="900" poster="assets/media/stories/papa-de-poster.webp">
    <source src="assets/media/stories/papa-de.mp4" type="video/mp4">
  </video>
</section>
```

## 4. Подключение

В `<head>` после строки со `floating-trial.css` добавь:

```html
<link rel="stylesheet" href="stories-video.css?v=20261107">
```

Перед строкой `<script defer src="floating-trial.js?v=20261106"></script>` добавь:

```html
<script defer src="stories-video.js?v=20261107"></script>
```

## 5. Файл `stories-video.js` (полный текст)

```js
'use strict';
/* Short 4:5 story videos (Mama, Papa). Language follows the site's DE/CS/RU switch.
   Playback is always started by the visitor; only one video plays at a time. */
(() => {
  const players = [...document.querySelectorAll('video[data-story]')];
  if (!players.length) return;
  const languages = ['de', 'cs', 'ru'];
  const base = 'assets/media/stories/';
  // Browser translation can rewrite html.lang; the pressed language button stays authoritative.
  const language = () => {
    const picked = document.querySelector('[data-lang][aria-pressed="true"]')?.dataset.lang || document.documentElement.lang;
    return languages.includes(picked) ? picked : 'de';
  };
  let current = '';
  function apply() {
    const lang = language();
    if (lang === current) return;
    current = lang;
    players.forEach(video => {
      const name = video.dataset.story;
      const source = video.querySelector('source');
      const src = `${base}${name}-${lang}.mp4`;
      if (source.getAttribute('src') === src) return;
      video.pause();
      video.poster = `${base}${name}-${lang}-poster.webp`;
      source.setAttribute('src', src);
      video.load();
    });
  }
  apply();
  new MutationObserver(apply).observe(document.documentElement, {attributes: true, attributeFilter: ['lang']});
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => setTimeout(apply, 0)));
  document.addEventListener('visibilitychange', () => { if (document.hidden) players.forEach(video => video.pause()); });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (!entry.isIntersecting) entry.target.pause(); }), {threshold: 0});
    players.forEach(video => observer.observe(video));
  }
  const all = [...players, document.getElementById('portraitVideo')].filter(Boolean);
  all.forEach(video => video.addEventListener('play', () => all.forEach(other => { if (other !== video) other.pause(); })));
})();
```

## 6. Файл `stories-video.css` (полный текст)

```css
/* Short 4:5 story videos (Mama, Papa) */
.story-video{padding-top:clamp(32px,6vw,72px);padding-bottom:clamp(32px,6vw,72px)}
.story-video-player{display:block;margin:0 auto;width:100%;max-width:400px;height:auto;aspect-ratio:4/5;background:#f4f0e6;border-radius:6px;box-shadow:0 18px 40px rgba(52,46,43,.12)}
@media (max-width:760px){.story-video-player{max-width:340px}}
```

## 7. Чего не делать

- Не включать автозапуск и не убирать `preload="none"`: ролик запускается только по нажатию.
- Не трогать нынешний фильм `#portraitVideo` и `media.js`.
- Не включать русскую версию сайта. Русские ролики лежат на будущее, скрипт сам возьмёт их, когда русский язык вернётся.

## 8. Проверка перед ответом

- На DE после первого экрана ролик «Мама» с немецкой обложкой, после образца подарка ролик «Папа».
- После нажатия CS обложки и ролики сменились на чешские, после DE снова немецкие.
- Ролики играют на телефоне прямо на странице, пропорция 4:5, не растянуты.
- Когда запускаешь один ролик, другой и старый фильм ставятся на паузу.
