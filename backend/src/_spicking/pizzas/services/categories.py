from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from _spicking.pizzas.models import PizzaCategory


async def get_pizzas_categories(session: AsyncSession) -> list[PizzaCategory]:
    query = select(PizzaCategory).order_by(PizzaCategory.title)
    categories = await session.execute(query)
    return list(categories.scalars())
