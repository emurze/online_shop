from fastapi import APIRouter

from api_v1.auth.backend import fastapi_users, authentication_backend
from api_v1.auth.schemas import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_auth_router(authentication_backend))
