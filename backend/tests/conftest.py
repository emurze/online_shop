from typing import Any

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)

from config import AppConfig
from main import create_app
from shared.db import Base


@pytest.fixture(scope="function")
def config() -> AppConfig:
    return AppConfig(
        title="Test",
        db_dsn="postgresql+asyncpg://postgres:password@test_db:5432/postgres",
    )


@pytest.fixture(scope="function")
async def engine(config: AppConfig) -> AsyncEngine:
    eng = create_async_engine(config.db_dsn, poolclass=NullPool)

    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield eng


@pytest.fixture(scope="function")
async def db_session(engine: AsyncEngine) -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture(scope="function")
async def api_client(config: AppConfig) -> AsyncClient:
    api: Any = create_app(config)

    async with AsyncClient(
        transport=ASGITransport(app=api),
        base_url="http://test",
    ) as async_test_client:
        yield async_test_client
