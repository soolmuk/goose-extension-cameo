$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptRoot "..\..")
Set-Location $RepoRoot

$PythonBin = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { "python" }
$McpServerSource = $env:MCP_SERVER_SOURCE
$McpPackageSpec = $env:MCP_PACKAGE_SPEC

if (-not $McpServerSource -and -not $McpPackageSpec) {
    throw @"
Missing MCP server input.

This repository does not vendor upstream Cameo MCP source. Provide one of:
  `$env:MCP_SERVER_SOURCE = 'C:\path\to\compatible\mcp-server'
  `$env:MCP_PACKAGE_SPEC = 'cameo-mcp-server @ file:///C:/path/to/package.whl'
"@
}

& $PythonBin -m venv .build-venv
. .build-venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
if ($McpServerSource) {
    python -m pip install $McpServerSource
} else {
    python -m pip install $McpPackageSpec
}
python -m pip install pyinstaller PyYAML
python -m PyInstaller .\packaging\pyinstaller\cameo-mcp-bridge.spec --noconfirm
