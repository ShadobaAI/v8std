# Самодостаточный образ v8std MCP

Образ `v8std-mcp:latest` содержит MCP-сервер и сформированные
при сборке `pages.jsonl`, `search-vectors.jsonl`, `llms.txt` и `llms-full.txt`.
Контейнер не требует checkout репозитория, volume или генерации при старте.

## Локальная сборка

Запустите:

```cmd
build-v8std-mcp.cmd
```

Скрипт выполняет `docker build --no-cache -f Dockerfile.mcp`, поэтому все
артефакты создаются заново. Образ получает локальный тег `v8std-mcp:latest` и
готовый для публикации тег `<docker-hub-namespace>/v8std-mcp:latest`. Namespace
автоматически определяется из учетных данных `docker login`. Его можно явно
переопределить переменной окружения `V8STD_MCP_DOCKER_USER`. Автоматической
публикации нет.

При необходимости опубликуйте образ вручную:

```cmd
docker login
build-v8std-mcp.cmd
docker push <docker-hub-namespace>/v8std-mcp:latest
```

## Запуск сотрудником

Убедитесь, что образ уже загружен локально, и запустите контейнер:

```cmd
docker run --name v8std-mcp --restart unless-stopped -p 127.0.0.1:8766:8766 -d <docker-hub-namespace>/v8std-mcp:latest
```

В Windows те же команды выполняет:

```cmd
run-v8std-mcp.cmd
```

Без аргументов скрипт использует локальный образ `v8std-mcp:latest`. При необходимости
можно явно передать другой тег: `run-v8std-mcp.cmd <docker-hub-namespace>/v8std-mcp:latest`.
Скрипт не выполняет `docker pull`; обновление образа выполняется вручную:

```cmd
docker pull <docker-hub-namespace>/v8std-mcp:latest
```

После запуска MCP доступен по адресу `http://127.0.0.1:8766/mcp`.
