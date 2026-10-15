---
id: vanessa:mcp:get_window_list_testclient
title: "Vanessa MCP: get_window_list_testclient"
description: "Документированное назначение и ограничения get_window_list_testclient."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_window_list_testclient]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_window_list_testclient

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Получает список внутренних окон клиента тестирования. Результат можно использовать для управления окнами с помощью инструмента **window_management** (активизировать, закрыть, открыть навигационную ссылку), либо для получения данных из текущего окна **get_active_window_data**. Результат нельзя использовать для получения скриншота окна, т.к. список внутренних окон клиента тестирования и список окон с точки зрения операционной системы - это разные вещи.

## Связанные темы

- [Проверки форм и таблиц](../patterns/form-assertions-and-tables.md)
- [Модальные окна](../patterns/modal-dialogs.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
