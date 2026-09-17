"""Run inside the standalone fork image, with no volumes and --network none."""
import collections
import json
import time
import urllib.request
from pathlib import Path


def main():
    rows = [json.loads(line) for line in Path('/opt/v8std/data/ai/pages.jsonl').read_text().splitlines()]
    counts = collections.Counter(row['collection'] for row in rows)
    assert counts['corporate'] > 0 and counts['yaxunit'] > 0, counts
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
    for collection in ('corporate', 'yaxunit'):
        page = next(row for row in rows if row['collection'] == collection and row['body_markdown'])
        result = rpc('tools/call', {'name': 'v8std_get_page', 'arguments': {'id_or_alias_or_url': page['id']}})
        data = result['structuredContent']
        assert data['found'] and data['page']['collection'] == collection, data
        assert data['page']['body_markdown'], data
        result = rpc('tools/call', {'name': 'v8std_search',
                     'arguments': {'query': page['id'], 'collections': [collection]}})['structuredContent']
        assert result['results'] and all(row['collection'] == collection for row in result['results']), result
    print(json.dumps({'collections': counts, 'tools': len(tools), 'offline_http': 'ok'}))


if __name__ == '__main__':
    main()
