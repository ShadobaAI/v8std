---
id: vanessa:mcp:manage_app
title: "Vanessa MCP: manage_app"
description: "Документированное назначение и ограничения manage_app."
collection: vanessa
type: reference
tags: [vanessa, mcp, manage_app]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: manage_app

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Универсальный инструмент для управления приложением клиента тестирования. Поддерживаемые действия (параметр **action**): **set_file_dialog_result** - установить результат диалога выбора файла в клиенте тестирования (параметры: **cancel** - булево, необязательное, по умолчанию Ложь: Истина = отмена диалога, Ложь = файл выбран; **file_name** - строка, путь к выбранному файлу, обязателен при cancel=Ложь; **filter_index** - целое неотрицательное число, необязательный индекс фильтра диалога; при cancel=Истина параметры file_name и filter_index игнорируются). Установленный результат сработает при следующем открытии диалога выбора файла в клиенте тестирования; требует подключённого клиента тестирования (**manage_test_client**, action='connect'). **clear_file_dialog_result** - очистить ранее установленный результат диалога выбора файла (не требует параметров; требуется платформа 8.3.25+).

## Связанные темы

- [Браузер и внешние приложения](../patterns/browser-and-external-ui.md)
- [Компоненты взаимодействия с ОС](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
