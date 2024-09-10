import uuid
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.pizzas import services
from api_v1.pizzas.exceptions import (
    PizzaNotFoundException,
    PizzaUserOrCategoryNotFoundException,
)
from api_v1.pizzas.schemas import (
    PizzaRead,
    PizzaCreate,
    PizzaPartialUpdate,
    PizzaPageRead,
)
from shared.db import get_session
from shared.schemas import ErrorSchema

router = APIRouter(prefix="/pizzas", tags=["pizzas"])


async def get_pizza_or_404(
    session: AsyncSession,
    pizza_id: UUID,
    for_update: bool = False,
):
    try:
        return await services.get_pizza_by_id(
            session=session,
            pizza_id=pizza_id,
            for_update=for_update,
        )
    except PizzaNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found",
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PizzaPageRead,
)
async def get_pizzas(
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = Query(
        None,
        alias="sort_by",
        description="Format: price:desc, name:asc",
    ),
    filter_by: Optional[str] = Query(
        None,
        alias="filter_by",
        description="Format: title=pizza, description=best pizza",
    ),
    session: AsyncSession = Depends(get_session),
):
    return await services.get_pizzas(
        session,
        page=page,
        limit=limit,
        sort_by=sort_by,
        filter_by=filter_by,
    )


@router.get(
    "/sizes",
    status_code=status.HTTP_200_OK,
    response_model=list[int],
)
async def get_pizza_categories(session: AsyncSession = Depends(get_session)):
    return await services.get_pizza_sizes(session)


@router.get(
    "/types",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
)
async def get_pizza_types(session: AsyncSession = Depends(get_session)):
    return await services.get_pizza_types(session)


@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
)
async def get_pizza_categories(session: AsyncSession = Depends(get_session)):
    return await services.get_pizza_categories(session)


@router.get(
    "/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        }
    },
)
async def get_pizza_by_id(
    pizza_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await get_pizza_or_404(session, pizza_id)


@router.get(
    "/latest",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        }
    },
)
async def get_latest_pizza(db_session: AsyncSession = Depends(get_session)):
    try:
        return await services.get_latest_pizza(db_session)
    except PizzaNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found",
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        },
    },
)
async def create_pizza(
    pizza_dto: PizzaCreate,
    db_session: AsyncSession = Depends(get_session),
):
    try:
        pizza_id = uuid.uuid4()
        await services.add_pizza(db_session, pizza_id, pizza_dto)
        return await services.get_pizza_by_id(db_session, pizza_id)
    except PizzaUserOrCategoryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Category for pizza not found",
        )


@router.patch(
    "/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        }
    },
)
async def update_pizza(
    pizza_id: UUID,
    pizza_dto: PizzaPartialUpdate,
    session: AsyncSession = Depends(get_session),
):
    pizza = await get_pizza_or_404(session, pizza_id, for_update=True)
    await services.update_pizza(session, pizza=pizza, pizza_dto=pizza_dto)
    await session.refresh(pizza)
    return pizza


@router.delete(
    "/{pizza_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_pizza(
    pizza_id: UUID,
    db_session: AsyncSession = Depends(get_session),
):
    await services.delete_pizza(db_session, pizza_id)
