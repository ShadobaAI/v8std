---
id: vanessa:patterns:tags-and-selection
title: "Выбрать сценарии по тегам и включить диагностические теги"
description: "Различие меток feature/сценария и служебных @tree, @ExportScenarios, @screenshot, @recordvideo; требования и эффекты записи."
collection: "vanessa"
type: "pattern"
tags: ["vanessa", "pattern", "tags", "selection", "filter", "screenshot", "video", "tree", "export"]
aliases: ["как запустить только сценарии с тегом", "как исключить feature по тегу", "@tree @ExportScenarios что означают", "@screenshot скриншот до и после шага", "@recordvideo @StopRecordVideo @StartRecordVideo"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/КакУстроенFeatureФайлЗаголовокФичи.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/КакУстроенFeatureФайлСекцияСценария.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ТегСнятияСкриншотов.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ТегЗаписиВидеоВыполненияСценария.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ГруппыШагов.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ПодсценарииЧастьОдин.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/training/features/Примеры/ПримерТегСнятияСкриншотов.feature", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/training/features/Примеры/ПримерТегЗаписиВидеоВыполненияСценария1.feature", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/training/features/Примеры/ПримерТегЗаписиВидеоВыполненияСценария2.feature"]
---

# Выбрать сценарии по тегам и включить диагностические теги

Основание: MainHelp 1.2.043.1 и учебные feature тегов. Позиции и описанные эффекты — документированное поведение; схема отбора зависит от текущего runner/runtime. Не выводите синтаксис JSON-фильтров или логических выражений тегов из одного примера метки.

## Разместить теги на нужном уровне

Теги feature идут до `Функциональность:`, теги сценария — перед `Сценарий:`. Обычная метка позволяет отобрать или исключить часть feature/сценариев; обработчик определяет её смысл.

```gherkin
# language: ru
@проверкаСтрок
Функциональность: Сохранение значений

@smoke
Сценарий: Проверка_1
    И я запоминаю строку "готово" в переменную "Результат"
    Тогда переменная "Результат" имеет значение "готово"
```

Это пример размещения, а не команда запуска. Параметры отбора определяются конфигурацией runner и текущим контрактом MCP. Нулевая выборка означает отсутствие выполненных проверок. Выполнение выбранного сценария, текущего feature и всех загруженных feature имеет разный охват: [запуск и диагностика](execution-debugging.md).

## Не смешивать фильтр с изменением семантики

`@tree` включает обработку иерархических групп шагов, когда она не включена настройкой по умолчанию. Изменение отступов тогда меняет, какие строки выполняются. `@ExportScenarios` в секции тегов feature делает его сценарии доступными как подсценарии. Это не произвольные ярлыки отбора и не замена подключения библиотек.

Теги `@типшага:`, `@описание:`, `@примериспользования:` описывают экспортный сценарий для дерева известных шагов; см. [подсценарии и библиотеки](subscenarios-and-libraries.md). Они не являются asserts.

## Получить скриншоты около проблемного шага

Учебный пример ставит `@screenshot` непосредственно перед нужным шагом:

```gherkin
@screenshot
И Пауза 2
```

Этот пример показывает позицию диагностического тега; пауза не рекомендуется как проверка результата. При включённой соответствующей настройке Vanessa делает два скриншота: перед и после следующего шага. Если включён Allure, изображения добавляются к отчёту. Сам тег не включает отсутствующую настройку и не доказывает состояние приложения.

## Записать видео и понимать границы фрагмента

`@recordvideo` включает запись экрана с указанного места до конца выполнения сценария; нужна установленная `ffmpeg`. При включённом Allure видео прикладывается к отчёту.

```gherkin
@recordvideo
И Пауза 2
```

`@StopRecordVideo` и `@StartRecordVideo` показаны для остановки и продолжения фрагмента записи внутри группового шага при создании автоинструкции. Не переносите их без проверки на произвольный режим записи и не путайте с остановкой выполнения сценария.

Диагностические артефакты дополняют проверяющие шаги, но не заменяют assertions. Обрабатывайте фактический текст и изображение ошибки: [сохранение ожиданий](steps-assertions.md).

Источники: [теги сценария](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/КакУстроенFeatureФайлСекцияСценария.MD); [скриншоты](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ТегСнятияСкриншотов.MD); [запись выполнения](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ТегЗаписиВидеоВыполненияСценария.MD).
