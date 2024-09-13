from typing import Optional
from uuid import UUID

from shared.schemas import Schema


class UserCreate(Schema):
    username: str
    password: str
    email: str


class UserLogin(Schema):
    username: str
    password: str


class UserRead(Schema):
    id: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
