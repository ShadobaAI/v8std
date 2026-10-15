---
id: vanessa:mcp:search_for_steps_by_keywords
title: "Vanessa MCP: search_for_steps_by_keywords"
description: "Документированное назначение и ограничения search_for_steps_by_keywords."
collection: vanessa
type: reference
tags: [vanessa, mcp, search_for_steps_by_keywords]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: search_for_steps_by_keywords

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Ищет шаги Vanessa Automation по переданной строке поиска и возвращает их в формате Markdown. Поиск производится по: представлению шагов, описании шагов и типу шагов. В любой параметр можно передавать несколько значений, разделенных вертикальной чертой \|. Пример поиска шагов в представлении которых встречается слово "кнопка": **search_name** = "кнопка\|кнопки\|кнопку". Пример исключения шагов в представлении которых встречается слово "поле": **exclude_name** = "поле\|поля". Пример поиска шагов в описании которых встречается слово "клиент тестирования": **search_description** = "клиент тестирования". Пример исключения шагов в описании которых встречается слово "гиперссылка": **exclude_description** = "гиперссылка\|гиперссылки". Пример поиска шагов в типе которых встречается строка "Объекты конфигурации": **search_type** = "Объекты конфигурации". Пример исключения шагов в описании которых встречается строка "Переменные среды": **exclude_type** = "Переменные среды".

## Связанные темы

- [Библиотека шагов и проверки](../patterns/steps-assertions.md)
- [Библиотеки и экспортные сценарии](../patterns/subscenarios-and-libraries.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
