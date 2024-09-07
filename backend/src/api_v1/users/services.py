from typing import NoReturn
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.exceptions import UserNotFoundException
from api_v1.users.models import User


async def get_users(session: AsyncSession) -> list[User]:
    query = select(User).order_by(User.updated_at.desc())  # todo: logged_in
    result = await session.execute(query)
    return list(result.scalars())


async def get_user_by_id(
    session: AsyncSession,
    user_id: UUID,
    for_update: bool = False,
) -> User | NoReturn:
    query = select(User).filter_by(id=user_id)  # todo: joined + auth

    if for_update:
        query = query.with_for_update()

    user = (await session.execute(query)).scalar_one_or_none()

    if user is None:
        raise UserNotFoundException()

    return user
