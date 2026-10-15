---
id: vanessa:patterns:modal-dialogs
title: "Модальные диалоги: состояние окна, локаторы и продолжение"
description: "Чем диалог 1С отличается от native-окна и файлового диалога, как неоднозначный заголовок влияет на действие."
collection: "vanessa"
type: "pattern"
aliases: ["модальный диалог Vanessa", "paused_modal_dialog", "одинаковые заголовки окон", "внутреннее окно или окно ОС"]
tags: ["vanessa", "modal-dialogs", "модальный диалог Vanessa", "paused_modal_dialog", "одинаковые заголовки окон"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/index.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/UIAutomation/UIAutomation.md"]
---

# Модальные диалоги: состояние окна, локаторы и продолжение

## Разные механизмы окон

Внутреннее окно 1С, отдельное окно ОС и системный файловый диалог имеют разные способы обнаружения и управления. `window_management` относится к окнам приложения; снимок ОС требует соответствующего OS-окна. Файловый диалог дополнительно различается для thin/thick и web.

Заголовок, значимый текст, кнопки и предшествующее действие определяют смысл диалога. Маска `*` поддерживается не всеми механизмами одинаково и может совпасть с несколькими окнами. UI Automation ID относится к состоянию элемента и может измениться после его пересоздания.

## Приостановленная цепочка действий

MCP может вернуть `paused_modal_dialog`: дальнейшие действия цепочки не завершены. Обработка известного диалога и продолжение оставшейся части отличаются от повторения всей цепочки. Повтор с начала способен второй раз выполнить уже завершённые действия.

Нажатие «Да», «Записать» или «Удалить» имеет эффект конкретной операции; одинаковая подпись кнопки в разных диалогах не означает одинаковое действие. Произвольная пауза не доказывает, что диалог закрыт или операция успешна.

Связанные темы: [выбор файла](files-and-dialogs.md), [внешние окна](browser-and-external-ui.md), [ожидания](synchronization-and-waits.md), [MCP действий](../mcp/execute_form_actions.md).

## Источники

[index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); [index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/index.md); [UIAutomation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/UIAutomation/UIAutomation.md).
