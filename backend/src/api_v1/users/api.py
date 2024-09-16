from fastapi import APIRouter

from api_v1.auth.backend import fastapi_users
from api_v1.auth.schemas import UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
