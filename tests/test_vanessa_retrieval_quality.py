"""User-task retrieval checks for curated Vanessa knowledge, without upstream access."""
from __future__ import annotations
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from runtime.v8std_mcp_index import V8StdIndex
generator=importlib.import_module('generate_ai_artifacts')

class VanessaRetrievalQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory=tempfile.TemporaryDirectory()
        data=generator.build_site_ai_index(ROOT)
        text=generator.build_pages_jsonl(data['pages'])
        cls.rows=[json.loads(line) for line in text.splitlines()]
        cls.patterns={row['id']:row for row in cls.rows if row['collection']=='vanessa' and row['type']=='pattern'}
        path=Path(cls.directory.name)/'pages.jsonl'
        path.write_text(text,encoding='utf-8')
        cls.index=V8StdIndex(pages_path=path)
        cls.index.load()

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_task_queries_find_useful_recipe_in_first_three(self):
        cases={
            'структура папок UI тестов features библиотеки':'project-layout',
            'вынести повторяющиеся действия экспортный сценарий':'subscenarios-and-libraries',
            'подготовка данных независимый повторный запуск':'test-data-strategies',
            'несколько наборов данных Примеры':'scenario-outlines',
            'сценарий падает только на CI сравнение формы':'compatibility-and-troubleshooting',
            'таймаут асинхронного шага пауза':'synchronization-and-waits',
            'веб клиент выбор файла диалог':'files-and-dialogs',
            'проверка таблицы MXL эталон звездочка':'form-assertions-and-tables',
            'код менеджера и клиента разные базы':'embedded-code-and-context',
            'отчёт Allure JUnit артефакты':'reporting-and-artifacts',
            'SMTP IMAP кириллица тема письма':'email-testing',
            'VAParams приоритет переменные среды':'configuration-and-ci',
            'фильтр сценариев теги исключение':'tags-and-selection',
            'GlobalVars глобальные переменные параметры':'variables-and-parameters',
        }
        for mode in ('bm25','hybrid'):
            for query,expected in cases.items():
                with self.subTest(mode=mode,query=query):
                    result=self.index.search(query,collections=['vanessa'],types=['pattern'],mode=mode,limit=3)
                    ids=[row['id'] for row in result['results']]
                    self.assertIn('vanessa:patterns:'+expected,ids)

    def test_recipes_are_complete_structured_sourced_and_connected(self):
        self.assertEqual(len(self.patterns),39)
        for key,record in self.patterns.items():
            with self.subTest(id=key):
                result=self.index.page(key,body_limit=12000)
                self.assertTrue(result['found'])
                self.assertFalse(result['page']['body_truncated'])
                self.assertTrue(record['source_urls'],'Missing source URLs')
                self.assertTrue(record['related'],'Missing knowledge links')
                self.assertGreaterEqual(record['body_markdown'].count('\n## '),2)
                self.assertGreaterEqual(len(record['aliases']),3)
        section=self.index.section('vanessa:patterns:project-layout','Роли каталогов и параметры Vanessa')
        self.assertTrue(section['found'])
        self.assertIn('librarycatalogs',section['body_markdown'])

    def test_executable_gherkin_tokens_survive_actual_render_and_retrieval(self):
        body=self.index.page('vanessa:patterns:scenario-outlines',body_limit=12000)['page']['body_markdown']
        self.assertIn('И я запоминаю строку <Вход> в переменную',body)
        self.assertIn('Тогда переменная \"Результат\" имеет значение <Ожидание>',body)
        variables=self.index.page('vanessa:patterns:variables-and-parameters',body_limit=12000)['page']['body_markdown']
        self.assertIn('GlobalVars',variables)
        self.assertIn('КонтекстСохраняемый',variables)
        embedded=self.index.page('vanessa:patterns:embedded-code-and-context',body_limit=12000)['page']['body_markdown']
        self.assertIn('Ванесса.Объект.ЗначениеНаСервере = Контекст.ИмяПеременной;',embedded)
        self.assertIn('"""bsl',embedded)

    def test_editor_context_commands_are_retrievable_with_distinct_scope(self):
        result=self.index.section('vanessa:patterns:editor-workflow','Выполнить часть сценария и перейти к связанному файлу')
        self.assertTrue(result['found'])
        body=result['body_markdown']
        for token in ('Ctrl+F5','Ctrl+Shift+F5','Alt+F5','F11','Shift+F7','Ctrl+F7','Ctrl+Shift+T','Ctrl+J'):
            self.assertIn(token,body)
        self.assertIn('Следующие сценарии не выполняются',body)
        self.assertIn('После текущего выполняются следующие сценарии',body)
        self.assertIn('активно окно',body)

    def test_source_urls_with_spaces_and_knowledge_skill_boundary(self):
        expected='https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/Режим%20совместимости%208.2.md'
        for stem in ('compatibility-and-troubleshooting','runtime-distribution-and-custom-steps'):
            page=self.index.page('vanessa:patterns:'+stem,body_limit=12000)['page']
            self.assertIn(expected,page['source_urls'])
        env=self.index.page('vanessa:patterns:environment-readiness',body_limit=12000)['page']['body_markdown']
        self.assertNotIn('Выберите профиль',env)
        self.assertNotIn('Подтвердите владение',env)
        execution=self.index.page('vanessa:patterns:execution-debugging',body_limit=12000)['page']['body_markdown']
        self.assertNotIn('awaiting_editor_enable',execution)
        self.assertNotIn('--editor-transition',execution)
        self.assertIn('отключая',execution)

    def test_coverage_declares_missing_media_instead_of_invented_syntax(self):
        data=json.loads((ROOT/'docs/vanessa/source-map.json').read_text(encoding='utf-8'))
        pointer=[entry for entry in data['entries'] if entry['disposition']=='pointer_only']
        self.assertEqual(len(pointer),3)
        self.assertTrue(all('видео' in entry['note'].lower() for entry in pointer))
        manual=[entry for entry in data['entries'] if entry['path'].startswith('docs/MainHelp/1.2.043.1/')]
        self.assertEqual(len(manual),175)
        self.assertEqual({entry['disposition'] for entry in manual},{'curated','pointer_only','navigation'})
        self.assertTrue(any(entry['disposition']=='example_workflow' for entry in data['entries']))
        docker=(ROOT/'Dockerfile.mcp').read_text(encoding='utf-8')
        self.assertIn('COPY docs/vanessa/source-map.json /opt/v8std/data/vanessa-source-map.json',docker)

if __name__=='__main__':unittest.main()
