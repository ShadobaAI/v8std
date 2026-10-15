"""Explicit deterministic sync of Vanessa documentation; never reads 1C source."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from v8std_vanessa_snapshot import BASE_MCP_TOOLS, DISPOSITIONS, digest, frontmatter_id, safe_path, validate_source_map

VERSION = "2"
SOURCE = "docs/AI/index.md"
EXAMPLES = ("docs/AI/examples/ЗапускаемПромптыВРучную/InstructionsResearch.md", "docs/AI/examples/ЗапускаемПромптыВРучную/InstructionsWriteScenario.md")
TOOL_ROW = re.compile(r"^\| \*\*([a-z][a-z0-9_]*)\*\* \| (.*) \|$", re.MULTILINE)

def tool_rows(document):
    rows = TOOL_ROW.findall(document)
    candidates = [line for line in document.splitlines() if line.startswith("| **")]
    if not rows or len(rows) != len(candidates) or len(rows) != len({name for name, _ in rows}):
        raise ValueError("missing or duplicate documented MCP tools")
    return dict(rows)

def source_snapshot(root, project, paths, revision):
    inputs = []
    for p in sorted(paths):
        safe_path(p)
        target = (root / p).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError("source escapes upstream root: " + p)
        inputs.append({"path": p, "sha256": digest(target.read_bytes())})
    return {"project": project, "revision": revision, "content_revision": "sha256:" + digest(json.dumps(inputs, sort_keys=True, ensure_ascii=False).encode()), "inputs": inputs}

def source_inventory(upstream, registry):
    paths = {p.relative_to(upstream).as_posix() for p in (upstream / "docs").rglob("*") if p.is_file() and p.suffix.lower() == ".md"}
    paths.update({"README.md", "examples/README.md"})
    paths.update(e["path"] for e in registry["entries"] if e["path"].lower().endswith(".feature"))
    return paths

def curated_patterns(destination, registry):
    paths = sorted(p for p in (destination / "patterns").iterdir() if p.is_file() and p.suffix.lower() == ".md")
    documents = []
    ids = set()
    for path in paths:
        content = path.read_bytes()
        expected = "vanessa:patterns:" + path.stem
        if frontmatter_id(content) != expected or expected in ids:
            raise ValueError("invalid or duplicate curated pattern id: " + path.name)
        ids.add(expected)
        documents.append({"id": expected, "path": path.relative_to(destination).as_posix(), "sha256": digest(content)})
    validate_source_map(registry, pattern_ids=ids)
    return documents

def related_patterns(name):
    groups = (
        ({"open_feature_file", "get_editor_state", "check_syntax", "load_features", "select_scenario", "select_step", "get_info_about_line_scenario", "manage_breakpoints"}, (("editor-workflow", "Редактор, файлы и инструменты"),)),
        ({"run_scenario", "stop_scenario", "execute_feature_step", "manage_breakpoints", "select_scenario", "select_step"}, (("execution-debugging", "Запуск и отладка сценария"), ("execution-lifecycle", "Отбор, ожидания и статусы выполнения"))),
        ({"get_test_results", "get_event_log_manager", "get_event_log_test_client", "get_window_screenshot_os", "save_table_document_to_file"}, (("reporting-and-artifacts", "Отчёты и диагностические артефакты"),)),
        ({"user_actions_recording"}, (("exploration-recording", "Исследование формы и запись действий"), ("external-components", "Компоненты и режимы записи"))),
        ({"execute_form_actions", "find_form_elements", "get_active_window_data", "get_form_analysis", "get_form_element_data", "get_object_attributes", "get_table_data", "manage_command_interface", "manage_form_elements", "get_window_list_testclient", "save_table_document_to_file"}, (("form-assertions-and-tables", "Проверки форм и таблиц"), ("modal-dialogs", "Модальные окна"))),
        ({"manage_test_client", "manage_test_client_profiles", "close_test_client"}, (("test-client-profiles", "Подключения и параметры TestClient"),)),
        ({"activate_process_os", "get_process_list_os", "get_environment_data", "get_vanessa_automation_state", "get_window_list_os", "get_window_screenshot_os"}, (("environment-readiness", "Окружение менеджера и клиента"), ("external-components", "Возможности внешней компоненты"))),
        ({"get_vanessa_automation_state", "get_test_results"}, (("execution-debugging", "Состояние и результаты выполнения"),)),
        ({"get_extension_list"}, (("external-components", "VanessaExt и VAExtension"), ("extension-capabilities", "Возможности расширения клиентской базы"))),
        ({"frequently_used_steps", "search_for_steps_by_keywords", "get_info_about_line_scenario"}, (("steps-assertions", "Библиотека шагов и проверки"), ("subscenarios-and-libraries", "Библиотеки и экспортные сценарии"))),
        ({"get_data_from_knowledge_base"}, (("catalog", "Каталог справки Vanessa"),)),
        ({"manage_app", "manage_clipboard", "manage_uiautomation", "input_text_to_active_field", "window_management"}, (("browser-and-external-ui", "Браузер и внешние приложения"), ("external-components", "Компоненты взаимодействия с ОС"))),
        ({"manage_variables"}, (("variables-and-parameters", "Переменные и параметры"), ("embedded-code-and-context", "Вычисления и контекст"))),
        ({"speak_text", "voice_notification"}, (("video-and-instructions", "Озвучка и автоинструкции"), ("video-authoring", "Подготовка видеоинструкций"))),
    )
    matches = [item for names, topics in groups if name in names for item in topics]
    return list(dict.fromkeys(matches)) or [("catalog", "Каталог справки Vanessa")]

def render_card(name, description, source):
    revision = source["revision"] or "Git revision неизвестна; точная редакция определена content_revision и input SHA-256 в manifest.json"
    url = "https://github.com/Pr-Mex/vanessa-automation/blob/" + (source["revision"] or "develop") + "/" + SOURCE
    links = "\n".join(f"- [{title}](../patterns/{stem}.md)" for stem, title in related_patterns(name))
    return f"""---
