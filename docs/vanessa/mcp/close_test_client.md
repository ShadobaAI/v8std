---
id: vanessa:mcp:close_test_client
title: "Vanessa MCP: close_test_client"
description: "Документированное назначение и ограничения close_test_client."
collection: vanessa
type: reference
tags: [vanessa, mcp, close_test_client]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: close_test_client

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Закрывает сеанс клиента тестирования по имени профиля. Если профиль не указан — закрывает текущий подключенный профиль. Используйте для завершения работы с клиентом тестирования после выполнения тестов.

## Связанные темы

- [Подключения и параметры TestClient](../patterns/test-client-profiles.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
