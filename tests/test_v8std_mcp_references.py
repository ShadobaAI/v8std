"""Knowledge navigation stays in MCP without changing source or executable examples."""
import copy
import json
import unittest
import threading
from unittest.mock import patch

from tests import mcp_snapshot_fixtures as fixture
from tests.test_v8std_mcp_tools_only import http_rpc, initialize, call_tool
from runtime.v8std_mcp_index import V8StdIndex
from runtime.v8std_mcp_runtime import SnapshotIndex, build_generation
from runtime.v8std_mcp_snapshot_format import verify_archive
from runtime.v8std_mcp_references import ReferenceCatalog, ToolReferenceIndex, present_mcp_result, TOOL_REFERENCES
from runtime.v8std_mcp_presentation import present_tool_markdown


class ReferencePresentationTests(unittest.TestCase):
    def setUp(self):
        self.pages=[fixture.page_fixture()]
        self.catalog=ReferenceCatalog(self.pages)

    def markdown(self,text):
        return present_tool_markdown(text,self.catalog,context='https://v8std.ru/std/437.md')

    def test_links_become_existing_corpus_references_and_sources_keep_their_labels(self):
        text='[стандарт](https://v8std.ru/std/437/?view=full#query) [источник](https://its.1c.ru/db/v8std#437)'
        self.assertEqual(self.markdown(text),'[стандарт](v8std:std437) источник')
        self.assertEqual(self.markdown('[см.](437.md)'), '[см.](v8std:std437)')
        self.assertEqual(self.markdown('https://v8std.ru/std/437/ и https://external.invalid/x.'), 'v8std:std437 и .')

    def test_references_nested_labels_images_and_containers_preserve_text(self):
        text='> [сложный **текст**][s] и ![рисунок](https://external.invalid/img.png)\r\n>\r\n> [s]: https://external.invalid/x "title"\r\n'
        body=self.markdown(text)
        self.assertIn('сложный **текст** и рисунок',body)
        self.assertNotIn('https://',body)
        self.assertIn('\r\n',body)
        known='[Стандарт][s]\n\n[s]: https://v8std.ru/std/437/\n'
        self.assertIn('[s]: v8std:std437',self.markdown(known))
        self.assertNotIn('https://',self.markdown('![https://external.invalid/image](https://external.invalid/image)'))

    def test_literal_code_and_gherkin_angles_remain_byte_exact(self):
        code='```gherkin\r\nИ строка <Вход> равна <Ожидание>\r\nИ адрес "https://example.invalid/x"\r\n```'
        inline='`[literal](https://example.invalid/x)`'
        html='<pre><code>https://example.invalid/x</code></pre>'
        for text in (code,inline,html):
            self.assertEqual(self.markdown(text),text)

    def test_html_and_metadata_do_not_offer_web_navigation(self):
        text='<a href="https://external.invalid/x">источник</a>\n\n<a href="https://external.invalid/x">https://external.invalid/x</a>'
        self.assertNotIn('https://',self.markdown(text))
        page=copy.deepcopy(self.pages[0]); page['body_markdown']='[S](https://v8std.ru/std/437/)'
        original=copy.deepcopy(page)
        result=present_mcp_result({'page':page,'candidates':[page]},self.pages)
        self.assertEqual(page,original)
        for value in (result['page'],result['candidates'][0]):
            self.assertNotIn('url',value)
            self.assertNotIn('source_urls',value)
            self.assertNotIn('markdown_url',value)
            self.assertEqual(value['ref'],'v8std:std437')
        self.assertNotIn('https://',json.dumps(result))

    def test_ambiguous_sections_are_explicit_and_exact_anchors_still_resolve(self):
        pages=[{'id':'A','title':'Раздел A','url':'https://v8std.ru/guide/#a','source_path':'guide.md'},
               {'id':'B','title':'Раздел B','url':'https://v8std.ru/guide/#b','source_path':'guide.md'}]
        page={'id':'X','body_markdown':'[Руководство](guide.md)'}
        result=present_mcp_result(page,pages)
        self.assertEqual(result['body_markdown'],'Руководство')
        self.assertEqual([item['ref'] for item in result['reference_candidates']],['v8std:A','v8std:B'])
        catalog=ReferenceCatalog(pages)
        self.assertEqual(catalog.link('https://v8std.ru/guide/#b'),'v8std:B')

    def test_relative_vanessa_links_resolve_to_their_actual_ids(self):
        pages=[{'id':'vanessa:patterns:one','url':'https://v8std.ru/vanessa/patterns/one/',
                'markdown_url':'https://v8std.ru/vanessa/patterns/one.md','body_markdown':'[Другая](two.md)'},
               {'id':'vanessa:patterns:two','url':'https://v8std.ru/vanessa/patterns/two/',
                'markdown_url':'https://v8std.ru/vanessa/patterns/two.md'}]
        result=present_mcp_result(pages[0],pages)
        self.assertEqual(result['body_markdown'],'[Другая](v8std:vanessa:patterns:two)')


