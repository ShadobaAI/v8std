# Стандарты разработки 1С

https://v8std.ru

## Локальный MCP

```bash
docker compose -f docker-compose/docker-compose.yml up -d v8std-mcp
```

<!-- BEGIN V8STD-FORK -->
MCP-сервер будет доступен на `http://127.0.0.1:8766/mcp` и читает локальный индекс
`docs/ai/pages.jsonl` из смонтированного репозитория.

Упрощенный запуск готового образа:

```bash
docker run --pull=always --name v8std -p 127.0.0.1:8766:8766 -d aleksp99/v8std-mcp:latest
```

```bash
codex mcp add v8std-local --url http://127.0.0.1:8766/mcp
```

### Самодостаточный MCP-образ

Для локальной сборки образа со всеми заранее сформированными MCP-артефактами:

```cmd
build-v8std-mcp.cmd
```

Скрипт всегда пересобирает образ без кеша с тегом
`<docker-hub-namespace>/v8std-mcp:latest`. Namespace определяется из учетных данных
`docker login`; при необходимости его можно переопределить переменной окружения
`V8STD_MCP_DOCKER_USER`. Скрипт не публикует образ.

Для запуска собранного образа без Docker Compose передайте его полный тег:

```cmd
run-v8std-mcp.cmd <docker-hub-namespace>/v8std-mcp:latest
```

Скрипт не выполняет `docker pull`. Другой тег образа при необходимости можно передать
первым аргументом: `run-v8std-mcp.cmd <docker-hub-namespace>/v8std-mcp:latest`.

Подробности и команды ручной публикации: [инструкция по сборке и запуску](docs/mcp-image.md).
<!-- END V8STD-FORK -->
