from collections.abc import AsyncGenerator

import redis.asyncio
from redis.asyncio import Redis
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from config import config


class Base(DeclarativeBase):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    )


_engine = create_async_engine(config.db_dsn)
_session_factory = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with _session_factory() as session:
        yield session


async def get_redis() -> Redis:
    return redis.asyncio.from_url(
        config.redis_dsn,
        decode_responses=True,
    )
