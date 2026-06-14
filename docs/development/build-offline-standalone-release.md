# Build Offline Standalone Release

Release build machines may use the internet to download build dependencies. Target install machines must not.

This repository contains only standalone packaging/release tooling. It does **not** vendor the MCP server source or the Java Cameo plugin source. Provide compatible private/prebuilt inputs during the release build.

## One-command Build From Upstream Source

To use the upstream repository as a build-time input without vendoring it here:

```bash
TARGET_OS=macos TARGET_ARCH=arm64 ARCHIVE=tar.gz \
  packaging/scripts/build-release-from-upstream.sh
```

This clones or updates `https://github.com/ajhcs/cameo-mcp-bridge.git` under `.external/cameo-mcp-bridge`, which is ignored by git. The fetched source is used only on the release build machine.

Override the upstream ref when needed:

```bash
UPSTREAM_REF=<commit-or-tag> \
TARGET_OS=macos TARGET_ARCH=arm64 ARCHIVE=tar.gz \
  packaging/scripts/build-release-from-upstream.sh
```

To also build and package the Java Cameo plugin, provide a local Cameo install:

```bash
BUILD_PLUGIN=true \
CAMEO_HOME=/path/to/CatiaMagic \
JDK17_HOME=/path/to/jdk-17 \
TARGET_OS=macos TARGET_ARCH=arm64 ARCHIVE=tar.gz \
  packaging/scripts/build-release-from-upstream.sh
```


## Python Standalone Bundle

Build separately on each target OS/architecture. Provide one of the following inputs:

- `MCP_SERVER_SOURCE=/path/to/compatible/mcp-server` for a local Python package/source directory.
- `MCP_PACKAGE_SPEC='cameo-mcp-server @ file:///path/to/cameo_mcp_server-2.3.5-py3-none-any.whl'` for a prebuilt local wheel/package spec.

macOS/Linux example:

```bash
MCP_SERVER_SOURCE=/path/to/compatible/mcp-server \
  packaging/scripts/build-standalone.sh
python3 packaging/scripts/assemble-standalone-bundle.py --os linux --arch x64 --archive tar.gz
```

macOS target-architecture examples:

```bash
PYINSTALLER_TARGET_ARCH=arm64 MCP_SERVER_SOURCE=/path/to/compatible/mcp-server \
  packaging/scripts/build-standalone.sh
python3 packaging/scripts/assemble-standalone-bundle.py --os macos --arch arm64 --archive tar.gz

PYINSTALLER_TARGET_ARCH=x86_64 MCP_SERVER_SOURCE=/path/to/compatible/mcp-server \
  packaging/scripts/build-standalone.sh
python3 packaging/scripts/assemble-standalone-bundle.py --os macos --arch x64 --archive tar.gz
```

Windows example:

```powershell
$env:MCP_SERVER_SOURCE = 'C:\path\to\compatible\mcp-server'
packaging\scripts\build-standalone.ps1
python packaging\scripts\assemble-standalone-bundle.py --os windows --arch x64 --archive zip
```

Expected PyInstaller output:

- Windows: `dist/cameo-mcp-bridge/cameo-mcp-bridge.exe`
- macOS/Linux: `dist/cameo-mcp-bridge/cameo-mcp-bridge`

## Cameo Plugin Zip

This repository does not vendor Java plugin source. Build or obtain the precompiled Cameo plugin artifact outside this repository, then point `PLUGIN_DIST` at the copy-ready `com.claude.cameo.bridge` folder:

```bash
PLUGIN_DIST=/path/to/com.claude.cameo.bridge \
  packaging/scripts/package-cameo-plugin.sh
```

The zip must contain:

- `com.claude.cameo.bridge/plugin.xml`
- `com.claude.cameo.bridge/cameo-mcp-bridge-2.3.5.jar`
- `com.claude.cameo.bridge/README-INSTALL-CAMEO-PLUGIN.md`

## Checksums

```bash
python3 packaging/scripts/generate-checksums.py release
```

## Validation

Run packaging helper checks:

```bash
python3 -m py_compile \
  packaging/standalone/cameo_mcp_bridge_standalone.py \
  packaging/standalone/cameo_mcp_standalone/goose_config.py \
  packaging/scripts/assemble-standalone-bundle.py \
  packaging/scripts/generate-checksums.py

bash -n \
  packaging/scripts/build-standalone.sh \
  packaging/scripts/package-cameo-plugin.sh \
  packaging/scripts/smoke-test-standalone.sh \
  packaging/scripts/create-github-release.sh \
  packaging/templates/install/install-goose.sh \
  packaging/templates/install/uninstall-goose.sh
```

Run packaged smoke tests on every target OS/arch after real artifacts are built:

```bash
packaging/scripts/smoke-test-standalone.sh /path/to/cameo-mcp-bridge
```

Then follow `docs/development/offline-standalone-validation.md` in clean no-network machines.

## Publish

Only after validation, commit, tag, push, and create a GitHub Release using `packaging/scripts/create-github-release.sh` or the GitHub UI.
