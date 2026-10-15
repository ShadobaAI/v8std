"""Validate packaged Vanessa corpus without accessing upstream."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

PATTERNS = {"environment-readiness", "exploration-recording", "steps-assertions", "gherkin-structure", "fixtures-idempotency", "execution-debugging", "modal-dialogs", "failure-classification"}
BASE_MCP_TOOLS = set("""activate_process_os check_syntax close_test_client execute_feature_step execute_form_actions find_form_elements frequently_used_steps get_active_window_data get_data_from_knowledge_base get_editor_state get_environment_data get_event_log_manager get_event_log_test_client get_extension_list get_form_analysis get_form_element_data get_info_about_line_scenario get_object_attributes get_process_list_os get_table_data get_test_results get_vanessa_automation_state get_window_list_os get_window_list_testclient get_window_screenshot_os input_text_to_active_field load_features manage_app manage_breakpoints manage_clipboard manage_command_interface manage_form_elements manage_test_client manage_test_client_profiles manage_uiautomation manage_variables open_feature_file run_scenario save_table_document_to_file search_for_steps_by_keywords select_scenario select_step speak_text stop_scenario user_actions_recording voice_notification window_management""".split())
DISPOSITIONS = {"curated", "historical", "release_history", "navigation", "example_workflow", "pointer_only", "translation"}
UPSTREAM = "Pr-Mex/vanessa-automation"
DEVKIT = "1c-neurofish/onec-client-mcp-devkit"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("invalid relative path")
    if value.startswith("/") or any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError("invalid relative path")
    return PurePosixPath(value)


def frontmatter_id(content):
    lines = content.decode("utf-8-sig").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("document requires frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("unclosed document frontmatter") from error
    values = [line.removeprefix("id:").strip() for line in lines[1:end] if line.startswith("id:")]
    if len(values) != 1:
        raise ValueError("frontmatter requires one canonical id")
    value = values[0]
    if len(value) > 1 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    if not re.fullmatch(r"vanessa:(?:patterns|mcp):[a-z0-9_-]+", value):
        raise ValueError("invalid frontmatter id")
    return value


def validate_source_map(data, *, input_paths=None, pattern_ids=None):
    if data["format_version"] != 1 or not isinstance(data["manual_version"], str) or not data["manual_version"].strip():
        raise ValueError("unsupported source map")
    if not isinstance(data["scope"], str) or not data["scope"].strip():
        raise ValueError("source map requires explicit scope")
    required = data["required_patterns"]
    if not isinstance(required, list) or any(not isinstance(x, str) or not re.fullmatch(r"vanessa:patterns:[a-z0-9-]+", x) for x in required):
        raise ValueError("invalid required pattern ids")
    if required != sorted(set(required)) or not {"vanessa:patterns:" + x for x in PATTERNS}.issubset(required):
        raise ValueError("source map must retain baseline patterns and unique sorted ids")
    entries = data["entries"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("empty source map")
    paths, folded = set(), set()
    for entry in entries:
        path = entry["path"]
        safe_path(path)
        if path in paths or path.casefold() in folded:
            raise ValueError("duplicate source map path")
        paths.add(path)
        folded.add(path.casefold())
        if entry["disposition"] not in DISPOSITIONS or not isinstance(entry["note"], str) or not entry["note"].strip():
            raise ValueError("source map requires disposition and concrete note")
        refs = entry["patterns"]
        if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs) or len(refs) != len(set(refs)) or not set(refs).issubset(required):
            raise ValueError("unknown or duplicate source map pattern")
        if entry["disposition"] == "curated" and not refs:
            raise ValueError("curated source requires patterns")
    if input_paths is not None and paths != set(input_paths):
        raise ValueError("source map differs from source inventory: unmapped=" + repr(sorted(set(input_paths)-paths)) + "; absent=" + repr(sorted(paths-set(input_paths))))
    if pattern_ids is not None and set(required) != set(pattern_ids):
        raise ValueError("required patterns differ from packaged patterns")
    return paths


def validate_vanessa_snapshot(root: Path) -> None:
    destination = root / "docs/vanessa"
    if not destination.exists():
        return
    try:
        manifest = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
        version = str(manifest["generator"]["version"])
        if manifest["format_version"] != 1 or version not in {"1", "2"}:
            raise ValueError("unsupported format or generator")
        if manifest["generator"]["path"] != "scripts/sync_vanessa_docs.py":
            raise ValueError("invalid generator provenance path")
        generator = root / "scripts/sync_vanessa_docs.py"
        if generator.is_file() and digest(generator.read_bytes()) != manifest["generator"]["sha256"]:
            raise ValueError("generator differs from snapshot")
        coverage = manifest["coverage"]
        if coverage["complete"] is not True or coverage["runtime_schema_verified"] is not False:
            raise ValueError("incomplete or unsubstantiated coverage")
        sources = manifest["sources"]
        if len(sources) != 2 or {s["project"] for s in sources} != {UPSTREAM, DEVKIT}:
            raise ValueError("missing source provenance")
        sources_by_project = {}
        for source in sources:
            inputs = source["inputs"]
            revision = "sha256:" + digest(json.dumps(inputs, sort_keys=True, ensure_ascii=False).encode())
            if source["content_revision"] != revision or not inputs:
                raise ValueError("invalid source revision")
            seen, folded = set(), set()
            for item in inputs:
                path = item["path"]
                safe_path(path)
                if path.casefold() in folded or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
                    raise ValueError("invalid source input path or hash")
                seen.add(path)
                folded.add(path.casefold())
            sources_by_project[source["project"]] = seen
        license = manifest["license"]
        if license["spdx"] != "BSD-3-Clause" or license["path"] != "LICENSE":
            raise ValueError("invalid license provenance")
        paths, ids = set(), set()
        for item in [*manifest["documents"], license]:
            raw = item["path"]
            path = safe_path(raw)
            if raw in paths:
                raise ValueError("invalid or duplicate packaged path")
            paths.add(raw)
            content = (destination / path).read_bytes()
            if digest(content) != item["sha256"]:
                raise ValueError("changed packaged document: " + raw)
            if "id" in item:
                expected = "vanessa:" + ":".join(path.with_suffix("").parts)
                if item["id"] != expected or expected in ids or path.parts[0] not in {"patterns", "mcp"}:
                    raise ValueError("invalid or duplicate stable id")
                if frontmatter_id(content) != expected:
                    raise ValueError("document id differs from manifest")
                ids.add(expected)
        actual = {p.relative_to(destination).as_posix() for folder in ("mcp", "patterns") for p in (destination/folder).glob("*.md")}
        if actual != paths - {"LICENSE"}:
            raise ValueError("documents differ from manifest")
        patterns = {x for x in ids if x.startswith("vanessa:patterns:")}
        tools = {x.removeprefix("vanessa:mcp:") for x in ids if x.startswith("vanessa:mcp:")}
        if not {"vanessa:patterns:" + x for x in PATTERNS}.issubset(patterns):
            raise ValueError("missing baseline curated patterns")
        if not BASE_MCP_TOOLS.issubset(tools) and version == "2":
            raise ValueError("missing baseline MCP cards")
        if coverage["patterns"] != len(patterns) or coverage["documented_tools"] != len(tools) or not tools:
            raise ValueError("incorrect document coverage")
        if version == "1":
            if patterns != {"vanessa:patterns:" + x for x in PATTERNS}:
                raise ValueError("legacy snapshot requires baseline patterns")
        else:
            provenance = manifest["source_map"]
            if provenance["path"] != "source-map.json":
                raise ValueError("invalid source map provenance path")
            raw = (destination / provenance["path"]).read_bytes()
            if digest(raw) != provenance["sha256"]:
                raise ValueError("changed source map")
            registry = json.loads(raw)
            upstream_inputs = sources_by_project[UPSTREAM]
            if "LICENSE" not in upstream_inputs or sources_by_project[DEVKIT] != {"README.md"}:
                raise ValueError("missing license or devkit input")
            upstream_license = next(item for item in next(s for s in sources if s["project"] == UPSTREAM)["inputs"] if item["path"] == "LICENSE")
            if upstream_license["sha256"] != license["sha256"]:
                raise ValueError("license differs from upstream input")
            validate_source_map(registry, input_paths=upstream_inputs-{"LICENSE"}, pattern_ids=patterns)
            counts = {kind: sum(e["disposition"] == kind for e in registry["entries"]) for kind in sorted(DISPOSITIONS)}
            if coverage["classified_sources"] != len(registry["entries"]) or coverage["dispositions"] != counts or coverage["manual_version"] != registry["manual_version"] or coverage["scope"] != registry["scope"]:
                raise ValueError("incorrect source map coverage")
    except (OSError, KeyError, TypeError, AttributeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"invalid Vanessa snapshot: {error}") from error

