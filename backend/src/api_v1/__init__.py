from fastapi import APIRouter
from api_v1.auth.api import router as auth_router

router = APIRouter()
router.include_router(auth_router)
