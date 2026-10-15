from __future__ import annotations
import importlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from scripts import sync_vanessa_docs as sync
from scripts.v8std_vanessa_snapshot import BASE_MCP_TOOLS, PATTERNS, digest, validate_vanessa_snapshot
from runtime.v8std_mcp_index import V8StdIndex

generator=importlib.import_module("generate_ai_artifacts")

class VanessaCollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=generator.build_site_ai_index(ROOT)
        cls.jsonl=generator.build_pages_jsonl(cls.data["pages"])
        cls.rows=[json.loads(x) for x in cls.jsonl.splitlines()]
        cls.vanessa=[x for x in cls.rows if x["collection"] == "vanessa"]
        cls.manifest=json.loads((ROOT/"docs/vanessa/manifest.json").read_text(encoding="utf-8"))

    def test_all_manifest_ids_retrieve_full_pages_and_mcp_sections_offline(self):
        expected={x["id"] for x in self.manifest["documents"]}
        self.assertEqual({x["id"] for x in self.vanessa},expected)
        with tempfile.TemporaryDirectory() as directory:
            pages=Path(directory)/"pages.jsonl"
            pages.write_text(self.jsonl,encoding="utf-8")
            index=V8StdIndex(pages_path=pages)
            index.load()
            for record in self.vanessa:
                result=index.page(record["id"],body_limit=30000)
                self.assertTrue(result["found"],record["id"])
                self.assertFalse(result["page"]["body_truncated"],record["id"])
                self.assertEqual(result["page"]["body_markdown"],record["body_markdown"])
            section=index.section("vanessa:mcp:run_scenario","Назначение, документированные параметры и ответ")
            self.assertTrue(section["found"])
            self.assertIn("reloadAndRunFromLine",section["body_markdown"])
            hits=index.search("запись действий",collections=["vanessa"])["results"]
            self.assertTrue(hits)
            self.assertTrue(all(x["collection"] == "vanessa" for x in hits))
            self.assertFalse(index.pattern("vanessa:patterns:execution-debugging")["found"])

    def test_environment_launch_examples_survive_rendering_and_page_retrieval(self):
        record=next(x for x in self.vanessa if x["id"] == "vanessa:patterns:environment-readiness")
        with tempfile.TemporaryDirectory() as directory:
            pages=Path(directory)/"pages.jsonl"
            pages.write_text(json.dumps(record,ensure_ascii=False)+"\n",encoding="utf-8")
            index=V8StdIndex(pages_path=pages)
            index.load()
            result=index.page(record["id"],body_limit=6000)
            self.assertTrue(result["found"])
            self.assertFalse(result["page"]["body_truncated"])
            body=result["page"]["body_markdown"]
            for example in (
                'ENTERPRISE /TESTMANAGER /Execute EPF_PATH',
                'ENTERPRISE /TESTMANAGER /URL NAVIGATION_URL',
                '/C "runMcp;mcpPort=MCP_PORT"',
                '/IBConnectionString "File=""BASE_PATH"";"',
            ):
                with self.subTest(example=example):
                    self.assertIn(example,body)

    def test_existing_ids_and_public_exclusion_are_unchanged(self):
        records_without=generator.build_pages_jsonl([p for p in self.data["pages"] if p["collection"] != "vanessa"])
        old=[json.loads(x) for x in records_without.splitlines()]
        # Private README links are intentionally removed from indexed text only when
        # that private collection is present. Legacy identity/typing must stay stable.
        identity=lambda rows: [(x["id"], x["collection"], x["type"], x.get("document_id"), x.get("section")) for x in rows]
        self.assertEqual(identity([x for x in self.rows if x["collection"] != "vanessa"]),identity(old))
        for collection in ("v8std","corporate","yaxunit"):
            self.assertTrue(any(x["collection"] == collection for x in old))
        public=generator.build_pages_jsonl(self.data["pages"],public_only=True)
        self.assertFalse(any(json.loads(x)["collection"] == "vanessa" for x in public.splitlines()))
        actual_patterns={x["id"].removeprefix("vanessa:patterns:") for x in self.vanessa if x["type"] == "pattern"}
        expected_patterns={x["id"].removeprefix("vanessa:patterns:") for x in self.manifest["documents"] if x["id"].startswith("vanessa:patterns:")}
        self.assertEqual(actual_patterns,expected_patterns)
        self.assertTrue(PATTERNS.issubset(actual_patterns))
        self.assertTrue({"vanessa:mcp:"+x for x in BASE_MCP_TOOLS}.issubset({x["id"] for x in self.vanessa}))

    def test_offline_validation_rejects_changed_missing_extra_and_incomplete_documents(self):
        for fault in ("changed","missing","extra","coverage"):
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                destination=root/"docs/vanessa"
                shutil.copytree(ROOT/"docs/vanessa",destination)
                validate_vanessa_snapshot(root)
                card=destination/"mcp/run_scenario.md"
                if fault == "changed":
                    card.write_text("changed",encoding="utf-8")
                elif fault == "missing":
                    card.unlink()
                elif fault == "extra":
                    (destination/"mcp/unknown.md").write_text("extra",encoding="utf-8")
                else:
                    manifest=json.loads((destination/"manifest.json").read_text(encoding="utf-8"))
                    manifest["coverage"]["complete"]=False
                    (destination/"manifest.json").write_text(json.dumps(manifest),encoding="utf-8")
                with self.assertRaisesRegex(ValueError,"invalid Vanessa snapshot"):
                    validate_vanessa_snapshot(root)

    def test_sync_is_deterministic_rejects_drift_and_duplicate_tool_names(self):
        with tempfile.TemporaryDirectory() as directory:
            upstream,devkit,repository=VanessaSnapshotV2Tests.fixture(Path(directory))
            first=sync.sync(upstream,devkit,repository)
            second=sync.sync(upstream,devkit,repository,check=True)
            self.assertEqual(first,second)
            self.assertIsNone(first["sources"][0]["revision"])
            self.assertFalse(first["coverage"]["runtime_schema_verified"])
            (repository/"docs/vanessa/mcp/run_scenario.md").write_text("drift",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"stale Vanessa snapshot"):
                sync.sync(upstream,devkit,repository,check=True)
        with self.assertRaisesRegex(ValueError,"duplicate"):
            sync.tool_rows("| **test** | x |\n| **test** | y |")
        with self.assertRaisesRegex(ValueError,"missing"):
            sync.tool_rows("| **test** | x |\n| **UPSTREAM-CHANGED** | y |")

    def test_docker_packages_manifest_and_license_without_upstream_runtime(self):
        docker=(ROOT/"Dockerfile.mcp").read_text(encoding="utf-8")
        self.assertIn("COPY docs/vanessa/LICENSE",docker)
        self.assertIn("COPY docs/vanessa/manifest.json",docker)
        self.assertIn("!scripts/v8std_vanessa_snapshot.py",(ROOT/".dockerignore").read_text(encoding="utf-8"))
        self.assertNotIn("sync_vanessa_docs",(ROOT/"scripts/run_v8std_mcp_image.sh").read_text(encoding="utf-8"))


