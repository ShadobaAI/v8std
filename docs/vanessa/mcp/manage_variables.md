---
id: vanessa:mcp:manage_variables
title: "Vanessa MCP: manage_variables"
description: "Документированное назначение и ограничения manage_variables."
collection: vanessa
type: reference
tags: [vanessa, mcp, manage_variables]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: manage_variables

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Чтение, установка и удаление переменных тестового контекста. Действия с переменными: **get** (по умолчанию), **set**, **delete**. Переменные позволяют хранить произвольные значения в памяти Vanessa Automation. Переменные бывают локальные и глобальные. Локальные существуют только во время выполнения сценария. Перед началом выполнения сценария все локальные переменные удаляются. Глобальные переменные существуют пока работает Vanessa Automation и не удаляются перед выполнением сценария.

## Связанные темы

- [Переменные и параметры](../patterns/variables-and-parameters.md)
- [Вычисления и контекст](../patterns/embedded-code-and-context.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
