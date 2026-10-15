---
id: vanessa:mcp:get_event_log_test_client
title: "Vanessa MCP: get_event_log_test_client"
description: "Документированное назначение и ограничения get_event_log_test_client."
collection: vanessa
type: reference
tags: [vanessa, mcp, get_event_log_test_client]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: get_event_log_test_client

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Читает журнал регистрации базы клиента тестирования. Отбор и обрезка выполняются внутри базы клиента (обработка VAExtension_ЖурналРегистрации расширения VAExtension), менеджеру возвращается только результат, поэтому лишний трафик клиент -> менеджер не гоняется. Журнал читается в привилегированном режиме: права пользователя клиента тестирования чтение не ограничивают - учитывайте это, данные ЖР могут быть чувствительными. Контракт параметров и формат ответа те же, что у **get_event_log_manager** (период, событие, комментарий, уровень, пользователь, компьютер, приложение, метаданные, данные, сеанс, сервер, порты, транзакция, статус транзакции, **limit**, **scan_limit**, **display_order**, **columns**, **data_max_length**, **output_file**, **output_format**). Требует подключённого клиента тестирования (**manage_test_client**, action='connect') и расширения VAExtension версии 1.40 и выше в базе клиента.

## Связанные темы

- [Отчёты и диагностические артефакты](../patterns/reporting-and-artifacts.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
