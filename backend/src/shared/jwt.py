from datetime import datetime, timedelta
from typing import Any

import jwt

from config import config


def encode_jwt(
    payload: dict,
    expire_timedelta: timedelta,
    private_key: str = config.auth_jwt.private_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
) -> str:
    to_encode = payload.copy()
    to_encode["exp"] = datetime.now() + expire_timedelta
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
    jwt_token: str,
    public_key: str = config.auth_jwt.public_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
) -> Any:
    return jwt.decode(jwt_token, public_key, algorithms=[algorithm])
