from typing import NoReturn

from fastapi import HTTPException, Depends
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
    HTTPAuthorizationCredentials,
)
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth import services
from api_v1.auth.exceptions import (
    UserNotFoundException,
    UserNotActiveException,
)
from api_v1.auth.models import User
from api_v1.auth.tokens import (
    TOKEN_TYPE_KEY,
    REFRESH_TOKEN_TYPE,
    ACCESS_TOKEN_TYPE,
)
from shared.db import get_session
from shared.jwt import decode_jwt

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def decode_token(any_token: str) -> dict:
    try:
        return decode_jwt(any_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except (InvalidTokenError, UserNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )


async def get_user_by_token_sub(
    session: AsyncSession,
    token: str,
    required_token_type: str,
) -> User | NoReturn:
    try:
        token_payload = decode_token(token)
        if token_payload[TOKEN_TYPE_KEY] != required_token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token is not {required_token_type!r}",
            )
        return await services.authenticate_user_by_sub(
            session, token_payload["sub"]
        )
    except UserNotActiveException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active",
        )


async def get_user_by_refresh_token(
    session: AsyncSession = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User | NoReturn:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await get_user_by_token_sub(
        session, token.credentials, REFRESH_TOKEN_TYPE
    )


async def get_user_by_access_token(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User | NoReturn:
    return await get_user_by_token_sub(session, token, ACCESS_TOKEN_TYPE)
