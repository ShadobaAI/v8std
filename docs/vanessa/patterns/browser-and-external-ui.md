---
id: vanessa:patterns:browser-and-external-ui
title: "Web-клиент, Chrome debug и внешние окна UI Automation"
description: "Отличия браузерного testing API, web socket, HTML-полей и Windows UI Automation; требования к идентификации окна и ограничения режима."
collection: "vanessa"
type: "pattern"
aliases: ["тестирование web клиента", "браузер Chrome debug", "UI Automation Inspector", "Windows SDK", "поле HTML документа", "внешние окна PID"]
tags: ["vanessa", "browser-and-external-ui", "тестирование web клиента", "браузер Chrome debug", "UI Automation Inspector"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/Браузер.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/UIAutomation/UIAutomation.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/index.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава08/КакТестироватьHTMLДокумент.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава11/ШагиДляРаботыСUIAutomation.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава14/ОписаниеПрямойРаботыСБраузером.MD"]
---

# Web-клиент, Chrome debug и внешние окна UI Automation

## Web-клиент 1С и произвольный сайт

Прямое управление браузером через VanessaExt и web socket отличается от TestClient 1С в опубликованной базе. Для произвольных сайтов документация описывает включение VanessaExt, Chrome debug и режима «Использовать браузер + web socket». Для web-клиента дополнительно нужны правильная публикация, тип подключения и доступность сервера; версии платформы менеджера и клиента должны совпадать.

Документация различает соединение с web-сервером файловой базы и сервером кластера серверной базы. Номера 1538/1541 приведены как типовые значения, а не доказательство адреса текущего окружения. Уникальность web-подключения определяется его именем.

## Профиль Chrome и фоновые вкладки

FAQ описывает для Chrome начиная с 136 необходимость `--user-data-dir` при использовании `--remote-debugging-port`. Отдельный профиль браузера является частью конфигурации этого режима. Кнопки настройки добавляют параметры против замедления фоновых/перекрытых вкладок:

```text
--remote-debugging-port=DEBUG_PORT
--user-data-dir=BROWSER_PROFILE_PATH
--disable-background-timer-throttling
--disable-renderer-backgrounding
--disable-backgrounding-occluded-windows
--disable-features=CalculateNativeWinOcclusion
```

Последний параметр в источнике относится к Windows. При уже существующем `--disable-features` список дополняется через запятую; повтор того же ключа оставляет только последнее значение. Это контракт указанного FAQ, не проверка совместимости любого будущего Chrome.

## Завершение и сброс

Закрытие вкладки крестиком с работающим web-клиентом может оставить сеанс на сервере; FAQ рекомендует штатный выход из приложения. Шаг сброса браузера может принудительно закрыть **все** процессы браузера текущего пользователя по имени, включая личные окна. Он отличается от закрытия текущего TestClient.

## UI Automation для внешних элементов

Microsoft UI Automation в описанных шагах работает под Windows. Цель определяется процессом, заголовком и типом элемента; Inspector из Windows SDK или аналог помогает исследовать эти свойства. PID внешнего процесса можно получить через VanessaExt; в профиле клиента также существуют данные его PID. Совпадения одного заголовка без установленного процесса недостаточно.

UIAutomation.md показывает получение ID по внутреннему имени элемента TestClient через VAExtension и дальнейший клик по ID. Для этого способа элемент должен поддерживать подсказку. Изменение заголовка может создать новый UIA-элемент и новый ID — такой ID не является вечным локатором.

## Поле HTML и ограничения источника

Урок версии 1.2.043.1 описывает ограниченность платформенного testing API для HTML-поля. Среди альтернатив — поддерживаемые действия VAExtension, специальное расширение либо поиск изображения с эмуляцией ввода. Это версионное описание, а не утверждение о любой платформе. Урок «Прямая работа с браузером» содержит только ссылку на видео: драйвер и сигнатуры из него в текстовом snapshot не извлечены.

Связанные темы: [файловые диалоги web](files-and-dialogs.md), [профили](test-client-profiles.md), [компоненты](external-components.md).

## Источники

[Браузер](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/Браузер.md); [UIAutomation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/UIAutomation/UIAutomation.md); [index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/index.md); [КакТестироватьHTMLДокумент](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава08/КакТестироватьHTMLДокумент.MD); [ШагиДляРаботыСUIAutomation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава11/ШагиДляРаботыСUIAutomation.MD); [ОписаниеПрямойРаботыСБраузером](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава14/ОписаниеПрямойРаботыСБраузером.MD).
