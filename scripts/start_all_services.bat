@echo off
echo ============================================
echo    Bot Detection System - Microservices
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

echo Installing/updating requirements...
pip install -r requirements.txt >nul 2>&1

echo.
echo Starting Microservices...
echo ========================

echo [1/4] Starting ML Model Service (Port 5002)...
start "ML Model Service" cmd /k "cd /d d:\hack\botv1 && call .venv\Scripts\activate.bat && cd backend\services\ml_model && python service.py"
timeout /t 5

echo [2/4] Starting Honeypot Service (Port 5001)...
start "Honeypot Service" cmd /k "cd /d d:\hack\botv1 && call .venv\Scripts\activate.bat && cd backend\services\honeypot && python service.py"
timeout /t 3

echo [3/4] Starting Fingerprinting Service (Port 5003)...
start "Fingerprinting Service" cmd /k "cd /d d:\hack\botv1 && call .venv\Scripts\activate.bat && cd backend\services\fingerprinting && python service.py"
timeout /t 3

echo [4/4] Starting API Gateway (Port 5000)...
start "API Gateway" cmd /k "cd /d d:\hack\botv1 && call .venv\Scripts\activate.bat && cd backend\api_gateway && python app.py"

echo.
echo ============================================
echo All Microservices Started Successfully!
echo ============================================
echo 🧠 ML Model Service:      http://localhost:5002/health
echo 🍯 Honeypot Service:      http://localhost:5001/health
echo 👆 Fingerprinting:        http://localhost:5003/health
echo 🚪 API Gateway:           http://localhost:5000/health
echo ============================================
echo 
echo Main Endpoint: POST http://localhost:5000/predict
echo.
echo Waiting for services to start...
timeout /t 10

echo Testing service health...
echo ========================
curl -s http://localhost:5000/health > nul 2>&1 && echo ✅ API Gateway: READY || echo ❌ API Gateway: NOT READY
curl -s http://localhost:5002/health > nul 2>&1 && echo ✅ ML Model: READY || echo ❌ ML Model: NOT READY  
curl -s http://localhost:5001/health > nul 2>&1 && echo ✅ Honeypot: READY || echo ❌ Honeypot: NOT READY
curl -s http://localhost:5003/health > nul 2>&1 && echo ✅ Fingerprinting: READY || echo ❌ Fingerprinting: NOT READY

echo.
echo ============================================
echo System Ready! You can now:
echo 1. Test the API: python test_backend.py  
echo 2. Use the frontend: cd frontend && npm run dev
echo 3. Submit forms to: http://localhost:5000/predict
echo ============================================

pause
