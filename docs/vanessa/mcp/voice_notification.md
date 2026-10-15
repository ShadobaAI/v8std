---
id: vanessa:mcp:voice_notification
title: "Vanessa MCP: voice_notification"
description: "Документированное назначение и ограничения voice_notification."
collection: vanessa
type: reference
tags: [vanessa, mcp, voice_notification]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: voice_notification

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Воспроизводит голосовое уведомление через внешнюю компоненту VanessaExt. Полезно в тех случаях, если ИИ агент работает в отдельной виртуальной машине, выполняет какое-то длинное задание и пользователю удобно получать голосовое уведомление о: задании выполненном, необходимости принять решение, задании, которое не может быть выполнено, или ошибке при выполнении задания.

## Связанные темы

- [Озвучка и автоинструкции](../patterns/video-and-instructions.md)
- [Подготовка видеоинструкций](../patterns/video-authoring.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
