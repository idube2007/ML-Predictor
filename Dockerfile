FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r sris/backend/requirements.txt

# Create necessary directories for models and data
RUN mkdir -p sris/models sris/data

# Set working directory to the backend
WORKDIR /app/sris/backend

# Use a direct command to skip entrypoint script issues
# We use python -m uvicorn for the most reliable module path resolution
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info"]
