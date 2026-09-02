@echo off
setlocal

set "V8STD_MCP_IMAGE=v8std-mcp:latest"

pushd "%~dp0" || goto :error
set "V8STD_MCP_PUSHD=1"

docker build --no-cache --file Dockerfile.mcp --tag "%V8STD_MCP_IMAGE%" . || goto :error

popd
set "V8STD_MCP_PUSHD="
echo Built %V8STD_MCP_IMAGE%
pause
exit /b 0

:error
if defined V8STD_MCP_PUSHD popd
echo Failed to build %V8STD_MCP_IMAGE%.
pause
exit /b 1
