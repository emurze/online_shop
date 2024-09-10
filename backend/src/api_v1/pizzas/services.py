import math
from typing import NoReturn, Optional
from uuid import UUID

from sqlalchemy import delete, select, func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.pizzas.exceptions import (
    PizzaNotFoundException,
    PizzaUserOrCategoryNotFoundException,
)
from api_v1.pizzas.models import Pizza, PizzaCategory, PizzaSize, PizzaType
from api_v1.pizzas.schemas import (
    PizzaCreate,
    PizzaPartialUpdate,
)
from shared.db import convert_filter_by, convert_sort_by


def get_options() -> list:
    return [
        selectinload(Pizza.sizes),
        selectinload(Pizza.types),
    ]


async def get_pizzas(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = None,
    filter_by: Optional[str] = None,
) -> dict:
    query = select(Pizza).options(*get_options())

    if filter_by is not None and filter_by != "all":
        # filter modes and_, or_
        query = query.filter(or_(*convert_filter_by(Pizza, filter_by)))

    if sort_by is not None and sort_by != "null":
        query = query.order_by(*convert_sort_by(Pizza, sort_by))

    # pagination
    offset_page = page - 1
    query = query.offset(offset_page * limit).limit(limit)

    # total record
    count_query = select(func.count("*")).select_from(Pizza)
    total_record = (await session.execute(count_query)).scalar() or 0

    # total page
    total_pages = math.ceil(total_record / limit)

    # Fetch result
    result = await session.execute(query)
    result = result.scalars()
    result = [
        {
            **pizza.as_dict(exclude={"sizes"}),
            "sizes": [size.size for size in pizza.sizes],
            "types": [pizza_type.type for pizza_type in pizza.types],
        }
        for pizza in result.all()
    ]

    return {
        "page_number": page,
        "page_size": limit,
        "total_pages": total_pages,
        "total_record": total_record,
        "content": result,
    }


async def get_pizza_by_id(
    session: AsyncSession,
    pizza_id: UUID,
    for_update: bool = False,
) -> Pizza:
    pizza: Pizza | None = await session.get(
        Pizza,
        pizza_id,
        options=get_options(),
        with_for_update=for_update,
    )

    if pizza is None:
        raise PizzaNotFoundException()

    return pizza


async def get_pizza_types(session: AsyncSession) -> list[str]:
    query = select(PizzaType.type).order_by(PizzaType.type)
    types = await session.execute(query)
    return list(types.scalars())


async def get_pizza_sizes(session: AsyncSession) -> list[int]:
    query = select(PizzaSize.size).order_by(PizzaSize.size)
    categories = await session.execute(query)
    return list(categories.scalars())


async def get_pizza_categories(session: AsyncSession) -> list[str]:
    query = select(PizzaCategory.title).order_by(PizzaCategory.title)
    categories = await session.execute(query)
    return list(categories.scalars())


async def get_latest_pizza(session: AsyncSession) -> Pizza | NoReturn:
    query = (
        select(Pizza).options(*get_options()).order_by(Pizza.title).limit(1)
    )
    latest_pizza = (await session.execute(query)).scalar_one_or_none()

    if latest_pizza is None:
        raise PizzaNotFoundException()

    return latest_pizza


async def add_pizza(
    session: AsyncSession,
    pizza_id: UUID,
    pizza_dto: PizzaCreate,
) -> None:
    try:
        pizza = Pizza(id=pizza_id, **pizza_dto.model_dump())
        session.add(pizza)
        await session.commit()
    except IntegrityError:
        raise PizzaUserOrCategoryNotFoundException()


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
