#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

VERSION="${VERSION:-2.3.5}"
TARGET_OS="${TARGET_OS:-macos}"
TARGET_ARCH="${TARGET_ARCH:-arm64}"
ARCHIVE="${ARCHIVE:-tar.gz}"
UPSTREAM_DIR="${UPSTREAM_DIR:-.external/cameo-mcp-bridge}"
BUILD_PLUGIN="${BUILD_PLUGIN:-false}"
CAMEO_HOME="${CAMEO_HOME:-}"
JDK17_HOME_VALUE="${JDK17_HOME:-${JAVA17_HOME:-}}"

packaging/scripts/fetch-upstream-source.sh

MCP_SERVER_SOURCE="$UPSTREAM_DIR/mcp-server" \
  PYINSTALLER_TARGET_ARCH="${PYINSTALLER_TARGET_ARCH:-}" \
  packaging/scripts/build-standalone.sh

python3 packaging/scripts/assemble-standalone-bundle.py \
  --version "$VERSION" \
  --os "$TARGET_OS" \
  --arch "$TARGET_ARCH" \
  --archive "$ARCHIVE" \
  --upstream-source-dir "$UPSTREAM_DIR"

if [ "$BUILD_PLUGIN" = "true" ]; then
  if [ -z "$CAMEO_HOME" ]; then
    echo "BUILD_PLUGIN=true requires CAMEO_HOME=/path/to/CatiaMagic" >&2
    exit 2
  fi
  if [ -n "$JDK17_HOME_VALUE" ]; then
    (cd "$UPSTREAM_DIR/plugin" && JDK17_HOME="$JDK17_HOME_VALUE" ./gradlew assemblePlugin -PcameoHome="$CAMEO_HOME" -Pjdk17Home="$JDK17_HOME_VALUE")
  else
    (cd "$UPSTREAM_DIR/plugin" && ./gradlew assemblePlugin -PcameoHome="$CAMEO_HOME")
  fi
  PLUGIN_DIST="$UPSTREAM_DIR/plugin/build/plugin-dist/com.claude.cameo.bridge" \
    UPSTREAM_SOURCE_DIR="$UPSTREAM_DIR" \
    VERSION="$VERSION" \
    packaging/scripts/package-cameo-plugin.sh
fi

python3 packaging/scripts/generate-checksums.py release
