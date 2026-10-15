---
id: vanessa:mcp:find_form_elements
title: "Vanessa MCP: find_form_elements"
description: "Документированное назначение и ограничения find_form_elements."
collection: vanessa
type: reference
tags: [vanessa, mcp, find_form_elements]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: find_form_elements

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Ищет элементы в активном окне клиента тестирования платформенным методом НайтиОбъекты: по заголовку, по имени элемента или по обоим (параметр **search_by**: all/title/name; по умолчанию all). Символ * - маска (например, *Товар*). Для каждого найденного элемента выводится заголовок, внутреннее имя, тип и вид, родитель первого уровня, а также имя табличной части, если элемент находится в таблице (учитываются колонки, вложенные в группы внутри таблицы). Параметр **search_string** обязателен; **limit** ограничивает число элементов в ответе (по умолчанию 50, 0 - без ограничения). Поиск идёт только по активному окну; элементы на ещё не открытых закладках могут не находиться - переключите закладку (**switch_tab**). Пустой результат - не ошибка. Требует платформы 8.3.25 и выше и подключённого клиента тестирования. Это поиск элементов формы клиента тестирования (не путать с **find_elements** UI Automation в **manage_uiautomation**).

## Связанные темы

- [Проверки форм и таблиц](../patterns/form-assertions-and-tables.md)
- [Модальные окна](../patterns/modal-dialogs.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
