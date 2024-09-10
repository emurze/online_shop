import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from api_v1.auth.models import User
from api_v1.pizzas.models import Pizza
from api_v1.profiles.models import Profile
from entrypoints.commands._base import db_command
from shared.db import cast_any as _


async def get_users_with_posts(session: AsyncSession) -> None:
    query = select(User).options(
        joinedload(User.profile),
        selectinload(User.pizzas),
    )
    users = await session.scalars(query)

    for user in users.all():
        print(user, user.pizzas)


async def get_posts_with_users(session: AsyncSession) -> None:
    query = select(Pizza).options(joinedload(Pizza.user)).order_by(Pizza.id)
    pizzas = await session.scalars(query)

    for pizza in pizzas.all():
        print(pizza, pizza.user)


async def get_profile_with_user_with_posts(session: AsyncSession) -> None:
    query = (
        select(Profile)
        .options(joinedload(Profile.user).selectinload(User.pizzas))
        .where(_(User.username == "petersamber"))
        .order_by(User.id)
    )
    profiles = await session.scalars(query)

    for profile in profiles.all():
        print(profile.user)
        for pizza in profile.user.pizzas:
            print(f"- {pizza.title}")


async def run_script(session: AsyncSession) -> None:
    await get_profile_with_user_with_posts(session)


if __name__ == "__main__":
    asyncio.run(db_command(run_script))
