---
id: vanessa:mcp:get_data_from_knowledge_base
title: "Vanessa MCP: get_data_from_knowledge_base"
description: "Документированное назначение и ограничения get_data_from_knowledge_base."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_data_from_knowledge_base]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_data_from_knowledge_base

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Получает информацию из базы знаний, в которой хранится информация о часто возникающих вопросах и как их решить. Данные в базе знаний хранятся в формате Вопрос - ответ. Чтобы экономить токены можно получать данные порциями. В начале ответа указывается размер переданных данных в байтах и символах: если символов в полученном тексте меньше указанного, ответ был обрезан MCP-клиентом. Можно получить только тексты вопросов, чтобы потом получить ответ только на нужный вопрос. Можно выполнить поиск по вопросам и ответам. Поиск работает без учёта регистра букв. Всю базу знаний можно записать в файл: format=**save_to_file** и параметр **file_path** (файл создаётся на машине Vanessa Automation).

## Связанные темы

- [Каталог справки Vanessa](../patterns/catalog.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
