#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = REPO_ROOT / "scripts" / "knowledge" / "yaxunit-api-targets.txt"
DEFAULT_DESTINATION = REPO_ROOT / "docs" / "yaxunit"
SOURCE_ROOT = Path("exts/yaxunit/src")
MODULE_NAME_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9_]+$")
DECLARATION_RE = re.compile(
    r"^\s*(Функция|Процедура|Function|Procedure)\s+([A-Za-zА-Яа-яЁё0-9_]+)\s*\(",
    re.IGNORECASE,
)
DEPRECATED_CALL_RE = re.compile(
    r'ВызовУстаревшегоМетода\(\s*"[^"]+"\s*,\s*"(?P<replacement>[^"]+)"\s*,\s*"(?P<version>[^"]+)"',
    re.IGNORECASE,
)
MAX_SUMMARY_CHARS = 900
MAX_PARAMETER_CHARS = 1800
MAX_RETURN_CHARS = 600


@dataclass(frozen=True)
class ApiTarget:
    name: str
    source_path: PurePosixPath


@dataclass(frozen=True)
class ApiSymbol:
    module: str
    kind: str
    name: str
    signature: str
    line: int
    summary: str
    parameters: tuple[str, ...]
    returns: tuple[str, ...]
    deprecated: bool
    replacement: str | None
    deprecated_since: str | None


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_targets(path: Path) -> list[ApiTarget]:
    targets: list[ApiTarget] = []
    seen: set[str] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        parts = [part.strip() for part in value.split("|", 1)]
        if len(parts) != 2 or not MODULE_NAME_RE.fullmatch(parts[0]):
            raise ValueError(f"invalid YaXUnit API target at line {line_number}: {value}")
        source_path = PurePosixPath(parts[1])
        if source_path.is_absolute() or ".." in source_path.parts or source_path.suffix.lower() != ".bsl":
            raise ValueError(f"invalid YaXUnit API source at line {line_number}: {parts[1]}")
        if parts[0] in seen:
            raise ValueError(f"duplicate YaXUnit API target at line {line_number}: {parts[0]}")
        seen.add(parts[0])
        targets.append(ApiTarget(parts[0], source_path))
    if not targets:
        raise ValueError("YaXUnit API target list is empty")
    return targets


