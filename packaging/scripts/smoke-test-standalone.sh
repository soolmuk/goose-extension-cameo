#!/usr/bin/env bash
set -euo pipefail

BUNDLE_ROOT="${1:-cameo-mcp-bridge}"
EXE="$BUNDLE_ROOT/bin/cameo-mcp-bridge"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

if [ ! -x "$EXE" ]; then
  chmod +x "$EXE" || true
fi

"$EXE" --print-goose-config >/dev/null
"$EXE" --install-goose --config "$TMPDIR/config.yaml" >/dev/null
test -f "$TMPDIR/config.yaml"
ls "$TMPDIR"/config.yaml.backup-* >/dev/null
"$EXE" --uninstall-goose --config "$TMPDIR/config.yaml" >/dev/null
