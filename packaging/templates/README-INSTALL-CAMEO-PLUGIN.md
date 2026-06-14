# Cameo MCP Bridge Plugin Offline Install

This folder is the precompiled CATIA Magic / Cameo plugin for Cameo MCP Bridge version 2.3.5.

## Install

1. Close CATIA Magic / Cameo Systems Modeler.
2. Copy the entire `com.claude.cameo.bridge/` folder into your Cameo plugin directory:
   - Windows example: `C:\Program Files\CATIA Magic\plugins\com.claude.cameo.bridge\`
   - macOS/Linux example: `<CAMEO_HOME>/plugins/com.claude.cameo.bridge/`
3. Start CATIA Magic / Cameo.
4. Open a project.
5. Verify the local bridge is healthy:

```text
http://127.0.0.1:18740/api/v1/status
```

The response should report `pluginVersion`/`version` as `2.3.5`.

## Port Override

The plugin listens on `127.0.0.1:18740` by default. To change it, add a JVM option to Cameo's vmoptions file:

```text
-Dcameo.mcp.port=18741
```

If you change the plugin port, set the same port in the Goose standalone install via `CAMEO_BRIDGE_PORT` or by editing the Goose config entry.

## Compatibility

Use this plugin with the matching Cameo MCP Goose standalone bundle version `2.3.5`. The bridge requires exact plugin-version compatibility for non-status operations.
