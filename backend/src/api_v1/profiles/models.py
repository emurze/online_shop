from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.db import Base

if TYPE_CHECKING:
    from api_v1.auth.models import User


class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    bio: Mapped[Optional[str]]
    birthday: Mapped[str]
    gender: Mapped[str]
    photo_url: Mapped[Optional[str]]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="profile")

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(first_name={self.first_name!r}, last_name={self.last_name!r})"
        )
