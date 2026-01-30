# SRIS - Smart Retail Intelligence System

A full-stack, machine learning powered retail analytics platform.

## Features
- **Dynamic Pricing**: Regression-based price optimization.
- **Demand Forecasting**: Time-series analysis for inventory planning.
- **Segmentation**: Customer clustering for targeted marketing.
- **Anomalies**: Sales irregularity detection.
- **Dashboard**: Premium, interactive data visualization.

## Quick Start (Local)

### 1. Requirements
- Python 3.9+
- Node.js (Optional, for advanced Tailwind customization)

### 2. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python scripts/generate_data.py
```

### 3. Run Backend
Run the included batch file:
```bash
./run_backend.bat
```
Or manually:
```bash
cd sris/backend
python -m uvicorn main:app --reload
```

### 4. Run Frontend
Simply open `frontend/login.html` in your browser. (Note: Ensure the backend is running for data fetching and ML predictions).

## Project Structure
- `backend/`: FastAPI application, API routes, and ML pipelines.
- `frontend/`: HTML/CSS/JS dashboard and UI components.
- `data/`: CSV datasets (Generated/Uploaded).
- `models/`: Trained ML model binaries.
- `scripts/`: Utility scripts for data generation.

## Testing
- Run `pytest` in the `backend/` directory to execute automated tests.
