# from typing import Optional
#
# from pydantic import EmailStr
#
# from shared.schemas import Schema
#
#
# class TokenRead(Schema):
#     access_token: str
#     refresh_token: str | None = None
#     token_type: str = "Bearer"
#
#
# class UserCreate(Schema):
#     username: str
#     password: str
#     email: EmailStr = None
#
#
# class UserRead(Schema):
#     username: Optional[str] = None
#     email: Optional[str] = None
#     is_active: Optional[bool] = None
#     is_superuser: Optional[bool] = None
