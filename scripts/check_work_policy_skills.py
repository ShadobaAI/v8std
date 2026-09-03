"""Check repository-owned skill selectors against the generated local v8std corpus."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from v8std_mcp_index import V8StdIndex


def check_skills(index: V8StdIndex, root: Path) -> dict:
    skill = root / "1c-code-change" / "SKILL.md"
    reference = skill.parent / "references" / "requirements.md"
    if "references/requirements.md" not in skill.read_text(encoding="utf-8"):
        raise ValueError(f"requirements reference is not reachable from {skill}")
    text = reference.read_text(encoding="utf-8")
    expected = {
        "bsl-change-policy", "bsl-type-transparency", "bsl-readability",
        "bsl-formatting", "module-organization", "query-conventions", "error-reporting",
    }
    selectors = set()
    covered = set()
    for key, headings in re.findall(r"`([a-z][a-z-]+)(?: / ([^`]+))?`", text):
        if key not in expected:
            if headings:
                raise ValueError(f"unknown corporate document selector: {key}")
            continue
        covered.add(key)
        for heading in headings.split(";") if headings else [""]:
            selectors.add((f"corporate:work:{key}:overview", heading.strip()))
    if covered != expected:
        raise ValueError(f"missing corporate document selectors in {reference}: {expected - covered}")
    for page_id, heading in sorted(selectors):
        result = index.section(page_id, heading) if heading else index.summary(page_id, body_limit=6000)
        body = result.get("page", result)
        if (
            not result.get("found") or body.get("body_truncated") is not False
            or body.get("id") != page_id
        ):
            raise ValueError(f"missing/ambiguous/truncated evidence: {page_id} / {heading}")
    standards = set(re.findall(r"\bstd\d+\b", text))
    for page_id in standards:
        if index.resolve(page_id) is None:
            raise ValueError(f"missing general standard: {page_id}")
    return {"skills": str(root), "corporate_selectors": len(selectors), "standards": len(standards)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, action="append", required=True)
    parser.add_argument(
        "--pages", type=Path,
        default=Path(__file__).resolve().parents[1] / "docs" / "ai" / "pages.jsonl",
    )
    args = parser.parse_args()
    index = V8StdIndex(pages_path=args.pages)
    index.load()
    for root in args.skills:
        print(json.dumps(check_skills(index, root), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
