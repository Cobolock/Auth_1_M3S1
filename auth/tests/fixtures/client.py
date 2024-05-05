from collections.abc import AsyncIterator

import pytest

from fastapi import FastAPI
from fastapi_limiter.depends import RateLimiter
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth.db.postgres import get_session
from auth.db.redis import get_redis
from auth.main import app


@pytest.fixture()
async def test_app(session: AsyncSession, redis_client: Redis) -> FastAPI:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_redis] = lambda: redis_client
    app.dependency_overrides[RateLimiter] = lambda: None
    return app


@pytest.fixture()
async def test_client(test_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=test_app, base_url="https://test") as client:
        yield client
