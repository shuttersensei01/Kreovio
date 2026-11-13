# Decisions

## 2026-11-13 — Start from an empty remote repository

**Context:** The referenced GitHub repository had no commits or files.

**Decision:** Create the Phase 0 scaffold directly on `phase/0-scaffold`, retaining Python 3.12 and the fixed technology choices in the supplied brief.

**Consequences:** Later phases can build on a runnable API skeleton. Docker must be installed locally before the MongoDB/Redis integration acceptance check can run.

## 2026-11-13 — Health endpoint degrades gracefully

**Context:** The API should identify Mongo replica-set and Redis availability.

**Decision:** `/health` attempts both checks and returns 503 with individual service statuses when either is unavailable.

**Consequences:** Orchestrators can detect unavailable infrastructure, while operators see the specific dependency that failed.

## 2026-11-13 — Use the existing local MongoDB listener

**Context:** The owner uses the local MongoDB instance on port 27017 through MongoDB Compass.

**Decision:** Kreovio defaults to `localhost:27017` with the required `rs0` replica-set connection option.

**Consequences:** The local MongoDB server must be configured with `replSetName: rs0` and initialized before transactional functionality is used.

