from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from shared.db import Base

# TODO: add permissions

if TYPE_CHECKING:
    from api_v1.pizzas.models import Pizza
    from api_v1.profiles.models import Profile


class User(Base):
    username: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = True
    is_superuser: Mapped[bool] = False
    profile: Mapped["Profile"] = relationship(back_populates="user")
    pizzas: Mapped[list["Pizza"]] = relationship(
        collection_class=list,
        back_populates="user",
    )
