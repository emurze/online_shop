import logging
from typing import NoReturn
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.pizzas.exceptions import PizzaNotFoundException
from api_v1.pizzas.models import Pizza
from api_v1.pizzas.schemas import PizzaCreate, PizzaPartialUpdate

lg = logging.getLogger(__name__)


async def get_pizzas(session: AsyncSession) -> list[Pizza]:
    query = select(Pizza).order_by(Pizza.title.asc())
    result = await session.execute(query)
    return list(result.scalars())


async def get_pizza_by_id(
    session: AsyncSession,
    pizza_id: UUID,
    for_update: bool = False,
) -> Pizza:
    query = select(Pizza).filter_by(id=pizza_id)

    if for_update:
        query = query.with_for_update()

    pizza = (await session.execute(query)).scalar_one_or_none()

    if pizza is None:
        raise PizzaNotFoundException()

    return pizza


async def get_latest_pizza(session: AsyncSession) -> Pizza | NoReturn:
    query = select(Pizza).order_by(Pizza.title).limit(1)
    latest_pizza = (await session.execute(query)).scalar_one_or_none()

    if latest_pizza is None:
        raise PizzaNotFoundException()

    return latest_pizza


async def add_pizza(
    session: AsyncSession,
    pizza_id: UUID,
    pizza_dto: PizzaCreate,
) -> None:
    pizza = Pizza(id=pizza_id, **pizza_dto.model_dump())
    session.add(pizza)
    await session.commit()


async def delete_pizza(session: AsyncSession, pizza_id: UUID) -> None:
    command = delete(Pizza).filter_by(id=pizza_id)
    await session.execute(command)
    await session.commit()


async def update_pizza(
    session: AsyncSession,
    pizza: Pizza,
    pizza_dto: PizzaPartialUpdate,
) -> None:
    for name, value in pizza_dto.model_dump(exclude_unset=True).items():
        setattr(pizza, name, value)
    await session.commit()
