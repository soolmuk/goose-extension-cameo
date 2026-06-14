param(
    [switch]$WhatIf
)
$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BundleRoot = Resolve-Path (Join-Path $ScriptRoot "..")
$Exe = Join-Path $BundleRoot "bin\cameo-mcp-bridge.exe"

if (-not (Test-Path $Exe)) {
    throw "Cannot find standalone executable: $Exe"
}

if ($WhatIf) {
    Write-Host "Would run: $Exe --uninstall-goose"
    exit 0
}

& $Exe --uninstall-goose
if ($LASTEXITCODE -ne 0) {
    throw "Goose unregistration failed."
}
