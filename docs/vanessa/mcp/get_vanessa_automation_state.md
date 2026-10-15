---
id: vanessa:mcp:get_vanessa_automation_state
title: "Vanessa MCP: get_vanessa_automation_state"
description: "Документированное назначение и ограничения get_vanessa_automation_state."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_vanessa_automation_state]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_vanessa_automation_state

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Возвращает текущее состояние Vanessa Automation в формате Markdown: выполняется ли сценарий, текущая фича (имя, путь, язык, теги), текущий сценарий (имя, статус, теги), текущий шаг (id, текст, значения параметров, номер строки, статус; статус Running означает, что шаг выполняется), подключен ли клиент тестирования. Используйте для получения контекста перед написанием или анализом тестов.

## Связанные темы

- [Окружение менеджера и клиента](../patterns/environment-readiness.md)
- [Возможности внешней компоненты](../patterns/external-components.md)
- [Состояние и результаты выполнения](../patterns/execution-debugging.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
