"""MCP navigation by stable corpus references, independent of web sources."""
from __future__ import annotations

from contextvars import ContextVar
from functools import wraps
import re
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

from runtime.v8std_mcp_presentation import present_tool_markdown
from runtime.v8std_mcp_index import markdown_sections, clamp_body_limit, clamp_compact_body_limit

TOOL_REFERENCES = ContextVar("v8std_tool_references", default=False)
PREFIX = "v8std:"
TOOLS = frozenset({"search", "page", "summary", "section", "pattern", "api_card",
                   "requirements_for_context", "related", "related_ids",
                   "explain_snippet", "explain_diagnostics"})
LOOKUP_TOOLS = TOOLS - {"search", "requirements_for_context", "explain_snippet", "explain_diagnostics"}
WEB = re.compile(r"https?://[^\s<>\"'`]+", re.I)


def lookup_reference(value):
    return value[len(PREFIX):] if isinstance(value, str) and value.startswith(PREFIX) else value


def _key(value):
    value = value.replace("\\", "/")
    parts = urlsplit(value)
    return unquote(urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                              parts.path.rstrip("/"), "", parts.fragment)))


class ReferenceCatalog:
    def __init__(self, pages):
        self.ids = {page["id"] for page in pages}
        self.targets = {}
        self.documents = set()
        self.ambiguous = set()
        for page in pages:
            if page.get("url") and not urlsplit(page["url"]).fragment:
                self.documents.add(page["id"])
            for field in ("url", "markdown_url", "source_path"):
                value = page.get(field)
                if value:
                    self.targets.setdefault(_key(value), set()).add(page["id"])
            for alias in page.get("aliases", []):
                if isinstance(alias, str) and alias.startswith(("http://", "https://")):
                    self.targets.setdefault(_key(alias), set()).add(page["id"])

    def link(self, value, *, context=None):
        if value.startswith(PREFIX) and lookup_reference(value) in self.ids:
            return value
        if value in self.ids:
            return PREFIX + value
        candidates = [value]
        if context:
            candidates.append(urljoin(context, value))
        ambiguous = set()
        for candidate in candidates:
            key = _key(candidate)
            targets = self.targets.get(key) or self.targets.get(key.split("#")[0]) or set()
            documents = targets & self.documents
            preferred = documents if len(documents) == 1 else targets
            if len(preferred) == 1:
                return PREFIX + next(iter(preferred))
            ambiguous.update(targets)
        self.ambiguous.update(ambiguous)
        return None


def present_mcp_result(value, pages, *, limits=None):
    catalog = ReferenceCatalog(pages)
    page_map = {page["id"]: page for page in pages}

    def visit(item, context=None):
        if isinstance(item, list):
            return [visit(child, context) for child in item]
        if not isinstance(item, dict):
            return WEB.sub("", item) if isinstance(item, str) else item
        own = page_map.get(item.get("id"))
        if own:
            context = own.get("markdown_url") or own.get("url") or context
        result = {}
        for key, child in item.items():
            # Provenance stays in canonical pages, manifests and source maps.
            if key in {"url", "urls", "href", "src"} or key.endswith(("_url", "_urls")):
                continue
            if key == "body_markdown" and isinstance(child, str):
                source = child
                if own and item.get("body_truncated"):
                    source = own.get("body_markdown", child)
                    if item.get("heading"):
                        sections = [section for section in markdown_sections(source)
                                    if section["heading"] == item["heading"]]
                        if len(sections) == 1:
                            source = sections[0]["body_markdown"]
                rendered = present_tool_markdown(source, catalog, context=context)
                budget = None
                if limits:
                    defaults = {"page": 12000, "summary": 2000,
                                "section": 6000, "pattern": 6000, "api_card": 6000,
                                "requirements_for_context": 1000}
                    method = limits["method"]
                    if method in defaults:
                        clamp = clamp_body_limit if method == "page" else clamp_compact_body_limit
                        budget = clamp(limits.get("body_limit", defaults[method]))
                elif item.get("body_truncated"):
                    budget = len(child.removesuffix("\n\n..."))
                if budget is not None:
                    result["body_truncated"] = len(rendered) > budget
                    rendered = rendered[:budget].rstrip() + ("\n\n..." if len(rendered) > budget else "")
                result[key] = rendered
            elif key in {"snippet", "normalized_snippet", "normalized_text"}:
                result[key] = child
            elif key != "body_truncated" or key not in result:
                result[key] = visit(child, context)
        if own:
            result["ref"] = PREFIX + own["id"]
        return result

    result = visit(value)
    if isinstance(result, dict) and catalog.ambiguous:
        result["reference_candidates"] = [
            {"id": key, "title": page_map[key].get("title", key), "ref": PREFIX + key}
            for key in sorted(catalog.ambiguous)]
    return result


class ToolReferenceIndex:
    """Apply one MCP view without changing ranking, snapshots or source hashes."""
    def __init__(self, index, *, snapshot=False):
        self.index, self.snapshot = index, snapshot

    def __getattr__(self, name):
        method = getattr(self.index, name)
        if name not in TOOLS:
            return method

        @wraps(method)
        def call(*args, **kwargs):
            if name in LOOKUP_TOOLS:
                if args:
                    args = (lookup_reference(args[0]), *args[1:])
                else:
                    for key in ("id_or_alias_or_url", "module_or_alias"):
                        if key in kwargs:
                            kwargs[key] = lookup_reference(kwargs[key])
            limits = {"method": name}
            limit_key = "body_limit_per_item" if name == "requirements_for_context" else "body_limit"
            if limit_key in kwargs:
                limits["body_limit"] = kwargs[limit_key]
            token = TOOL_REFERENCES.set(limits)
            try:
                if self.snapshot:
                    return method(*args, **kwargs)
                # Legacy mutable indexes refresh under the same reentrant lock.
                with self.index._lock:
                    result = method(*args, **kwargs)
                    return present_mcp_result(result, self.index._pages, limits=limits)
            finally:
                TOOL_REFERENCES.reset(token)
        return call
