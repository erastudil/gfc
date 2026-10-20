$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    $env:PYTHONPATH = "src"

    Write-Host "==> Running gfc check..."
    python -m gfc check
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "==> Running gfc unit tests..."
    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "==> All gfc checks passed!"
} finally {
    Pop-Location
}
