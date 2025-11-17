@echo off
REM Start Flask Backend Server

echo ====================================
echo  Starting Backend API Server
echo ====================================
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements-api.txt

echo.
echo ====================================
echo  Backend API Running
echo ====================================
echo.
echo API URL: http://localhost:5000
echo Health Check: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the Flask app
python app.py

pause

