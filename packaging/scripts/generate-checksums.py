#!/usr/bin/env python3
"""Generate SHA-256 checksums for release artifacts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

DEFAULT_PATTERNS = [
    "cameo-mcp-goose-python-standalone-*",
    "cameo-mcp-bridge-cameo-plugin-*.zip",
    "UPSTREAM_SOURCE.txt",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_dir", nargs="?", default="release")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    release_dir = Path(args.release_dir)
    artifacts: list[Path] = []
    for pattern in DEFAULT_PATTERNS:
        artifacts.extend(p for p in release_dir.glob(pattern) if p.is_file())
    artifacts = sorted(set(artifacts))

    output = Path(args.output) if args.output else release_dir / "checksums.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{sha256(path)}  {path.name}" for path in artifacts if path.resolve() != output.resolve()]
    output.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
