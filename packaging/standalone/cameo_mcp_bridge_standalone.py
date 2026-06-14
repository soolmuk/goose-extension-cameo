"""Standalone PyInstaller entrypoint for Cameo MCP Bridge."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _add_development_paths() -> None:
    """Allow running this file directly from a source checkout.

    PyInstaller builds receive import paths from the spec file. In a checkout,
    ``python3 packaging/standalone/cameo_mcp_bridge_standalone.py`` would not
    otherwise see ``mcp-server/cameo_mcp`` because Python starts with only this
    script's directory on ``sys.path``.
    """

    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    candidates = [repo_root / "mcp-server", repo_root / "packaging" / "standalone"]
    for candidate in candidates:
        if candidate.exists():
            candidate_text = str(candidate)
            if candidate_text not in sys.path:
                sys.path.insert(0, candidate_text)


_add_development_paths()

from cameo_mcp.server import main as run_mcp_server  # noqa: E402
from cameo_mcp_standalone.goose_config import (  # noqa: E402
    install_goose_extension,
    print_goose_config_snippet,
    uninstall_goose_extension,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cameo MCP Bridge standalone bundle")
    parser.add_argument("--install-goose", action="store_true")
    parser.add_argument("--uninstall-goose", action="store_true")
    parser.add_argument("--print-goose-config", action="store_true")
    parser.add_argument("--config", default=None, help="Explicit Goose config.yaml path")
    parser.add_argument("--port", default="18740", help="Cameo bridge port")
    parser.add_argument("--timeout", default="300", help="Goose extension timeout in seconds")
    args = parser.parse_args()

    selected_modes = sum(
        bool(value)
        for value in (args.install_goose, args.uninstall_goose, args.print_goose_config)
    )
    if selected_modes > 1:
        parser.error("choose only one of --install-goose, --uninstall-goose, or --print-goose-config")

    if args.install_goose:
        install_goose_extension(config_path=args.config, port=args.port, timeout=args.timeout)
        return
    if args.uninstall_goose:
        uninstall_goose_extension(config_path=args.config)
        return
    if args.print_goose_config:
        print_goose_config_snippet(port=args.port, timeout=args.timeout)
        return

    run_mcp_server()


if __name__ == "__main__":
    main()
