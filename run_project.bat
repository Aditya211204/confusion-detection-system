@echo off
echo ========================================
echo AI Confusion Detection System
echo ========================================
echo.

IF NOT EXIST "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting backend server...
echo The app will be available at http://127.0.0.1:5000
echo.

REM Automatically open the frontend
start "" "http://127.0.0.1:5000"

REM Run the backend
venv\Scripts\python.exe backend/app.py

pause
