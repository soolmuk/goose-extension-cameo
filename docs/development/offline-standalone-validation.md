# Offline Standalone Validation

Use this checklist before publishing offline Goose standalone artifacts.

## Clean Target Setup

- Use a clean VM or machine for each target OS/architecture.
- Disable network access before target installation.
- Ensure Python is not installed or is not available on `PATH`.
- Do not install pip, uv, npm, cargo, or Gradle on the target machine.

## Bundle Smoke Test

1. Copy the OS-specific `cameo-mcp-goose-python-standalone-*.zip` or `*.tar.gz` to the target.
2. Unpack it.
3. Run:

```bash
cameo-mcp-bridge/bin/cameo-mcp-bridge --print-goose-config
```

Expected: YAML snippet prints without importing target-machine Python.

## Goose Config Mutation Test

Run:

```bash
cameo-mcp-bridge/install/install-goose.sh
```

Windows:

```powershell
cameo-mcp-bridge\install\install-goose.ps1
```

Verify:

- Goose config was created or updated.
- A backup exists next to `config.yaml` named `config.yaml.backup-YYYYMMDD-HHMMSS`.
- No installer command attempts network access.
- The `cmd` path in Goose config is absolute and points to `bin/cameo-mcp-bridge(.exe)`.

## Cameo Bridge Validation

1. Install the separate Cameo plugin zip.
2. Restart Cameo and open a project.
3. Confirm `http://127.0.0.1:18740/api/v1/status` reports plugin version `2.3.5`.
4. Start Goose and verify `cameo_status` and `cameo_get_capabilities`.

## Failure Cases

- With Cameo not running, `cameo_status` should return a clear connection error.
- With mismatched Java plugin version, capability handshake should report compatibility failure.
