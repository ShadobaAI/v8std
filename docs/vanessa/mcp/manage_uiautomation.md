---
id: vanessa:mcp:manage_uiautomation
title: "Vanessa MCP: manage_uiautomation"
description: "Документированное назначение и ограничения manage_uiautomation."
collection: vanessa
type: reference
tags: [vanessa, mcp, manage_uiautomation]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md"]
---

# Vanessa MCP: manage_uiautomation

## Контракт и версия

Справочная карточка из `docs/AI/index.md`. Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

Универсальный инструмент для работы с технологией UI Automation (Windows) в любых приложениях: поиск элементов UI Automation по PID/имени/типу/подсказке, чтение свойств элемента, навигация по дереву (родитель/дети/следующий/активный элемент), клики (левый/правый/двойной), эмуляция ввода текста, нажатие сочетаний клавиш, вращение колеса мыши, перемещение курсора, визуальные эффекты на экране (затемнение, рамка, эллипс, стрелка, подсказка-балун). Поддерживаемые действия (параметр **action**): **find_elements** — поиск элементов (**pid** обязателен; критерии отбора — **name**, **control_type** или **help_text**: без них внешняя компонента ничего не находит, в ответе будет пустой список и подсказка про критерий; необязательные параметры: **name** — точное совпадение имени, **control_type** — тип элемента (ControlType): Button, Text, Edit, ComboBox, Document, Pane, TabItem, MenuItem, CheckBox, RadioButton, Hyperlink, ListItem, Custom, Group и др., **help_text** — отбор по подсказке (HelpText), **window_title** — отбор по вхождению в заголовок окна без учёта регистра, **limit** — максимум элементов в ответе, 0 — вернуть все, по умолчанию 100), **get_element** — свойства элемента (требуется **element_id**), **get_children** — дочерние элементы (требуется **element_id**; необязательные **name**, **control_type** — отбор по вхождению), **get_parent** — родительский элемент (требуется **element_id**), **get_next** — следующий элемент (требуется **element_id**), **get_active** — активный элемент UI Automation (необязательный **pid** — проверка, что активный элемент принадлежит этому процессу), **click** — клик по элементу (требуется **element_id**; необязательный **click_type**: left (по умолчанию), right, double), **input_text** — ввод текста (требуется **value**; необязательные **element_id** — сначала клик по элементу для передачи фокуса, **delay** — задержка между символами в мс, по умолчанию 100), **press_keys** — сочетание клавиш (требуется **keys**, например Ctrl+S, ENTER, Alt+F4), **mouse_wheel** — вращение колеса мыши (требуется **direction**: forward или back; необязательный **keys** — клавиши-модификаторы), **move_cursor** — перемещение курсора (указать **element_id** либо **x** и **y**), **effect** — визуальный эффект (требуется **effect_type**: dim — затемнение вокруг области, frame — рамка, ellipse — эллипс, arrow — стрелка от центра экрана к области, balloon — подсказка-балун с текстом; цель — **element_id** либо **left** и **top** (необязательно **width** и **height**); необязательные параметры стиля: **text** (для balloon — обязательный текст подсказки; для dim — необязательная надпись; у рамки, эллипса и стрелки не применяется), **color** (число или имя цвета, например 'Красный'), **thickness**, **transparency**, **duration**, **frame_delay**, **font_name**, **font_size**, **font_color**, **background**, **radius**). Элементы адресуются идентификатором **element_id** из результата action='find_elements' — он действует, пока окно не изменилось. Внимание: действия выполняются в реальных окнах операционной системы — проверяйте PID процесса и найденный элемент перед кликом; перед кликом и вводом текста активизируйте окно инструментом **activate_process_os**, по неактивному окну клик не срабатывает. Требует включённую внешнюю компоненту VanessaExt.

## Связанные темы

- [Браузер и внешние приложения](../patterns/browser-and-external-ui.md)
- [Компоненты взаимодействия с ОС](../patterns/external-components.md)

Источник: [Vanessa Automation](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/AI/index.md); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
