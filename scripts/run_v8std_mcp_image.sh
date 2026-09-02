#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${V8STD_MCP_DATA_DIR:-/opt/v8std/data}"
PAGES_PATH="${V8STD_MCP_PAGES:-${DATA_DIR}/ai/pages.jsonl}"
VECTORS_PATH="${V8STD_MCP_VECTORS:-${DATA_DIR}/ai/search-vectors.jsonl}"
MCP_HOST="${V8STD_MCP_HOST:-0.0.0.0}"
MCP_PORT="${V8STD_MCP_PORT:-8766}"
MCP_PATH="${V8STD_MCP_PATH:-/mcp}"
MCP_CACHE_DIR="${V8STD_MCP_CACHE_DIR:-/tmp/v8std-mcp}"

for required_file in \
    "${PAGES_PATH}" \
    "${VECTORS_PATH}" \
    "${DATA_DIR}/llms.txt" \
    "${DATA_DIR}/llms-full.txt" \
    "/opt/v8std/retrieval-rules.yml"; do
    if [ ! -s "${required_file}" ]; then
        printf 'error: required MCP image artifact does not exist or is empty: %s\n' "${required_file}" >&2
        exit 1
    fi
done

exec python "${SCRIPT_DIR}/v8std_mcp_server.py" \
    --pages "${PAGES_PATH}" \
    --vectors "${VECTORS_PATH}" \
    --cache-dir "${MCP_CACHE_DIR}" \
    --host "${MCP_HOST}" \
    --port "${MCP_PORT}" \
    --mcp-path "${MCP_PATH}" \
    --allowed-host "127.0.0.1:*" \
    --allowed-host "localhost:*" \
    --allowed-host "v8std-mcp:*" \
    --allowed-origin "http://127.0.0.1:*" \
    --allowed-origin "http://localhost:*"
