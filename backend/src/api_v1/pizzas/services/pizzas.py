import math
from typing import NoReturn, Optional
from uuid import UUID

from sqlalchemy import delete, select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.auth.models import User
from api_v1.pizzas.exceptions import (
    PizzaNotFoundException,
    PizzaUserNotFoundException,
    PizzaCategoryNotFoundException,
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


def map_pizza_to_dict(pizza: Pizza) -> dict:
    return {
        **pizza.as_dict(exclude={"sizes"}),
        "sizes": [size.size for size in pizza.sizes],
        "types": [pizza_type.type for pizza_type in pizza.types],
    }


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
    content = [map_pizza_to_dict(pizza) for pizza in result.scalars()]

    return {
        "page_number": page,
        "page_size": limit,
        "total_pages": total_pages,
        "total_record": total_record,
        "content": content,
    }


async def get_pizza_by_id(
    session: AsyncSession,
    pizza_id: UUID,
    for_update: bool = False,
) -> Pizza | dict | NoReturn:
    pizza: Pizza | None = await session.get(
        Pizza,
        pizza_id,
        options=get_options(),
        with_for_update=for_update,
    )

    if pizza is None:
        raise PizzaNotFoundException()

    if for_update:
        return pizza

    return map_pizza_to_dict(pizza)


async def get_latest_pizza(session: AsyncSession) -> dict | NoReturn:
    query = (
        select(Pizza).options(*get_options()).order_by(Pizza.title).limit(1)
    )
    latest_pizza = (await session.execute(query)).scalar_one_or_none()

    if latest_pizza is None:
        raise PizzaNotFoundException()

    return map_pizza_to_dict(latest_pizza)


async def add_pizza(
    session: AsyncSession,
    pizza_id: UUID,
    pizza_dto: PizzaCreate,
) -> None:
    # Check user_id
    if pizza_dto.user_id:
        user = await session.get(User, pizza_dto.user_id)
        if not user:
            raise PizzaUserNotFoundException()

    # Check category_id
    if pizza_dto.category_id:
        category = await session.get(PizzaCategory, pizza_dto.category_id)
        if not category:
            raise PizzaCategoryNotFoundException()

    # Find missing sizes
    query1 = select(PizzaSize).where(PizzaSize.size.in_(pizza_dto.sizes))
    existing_sizes = list((await session.execute(query1)).scalars())
    existing_size_values = {size.size for size in existing_sizes}
    missing_size_values = set(pizza_dto.sizes) - existing_size_values

    # Create missing sizes
    new_sizes = [PizzaSize(size=size) for size in missing_size_values]
    session.add_all(new_sizes)
    sizes = existing_sizes + new_sizes

    # Find missing types
    query2 = select(PizzaType).where(PizzaType.type.in_(pizza_dto.types))
    existing_types = list((await session.execute(query2)).scalars())
    existing_type_values = {type_.type for type_ in existing_types}
    missing_type_values = set(pizza_dto.types) - existing_type_values

    # Create missing types
    new_types = [PizzaType(type=type_) for type_ in missing_type_values]
    session.add_all(new_types)
    types = existing_types + new_types

    # Create pizza
    pizza = Pizza(
        id=pizza_id,
        sizes=sizes,
        types=types,
        **pizza_dto.model_dump(
            exclude={"sizes", "types"},
        ),
    )
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
    print(pizza)
    for name, value in pizza_dto.model_dump(exclude_unset=True).items():
        setattr(pizza, name, value)
    await session.commit()
