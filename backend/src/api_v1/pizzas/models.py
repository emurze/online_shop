import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, TEXT, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from shared.db import Base, Money

if TYPE_CHECKING:
    from api_v1.auth.models import User


class Pizza(Base):
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
    price: Mapped[Optional[Money]] = mapped_column(Money)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="pizzas")
