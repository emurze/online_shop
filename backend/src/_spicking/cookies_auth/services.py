# from typing import TypeAlias, NoReturn
# from uuid import UUID
#
# from sqlalchemy import select, exists, delete
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from api_v1.auth.exceptions import (
#     UserNotFoundException,
#     UserEmailAlwaysExistsException,
#     UserNameAlwaysExistsException,
#     UserNotAuthenticatedException,
# )
# from api_v1.auth.models import User, Session
# from api_v1.auth.schemas import UserCreate
# from shared.db import cast_any as _
# from shared.hasher import hash_password
#
# UserId: TypeAlias = UUID
# SessionId: TypeAlias = UUID
#
#
# async def register(
#     session: AsyncSession,
#     user_dto: UserCreate,
#     user_id: UUID,
# ) -> None:
#     query = select(exists().where(_(User.username == user_dto.username)))
#     if (await session.execute(query)).scalar():
#         raise UserNameAlwaysExistsException()
#
#     query = select(exists().where(_(User.email == user_dto.email)))
#     if (await session.execute(query)).scalar():
#         raise UserEmailAlwaysExistsException()
#
#     user = User(
#         id=user_id,
#         hashed_password=hash_password(user_dto.password),
#         **user_dto.model_dump(exclude={"password"}),
#     )
#     session.add(user)
#     await session.commit()
#
#
# async def authenticate_by_username(
#     session: AsyncSession,
#     username: str,
# ) -> User | NoReturn:
#     query = select(User).where(_(User.username == username))
#     if user := (await session.execute(query)).scalar():
#         return user
#     else:
#         raise UserNotAuthenticatedException()
#
#
# async def authenticate_by_session_id(
#     session: AsyncSession,
#     session_id: str,
# ) -> User | None:
#     query = (
#         select(User)
#         .join(Session, Session.user_id == User.id)
#         .where(_(Session.id == session_id))
#     )
#     return (await session.execute(query)).scalar()
#
#
# async def create_session(
#     session: AsyncSession,
#     session_id: UUID,
#     user_id: UUID,
# ) -> None:
#     new_session = Session(id=session_id, user_id=user_id)
#     session.add(new_session)
#     await session.commit()
#
#
# async def delete_session(
#     session: AsyncSession,
#     session_id: str,
# ) -> None:
#     command = delete(Session).where(_(Session.id == session_id))
#     await session.execute(command)
#     await session.commit()
#
#
# async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User:
#     user: User | None = await session.get(User, user_id)
#
#     if user is None:
#         raise UserNotFoundException()
#
#     return user
