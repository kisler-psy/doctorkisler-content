УСТАРЕЛ 3.11.2026: этот текст целиком вошёл в site-fixes-chatgpt.md (Заход 2, часть 3). ChatGPT отдавать только тот файл.

Внеси на сайт два события пикселя Meta для бесплатной пробы. Вопросы не задавай, сделай и пришли ссылку.

Зачем: реклама зовёт на бесплатную пробу, а пиксель сейчас отмечает только предзапись (Lead). Meta должна видеть, кто начал пробу и кто получил первую сцену.

## 1. meta-consent.js

Рядом с trackWaitlist добавь функцию trackTrial(stage, lang) по тем же правилам согласия:

- Работает только если allowed(). События, сделанные до согласия, потом не отправлять.
- Каждый stage отправляется не больше одного раза за загрузку страницы.
- Очередь как у pendingLeads: событие кладётся в очередь, вызывается startTracking(), отправка в flush() после PageView. В stopTracking() эту очередь тоже очищать.
- stage 'opened' → fbq('trackCustom', 'TrialOpened', {language: lang})
- stage 'scene' → fbq('track', 'StartTrial', {content_name: 'free_scene', language: lang, value: 0, currency: 'EUR'})
- В параметры событий не передавать ничего, кроме этого: ни имён, ни ответов, ни текста сцены, ни повода.

Экспорт: window.PortraitMeta = Object.freeze({trackWaitlist, trackTrial}).

## 2. app.js

- В startWizard, сразу после того как окно пробы открылось (после openDialog, только когда liveTest и проверка PortraitAI.check() прошла): try{window.PortraitMeta?.trackTrial('opened', language);}catch{}
- В generateScene, в ветке, где получена готовая сцена (target.aiResult=result; target.step=4): try{window.PortraitMeta?.trackTrial('scene', lang);}catch{}. При needs_detail и при ошибке событие не отправлять.

## 3. Политика конфиденциальности

На /privacy-de, /privacy-cs, /privacy-ru и в privacyBody в copy.js, в абзаце про пиксель Meta, замени описание того, что он измеряет:

- DE: «Es misst, ob jemand über unsere Werbung auf Facebook oder Instagram zu uns gekommen ist, die kostenlose Probe genutzt oder sich vorgemerkt hat. Deine Antworten und Texte werden dabei nicht an Meta übermittelt.»
- CS: «Měří, jestli někdo přišel přes naši reklamu na Facebooku nebo Instagramu, vyzkoušel ukázku zdarma nebo se zapsal. Tvoje odpovědi a texty se přitom do Mety neposílají.»
- RU: «Он показывает, пришёл ли человек из нашей рекламы в Facebook или Instagram, попробовал ли бесплатную пробу и записался ли он. Ваши ответы и тексты при этом в Meta не передаются.»

## 4. Ничего больше не меняй

Остальные тексты, дизайн, пробу и форму предзаписи не трогай. Событие Lead оставь как есть.

## 5. Проверка перед ответом

- До согласия и после «Отказаться» при открытии пробы нет запросов к facebook.com.
- После согласия: открыл пробу → уходит TrialOpened; получил сцену → уходит StartTrial. Повторное открытие на той же странице второй раз не отправляет.
- В запросах к facebook.com/tr нет текста ответов и имён.
- Предзапись по-прежнему отправляет Lead.
