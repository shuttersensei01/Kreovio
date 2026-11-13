.DEFAULT_GOAL := test

up:
	docker compose up -d mongo mongo-init redis

down:
	docker compose down

test:
	cd backend && uv run pytest

lint:
	cd backend && uv run ruff check .

typecheck:
	cd backend && uv run mypy app

report:
	cd backend && uv run pytest --junitxml=../junit.xml --cov=app --cov-report=xml:../coverage.xml --cov-report=html:../htmlcov

seed:
	cd backend && uv run python scripts/seed.py

demo:
	cd backend && uv run python scripts/demo.py

eval:
	cd backend && uv run pytest tests/ai_eval

eval-live:
	cd backend && uv run pytest -m live tests/ai_eval