class ReferenceWireTests(unittest.TestCase):
    def index(self):
        files=fixture.corpus_files()
        return V8StdIndex.from_validated_bytes(files['pages.jsonl'],files['search-vectors.jsonl'])

    def test_all_eleven_tools_use_the_same_reference_view_on_real_wire(self):
        index=self.index()
        calls={
            'v8std_search':{'query':'std437'},
            'v8std_get_page':{'id_or_alias_or_url':'v8std:std437'},
            'v8std_get_summary':{'id_or_alias_or_url':'v8std:std437'},
            'v8std_get_section':{'id_or_alias_or_url':'v8std:std437','heading':'Запросы'},
            'v8std_get_pattern':{'id_or_alias_or_url':'v8std:std437'},
            'v8std_get_api_card':{'module_or_alias':'v8std:std437'},
            'v8std_get_requirements_for_context':{'context':'Запросы'},
            'v8std_get_related':{'id_or_alias_or_url':'v8std:std437'},
            'v8std_get_related_ids':{'id_or_alias_or_url':'v8std:std437'},
            'v8std_explain_snippet':{'snippet':'Адрес = \"https://example.invalid/api\";'},
            'v8std_explain_diagnostics':{'codes':['missing']},
        }
        with patch.object(index,'_fetch_url',side_effect=AssertionError('network')):
            with http_rpc(index) as rpc:
                initialize(rpc)
                for name,args in calls.items():
                    with self.subTest(tool=name):
                        result=call_tool(self,rpc,name,args)
                        output=json.dumps(result,ensure_ascii=False)
                        if name=='v8std_explain_snippet':
                            self.assertIn('https://example.invalid/api',result['normalized_text'])
                        self.assertNotIn('"markdown_url"',output)
                        self.assertNotIn('"source_urls"',output)
                        self.assertNotIn('[Стандарт](https://',output)
                page=call_tool(self,rpc,'v8std_get_page',{'id_or_alias_or_url':'v8std:std437'})
                self.assertTrue(page['found'])
                self.assertIn('[Стандарт](v8std:std437)',page['page']['body_markdown'])
        self.assertFalse(TOOL_REFERENCES.get())
        self.assertEqual(index.page('std437')['page']['body_markdown'],fixture.BODY)

    def test_successful_compact_cards_format_before_cutting_code_literals(self):
        pattern={**fixture.page_fixture(), 'id':'yaxunit:patterns:boundary',
                 'collection':'yaxunit', 'type':'pattern', 'title':'Граничнаяпараметризация',
                 'url':'https://v8std.ru/yaxunit/patterns/boundary/',
                 'markdown_url':'https://v8std.ru/yaxunit/patterns/boundary.md',
                 'aliases':[], 'tags':['pattern'],
                 'body_markdown':'# Граничнаяпараметризация\n\n`https://example.invalid/'+('x'*1600)+'`'}
        api={**pattern,'id':'yaxunit:api:boundary','type':'reference','tags':['api','Модуль'],
             'url':'https://v8std.ru/yaxunit/api/boundary/',
             'markdown_url':'https://v8std.ru/yaxunit/api/boundary.md',
             'body_markdown':'# API\n\n## Метод\n\n`https://example.invalid/'+('x'*1600)+'`'}
        pages=[fixture.page_fixture(),pattern,api]
        index=V8StdIndex.from_validated_bytes(fixture.jsonl_bytes(pages),fixture.jsonl_bytes(fixture.vector_fixtures()))
        with http_rpc(index) as rpc:
            initialize(rpc)
            cases=[('v8std_get_page',{'id_or_alias_or_url':'v8std:'+pattern['id'],'body_limit':1000}),
                   ('v8std_get_summary',{'id_or_alias_or_url':'v8std:'+pattern['id'],'body_limit':250}),
                   ('v8std_get_pattern',{'id_or_alias_or_url':'v8std:'+pattern['id'],'body_limit':250}),
                   ('v8std_get_api_card',{'module_or_alias':'v8std:'+api['id'],'body_limit':250}),
                   ('v8std_get_api_card',{'module_or_alias':'v8std:'+api['id'],'member':'Метод','body_limit':250}),
                   ('v8std_get_section',{'id_or_alias_or_url':'v8std:'+api['id'],'heading':'Метод','body_limit':250})]
            for name,args in cases:
                with self.subTest(tool=name,args=args):
                    result=call_tool(self,rpc,name,args)
                    self.assertTrue(result['found'])
                    body=result.get('page',result)
                    self.assertIn('`https://example.invalid/',body['body_markdown'])
                    self.assertTrue(body['body_truncated'])
                    self.assertLessEqual(len(body['body_markdown']),args['body_limit']+5)

    def test_legacy_refresh_cannot_replace_catalog_during_a_tool_call(self):
        index=self.index()
        view=ToolReferenceIndex(index)
        entered=threading.Event(); release=threading.Event(); updated=threading.Event()
        original=index.page
        outputs=[]
        def reading(*args,**kwargs):
            result=original(*args,**kwargs)
            entered.set()
            self.assertTrue(release.wait(2))
            return result
        def replacing():
            with index._lock:
                index._pages=[]
                updated.set()
        with patch.object(index,'page',side_effect=reading):
            reader=threading.Thread(target=lambda:outputs.append(view.page('std437')))
            reader.start(); self.assertTrue(entered.wait(2))
            writer=threading.Thread(target=replacing)
            writer.start()
            try:
                self.assertFalse(updated.wait(.05))
            finally:
                release.set(); reader.join(2); writer.join(2)
        self.assertFalse(reader.is_alive())
        self.assertFalse(writer.is_alive())
        self.assertEqual(outputs[0]['page']['ref'],'v8std:std437')
        self.assertIn('[Стандарт](v8std:std437)',outputs[0]['page']['body_markdown'])

    def test_snapshot_truncation_flag_survives_whitespace_at_the_boundary(self):
        page={**fixture.page_fixture(),'body_markdown':('x'*900)+(' '*200)+'tail'}
        vectors=fixture.vector_fixtures()
        vectors[1]['text_sha256']=fixture.sha256(page['body_markdown'].encode())
        files=fixture.with_metadata(fixture.corpus_files(pages=[page],vectors=vectors))
        generation=build_generation(verify_archive(*fixture.snapshot_fixture(files=files)),max_snippet_chars=4000)
        class Current:
            def current(self):return generation
        index=SnapshotIndex(); index.coordinator=Current()
        page=ToolReferenceIndex(index,snapshot=True).page('v8std:std437',body_limit=1000)['page']
        self.assertTrue(page['body_truncated'])
        self.assertNotIn('tail',page['body_markdown'])

    def test_snapshot_call_uses_one_generation_and_keeps_source_hash(self):
        snapshot=verify_archive(*fixture.snapshot_fixture())
        generation=build_generation(snapshot,max_snippet_chars=4000)
        class Current:
            accesses=0
            def current(self):
                self.accesses+=1
                return generation
        index=SnapshotIndex()
        index.coordinator=Current()
        view=ToolReferenceIndex(index,snapshot=True)
        result=view.page('v8std:std437')
        self.assertEqual(index.coordinator.accesses,1)
        self.assertEqual(result['page']['ref'],'v8std:std437')
        self.assertIn('[Стандарт](v8std:std437)',result['page']['body_markdown'])
        self.assertEqual(generation.index.page('std437')['page']['body_markdown'],fixture.BODY)
        self.assertFalse(TOOL_REFERENCES.get())

if __name__=='__main__':unittest.main()
