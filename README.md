# Kreovio

AI-assisted client-journey platform for creative businesses.

## Local setup

1. Install Python 3.12, [uv](https://docs.astral.sh/uv/), and Docker Desktop.
2. Copy `.env.example` to `.env` and replace development secrets.
3. Run `make up` to start MongoDB (single-node replica set) and Redis.
4. Run `make test`, `make lint`, and `make typecheck`.

Run the API with `cd backend && uv run uvicorn app.main:app --reload`. `GET /health` reports MongoDB replica-set and Redis state.

Ollama is optional in Phase 0: run `docker compose --profile ollama up -d` when a local model is needed.

