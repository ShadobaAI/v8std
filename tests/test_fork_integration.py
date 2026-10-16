"""Regression checks for fork metadata at upstream integration boundaries."""
import unittest
import json
import tempfile
from pathlib import Path

from scripts.generate_ai_artifacts import build_ignored_ref_context, strip_ignored_markdown_refs
from runtime.v8std_mcp_index import V8StdIndex


class ForkIntegrationTests(unittest.TestCase):
    def test_unindexed_readme_without_id_does_not_strip_fragments(self):
        ignored = build_ignored_ref_context([
            {"id": "", "title": "Private overview", "url": "https://v8std.ru/corporate/README/"},
            {"id": "private", "title": "Private page", "url": "https://v8std.ru/private/"},
        ])
        text = "ID: #std400\n\nSee [1.3](https://v8std.ru/std/400/#13)."
        self.assertEqual(strip_ignored_markdown_refs(text, ignored), text)
        self.assertEqual(strip_ignored_markdown_refs("[Private](https://v8std.ru/private/)", ignored), "")

    def test_cursor_is_bound_to_collection_even_when_ranked_results_are_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            pages = Path(directory) / "pages.jsonl"
            pages.write_text("\n".join(json.dumps({
                "id": f"corporate:test{number}", "type": "rule", "collection": "corporate",
                "title": "Module policy", "level": "mandatory",
            }) for number in range(4)), encoding="utf-8")
            index = V8StdIndex(pages_path=pages)
            index.load()
            # The public-corpus cutoff must not suppress a small selected collection.
            self.assertTrue(index.search("module", collections=["corporate"])["results"])
            self.assertEqual(index.search("zxqvnonexistent", collections=["corporate"])["results"], [])
            first = index.search("module", mode="bm25", limit=1, collections=["corporate"])
            self.assertEqual(first["total"], 4)
            second = index.search("module", mode="bm25", limit=1, collections=["corporate"],
                                  cursor=first["next_cursor"])
            self.assertNotEqual(first["results"][0]["id"], second["results"][0]["id"])
            for collections in (None, ["corporate", "yaxunit"]):
                with self.subTest(collections=collections), self.assertRaisesRegex(ValueError, "stale search cursor"):
                    index.search("module", mode="bm25", limit=1, collections=collections,
                                 cursor=first["next_cursor"])
