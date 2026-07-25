$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $projectRoot "backend"
$frontendDir = Join-Path $projectRoot "frontend"
$env:BACKEND_URL = "http://127.0.0.1:8000"

Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
Set-Location $backendDir
C:/Users/sunee/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m pip install -r requirements.txt

Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location $frontendDir
C:/Users/sunee/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m pip install -r requirements.txt

Write-Host "Starting backend on http://127.0.0.1:8000" -ForegroundColor Green
Start-Process -FilePath "C:/Users/sunee/AppData/Local/Microsoft/WindowsApps/python3.12.exe" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -WorkingDirectory $backendDir

Write-Host "Starting frontend on http://127.0.0.1:8501" -ForegroundColor Green
Start-Process -FilePath "C:/Users/sunee/AppData/Local/Microsoft/WindowsApps/python3.12.exe" -ArgumentList "-m streamlit run app.py" -WorkingDirectory $frontendDir

Write-Host "Services started. Press Ctrl+C to stop them." -ForegroundColor Yellow
