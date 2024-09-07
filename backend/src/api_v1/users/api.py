import uuid
from typing import NoReturn
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.users import services
from api_v1.users.exceptions import UserNotFoundException
from api_v1.users.models import User
from api_v1.users.schemas import UserRead
from shared.db import get_session
from shared.schemas import ErrorSchema

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_or_404(
    user_id: UUID,
    session: AsyncSession,
    for_update: bool = False,
) -> User | NoReturn:
    try:
        return await services.get_user_by_id(
            session=session,
            user_id=user_id,
            for_update=for_update,
        )
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
async def get_users(session: AsyncSession = Depends(get_session)):
    return await services.get_users(session)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorSchema,
        }
    },
)
async def get_my_user():  # todo: custom with auth
    return {"detail": "Not Implemented"}


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorSchema,
        }
    },
)
async def get_user_by_id(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await get_user_or_404(session=session, user_id=user_id)
