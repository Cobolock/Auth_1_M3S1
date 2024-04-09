from collections.abc import AsyncGenerator
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from auth.core.config import pg_config


class UUIDBase(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


dsn = f"postgresql+asyncpg://{pg_config.user}:{pg_config.password}@{pg_config.host}:{pg_config.port}/{pg_config.db}"
engine = create_async_engine(dsn, echo=True, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)
