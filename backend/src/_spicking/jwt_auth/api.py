# import uuid
#
# from fastapi import APIRouter, Depends, HTTPException, Form
#
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status
#
# from _spicking.jwt_auth import services
# from _spicking.jwt_auth.dependencies import (
#     get_user_by_refresh_token,
#     get_user_by_access_token,
# )
# from _spicking.jwt_auth.exceptions import (
#     UserNameAlwaysExistsException,
#     UserEmailAlwaysExistsException,
#     UserNotFoundException,
#     UserPasswordNotVerifiedException,
#     UserNotActiveException,
# )
# from _spicking.jwt_auth.models import User
# from _spicking.jwt_auth.schemas import (
#     UserCreate,
#     UserRead,
#     TokenRead,
# )
# from _spicking.jwt_auth.tokens import (
#     create_access_token,
#     create_refresh_token,
# )
# from shared.db import get_session
# from shared.schemas import ErrorSchema
#
# router = APIRouter(
#     prefix="/jwt_auth",
#     tags=["jwt_auth"],
# )
#
#
# @router.post(
#     "/register",
#     status_code=status.HTTP_201_CREATED,
#     response_model=UserRead,
#     responses={
#         status.HTTP_409_CONFLICT: {"model": ErrorSchema},
#     },
# )
# async def register(
#     user_dto: UserCreate,
#     session: AsyncSession = Depends(get_session),
# ):
#     try:
#         user_id = uuid.uuid4()
#         await services.register(session, user_dto, user_id)
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
#     return await services.get_user_by_id(session, user_id)
#
#
# @router.post(
#     "/login",
#     status_code=status.HTTP_200_OK,
#     response_model=TokenRead,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
#         status.HTTP_403_FORBIDDEN: {"model": ErrorSchema},
#     },
# )
# async def login(
#     username: str = Form(),
#     password: str = Form(),
#     session: AsyncSession = Depends(get_session),
# ):
#     try:
#         user = await services.authenticate_user(session, username, password)
#
#     except (UserNotFoundException, UserPasswordNotVerifiedException):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )
#
#     except UserNotActiveException:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User is not active",
#         )
#
#     access_token = create_access_token(user)
#     refresh_token = create_refresh_token(user)
#     return TokenRead(
#         access_token=access_token,
#         refresh_token=refresh_token,
#     )
#
#
# @router.post(
#     "/refresh",
#     status_code=status.HTTP_200_OK,
#     response_model=TokenRead,
#     response_model_exclude_none=True,
# )
# async def refresh(user: User = Depends(get_user_by_refresh_token)):
#     access_token = create_access_token(user)
#     return TokenRead(
#         access_token=access_token,
#     )
#
#
# @router.get(
#     "/users/me",
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
#         status.HTTP_403_FORBIDDEN: {"model": ErrorSchema},
#     },
# )
# async def get_user_me(user: User = Depends(get_user_by_access_token)):
#     return {
#         "username": user.username,
#         "email": user.email,
#     }
