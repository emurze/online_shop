import asyncio
import uuid

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.models import User
from api_v1.pizzas.models import Pizza
from api_v1.profiles.models import Profile
from config import AppConfig, get_db_dsn_for_environment
from entrypoints.clear_db import clear_db
from shared.db import DatabaseAdapter, hash_password


async def fill_db(session: AsyncSession) -> None:
    await clear_db(session)
    faker = Faker()
    session.add_all(
        [
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
            )
            for _ in range(100)
        ]
    )
    user_id = uuid.uuid4()
    session.add(
        User(
            id=user_id,
            username=faker.user_name(),
            email=faker.email(),
            hashed_password=hash_password("12345678"),
            is_superuser=True,
        ),
    )
    session.add(
        Profile(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            bio=faker.text(max_nb_chars=100),
            birthday=faker.date(),
            gender=faker.random_element(["male", "female"]),
            user_id=user_id,
        )
    )
    await session.commit()


async def main(config=AppConfig()) -> None:
    db_dsn = get_db_dsn_for_environment(config)
    db_adapter = DatabaseAdapter(db_dsn=db_dsn, echo=True)

    async with db_adapter.session_factory() as session:
        await fill_db(session)


if __name__ == "__main__":
    asyncio.run(main())
