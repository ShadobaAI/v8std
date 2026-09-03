@echo off
setlocal

set "V8STD_MCP_IMAGE=v8std-mcp:latest"
if not defined V8STD_MCP_DOCKER_USER for /f "usebackq delims=" %%U in (`powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\get_docker_hub_username.ps1"`) do set "V8STD_MCP_DOCKER_USER=%%U"
if not defined V8STD_MCP_DOCKER_USER goto :docker_login_required
set "V8STD_MCP_PUSH_IMAGE=%V8STD_MCP_DOCKER_USER%/v8std-mcp:latest"

pushd "%~dp0" || goto :error
set "V8STD_MCP_PUSHD=1"

docker build --no-cache --file Dockerfile.mcp --tag "%V8STD_MCP_PUSH_IMAGE%" --tag "%V8STD_MCP_IMAGE%" . || goto :error

popd
set "V8STD_MCP_PUSHD="
echo Built %V8STD_MCP_IMAGE% and %V8STD_MCP_PUSH_IMAGE%
pause
exit /b 0

:docker_login_required
echo Docker Hub login was not found. Run docker login and try again.
echo You can also set V8STD_MCP_DOCKER_USER explicitly.
pause
exit /b 1

:error
if defined V8STD_MCP_PUSHD popd
echo Failed to build %V8STD_MCP_IMAGE%.
pause
exit /b 1
