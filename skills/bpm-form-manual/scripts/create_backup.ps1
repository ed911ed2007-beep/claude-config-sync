param(
  [Parameter(Mandatory=$true)][string]$ProjectDir,
  [Parameter(Mandatory=$true)][string]$BackupRoot,
  [string]$Date = (Get-Date -Format 'yyyy-MM-dd'),
  [string[]]$Include = @(
    '20260311_BPM三表單操作手冊_v2_utf8.pptx',
    '20260311_STYLE_BASELINE_v2_utf8.md',
    'make_manual_utf8.py',
    'manual_paths.json'
  )
)

$backupDir = Join-Path $BackupRoot ("backup_" + $Date)
New-Item -ItemType Directory -Force $backupDir | Out-Null

foreach ($name in $Include) {
  $src = Join-Path $ProjectDir $name
  if (Test-Path $src) {
    Copy-Item -Path $src -Destination $backupDir -Force
  }
}

Write-Output $backupDir
