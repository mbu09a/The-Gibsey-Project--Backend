# Gibsey Project Makefile

.PHONY: seed test backend

seed:
	python -m scripts.seed --force

backend:
	pip install -r backend/app/requirements.txt

test: backend
	pytest -q 