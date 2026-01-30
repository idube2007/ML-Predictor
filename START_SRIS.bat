@echo off
echo ==========================================
echo   Smart Retail Intelligence System (SRIS)
echo ==========================================
echo.
echo Starting Backend Server...
start "SRIS Backend" /D "d:\MLAPP\sris\backend" python -m uvicorn main:app --host 127.0.0.1 --port 8000

echo.
echo Waiting for server to initialize...
timeout /t 5 /nobreak > nul

echo Opening Unified App...
start "" "http://127.0.0.1:8000"

echo.
echo ==========================================
echo   System is now running!
echo   Unified App: http://127.0.0.1:8000
echo ==========================================
echo.
pause
