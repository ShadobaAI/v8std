---
id: vanessa:mcp:execute_feature_step
title: "Vanessa MCP: execute_feature_step"
description: "Документированное назначение и ограничения execute_feature_step."
collection: vanessa
type: reference
tags: [vanessa, mcp, execute_feature_step]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: execute_feature_step

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Выполняет шаг из .feature файла по номеру строки. Валидирует что файл открыт в редакторе, активирует вкладку при необходимости.

## Связанные темы

- [Запуск и отладка сценария](../patterns/execution-debugging.md)
- [Отбор, ожидания и статусы выполнения](../patterns/execution-lifecycle.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
