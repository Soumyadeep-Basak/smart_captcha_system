@echo off
echo ============================================
echo    Unified Bot Detection API - Modular
echo ============================================

cd /d "d:\hack\botv1"

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo Checking virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo WARNING: Virtual environment not found. Creating one...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing/updating basic requirements...
pip install flask flask-cors pandas numpy requests >nul 2>&1

echo.
echo Starting Unified Bot Detection API...
echo =====================================

echo Architecture: Single API with Modular Functions
echo Port: 5000
echo.

cd backend\api
python app.py

pause
