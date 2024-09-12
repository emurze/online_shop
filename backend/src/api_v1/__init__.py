from fastapi import APIRouter
from api_v1.pizzas.api import router as pizzas_router
from api_v1.profiles.api import router as profiles_router
from api_v1.auth.api import router as auth_router
from api_v1.demo_auth.api import router as demo_auth_router

router = APIRouter()
# router.include_router(auth_router)
router.include_router(demo_auth_router)
router.include_router(pizzas_router)
router.include_router(profiles_router)
