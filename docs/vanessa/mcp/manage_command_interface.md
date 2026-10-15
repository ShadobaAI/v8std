---
id: vanessa:mcp:manage_command_interface
title: "Vanessa MCP: manage_command_interface"
description: "Документированное назначение и ограничения manage_command_interface."
collection: vanessa
type: reference
tags: [vanessa, mcp, manage_command_interface]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: manage_command_interface

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Универсальный инструмент для работы с командным интерфейсом 1С:Предприятия. Поддерживаемые действия (параметр **action**): **get_section_panel** - получить панель разделов (первый уровень), **get_function_panel** - получить панель функций (второй уровень, у функций есть навигационная ссылка, которую потом можно использовать для прямого вызова функции), **click_section_panel** - нажать кнопку панели разделов (после этого действия появится панель функций данного раздела и интерфейс клиента тестирования будет заблокирован, пока не будет выбрана команда из панели функций), **click_function_panel** - нажать кнопку панели функций (после нажатия на кнопку панели функций нужно проверить, что открылось нужное окно клиента тестирования с помощью инструмента **get_window_list_testclient**), **close_function_panel** - закрыть панель функций, если она открыта (если панель функций не была открыта, просто возвращает сообщение о том, что панель функций не была открыта), **get_all** - получить весь командный интерфейс (панель разделов и для каждой кнопки панель функций). Для **click_section_panel**: **command** (обязательно) - имя кнопки для нажатия, **returnFunctionPanel** (необязательно) - вернуть содержимое панели функций после нажатия. Для **click_function_panel**: **command** (обязательно) - имя кнопки для нажатия, **group** (необязательно) - имя группы, если команды не уникальны.

## Связанные темы

- [Проверки форм и таблиц](../patterns/form-assertions-and-tables.md)
- [Модальные окна](../patterns/modal-dialogs.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
