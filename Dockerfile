FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

# DO NOT CHANGE MIRROR — Debian security repo breaks otherwise
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    rm -rf /var/lib/apt/lists/* && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . /app

RUN mkdir -p /data /cron
RUN chmod 644 /app/cron/2fa-cron && crontab /app/cron/2fa-cron

EXPOSE 8080

CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
