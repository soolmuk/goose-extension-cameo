#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUNDLE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXE="$BUNDLE_ROOT/bin/cameo-mcp-bridge"

if [ ! -x "$EXE" ]; then
  chmod +x "$EXE" || true
fi
if [ ! -x "$EXE" ]; then
  echo "Cannot execute standalone binary: $EXE" >&2
  exit 1
fi

"$EXE" --uninstall-goose
