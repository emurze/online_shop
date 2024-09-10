from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from shared.db import Base

if TYPE_CHECKING:
    from api_v1.orders.models import Order


class Coupon(Base):
    active: Mapped[bool] = True
    orders: Mapped[list["Order"]] = relationship(
        back_populates="coupon",
    )
