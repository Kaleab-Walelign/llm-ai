#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  echo "Create .env from .env.example and set GEMINI_API_KEY"
  cp .env.example .env
  exit 1
fi
export PYTHONPATH=.
exec uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
