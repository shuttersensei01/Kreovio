from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.db import Infrastructure, create_infrastructure
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    app.state.infrastructure = create_infrastructure(settings)
    yield
    await app.state.infrastructure.close()


app = FastAPI(title="Kreovio", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health() -> JSONResponse:
    infrastructure: Infrastructure = app.state.infrastructure
    mongo_status: dict[str, Any] = {"status": "ok", "replica_set": False}
    redis_status = {"status": "ok"}
    try:
        hello = await infrastructure.mongo.admin.command("hello")
        mongo_status["replica_set"] = bool(hello.get("setName"))
        if not mongo_status["replica_set"]:
            mongo_status["status"] = "degraded"
    except Exception:
        mongo_status["status"] = "unavailable"
    try:
        await infrastructure.redis.ping()
    except Exception:
        redis_status["status"] = "unavailable"
    healthy = mongo_status["status"] == "ok" and redis_status["status"] == "ok"
    return JSONResponse(
        status_code=200 if healthy else 503,
        content={
            "status": "ok" if healthy else "degraded",
            "mongo": mongo_status,
            "redis": redis_status,
        },
    )

