Новых правок для сайта сейчас нет. Всё ниже уже внесено и проверено на живом сайте, этот файл в ChatGPT не отдавать.

# Архив: уже внесено

## Заход 2 · 3.11.2026 (на сайте, проверено 3.11.2026)

## Часть 1. Тексты, которые видят все посетители

Русскую версию не меняй. В пунктах 1 и 2 меняется только немецкий текст, русский и чешский блока «О создателях» оставь как есть.

### 1. DE · главная, блок «Über uns» (creators.p4 в editorial-copy.json)

Было: Diesen Satz höre ich bis heute in ihrer Stimme.
Стало: Diesen Satz habe ich bis heute mit ihrer Stimme im Ohr.

### 2. DE · главная, блок «Über uns» (creators.p5 в editorial-copy.json)

Было: Ich druckte sie mit Familienfotos auf Fotopapier und las sie meiner Mutter vor, vor Aufregung kam ich immer wieder ins Stocken. Sie schwieg lange, nur über ihre Wangen liefen Tränen.
Стало: Ich druckte sie mit Familienfotos auf Fotopapier und las sie meiner Mutter vor. Ich war so aufgeregt, dass ich immer wieder ins Stocken kam. Sie schwieg lange, nur die Tränen liefen ihr über die Wangen.

### 3. DE · образец для Мары, глава 07 «Ohne Spoiler» (sample.chapter.07.body в editorial-copy.json) и тот же текст в PDF-образце portrait-sample-de.pdf

Было: Man kann einen nahen Menschen immer weiter kennenlernen, selbst wenn man ihn schon sein ganzes Leben kennt.
Стало: Man kann einen Menschen, der einem nahesteht, immer weiter kennenlernen, selbst wenn man ihn schon sein ganzes Leben kennt.

### 4. DE · описание сайта для Google и превью ссылок (meta.description в editorial-copy.json)

Было: Für einen nahen Menschen – oder für dich selbst.
Стало: Für einen Menschen, der dir nahesteht – oder für dich selbst.

### 5. DE · окно бесплатной пробы, пример тона «Leicht und humorvoll» (tone.example.humorous в editorial-copy.json)

Было: Bei mir gab es Regen und keinen einzigen Schirm.
Стало: Es regnete, und ich hatte keinen einzigen Schirm.

### 6. CS · главная, вопрос «Dá se text upravit?» (faq.revision.a в editorial-copy.json)

Было: Chyby na naší straně opravíme vždy, nad rámec tohoto kola.
Стало: Chyby na naší straně opravíme vždy, i nad rámec tohoto kola.

### 7. CS · сбор воспоминаний, отправка ссылки на почту (resumeEmailHelp в ux-copy.json)

Было: Pošleme ti odkaz, abys mohl pokračovat na libovolném zařízení.
Стало: Pošleme ti odkaz, se kterým můžeš pokračovat na libovolném zařízení.

## Часть 2. Юридические страницы и раздел сбора воспоминаний

### 8. DE · /offer-de и /privacy-de: «Preisrecht» заменить на «Preisgarantie»

По-немецки «Preisrecht» значит «ценовое законодательство», а не «право на цену». Замени во всех 16 местах ниже. Род меняется (das → die), поэтому меняй ровно эти куски:

- /offer-de: «Sie umfasst die Anmeldung für eine E-Mail zum Start und das bestätigte Preisrecht.» → «Sie umfasst die Anmeldung für eine E-Mail zum Start und die bestätigte Preisgarantie.»
- /offer-de: «ist das Preisrecht bestätigt.» → «ist die Preisgarantie bestätigt.»
- /offer-de: «Das bestätigte Recht gilt nach Verkaufsstart einmal» → «Die bestätigte Preisgarantie gilt nach Verkaufsstart einmal»
- /offer-de: «Es handelt sich um ein Preisrecht für einen Kauf,» → «Es handelt sich um eine Preisgarantie für einen Kauf,»
- /offer-de: «Eine Abmeldung lässt dein bereits bestätigtes Preisrecht bestehen.» → «Eine Abmeldung lässt deine bereits bestätigte Preisgarantie bestehen.»
- /offer-de: «erzeugt kein zusätzliches Preisrecht.» → «erzeugt keine zusätzliche Preisgarantie.»
- /offer-de: «nicht als Verzicht auf das Preisrecht.» → «nicht als Verzicht auf die Preisgarantie.»
- /privacy-de: «Die Bestätigung und Verwaltung des von dir angeforderten Preisrechts ist» → «Die Bestätigung und Verwaltung der von dir angeforderten Preisgarantie ist»
- /privacy-de: «Eine Abmeldung hebt das bereits bestätigte Preisrecht nicht auf.» → «Eine Abmeldung hebt die bereits bestätigte Preisgarantie nicht auf.»
- /privacy-de: «Nach Ausstellung des Preisrechts werden» → «Nach Ausstellung der Preisgarantie werden»
- /privacy-de: «die Einwilligung und das Preisrecht auf der Hosting-Infrastruktur» → «die Einwilligung und die Preisgarantie auf der Hosting-Infrastruktur»
- /privacy-de: «damit ein bereits entstandenes Preisrecht nicht verloren geht» → «damit eine bereits erteilte Preisgarantie nicht verloren geht»
- /privacy-de: «ob bereits ein Preisrecht entstanden ist,» → «ob bereits eine Preisgarantie erteilt wurde,»
- /privacy-de: «und hebt das Preisrecht nicht auf.» → «und hebt die Preisgarantie nicht auf.»
- /privacy-de: «Das Preisrecht hat kein Ablaufdatum.» → «Die Preisgarantie hat kein Ablaufdatum.»
- /privacy-de: «verhindert doppelte Preisrechte;» → «verhindert doppelte Preisgarantien;»

