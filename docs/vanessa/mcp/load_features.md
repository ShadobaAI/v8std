---
id: vanessa:mcp:load_features
title: "Vanessa MCP: load_features"
description: "Документированное назначение и ограничения load_features."
collection: vanessa
type: reference
tags: [vanessa, mcp, load_features]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: load_features

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Загружает или перезагружает .feature файлы. Используйте после того как вы отредактировали .feature файл, чтобы перечитать файл с диска в Vanessa Automation. Это лучший способ перезагрузить текущий файл в редакторе не указывая имя файла.

## Связанные темы

- [Редактор, файлы и инструменты](../patterns/editor-workflow.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
