---
id: vanessa:mcp:get_active_window_data
title: "Vanessa MCP: get_active_window_data"
description: "Документированное назначение и ограничения get_active_window_data."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_active_window_data]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_active_window_data

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

В зависимости от параметра **type** возвращает важные свойства активного окна клиента тестирования: если type=**window_caption** - возвращает самое важное значение активного окна: его заголовок. По заголовку окна можно найти окно и получить его данные, можно активизировать окно, можно закрыть окно. Если type=**navigation_link** - возвращает навигационную ссылку активного окна. Навигационная ссылка потом может быть использована для открытия окна по навигационной ссылке. Также навигационная ссылка помогает понять с каким объектом метаданных связано активное окно. Если type=**form_name** - возвращает имя формы, подчиненной активному окну. Имя формы позволяет понять с каким объектом метаданных связано активное окно, т.к. в имени формы чаще всего содержится имя объекта метаданных. Если type=**form_caption** - возвращает заголовок формы, подчиненной активному окну. Чаще всего такой заголовок формы совпадает с заголовком окна-владельца и он нужен редко.

## Связанные темы

- [Проверки форм и таблиц](../patterns/form-assertions-and-tables.md)
- [Модальные окна](../patterns/modal-dialogs.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
