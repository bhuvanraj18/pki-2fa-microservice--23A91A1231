# -----------------------------
# Stage 1: Builder
# -----------------------------
FROM python:3.11-slim-bookworm AS builder
WORKDIR /app

# Install necessary build tools (stable mirror)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tzdata \
        ca-certificates && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies into vendor folder
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir --target /app/vendor -r requirements.txt

# Copy project files
COPY app ./app
COPY scripts ./scripts
COPY student_private.pem student_public.pem instructor_public.pem ./
COPY cron/totp_cron ./cron/totp_cron


# -----------------------------
# Stage 2: Runtime
# -----------------------------
FROM python:3.11-slim-bookworm AS runtime
LABEL maintainer="student"

ENV TZ=UTC
ENV DATA_DIR=/data
WORKDIR /srv/app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        tzdata \
        ca-certificates && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories for persistence
RUN mkdir -p /data /cron && chmod 0755 /data /cron

# Copy vendor packages from builder
COPY --from=builder /app/vendor /srv/app/vendor
ENV PYTHONPATH=/srv/app/vendor

# Copy application files
COPY --from=builder /app/app ./app
COPY --from=builder /app/student_private.pem ./student_private.pem
COPY --from=builder /app/student_public.pem ./student_public.pem
COPY --from=builder /app/instructor_public.pem ./instructor_public.pem
COPY --from=builder /app/scripts ./scripts

# Copy cron config
COPY --from=builder /app/cron/totp_cron /etc/cron.d/totp_cron
RUN chmod 0644 /etc/cron.d/totp_cron

# Ensure scripts are executable
RUN chmod +x ./scripts/run_cron.sh
RUN chmod +x ./scripts/run_uvicorn.sh

EXPOSE 8080
VOLUME ["/data", "/cron"]

# Start cron & API
CMD ["bash", "-c", "cron -f & exec ./scripts/run_uvicorn.sh"]
