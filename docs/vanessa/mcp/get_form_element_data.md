---
id: vanessa:mcp:get_form_element_data
title: "Vanessa MCP: get_form_element_data"
description: "Документированное назначение и ограничения get_form_element_data."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_form_element_data]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_form_element_data

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Получает данные указанного элемента формы клиента тестирования. Возвращает информацию об элементе в формате Markdown: Имя элемента, Заголовок, Тип, Вид, Значение, Представление (если применимо), Флаги: Видимость, Доступность, ТолькоПросмотр. Параметр **element_name** обязателен и должен содержать имя элемента формы.

## Связанные темы

- [Проверки форм и таблиц](../patterns/form-assertions-and-tables.md)
- [Модальные окна](../patterns/modal-dialogs.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
