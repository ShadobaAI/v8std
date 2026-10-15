---
id: vanessa:patterns:gherkin-structure
title: "Gherkin Vanessa: структура и выбор конструкции"
description: "Карта конструкций feature: заголовок, Контекст, сценарий, примеры, переменные и экспортные сценарии."
collection: "vanessa"
type: "pattern"
aliases: ["структура Gherkin Vanessa", "как устроен feature файл", "Контекст или сценарий", "Turbo Gherkin конструкции"]
tags: ["vanessa", "gherkin-structure", "структура Gherkin Vanessa", "как устроен feature файл", "Контекст или сценарий"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ЧтоТакоеЯзыкGherkin.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/КакУстроенFeatureФайлСекцияКонтекст.MD", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Gherkin Vanessa: структура и выбор конструкции

## Сценарий как описание поведения

Feature объединяет поведение по теме. Сценарий выражает исходное состояние, действия и наблюдаемый результат. Язык, отступы, группы и специальные секции имеют синтаксический смысл; требования конкретного проекта могут дополнительно определять стиль имён и файлов.

## Какая конструкция для какой задачи

| Задача | Тема |
| --- | --- |
| Общая подготовка перед сценариями одного feature | [Секции feature и Контекст](feature-sections.md) |
| Одинаковое поведение на нескольких наборах параметров | [Структура сценария и Примеры](scenario-outlines.md) |
| Повторяющийся процесс между feature | [Экспортные сценарии и библиотеки](subscenarios-and-libraries.md) |
| Значения, таблицы и вычисления | [Переменные и параметры](variables-and-parameters.md) |
| Ветвление, повторение, обработка ошибки | [Условия, циклы и исключения](conditions-loops-exceptions.md) |
| Выбор набора исполнения | [Теги и фильтры](tags-and-selection.md) |

`Контекст` описан в документации и выполняется перед сценариями; запрет Контекста в отдельном AI-примере относится к тому примеру. Таблица данных сценария, таблица Примеров и таблица секции Переменные не являются взаимозаменяемыми.

## Файл и редактор

Сохранённый файл и содержимое уже открытой вкладки могут различаться. Перезагрузка и проверка синтаксиса относятся к исполняемой версии текста, а не только к имени пути. Записанный Turbo Gherkin — исходный материал для сценария, а не доказательство полноты проверок.

Связанная тема: [организация каталогов](project-layout.md).

## Источники

[ЧтоТакоеЯзыкGherkin](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/ЧтоТакоеЯзыкGherkin.MD); [КакУстроенFeatureФайлСекцияКонтекст](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/1.2.043.1/Глава03/КакУстроенFeatureФайлСекцияКонтекст.MD); [index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md).
