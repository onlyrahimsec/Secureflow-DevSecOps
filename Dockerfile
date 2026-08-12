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

WORKDIR /app

# ------------------------------------------------------------
# Create dedicated non-root user
# ------------------------------------------------------------

RUN addgroup --system secureflow \
    && adduser --system --ingroup secureflow secureflow

# ------------------------------------------------------------
# Copy requirements
# ------------------------------------------------------------

COPY app/requirements.txt /app/requirements.txt

# ------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------

RUN python -m pip install --no-cache-dir --upgrade pip setuptools \
    && python -m pip install --no-cache-dir -r /app/requirements.txt \
    && python -m pip install --no-cache-dir --upgrade \
        "msgpack>=1.2.1" \
        "setuptools>=78.1.1"

# ------------------------------------------------------------
# Remove pip cache and temporary files
# ------------------------------------------------------------

RUN rm -rf /root/.cache/pip \
           /tmp/*

# ------------------------------------------------------------
# Verify actual installed versions
# ------------------------------------------------------------

RUN python -c "import msgpack; print('msgpack:', msgpack.__version__)" \
    && python -c "import setuptools; print('setuptools:', setuptools.__version__)"

# ------------------------------------------------------------
# Copy application
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
# Health check
# ------------------------------------------------------------

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" \
    || exit 1

# ------------------------------------------------------------
# Start application
# ------------------------------------------------------------

CMD ["python", "app/app.py"]
