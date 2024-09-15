from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.manager import UserManager
from api_v1.auth.models import User, AccessToken
from shared.db import get_session


async def get_user_db(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[SQLAlchemyUserDatabase]:
    yield User.get_db(session=session)


async def get_access_token_db(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[SQLAlchemyAccessTokenDatabase]:
    yield AccessToken.get_db(session=session)


async def get_user_manager(
    user_db: Annotated[
        SQLAlchemyUserDatabase,
        Depends(get_user_db),
    ]
):
    yield UserManager(user_db)
