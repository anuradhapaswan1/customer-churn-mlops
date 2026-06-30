# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy requirements file from context
COPY requirements.txt .

# Install dependencies into wheels directory to avoid compiling in final image
RUN pip install --no-cache-dir --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ==========================================
# STAGE 2: Final Production Image
# ==========================================
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer streams for real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    MODEL_PATH=/models/churn_model.pkl

WORKDIR /app

# Create a non-root group and user for secure sandbox execution
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy wheels from builder stage and install dependencies
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application source files
COPY --chown=appuser:appgroup . .

# Setup directory for external model mounting and volume declaration
RUN mkdir -p /models && chown -R appuser:appgroup /models
VOLUME ["/models"]

# Switch to non-root user
USER appuser

# Expose internal API port
EXPOSE 8000

# Run FastAPI backend via Uvicorn bound to all interfaces
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]