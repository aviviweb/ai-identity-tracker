param(
    [int]$ApiPort = 8010,
    [int]$WebPort = 3000
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$backend  = Join-Path $repoRoot 'backend'
$frontend = Join-Path $repoRoot 'frontend'
$venvPy   = Join-Path $backend '.venv\Scripts\python.exe'

function Ensure-Venv {
    if (-not (Test-Path $venvPy)) {
        Push-Location $backend
        try {
            py -3.11 -m venv .venv
            & $venvPy -m pip install -U pip setuptools wheel
            & $venvPy -m pip install -U -e .
        } finally { Pop-Location }
    }
}

function Stop-Port([int]$Port){
    try {
        $pids = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
        if ($pids) { foreach($pid in $pids){ try { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue } catch {} } }
    } catch {}
}

Ensure-Venv

Stop-Port -Port 8001
Stop-Port -Port $ApiPort

# Start backend
$env:DATABASE_URL = 'sqlite:///C:/dev/ai-identity-tracker/dev.db'
$env:DEMO_MODE    = 'true'
$env:CORS_ORIGINS = "http://localhost:$WebPort,http://127.0.0.1:$WebPort"
$env:JWT_SECRET   = 'dev-secret-change'
Start-Process powershell -ArgumentList "-NoProfile -Command cd `"$backend`"; `$env:DATABASE_URL='$($env:DATABASE_URL)'; `$env:DEMO_MODE='$($env:DEMO_MODE)'; `$env:CORS_ORIGINS='$($env:CORS_ORIGINS)'; `$env:JWT_SECRET='$($env:JWT_SECRET)'; & `"$venvPy`" -m uvicorn app.main:app --host 127.0.0.1 --port $ApiPort" | Out-Null

# Wait for health
$ready = $false
for ($i=0; $i -lt 40; $i++){
    try { $r = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:$ApiPort/health" -TimeoutSec 1; if($r.StatusCode -eq 200){ $ready=$true; break } } catch {}
    Start-Sleep -Milliseconds 300
}
if (-not $ready) { throw "API not healthy on port $ApiPort" }

# Run backend smoke tests automatically
$env:TEST_API_BASE = "http://127.0.0.1:$ApiPort"
& $venvPy -m pytest -q

# Prepare frontend env and start dev server
$envFile = Join-Path $frontend '.env.local'
Set-Content -NoNewline -Path $envFile -Value "NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:$ApiPort`r`n"
Start-Process powershell -ArgumentList "-NoProfile -Command cd `"$frontend`"; npm install; npm run dev -- -p $WebPort" | Out-Null

Write-Host "Backend: http://127.0.0.1:$ApiPort" -ForegroundColor Green
Write-Host "Frontend: http://localhost:$WebPort" -ForegroundColor Green


