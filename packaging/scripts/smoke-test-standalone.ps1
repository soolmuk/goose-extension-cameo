param(
    [string]$BundleRoot = "cameo-mcp-bridge"
)
$ErrorActionPreference = "Stop"
$Exe = Join-Path $BundleRoot "bin\cameo-mcp-bridge.exe"
$Temp = New-Item -ItemType Directory -Path ([System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString()))
try {
    & $Exe --print-goose-config | Out-Null
    & $Exe --install-goose --config (Join-Path $Temp.FullName "config.yaml") | Out-Null
    if (-not (Test-Path (Join-Path $Temp.FullName "config.yaml"))) { throw "config.yaml was not created" }
    if (-not (Get-ChildItem $Temp.FullName -Filter "config.yaml.backup-*")) { throw "backup was not created" }
    & $Exe --uninstall-goose --config (Join-Path $Temp.FullName "config.yaml") | Out-Null
} finally {
    Remove-Item -Recurse -Force $Temp
}
