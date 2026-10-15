---
id: vanessa:mcp:get_editor_state
title: "Vanessa MCP: get_editor_state"
description: "Документированное назначение и ограничения get_editor_state."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_editor_state]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_editor_state

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Возвращает состояние Monaco-редактора Vanessa Automation: открытые вкладки, содержимое активного документа, позицию курсора, ошибки. Один вызов для полного понимания контекста редактора. Если feature файл загружен в редактор Vanessa Automation, то уже можно запускать его сценарии на выполнение с помощью **run_scenario**.

## Связанные темы

- [Редактор, файлы и инструменты](../patterns/editor-workflow.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
