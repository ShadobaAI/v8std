---
id: vanessa:mcp:run_scenario
title: "Vanessa MCP: run_scenario"
description: "Документированное назначение и ограничения run_scenario."
collection: vanessa
type: reference
tags: [vanessa, mcp, run_scenario]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: run_scenario

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Запускает выполнение сценариев. Отправляет прогресс по каждому шагу (step N/M). Возвращает итоговый результат после завершения. Если указан **filePath** — загрузит фичу, откроет в редакторе и запустит. Режимы: **all** (по умолчанию — все сценарии. Если просят выполнить все сценарии надо использовать режим all), **reloadAndRun** (перезагрузить и запустить фича файл с начала), **selected** (выбранный в редакторе, перед этим надо вызвать **select_scenario**), **fromCurrentStep** (с текущего шага, перед этим нужно вызвать **select_step**), **reloadAndRunFromLine** (перезагрузить фича файл и выполнить сценарий со строки указанной в **lineNumber**).

## Связанные темы

- [Запуск и отладка сценария](../patterns/execution-debugging.md)
- [Отбор, ожидания и статусы выполнения](../patterns/execution-lifecycle.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
