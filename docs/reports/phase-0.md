# Phase 0 — Scaffold

## Built

- Python 3.12 FastAPI scaffold with settings, structured logging, UTC clock and dependency-aware health endpoint.
- Docker Compose services for MongoDB 7 replica set, Redis, and optional Ollama.
- uv project metadata, Make targets, unit-test skeleton, environment template, CI provisioning of MongoDB/Redis, and developer documentation.
- `make report` produces JUnit XML, XML/HTML coverage, and `docs/reports/TEST_REPORT.md`.

## Tests

- `make report` passes: 4 tests, ruff, mypy, and 92.5% branch coverage.
- Unit tests cover the UTC clock and healthy/unavailable MongoDB/Redis health responses.

## Known gaps

- GNU Make is installed and available in new terminals. Docker Desktop installation remains incomplete.
- The existing MongoDB process at `localhost:27017` is not replica-set enabled. Updating its protected configuration requires Windows administrator rights before transactions and live health can be verified.
- User, workspace, repository, audit, indexes and seed data begin in Phase 1.

## Run

Install/start Docker Desktop, configure local MongoDB with `replSetName: rs0`, then run `make up`, `make test`, `make lint`, `make typecheck`, and `make report`.

