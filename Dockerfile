# -------------------------------------------------------------
# NorthStar Commercial Insurance Intake & Triage Gateway
# Production Dockerfile for Google Cloud Run Global Deployment
# -------------------------------------------------------------

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APP_ENV=production \
    GCP_REGION=asia-south1

WORKDIR /app

# Install system dependencies (build-essential, curl, libsqlite3)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and data
COPY app/ ./app/
COPY data/ ./data/

# Create app directory, data directory, and non-root user
RUN mkdir -p /app/data && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# Cloud Run container entrypoint
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 2
