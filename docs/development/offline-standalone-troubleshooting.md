# Offline Standalone Troubleshooting

## Goose Config Path Not Found

The installer uses Goose's documented paths:

- macOS/Linux: `~/.config/goose/config.yaml`
- Windows: `%APPDATA%\Block\goose\config\config.yaml`

Pass `--config /path/to/config.yaml` directly to `bin/cameo-mcp-bridge` if your installation uses a custom path.

## Invalid Goose YAML

If install reports invalid YAML, restore the newest backup or fix the YAML manually. Backups are named:

```text
config.yaml.backup-YYYYMMDD-HHMMSS
```

## Restore From Backup

1. Close Goose.
2. Rename current `config.yaml` to keep a copy.
3. Copy the selected `config.yaml.backup-*` to `config.yaml`.
4. Restart Goose.

## macOS Quarantine / Codesign

Unsigned PyInstaller artifacts may require Gatekeeper approval. Document your organization's approved quarantine removal or signing workflow before distributing internally.

## Linux glibc Baseline

PyInstaller bundles are not fully portable across all Linux distributions. Build on the oldest supported baseline distribution and validate there.

## Windows Antivirus False Positive

PyInstaller executables can trigger reputation-based antivirus warnings. Verify SHA-256 checksums and, for broad distribution, code-sign the executable.

## Java Plugin Not Loaded

Check that the full folder exists:

```text
<CAMEO_HOME>/plugins/com.claude.cameo.bridge/plugin.xml
<CAMEO_HOME>/plugins/com.claude.cameo.bridge/cameo-mcp-bridge-2.3.5.jar
```

Restart Cameo after copying. Confirm `/api/v1/status` responds.

## Port Mismatch

The Java plugin defaults to `-Dcameo.mcp.port=18740`. The Goose extension sets `CAMEO_BRIDGE_PORT=18740` by default. If you change one, change the other.

## Version Mismatch

The standalone MCP bundle and Java plugin must both be version `2.3.5`. Mismatch can make status work while other tools fail compatibility checks.

## YAML Formatting

The offline installer uses PyYAML inside the bundled executable. It preserves Goose config keys and extension mappings, but YAML formatting/comments may be normalized when the file is rewritten. Use the timestamped backup if you need to recover the exact previous text formatting.
