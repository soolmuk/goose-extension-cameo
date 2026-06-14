param(
    [switch]$WhatIf
)
$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BundleRoot = Resolve-Path (Join-Path $ScriptRoot "..")
$Exe = Join-Path $BundleRoot "bin\cameo-mcp-bridge.exe"
$Port = if ($env:CAMEO_BRIDGE_PORT) { $env:CAMEO_BRIDGE_PORT } else { "18740" }
$Timeout = if ($env:GOOSE_CAMEO_TIMEOUT) { $env:GOOSE_CAMEO_TIMEOUT } else { "300" }

if (-not (Test-Path $Exe)) {
    throw "Cannot find standalone executable: $Exe"
}

if ($WhatIf) {
    Write-Host "Would run: $Exe --install-goose --port $Port --timeout $Timeout"
    exit 0
}

& $Exe --install-goose --port $Port --timeout $Timeout
if ($LASTEXITCODE -ne 0) {
    throw "Goose registration failed. Run '$Exe --print-goose-config' for manual configuration."
}
