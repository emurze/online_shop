from typing import NoReturn
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profiles.exceptions import ProfileNotFoundException
from api_v1.profiles.models import Profile


async def get_profiles(session: AsyncSession) -> list[Profile]:
    query = select(Profile).order_by(Profile.updated_at.desc())
    result = await session.execute(query)
    return list(result.scalars())


async def get_profile_by_id(
    session: AsyncSession,
    profile_id: UUID,
    for_update: bool = False,
) -> Profile | NoReturn:
    query = select(Profile).filter_by(id=profile_id)

    if for_update:
        query = query.with_for_update()

    profile = (await session.execute(query)).scalar_one_or_none()

    if profile is None:
        raise ProfileNotFoundException()

    return profile
