# Phase 0 — Scaffold

## Built

- Python 3.12 FastAPI scaffold with settings, structured logging, UTC clock and dependency-aware health endpoint.
- Docker Compose services for MongoDB 7 replica set, Redis, and optional Ollama.
- uv project metadata, Make targets, unit-test skeleton, environment template, and developer documentation.

## Tests

- Unit tests cover the UTC clock and a healthy Mongo replica-set/Redis health response.

## Known gaps

- Docker is not installed in the current environment, so local service integration could not be verified yet.
- User, workspace, repository, audit, indexes and seed data begin in Phase 1.

## Run

Install uv, run `make up`, then `make test`, `make lint`, and `make typecheck`.

