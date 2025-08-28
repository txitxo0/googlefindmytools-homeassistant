# Stage 1: Builder
# This stage installs all Python dependencies.
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
# This is the final, smaller image. We start from a clean base and only copy
# the necessary artifacts from the builder stage.
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only the runtime dependencies (Google Chrome)
RUN apt-get update && apt-get install -y ca-certificates gnupg wget --no-install-recommends \
    && mkdir -p /etc/apt/keyrings \
    && wget -q -O- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor | tee /etc/apt/keyrings/google-chrome.gpg > /dev/null \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \ 
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy only the installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy your application code
COPY . .

ENV HEADLESS=true

RUN useradd --system --create-home appuser
USER appuser

CMD ["python", "publish_mqtt.py"]
