@echo off
echo ========================================
echo    Service Restart & Cleanup Script
echo ========================================

echo Checking for hanging Python processes...
tasklist | findstr python.exe
if errorlevel 1 (
    echo No Python processes found
) else (
    echo Found Python processes. Terminating...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2
)

echo Checking if ports are still in use...
netstat -an | findstr ":500"

echo.
echo Cleaning up any orphaned processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5001"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5002"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5003"') do taskkill /f /pid %%a >nul 2>&1

echo.
echo Waiting for ports to be released...
timeout /t 5

echo.
echo Starting health check...
cd /d "d:\hack\botv1"
python test_services_health.py

echo.
echo Starting services again...
call scripts\start_all_services.bat

echo.
echo Done! Services should be starting up now.
echo Wait about 30 seconds then check: http://localhost:5000/health
pause
