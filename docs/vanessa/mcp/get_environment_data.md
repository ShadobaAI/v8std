---
id: vanessa:mcp:get_environment_data
title: "Vanessa MCP: get_environment_data"
description: "Документированное назначение и ограничения get_environment_data."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_environment_data]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_environment_data

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Получает важные данные об окружении: текущая дата и время, версия платформы 1С:Предприятие, данные об операционной системе, какая используется VA - обычная или Single, включено ли использование внешней компоненты VanessaExt, в какой базе запущен менеджер тестирования, версия MCP (код этого репозитория; версия расширения Мсп_Сервер в неё не входит).

## Связанные темы

- [Окружение менеджера и клиента](../patterns/environment-readiness.md)
- [Возможности внешней компоненты](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
