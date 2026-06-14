$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptRoot "..\..")
Set-Location $RepoRoot

python -m venv .build-venv
. .build-venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .\mcp-server
python -m pip install pyinstaller PyYAML
pyinstaller .\packaging\pyinstaller\cameo-mcp-bridge.spec --noconfirm
