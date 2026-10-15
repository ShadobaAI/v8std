---
id: vanessa:mcp:input_text_to_active_field
title: "Vanessa MCP: input_text_to_active_field"
description: "Документированное назначение и ограничения input_text_to_active_field."
collection: vanessa
type: reference
tags: [vanessa, mcp, input_text_to_active_field]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: input_text_to_active_field

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Вводит текст в активное поле, эмулируя ввод с клавиатуры через внешнюю компоненту VanessaExt. Имя элемента формы указывать не нужно: текст вводится в то окно, которое сейчас активно в операционной системе. Если текст должен попасть в неактивное окно, передайте **activate_window**=true - тогда перед вводом будет активизировано окно клиента тестирования, либо окно, заданное параметрами **pid** или **window_title**. Раскладка клавиатуры не важна. Вводятся только символы: клавиши Enter, Tab и другие не эмулируются, для них используйте **manage_uiautomation** **press_keys**. Для длинного или многострочного текста поместите его в буфер обмена (**manage_clipboard**, action='set_text') и вставьте сочетанием Ctrl+V (**manage_uiautomation**, action='press_keys'). Эмуляция ввода не сообщает об ошибках и может быть прервана, поэтому после ввода проверьте значение поля (**get_form_element_data**). Пока идёт ввод, инструмент занят: не вызывайте одновременно другие отложенные инструменты (**speak_text**, **activate_process_os** и т.п.). При выполнении сценариев инструмент отказывает - сначала остановите сценарии (**stop_scenario**). Параметры: **text** (обязательный, максимум 1000 символов), **delay** (задержка между символами в мс, от 0 до 5000, по умолчанию 100 - примерно 10 символов в секунду; длина текста, умноженная на задержку, не должна быть больше 45000), **activate_window** (по умолчанию false), **pid** и **window_title** (взаимоисключающие, используются только вместе с **activate_window**=true; в **window_title** поддерживаются маски с *, маска проверяется на полное совпадение строки, поэтому для поиска по части строки оборачивайте выражение в * с обеих сторон). Требует включённую внешнюю компоненту VanessaExt. Не работает в веб-клиенте и под Linux.

## Связанные темы

- [Браузер и внешние приложения](../patterns/browser-and-external-ui.md)
- [Компоненты взаимодействия с ОС](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
