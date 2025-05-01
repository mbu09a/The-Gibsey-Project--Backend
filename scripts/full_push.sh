#!/usr/bin/env bash
set -euo pipefail

# Final clean-up and first push to GitHub
# 1. Sanity checks (local)
git status -s
docker compose build fastapi redis cassandra-init
docker compose up -d redis cassandra-init fastapi
sleep 15
docker compose exec fastapi pytest -q

# 2. Fast-forward main and squash-merge work branch
git checkout main
git pull --rebase
git merge --squash codex/cicd-pipeline
git commit -m "backend: initial feature-complete MVP (vector search)"

# 3. Push main branch and set upstream
git push -u origin main

# 4. Optionally push long-lived feature branches for reference
git push origin codex/cicd-pipeline codex/redis-cache codex/auto-backend-upgrade || true

# 5. Reminder: verify the CI/CD workflow in GitHub Actions
echo "✅ CI/CD workflow should now be running (check Actions tab on GitHub)."