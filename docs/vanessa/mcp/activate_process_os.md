---
id: vanessa:mcp:activate_process_os
title: "Vanessa MCP: activate_process_os"
description: "Документированное назначение и ограничения activate_process_os."
collection: vanessa
type: reference
tags: [vanessa, mcp, activate_process_os]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: activate_process_os

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Активизирует окно процесса операционной системы: выводит его на передний план и передаёт ему фокус. Аналог шагов <И я активизирую процесс "PID"> и <И я активизирую процесс по заголовку "Заголовок">; полная аналогия с шагом по заголовку — при поиске с маской *заголовок*, без маски отбор шире — по подстроке. Нужно передать один из параметров: **pid** (положительное число; активизировать главное окно процесса) или **window_title** (найти процесс по заголовку или части заголовка окна; поддерживаются маски с *, например *Блокнот*; поиск без учёта регистра; маска проверяется на полное совпадение строки, поэтому для поиска по части строки оборачивайте выражение в * с обеих сторон). Параметры pid и window_title взаимоисключающие. Полезно перед всем, что работает с активным окном: эмуляция клавиатуры, ввод текста, шаги UI Automation, снятие скриншота. Для работы нужна включённая внешняя компонента VanessaExt. Не работает в веб-клиенте. Клиент тестирования не требуется.

## Связанные темы

- [Окружение менеджера и клиента](../patterns/environment-readiness.md)
- [Возможности внешней компоненты](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
