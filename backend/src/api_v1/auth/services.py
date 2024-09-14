from typing import NoReturn
from uuid import UUID

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.exceptions import (
    UserNameAlwaysExistsException,
    UserEmailAlwaysExistsException,
    UserNotFoundException,
    UserNotActiveException,
    UserPasswordNotVerifiedException,
)
from api_v1.auth.models import User
from api_v1.auth.schemas import UserCreate
from shared.db import cast_any as _
from shared.hasher import verify_password, hash_password


async def authenticate_user_by_sub(
    session: AsyncSession,
    sub: str,
) -> User | NoReturn:
    user = await session.get(User, sub)

    if not user:
        raise UserNotFoundException()

    if not user.is_active:
        raise UserNotActiveException()

    return user


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> User | NoReturn:
    query = select(User).where(_(User.username == username))
    user: User | None = (await session.execute(query)).scalar()

    if not user:
        raise UserNotFoundException()

    if not verify_password(password, user.hashed_password):
        raise UserPasswordNotVerifiedException()

    if not user.is_active:
        raise UserNotActiveException()

    return user


async def register(
    session: AsyncSession,
    user_dto: UserCreate,
    user_id: UUID,
) -> None:
    query = select(exists().where(_(User.username == user_dto.username)))
    if (await session.execute(query)).scalar():
        raise UserNameAlwaysExistsException()

    query = select(exists().where(_(User.email == user_dto.email)))
    if (await session.execute(query)).scalar():
        raise UserEmailAlwaysExistsException()

    user = User(
        id=user_id,
        hashed_password=hash_password(user_dto.password),
        **user_dto.model_dump(exclude={"password"}),
    )
    session.add(user)
    await session.commit()


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    user: User | None = await session.get(User, user_id)

    if not user:
        raise UserNotFoundException()

    return user