id: vanessa:mcp:{name}
title: "Vanessa MCP: {name}"
description: "Документированное назначение и ограничения {name}."
collection: vanessa
type: reference
tags: [vanessa, mcp, {name}]
publish_publicly: false
source_urls: ["{url}"]
---

# Vanessa MCP: {name}

## Контракт и версия

Справочная карточка из `{SOURCE}`. {revision}.
Версия runtime и JSON Schema этим snapshot не подтверждены. Полный контракт конкретного сервера публикуется в `tools/list` и `inputSchema`. Документированное описание ниже может раскрывать отдельные параметры и эффекты, но не устанавливает отсутствующие в нём типы, обязательность, enum или структуру ответа.

## Назначение, документированные параметры и ответ

{description}

## Связанные темы

{links}

Источник: [Vanessa Automation]({url}); точные входные хеши и границы полноты — `docs/vanessa/manifest.json`. BSD-3-Clause: `docs/vanessa/LICENSE`.
"""

def sync(upstream, devkit, repository, *, revision=None, devkit_revision=None, check=False):
    destination = repository / "docs/vanessa"
    registry_bytes = (destination / "source-map.json").read_bytes()
    registry = json.loads(registry_bytes)
    validate_source_map(registry)
    inventory = source_inventory(upstream, registry)
    validate_source_map(registry, input_paths=inventory)
    source = source_snapshot(upstream, "Pr-Mex/vanessa-automation", inventory | {"LICENSE"}, revision)
    dependency = source_snapshot(devkit, "1c-neurofish/onec-client-mcp-devkit", ("README.md",), devkit_revision)
    rows = tool_rows((upstream / SOURCE).read_text(encoding="utf-8-sig"))
    if not BASE_MCP_TOOLS.issubset(rows):
        raise ValueError("missing baseline documented MCP tool ids")
    files = {f"mcp/{n}.md": render_card(n, d, source).encode() for n, d in sorted(rows.items())}
    files["LICENSE"] = (upstream / "LICENSE").read_bytes()
    documents = [{"id": "vanessa:mcp:" + Path(p).stem, "path": p, "sha256": digest(c)} for p, c in files.items() if p.endswith(".md")]
    patterns = curated_patterns(destination, registry)
    documents.extend(patterns)
    manifest = {
        "format_version": 1,
        "generator": {"path": "scripts/sync_vanessa_docs.py", "version": VERSION, "sha256": digest(Path(__file__).read_bytes())},
        "sources": [source, dependency],
        "source_map": {"path": "source-map.json", "sha256": digest(registry_bytes)},
        "license": {"spdx": "BSD-3-Clause", "path": "LICENSE", "sha256": digest(files["LICENSE"])},
        "coverage": {
            "complete": True, "scope": registry["scope"], "manual_version": registry["manual_version"],
            "documented_tools": len(rows), "patterns": len(patterns), "runtime_schema_verified": False,
            "classified_sources": len(registry["entries"]),
            "dispositions": {kind: sum(e["disposition"] == kind for e in registry["entries"]) for kind in sorted(DISPOSITIONS)},
        },
        "documents": sorted(documents, key=lambda x: x["id"]),
    }
    files["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    existing = {p.relative_to(destination).as_posix() for p in (destination / "mcp").glob("*.md")}
    if existing - set(files):
        raise ValueError("obsolete MCP cards: explicit review/removal required")
    if check:
        stale = [n for n,c in files.items() if not (destination/n).is_file() or (destination/n).read_bytes() != c]
        if stale:
            raise ValueError("stale Vanessa snapshot: " + ", ".join(stale))
    else:
        for n,c in files.items():
            target=destination/n
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(c)
    return manifest

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--devkit", type=Path, required=True)
    parser.add_argument("--revision", help="Known revision; omit for an archive with unknown Git revision")
    parser.add_argument("--devkit-revision")
    parser.add_argument("--check", action="store_true")
    opts=parser.parse_args()
    manifest=sync(opts.upstream, opts.devkit, Path(__file__).resolve().parents[1], revision=opts.revision, devkit_revision=opts.devkit_revision, check=opts.check)
    print(json.dumps(manifest["coverage"], ensure_ascii=False))

if __name__ == "__main__":
    main()
