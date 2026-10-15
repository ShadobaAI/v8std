---
id: vanessa:mcp:manage_test_client_profiles
title: "Vanessa MCP: manage_test_client_profiles"
description: "Документированное назначение и ограничения manage_test_client_profiles."
collection: vanessa
type: reference
tags: [vanessa, mcp, manage_test_client_profiles]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: manage_test_client_profiles

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Универсальный инструмент для работы с таблицей профилей клиентов тестирования Vanessa Automation. Поддерживаемые действия (параметр **action**): **get_list** - получить список всех профилей клиентов тестирования, **add** - добавить новый профиль в таблицу, **edit** - редактировать существующий профиль. Для **add** и **edit**: **name** (обязательно) - имя профиля, **synonym** - синоним профиля, **infobase_path** - строка подключения к базе, **additional_parameters** - дополнительные параметры подключения, **client_type** - тип клиента (Тонкий (основной вариант), Толстый, Web, МобильныйКлиент, МобильноеПриложение, МобильныйКлиентАвтономный, ОбычноеПриложение), **computer_name** - имя компьютера. Уточнение. Если параметры клиента тестирования изменились, то это может потребовать перезапуска клиента тестирования. Подробная информация про то как устроена таблица клиентов тестирования есть в базе знаний, инструмент **get_data_from_knowledge_base**.

## Связанные темы

- [Подключения и параметры TestClient](../patterns/test-client-profiles.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
