@echo off
setlocal

set "V8STD_MCP_IMAGE=v8std-mcp:latest"
if not "%~1"=="" set "V8STD_MCP_IMAGE=%~1"
set "V8STD_MCP_CONTAINER=v8std"

docker container inspect "%V8STD_MCP_CONTAINER%" >nul 2>&1
if not errorlevel 1 (
    echo Error: container "%V8STD_MCP_CONTAINER%" already exists.
    echo Remove or rename it before running this script again.
    pause
    exit /b 1
)

docker run --name "%V8STD_MCP_CONTAINER%" --restart unless-stopped -p 127.0.0.1:8766:8766 -d "%V8STD_MCP_IMAGE%" || goto :error

echo Container "%V8STD_MCP_CONTAINER%" started successfully.
pause
exit /b 0

:error
echo Failed to start the container.
pause
exit /b 1
