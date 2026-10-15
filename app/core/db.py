import logging
from typing import Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import PyMongoError

from app.core.config import get_settings

logger = logging.getLogger("uvicorn.error")

_client: AsyncMongoClient[dict[str, Any]] | None = None


async def connect_mongo() -> None:
    global _client
    settings = get_settings()
    _client = AsyncMongoClient(
        settings.mongo_uri.get_secret_value(),
        tz_aware=True,
        serverSelectionTimeoutMS=5000,
    )
    await _client.admin.command("ping")
    logger.info("MongoDB connected (database: %s)", settings.mongo_name)


async def close_mongo() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None
        logger.info("MongoDB connection closed")


def get_db() -> AsyncDatabase[dict[str, Any]]:
    if _client is None:
        raise RuntimeError("MongoDB is not connected")
    return _client[get_settings().mongo_name]


async def ping_mongo() -> bool:
    try:
        await get_db().command("ping")
    except (PyMongoError, RuntimeError):
        return False
    return True
