from dataclasses import dataclass
from typing import Any

from pymongo import AsyncMongoClient
from redis.asyncio import Redis

from app.core.config import Settings


@dataclass
class Infrastructure:
    mongo: AsyncMongoClient[dict[str, Any]]
    redis: Redis

    async def close(self) -> None:
        await self.mongo.close()
        await self.redis.aclose()


def create_infrastructure(settings: Settings) -> Infrastructure:
    return Infrastructure(
        mongo=AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=1_000),
        redis=Redis.from_url(settings.redis_url, socket_connect_timeout=1),
    )

