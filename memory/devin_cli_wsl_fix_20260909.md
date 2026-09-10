# Devin CLI WSL Fix - 2026-09-09

## Finding

Devin CLI is supported by official Devin documentation for Windows and WSL. The local machine had Devin Desktop installed, but `devin` was not available from the CLI because the shell command shim had not been installed to PATH.

## Local Paths

- Devin Desktop: `D:\Company\Users\edward.yg.APEXGRP\AppData\Local\Programs\Devin\Devin.exe`
- Bundled CLI: `D:\Company\Users\edward.yg.APEXGRP\AppData\Local\Programs\Devin\resources\app\extensions\windsurf\devin\bin\devin.exe`
- Windows CLI shim: `D:\Company\Users\edward.yg.APEXGRP\AppData\Local\devin\bin\devin.cmd`
- WSL wrapper: `/home/edward/.local/bin/devin`

## Verified

- Devin Desktop version: `3.9.19`
- Devin CLI version: `devin 3000.6.19 (e2b252e2)`
- Windows command resolution after PATH refresh:
  `D:\Company\Users\edward.yg.APEXGRP\AppData\Local\devin\bin\devin.cmd`
- Auth status: not logged in.
- Credentials path expected by Devin:
  `D:\Company\Users\edward.yg.APEXGRP\AppData\Roaming\devin\credentials.toml`

## Current Next Step

Open a new PowerShell or Windows Terminal session and run:

```powershell
devin auth login
devin auth status
```

If authentication succeeds but usage returns `Not authorized`, the Devin enterprise admin must enable CLI access and assign the `Use Devin CLI` role.

## Notes

The WSL/Codex sandbox can fail when directly launching Windows `.exe` or `powershell.exe` with a WSL vsock error. Use `rtk powershell.exe` from Codex-controlled flows, or run `devin` directly from a normal user terminal.
