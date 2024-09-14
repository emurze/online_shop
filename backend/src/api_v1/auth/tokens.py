from datetime import timedelta

from api_v1.auth.models import User
from config import config
from shared.jwt import encode_jwt

TOKEN_TYPE_KEY = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt_token(
    token_type: str,
    token_data: dict,
    expire_timedelta: timedelta,
) -> str:
    payload = {
        TOKEN_TYPE_KEY: token_type,
        **token_data,
    }
    return encode_jwt(payload, expire_timedelta)


def create_access_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
    }
    return create_jwt_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(
            minutes=config.auth_jwt.access_token_expire_minutes,
        ),
    )


def create_refresh_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
    }
    return create_jwt_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(
            days=config.auth_jwt.refresh_token_expire_days,
        ),
    )
