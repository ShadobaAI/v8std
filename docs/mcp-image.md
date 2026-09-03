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
артефакты создаются заново. Образ получает один готовый для публикации тег
`<docker-hub-namespace>/v8std-mcp:latest`. Namespace
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
docker run --name v8std --restart unless-stopped -p 127.0.0.1:8766:8766 -d <docker-hub-namespace>/v8std-mcp:latest
```

В Windows собранный образ запускается с его полным тегом:

```cmd
run-v8std-mcp.cmd <docker-hub-namespace>/v8std-mcp:latest
```

Без аргументов скрипт по-прежнему использует локальный образ `v8std-mcp:latest`, но
`build-v8std-mcp.cmd` этот дополнительный тег не создает.
Скрипт не выполняет `docker pull`; обновление образа выполняется вручную:

```cmd
docker pull <docker-hub-namespace>/v8std-mcp:latest
```

После запуска MCP доступен по адресу `http://127.0.0.1:8766/mcp`.
