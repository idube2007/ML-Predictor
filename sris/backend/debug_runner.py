import sys
import os
import traceback

# Force unbuffered output so logs appear immediately
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("--- DEBUG RUNNER STARTING ---")
print(f"Python Version: {sys.version}")
print(f"CWD: {os.getcwd()}")
try:
    print(f"Files in CWD: {os.listdir('.')}")
    print(f"Files in ../: {os.listdir('..')}")
except Exception as e:
    print(f"Error listing dirs: {e}")

print(f"Sys Path: {sys.path}")

try:
    print("Attempting to import main...")
    import main
    print("Import main success!", flush=True)
except Exception:
    print("!!! IMPORT MAIN FAILED !!!", flush=True)
    traceback.print_exc()
    sys.exit(1)

print("Starting Uvicorn programmatically...", flush=True)
try:
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), log_level="info")
except Exception:
    print("!!! UVICORN START FAILED !!!", flush=True)
    traceback.print_exc()
    sys.exit(1)
