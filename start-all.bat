@echo off
REM Start both Backend and Frontend

echo ====================================
echo  Bank Marketing Dashboard Launcher
echo ====================================
echo.
echo Starting Backend and Frontend...
echo.

REM Start backend in new window
start "Backend API" cmd /k call start-backend.bat

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "React Frontend" cmd /k call start-frontend.bat

echo.
echo ====================================
echo Both servers are starting!
echo ====================================
echo.
echo Backend API: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Two windows will open:
echo  1. Backend API Server (Flask)
echo  2. React Frontend (Development Server)
echo.
echo Wait for both to finish loading...
echo Your browser will open automatically.
echo.

pause

