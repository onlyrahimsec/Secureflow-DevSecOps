# ============================================================
# SecureFlow — Hardened Container Image
# SP8 — Container Security
# ============================================================

FROM python:3.12-slim

# ------------------------------------------------------------
# Python runtime hardening
# ------------------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# ------------------------------------------------------------
# Create dedicated non-root user
# ------------------------------------------------------------

RUN addgroup --system secureflow \
    && adduser --system --ingroup secureflow secureflow

# ------------------------------------------------------------
# Copy dependency definition first
# ------------------------------------------------------------

COPY app/requirements.txt /app/requirements.txt

# ------------------------------------------------------------
# Upgrade packaging tooling and install dependencies
# ------------------------------------------------------------

RUN python -m pip install --no-cache-dir --upgrade \
        pip \
        setuptools>=78.1.1 \
    && python -m pip install --no-cache-dir \
        msgpack>=1.2.1 \
    && python -m pip install --no-cache-dir \
        -r /app/requirements.txt

# ------------------------------------------------------------
# Explicit security verification
# ------------------------------------------------------------

RUN python -c "import setuptools; print('setuptools:', setuptools.__version__)" \
    && python -c "import msgpack; print('msgpack:', msgpack.__version__)"

# ------------------------------------------------------------
# Copy application source
# ------------------------------------------------------------

COPY app /app/app

# ------------------------------------------------------------
# Set ownership
# ------------------------------------------------------------

RUN chown -R secureflow:secureflow /app

# ------------------------------------------------------------
# Drop root privileges
# ------------------------------------------------------------

USER secureflow

# ------------------------------------------------------------
# Application port
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
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" \
    || exit 1

# ------------------------------------------------------------
# Start SecureFlow
# ------------------------------------------------------------

CMD ["python", "app/app.py"]
