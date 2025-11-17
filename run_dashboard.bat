@echo off
REM Bank Marketing Dashboard Launcher
REM This script automatically starts the Streamlit dashboard

echo ====================================
echo  Bank Marketing Analytics Dashboard
echo ====================================
echo.
echo Starting dashboard...
echo.
echo The dashboard will open in your default browser.
echo Press Ctrl+C to stop the dashboard.
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ERROR: Streamlit is not installed!
    echo.
    echo Installing required packages...
    pip install -r requirements.txt
    echo.
)

REM Run the dashboard
streamlit run dashboard.py

pause