### 9. DE · /privacy-de, раздел «Öffentlicher Generierungstest»

Было: Ein geschützter Code der IP-Adresse und ein Zähler begrenzen die Anfragen
Стало: Ein pseudonymisierter Prüfwert der IP-Adresse und ein Zähler begrenzen die Anfragen

### 10. CS · /privacy-cs, раздел «Veřejný test generování»

Было: Chráněný kód IP adresy a čítač omezují četnost požadavků
Стало: Pseudonymizovaná kontrolní hodnota IP adresy a čítač omezují četnost požadavků

### 11. DE · /privacy-de, раздел 7

Было: Auf der Website ist kein Brevo Tracker eingebunden
Стало: Auf der Website ist kein Brevo-Tracker eingebunden

### 12. DE · /privacy-de, раздел про письмо с готовым подарком

Было: den Zugriff auf die Geschenkseite und die PDF.
Стало: den Zugriff auf die Geschenkseite und das PDF.

### 13. DE · ux-copy.json (раздел сбора воспоминаний): «die PDF» → «das PDF»

На всём сайте «das PDF», здесь осталось «die PDF». Замени в этих ключах немецкой версии:

- readyHelp: «oder die PDF speichern.» → «oder das PDF speichern.»
- emailReadyHint: «und die PDF herunterladen kannst.» → «und das PDF herunterladen kannst.»
- emailFailed: «oder die PDF hier herunterladen.» → «oder das PDF hier herunterladen.»
- emailCooldown: «Dein Geschenk und die PDF sind hier verfügbar.» → «Dein Geschenk und das PDF sind hier verfügbar.»
- emailRateLimited: «Dein Geschenk und die PDF sind hier verfügbar.» → «Dein Geschenk und das PDF sind hier verfügbar.»
- emailPublishHint: «zur Seite mit der PDF.» → «zur Seite mit dem PDF.»

## Часть 3. Пиксель Meta для бесплатной пробы

Зачем: реклама зовёт на бесплатную пробу, а пиксель сейчас отмечает только предзапись (Lead). Meta должна видеть, кто начал пробу и кто получил первую сцену.

### 3.1 meta-consent.js

Рядом с trackWaitlist добавь функцию trackTrial(stage, lang) по тем же правилам согласия:

- Работает только если allowed(). События, сделанные до согласия, потом не отправлять.
- Каждый stage отправляется не больше одного раза за загрузку страницы.
- Очередь как у pendingLeads: событие кладётся в очередь, вызывается startTracking(), отправка в flush() после PageView. В stopTracking() эту очередь тоже очищать.
- stage 'opened' → fbq('trackCustom', 'TrialOpened', {language: lang})
- stage 'scene' → fbq('track', 'StartTrial', {content_name: 'free_scene', language: lang, value: 0, currency: 'EUR'})
- В параметры событий не передавать ничего, кроме этого: ни имён, ни ответов, ни текста сцены, ни повода.

Экспорт: window.PortraitMeta = Object.freeze({trackWaitlist, trackTrial}).

### 3.2 app.js

- В startWizard, сразу после того как окно пробы открылось (после openDialog, только когда liveTest и проверка PortraitAI.check() прошла): try{window.PortraitMeta?.trackTrial('opened', language);}catch{}
- В generateScene, в ветке, где получена готовая сцена (target.aiResult=result; target.step=4): try{window.PortraitMeta?.trackTrial('scene', lang);}catch{}. При needs_detail и при ошибке событие не отправлять.

