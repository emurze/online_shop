import uuid
from typing import Optional, TYPE_CHECKING

import logging
from fastapi_users import BaseUserManager, UUIDIDMixin

from api_v1.auth.models import User
from config import app_config as conf

if TYPE_CHECKING:
    from starlette.requests import Request


lg = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = conf.access_token.reset_password_token_secret
    verification_token_secret = conf.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        lg.info(f"User {user.id} has registered.")

    # async def on_after_forgot_password(
    #     self,
    #     user: User,
    #     token: str,
    #     request: Optional["Request"] = None,
    # ):
    #     lg.info(
    #         f"User {user.id} has forgot their password. Reset token: {token}"
    #     )
    #
    # async def on_after_request_verify(
    #     self,
    #     user: User,
    #     token: str,
    #     request: Optional["Request"] = None,
    # ):
    #     lg.info(
    #         f"Verification requested for user {user.id}. "
    #         f"Verification token: {token}"
    #     )
