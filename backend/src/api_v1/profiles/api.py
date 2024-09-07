from typing import NoReturn
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.profiles import services
from api_v1.profiles.exceptions import ProfileNotFoundException
from api_v1.profiles.models import Profile
from api_v1.profiles.schemas import ProfileRead
from shared.db import get_session
from shared.schemas import ErrorSchema

router = APIRouter(prefix="/profiles", tags=["profiles"])


async def get_profile_or_404(
    profile_id: UUID,
    session: AsyncSession,
    for_update: bool = False,
) -> Profile | NoReturn:
    try:
        return await services.get_profile_by_id(
            session=session,
            profile_id=profile_id,
            for_update=for_update,
        )
    except ProfileNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ProfileRead],
)
async def get_profiles(session: AsyncSession = Depends(get_session)):
    return await services.get_profiles(session)


@router.get(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Profile not found",
            "model": ErrorSchema,
        }
    },
)
async def get_profile_by_id(
    profile_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await get_profile_or_404(session=session, profile_id=profile_id)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=ProfileRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Profile not found",
            "model": ErrorSchema,
        }
    },
)
async def get_my_profile():  # todo: custom with auth
    return {"detail": "Not Implemented"}
