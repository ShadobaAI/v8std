from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


VALID_COLLECTIONS = {"v8std", "corporate", "yaxunit"}
VALID_TYPES = {"standard", "diagnostic", "fix", "pattern", "service", "rule", "reference"}
VALID_CORPORATE_LEVELS = {"mandatory", "recommended", "reference"}
SECTION_COLLECTIONS = {"corporate", "yaxunit"}

H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
H3_RE = re.compile(r"^###\s+(?P<title>.+?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)]\([^)]+\)")
MARKDOWN_MARKUP_RE = re.compile(r"[`*_~<>]")
HTML_TAG_RE = re.compile(r"<[^>]+>")
SAFE_ID_RE = re.compile(r"[^a-z0-9а-яё]+", re.IGNORECASE)
MAX_SECTION_CHARS = 9000


def dedupe_strings(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def plain_text(value: str) -> str:
    value = MARKDOWN_LINK_RE.sub(r"\1", value)
    value = HTML_TAG_RE.sub("", value)
    value = MARKDOWN_MARKUP_RE.sub("", value)
    return re.sub(r"\s+", " ", value).strip()


def classify_collection(relative: Path) -> str:
    if relative.parts and relative.parts[0] == "corporate":
        return "corporate"
    if relative.parts[:1] == ("yaxunit",):
        return "yaxunit"
    return "v8std"


def stable_slug(value: str) -> str:
    normalized = plain_text(value).lower().replace("ё", "е")
    return SAFE_ID_RE.sub("-", normalized).strip("-")


def yaxunit_document_id(relative: Path) -> str:
    parts = list(relative.with_suffix("").parts[1:])
    if parts[:1] == ["documentation"]:
        parts = parts[1:]
    if parts[:1] == ["features"]:
        parts = parts[1:]
    normalized = [stable_slug(part) for part in parts if stable_slug(part)]
    return "yaxunit:" + ":".join(normalized)


def metadata_bool(front_matter: dict[str, Any], key: str, default: bool) -> bool:
    value = front_matter.get(key, default)
    if not isinstance(value, bool):
        raise ValueError(f"front matter '{key}' must be boolean")
    return value


def normalized_tags(front_matter: dict[str, Any]) -> list[str]:
    tags = front_matter.get("tags", [])
    if tags is None:
        return []
    if not isinstance(tags, list):
        raise ValueError("front matter 'tags' must be a list")
    return dedupe_strings(str(tag) for tag in tags)


def normalized_aliases(front_matter: dict[str, Any]) -> list[str]:
    aliases = front_matter.get("aliases", [])
    if aliases is None:
        return []
    if not isinstance(aliases, list) or any(not isinstance(alias, str) or not alias.strip() for alias in aliases):
        raise ValueError("front matter 'aliases' must be a string list")
    return dedupe_strings(aliases)


def validate_source_metadata(
    relative: Path,
    front_matter: dict[str, Any],
    collection: str,
    page_type: str,
    page_id: str,
) -> None:
    if front_matter.get("index_for_ai") is False:
        return
    if collection not in VALID_COLLECTIONS:
        raise ValueError(f"unknown collection '{collection}' in {relative}")
    if page_type not in VALID_TYPES:
        raise ValueError(f"unknown type '{page_type}' in {relative}")
    if not page_id:
        raise ValueError(f"missing stable id in {relative}")
    if collection != "corporate":
        return
    required = {"id", "collection", "type", "level", "tags"}
    missing = sorted(required - set(front_matter))
    if missing:
        raise ValueError(f"missing corporate metadata {', '.join(missing)} in {relative}")
    if front_matter.get("collection") != "corporate":
        raise ValueError(f"corporate collection must be 'corporate' in {relative}")
    level = front_matter.get("level")
    if level not in VALID_CORPORATE_LEVELS:
        raise ValueError(f"unknown corporate level '{level}' in {relative}")
    tags = front_matter.get("tags")
    if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        raise ValueError(f"corporate tags must be a non-empty string list in {relative}")


def validate_yaxunit_snapshot(root: Path) -> None:
    destination = root / "docs" / "yaxunit"
    if not destination.exists():
        return
    manifest_path = destination / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid YaXUnit manifest: {error}") from error
    required = {"project", "revision", "source_path", "license", "license_sha256", "targets"}
    if set(manifest) != required:
        raise ValueError("invalid YaXUnit manifest fields")
    if manifest["project"] != "bia-technologies/yaxunit" or manifest["license"] != "Apache-2.0":
        raise ValueError("invalid YaXUnit manifest provenance")
    if not isinstance(manifest["revision"], str) or not manifest["revision"].strip():
        raise ValueError("invalid YaXUnit manifest revision")
    if manifest["source_path"] != "exts/yaxunit/src" or not isinstance(manifest["targets"], list):
        raise ValueError("invalid YaXUnit manifest source")

    license_path = destination / "LICENSE"
    if not license_path.is_file() or hashlib.sha256(license_path.read_bytes()).hexdigest() != manifest["license_sha256"]:
        raise ValueError("invalid YaXUnit license snapshot")

    expected_paths: set[str] = set()
    manifest_targets: list[tuple[str, str]] = []
    hash_re = re.compile(r"^[0-9a-f]{64}$")
    target_fields = {
        "name",
        "source_path",
        "source_sha256",
        "generated_path",
        "generated_sha256",
        "exports",
    }
    for item in manifest["targets"]:
        if not isinstance(item, dict) or set(item) != target_fields:
            raise ValueError("invalid YaXUnit manifest target entry")
        module = item["name"]
        if not isinstance(module, str) or not module.strip() or any(module == name for name, _ in manifest_targets):
            raise ValueError(f"invalid or duplicate YaXUnit API target: {module}")
        source_path = PurePosixPath(str(item["source_path"]))
        if (
            source_path.is_absolute()
            or ".." in source_path.parts
            or source_path.parts[:3] != ("exts", "yaxunit", "src")
            or source_path.suffix.lower() != ".bsl"
        ):
            raise ValueError(f"invalid YaXUnit source path: {source_path}")
        generated = validate_relative_path(item["generated_path"])
        if PurePosixPath(generated).parts[:1] != ("api",):
            raise ValueError(f"invalid YaXUnit generated path: {generated}")
        if generated in expected_paths:
            raise ValueError(f"duplicate YaXUnit generated path: {generated}")
        if not isinstance(item["exports"], int) or item["exports"] <= 0:
            raise ValueError(f"invalid YaXUnit export count for {module}")
        if not hash_re.fullmatch(str(item["source_sha256"])) or not hash_re.fullmatch(str(item["generated_sha256"])):
            raise ValueError(f"invalid YaXUnit hash for {module}")
        expected_paths.add(generated)
        manifest_targets.append((module, source_path.as_posix()))
        generated_file = destination / Path(*PurePosixPath(generated).parts)
        if not generated_file.is_file() or hashlib.sha256(generated_file.read_bytes()).hexdigest() != item["generated_sha256"]:
            raise ValueError(f"invalid YaXUnit generated API file: {generated}")

    actual_paths = {
        path.relative_to(destination).as_posix()
        for path in (destination / "api").rglob("*.md")
    }
    if actual_paths != expected_paths:
        raise ValueError("YaXUnit API files do not match manifest")
    if (destination / "documentation").exists():
        raise ValueError("legacy YaXUnit documentation snapshot is not allowed")

    targets_path = root / "scripts" / "knowledge" / "yaxunit-api-targets.txt"
    configured_targets: list[tuple[str, str]] = []
    for raw in targets_path.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        name, relative_source = (part.strip() for part in value.split("|", 1))
        configured_targets.append((name, (PurePosixPath("exts/yaxunit/src") / relative_source).as_posix()))
    if configured_targets != manifest_targets:
        raise ValueError("YaXUnit API target list does not match manifest")

    patterns = sorted((destination / "patterns").glob("*.md"))
    if not patterns:
        raise ValueError("YaXUnit usage patterns are missing")


def validate_relative_path(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("invalid YaXUnit manifest path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.suffix.lower() != ".md":
        raise ValueError(f"invalid YaXUnit manifest path: {value}")
    return path.as_posix()


def split_h2_sections(markdown: str) -> list[tuple[str, str, str]]:
    lines = markdown.splitlines()
    headings: list[tuple[int, str]] = []
    in_code_block = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            match = H2_RE.match(line)
            if match:
                headings.append((index, plain_text(match.group("title"))))

    sections: list[tuple[str, str, str]] = []
    first_heading = headings[0][0] if headings else len(lines)
    overview = "\n".join(lines[:first_heading]).strip()
    if overview:
        sections.append(("overview", "Обзор", overview))
    for position, (start, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        slug = stable_slug(title)
        if not slug:
            raise ValueError(f"empty stable section slug for heading '{title}'")
        sections.extend(split_large_section(slug, title, body))
    if not sections and markdown.strip():
        sections.append(("overview", "Обзор", markdown.strip()))
    if any(not body.strip() for _, _, body in sections):
        raise ValueError("empty semantic section")
    return sections


def split_large_section(section_id: str, title: str, body: str) -> list[tuple[str, str, str]]:
    if len(body) <= MAX_SECTION_CHARS:
        return [(section_id, title, body)]
    lines = body.splitlines()
    headings: list[tuple[int, str]] = []
    in_code_block = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            match = H3_RE.match(line)
            if match:
                headings.append((index, plain_text(match.group("title"))))
    if not headings:
        return [(section_id, title, body)]

    result: list[tuple[str, str, str]] = []
    intro = "\n".join(lines[:headings[0][0]]).strip()
    if len(intro.splitlines()) > 1:
        result.append((f"{section_id}:overview", f"{title} — Обзор", intro))
    for position, (start, h3_title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        h3_body = "\n".join(lines[start:end]).strip()
        h3_id = stable_slug(h3_title)
        if not h3_id:
            raise ValueError(f"empty stable section slug for heading '{h3_title}'")
        result.append((f"{section_id}:{h3_id}", f"{title} — {h3_title}", h3_body))
    return result


def section_description(body: str, fallback: str) -> str:
    for block in re.split(r"\n{2,}", body):
        cleaned = re.sub(r"^#{1,6}\s+", "", block.strip())
        cleaned = plain_text(cleaned)
        if cleaned:
            return cleaned if len(cleaned) <= 180 else cleaned[:177].rstrip() + "..."
    return fallback


def expand_retrieval_records(indexed_pages: list[dict[str, Any]], *, public_only: bool = False) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for page in indexed_pages:
        if public_only and not page.get("_publish_publicly", True):
            continue
        if page["collection"] not in SECTION_COLLECTIONS:
            page_records = [page]
        else:
            page_records = []
            for section_id, section_title, body in split_h2_sections(page["body_markdown"]):
                record = dict(page)
                record["document_id"] = page["id"]
                record["id"] = f"{page['id']}:{section_id}"
                record["section"] = section_title
                record["title"] = f"{page['title']} — {section_title}"
                record["description"] = section_description(body, page["description"])
                record["aliases"] = dedupe_strings([*page["aliases"], page["id"], section_title])
                record["url"] = f"{page['url'].split('#', 1)[0]}#{section_id}"
                record["markdown_url"] = f"{page['markdown_url'].split('#', 1)[0]}#{section_id}"
                record["body_markdown"] = body
                record["related"] = []
                page_records.append(record)
        for record in page_records:
            if record["id"] in seen_ids:
                raise ValueError(f"duplicate stable id: {record['id']}")
            seen_ids.add(record["id"])
            records.append(record)
    return records
