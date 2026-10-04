$ErrorActionPreference = "Stop"

Write-Host "==> Running gfc check..."
python -m gfc check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> All gfc checks passed!"
