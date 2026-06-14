#!/usr/bin/env python3
"""Assemble a PyInstaller dist folder into the offline one-folder release layout."""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import stat
import tarfile
import zipfile
from pathlib import Path

VERSION = "2.3.5"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copytree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for child in src.iterdir():
        target = dst / child.name
        if child.is_dir():
            shutil.copytree(child, target, dirs_exist_ok=True)
        else:
            shutil.copy2(child, target)


def make_executable(path: Path) -> None:
    if os.name != "nt" and path.exists():
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def archive_bundle(bundle_root: Path, output_path: Path, archive_type: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if archive_type == "zip":
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(bundle_root.rglob("*")):
                zf.write(path, path.relative_to(bundle_root.parent))
    elif archive_type == "tar.gz":
        with tarfile.open(output_path, "w:gz") as tf:
            tf.add(bundle_root, arcname=bundle_root.name)
    else:
        raise ValueError(f"unsupported archive type: {archive_type}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", default="dist/cameo-mcp-bridge", help="PyInstaller dist folder")
    parser.add_argument("--out", default="release", help="Release output directory")
    parser.add_argument("--version", default=VERSION)
    parser.add_argument("--os", default=platform.system().lower().replace("darwin", "macos"))
    parser.add_argument("--arch", default=platform.machine().lower().replace("amd64", "x64").replace("x86_64", "x64"))
    parser.add_argument("--archive", choices=["zip", "tar.gz"], default=None)
    parser.add_argument(
        "--upstream-source-dir",
        default=os.environ.get("UPSTREAM_SOURCE_DIR") or os.environ.get("UPSTREAM_DIR"),
        help="Optional build-time upstream checkout whose LICENSE/source metadata should be included",
    )
    args = parser.parse_args()

    dist = Path(args.dist).resolve()
    if not dist.is_dir():
        raise SystemExit(f"Missing PyInstaller dist folder: {dist}")

    archive_type = args.archive or ("zip" if args.os == "windows" else "tar.gz")
    out_dir = Path(args.out).resolve()
    work_root = out_dir / "work" / f"cameo-mcp-goose-python-standalone-{args.version}-{args.os}-{args.arch}"
    if work_root.exists():
        shutil.rmtree(work_root)

    bundle_root = work_root / "cameo-mcp-bridge"
    bin_dir = bundle_root / "bin"
    runtime_dir = bundle_root / "runtime"
    bin_dir.mkdir(parents=True)
    runtime_dir.mkdir(parents=True)

    exe_name = "cameo-mcp-bridge.exe" if args.os == "windows" else "cameo-mcp-bridge"
    source_exe = dist / exe_name
    if not source_exe.exists() and args.os != "windows":
        source_exe = dist / "cameo-mcp-bridge"
    if not source_exe.exists():
        raise SystemExit(f"Missing PyInstaller executable in {dist}: {exe_name}")

    # Preserve PyInstaller's relative onedir layout. The spec uses
    # contents_directory="runtime", so the executable expects ../runtime when
    # moved into bin/.
    shutil.copy2(source_exe, bin_dir / exe_name)
    make_executable(bin_dir / exe_name)
    if (dist / "runtime").is_dir():
        copytree_contents(dist / "runtime", runtime_dir)
        for child in dist.iterdir():
            if child.name in {source_exe.name, "runtime"}:
                continue
            target = bundle_root / child.name
            if child.is_dir():
                shutil.copytree(child, target, dirs_exist_ok=True)
            else:
                shutil.copy2(child, target)
    else:
        # Compatibility with older PyInstaller specs that place support files
        # beside the executable.
        for child in dist.iterdir():
            if child.name == source_exe.name:
                continue
            target = runtime_dir / child.name
            if child.is_dir():
                shutil.copytree(child, target, dirs_exist_ok=True)
            else:
                shutil.copy2(child, target)

    # PyInstaller resolves its contents directory relative to the executable.
    # Keep the documented root-level runtime/ directory, and mirror/symlink the
    # actual PyInstaller support directories back under bin/ after moving the
    # executable there. Current PyInstaller defaults to _internal; older/custom
    # specs may use runtime.
    support_dirs = [child for child in runtime_dir.iterdir() if child.is_dir()]
    if args.os == "windows":
        for support_dir in support_dirs:
            bin_support = bin_dir / support_dir.name
            if not bin_support.exists():
                shutil.copytree(support_dir, bin_support, dirs_exist_ok=True)
    else:
        for support_dir in support_dirs:
            bin_support = bin_dir / support_dir.name
            if not bin_support.exists():
                bin_support.symlink_to(Path("..") / "runtime" / support_dir.name, target_is_directory=True)

    copytree_contents(Path("packaging/templates/install"), bundle_root / "install")
    copytree_contents(Path("packaging/templates/goose"), bundle_root / "goose")
    shutil.copy2("packaging/templates/README-OFFLINE.md", bundle_root / "README-OFFLINE.md")
    (bundle_root / "VERSION").write_text(args.version + "\n", encoding="utf-8")

    if args.upstream_source_dir:
        upstream_dir = Path(args.upstream_source_dir).resolve()
        if upstream_dir.exists():
            third_party_dir = bundle_root / "THIRD-PARTY"
            third_party_dir.mkdir(parents=True, exist_ok=True)
            upstream_license = upstream_dir / "LICENSE"
            if upstream_license.exists():
                shutil.copy2(upstream_license, third_party_dir / "cameo-mcp-bridge-LICENSE")
            metadata = []
            metadata.append("Build-time upstream source (not vendored in packaging repository)\n")
            metadata.append(f"Repository: https://github.com/ajhcs/cameo-mcp-bridge.git\n")
            metadata.append(f"Local source dir: {upstream_dir}\n")
            head_file = upstream_dir / ".git" / "HEAD"
            if head_file.exists():
                metadata.append(f"Git HEAD: {head_file.read_text(encoding='utf-8').strip()}\n")
            (third_party_dir / "cameo-mcp-bridge-SOURCE.txt").write_text("".join(metadata), encoding="utf-8")

    executable_checksum = sha256(bin_dir / exe_name)
    (bundle_root / "checksums.txt").write_text(
        f"{executable_checksum}  bin/{exe_name}\n",
        encoding="utf-8",
    )

    archive_name = f"cameo-mcp-goose-python-standalone-{args.version}-{args.os}-{args.arch}.{archive_type}"
    archive_path = out_dir / archive_name
    archive_bundle(bundle_root, archive_path, archive_type)
    print(archive_path)


if __name__ == "__main__":
    main()
