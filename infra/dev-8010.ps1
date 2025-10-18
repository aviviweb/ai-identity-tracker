param(
    [int]$ApiPort = 8010,
    [int]$WebPort = 3000
)

$ErrorActionPreference = "Stop"

function Stop-Port {
    param([int]$Port)
    try {
        $pids = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
        if ($pids) {
            foreach ($pid in $pids) { try { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue } catch {} }
            Write-Host "Stopped processes holding port $Port"
        }
    } catch {}
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$backend  = Join-Path $repoRoot 'backend'
$venvPy   = Join-Path $backend '.venv\Scripts\python.exe'

Push-Location $backend
try {
    # Ensure venv
    if (-not (Test-Path $venvPy)) {
        py -3.11 -m venv .venv
        & $venvPy -m pip install -U pip setuptools wheel
        & $venvPy -m pip install -U -e .
    }

    # Free conflicting ports
    Stop-Port -Port 8001
    Stop-Port -Port $ApiPort

    # Start backend on $ApiPort
    $env:DATABASE_URL = 'sqlite:///C:/dev/ai-identity-tracker/dev.db'
    $env:DEMO_MODE    = 'true'
    $env:CORS_ORIGINS = "http://localhost:$WebPort,http://127.0.0.1:$WebPort"
    $env:JWT_SECRET   = 'dev-secret-change'

    Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile -Command cd `"$backend`"; `$env:DATABASE_URL='$($env:DATABASE_URL)'; `$env:DEMO_MODE='$($env:DEMO_MODE)'; `$env:CORS_ORIGINS='$($env:CORS_ORIGINS)'; `$env:JWT_SECRET='$($env:JWT_SECRET)'; & `"$venvPy`" -m uvicorn app.main:app --host 127.0.0.1 --port $ApiPort" | Out-Null

    # Wait for health
    $ready = $false
    for ($i=0; $i -lt 40; $i++) {
        try {
            $r = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:$ApiPort/health" -TimeoutSec 1
            if ($r.StatusCode -eq 200) { $ready = $true; break }
        } catch {}
        Start-Sleep -Milliseconds 300
    }
    if (-not $ready) { throw "API not healthy on port $ApiPort" }
    Write-Host "API ready on http://127.0.0.1:$ApiPort" -ForegroundColor Green

    # Run backend tests
    $env:TEST_API_BASE = "http://127.0.0.1:$ApiPort"
    & $venvPy -m pytest -q
}
finally {
    Pop-Location
}


