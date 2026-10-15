---
id: vanessa:patterns:project-layout
title: "Как организовать каталоги проекта UI-тестов Vanessa"
description: "Разделение запускаемых features, экспортных библиотек, данных, макетов, конфигурации и результатов; связи с КаталогПроекта и КаталогиБиблиотек."
collection: "vanessa"
type: "pattern"
aliases: ["структура каталогов тестов", "как организовать каталоги тестов", "папки проекта Vanessa", "features libraries fixtures", "куда складывать макеты и скриншоты"]
tags: ["vanessa", "project-layout", "структура каталогов тестов", "как организовать каталоги тестов", "папки проекта Vanessa"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/JsonParams/JsonParamsRU.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/CommandSetting/CommandSetting.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/index.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава08/ПроверитьРавенствоТабличногоДокументаЭталону.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/examples/МультиАгент/Инструкции/InstructionsResearch.md"]
---

# Как организовать каталоги проекта UI-тестов Vanessa

## Роли каталогов и параметры Vanessa

Vanessa различает корень проекта, входной файл/каталог сценариев, каталоги библиотек и пути результатов. В настройках это `КаталогПроекта` (`projectpath`), `КаталогФич` (`featurepath`), `КаталогиБиблиотек` (`librarycatalogs`) и отдельные каталоги отчётов. Совпадение этих путей не обязательно. Без явного `WorkspaceRoot` исходным корнем может оказаться каталог обработки Vanessa, поэтому перенос EPF не должен незаметно менять пути тестов.

## Пример структуры по назначению

Это прикладная схема на основе описанных механизмов, а не обязательные имена каталогов Vanessa:

```text
ui-tests/
  features/
    smoke/                  # короткие проверки открытия и доступности
    business/               # пользовательские сценарии по подсистемам
      sales/
        create-order.feature
        expected-order.mxl  # эталон рядом с использующим feature
  libraries/                # экспортные .feature, явно подключённые как библиотеки
  data/                     # версионируемые JSON/сценарии подготовки данных
  settings/                 # шаблоны VAParams для разных способов запуска
  artifacts/                # результаты конкретных прогонов
    allure-results/
    junit/
    screenshots/
  .local/                   # локальные параметры подключения и рабочее состояние
```

`features/` выбирается входом исполнения, `libraries/` — библиотечным путём. Наличие папки с именем `libraries` само по себе не включает её в поиск экспортов. Общие операции оформляются [экспортными сценариями](subscenarios-and-libraries.md), а не копиями одного длинного сценария.

## Макеты, данные и результаты

Для шага сравнения табличного документа руководство описывает поиск MXL по имени без расширения в корне проекта либо рядом с feature. Произвольная папка `templates/` не становится автоматически доступной: нужны поддерживаемый конкретным шагом путь или механизм поиска. [Данные](test-data-strategies.md) и эталоны имеют отдельный жизненный цикл; выгрузка результата не является новым эталоном автоматически.

Стабильные сценарии, библиотеки и небольшие тестовые данные обычно версионируются. Локальные подключения, credentials и результаты запусков отделяются от общего набора. В AI-примере документации есть папки `png/`, `research/` и инструкции субагентам: это структура конкретного примера, а не требование каждого проекта Vanessa.

## Что определяет проект

Разделение smoke/бизнес-проверок, названия файлов, правила нумерации и каталог результатов выбираются проектом. Тесты форм и проверки движений документов полезно отделять: они имеют разные действия, данные и критерии результата. Сценарии записи, копирования и проведения требуют [явной стратегии данных](test-data-strategies.md), даже если созданы генератором smoke.

Связанные темы: [конфигурация и CI](configuration-and-ci.md), [генерация smoke](smoke-test-generation.md), [отчёты](reporting-and-artifacts.md), [разделы feature](feature-sections.md).

## Источники

[JsonParamsRU](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/JsonParams/JsonParamsRU.md); [CommandSetting](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/CommandSetting/CommandSetting.md); [index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/index.md); [ПроверитьРавенствоТабличногоДокументаЭталону](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава08/ПроверитьРавенствоТабличногоДокументаЭталону.MD); [InstructionsResearch](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/examples/МультиАгент/Инструкции/InstructionsResearch.md).
