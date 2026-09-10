#!/usr/bin/env bash
set -euo pipefail

DEVIN_EXE='D:\Company\Users\edward.yg.APEXGRP\AppData\Local\Programs\Devin\resources\app\extensions\windsurf\devin\bin\devin.exe'

if command -v rtk >/dev/null 2>&1; then
  PS=(rtk powershell.exe)
else
  PS=(powershell.exe)
fi

"${PS[@]}" -NoProfile -ExecutionPolicy Bypass -Command '
  $exe = $args[0]
  if ($args.Length -gt 1) {
    $rest = $args[1..($args.Length - 1)]
  } else {
    $rest = @()
  }
  & $exe @rest
  exit $LASTEXITCODE
' "$DEVIN_EXE" "$@"
