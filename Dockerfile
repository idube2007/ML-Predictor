FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
# libgomp1 is absolutely required for scikit-learn on slim images
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . .

# Install dependencies from the unified requirements file
RUN pip install --no-cache-dir -r sris/backend/requirements.txt

# Set working directory to the backend code
WORKDIR /app/sris/backend

# Direct command to avoid shell script issues
# Render provides $PORT
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
