---
id: vanessa:mcp:window_management
title: "Vanessa MCP: window_management"
description: "Документированное назначение и ограничения window_management."
collection: vanessa
type: reference
tags: [vanessa, mcp, window_management]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: window_management

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Универсальный инструмент для управления окнами клиента тестирования. Поддерживаемые действия (параметр **action**): **activate** - активизировать окно по заголовку (требуется **window_title**), **close** - закрыть окно по заголовку (требуется **window_title**; для поиска по части заголовка используйте маску *, например '*Окно*'), **open_navigation** - открыть навигационную ссылку (требуется **navigation_link**). Для активизации окна: укажите **action**='activate' и **window_title** с полным заголовком окна или используйте символы * для поиска по частичному совпадению (например, '*Окно*'). Без маски заголовок сравнивается целиком. Для закрытия окна: укажите **action**='close' и **window_title** с полным заголовком окна или используйте символы * для поиска по частичному совпадению (например, '*Окно*'). Без маски заголовок сравнивается целиком. Для открытия формы: укажите **action**='open_navigation' и **navigation_link** с навигационной ссылкой; если такая форма уже открыта, открывается новое окно - переключитесь на нужное окно действием **activate**, дубликаты закрывайте действием **close**.

## Связанные темы

- [Браузер и внешние приложения](../patterns/browser-and-external-ui.md)
- [Компоненты взаимодействия с ОС](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
