---
id: vanessa:patterns:catalog
title: "Vanessa: карта практических паттернов"
description: "Навигация по задачам UI-тестирования: каталоги, сценарии, данные, клиенты, исполнение, проверки, интеграции и диагностика."
collection: "vanessa"
type: "pattern"
aliases: ["паттерны Vanessa", "карта знаний Vanessa", "с чего начать UI тесты", "рекомендации организации тестирования Vanessa"]
tags: ["vanessa", "каталог", "навигация", "паттерны"]
publish_publicly: false
---

# Vanessa: карта практических паттернов

Компактные рецепты сгруппированы по задачам; это переработка текстовой документации, а не копия руководства. Один рецепт соответствует стабильному ID `vanessa:patterns:имя`; связанные темы образуют переходы между страницами.

## Структура проекта и тестов

- [Каталоги features, библиотек, данных, макетов и результатов](project-layout.md).
- [Выбор конструкции Gherkin](gherkin-structure.md).
- [Заголовок, Контекст и секции feature](feature-sections.md).
- [Один сценарий на нескольких наборах Примеров](scenario-outlines.md).
- [Теги, фильтры и исключённые сценарии](tags-and-selection.md).
- [Повторяющееся поведение и экспортные библиотеки](subscenarios-and-libraries.md).
- [Переменные, параметры, таблицы и многострочный текст](variables-and-parameters.md).
- [Условия, циклы, Попытка/Исключение](conditions-loops-exceptions.md).

## Данные и проверки

- [Собственные данные, внешние наборы и эталонная база](test-data-strategies.md).
- [Повторяемость и частичный сбой](fixtures-idempotency.md).
- [Генерация smoke по метаданным и исключения](smoke-test-generation.md).
- [Библиотечное действие и критерий проверки](steps-assertions.md).
- [Состояние формы, доступность, MXL и маски](form-assertions-and-tables.md).
- [Асинхронность, ожидания и паузы](synchronization-and-waits.md).

## Окружение, выполнение и диагностика

- [Менеджер, TestClient, MCP и компоненты](environment-readiness.md).
- [VAParams, /C, переменные среды и статусы CI](configuration-and-ci.md).
- [Сохранённые настройки и режимы](runtime-settings.md).
- [Подключения, порты и пользователи клиентов](test-client-profiles.md).
- [Начало, остановка, повтор и завершение выполнения](execution-lifecycle.md).
- [MCP-режимы запуска и полнота результата](execution-debugging.md).
- [Allure, JUnit, вложения, журналы и снимки](reporting-and-artifacts.md).
- [Тест, продукт, данные, инфраструктура и неизвестный исход](failure-classification.md).
- [Различия CI/local, эталон, версия и совместимость](compatibility-and-troubleshooting.md).

## Исследование UI и расширения

- [Анализ формы и запись Turbo Gherkin](exploration-recording.md).
- [Навигация редактора, таблицы и точки останова](editor-workflow.md).
- [Окна, модальные диалоги и неполная цепочка действий](modal-dialogs.md).
- [Выбор/сохранение файла в thin/thick и web](files-and-dialogs.md).
- [Роли VanessaExt и VAExtension](external-components.md).
- [Возможности расширения, контексты и побочные эффекты](extension-capabilities.md).
- [Код менеджера, клиента и серверные выражения](embedded-code-and-context.md).
- [Single, полная поставка и свои шаги](runtime-distribution-and-custom-steps.md).

## Интеграции и специальные режимы

- [Несколько баз, роли, обмены и RAT](integration-multiple-bases.md).
- [Chrome debug, web socket, HTML и UI Automation](browser-and-external-ui.md).
- [Мобильный клиент, приложение и adb](mobile-testing.md).
- [Почта SMTP/IMAP и проверка доставки](email-testing.md).
- [Настройка видео, озвучки и автоинструкций](video-and-instructions.md).
- [Авторские директивы видео и TTS](video-authoring.md).
- [Интерактивные уроки и исполнение без основной формы](onboarding-and-embedded-run.md).

## Справка, навык и проект

Здесь находятся факты Vanessa, синтаксис, варианты решения, условия и ограничения версий. Порядок действий ИИ, проверка полномочий, управление блокировками и отчёт о задаче принадлежат навыку. Конкретные базы, пути, credentials и локальные соглашения принадлежат профилю и тестовому проекту.

Карточки `vanessa:mcp:имя_инструмента` описывают документированную семантику MCP; фактические параметры исполнения задаёт подключённый runtime. Специализированные инструменты `get_pattern/get_api_card` в v8std относятся к YAxUnit; Vanessa доступна через поиск, полную страницу и секцию.

## Границы источников

Основное руководство — MainHelp 1.2.043.1, вместе с тематическими Markdown-страницами и точными Gherkin-примерами. Карта `source-map.json` классифицирует текущие источники, исторические версии, переводы, release history и проектные AI-примеры. Ссылки только на видео и синтаксис исключительно на картинках отмечены как ограничения: они не превращены в вымышленные исполняемые шаги.

Советы конкретного учебного проекта, например обязательный `png/`, фиксированная ERP-база или запрет Контекста, не являются универсальной структурой Vanessa. Схема каталогов в рецепте явно обозначена как прикладная рекомендация на основе механизмов фреймворка.

## Источники

[Оглавление MainHelp](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MainHelp/index.MD), [документация Vanessa](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/index.md). Редакции и SHA-256 зафиксированы в manifest, Git revision архива не выдумывается.
