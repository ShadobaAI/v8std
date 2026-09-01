#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import time
from pathlib import Path

from atomic_files import atomic_write_text


PRIVATE_DIRECTORIES = {"corporate", "yaxunit"}
STAGING_DIRECTORY = Path(".cache/public-docs")
CONFIG_NAME = ".zensical-public.toml"
LOCAL_CONFIG_NAME = ".zensical-local.toml"


def markdown_title(path: Path) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else path.stem


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def navigation_items(paths: list[Path], docs_dir: Path) -> str:
    return ",\n".join(
        f"        {{ {toml_string(markdown_title(path))} = "
        f"{toml_string(path.relative_to(docs_dir).as_posix())} }}"
        for path in paths
    )


def local_navigation(docs_dir: Path) -> str:
    patterns = sorted((docs_dir / "yaxunit" / "patterns").glob("*.md"), key=markdown_title)
    api = sorted((docs_dir / "yaxunit" / "api").glob("*.md"), key=markdown_title)
    return f'''[[project.nav]]
"YaXUnit" = [
    {{ "Обзор" = "yaxunit/README.md" }},
    {{ "Паттерны использования" = [
{navigation_items(patterns, docs_dir)}
    ] }},
    {{ "API ядра" = [
{navigation_items(api, docs_dir)}
    ] }},
]

[[project.nav]]
"Корпоративные материалы" = "corporate/README.md"'''


def local_config(config: str, docs_dir: Path) -> str:
    return f"{config.rstrip()}\n\n{local_navigation(docs_dir)}\n"


def public_config(config: str) -> str:
    marker = "[project]"
    if marker not in config:
        raise ValueError("zensical.toml has no [project] section")
    return config.replace(marker, f'{marker}\ndocs_dir = "{STAGING_DIRECTORY.as_posix()}"', 1)


def public_files(docs_dir: Path) -> list[Path]:
    return [
        path
        for path in docs_dir.rglob("*")
        if path.is_file() and path.relative_to(docs_dir).parts[0] not in PRIVATE_DIRECTORIES
    ]


def synchronize(root: Path) -> None:
    docs_dir = root / "docs"
    staging_dir = root / STAGING_DIRECTORY
    staging_dir.mkdir(parents=True, exist_ok=True)
    expected: set[Path] = set()
    for source in public_files(docs_dir):
        relative = source.relative_to(docs_dir)
        expected.add(relative)
        destination = staging_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if (
            not destination.is_file()
            or destination.stat().st_size != source.stat().st_size
            or destination.stat().st_mtime_ns != source.stat().st_mtime_ns
        ):
            shutil.copy2(source, destination)

    for destination in sorted(staging_dir.rglob("*"), reverse=True):
        if destination.is_file() and destination.relative_to(staging_dir) not in expected:
            destination.unlink()
        elif destination.is_dir() and not any(destination.iterdir()):
            destination.rmdir()


def prepare(root: Path) -> Path:
    docs_dir = root / "docs"
    staging_dir = root / STAGING_DIRECTORY
    if staging_dir.exists() or staging_dir.is_symlink():
        if staging_dir.is_symlink() or staging_dir.is_file():
            staging_dir.unlink()
        else:
            shutil.rmtree(staging_dir)
    synchronize(root)

    config_path = root / CONFIG_NAME
    atomic_write_text(config_path, public_config((root / "zensical.toml").read_text(encoding="utf-8")))
    return config_path


def prepare_local(root: Path) -> Path:
    config_path = root / LOCAL_CONFIG_NAME
    atomic_write_text(
        config_path,
        local_config((root / "zensical.toml").read_text(encoding="utf-8"), root / "docs"),
    )
    return config_path


def watch(root: Path, interval: float = 0.5) -> None:
    while True:
        synchronize(root)
        time.sleep(interval)


def clean(root: Path) -> None:
    config_path = root / CONFIG_NAME
    config_path.unlink(missing_ok=True)
    staging_dir = root / STAGING_DIRECTORY
    if staging_dir.is_symlink() or staging_dir.is_file():
        staging_dir.unlink(missing_ok=True)
    elif staging_dir.is_dir():
        shutil.rmtree(staging_dir)


def clean_local(root: Path) -> None:
    (root / LOCAL_CONFIG_NAME).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare docs input for a public Zensical build.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.local and args.watch:
        parser.error("--local does not require --watch; Zensical watches docs directly")
    if args.local and args.clean:
        clean_local(root)
    elif args.local:
        print(prepare_local(root))
    elif args.clean:
        clean(root)
    elif args.watch:
        watch(root)
    else:
        print(prepare(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
