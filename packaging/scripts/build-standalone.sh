#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

python3 -m venv .build-venv
# shellcheck disable=SC1091
. .build-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./mcp-server
python -m pip install pyinstaller PyYAML
pyinstaller ./packaging/pyinstaller/cameo-mcp-bridge.spec --noconfirm
