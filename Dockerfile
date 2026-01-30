FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r sris/backend/requirements.txt

# Set working directory to backend
WORKDIR /app/sris/backend

# Ensure entrypoint is executable
RUN chmod +x entrypoint.sh

# Use the entrypoint script
CMD ["./entrypoint.sh"]