def git_revision(source: Path) -> str:
    command = [
        "git",
        "-c",
        f"safe.directory={source.resolve().as_posix()}",
        "-C",
        str(source),
        "rev-parse",
        "HEAD",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _preceding_comments(lines: list[str], declaration_index: int) -> list[str]:
    index = declaration_index - 1
    while index >= 0 and (
        not lines[index].strip()
        or lines[index].lstrip().startswith("&")
        or lines[index].lstrip().startswith("//@")
    ):
        index -= 1
    comments: list[str] = []
    while index >= 0 and lines[index].lstrip().startswith("//"):
        value = lines[index].lstrip()[2:]
        if value.startswith(" "):
            value = value[1:]
        if not value.lstrip().startswith("@"):  # Static-analysis directives are not API documentation.
            comments.append(value.rstrip())
        index -= 1
    comments.reverse()
    return comments


def _compact_text(lines: list[str], limit: int) -> str:
    compact: list[str] = []
    previous_blank = True
    for raw in lines:
        value = raw.strip()
        if not value:
            if compact and not previous_blank:
                compact.append("")
            previous_blank = True
            continue
        compact.append(value)
        previous_blank = False
    while compact and not compact[-1]:
        compact.pop()
    text = "\n".join(compact)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _normalise_items(lines: list[str], limit: int) -> tuple[str, ...]:
    items: list[str] = []
    for raw in lines:
        value = raw.strip()
        if not value:
            continue
        match = re.match(r"^(?P<name>[A-Za-zА-Яа-яЁё0-9_]+)\s*-\s*(?P<body>.+)$", value)
        if match:
            items.append(f"`{match.group('name')}` — {match.group('body').replace(' - ', ' — ')}")
        elif items:
            items[-1] += " " + value
        else:
            items.append(value)
    result: list[str] = []
    used = 0
    for item in items:
        if used + len(item) > limit:
            break
        result.append(item)
        used += len(item)
    return tuple(result)


def _comment_sections(comments: list[str]) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    sections: dict[str, list[str]] = {"summary": [], "parameters": [], "returns": [], "example": []}
    current = "summary"
    for raw in comments:
        heading = raw.strip().lower().rstrip(":")
        if heading == "параметры":
            current = "parameters"
            continue
        if heading in {"возвращаемое значение", "возвращает"}:
            current = "returns"
            continue
        if heading in {"пример", "примеры"}:
            current = "example"
            continue
        sections[current].append(raw)
    summary = _compact_text(sections["summary"], MAX_SUMMARY_CHARS)
    parameters = _normalise_items(sections["parameters"], MAX_PARAMETER_CHARS)
    returns = _normalise_items(sections["returns"], MAX_RETURN_CHARS)
    return summary, parameters, returns


def parse_exported_symbols(module: str, source_file: Path) -> list[ApiSymbol]:
    lines = source_file.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").splitlines()
    symbols: list[ApiSymbol] = []
    index = 0
    while index < len(lines):
        match = DECLARATION_RE.match(lines[index])
        if not match:
            index += 1
            continue

        declaration_end = index
        parenthesis_balance = 0
        saw_parenthesis = False
        exported = False
        while declaration_end < len(lines):
            declaration_line = lines[declaration_end]
            parenthesis_balance += declaration_line.count("(") - declaration_line.count(")")
            saw_parenthesis = saw_parenthesis or "(" in declaration_line
            exported = exported or bool(re.search(r"\b(?:Экспорт|Export)\b", declaration_line, re.IGNORECASE))
            if saw_parenthesis and parenthesis_balance <= 0:
                break
            declaration_end += 1
        if not exported:
            index = declaration_end + 1
            continue

        kind = match.group(1).capitalize()
        name = match.group(2)
        raw_signature = " ".join(line.strip() for line in lines[index : declaration_end + 1])
        raw_signature = re.sub(r"\s+", " ", raw_signature).strip()
        signature = re.sub(
            rf"^({re.escape(match.group(1))})\s+{re.escape(name)}",
            rf"\1 {module}.{name}",
            raw_signature,
            count=1,
            flags=re.IGNORECASE,
        )

        end_marker = "EndFunction" if kind.lower() == "function" else "EndProcedure" if kind.lower() == "procedure" else "КонецФункции" if kind.lower() == "функция" else "КонецПроцедуры"
        body_end = declaration_end + 1
        while body_end < len(lines) and not re.match(
            rf"^{end_marker}\b",
            lines[body_end].strip(),
            re.IGNORECASE,
        ):
            body_end += 1
        body = "\n".join(lines[declaration_end + 1 : body_end])
        deprecated_match = DEPRECATED_CALL_RE.search(body)
        comments = _preceding_comments(lines, index)
        summary, parameters, returns = _comment_sections(comments)
        deprecated = "устарел" in " ".join(comments).lower() or deprecated_match is not None
        symbols.append(
            ApiSymbol(
                module=module,
                kind=kind,
                name=name,
                signature=signature,
                line=index + 1,
                summary=summary or f"Экспортный метод модуля `{module}`.",
                parameters=parameters,
                returns=returns,
                deprecated=deprecated,
                replacement=deprecated_match.group("replacement") if deprecated_match else None,
                deprecated_since=deprecated_match.group("version") if deprecated_match else None,
            )
        )
        index = body_end + 1

    names = [symbol.name.casefold() for symbol in symbols]
    if len(names) != len(set(names)):
        raise ValueError(f"duplicate exported API symbol in {module}")
    if not symbols:
        raise ValueError(f"no exported API symbols in {source_file}")
    return symbols


def render_module(module: str, symbols: list[ApiSymbol], source_path: str, revision: str) -> bytes:
    lines = [
        "---",
        f"title: API {module}",
        f'description: "Публичные экспортные методы модуля {module} из ядра YaXUnit."',
        f"tags: [yaxunit, api, {module}]",
        "publish_publicly: false",
        "---",
        "",
        f"# API {module}",
        "",
        f"Компактный справочник по {len(symbols)} экспортным методам. Сигнатуры получены из ядра YaXUnit ревизии `{revision}`.",
        "",
    ]
    for symbol in symbols:
        lines.extend([f"## {module}.{symbol.name}", "", f"`{symbol.signature}`", "", symbol.summary, ""])
        if symbol.deprecated:
            status = "**Статус:** устарел."
            if symbol.replacement:
                status += f" Используйте `{symbol.replacement}`."
            if symbol.deprecated_since:
                status += f" Переход объявлен в `{symbol.deprecated_since}`."
            lines.extend([status, ""])
        if symbol.parameters:
            lines.extend(["**Параметры:**", *[f"- {item}" for item in symbol.parameters], ""])
        if symbol.returns:
            lines.extend(["**Возвращает:**", *[f"- {item}" for item in symbol.returns], ""])
        lines.extend([f"Источник ядра: `{source_path}:{symbol.line}`.", ""])
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def expected_snapshot(
    source: Path,
    targets: list[ApiTarget],
    revision: str,
) -> tuple[dict[str, bytes], bytes, bytes]:
    files: dict[str, bytes] = {}
    manifest_targets: list[dict[str, object]] = []
    missing: list[str] = []
    for target in targets:
        module = target.name
        relative_source = SOURCE_ROOT / Path(*target.source_path.parts)
        source_file = source / relative_source
        if not source_file.is_file():
            missing.append(relative_source.as_posix())
            continue
        source_payload = source_file.read_bytes()
        symbols = parse_exported_symbols(module, source_file)
        generated_path = PurePosixPath("api") / f"{module}.md"
        generated_payload = render_module(module, symbols, relative_source.as_posix(), revision)
        files[generated_path.as_posix()] = generated_payload
        manifest_targets.append(
            {
                "exports": len(symbols),
                "generated_path": generated_path.as_posix(),
                "generated_sha256": sha256(generated_payload),
                "name": module,
                "source_path": relative_source.as_posix(),
                "source_sha256": sha256(source_payload),
            }
        )

    license_path = source / "LICENSE"
    if not license_path.is_file():
        missing.append("LICENSE")
    if missing:
        raise FileNotFoundError("missing YaXUnit source files: " + ", ".join(missing))

    license_payload = license_path.read_bytes()
    manifest = {
        "license": "Apache-2.0",
        "license_sha256": sha256(license_payload),
        "targets": manifest_targets,
        "project": "bia-technologies/yaxunit",
        "revision": revision,
        "source_path": SOURCE_ROOT.as_posix(),
    }
    manifest_payload = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return files, license_payload, manifest_payload


def snapshot_drift(
    destination: Path,
    files: dict[str, bytes],
    license_payload: bytes,
    manifest_payload: bytes,
) -> list[str]:
    drift: list[str] = []
    api_directory = destination / "api"
    expected_paths = set(files)
    actual_paths = (
        {path.relative_to(destination).as_posix() for path in api_directory.rglob("*.md")}
        if api_directory.is_dir()
        else set()
    )
    for relative, payload in files.items():
        target = destination / Path(*PurePosixPath(relative).parts)
        if not target.is_file() or target.read_bytes() != payload:
            drift.append(f"changed: {relative}")
    for relative in sorted(actual_paths - expected_paths):
        drift.append(f"unexpected: {relative}")
    if (destination / "documentation").exists():
        drift.append("unexpected: documentation/")
    for name, payload in (("LICENSE", license_payload), ("manifest.json", manifest_payload)):
        target = destination / name
        if not target.is_file() or target.read_bytes() != payload:
            drift.append(f"changed: {name}")
    return drift


def _remove_generated_tree(path: Path, destination: Path) -> None:
    resolved = path.resolve()
    root = destination.resolve()
    if resolved == root or not resolved.is_relative_to(root):
        raise ValueError(f"refusing to remove path outside YaXUnit destination: {resolved}")
    if not path.exists():
        return
    for child in sorted((item for item in path.rglob("*") if item.is_file()), reverse=True):
        child.unlink()
    for child in sorted((item for item in path.rglob("*") if item.is_dir()), reverse=True):
        child.rmdir()
    path.rmdir()


def synchronize(
    source: Path,
    destination: Path,
    targets_path: Path,
    revision: str,
    *,
    check: bool,
) -> None:
    targets = load_targets(targets_path)
    files, license_payload, manifest_payload = expected_snapshot(source, targets, revision)
    drift = snapshot_drift(destination, files, license_payload, manifest_payload)
    if check:
        if drift:
            raise RuntimeError("YaXUnit API knowledge is out of date:\n" + "\n".join(drift))
        return

    destination.mkdir(parents=True, exist_ok=True)
    for relative, payload in files.items():
        atomic_write_bytes(destination / Path(*PurePosixPath(relative).parts), payload)
    api_directory = destination / "api"
    expected_paths = set(files)
    if api_directory.is_dir():
        for path in sorted(api_directory.rglob("*.md"), reverse=True):
            if path.relative_to(destination).as_posix() not in expected_paths:
                path.unlink()
        for directory in sorted((path for path in api_directory.rglob("*") if path.is_dir()), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
    _remove_generated_tree(destination / "documentation", destination)
    atomic_write_bytes(destination / "LICENSE", license_payload)
    atomic_write_bytes(destination / "manifest.json", manifest_payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate compact YaXUnit API knowledge from an exact local core checkout.")
    parser.add_argument("--source", type=Path, required=True, help="Local YaXUnit checkout root.")
    parser.add_argument("--revision", help="Must equal the local checkout HEAD; defaults to HEAD.")
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGETS)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    parser.add_argument("--check", action="store_true", help="Fail when generated API knowledge differs; do not write.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"YaXUnit source directory does not exist: {source}")
    head_revision = git_revision(source)
    revision = (args.revision or head_revision).strip()
    if revision != head_revision:
        raise ValueError(f"YaXUnit revision {revision} does not match checkout HEAD {head_revision}")
    synchronize(
        source,
        args.destination.resolve(),
        args.targets.resolve(),
        revision,
        check=args.check,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
