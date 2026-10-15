---
id: vanessa:mcp:get_event_log_manager
title: "Vanessa MCP: get_event_log_manager"
description: "Документированное назначение и ограничения get_event_log_manager."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_event_log_manager]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_event_log_manager

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Читает журнал регистрации базы менеджера тестирования (той базы, где запущена Vanessa Automation) штатным механизмом платформы. Читаются последние события периода; порядок вывода по умолчанию - от новых к старым. Вызывающая сторона сама выбирает нужные колонки (**columns**), платформа не материализует лишние. Отборы: **date_start**, **date_end** (по умолчанию - последний час), **event** (системное имя или представление; **event_match_type**: exact/partial/starts_with), **comment** (**comment_match_type**), **level**, **user**, **computer**, **application**, **metadata**, **data** (навигационная ссылка или ЗначениеВСтрокуВнутр), **data_presentation**, **session**, **server**, **port**, **sync_port**, **transaction**, **transaction_status**; несколько значений - через '|' (у comment, data и data_presentation - одно значение). **limit** (по умолчанию 100, максимум 1000) и **scan_limit** (по умолчанию 1000, максимум 20000) ограничивают выборку и объём чтения. **display_order** - порядок вывода (desc/asc). **data_max_length** обрезает значение колонки data. Ответ - markdown-таблица; в шапке счётчики (прочитано платформой / отобрано после фильтра / показано), признаки усечения и значение **date_end** для продолжения выборки. Большие ответы можно писать в файл: **output_file** (+ **output_format**=markdown/json), тогда в ответе остаются шапка, путь, размер и превью. Требует права ЖурналРегистрации (EventLog) у пользователя, от имени которого запущена Vanessa Automation.

## Связанные темы

- [Отчёты и диагностические артефакты](../patterns/reporting-and-artifacts.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
