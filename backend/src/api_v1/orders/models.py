import uuid
from typing import Optional

from pydantic import PositiveInt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING
from shared.db import Base

if TYPE_CHECKING:
    from api_v1.auth.models import User


class Order(Base):
    payment_id: Mapped[Optional[str]]
    paid: Mapped[bool] = False
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete",
    )
    # user: Mapped["User"] = relationship(back_populates="orders")
    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))


class OrderItem(Base):
    quantity: Mapped[PositiveInt]
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="order_items",
        cascade="all, delete",
    )
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order.id"))
