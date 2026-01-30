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

echo.
echo Opening Frontend Dashboard...
start "" "d:\MLAPP\sris\frontend\login.html"

echo.
echo ==========================================
echo   System is now running!
echo   Backend: http://localhost:8000
echo   Frontend: login.html
echo ==========================================
echo.
pause
