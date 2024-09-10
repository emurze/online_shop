from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.pizzas import services
from shared.db import get_session

type_router = APIRouter(prefix="/types")


@type_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
)
async def get_pizzas_types(session: AsyncSession = Depends(get_session)):
    return await services.get_pizzas_types(session)
