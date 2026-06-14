# Offline Goose Standalone Cameo MCP Bridge v2.3.5 macOS Preview

This pre-release provides offline one-folder Goose standalone bundles built from `https://github.com/ajhcs/cameo-mcp-bridge.git` as a build-time upstream input, without vendoring upstream source in this repository.

## Included artifacts

- `cameo-mcp-goose-python-standalone-2.3.5-macos-arm64.tar.gz`
- `cameo-mcp-goose-python-standalone-2.3.5-macos-x64.tar.gz`
- `checksums.txt`
- `UPSTREAM_SOURCE.txt`

## Not included yet

These artifacts still require target builders or additional compatibility work and are intentionally not part of this preview:

- Windows x64 standalone bundle
- Linux x64 standalone bundle
- Cameo Java plugin zip

The Cameo plugin build from the upstream source was attempted against the local CATIA Magic / Cameo 2026 installation, but that install's Java API/classpath differs from the upstream Gradle expectations and newer API signatures no longer match several presentation/diagram methods.

## Build provenance

The upstream source was fetched at build time only. See `UPSTREAM_SOURCE.txt` for the exact upstream repository/ref/commit used.

## Install summary

1. Install a compatible Cameo Java plugin separately.
2. Restart Cameo and verify `http://127.0.0.1:18740/api/v1/status`.
3. Unpack the macOS Goose standalone bundle for your CPU architecture.
4. Run `install/install-goose.sh`.
5. Restart Goose or begin a new Goose session and run `cameo_status`.

## Offline guarantee

Target machines do not need Python, venv creation, pip, uv, npm, cargo, Gradle, or internet access. Installer scripts only call bundled local files and update Goose config.

## Goose config backups

Each automatic config write creates a same-directory backup named `config.yaml.backup-YYYYMMDD-HHMMSS`.

## Checksum verification

Verify downloaded artifacts with SHA-256 values in `checksums.txt` before installation.
