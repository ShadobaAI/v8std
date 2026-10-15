---
id: vanessa:mcp:get_window_list_os
title: "Vanessa MCP: get_window_list_os"
description: "Документированное назначение и ограничения get_window_list_os."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_window_list_os]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_window_list_os

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Возвращает список окон доступных для снятия скриншота с точки зрения операционной системы. Нужно вызвать перед **get_window_screenshot_os**.

## Связанные темы

- [Окружение менеджера и клиента](../patterns/environment-readiness.md)
- [Возможности внешней компоненты](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
