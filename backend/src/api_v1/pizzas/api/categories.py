from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.pizzas import services
from api_v1.pizzas.schemas import PizzaCategoryRead
from shared.db import get_session

category_router = APIRouter(prefix="/categories")


@category_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[PizzaCategoryRead],
)
async def get_pizzas_categories(session: AsyncSession = Depends(get_session)):
    return await services.get_pizzas_categories(session)
