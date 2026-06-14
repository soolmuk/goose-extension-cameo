# Offline Goose Standalone Cameo MCP Bridge v2.3.5

This release adds offline one-folder Goose extension packaging for the existing Cameo MCP Python server and ships the Cameo Java plugin as a separate precompiled artifact.

## Artifacts

- `cameo-mcp-goose-python-standalone-2.3.5-windows-x64.zip`
- `cameo-mcp-goose-python-standalone-2.3.5-macos-arm64.tar.gz`
- `cameo-mcp-goose-python-standalone-2.3.5-macos-x64.tar.gz`
- `cameo-mcp-goose-python-standalone-2.3.5-linux-x64.tar.gz`
- `cameo-mcp-bridge-cameo-plugin-2.3.5.zip`
- `checksums.txt`

## Install Summary

1. Copy `com.claude.cameo.bridge/` from the Cameo plugin zip into the CATIA Magic/Cameo plugins directory.
2. Restart Cameo and verify `http://127.0.0.1:18740/api/v1/status`.
3. Unpack the OS-specific Goose standalone bundle.
4. Run `install/install-goose.sh` or `install\install-goose.ps1`.
5. Restart Goose or begin a new Goose session and run `cameo_status`.

## Offline Guarantee

Target machines do not need Python, venv creation, pip, uv, npm, cargo, Gradle, or internet access. Installer scripts only call bundled local files and update Goose config.

## Goose Config Backups

Each automatic config write creates a same-directory backup named `config.yaml.backup-YYYYMMDD-HHMMSS`.

## Compatibility

Use the `2.3.5` standalone MCP bundle with the `2.3.5` Cameo Java plugin. Exact plugin-version compatibility is required for normal operations.

## Checksum Verification

Verify downloaded artifacts with SHA-256 values in `checksums.txt` before installation.
