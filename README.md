# goose-extension-cameo

Offline standalone packaging and release tooling for a Goose-compatible Cameo MCP extension.

This repository intentionally does **not** include source code imported from `https://github.com/ajhcs/cameo-mcp-bridge.git`.

## What remains here

- Standalone launcher/config helper code under `packaging/standalone/`
- PyInstaller/build/release helper scripts under `packaging/`
- Offline Goose install/uninstall templates
- Release manifest/templates and release notes
- Offline standalone build/install/validation documentation

## What is not included

- The upstream Python MCP server source
- The upstream Java Cameo plugin source
- Upstream tests, plans, changelog, or project documentation

The standalone packaging scripts assume that a compatible MCP server package and Cameo plugin artifact are provided by the release/build process, but those upstream sources are not vendored in this repository.
