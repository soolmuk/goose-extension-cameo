# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller one-folder spec for the offline Cameo MCP Bridge bundle."""

from pathlib import Path
import os

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None
REPO_ROOT = Path(SPECPATH).parents[1]
MCP_SERVER_SOURCE = os.environ.get("MCP_SERVER_SOURCE")
PATHEX = [str(REPO_ROOT / "packaging" / "standalone")]
if MCP_SERVER_SOURCE:
    PATHEX.insert(0, str(Path(MCP_SERVER_SOURCE).resolve()))

hiddenimports = [
    "mcp.server.fastmcp",
    "cameo_mcp.server",
    "cameo_mcp.client",
    "cameo_mcp.verification",
    "cameo_mcp.auto_remediation",
    "cameo_mcp.proofing",
    "cameo_mcp.semantic_validation",
    "cameo_mcp.state_machine_semantics",
    "cameo_mcp.methodology_workflows",
    "cameo_mcp.methodology.registry",
    "cameo_mcp.methodology.runtime",
    "cameo_mcp.methodology.service",
    "cameo_mcp_standalone.goose_config",
]
hiddenimports += collect_submodules("PIL")
hiddenimports += collect_submodules("pptx")
hiddenimports += collect_submodules("yaml")

a = Analysis(
    [str(REPO_ROOT / "packaging" / "standalone" / "cameo_mcp_bridge_standalone.py")],
    pathex=PATHEX,
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="cameo-mcp-bridge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=os.environ.get("PYINSTALLER_TARGET_ARCH"),
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="cameo-mcp-bridge",
    contents_directory="runtime",
)
