# Bank Marketing Dashboard Launcher (PowerShell)
# This script automatically starts the Streamlit dashboard

Write-Host "====================================" -ForegroundColor Cyan
Write-Host " Bank Marketing Analytics Dashboard" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting dashboard..." -ForegroundColor Green
Write-Host ""
Write-Host "The dashboard will open in your default browser."
Write-Host "Press Ctrl+C to stop the dashboard."
Write-Host ""

# Check if streamlit is installed
$streamlitInstalled = python -c "import streamlit" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Streamlit is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host ""
}

# Run the dashboard
streamlit run dashboard.py

Write-Host ""
Write-Host "Dashboard stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"

