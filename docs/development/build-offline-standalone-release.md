# Build Offline Standalone Release

Release build machines may use the internet to download build dependencies. Target install machines must not.

## Python Standalone Bundle

Build separately on each target OS/architecture:

```bash
packaging/scripts/build-standalone.sh
python3 packaging/scripts/assemble-standalone-bundle.py --os linux --arch x64 --archive tar.gz
```

Windows:

```powershell
packaging\scripts\build-standalone.ps1
python packaging\scripts\assemble-standalone-bundle.py --os windows --arch x64 --archive zip
```

Expected PyInstaller output:

- Windows: `dist/cameo-mcp-bridge/cameo-mcp-bridge.exe`
- macOS/Linux: `dist/cameo-mcp-bridge/cameo-mcp-bridge`

## Cameo Plugin Zip

Build with a Cameo install available to Gradle:

```bash
cd plugin
./gradlew assemblePlugin -PcameoHome=/path/to/CatiaMagic
cd ..
packaging/scripts/package-cameo-plugin.sh
```

The zip must contain:

- `com.claude.cameo.bridge/plugin.xml`
- `com.claude.cameo.bridge/cameo-mcp-bridge-2.3.5.jar`
- `com.claude.cameo.bridge/README-INSTALL-CAMEO-PLUGIN.md`

## Checksums

```bash
python3 packaging/scripts/generate-checksums.py release
```

## Validation

Run unit tests:

```bash
cd mcp-server
python3 -m pytest
```

Run packaged smoke tests on every target OS/arch:

```bash
packaging/scripts/smoke-test-standalone.sh /path/to/cameo-mcp-bridge
```

Then follow `docs/development/offline-standalone-validation.md` in clean no-network machines.

## Publish

Only after validation, commit, tag, push, and create a GitHub Release using `packaging/scripts/create-github-release.sh` or the GitHub UI.
