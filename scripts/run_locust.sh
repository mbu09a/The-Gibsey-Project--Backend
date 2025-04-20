#!/usr/bin/env bash
# Headless load test: 100 users, spawn 10/sec, 60 seconds

set -euo pipefail

docker compose exec fastapi locust -f tests/locustfile.py \
  --host http://localhost:8000 \
  --headless -u 100 -r 10 -t 60s