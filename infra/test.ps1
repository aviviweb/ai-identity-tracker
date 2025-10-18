param(
    [string]$ApiBase = "http://127.0.0.1:8001"
)

$ErrorActionPreference = "Stop"

Push-Location "$PSScriptRoot\..\backend"
try {
    $env:DATABASE_URL = 'sqlite:///C:/dev/ai-identity-tracker/dev.db'
    $env:DEMO_MODE = 'true'
    $env:CORS_ORIGINS = 'http://localhost:3000,http://127.0.0.1:3000'
    $env:JWT_SECRET = 'dev-secret-change'
    $env:TEST_API_BASE = $ApiBase

    .\.venv\Scripts\python.exe -m pytest
}
finally {
    Pop-Location
}



