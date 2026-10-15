---
id: vanessa:patterns:onboarding-and-embedded-run
title: "Интерактивная справка, onboarding и запуск без формы Vanessa"
description: "Разные режимы обучающих сценариев, зависимости VanessaInteractive и программный запуск feature либо текста без открытия основной формы."
collection: "vanessa"
type: "pattern"
aliases: ["интерактивная справка Vanessa", "onboarding", "VanessaInteractive", "запуск сценария без открытия формы", "ВыполнитьСценарииБезОткрытияФормы"]
tags: ["vanessa", "onboarding-and-embedded-run", "интерактивная справка Vanessa", "onboarding", "VanessaInteractive"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/Onboarding.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/SettingUpInteractiveHelp.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/VanessaInteractiveDemo.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/ЗапускБезОткрытияФормы.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава00/ЧтоНужноЧтобыИнтерактивнаяСправкаРаботала.MD"]
---

# Интерактивная справка, onboarding и запуск без формы Vanessa

## Обучающий урок и UI-тест

Интерактивная справка воспроизводит урок с помощью VanessaExt; она чувствительна к размеру окна и пользовательскому вводу. Кеш озвучки и учебных файлов относится к версии поставки. После урока может остаться отдельное окно Vanessa в режиме обучения — это предусмотренное поведение, а не результат UI-теста продукта.

Автоинструкция, обучающий урок и проверочный сценарий используют Gherkin, но имеют разные критерии успеха. Снятое видео не заменяет assertions теста.

## Встраивание onboarding

Документация описывает расширение VanessaInteractive с вложенной Vanessa Automation Single и интеграцией в нужные формы конфигурации. Web-demo дополнительно требует публикации и доступа сервера к каталогу. Это изменение тестируемого решения/инфраструктуры, отдельное от написания feature-файла. Наличие обычной Vanessa не означает, что onboarding уже встроен.

## Программный запуск без основной формы

API примера предлагает два источника: `УстановитьФичаФайл(ПутьКФичаФайлу)` либо `УстановитьТекстФичаФайла(ТекстФичаФайла)`. Настройки передаются отдельно методом `УстановитьНастройкиПриЗапускеБезОткрытияФормы`, затем вызывается `ВыполнитьСценарииБезОткрытияФормы`. Для отладки существует `ОткрытьОсновнуюФорму`.

Это методы обработки Vanessa из приведённого документа, а не встроенные платформенные функции и не MCP-инструменты. Пример получения формы содержит настройку инициализации редактора, но не показывает её передачу вторым параметром `ПолучитьФорму`; он не доказывает, что одна локальная переменная уже меняет режим редактора.

События начала и окончания называются `ЗапускСценариевVanessaAutomation` и `ОкончаниеВыполненияСценариевVanessaAutomation`. Само событие окончания не является детальным результатом всех проверок.

Связанные темы: [видео и инструкции](video-and-instructions.md), [компоненты](external-components.md), [редактор](editor-workflow.md).

## Источники

[Onboarding](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/Onboarding.md); [SettingUpInteractiveHelp](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/SettingUpInteractiveHelp.md); [VanessaInteractiveDemo](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/VanessaInteractiveDemo.md); [ЗапускБезОткрытияФормы](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/InteractiveHelp/ЗапускБезОткрытияФормы.md); [ЧтоНужноЧтобыИнтерактивнаяСправкаРаботала](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава00/ЧтоНужноЧтобыИнтерактивнаяСправкаРаботала.MD).
