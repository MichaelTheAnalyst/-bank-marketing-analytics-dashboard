@echo off
REM Start React Frontend

echo ====================================
echo  Starting React Frontend
echo ====================================
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    echo This may take a few minutes...
    npm install
    echo.
)

echo.
echo ====================================
echo  React App Starting
echo ====================================
echo.
echo Frontend URL: http://localhost:3000
echo.
echo The browser will open automatically
echo Press Ctrl+C to stop the server
echo.

REM Start React development server
npm start

pause

