---
id: vanessa:mcp:manage_clipboard
title: "Vanessa MCP: manage_clipboard"
description: "Документированное назначение и ограничения manage_clipboard."
collection: vanessa
type: reference
tags: [vanessa, mcp, manage_clipboard]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: manage_clipboard

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Работает с системным буфером обмена операционной системы через внешнюю компоненту VanessaExt. Поддерживаемые действия (параметр **action**): **set_text** - поместить текст в буфер обмена (требуется **text**), **get_text** - прочитать текст из буфера обмена (при большом объёме вернутся только первые 100000 символов), **clear** - очистить буфер обмена. Основной сценарий: длинный или многострочный текст нельзя ввести инструментом **input_text_to_active_field** (лимит 1000 символов), поэтому текст помещают в буфер обмена (action='set_text'), активизируют окно-приёмник (**activate_process_os**) и вставляют текст сочетанием Ctrl+V (**manage_uiautomation**, action='press_keys'). Буфер обмена - общий ресурс операционной системы: инструмент затирает то, что пользователь скопировал ранее, а тестируемое приложение или шаг сценария может перезаписать буфер. Если в буфере обмена файлы, а не текст, action='get_text' вернёт список путей к файлам. Если буфер обмена занят другим приложением, текст может вернуться пустым - повторите вызов. Пока идёт работа с буфером обмена, не вызывайте одновременно другие отложенные инструменты (**speak_text**, **input_text_to_active_field** и т.п.). Параметр **text** обязателен для action='set_text', максимум 100000 символов, многострочный текст передавайте целиком: переводы строк сохраняются. Требует включённую внешнюю компоненту VanessaExt. Не работает в веб-клиенте. Под Linux поддерживается только текст, файлы и картинки недоступны. При запрете синхронных вызовов способ вставки через **manage_uiautomation** **press_keys** не работает.

## Связанные темы

- [Браузер и внешние приложения](../patterns/browser-and-external-ui.md)
- [Компоненты взаимодействия с ОС](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
