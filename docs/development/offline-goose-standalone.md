# Offline Goose Standalone Installation

The offline Goose standalone package lets Goose launch the Cameo MCP server as a Standard IO extension without requiring Python or internet access on the target machine.

## Choose Artifacts

Download or transfer both:

1. One OS-specific Goose standalone bundle.
2. `cameo-mcp-bridge-cameo-plugin-2.3.5.zip`.

## Install Cameo Plugin

1. Close CATIA Magic / Cameo.
2. Copy `com.claude.cameo.bridge/` into `<CAMEO_HOME>/plugins/`.
3. Restart Cameo and open a project.
4. Verify `http://127.0.0.1:18740/api/v1/status`.

## Install Goose Extension

Unpack the Goose bundle somewhere permanent, then run:

```bash
cameo-mcp-bridge/install/install-goose.sh
```

Windows:

```powershell
cameo-mcp-bridge\install\install-goose.ps1
```

The installer updates:

- macOS/Linux: `~/.config/goose/config.yaml`
- Windows: `%APPDATA%\Block\goose\config\config.yaml`

Before each write it creates `config.yaml.backup-YYYYMMDD-HHMMSS` in the same directory.

## Manual Goose YAML

If automatic install fails:

```bash
cameo-mcp-bridge/bin/cameo-mcp-bridge --print-goose-config
```

Merge the output into Goose `config.yaml`. Replace `cmd` with the absolute path to your unpacked executable if needed.

## Verify In Goose

Start a new Goose session and ask for:

- `cameo_status`
- `cameo_get_capabilities`

`compatibility.clientCompatible` should be true when the Python standalone and Java plugin versions match.

## Offline Restrictions

Target install does not run `pip install`, `git clone`, `curl`, `wget`, `npm`, cargo, or Gradle compilation.
