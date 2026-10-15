---
id: vanessa:mcp:get_test_results
title: "Vanessa MCP: get_test_results"
description: "Документированное назначение и ограничения get_test_results."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_test_results]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_test_results

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Подробные результаты выполнения сценария: статус каждого шага, время, ошибки. Если scenarioId не указан — результат последнего сценария.

## Связанные темы

- [Отчёты и диагностические артефакты](../patterns/reporting-and-artifacts.md)
- [Состояние и результаты выполнения](../patterns/execution-debugging.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
