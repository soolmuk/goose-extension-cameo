"""Goose config helpers for the offline Cameo MCP Bridge bundle."""

from __future__ import annotations

import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

EXTENSION_ID = "cameo-bridge"
DISPLAY_NAME = "Cameo MCP Bridge"
DESCRIPTION = "Offline standalone Cameo MCP Bridge for CATIA Magic / Cameo Systems Modeler"
DEFAULT_PORT = "18740"
DEFAULT_TIMEOUT = "300"


def default_goose_config_path() -> Path:
    """Return Goose config path per goose-docs.ai config-files documentation."""

    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA is not set; pass --config explicitly")
        return Path(appdata) / "Block" / "goose" / "config" / "config.yaml"
    return Path.home() / ".config" / "goose" / "config.yaml"


def resolve_config_path(config_path: str | os.PathLike[str] | None = None) -> Path:
    """Resolve an explicit or platform-default Goose config path."""

    if config_path:
        return Path(config_path).expanduser().resolve()
    return default_goose_config_path()


def backup_config(config_path: Path) -> Path:
    """Create a same-directory timestamped backup before mutating config.

    If the config file does not exist yet, an empty backup marker is created.
    This keeps the installer's "every write creates a backup" policy simple and
    gives users an obvious pre-install restore point even for first-time setup.
    """

    config_path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = config_path.with_name(f"{config_path.name}.backup-{timestamp}")
        if not backup_path.exists():
            break
        time.sleep(0.1)

    if config_path.exists():
        shutil.copy2(config_path, backup_path)
    else:
        backup_path.write_text("", encoding="utf-8")
    return backup_path


def standalone_executable_path() -> Path:
    """Return the absolute command path Goose should launch."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve()
    return Path(sys.argv[0]).expanduser().resolve()


def _parse_timeout(timeout: str | int) -> int:
    try:
        value = int(timeout)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"timeout must be an integer number of seconds, got {timeout!r}") from exc
    if value <= 0:
        raise ValueError("timeout must be greater than zero")
    return value


def build_extension_entry(
    *,
    cmd: str | os.PathLike[str] | None = None,
    port: str = DEFAULT_PORT,
    timeout: str | int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Build the Goose stdio extension entry for cameo-bridge."""

    command = Path(cmd).expanduser().resolve() if cmd is not None else standalone_executable_path()
    return {
        "bundled": False,
        "display_name": DISPLAY_NAME,
        "enabled": True,
        "name": EXTENSION_ID,
        "timeout": _parse_timeout(timeout),
        "type": "stdio",
        "available_tools": [],
        "cmd": str(command),
        "args": [],
        "description": DESCRIPTION,
        "env_keys": [],
        "envs": {"CAMEO_BRIDGE_PORT": str(port)},
    }


def _load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists() or config_path.stat().st_size == 0:
        return {}
    try:
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Invalid Goose YAML config at {config_path}: {exc}") from exc
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise RuntimeError(f"Goose config root must be a mapping: {config_path}")
    return loaded


def _write_config(config_path: Path, data: dict[str, Any]) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
    config_path.write_text(serialized, encoding="utf-8")


def _extensions_mapping(data: dict[str, Any]) -> dict[str, Any]:
    extensions = data.get("extensions")
    if extensions is None:
        extensions = {}
        data["extensions"] = extensions
    if not isinstance(extensions, dict):
        raise RuntimeError("Goose config 'extensions' key must be a mapping")
    return extensions


def install_goose_extension(
    *,
    config_path: str | os.PathLike[str] | None = None,
    port: str = DEFAULT_PORT,
    timeout: str | int = DEFAULT_TIMEOUT,
) -> tuple[Path, Path]:
    """Install or update the cameo-bridge Goose stdio extension.

    Returns ``(config_path, backup_path)`` for scripts/tests. The function also
    prints human-readable status for end users running the bundled installer.
    """

    path = resolve_config_path(config_path)
    if not path.exists():
        print(f"Goose config does not exist; creating: {path}")
    data = _load_config(path)
    extensions = _extensions_mapping(data)
    extensions[EXTENSION_ID] = build_extension_entry(port=port, timeout=timeout)
    backup_path = backup_config(path)
    _write_config(path, data)
    print(f"Installed Goose extension '{EXTENSION_ID}' in {path}")
    print(f"Backup created: {backup_path}")
    return path, backup_path


def uninstall_goose_extension(
    *,
    config_path: str | os.PathLike[str] | None = None,
) -> tuple[Path, Path | None]:
    """Remove the cameo-bridge Goose extension if present."""

    path = resolve_config_path(config_path)
    if not path.exists():
        print(f"Goose config does not exist; nothing to uninstall: {path}")
        return path, None

    data = _load_config(path)
    extensions = data.get("extensions")
    if not isinstance(extensions, dict) or EXTENSION_ID not in extensions:
        print(f"Goose extension '{EXTENSION_ID}' is not installed in {path}")
        return path, None

    del extensions[EXTENSION_ID]
    if not extensions:
        data["extensions"] = {}
    backup_path = backup_config(path)
    _write_config(path, data)
    print(f"Removed Goose extension '{EXTENSION_ID}' from {path}")
    print(f"Backup created: {backup_path}")
    return path, backup_path


def print_goose_config_snippet(
    *,
    port: str = DEFAULT_PORT,
    timeout: str | int = DEFAULT_TIMEOUT,
) -> None:
    """Print a manual Goose YAML snippet matching the installer output."""

    snippet = {"extensions": {EXTENSION_ID: build_extension_entry(port=port, timeout=timeout)}}
    print(yaml.safe_dump(snippet, sort_keys=False, default_flow_style=False, allow_unicode=True), end="")
