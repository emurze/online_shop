import importlib
import logging
import pkgutil
import re
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime
from functools import lru_cache
from typing import Optional

from sqlalchemy import DateTime, func, MetaData
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

from config import app_config, MODULES_DIR, Config


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        """Convert CamelCase to snake_case"""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    metadata = MetaData(naming_convention=app_config.db.naming_convention)
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

    def __str__(self) -> str:
        raise NotImplemented()

    def __repr__(self) -> str:
        return str(self)

    def as_dict(self, exclude: Optional[set] = None) -> dict:
        exclude = exclude or set()
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns  # type: ignore
            if column.name not in exclude
        }


class DatabaseAdapter:
    def __init__(
        self,
        dsn: str,
        echo: bool,
        pool_size: int,
        pool_max_overflow: int,
    ) -> None:
        self.engine = create_async_engine(
            dsn,
            echo=echo,
            pool_size=pool_size,
            max_overflow=pool_max_overflow,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()


def populate_base() -> None:
    """Populates Base by models imported from entire application."""
    lg = logging.getLogger(__name__)
    modules_dir_name = MODULES_DIR.name

    if not MODULES_DIR.exists():
        lg.error(f"{MODULES_DIR} does not exist")
        return

    for _, module_name, __ in pkgutil.iter_modules([str(MODULES_DIR)]):
        module_path = f"{modules_dir_name}.{module_name}.models"
        try:
            importlib.import_module(module_path)
            lg.debug(f"Successfully imported: {module_path}")
        except ModuleNotFoundError:
            lg.warning(f"No models.py found in {module_name}")
        except Exception as e:
            lg.error(f"Error importing {module_path}: {e}")


def get_db_adapter(config: Config = app_config) -> DatabaseAdapter:
    return DatabaseAdapter(
        dsn=config.db.dsn,
        echo=config.db.echo,
        pool_size=config.db.pool_size,
        pool_max_overflow=config.db.pool_max_overflow,
    )


@lru_cache(maxsize=1)
def _get_db_adapter() -> DatabaseAdapter:
    return get_db_adapter()


async def get_session() -> AsyncGenerator[AsyncSession]:
    db_adapter = _get_db_adapter()
    async with db_adapter.session_factory() as session:
        yield session
