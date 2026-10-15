---
id: vanessa:mcp:get_process_list_os
title: "Vanessa MCP: get_process_list_os"
description: "Документированное назначение и ограничения get_process_list_os."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_process_list_os]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_process_list_os

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Возвращает список процессов операционной системы в формате Markdown-таблицы: PID и командная строка (при наличии данных - и дата старта процесса). Полезно для диагностики: какие процессы запущены, какие клиенты тестирования активны. Параметр **only_1c** - если true, вернутся только процессы 1С (отбор выполняет внешняя компонента VanessaExt). Параметр **filter** отбирает процессы по части имени процесса, командной строки или PID; поддерживаются выражения с масками, где * - произвольный набор символов, например *1C*; если маски нет - выполняется поиск подстроки; поиск без учёта регистра; маска проверяется на полное совпадение строки, поэтому для поиска по части строки оборачивайте выражение в * с обеих сторон. Параметр **limit** - максимальное количество процессов в ответе (0 - вернуть все, по умолчанию 100). Для работы нужна включённая внешняя компонента VanessaExt. Не работает в веб-клиенте.

## Связанные темы

- [Окружение менеджера и клиента](../patterns/environment-readiness.md)
- [Возможности внешней компоненты](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
