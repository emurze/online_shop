from fastapi import APIRouter
from api_v1.pizzas.api import router as pizzas_router
from api_v1.users.api import router as users_router

router = APIRouter()
router.include_router(pizzas_router)
router.include_router(users_router)
