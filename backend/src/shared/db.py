import importlib
import logging
import pkgutil
import re
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any, cast, Optional

from faker.utils.text import slugify
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


db_adapter = DatabaseAdapter(
    dsn=config.db.dsn,
    echo=config.db.echo,
    pool_size=config.db.pool_size,
    pool_max_overflow=config.db.pool_max_overflow,
)


def populate_base() -> None:
    """Populates Base by models imported from entire application."""
    lg = logging.getLogger(__name__)
    modules_dir = config.modules_dir

    if not modules_dir.exists():
        lg.error(f"{modules_dir} does not exist")
        return

    for _, module_name, __ in pkgutil.iter_modules([str(modules_dir)]):
        module_path = f"{config.modules_dir_name}.{module_name}.models"
        try:
            importlib.import_module(module_path)
            lg.debug(f"Successfully imported: {module_path}")
        except ModuleNotFoundError:
            lg.warning(f"No models.py found in {module_name}")
        except Exception as e:
            lg.error(f"Error importing {module_path}: {e}")


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with db_adapter.session_factory() as session:
        yield session


def make_slug(oid: uuid.UUID, title: str) -> str:
    return slugify(f"{str(oid)[:13]}-{title}")


def cast_any(obj: Any) -> Any:
    return cast(Any, obj)


def convert_filter_by(model_class: type[Base], filter_by: str) -> list:
    """TODO: write input / output docs"""
    if filter_by is not None and filter_by != "null":
        criteria = dict(x.strip().split("=") for x in filter_by.split(","))

        criteria_list = []
        for attr, value in criteria.items():
            if _attr := getattr(model_class, attr, None):
                if attr.endswith("id"):
                    criteria_list.append(_attr == value)
                else:
                    search = f"%{value}%"
                    criteria_list.append(_attr.ilike(search))

        return criteria_list

    return []


def convert_sort_by(model_class: type[Base], sort_by: str):
    """TODO: write input / output docs"""
    sort_fields = sort_by.split(",")
    sort_criteria = []
    for field_direction in sort_fields:
        field, direction = field_direction.split(":")
        if _attr := getattr(model_class, field, None):
            if direction == "asc":
                sort_criteria.append(_attr.asc())
            elif direction == "desc":
                sort_criteria.append(_attr.desc())

    return sort_criteria


Money = DECIMAL(precision=10, scale=2)
