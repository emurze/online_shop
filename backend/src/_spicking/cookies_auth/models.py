# import uuid
# from typing import TYPE_CHECKING
#
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import Mapped, relationship, mapped_column
#
# from shared.db import Base
#
# if TYPE_CHECKING:
#     from api_v1.pizzas.models import Pizza
#     from api_v1.profiles.models import Profile
#     from api_v1.orders.models import Order
#
#
# class Session(Base):
#     user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
#     user: Mapped["User"] = relationship(back_populates="sessions")
#
#
# class User(Base):
#     username: Mapped[str] = mapped_column(unique=True)
#     email: Mapped[str] = mapped_column(unique=True)
#     hashed_password: Mapped[str]
#     is_active: Mapped[bool] = True
#     is_superuser: Mapped[bool] = False
#     profile: Mapped["Profile"] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )
#     pizzas: Mapped[list["Pizza"]] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )
#     sessions: Mapped[list["Session"]] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )
#     # orders: Mapped[list["Order"]] = relationship(
#     #     back_populates="user",
#     #     cascade="all, delete-orphan",
#     # )
#
#     def __str__(self) -> str:
#         return f"{type(self).__name__}(username={self.username!r})"
#
#     def __repr__(self) -> str:
#         return str(self)
