#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from atomic_files import atomic_write_text


PRIVATE_PREFIXES = ("corporate/", "yaxunit/")


def relative_location(value: str) -> str:
    parsed = urlsplit(value)
    path = parsed.path if parsed.scheme or parsed.netloc else value.split("#", 1)[0].split("?", 1)[0]
    return path.lstrip("/").replace("\\", "/")


def is_private_location(value: Any) -> bool:
    return isinstance(value, str) and relative_location(value).startswith(PRIVATE_PREFIXES)


def sanitize_search_payload(value: Any) -> Any:
    if isinstance(value, list):
        return [cleaned for item in value if (cleaned := sanitize_search_payload(item)) is not None]
    if not isinstance(value, dict):
        return value
    for key in ("location", "url", "path"):
        if is_private_location(value.get(key)):
            return None
    return {key: sanitize_search_payload(item) for key, item in value.items()}


def sanitize_search_index(path: Path) -> None:
    if not path.is_file():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    cleaned = sanitize_search_payload(payload)
    atomic_write_text(path, json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")) + "\n")


def sanitize_sitemap(path: Path) -> None:
    if not path.is_file():
        return
    tree = ET.parse(path)
    root = tree.getroot()
    namespace = root.tag.partition("}")[0].lstrip("{") if "}" in root.tag else ""
    loc_tag = f"{{{namespace}}}loc" if namespace else "loc"
    for url in list(root):
        location = url.find(loc_tag)
        if location is not None and is_private_location(location.text or ""):
            root.remove(url)
    ET.indent(tree, space="  ")
    payload = ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"
    atomic_write_text(path, payload)


def prune_private_site(site_dir: Path) -> None:
    for relative in (Path("corporate"), Path("yaxunit")):
        target = site_dir / relative
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    sanitize_search_index(site_dir / "search.json")
    sanitize_sitemap(site_dir / "sitemap.xml")


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove private knowledge collections from a public site build.")
    parser.add_argument("--site", type=Path, required=True)
    args = parser.parse_args()
    prune_private_site(args.site.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
