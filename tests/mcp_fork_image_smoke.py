"""Run inside the standalone fork image, with no volumes and --network none."""
import collections
import json
import hashlib
import time
import urllib.request
from pathlib import Path


def main():
    manifest = json.loads(Path('/opt/v8std/data/yaxunit-manifest.json').read_text())
    license_text = Path('/opt/v8std/LICENSES/yaxunit-Apache-2.0.txt').read_bytes()
    assert hashlib.sha256(license_text).hexdigest() == manifest['license_sha256']
    rows = [json.loads(line) for line in Path('/opt/v8std/data/ai/pages.jsonl').read_text().splitlines()]
    counts = collections.Counter(row['collection'] for row in rows)
    for collection in ('corporate', 'yaxunit', 'vanessa'):
        assert counts[collection] > 0, counts
    assert {'std800', 'std801', 'std802'} <= {row['id'] for row in rows}
    for attempt in range(60):
        try:
            urllib.request.urlopen('http://127.0.0.1:8766/healthz', timeout=2).close()
            break
        except OSError:
            if attempt == 59:
                raise
            time.sleep(1)

    def rpc(method, params):
        request = urllib.request.Request('http://127.0.0.1:8766/mcp',
            data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode(),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'})
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.load(response)
        assert 'error' not in payload, payload
        result = payload['result']
        assert not result.get('isError'), result
        return result

    rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                       'clientInfo': {'name': 'fork-image-smoke', 'version': '1'}})
    tools = rpc('tools/list', {})['tools']
    assert len(tools) == 11, tools
    search = next(tool for tool in tools if tool['name'] == 'v8std_search')
    assert {'collections', 'cursor'} <= search['inputSchema']['properties'].keys()
    for collection in ('corporate', 'yaxunit', 'vanessa'):
        page = next(row for row in rows if row['collection'] == collection and row['body_markdown'])
        result = rpc('tools/call', {'name': 'v8std_get_page', 'arguments': {'id_or_alias_or_url': page['id']}})
        data = result['structuredContent']
        assert data['found'] and data['page']['collection'] == collection, data
        assert data['page']['body_markdown'], data
        assert data['page']['ref'] == 'v8std:' + page['id'], data
        assert 'url' not in data['page'], data
        result = rpc('tools/call', {'name': 'v8std_search',
                     'arguments': {'query': page['id'], 'collections': [collection]}})['structuredContent']
        assert result['results'] and all(row['collection'] == collection for row in result['results']), result
    first = rpc('tools/call', {'name': 'v8std_search', 'arguments': {
        'query': 'модуль', 'mode': 'bm25', 'limit': 1, 'collections': ['v8std']}})['structuredContent']
    assert first['next_cursor'], first
    second = rpc('tools/call', {'name': 'v8std_search', 'arguments': {
        'query': 'модуль', 'mode': 'bm25', 'limit': 1, 'collections': ['v8std'],
        'cursor': first['next_cursor']}})['structuredContent']
    assert first['results'][0]['id'] != second['results'][0]['id'], (first, second)
    empty = rpc('tools/call', {'name': 'v8std_search', 'arguments': {
        'query': 'zxqvplmnonexistent987654'}})['structuredContent']
    assert empty['results'] == [] and empty['total'] == 0, empty
    print(json.dumps({'collections': counts, 'tools': len(tools), 'offline_http': 'ok'}))


if __name__ == '__main__':
    main()
