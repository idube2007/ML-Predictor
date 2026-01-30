FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
# sed is needed to fix line endings from Windows
RUN apt-get update && apt-get install -y \
    build-essential \
    sed \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r sris/backend/requirements.txt

# Set working directory to where main.py is
WORKDIR /app/sris/backend

# FIX FOR WINDOWS LINE ENDINGS:
# This converts CRLF to LF in case the file was saved on Windows
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Use the entrypoint script (using path to current dir)
CMD ["./entrypoint.sh"]
