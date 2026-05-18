#!/usr/bin/env bash
# Build and start NRMS AI API container
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Missing .env — copy from .env.example and set GEMINI_API_KEY"
  cp -n .env.example .env
  exit 1
fi

echo "Building and starting nrms-api..."
docker compose build --no-cache
docker compose up -d

echo "Waiting for health..."
for i in $(seq 1 30); do
  if curl -sf http://127.0.0.1:8001/health >/dev/null 2>&1; then
    echo "OK — API healthy at http://127.0.0.1:8001"
    curl -s http://127.0.0.1:8001/health
    echo ""
    echo "After nginx is configured: https://nrms.ati.gov.et/assistant"
    exit 0
  fi
  sleep 2
done

echo "Health check failed — logs:"
docker compose logs --tail=50 nrms-api
exit 1
