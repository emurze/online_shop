import uuid
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication.strategy import DatabaseStrategy

from api_v1.auth.utils import get_access_token_db, get_user_manager
from api_v1.auth.models import User
from config import app_config

if TYPE_CHECKING:
    from api_v1.auth.models import AccessToken
    from fastapi_users.authentication.strategy import AccessTokenDatabase

transport = BearerTransport(tokenUrl="/api/v1/auth/login")


def get_database_strategy(
    access_tokens_db: Annotated[
        "AccessTokenDatabase[AccessToken]",
        Depends(get_access_token_db),
    ]
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_tokens_db,
        lifetime_seconds=app_config.access_token.lifetime_seconds,
    )


authentication_backend = AuthenticationBackend(
    name="access-token",
    transport=transport,
    get_strategy=get_database_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager=get_user_manager,
    auth_backends=[authentication_backend],
)
