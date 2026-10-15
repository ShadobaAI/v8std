---
id: vanessa:mcp:open_feature_file
title: "Vanessa MCP: open_feature_file"
description: "Документированное назначение и ограничения open_feature_file."
collection: vanessa
type: reference
tags: [vanessa, mcp, open_feature_file]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: open_feature_file

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Открывает .feature файл в Vanessa Editor или активирует уже открытую вкладку. Параметр **filePath** обязателен. Используйте перед **check_syntax**, **execute_feature_step** и ручной навигацией по редактору.

## Связанные темы

- [Редактор, файлы и инструменты](../patterns/editor-workflow.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
