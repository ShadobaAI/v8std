---
title: База знаний YaXUnit
description: Компактный API ядра и паттерны использования YaXUnit.
index_for_ai: false
publish_publicly: false
---

# База знаний YaXUnit

`api/` генерируется из экспортных методов выбранной ревизии ядра, `patterns/` содержит короткие проверенные рецепты. Полная официальная документация сюда намеренно не копируется.

Каждый curated pattern задаёт явный canonical `id` вида `yaxunit:patterns:<name>` и публикуется как одна компактная retrieval-запись для прямого `v8std_get_page`. Прежний структурный ID с суффиксом `:overview` сохраняется как alias. Изменение заголовков не должно менять canonical ID; `v8std_search` предназначен для обнаружения неизвестного знания, а не для загрузки заранее известного pattern.

Обновление API выполняет `scripts/sync_yaxunit_docs.py`; ревизия, исходные хеши и число экспортов записываются в `manifest.json`.
