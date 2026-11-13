# Decisions

## 2026-11-13 — Start from an empty remote repository

**Context:** The referenced GitHub repository had no commits or files.

**Decision:** Create the Phase 0 scaffold directly on `phase/0-scaffold`, retaining Python 3.12 and the fixed technology choices in the supplied brief.

**Consequences:** Later phases can build on a runnable API skeleton. Docker must be installed locally before the MongoDB/Redis integration acceptance check can run.

## 2026-11-13 — Health endpoint degrades gracefully

**Context:** The API should identify Mongo replica-set and Redis availability.

**Decision:** `/health` attempts both checks and returns 503 with individual service statuses when either is unavailable.

**Consequences:** Orchestrators can detect unavailable infrastructure, while operators see the specific dependency that failed.

