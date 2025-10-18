param(
    [string]$ApiPort = "8001",
    [string]$WebPort = "3000"
)

$ErrorActionPreference = "Stop"

Push-Location "$PSScriptRoot\.."
try {
    $env:DATABASE_URL = 'sqlite:///C:/dev/ai-identity-tracker/dev.db'
    $env:DEMO_MODE = 'true'
    $env:CORS_ORIGINS = "http://localhost:$WebPort,http://127.0.0.1:$WebPort"
    $env:JWT_SECRET = 'dev-secret-change'

    Start-Process powershell -ArgumentList "-NoProfile -Command cd backend; .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port $ApiPort" | Out-Null
    Start-Process powershell -ArgumentList "-NoProfile -Command cd frontend; npm run dev -- -p $WebPort" | Out-Null
    Write-Host "Started backend on 127.0.0.1:$ApiPort and frontend on http://localhost:$WebPort"
}
finally {
    Pop-Location
}



