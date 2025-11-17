@echo off
REM Complete Setup and Launch Script
REM This script installs dependencies and launches the dashboard

echo ====================================
echo  Bank Marketing Dashboard Setup
echo ====================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Install/Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt
echo.

REM Check if installation was successful
python -c "import streamlit, pandas, sklearn, plotly" 2>nul
if errorlevel 1 (
    echo ERROR: Package installation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo ====================================
echo  Setup Complete!
echo ====================================
echo.
echo Starting dashboard...
echo.

REM Launch dashboard
streamlit run dashboard.py

pause

