# ============================================================
# SecureFlow — Hardened Container Image
# SP8 — Container Security
# ============================================================

FROM python:3.12-slim

# ------------------------------------------------------------
# Python runtime hardening
# ------------------------------------------------------------

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Send Python output directly to stdout/stderr
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# ------------------------------------------------------------
# Create dedicated non-root user
# ------------------------------------------------------------

RUN addgroup --system secureflow \
    && adduser --system --ingroup secureflow secureflow

# ------------------------------------------------------------
# Dependency installation
# ------------------------------------------------------------

# Copy dependency definition first for better Docker layer caching
COPY app/requirements.txt /app/requirements.txt

# Upgrade pip and install application dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Security updates for vulnerable transitive/build dependencies
RUN pip install --no-cache-dir --upgrade \
    "msgpack>=1.2.1" \
    "setuptools>=78.1.1"

# ------------------------------------------------------------
# Copy application source
# ------------------------------------------------------------

COPY app /app/app

# ------------------------------------------------------------
# File permissions
# ------------------------------------------------------------

RUN chown -R secureflow:secureflow /app

# ------------------------------------------------------------
# Drop root privileges
# ------------------------------------------------------------

USER secureflow

# ------------------------------------------------------------
# Application configuration
# ------------------------------------------------------------

EXPOSE 5000

# ------------------------------------------------------------
# Container health check
# ------------------------------------------------------------

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

# ------------------------------------------------------------
# Start SecureFlow
# ------------------------------------------------------------

CMD ["python", "app/app.py"]
