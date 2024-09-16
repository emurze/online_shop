from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    GUID,
    SQLAlchemyUserDatabase,
)
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
    SQLAlchemyAccessTokenDatabase,
)
from sqlalchemy import String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.db import Base

if TYPE_CHECKING:
    from api_v1.orders.models import Order


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    # orders: Mapped[list["Order"]] = relationship(
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    # )

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyUserDatabase:
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self) -> str:
        return f"{type(self).__name__}(username={self.username!r})"


class AccessToken(Base, SQLAlchemyBaseAccessTokenTableUUID):
    user_id: Mapped[GUID] = mapped_column(
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyAccessTokenDatabase:
        return SQLAlchemyAccessTokenDatabase(session, cls)

    def __str__(self) -> str:
        return f"{type(self).__name__}(user_id={self.user_id!r})"
