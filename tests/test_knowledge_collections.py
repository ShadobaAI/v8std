import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_module(name: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class KnowledgeCollectionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_module("generate_ai_artifacts")
        cls.collections = load_module("v8std_knowledge_collections")
        cls.index_module = load_module("v8std_mcp_index")
        cls.index_data = cls.generator.build_site_ai_index(REPO_ROOT)
        cls.jsonl = cls.generator.build_pages_jsonl(cls.index_data["pages"])
        cls.rows = [json.loads(line) for line in cls.jsonl.splitlines()]
        cls.index = cls.index_module.V8StdIndex(
            pages_path=REPO_ROOT / "docs" / "ai" / "pages.jsonl",
            vectors_path=REPO_ROOT / "docs" / "ai" / "search-vectors.jsonl",
        )
        cls.index.load()

    def test_existing_pages_get_backward_compatible_v8std_collection(self):
        std437 = next(row for row in self.rows if row["id"] == "std437")
        self.assertEqual(std437["collection"], "v8std")
        self.assertEqual(std437["type"], "standard")

    def test_future_corporate_standard_and_rule_are_section_records(self):
        base = {
            "description": "Описание",
            "aliases": [],
            "related": [],
            "source_urls": [],
            "_publish_publicly": False,
        }
        pages = [
            {
                **base,
                "id": "corporate:future-standard",
                "collection": "corporate",
                "type": "standard",
                "level": "recommended",
                "tags": ["future"],
                "title": "Будущий стандарт",
                "url": "https://example.invalid/corporate/future-standard/",
                "markdown_url": "https://example.invalid/corporate/future-standard.md",
                "source_path": "corporate/future-standard.md",
                "body_markdown": "## Требование\n\nТекст стандарта.",
            },
            {
                **base,
                "id": "corporate:future-rule",
                "collection": "corporate",
                "type": "rule",
                "level": "mandatory",
                "tags": ["future"],
                "title": "Будущее правило",
                "url": "https://example.invalid/corporate/future-rule/",
                "markdown_url": "https://example.invalid/corporate/future-rule.md",
                "source_path": "corporate/future-rule.md",
                "body_markdown": "## Требование\n\nТекст правила.",
            },
        ]
        corporate = self.collections.expand_retrieval_records(pages)
        self.assertTrue(any(row["type"] == "standard" and row["level"] == "recommended" for row in corporate))
        self.assertTrue(any(row["type"] == "rule" and row["level"] == "mandatory" for row in corporate))
        self.assertTrue(all(row.get("section") and row.get("document_id") for row in corporate))

    def test_repository_ships_private_additional_work_rules(self):
        expected_documents = {
            "corporate:work:bsl-change-policy",
            "corporate:work:bsl-type-transparency",
            "corporate:work:bsl-readability",
            "corporate:work:bsl-formatting",
            "corporate:work:module-organization",
            "corporate:work:query-conventions",
            "corporate:work:error-reporting",
        }
        corporate_rows = [row for row in self.rows if row["collection"] == "corporate"]
        self.assertEqual(
            {row["document_id"] for row in corporate_rows},
            expected_documents,
        )
        self.assertEqual(
            {row["id"] for row in corporate_rows},
            {f"{document_id}:overview" for document_id in expected_documents},
        )
        self.assertTrue(all(row["level"] == "mandatory" for row in corporate_rows))
        self.assertTrue(all("work" in row["tags"] for row in corporate_rows))

        expected_files = {
            "README.md",
            "work/README.md",
            "work/bsl-change-policy.md",
            "work/bsl-formatting.md",
            "work/bsl-readability.md",
            "work/bsl-type-transparency.md",
            "work/error-reporting.md",
            "work/module-organization.md",
            "work/query-conventions.md",
        }
        corporate_files = sorted(
            path.relative_to(REPO_ROOT / "docs" / "corporate").as_posix()
            for path in (REPO_ROOT / "docs" / "corporate").rglob("*")
            if path.is_file()
        )
        self.assertEqual(set(corporate_files), expected_files)

    def test_unindexed_corporate_indexes_do_not_require_retrieval_ids(self):
        corporate_indexes = [
            page
            for page in self.index_data["pages"]
            if Path(page["source_path"]).as_posix()
            in {"corporate/README.md", "corporate/work/README.md"}
        ]
        self.assertEqual(len(corporate_indexes), 2)
        self.assertTrue(all(not page["_index_for_ai"] for page in corporate_indexes))
        self.assertTrue(all(not page["id"] for page in corporate_indexes))

    def test_yaxunit_has_atomic_api_cards_and_compact_patterns(self):
        yaxunit = [row for row in self.rows if row["collection"] == "yaxunit"]
        api = [row for row in yaxunit if row["type"] == "reference"]
        patterns = [row for row in yaxunit if row["type"] == "pattern"]
        self.assertGreater(len(api), 450)
        expected_pattern_ids = {
            "yaxunit:patterns:assertions",
            "yaxunit:patterns:authoring-baseline",
            "yaxunit:patterns:data-isolation",
            "yaxunit:patterns:dependencies",
            "yaxunit:patterns:lifecycle-and-contexts",
            "yaxunit:patterns:mocking",
            "yaxunit:patterns:naming",
            "yaxunit:patterns:predicates-and-queries",
            "yaxunit:patterns:registration-and-parameters",
            "yaxunit:patterns:test-analysis-and-migration",
            "yaxunit:patterns:test-data",
            "yaxunit:patterns:test-module",
        }
        self.assertEqual({row["id"] for row in patterns}, expected_pattern_ids)
        self.assertTrue(all(len(row["body_markdown"]) <= 2000 for row in api))
        self.assertTrue(all(len(row["body_markdown"]) <= 1500 for row in patterns))
        self.assertFalse(any("](/api/" in row["body_markdown"] for row in yaxunit))
        self.assertTrue(
            all(f'{row["id"]}:overview' in row["aliases"] for row in patterns),
            "legacy generated pattern IDs must remain aliases",
        )
        self.assertTrue(all("#overview" not in row["url"] for row in patterns))
        self.assertTrue(all("#overview" not in row["markdown_url"] for row in patterns))

        pattern_aliases: dict[str, str] = {}
        for row in patterns:
            for alias in row["aliases"]:
                normalized = alias.strip().casefold()
                owner = pattern_aliases.setdefault(normalized, row["id"])
                self.assertEqual(owner, row["id"], f"ambiguous YaXUnit pattern alias: {alias}")

        combined_patterns = "\n".join(row["body_markdown"] for row in patterns)
        self.assertNotIn("Функция ИсполняемыеСценарии", combined_patterns)
        self.assertIn("Процедура ИсполняемыеСценарии() Экспорт", combined_patterns)
        self.assertIn("ЮТест.ОжидаетЧтоТаблицаБазы", combined_patterns)
        predicates = next(
            row for row in patterns if row["id"] == "yaxunit:patterns:predicates-and-queries"
        )
        self.assertNotIn("Записи = ЮТЗапросы.Записи", predicates["body_markdown"])
        self.assertIn(".СодержитЗаписи(Условие)", predicates["body_markdown"])
        naming = next(row for row in patterns if row["id"] == "yaxunit:patterns:naming")
        self.assertIn("ИсполняемыеСценарии", naming["body_markdown"])
        self.assertIn("ОМ_", naming["body_markdown"])
        self.assertIn("вспомогательный модуль", naming["body_markdown"].lower())
        isolation = next(row for row in patterns if row["id"] == "yaxunit:patterns:data-isolation")
        self.assertEqual(isolation["body_markdown"].count("ЮТТесты.ВТранзакции()"), 1)
        self.assertGreaterEqual(isolation["body_markdown"].count("ДобавитьТестовыйНабор"), 2)

        assertion = next(row for row in api if row.get("section") == "ЮТест.ОжидаетЧто")
        self.assertIn(
            'Функция ЮТест.ОжидаетЧто(ПроверяемоеЗначение, Сообщение = "") Экспорт',
            assertion["body_markdown"],
        )
        deprecated = next(row for row in api if row.get("section") == "ЮТТесты.Вызов")
        self.assertIn("**Статус:** устарел", deprecated["body_markdown"])
        self.assertIn("`ЮТТесты.Настроить`", deprecated["body_markdown"])
        builder = next(
            row for row in api if row.get("section") == "ЮТКонструкторТестовыхДанных.Записать"
        )
        self.assertIn(
            "Функция ЮТКонструкторТестовыхДанных.Записать(ВернутьОбъект = Ложь",
            builder["body_markdown"],
        )
        self.assertNotIn("**Минимальный пример:**", builder["body_markdown"])

        manifest = json.loads((REPO_ROOT / "docs" / "yaxunit" / "manifest.json").read_text(encoding="utf-8"))
        exported = sum(target["exports"] for target in manifest["targets"])
        api_methods = [row for row in api if row.get("section") != "Обзор"]
        self.assertEqual(len(api_methods), exported)

        api_names = {row.get("section") for row in api_methods}
        direct_calls = {
            match.group(0)
            for row in patterns
            for match in re.finditer(r"\b(?:ЮТ|Мокито)[A-Za-zА-Яа-яЁё0-9_]*\.[A-Za-zА-Яа-яЁё0-9_]+", row["body_markdown"])
        }
        self.assertEqual(sorted(direct_calls - api_names), [])

    def test_collection_filter_is_strict_and_default_limit_is_small(self):
        yaxunit = self.index.search(
            "конструктор объекта",
            collections=["yaxunit"],
            types=["reference"],
        )
        self.assertTrue(yaxunit["results"])
        self.assertTrue(all(row["collection"] == "yaxunit" for row in yaxunit["results"]))
        with tempfile.TemporaryDirectory() as temp_dir:
            pages_path = Path(temp_dir) / "pages.jsonl"
            pages_path.write_text(
                json.dumps(
                    {
                        "id": "corporate:future-rule:requirement",
                        "document_id": "corporate:future-rule",
                        "collection": "corporate",
                        "type": "rule",
                        "level": "mandatory",
                        "tags": ["future"],
                        "section": "Требование",
                        "title": "Будущее правило — Требование",
                        "description": "Изоляция внешних зависимостей",
                        "body_markdown": "Изоляция внешних зависимостей обязательна.",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            corporate_index = self.index_module.V8StdIndex(pages_path=pages_path)
            corporate_index.load()
            corporate = corporate_index.search("изоляция внешних зависимостей", collections=["corporate"])
            self.assertTrue(corporate["results"])
            self.assertTrue(all(row["collection"] == "corporate" for row in corporate["results"]))
        self.assertLessEqual(len(self.index.search("запрос")["results"]), 3)

    def test_yaxunit_search_prefers_exact_api_and_usage_patterns(self):
        cases = {
            "сигнатура ЮТест.ОжидаетЧто": "yaxunit:api:ютест:ютест-ожидаетчто",
            "как проверить исключение": "yaxunit:patterns:assertions",
            "как создать тестовый документ": "yaxunit:patterns:test-data",
            "как мокировать вызов метода": "yaxunit:patterns:mocking",
            "параметризованный тест": "yaxunit:patterns:registration-and-parameters",
            "ЮТТесты.Вызов": "yaxunit:api:юттесты:юттесты-вызов",
        }
        for query, expected_id in cases.items():
            with self.subTest(query=query):
                result = self.index.search(query, collections=["yaxunit"])
                self.assertTrue(result["results"])
                self.assertEqual(result["results"][0]["id"], expected_id)

    def test_yaxunit_routing_contract_references_known_direct_ids(self):
        contract = json.loads(
            (REPO_ROOT / "tests" / "yaxunit_retrieval_contract.json").read_text(encoding="utf-8")
        )
        pattern_ids = {
            row["id"]
            for row in self.rows
            if row["collection"] == "yaxunit" and row["type"] == "pattern"
        }
        for case in contract:
            with self.subTest(case=case["scenario"]):
                required = case["required"]
                self.assertEqual(len(required), len(set(required)))
                self.assertTrue(set(required) <= pattern_ids)
                if case["known"]:
                    self.assertEqual(case["search_max"], 0)
                else:
                    self.assertLessEqual(case["search_max"], 1)

    def test_engineering_routing_contract_has_valid_ids_and_budgets(self):
        contract = json.loads(
            (REPO_ROOT / "tests" / "engineering_retrieval_contract.json").read_text(
                encoding="utf-8"
            )
        )
        page_ids = {row["id"] for row in self.rows}
        for case in contract:
            with self.subTest(case=case["scenario"]):
                required = case["required"]
                self.assertEqual(len(required), len(set(required)))
                self.assertTrue(set(required) <= page_ids)
                if case["known"]:
                    self.assertEqual(case["search_max"], 0)
                else:
                    self.assertLessEqual(case["search_max"], 1)

    def test_legacy_yaxunit_pattern_id_resolves_to_canonical_page(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pages_path = Path(temp_dir) / "pages.jsonl"
            pages_path.write_text(self.jsonl, encoding="utf-8")
            index = self.index_module.V8StdIndex(pages_path=pages_path)
            index.load()
            page = index.page("yaxunit:patterns:authoring-baseline:overview")
            self.assertTrue(page["found"])
            self.assertEqual(page["page"]["id"], "yaxunit:patterns:authoring-baseline")

    def test_get_page_returns_only_selected_yaxunit_section(self):
        record = next(
            row
            for row in self.rows
            if row["collection"] == "yaxunit" and row.get("section") == "ЮТест.ОжидаетЧто"
        )
        result = self.index.page(record["id"], body_limit=30000)
        self.assertTrue(result["found"])
        self.assertEqual(result["page"]["body_markdown"], record["body_markdown"])
        self.assertNotIn("## ЮТест.Данные", result["page"]["body_markdown"])

    def test_private_collections_are_absent_from_public_outputs(self):
        public_rows = [
            json.loads(line)
            for line in self.generator.build_pages_jsonl(self.index_data["pages"], public_only=True).splitlines()
        ]
        llms = self.generator.build_llms_full_txt(self.index_data)
        self.assertTrue(all(row["collection"] == "v8std" for row in public_rows))
        self.assertNotIn("corporate:testability", llms)
        self.assertNotIn("yaxunit:", llms)

    def test_generation_keeps_stable_ids(self):
        first = [row["id"] for row in self.rows]
        second = [
            json.loads(line)["id"]
            for line in self.generator.build_pages_jsonl(self.index_data["pages"]).splitlines()
        ]
        self.assertEqual(first, second)

    def test_index_rejects_invalid_metadata_and_duplicate_ids(self):
        payloads = [
            [
                {"id": "duplicate", "type": "service", "collection": "v8std"},
                {"id": "duplicate", "type": "service", "collection": "v8std"},
            ],
            [{"id": "bad-type", "type": "unknown", "collection": "v8std"}],
            [{"id": "bad-collection", "type": "service", "collection": "unknown"}],
            [{"id": "bad-level", "type": "rule", "collection": "corporate", "level": "critical"}],
        ]
        for rows in payloads:
            with self.subTest(rows=rows), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "pages.jsonl"
                path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
                with self.assertRaises(self.index_module.IndexLoadError):
                    self.index_module.V8StdIndex(pages_path=path).load()


class YaXUnitSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync = load_module("sync_yaxunit_docs")

    def test_sync_is_deterministic_and_missing_module_source_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source_file = source / "exts" / "yaxunit" / "src" / "CommonModules" / "ЮТест" / "Module.bsl"
            source_file.parent.mkdir(parents=True)
            source_file.write_text(
                "// Проверяет значение.\n"
                "//\n"
                "// Параметры:\n"
                "//  Значение - Произвольный - Проверяемое значение\n"
                "Функция Проверить(Значение) Экспорт\n"
                "    Возврат Значение;\n"
                "КонецФункции\n\n"
                "// Устарела. Старый вызов.\n"
                "Функция СтарыйВызов() Экспорт\n"
                "    ВызовУстаревшегоМетода(\"ЮТест.СтарыйВызов\", \"ЮТест.Проверить\", \"1.0\");\n"
                "КонецФункции\n",
                encoding="utf-8",
            )
            (source / "LICENSE").write_bytes(b"Apache License\n")
            modules = root / "modules.txt"
            modules.write_text("ЮТест|CommonModules/ЮТест/Module.bsl\n", encoding="utf-8")
            destination = root / "destination"

            self.sync.synchronize(source, destination, modules, "revision-1", check=False)
            first = {
                path.relative_to(destination).as_posix(): path.read_bytes()
                for path in destination.rglob("*")
                if path.is_file()
            }
            self.sync.synchronize(source, destination, modules, "revision-1", check=False)
            second = {
                path.relative_to(destination).as_posix(): path.read_bytes()
                for path in destination.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first, second)
            self.sync.synchronize(source, destination, modules, "revision-1", check=True)
            generated = (destination / "api" / "ЮТест.md").read_text(encoding="utf-8")
            self.assertIn("Функция ЮТест.Проверить(Значение) Экспорт", generated)
            self.assertIn("Используйте `ЮТест.Проверить`", generated)
            manifest = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["targets"][0]["exports"], 2)

            source_file.unlink()
            with self.assertRaises(FileNotFoundError):
                self.sync.synchronize(source, destination, modules, "revision-1", check=False)


class PublicKnowledgePublishingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.publisher = load_module("publish_public_knowledge")

    def test_prunes_private_routes_search_and_sitemap(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            site = Path(temp_dir)
            (site / "corporate").mkdir()
            (site / "corporate" / "secret.html").write_text("secret", encoding="utf-8")
            (site / "yaxunit").mkdir(parents=True)
            (site / "yaxunit" / "secret.html").write_text("secret", encoding="utf-8")
            (site / "search.json").write_text(
                json.dumps(
                    {
                        "docs": [
                            {"location": "std/437/", "text": "public"},
                            {"location": "corporate/rules/testability/", "text": "secret"},
                            {"location": "/yaxunit/features/", "text": "secret"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (site / "sitemap.xml").write_text(
                "<?xml version='1.0' encoding='utf-8'?>\n"
                "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
                "<url><loc>https://v8std.ru/std/437/</loc></url>"
                "<url><loc>https://v8std.ru/corporate/rules/testability/</loc></url>"
                "</urlset>",
                encoding="utf-8",
            )

            self.publisher.prune_private_site(site)

            self.assertFalse((site / "corporate").exists())
            self.assertFalse((site / "yaxunit").exists())
            search = json.loads((site / "search.json").read_text(encoding="utf-8"))
            self.assertEqual([item["location"] for item in search["docs"]], ["std/437/"])
            sitemap = (site / "sitemap.xml").read_text(encoding="utf-8")
            self.assertIn("std/437", sitemap)
            self.assertNotIn("corporate", sitemap)


class PublicKnowledgePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preparer = load_module("prepare_public_knowledge")

    def test_public_docs_input_excludes_private_collections(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs" / "public").mkdir(parents=True)
            (root / "docs" / "corporate").mkdir()
            (root / "docs" / "yaxunit").mkdir()
            (root / "docs" / "public" / "index.md").write_text("public", encoding="utf-8")
            (root / "docs" / "corporate" / "secret.md").write_text("secret", encoding="utf-8")
            (root / "docs" / "yaxunit" / "secret.md").write_text("secret", encoding="utf-8")
            (root / "zensical.toml").write_text("[project]\nsite_name = 'test'\n", encoding="utf-8")

            config = self.preparer.prepare(root)
            staging = root / self.preparer.STAGING_DIRECTORY
            self.assertTrue((staging / "public" / "index.md").is_file())
            self.assertFalse((staging / "corporate").exists())
            self.assertFalse((staging / "yaxunit").exists())
            self.assertIn('docs_dir = ".cache/public-docs"', config.read_text(encoding="utf-8"))

            self.preparer.clean(root)
            self.assertFalse(config.exists())
            self.assertFalse(staging.exists())

    # BEGIN V8STD-FORK
    def test_local_config_exposes_knowledge_collections_in_navigation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs" / "corporate").mkdir(parents=True)
            (root / "docs" / "yaxunit" / "patterns").mkdir(parents=True)
            (root / "docs" / "yaxunit" / "api").mkdir(parents=True)
            (root / "docs" / "corporate" / "README.md").write_text(
                "# Корпоративные материалы\n", encoding="utf-8"
            )
            (root / "docs" / "yaxunit" / "README.md").write_text(
                "# База знаний YaXUnit\n", encoding="utf-8"
            )
            (root / "docs" / "yaxunit" / "patterns" / "mocking.md").write_text(
                "# Мокирование\n", encoding="utf-8"
            )
            (root / "docs" / "yaxunit" / "api" / "ЮТест.md").write_text(
                "# API ЮТест\n", encoding="utf-8"
            )
            (root / "zensical.toml").write_text(
                "[project]\nsite_name = 'test'\n", encoding="utf-8"
            )

            config = self.preparer.prepare_local(root)
            payload = config.read_text(encoding="utf-8")
            self.assertIn('"YaXUnit"', payload)
            self.assertIn('"Паттерны использования"', payload)
            self.assertIn('"API ядра"', payload)
            self.assertIn('"Корпоративные материалы" = "corporate/README.md"', payload)
            self.assertNotIn("docs_dir", payload)

            self.preparer.clean_local(root)
            self.assertFalse(config.exists())
    # END V8STD-FORK


if __name__ == "__main__":
    unittest.main()
