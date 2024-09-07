import re
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime

import redis.asyncio
from passlib.context import CryptContext
from redis.asyncio import Redis
from sqlalchemy import DateTime, func, DECIMAL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)

from config import config


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        """Convert CamelCase to snake_case"""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    )


class DatabaseAdapter:
    def __init__(self, db_dsn: str, echo: bool) -> None:
        self.engine = create_async_engine(db_dsn, echo=echo)
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )


db_adapter = DatabaseAdapter(db_dsn=config.db_dsn, echo=config.db_echo)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with db_adapter.session_factory() as session:
        yield session


async def get_redis() -> Redis:
    return redis.asyncio.from_url(
        config.redis_dsn,
        decode_responses=True,
    )


Money = DECIMAL(precision=10, scale=2)


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)
