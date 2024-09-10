from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.pizzas.models import PizzaSize, Pizza


async def get_pizzas_sizes(session: AsyncSession) -> list[int]:
    query = select(PizzaSize.size).order_by(PizzaSize.size)
    categories = await session.execute(query)
    return list(categories.scalars())


async def add_size_to_pizza(
    pizza_id: UUID,
    size: int,
    session: AsyncSession,
):
    size = PizzaSize(size=size)
    session.add(size)
    pizza = await session.get(
        Pizza,
        pizza_id,
        options=[selectinload(Pizza.sizes)],
        with_for_update=True,
    )
    pizza.sizes.append(size)
    await session.commit()
