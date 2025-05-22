# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies for zymbit (example: libzmq, may need adjustment)
RUN apt-get update && \
    apt-get install -y libzmq3-dev curl && \
    rm -rf /var/lib/apt/lists/*
# Install zymbit driver
# RUN curl -G https://s3.amazonaws.com/zk-sw-repo/install_zk_sw.sh | bash

# Copy requirements (assuming requirements.txt exists)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app (assuming main.py and app instance)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]