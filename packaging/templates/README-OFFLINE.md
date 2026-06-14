# Offline Goose Standalone Cameo MCP Bridge

This bundle runs the Cameo MCP Python server as a Goose Standard IO extension without requiring Python, a virtual environment, pip, npm, cargo, Gradle, or internet access on the target machine.

## What Is Included

```text
cameo-mcp-bridge/
  bin/                 # standalone executable Goose launches
  runtime/             # bundled runtime/dependency files from PyInstaller
  goose/               # manual Goose config template
  install/             # offline install/uninstall scripts
  README-OFFLINE.md
  VERSION
  checksums.txt
```

The Cameo Java plugin is distributed separately as `cameo-mcp-bridge-cameo-plugin-2.3.5.zip`.

## Install Order

1. Install the separate Cameo Java plugin zip into CATIA Magic / Cameo.
2. Restart Cameo and open a project.
3. Unpack this OS-specific Goose standalone bundle somewhere permanent.
4. Run the Goose installer for your OS:
   - Windows PowerShell: `install\install-goose.ps1`
   - macOS/Linux shell: `install/install-goose.sh`
5. Restart Goose or start a new Goose session.
6. Ask Goose to run `cameo_status` and `cameo_get_capabilities`.

## Goose Config Paths

The installer updates Goose's documented config path:

- macOS/Linux: `~/.config/goose/config.yaml`
- Windows: `%APPDATA%\Block\goose\config\config.yaml`

The installer uses PyYAML for config edits. It preserves config data, but YAML formatting/comments may be normalized; restore from the timestamped backup if exact previous formatting is required.

Every write creates a same-folder backup named:

```text
config.yaml.backup-YYYYMMDD-HHMMSS
```

## Manual Config Snippet

If automatic installation fails, run:

```bash
bin/cameo-mcp-bridge --print-goose-config
```

Then merge the printed `extensions.cameo-bridge` entry into Goose `config.yaml`. A template is also available at `goose/config.template.yaml`.

## Version Compatibility

The standalone MCP bundle version must match the Cameo Java plugin version. For this release both must be `2.3.5`. If versions do not match, status may work but non-status operations can be refused by the compatibility handshake.

## Offline Guarantee

Target installation scripts do not run `pip install`, `git clone`, `curl`, `wget`, `npm`, `cargo`, or Gradle. Dependency downloads are only needed on release build machines before artifacts are assembled.
