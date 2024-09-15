import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, TEXT, String, Table, Column, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from shared.db import Base
from shared.db_utils import Money

if TYPE_CHECKING:
    from api_v1.auth.models import User

pizza_size_association = Table(
    "pizza_size_association",
    Base.metadata,
    Column("pizza_id", UUID, ForeignKey("pizza.id"), primary_key=True),
    Column(
        "pizza_size_id",
        UUID,
        ForeignKey("pizza_size.id"),
        primary_key=True,
    ),
)

pizza_type_association = Table(
    "pizza_type_association",
    Base.metadata,
    Column("pizza_id", UUID, ForeignKey("pizza.id"), primary_key=True),
    Column(
        "pizza_type_id",
        UUID,
        ForeignKey("pizza_type.id"),
        primary_key=True,
    ),
)


class PizzaCategory(Base):
    title: Mapped[str]
    pizzas: Mapped[list["Pizza"]] = relationship(back_populates="category")

    def __str__(self) -> str:
        return f"{type(self).__name__}(title={self.title!r})"


class Pizza(Base):
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
    price: Mapped[Money] = mapped_column(Money)
    user: Mapped[Optional["User"]] = relationship(back_populates="pizzas")
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("user.id"))
    sizes: Mapped[set["PizzaSize"]] = relationship(
        secondary=pizza_size_association,
        back_populates="pizzas",
    )
    types: Mapped[set["PizzaType"]] = relationship(
        secondary=pizza_type_association,
        back_populates="pizzas",
    )
    category: Mapped[Optional["PizzaCategory"]] = relationship(
        back_populates="pizzas"
    )
    category_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("pizza_category.id")
    )

    def __str__(self) -> str:
        return f"{type(self).__name__}(title={self.title!r})"


class PizzaSize(Base):
    size: Mapped[int] = mapped_column(unique=True)
    pizzas: Mapped[list["Pizza"]] = relationship(
        secondary=pizza_size_association,
        back_populates="sizes",
    )

    def __str__(self) -> str:
        return f"{type(self).__name__}(size={self.size!r})"


class PizzaType(Base):
    type: Mapped[str] = mapped_column(unique=True)
    pizzas: Mapped[list["Pizza"]] = relationship(
        secondary=pizza_type_association,
        back_populates="types",
    )

    def __str__(self) -> str:
        return f"{type(self).__name__}(type={self.type!r})"
