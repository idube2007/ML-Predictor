FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project first to maintain structure
COPY . .

# Install dependencies
# Point to the requirements file inside the structure
RUN pip install --no-cache-dir -r sris/backend/requirements.txt

# Set working directory to where main.py is
WORKDIR /app/sris/backend

# Use shell form to allow variable expansion for $PORT
# Render provides the PORT env var
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
