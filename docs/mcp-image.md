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
артефакты создаются заново. Результат сохраняется только локально с тегом
`v8std-mcp:latest`; автоматической публикации нет.

При необходимости опубликуйте образ вручную:

```cmd
docker login
docker tag v8std-mcp:latest <docker-hub-namespace>/v8std-mcp:latest
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
