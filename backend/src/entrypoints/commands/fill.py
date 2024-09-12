import asyncio
import logging
import uuid
from typing import Optional

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.models import User
from api_v1.pizzas.models import Pizza, PizzaSize, PizzaType, PizzaCategory
from api_v1.profiles.models import Profile
from entrypoints.commands._base import db_command
from entrypoints.commands.clear import clear_db
from shared.hasher import hash_password

lg = logging.getLogger(__name__)


async def create_pizzas(
    session: AsyncSession,
    faker: Faker,
    user_id: uuid.UUID,
    count: int = 25,
) -> None:
    lg.info(f"{count} pizzas created")

    category = PizzaCategory(id=user_id, title="Category 1")
    lg.info(f"Pizza Category added {category.id}")

    types = [
        PizzaType(type="Think"),
        PizzaType(type="Fat"),
        PizzaType(type="Large"),
    ]
    sizes = [PizzaSize(size=40), PizzaSize(size=20)]
    pizzas = [
        Pizza(
            title=f"Pizza {faker.name()}",
            description=f"{faker.text(max_nb_chars=100)}",
            price=faker.pydecimal(
                left_digits=4,
                right_digits=2,
                positive=True,
                min_value=1,
                max_value=1000,
            ),
            category_id=category.id,
            user_id=user_id,
        )
        for _ in range(count)
    ]

    for pizza in pizzas:
        pizza.sizes.union(sizes)
        pizza.types.union(types)

    session.add(category)
    session.add_all(pizzas)


async def create_user(
    session: AsyncSession,
    faker: Faker,
    user_id: Optional[uuid.UUID] = None,
    is_superuser: bool = False,
) -> User:
    lg.info(f"User added {user_id}")
    user = User(
        id=user_id,
        username=faker.user_name(),
        email=faker.email(),
        hashed_password=hash_password("12345678"),
        is_superuser=is_superuser,
    )
    session.add(user)
    return user


async def create_profile(
    session: AsyncSession,
    faker: Faker,
    user_id: uuid.UUID,
) -> Profile:
    lg.info("Profile added to user")
    profile = Profile(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        bio=faker.text(max_nb_chars=100),
        birthday=faker.date(),
        gender=faker.random_element(["male", "female"]),
        user_id=user_id,
    )
    session.add(profile)
    return profile


async def fill_db(session: AsyncSession) -> None:
    await clear_db(session)
    user_id = uuid.uuid4()
    faker = Faker()

    user = await create_user(session, faker, user_id, is_superuser=True)
    profile = await create_profile(session, faker, user_id)
    pizzas = await create_pizzas(session, faker, user_id)

    await session.commit()


if __name__ == "__main__":
    asyncio.run(db_command(fill_db))
