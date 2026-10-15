# Стандарты разработки 1С

Сайт: [v8std.ru](https://v8std.ru). MCP: [ai.v8std.ru](https://ai.v8std.ru/mcp).

## MCP fork с corporate, yaxunit и vanessa, без сайта

```bash
docker build -f Dockerfile.mcp -t v8std-mcp:latest .
docker run --name v8std --restart unless-stopped -p 127.0.0.1:8766:8766 -d v8std-mcp:latest
```

Образ содержит локальные документы `corporate`, `yaxunit` и `vanessa`, индекс и все 11 методов
fork. При запуске не нужны сайт, checkout, volume или скачивание индекса.
Адрес MCP: `http://127.0.0.1:8766/mcp`.

Windows: `build-v8std-mcp.cmd`, затем `run-v8std-mcp.cmd <namespace>/v8std-mcp:latest`.
Сборщик выбирает namespace Docker Hub из `docker login` или `V8STD_MCP_DOCKER_USER`;
публикация выполняется отдельно. [Подробности](docs/mcp-image.md).

## Разработка сайта

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-build.lock
VIRTUAL_ENV="$PWD/.venv" bash scripts/zensical_docs.sh serve --dev-addr=127.0.0.1:8000
```

Контент находится в `docs/`, шаблоны — в `overrides/`. Сборка сайта не требует MCP.

## Устройство репозитория

- `scripts/`, `data/`, конфигурации в корне — сборка сайта и индекса.
- `runtime/` — MCP-сервис; имя не конфликтует с Python SDK `mcp`.
- `delivery/` — образы, публикация артефактов и доставка на VPS.
- `dev/` — подготовка контента и инструменты разработчика.
- `tests/` — действующие проверки; `spec/` — цель и устройство поставки.

Python-команды из новых каталогов запускаются из корня через `python -m`,
например `.venv/bin/python -m dev.content.acc_diagnostics generate --check`.
Тестовые зависимости: `.venv/bin/python -m pip install --require-hashes -r dev/requirements-test.lock`.
Тесты: `.venv/bin/python -m unittest discover -s tests -t .`.

## Готовые образы

Публичный и локальный MCP используют Streamable HTTP. Отдельный транспорт для локального запуска не требуется.

`delivery/local/compose.mcp.yaml` запускает готовый образ автора только с публичным
индексом. Он не содержит `corporate`, `yaxunit`, `vanessa` и дополнительных методов fork.
`delivery/local/compose.yaml` предназначен для сайта и совместного запуска с MCP.

[Целевая поставка](spec/delivery-target.md) · [Файлы сборки сайта](spec/local-site-build-files.md) ·
[План разделения](spec/repository-layout-plan.md)


## Навигация по знаниям через MCP

Ответы всех 11 инструментов используют ссылки вида `v8std:std437` и
`v8std:vanessa:patterns:project-layout`. Передайте такую ссылку целиком в
`v8std_get_page`, `v8std_get_section` или другой инструмент чтения; открывать
сайт для получения текста не требуется. Сохраняются canonical ID, секции и связи.
Если ссылка неоднозначна, `reference_candidates` перечисляет существующие
материалы для выбора, без произвольного первого совпадения.

В выдаче MCP нет полей `url`, `markdown_url`, `source_urls`. Известные ссылки
в тексте преобразуются во внутренние ссылки корпуса; у внешних источников
сохраняются названия. URL в примерах кода остаются буквальными данными.
Происхождение, полные тексты и хеши источников сохраняются в исходном корпусе,
manifest и source-map; представление сайта и ранжирование поиска не меняются.
Усечённый текст читается с большим `body_limit` или по известной секции через MCP.

Проверки: `python -m unittest tests.test_v8std_mcp_references
tests.test_v8std_mcp_presentation tests.test_v8std_mcp_server
tests.test_v8std_mcp_runtime tests.test_v8std_mcp_tools_only`.
