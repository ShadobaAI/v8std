# Поддержка Docker MCP форка

Основной сценарий ShadobaAI/v8std — самодостаточный Docker-образ с MCP по
Streamable HTTP на порту 8766. Сборка выполняется вручную через
`build-v8std-mcp.cmd`, публикация в Docker Hub — отдельным `docker push`.
Сайт и VPS автора не входят в этот сценарий. Их исходники и
`.github/workflows/ci.yml` сохранены в версии upstream для упрощения обновлений.
GitHub Actions отключены в настройках ShadobaAI/v8std (проверено через API
2026-10-16: `enabled: false`). Поэтому push не запускает CI автора, а его файл
остаётся без отличий от upstream. При следующем обновлении сохраняйте эту настройку.

## Приоритеты при обновлении

- `docs/corporate`, `docs/yaxunit`, `docs/vanessa`: сохранять документы форка,
  manifest, source-map, лицензии и стабильные ID. Обновления YaXUnit/Vanessa
  выполнять отдельно штатными `scripts/sync_*_docs.py`.
- В остальных общих файлах брать изменения zeegin/v8std, сохраняя исправления
  форка и интеграцию трёх коллекций. Не применять `git merge -X theirs`:
  это способно молча удалить нужные изменения внутри конфликтующих файлов.
- Использовать обычный merge: его второй родитель фиксирует принятый upstream
  и уменьшает объём следующего слияния. Не копировать дерево поверх форка.

## Проверенные отличия от upstream

| Отличие | Зачем сохранять | Проверка |
| --- | --- | --- |
| Пустые ID исключены из ignored refs | Не удалять чужие ссылки с фрагментами из-за неиндексируемого README | `tests.test_fork_integration` |
| `FastMCPSettings.model_rebuild()` | Устранить предупреждение о незавершённой модели lifespan при реальном запуске SDK | Запуск wire-тестов с `-W error` |
| Валидация ID, метаданных и manifest | Обнаруживать дубликаты и повреждение vendored документов до сборки образа | `tests.test_knowledge_collections`, `tests.test_vanessa_collections` |
| Фильтр collections и дополнительные типы | Искать корпоративные правила и справочники YaXUnit/Vanessa | Тесты коллекций и offline smoke |
| 11 инструментов и ссылки `v8std:` | Читать весь корпус через MCP, включая компактные карточки и секции | `tests.test_v8std_mcp_references`, `tests.test_v8std_mcp_tools_only` |
| Курсор учитывает collections | Отклонять продолжение при изменившемся фильтре даже с теми же результатами | `tests.test_fork_integration` |
| Порог hybrid не применяется при явном выборе дополнительных коллекций | Сохранить поиск в малых corporate/YaXUnit/Vanessa; порог upstream откалиброван на публичном корпусе | `tests.test_knowledge_collections` |
| Локальные `--pages` и `--vectors` | Исключить замену полного индекса публичным snapshot при запуске | `tests/mcp_fork_image_smoke.py` с `--network none` |

`llms.ignore` у стандартов исключает их из `llms.txt`, но не из MCP-индекса.
Приватность публикации определяется отдельно от включения документа в MCP.

## Следующее обновление

Из основного checkout с чистым рабочим деревом:

```bash
# Один раз, если remote ещё не настроен:
git remote add upstream https://github.com/zeegin/v8std.git
git fetch origin
git pull --ff-only origin main
git fetch upstream
python -m dev.fork.upstream_status
git rev-parse HEAD
git merge --no-commit --no-ff upstream/main
```

Сохранить напечатанный SHA форка как `BASE`. Разрешить конфликты с учётом таблицы,
затем проверить сохранность трёх разделов до коммита:

```bash
python -m dev.fork.upstream_status --verify-protected BASE
python -m pip install --require-hashes -r dev/requirements-test.lock
python scripts/generate_ai_artifacts.py
python scripts/generate_search_vectors.py
python -W error -m unittest tests.test_v8std_mcp_snippet.SnippetWireTests tests.test_v8std_mcp_runtime.RuntimeTests.test_official_http_discovery_before_ready_and_session_end_does_not_close_index
python -m dev.fork.check
python -m dev.checks.search_benchmark
docker build -f Dockerfile.mcp -t v8std-mcp:check .
docker run --name v8std-fork-check --network none -d v8std-mcp:check
docker exec -i v8std-fork-check python - < tests/mcp_fork_image_smoke.py
docker rm -f v8std-fork-check
git add <проверенные-файлы>
git commit
git push origin main
```

Для Windows вместо перенаправления stdin:
`Get-Content -Raw tests\mcp_fork_image_smoke.py | docker exec -i v8std-fork-check python -`.
Тестовую Python-среду создавать на Python 3.12; процессные проверки выполнять в Linux.
Проверки выполняются локально. Сборка проверяется без сети и без перезапуска
рабочего контейнера. Выпуск образа и обновление контейнера выполняются отдельно
по [инструкции](../docs/mcp-image.md).

Исторический `snippet_benchmark` upstream требует полного равенства результатов
обычного поиска с публичной базовой версией. Форк проверяет поведение snippet
набором unit/wire-тестов: у его результата дополнительные метаданные, ссылки и
коллекции, поэтому сравнение с публичным ответом на полное равенство неприменимо.

## Интеграция 2026-10-16

Исходный форк: `a812bed`; upstream: `2d4c358`; общая база: `919daef`.
Приняты 25 upstream-коммитов: стандарты 800–802 и исправления существующих,
калибровка поиска, пустая выдача без совпадений, курсоры, журнал клиента и поиска,
исправления VPS-выкладки и тесты. Три дополнительных раздела сохранены побайтно
в Git. Локальная копия из Downloads на момент сравнения совпадала с upstream.

Конфликты в index/runtime/server объединены вручную: сохранены расширения форка,
добавлены cursor/total/next_cursor и журнал клиента. Публичный snapshot по-прежнему
отделён от полного Docker-корпуса. Его тест и тест лицензий больше не требуют
предварительной сборки HTML-сайта.
Сгенерированные `docs/ai` и `docs/llms*.txt` исключены из Docker-контекста:
локальные тесты больше не сбрасывают кеш сборки своим индексом. Образ также
содержит лицензию и manifest YaXUnit рядом с метаданными Vanessa.
Тесты генератора используют один набор результатов для неизменяемого корпуса
класса, сокращая повторную генерацию больших `llms`-файлов при локальной проверке.
`dev.fork.check` запускает корпусные, поисковые, протокольные и контейнерные
проверки. Восемь модулей VPS-выкладки, установки, отката, host logging и CI-публикации автора
оставлены для отдельного запуска: они рассчитаны на его публичный runtime с
пятью инструментами. Все исходные тесты доступны через `unittest discover`; для выполнения им нужны соответствующие upstream-сценарии и зависимости.
Реальный образ форка проверяется со всеми 11 инструментами и ссылками `v8std:`;
общие проверки контейнера приведены к этому формату ссылок. Контроллер VPS и
его фикстуры взяты из upstream без адаптации под форк.

У двух общих запросов про Strategy/Observer до обновления уже были совпадения
Vanessa/YaXUnit выше нужного GoF-паттерна. В сценариях бенчмарка задана коллекция
`v8std`; в ней оба паттерна занимают первое место. Без фильтра поиск намеренно
остаётся общим по всем коллекциям. Проверки качества YaXUnit/Vanessa сохранены.
