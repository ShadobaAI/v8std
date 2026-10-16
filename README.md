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

## Поддержка форка

Этот форк [zeegin/v8std](https://github.com/zeegin/v8std) поставляет только MCP.
Дополнительные коллекции: `corporate`, `yaxunit`, `vanessa`. Общие стандарты,
диагностики и алгоритмы поиска обновляются из upstream с сохранением исправлений форка.

- [Обновление upstream и сохранённые исправления](spec/fork-maintenance.md).
- [Сборка, публикация и запуск Docker-образа](docs/mcp-image.md).
- Локальные проверки: `python -m dev.fork.check` и проверка образа без сети.
- CI автора сохранён без изменений; GitHub Actions отключены в настройках форка. Выпуск: ручной запуск `build-v8std-mcp.cmd`, затем ручной `docker push`.

Исходники сайта и VPS-поставки upstream сохранены для упрощения слияний;
Эти продукты не входят в ручной сценарий поставки форка. Готовый образ автора
`ghcr.io/zeegin/v8std-mcp:stable` содержит публичный корпус и не заменяет образ форка.

Для разработки используйте Python 3.12 и зависимости из `dev/requirements-test.lock`.
Набор проверок форка запускается через `python -m dev.fork.check`;
перед ним нужны `python scripts/generate_ai_artifacts.py` и
`python scripts/generate_search_vectors.py`. Тесты не требуют сборки HTML-сайта.

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
