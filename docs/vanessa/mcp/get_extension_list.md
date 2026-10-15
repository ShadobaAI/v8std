---
id: vanessa:mcp:get_extension_list
title: "Vanessa MCP: get_extension_list"
description: "Документированное назначение и ограничения get_extension_list."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_extension_list]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_extension_list

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Получает список всех расширений установленных в клиент тестирования. Клиент тестирования должен быть подключен. Возвращает информацию о каждом расширении. Поля: Имя, Версия, Назначение; Флаги: Активно, БезопасныйРежим. После вызова инструмент возвращает фокус окну, которое было активным до вызова.

## Связанные темы

- [VanessaExt и VAExtension](../patterns/external-components.md)
- [Возможности расширения клиентской базы](../patterns/extension-capabilities.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
