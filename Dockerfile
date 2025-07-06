# Stage 1: Builder
# This stage installs all Python dependencies.
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Stage 2: Runtime
# This is the final, smaller image.
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy only the installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy your application code
COPY . .

RUN useradd --system --create-home appuser
USER appuser

CMD ["python", "publish_mqtt.py"]
