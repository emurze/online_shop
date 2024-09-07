from sqlalchemy.orm import Mapped, relationship

from api_v1.pizzas.models import Pizza
from shared.db import Base

# TODO: add permissions


class User(Base):
    username: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_active: Mapped[bool] = True
    is_superuser: Mapped[bool] = False
    pizzas: Mapped[list["Pizza"]] = relationship(
        "Pizza",
        collection_class=list,
        back_populates="user",
    )
