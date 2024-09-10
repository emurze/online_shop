from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.pizzas.models import PizzaType


async def get_pizzas_types(session: AsyncSession) -> list[str]:
    query = select(PizzaType.type).order_by(PizzaType.type)
    types = await session.execute(query)
    return list(types.scalars())
