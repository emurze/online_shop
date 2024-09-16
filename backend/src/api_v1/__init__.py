from fastapi import APIRouter, Depends
from api_v1.auth.api import router as auth_router
from api_v1.users.api import router as users_router

from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])
router.include_router(auth_router)
router.include_router(users_router)
