#!/usr/bin/env bash
set -euo pipefail

VERSION="${VERSION:-2.3.5}"
PLUGIN_DIST="${PLUGIN_DIST:-plugin/build/plugin-dist/com.claude.cameo.bridge}"
RELEASE_DIR="${RELEASE_DIR:-release}"
OUT="$RELEASE_DIR/cameo-mcp-bridge-cameo-plugin-$VERSION"
ZIP="$RELEASE_DIR/cameo-mcp-bridge-cameo-plugin-$VERSION.zip"

if [ ! -d "$PLUGIN_DIST" ]; then
  echo "Missing $PLUGIN_DIST. Run plugin/gradlew assemblePlugin on the release build machine first." >&2
  exit 1
fi

rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT"
cp -R "$PLUGIN_DIST" "$OUT/com.claude.cameo.bridge"
cp "packaging/templates/README-INSTALL-CAMEO-PLUGIN.md" "$OUT/com.claude.cameo.bridge/README-INSTALL-CAMEO-PLUGIN.md"

if [ ! -f "$OUT/com.claude.cameo.bridge/plugin.xml" ]; then
  echo "Packaged plugin is missing plugin.xml" >&2
  exit 1
fi
if [ ! -f "$OUT/com.claude.cameo.bridge/cameo-mcp-bridge-$VERSION.jar" ]; then
  echo "Packaged plugin is missing cameo-mcp-bridge-$VERSION.jar" >&2
  exit 1
fi

( cd "$OUT" && zip -qr "../$(basename "$ZIP")" com.claude.cameo.bridge )
echo "$ZIP"
