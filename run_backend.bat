@echo off
echo Starting SRIS Backend...
cd sris/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause
