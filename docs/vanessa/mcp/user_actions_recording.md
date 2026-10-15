---
id: vanessa:mcp:user_actions_recording
title: "Vanessa MCP: user_actions_recording"
description: "Документированное назначение и ограничения user_actions_recording."
collection: vanessa
type: reference
tags: [vanessa, mcp, user_actions_recording]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: user_actions_recording

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Управляет записью действий пользователя в клиенте тестирования. Поддерживаемые действия (параметр **action**): **start** (по умолчанию) - начать запись действий пользователя, **stop** - остановить запись и вернуть записанные шаги в формате Turbo Gherkin (если после вызова **stop** нужно опять начать запись действий - то нужно вызвать инструмент с параметром **start**). При остановке записи возвращается текст шагов в формате Turbo Gherkin, которые были выполнены пользователем за время записи. Требует подключённого клиента тестирования.

## Связанные темы

- [Исследование формы и запись действий](../patterns/exploration-recording.md)
- [Компоненты и режимы записи](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
