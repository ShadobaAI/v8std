---
id: vanessa:patterns:configuration-and-ci
title: "VAParams и запуск Vanessa в CI: параметры, приоритеты, статус"
description: "Как различаются загрузка настроек и пакетное исполнение, /C и переменные среды, статус завершения и отсутствие сценариев."
collection: "vanessa"
type: "pattern"
aliases: ["VAParams JSON", "настройки CI Vanessa", "StartFeaturePlayer", "приоритет параметров запуска", "код возврата Vanessa", "пустой прогон тестов"]
tags: ["vanessa", "configuration-and-ci", "VAParams JSON", "настройки CI Vanessa", "StartFeaturePlayer"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/CommandSetting/CommandSetting.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/ReturnStatus/ReturnStatus.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/JsonParams/JsonParamsRU.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/JsonParams/JsonParamsEN.md"]
---

# VAParams и запуск Vanessa в CI: параметры, приоритеты, статус

## Загрузка настроек и выполнение — разные режимы

`VAParams=PARAMS_PATH` загружает JSON-настройки. Само наличие этого параметра не запускает сценарии. `StartFeaturePlayer` включает пакетное выполнение по выбранным настройкам. `UseEditor` отдельно включает инициализацию редактора: документация командной строки описывает его отсутствие по умолчанию как экономию ресурсов.

```text
/C "VAParams=PARAMS_PATH;WorkspaceRoot=PROJECT_PATH;UseEditor"
/C "StartFeaturePlayer;VAParams=CI_PARAMS_PATH;WorkspaceRoot=PROJECT_PATH"
```

Это фрагменты параметров Vanessa, а не полная строка запуска платформы. Внешняя и встроенная обработка описаны в [готовности окружения](environment-readiness.md).

## Приоритеты и форма значений

В `/C` пары разделяются `;`, имя и значение — `=`. Булевый флаг без значения означает истину. Допустимы русское имя настройки или документированный английский alias. Для массива в командной строке значения перечисляются через запятую; JSON-структура клиентов требует экранирования внутренних `;` как `\;`.

Документированный приоритет: JSON-файл → параметры `/C` → `VANESSA_КЛЮЧ`. Переменные среды с этим префиксом предназначены для CI-режима с `StartFeaturePlayer`; для локальной разработки документация рекомендует загрузку JSON. Это механизм настроек Vanessa, отдельный от секретов и переменных окружения проекта.

## Контрольные настройки

| Задача | Документированный параметр |
| --- | --- |
| Корень проекта | `WorkspaceRoot`, `КаталогПроекта` / `projectpath` |
| Исполняемые features | `КаталогФич` / `featurepath` |
| Экспортные библиотеки | `КаталогиБиблиотек` / `librarycatalogs` |
| Файл статуса | `ВыгружатьСтатусВыполненияСценариевВФайл`, `ПутьКФайлуДляВыгрузкиСтатусаВыполненияСценариев` |
| Игнорировать сохранённые настройки пользователя | `DisableLoadConfig` |
| Не загружать старую таблицу клиентов | `DisableLoadTestClientsTable` |
| Не загружать прежний feature при открытии | `DisableFeatureLoadOnOpenForm` |

Имена остальных полей зависят от редакции VAParams; подсказка `Alt+H` позволяет узнать имя настройки в форме. Перечисленные механизмы не означают, что нужно отключить пользовательские настройки в каждом запуске.

## Что означает файл статуса

| Статус | Смысл по ReturnStatus |
| --- | --- |
| `0` | При исполнении не было ошибок |
| `1` | Ошибки сценариев |
| `2` | Ошибка контекста, подключения TestClient либо сетевого взаимодействия |
| `3` | Не найдено ни одного сценария |
| `4` | Не удалась тихая установка VanessaExt |

Наличие процесса, отчёта или status `0` без ожидаемого сценария не подтверждает нужное покрытие. Отсутствующий файл статуса отличается от status `0`. Status `2` описывает класс проблемы и сам по себе не подтверждает безопасность повторения действий с данными.

## Отдельные технологические режимы

`InstallExtensionsAndClose` устанавливает CFE и завершает сеанс; это не прогон тестов. Он несовместим с `StartFeaturePlayer`; результат установки (`0` или `5`) относится к отдельному файлу `InstallExtensionsResult`, а не к приведённым выше статусам сценариев. Существующее расширение с тем же именем обновляется. `QuietInstallVanessaExtAndClose` также завершает только подготовку компоненты.

Связанные темы: [жизненный цикл](execution-lifecycle.md), [профили клиентов](test-client-profiles.md), [артефакты](reporting-and-artifacts.md).

## Источники

[CommandSetting](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/CommandSetting/CommandSetting.md); [ReturnStatus](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/ReturnStatus/ReturnStatus.md); [JsonParamsRU](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/JsonParams/JsonParamsRU.md); [JsonParamsEN](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/JsonParams/JsonParamsEN.md).
