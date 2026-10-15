---
id: vanessa:mcp:save_table_document_to_file
title: "Vanessa MCP: save_table_document_to_file"
description: "Документированное назначение и ограничения save_table_document_to_file."
collection: vanessa
type: reference
tags: [vanessa, mcp, save_table_document_to_file]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: save_table_document_to_file

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Сохраняет содержимое табличного документа в файл на диске. Поддерживаемые форматы: **mxl** (MXL), **xlsx** (Excel), **pdf** (PDF). Параметр **file_name** обязателен и должен содержать полный путь к файлу. Параметр **format** необязательный, по умолчанию **mxl**. Параметр **form_element_name** обязателен и должен содержать имя элемента формы (табличного документа) для сохранения.

## Связанные темы

- [Отчёты и диагностические артефакты](../patterns/reporting-and-artifacts.md)
- [Проверки форм и таблиц](../patterns/form-assertions-and-tables.md)
- [Модальные окна](../patterns/modal-dialogs.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
