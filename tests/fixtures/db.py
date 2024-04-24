from collections.abc import AsyncIterator

import pytest

from redis.asyncio import Redis
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from auth.models.base import Base


@pytest.fixture()
def async_engine(postgres_container: PostgresContainer) -> AsyncEngine:
    return create_async_engine(
        postgres_container.get_connection_url(),
        poolclass=NullPool,  # https://stackoverflow.com/a/75444607/12530392
    )


@pytest.fixture()
async def redis_client(redis_container: RedisContainer) -> AsyncIterator[Redis]:
    redis = Redis(
        host=redis_container.get_container_host_ip(),
        port=int(redis_container.get_exposed_port(redis_container.port)),
    )
    yield redis
    await redis.close()


@pytest.fixture()
async def _init_db(async_engine, redis_client: Redis) -> AsyncIterator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await redis_client.flushdb()
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def session(_init_db, async_engine) -> AsyncIterator[AsyncSession]:
    async with AsyncSession(
        async_engine, expire_on_commit=False, autoflush=False, autocommit=False
    ) as session:
        yield session
