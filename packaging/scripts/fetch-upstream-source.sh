#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

UPSTREAM_REPO="${UPSTREAM_REPO:-https://github.com/ajhcs/cameo-mcp-bridge.git}"
UPSTREAM_REF="${UPSTREAM_REF:-master}"
UPSTREAM_DIR="${UPSTREAM_DIR:-.external/cameo-mcp-bridge}"

if [ -d "$UPSTREAM_DIR/.git" ]; then
  echo "Updating upstream source in $UPSTREAM_DIR"
  git -C "$UPSTREAM_DIR" fetch --tags origin
else
  echo "Cloning upstream source into $UPSTREAM_DIR"
  rm -rf "$UPSTREAM_DIR"
  mkdir -p "$(dirname "$UPSTREAM_DIR")"
  git clone "$UPSTREAM_REPO" "$UPSTREAM_DIR"
  git -C "$UPSTREAM_DIR" fetch --tags origin
fi

git -C "$UPSTREAM_DIR" checkout "$UPSTREAM_REF"
UPSTREAM_COMMIT="$(git -C "$UPSTREAM_DIR" rev-parse HEAD)"

mkdir -p release
cat > release/UPSTREAM_SOURCE.txt <<EOF
Repository: $UPSTREAM_REPO
Ref: $UPSTREAM_REF
Commit: $UPSTREAM_COMMIT
Local source dir: $UPSTREAM_DIR

Source is fetched at build time and is not vendored in this repository.
EOF

echo "UPSTREAM_DIR=$UPSTREAM_DIR"
echo "UPSTREAM_COMMIT=$UPSTREAM_COMMIT"
