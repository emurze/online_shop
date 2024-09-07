import uuid
from typing import Optional

from sqlalchemy import ForeignKey, UUID, TEXT, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from shared.db import Base, Money


class Pizza(Base):
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
    price: Mapped[Optional[Money]] = mapped_column(Money)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID, ForeignKey("user.id")
    )
    user = relationship("User", back_populates="pizzas")
