#!/bin/bash
set -e

echo "Starting SRIS Production App..."
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -F

if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found in $(pwd)!"
    exit 1
fi

echo "Launching Uvicorn on PORT: $PORT"
exec python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
