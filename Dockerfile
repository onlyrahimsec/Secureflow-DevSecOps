# ============================================================
# SecureFlow — Hardened Container Image
# SP8 — Container Security
# ============================================================

FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Send Python output directly to stdout/stderr
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Create a dedicated non-root user
RUN addgroup --system secureflow \
    && adduser --system --ingroup secureflow secureflow

# Copy dependency definition first for better Docker layer caching
COPY app/requirements.txt /app/requirements.txt

# Install dependencies without pip cache
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY app /app/app

# Create required runtime directories if needed
RUN chown -R secureflow:secureflow /app

# Drop root privileges
USER secureflow

# Application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=10s \
            --retries=3 \
            CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

# Start SecureFlow
CMD ["python", "app/app.py"]