### 3.3 Политика конфиденциальности

Замени абзацы про пиксель на /privacy-de, /privacy-cs, /privacy-ru и в privacyBody в copy.js. В чешской политике везде обращение на «вы», а абзац про пиксель написан на «ты», поэтому чешские абзацы меняются целиком.

DE · /privacy-de и privacyBody (de) в copy.js
Было: Es misst, ob jemand über unsere Werbung auf Facebook oder Instagram zu uns gekommen ist und sich vorgemerkt hat.
Стало: Es misst, ob jemand über unsere Werbung auf Facebook oder Instagram zu uns gekommen ist, den kostenlosen Test genutzt oder sich vorgemerkt hat. Deine Antworten und Texte werden dabei nicht an Meta übermittelt.

CS · /privacy-cs и privacyBody (cs) в copy.js
Было: Pixel Meta: Pixel společnosti Meta Platforms Ireland Ltd. načteme jen tehdy, když v liště souhlasíš. Měří, jestli někdo přišel přes naši reklamu na Facebooku nebo Instagramu a zapsal se. Právním základem je tvůj souhlas (čl. 6 odst. 1 písm. a GDPR). Souhlas můžeš kdykoli odvolat přes „Nastavení cookies“ v patičce.
Стало: Pixel Meta: Pixel společnosti Meta Platforms Ireland Ltd. načteme jen tehdy, když v liště souhlasíte. Měří, jestli někdo přišel přes naši reklamu na Facebooku nebo Instagramu, vyzkoušel bezplatný test nebo se zapsal. Vaše odpovědi a texty se přitom do Mety neposílají. Právním základem je váš souhlas (čl. 6 odst. 1 písm. a GDPR). Souhlas můžete kdykoli odvolat přes „Nastavení cookies“ v patičce.

CS · /privacy-cs и privacyBody (cs) в copy.js
Было: Tvůj souhlas nebo odmítnutí uložíme na šest kalendářních měsíců do místního úložiště prohlížeče (localStorage); poté tě znovu požádáme o rozhodnutí.
Стало: Váš souhlas nebo odmítnutí uložíme na šest kalendářních měsíců do místního úložiště prohlížeče (localStorage); poté vás znovu požádáme o rozhodnutí.

RU · /privacy-ru и privacyBody (ru) в copy.js
Было: Он показывает, пришёл ли человек из нашей рекламы в Facebook или Instagram и записался ли он.
Стало: Он показывает, пришёл ли человек из нашей рекламы в Facebook или Instagram, воспользовался ли бесплатной пробой и записался ли он. Ваши ответы и тексты при этом в Meta не передаются.

### 3.4 Ничего больше не меняй

Остальные тексты, дизайн, пробу и форму предзаписи не трогай. Событие Lead оставь как есть.

## Проверка перед ответом

Тексты:
- На живом сайте (рендер страницы, не исходники) ни одной строки из «Было» больше нет, все строки из «Стало» стоят на месте: главная DE и CS, /sample?lang=de после «Geschenk öffnen», окно бесплатной пробы DE (пример тона «Leicht und humorvoll»), /offer-de, /privacy-de, /privacy-cs, /privacy-ru.
- Слова «Preisrecht» на /offer-de и /privacy-de не осталось ни разу.
- В PDF-образце portrait-sample-de.pdf глава 07 содержит «einen Menschen, der einem nahesteht».
- В meta description немецкой главной стоит «Für einen Menschen, der dir nahesteht – oder für dich selbst.»
- Русская версия сайта не изменилась, кроме абзаца про пиксель в /privacy-ru.

Пиксель:
- До согласия и после «Отказаться» при открытии пробы нет запросов к facebook.com.
- После согласия: открыл пробу → уходит TrialOpened; получил сцену → уходит StartTrial. Повторное открытие на той же странице второй раз не отправляет.
- В запросах к facebook.com/tr нет текста ответов и имён.
- Предзапись по-прежнему отправляет Lead.


## Заход 1 · 2.11.2026 (на сайте, проверено 2.11.2026)

1. Образец «Дочь — маме», глава 03: «тяжесть мандаринов / Gewicht der Früchte / váhu ovoce» заменены на мандарины в карманах (RU/DE/CS, страница sample и PDF-образцы).
2. Второй образец «Муж — жене»: «снимать его / abmachen werde ich ihn nicht / sundat ho» заменены на «снимать оленя / den Elch mache ich nicht ab / losíka sundávat».
