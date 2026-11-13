from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

import app.main as main_module
from app.core.config import Settings
from app.main import app


class MongoStub:
    admin = type("Admin", (), {"command": AsyncMock(return_value={"setName": "rs0"})})()


class RedisStub:
    ping = AsyncMock()


@pytest.mark.asyncio
async def test_health_reports_connected_services() -> None:
    app.state.infrastructure = type(
        "InfrastructureStub",
        (),
        {
            "mongo": MongoStub(),
            "redis": RedisStub(),
        },
    )()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "mongo": {"status": "ok", "replica_set": True},
        "redis": {"status": "ok"},
    }


@pytest.mark.asyncio
async def test_lifespan_creates_and_closes_infrastructure(monkeypatch: pytest.MonkeyPatch) -> None:
    infrastructure = type("InfrastructureStub", (), {"close": AsyncMock()})()
    monkeypatch.setattr(main_module, "create_infrastructure", lambda _settings: infrastructure)
    monkeypatch.setattr(main_module, "get_settings", lambda: Settings())
    async with main_module.lifespan(app):
        assert app.state.infrastructure is infrastructure
    infrastructure.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_health_reports_unavailable_dependencies() -> None:
    unavailable = AsyncMock(side_effect=ConnectionError)
    admin = type("Admin", (), {"command": unavailable})()
    mongo = type("MongoStub", (), {"admin": admin})()
    app.state.infrastructure = type(
        "InfrastructureStub",
        (),
        {
            "mongo": mongo,
            "redis": type("RedisStub", (), {"ping": unavailable})(),
        },
    )()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 503
    assert response.json()["mongo"]["status"] == "unavailable"
    assert response.json()["redis"]["status"] == "unavailable"

