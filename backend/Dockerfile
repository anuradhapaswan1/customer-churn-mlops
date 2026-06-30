# Use a lightweight python image matching your stack
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer streams for real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install basic compiler toolsets required by underlying C-libraries (like scikit-learn/xgboost)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the root context into the container build layer
COPY requirements.txt .

# Upgrade pip and install package dependencies without keeping cache footprints
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all local backend resources to our working directory container space
COPY . .

# Expose server port
EXPOSE 8000

# Run the API via Uvicorn bound to all interfaces inside the container
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]