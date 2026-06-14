#!/usr/bin/env bash
set -euo pipefail

TAG="${1:-v2.3.5-goose-offline.1}"
REPO="${GITHUB_REPOSITORY:-soolmuk/goose-extension-cameo}"
RELEASE_DIR="${RELEASE_DIR:-release}"
NOTES_FILE="${NOTES_FILE:-release/RELEASE_NOTES.md}"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI 'gh' is not installed. Create the release manually using artifacts in $RELEASE_DIR." >&2
  exit 1
fi

gh auth status >/dev/null

artifacts=()
while IFS= read -r -d '' file; do
  artifacts+=("$file")
done < <(find "$RELEASE_DIR" -maxdepth 1 -type f \( \
  -name 'cameo-mcp-goose-python-standalone-*.zip' -o \
  -name 'cameo-mcp-goose-python-standalone-*.tar.gz' -o \
  -name 'cameo-mcp-bridge-cameo-plugin-*.zip' -o \
  -name 'checksums.txt' -o \
  -name 'UPSTREAM_SOURCE.txt' \
\) -print0 | sort -z)

if [ "${#artifacts[@]}" -eq 0 ]; then
  echo "No release artifacts found in $RELEASE_DIR." >&2
  exit 1
fi
if [ ! -f "$NOTES_FILE" ]; then
  echo "Missing release notes file: $NOTES_FILE" >&2
  exit 1
fi

release_flags=()
if [ "${PRERELEASE:-false}" = "true" ]; then
  release_flags+=(--prerelease)
fi

gh release create "$TAG" \
  "${artifacts[@]}" \
  --repo "$REPO" \
  --title "Offline Goose Standalone Cameo MCP Bridge ${TAG}" \
  --notes-file "$NOTES_FILE" \
  "${release_flags[@]}"
