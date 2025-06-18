# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Suppress pip root user warning
ENV PIP_ROOT_USER_ACTION=ignore

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Set default environment variables (override at runtime if needed)
ENV ENV=PROD
ENV LOG_LEVEL=WARNING

# Entry point: start the WebSocket bot/orchestrator
CMD ["python", "main.py"]