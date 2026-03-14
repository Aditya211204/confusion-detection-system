@echo off
REM Setup script for Windows

echo ========================================
echo AI Confusion Detection System - Setup
echo ========================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Setup complete!
echo.
echo To start the system:
echo   1. Run: venv\Scripts\activate
echo   2. Run: cd backend
echo   3. Run: python app.py
echo   4. Open: frontend\index.html in browser
echo.
echo ========================================
pause
