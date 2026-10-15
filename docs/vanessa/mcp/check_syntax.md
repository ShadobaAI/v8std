---
id: vanessa:mcp:check_syntax
title: "Vanessa MCP: check_syntax"
description: "Документированное назначение и ограничения check_syntax."
collection: vanessa
type: reference
tags: [vanessa, mcp, check_syntax]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: check_syntax

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Проверяет синтаксис Gherkin в указанном feature-файле. Параметр **filePath** обязателен. Возвращает Markdown с найденными ошибками: неизвестные шаги, структурные проблемы, ошибки ключевых слов.

## Связанные темы

- [Редактор, файлы и инструменты](../patterns/editor-workflow.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
