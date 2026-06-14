#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

MCP_SERVER_SOURCE="${MCP_SERVER_SOURCE:-}"
MCP_PACKAGE_SPEC="${MCP_PACKAGE_SPEC:-}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ -z "$MCP_SERVER_SOURCE" ] && [ -z "$MCP_PACKAGE_SPEC" ]; then
  cat >&2 <<'EOF'
Missing MCP server input.

This repository does not vendor upstream Cameo MCP source. Provide one of:
  MCP_SERVER_SOURCE=/absolute/path/to/compatible/mcp-server
  MCP_PACKAGE_SPEC='cameo-mcp-server @ file:///absolute/path/to/package.whl'

Example:
  MCP_SERVER_SOURCE=/path/to/your/private/mcp-server packaging/scripts/build-standalone.sh
EOF
  exit 2
fi

"$PYTHON_BIN" -m venv .build-venv
# shellcheck disable=SC1091
. .build-venv/bin/activate
python -m pip install --upgrade pip
if [ -n "$MCP_SERVER_SOURCE" ]; then
  python -m pip install "$MCP_SERVER_SOURCE"
else
  python -m pip install "$MCP_PACKAGE_SPEC"
fi
python -m pip install pyinstaller PyYAML
python -m PyInstaller ./packaging/pyinstaller/cameo-mcp-bridge.spec --noconfirm
