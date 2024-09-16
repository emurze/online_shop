# import uuid
# from typing import Annotated
#
# from fastapi import APIRouter, Depends, HTTPException, Cookie
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status
# from starlette.responses import Response
#
# from shared.db import get_session
# from shared.schemas import ErrorSchema
# from . import services
# from .exceptions import (
#     UserEmailAlwaysExistsException,
#     UserNameAlwaysExistsException,
#     UserNotAuthenticatedException,
# )
# from .models import User
# from .schemas import UserCreate, UserRead, UserLogin
#
# router = APIRouter(prefix="/jwt_auth", tags=["jwt_auth"])
# COOKIE_SESSION_ID_KEY = "app-session-id"
#
#
# @router.post(
#     "/register",
#     response_model=UserRead,
#     responses={
#         status.HTTP_409_CONFLICT: {"model": ErrorSchema},
#     },
# )
# async def register(
#     dto: UserCreate,
#     session: AsyncSession = Depends(get_session),
# ):
#     try:
#         user_id = uuid.uuid4()
#         await services.register(session, dto, user_id)
#         return await services.get_user_by_id(session, user_id)
#
#     except UserNameAlwaysExistsException:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Username already exists",
#         )
#
#     except UserEmailAlwaysExistsException:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Email already exists",
#         )
#
#
# async def get_authenticated_user(
#     session_id: Annotated[
#         str | None, Cookie(alias=COOKIE_SESSION_ID_KEY)
#     ] = None,
#     session: AsyncSession = Depends(get_session),
# ) -> User:
#     if session_id is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#
#     user = await services.authenticate_by_session_id(session, session_id)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#
#     return user
#
#
# @router.post(
#     "/login",
#     response_model=dict,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
#     },
# )
# async def login(
#     dto: UserLogin,
#     response: Response,
#     session: AsyncSession = Depends(get_session),
# ):
#     try:
#         session_id = uuid.uuid4()
#         user = await services.authenticate_by_username(session, dto.username)
#         await services.create_session(session, session_id, user.id)
#
#         response.set_cookie(COOKIE_SESSION_ID_KEY, str(session_id))
#         return {"message": f"User {user.username} has successfully logged in"}
#
#     except UserNotAuthenticatedException:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#
#
# @router.post(
#     "/logout",
#     response_model=dict,
# )
# async def logout(
#     response: Response,
#     session_id: Annotated[
#         str | None, Cookie(alias=COOKIE_SESSION_ID_KEY)
#     ] = None,
#     user: User = Depends(get_authenticated_user),
#     session: AsyncSession = Depends(get_session),
# ):
#     await services.delete_session(session, session_id)
#     response.delete_cookie(COOKIE_SESSION_ID_KEY)
#     return {"message": f"User {user.username} has been logged out"}
#
#
# @router.get("/hello-world")
# async def get_hello_world(
#     user: User = Depends(get_authenticated_user),
# ) -> dict:
#     return {"message": f"hello world {user.username}"}