class VanessaSnapshotV2Tests(unittest.TestCase):
    def test_generated_cards_preserve_source_and_link_relevant_reference_topics(self):
        source = {"revision": None}
        description = "Документированные параметры и эффекты конкретного инструмента."
        for name in sorted(BASE_MCP_TOOLS):
            with self.subTest(tool=name):
                card = sync.render_card(name, description, source)
                self.assertIn(f"id: vanessa:mcp:{name}\n", card)
                self.assertIn(description, card)
                self.assertIn("inputSchema", card)
                self.assertNotIn("## Пример применения", card)
                self.assertNotIn("user_actions_recording(action=", card)
                self.assertNotIn("Проверьте соответствие", card)
                self.assertNotIn("в рамках задачи", card)
                topics = re.findall(r"\]\(\.\./patterns/([a-z0-9-]+)\.md\)", card)
                self.assertTrue(topics)
                self.assertEqual(len(topics), len(set(topics)))
                for stem in topics:
                    self.assertTrue((ROOT/"docs/vanessa/patterns"/(stem+".md")).is_file(), stem)
        expected = {
            "get_editor_state": "editor-workflow",
            "get_test_results": "reporting-and-artifacts",
            "run_scenario": "execution-debugging",
            "user_actions_recording": "exploration-recording",
            "find_form_elements": "form-assertions-and-tables",
            "manage_test_client_profiles": "test-client-profiles",
            "get_process_list_os": "environment-readiness",
        }
        for name, stem in expected.items():
            self.assertIn(f"../patterns/{stem}.md", sync.render_card(name, description, source))

    @staticmethod
    def fixture(root, *, extra=True):
        upstream, devkit, repository = root/"upstream", root/"devkit", root/"repository"
        destination = repository/"docs/vanessa"
        patterns = PATTERNS | ({"extra-reference"} if extra else set())
        for stem in sorted(patterns):
            target = destination/"patterns"/(stem+".md")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"---\nid: vanessa:patterns:{stem}\ncollection: vanessa\ntype: pattern\n---\n\n# {stem}\n\n## Задача\n\nСправочный рецепт.\n", encoding="utf-8")
        paths = [sync.SOURCE, *sync.EXAMPLES, "README.md", "examples/README.md", "docs/manual/Настройки.MD", "docs/training/example.feature"]
        for path in paths:
            target = upstream/path
            target.parent.mkdir(parents=True, exist_ok=True)
            body = "\n".join(f"| **{name}** | Purpose and documented options. |" for name in sorted(BASE_MCP_TOOLS)) if path == sync.SOURCE else "source text"
            target.write_text(body, encoding="utf-8")
        (upstream/"LICENSE").write_text("BSD-3-Clause fixture", encoding="utf-8")
        devkit.mkdir()
        (devkit/"README.md").write_text("unstable API", encoding="utf-8")
        required = ["vanessa:patterns:"+x for x in sorted(patterns)]
        registry = {
            "format_version": 1, "manual_version": "fixture-manual",
            "scope": "Classified text sources; external video and runtime schemas excluded.",
            "required_patterns": required,
            "entries": [{"path": path, "disposition": "curated", "patterns": [required[0]], "note": "Task-first reference for source text."} for path in sorted(paths)],
        }
        (destination/"source-map.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        return upstream, devkit, repository

    @staticmethod
    def rewrite_registry(repository, mutate, *, rehash_manifest=False):
        destination = repository/"docs/vanessa"
        path = destination/"source-map.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        mutate(registry)
        path.write_text(json.dumps(registry, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        if rehash_manifest:
            manifest_path = destination/"manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["source_map"]["sha256"] = digest(path.read_bytes())
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_dynamic_patterns_and_all_input_hashes_are_deterministic_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            upstream, devkit, repository = self.fixture(Path(directory))
            first = sync.sync(upstream, devkit, repository)
            self.assertEqual(first, sync.sync(upstream, devkit, repository, check=True))
            self.assertEqual(first["generator"]["version"], "2")
            self.assertEqual(first["format_version"], 1)
            self.assertEqual(first["coverage"]["patterns"], len(PATTERNS)+1)
            self.assertEqual(first["coverage"]["documented_tools"], len(BASE_MCP_TOOLS))
            self.assertFalse(first["coverage"]["runtime_schema_verified"])
            self.assertEqual(first["coverage"]["classified_sources"], 7)
            self.assertIn("docs/manual/Настройки.MD", {x["path"] for x in first["sources"][0]["inputs"]})
            self.assertIn("docs/training/example.feature", {x["path"] for x in first["sources"][0]["inputs"]})
            self.assertIn("LICENSE", {x["path"] for x in first["sources"][0]["inputs"]})
            for target in (upstream, devkit):
                self.assertTrue(target.resolve().is_relative_to(Path(directory).resolve()))
                shutil.rmtree(target)
            validate_vanessa_snapshot(repository)

    def test_sync_rejects_unmapped_new_source_missing_source_changed_source_and_missing_pattern(self):
        for fault in ("new-source", "missing-source", "changed-source", "missing-pattern", "extra-pattern", "bad-id", "body-id", "duplicate-id", "missing-tool"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                upstream, devkit, repository = self.fixture(Path(directory))
                sync.sync(upstream, devkit, repository)
                if fault == "new-source":
                    (upstream/"docs/manual/new.md").write_text("new", encoding="utf-8")
                elif fault == "missing-source":
                    (upstream/"docs/manual/Настройки.MD").unlink()
                elif fault == "changed-source":
                    (upstream/"docs/manual/Настройки.MD").write_text("changed", encoding="utf-8")
                elif fault == "missing-pattern":
                    (repository/"docs/vanessa/patterns/extra-reference.md").unlink()
                elif fault == "extra-pattern":
                    (repository/"docs/vanessa/patterns/unknown.md").write_text("---\nid: vanessa:patterns:unknown\n---\n", encoding="utf-8")
                elif fault == "bad-id":
                    (repository/"docs/vanessa/patterns/extra-reference.md").write_text("---\nid: vanessa:patterns:environment-readiness\n---\n", encoding="utf-8")
                elif fault == "body-id":
                    (repository/"docs/vanessa/patterns/extra-reference.md").write_text("---\ntitle: no id\n---\nid: vanessa:patterns:extra-reference\n", encoding="utf-8")
                elif fault == "duplicate-id":
                    (repository/"docs/vanessa/patterns/extra-reference.md").write_text("---\nid: vanessa:patterns:extra-reference\nid: vanessa:patterns:extra-reference\n---\n", encoding="utf-8")
                else:
                    target = upstream/sync.SOURCE
                    target.write_text("\n".join(x for x in target.read_text(encoding="utf-8").splitlines() if "**run_scenario**" not in x), encoding="utf-8")
                with self.assertRaises((ValueError, OSError)):
                    sync.sync(upstream, devkit, repository, check=True)

    def test_source_map_rejects_bad_paths_duplicates_missing_baseline_and_unknown_references(self):
        changes = {
            "traversal": lambda data: data["entries"][0].update(path="../escape.md"),
            "absolute": lambda data: data["entries"][0].update(path="C:/escape.md"),
            "duplicate": lambda data: data["entries"].append(dict(data["entries"][0])),
            "case-alias": lambda data: data["entries"].append({**data["entries"][0], "path": data["entries"][0]["path"].upper()}),
            "unknown-reference": lambda data: data["entries"][0].update(patterns=["vanessa:patterns:missing"]),
            "empty-curated": lambda data: data["entries"][0].update(patterns=[]),
            "empty-note": lambda data: data["entries"][0].update(note=""),
            "baseline-removed": lambda data: data["required_patterns"].remove("vanessa:patterns:environment-readiness"),
        }
        for fault, mutate in changes.items():
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                upstream, devkit, repository = self.fixture(Path(directory))
                self.rewrite_registry(repository, mutate)
                with self.assertRaises(ValueError):
                    sync.sync(upstream, devkit, repository)

    def test_offline_source_map_hash_inventory_required_patterns_and_counts_fail_closed(self):
        for fault in ("hash", "input-set", "required-patterns", "counts", "input-path", "input-duplicate"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as directory:
                upstream, devkit, repository = self.fixture(Path(directory))
                sync.sync(upstream, devkit, repository)
                if fault == "hash":
                    self.rewrite_registry(repository, lambda data: data.update(scope="changed"))
                elif fault == "input-set":
                    self.rewrite_registry(repository, lambda data: data["entries"].pop(), rehash_manifest=True)
                elif fault == "required-patterns":
                    self.rewrite_registry(repository, lambda data: data["required_patterns"].append("vanessa:patterns:zzz-missing"), rehash_manifest=True)
                else:
                    path = repository/"docs/vanessa/manifest.json"
                    manifest = json.loads(path.read_text(encoding="utf-8"))
                    if fault == "counts":
                        manifest["coverage"]["classified_sources"] += 1
                    else:
                        source = manifest["sources"][0]
                        if fault == "input-path":
                            source["inputs"][0]["path"] = "../escape"
                        else:
                            source["inputs"].append(dict(source["inputs"][0]))
                        source["content_revision"] = "sha256:"+digest(json.dumps(source["inputs"], sort_keys=True, ensure_ascii=False).encode())
                    path.write_text(json.dumps(manifest), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "invalid Vanessa snapshot"):
                    validate_vanessa_snapshot(repository)

    def test_legacy_generator_one_remains_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            upstream, devkit, repository = self.fixture(Path(directory), extra=False)
            manifest = sync.sync(upstream, devkit, repository)
            manifest["generator"]["version"] = "1"
            manifest.pop("source_map")
            path = repository/"docs/vanessa/manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            (repository/"docs/vanessa/source-map.json").unlink()
            validate_vanessa_snapshot(repository)


if __name__ == "__main__":
    unittest.main()
