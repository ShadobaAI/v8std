"""Regression checks for fork metadata at upstream integration boundaries."""
import unittest

from scripts.generate_ai_artifacts import build_ignored_ref_context, strip_ignored_markdown_refs


class ForkIntegrationTests(unittest.TestCase):
    def test_unindexed_readme_without_id_does_not_strip_fragments(self):
        ignored = build_ignored_ref_context([
            {"id": "", "title": "Private overview", "url": "https://v8std.ru/corporate/README/"},
            {"id": "private", "title": "Private page", "url": "https://v8std.ru/private/"},
        ])
        text = "ID: #std400\n\nSee [1.3](https://v8std.ru/std/400/#13)."
        self.assertEqual(strip_ignored_markdown_refs(text, ignored), text)
        self.assertEqual(strip_ignored_markdown_refs("[Private](https://v8std.ru/private/)", ignored), "")
