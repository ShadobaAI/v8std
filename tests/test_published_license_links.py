import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from markdown_it import MarkdownIt

from scripts.publish_license_texts import (THIRD_PARTY_PAGE, check_published_license_links, default_repo_root,
                                         publish_license_texts, LinkParser)


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublishedLicenseLinkTests(unittest.TestCase):
    def test_directory_index_links_all_unchanged_license_texts(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            names = publish_license_texts(REPO_ROOT, site)
            parser = LinkParser()
            parser.feed((site / "LICENSES/index.html").read_text())
            self.assertEqual(set(parser.hrefs), names)
            for name in names:
                self.assertEqual((site / "LICENSES" / name).read_bytes(),
                                 (REPO_ROOT / "LICENSES" / name).read_bytes())

    def test_container_repo_root_comes_from_wrapper_environment(self):
        with patch.dict("os.environ", {"V8STD_REPO_ROOT": "/docs"}):
            self.assertEqual(default_repo_root(), Path("/docs"))

    def test_attribution_source_links_every_published_third_party_license(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            publish_license_texts(REPO_ROOT, site)
            source = (REPO_ROOT / "docs/THIRD_PARTY_DIAGNOSTIC_ARTICLES.md").read_text(encoding="utf-8")
            target = site / THIRD_PARTY_PAGE
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(MarkdownIt().render(source), encoding="utf-8")
            checked = check_published_license_links(REPO_ROOT, site)

        self.assertEqual(
            checked,
            {
                "EPL-2.0.txt",
                "GPL-3.0.txt",
                "LGPL-3.0.txt",
            },
        )


if __name__ == "__main__":
    unittest.main()
